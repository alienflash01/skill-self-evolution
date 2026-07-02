"""CCBackend — real Claude Code replay backend for the sleep engine.

Uses `claude -p` (headless mode) to re-attempt mined tasks under a given
(skill, memory) configuration. Judging is heuristic-based:
- exact match for tasks with reference answers
- outcome-derived for tasks with success/fail labels
- keyword overlap for soft scores
"""
from __future__ import annotations

import json
import re
import subprocess
from typing import List, Tuple

from sleep.replay import Backend, _normalize, _keyword_soft
from sleep.models import EditRecord, ReplayResult, TaskRecord

_REFLECT_PROMPT = """You are analyzing failed tasks from an AI coding agent's recent sessions.
The agent tried these tasks but failed. Propose BOUNDED edits to the skill/memory
documents so the agent won't repeat the same mistakes.

Rules:
- Output ONLY a JSON array of edit objects
- Each edit: {{"target":"skill"|"memory", "op":"add", "content":"<rule text>", "rationale":"<why>"}}
- Maximum {budget} edits
- Be concise and general (not tied to specific files or paths)
- If no useful edits can be extracted, output []

Current skill document:
{skill}

Current memory document:
{memory}

Failed tasks ({fail_count}):
{failures_text}

Successful tasks ({success_count}):
{successes_text}

Proposed edits (JSON array):"""


def _strip_code_fence(text: str) -> str:
    """Remove markdown code fences (```json ... ``` or ``` ... ```) from text."""
    import re
    # Match ```json\n...\n``` or ```\n...\n```
    fence_pattern = re.compile(r"^```(?:json)?\s*\n?(.*?)\n?```\s*$", re.DOTALL)
    m = fence_pattern.match(text.strip())
    if m:
        return m.group(1).strip()
    # Also strip trailing ``` if present without opening
    text = text.strip()
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0].strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
    return text


class CCBackend(Backend):
    """Replay backend that calls `claude -p` for real task execution."""

    name = "cc"

    def __init__(self, model: str = "", claude_path: str = "claude",
                 timeout: int = 120):
        self.model = model
        self.claude_path = claude_path
        self.timeout = timeout

    # ── attempt: re-run a task with current skill+memory ────────────────────

    def attempt(self, task: TaskRecord, skill: str, memory: str) -> str:
        """Call claude -p to re-attempt the task. Returns response text."""
        prompt_parts = []
        if skill and skill.strip():
            prompt_parts.append(f"# Skill Instructions\n{skill.strip()}")
        if memory and memory.strip():
            prompt_parts.append(f"# Memory\n{memory.strip()}")
        prompt_parts.append(f"# Task\n{task.intent}")
        if task.context_excerpt:
            prompt_parts.append(f"# Context\n{task.context_excerpt}")

        full_prompt = "\n\n".join(prompt_parts)

        cmd = [self.claude_path, "-p", full_prompt, "--output-format", "text"]
        if self.model:
            cmd.extend(["--model", self.model])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            return result.stdout.strip() if result.returncode == 0 else ""
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return ""

    # ── judge: score the response ───────────────────────────────────────────

    def judge(self, task: TaskRecord, response: str) -> Tuple[float, float, str]:
        """Score the response. Returns (hard, soft, rationale)."""
        # Exact match
        if task.reference_kind == "exact" and task.reference:
            hard = 1.0 if _normalize(task.reference) in _normalize(response) else 0.0
            soft = max(hard, _keyword_soft(task.reference, response))
            return hard, soft, f"exact={'match' if hard else 'mismatch'}"

        # Outcome-derived
        outcome_scores = {"success": 1.0, "mixed": 0.5, "unknown": 0.5, "fail": 0.0}
        hard = outcome_scores.get(task.outcome, 0.5)
        soft = hard

        # Try keyword overlap with attempted solution for soft score
        if task.attempted_solution:
            soft = max(soft, _keyword_soft(task.attempted_solution, response))

        return hard, soft, f"outcome={task.outcome}"

    # ── reflect: propose edits from failures ────────────────────────────────

    def reflect(
        self,
        failures: List[Tuple[TaskRecord, ReplayResult]],
        successes: List[Tuple[TaskRecord, ReplayResult]],
        skill: str,
        memory: str,
        *,
        edit_budget: int = 4,
    ) -> List[EditRecord]:
        """Call claude to analyze failures and propose skill/memory edits."""
        if not failures:
            return []

        # Build failures summary
        fail_lines = []
        for task, result in failures[:10]:
            fail_lines.append(
                f"- Task: {task.intent[:200]}\n"
                f"  Reason: {result.fail_reason[:150]}\n"
                f"  Response: {result.response[:150]}"
            )

        success_lines = []
        for task, result in successes[:5]:
            success_lines.append(f"- Task: {task.intent[:200]}")

        prompt = _REFLECT_PROMPT.format(
            budget=edit_budget,
            skill=skill[:1000],
            memory=memory[:1000],
            fail_count=len(failures),
            failures_text="\n".join(fail_lines),
            success_count=len(successes),
            successes_text="\n".join(success_lines),
        )

        cmd = [self.claude_path, "-p", prompt, "--output-format", "text"]
        if self.model:
            cmd.extend(["--model", self.model])

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=self.timeout,
            )
            raw = result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return []

        # Strip markdown code fences before JSON parsing
        cleaned = _strip_code_fence(raw)

        # Parse JSON array of edits
        try:
            edits_data = json.loads(cleaned)
        except (json.JSONDecodeError, ValueError):
            return []

        edits: List[EditRecord] = []
        for item in edits_data[:edit_budget]:
            if not isinstance(item, dict):
                continue
            edits.append(EditRecord(
                target=item.get("target", "skill"),
                op=item.get("op", "add"),
                content=item.get("content", ""),
                rationale=item.get("rationale", ""),
            ))

        return edits

    def tokens_used(self) -> int:
        return 0  # CC CLI doesn't expose token counts in text mode
