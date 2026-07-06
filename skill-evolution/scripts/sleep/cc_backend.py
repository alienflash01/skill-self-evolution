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
Below, each failed task is paired with a comparable SUCCESSFUL task so you can see
exactly WHAT went wrong by contrast. Your goal is to find the meaningful differences
between failed and successful approaches, then distill them into concrete rules.

## Comparison Pairs (failure vs success)
{comparison_pairs}

## Current skill document
{skill}

## Current memory document
{memory}

## Instructions
- For each pair, identify the SPECIFIC behavioral difference between the failed and
  the successful response. Do NOT propose vague rules like "be careful" or "keep it concise".
- Each rule must be a concrete, actionable instruction that, if followed, would have
  changed the failed response to look more like the successful one.
- Focus on transferable patterns (formatting, process, verification, structure) rather
  than task-specific details.

Rules:
- Output ONLY a JSON array of edit objects
- Each edit: {{"target":"skill"|"memory", "op":"add", "content":"<rule text>", "rationale":"<why>"}}
- Maximum {budget} edits
- If no useful differences can be extracted, output []

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


# ── exit-code judging helpers ──────────────────────────────────────────────

def _judge_exit_code(task: TaskRecord, response: str) -> Tuple[float | None, float, str]:
    """Judge based on exit code.

    Returns (hard, soft, rationale).  If ``task.exit_code`` is *None*
    (not available), returns ``(None, ...)`` so the caller can fall back
    to outcome-based judging.
    """
    if task.exit_code is None:
        return None, 0.0, "no exit_code"

    if task.exit_code == 0:
        return 1.0, 1.0, "exit_code=0 (success)"

    return 0.0, 0.0, f"exit_code={task.exit_code} (failure)"


def _judge_outcome(task: TaskRecord, response: str) -> Tuple[float, float, str]:
    """Outcome-derived scoring (the pre-existing default path)."""
    outcome_scores = {"success": 1.0, "mixed": 0.5, "unknown": 0.5, "fail": 0.0}
    hard = outcome_scores.get(task.outcome, 0.5)
    soft = hard

    # Try keyword overlap with attempted solution for soft score
    if task.attempted_solution:
        soft = max(soft, _keyword_soft(task.attempted_solution, response))

    return hard, soft, f"outcome={task.outcome}"


class ExitCodeJudge:
    """Standalone exit-code judge.

    Useful for pipelines that want to score purely on exit codes without
    instantiating a full CCBackend (which carries claude_path / timeout).

    If the task has an exit_code, it is used:
      - exit 0  → hard 1.0
      - exit !=0 → hard 0.0
    If the task has no exit_code (None), it falls back to outcome-based
    scoring.
    """

    def judge(self, task: TaskRecord, response: str) -> Tuple[float, float, str]:
        hard, soft, rationale = _judge_exit_code(task, response)
        if hard is not None:
            return hard, soft, rationale
        return _judge_outcome(task, response)


class CCBackend(Backend):
    """Replay backend that calls `claude -p` for real task execution."""

    name = "cc"

    def __init__(self, model: str = "", reflect_model: str = "",
                 claude_path: str = "claude", timeout: int = 120):
        self.model = model
        self.reflect_model = reflect_model or model
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
        """Score the response. Returns (hard, soft, rationale).

        Priority:
        1. exit_code — if task.reference_kind == 'exit_code' and exit_code is set
        2. exact     — if task.reference_kind == 'exact' and reference is set
        3. outcome   — fallback to outcome-derived score
        """
        # Exit-code judging (highest priority)
        if task.reference_kind == "exit_code":
            hard, soft, rationale = _judge_exit_code(task, response)
            if hard is not None:
                return hard, soft, rationale
            # No exit_code available — fall through to outcome

        # Exact match
        if task.reference_kind == "exact" and task.reference:
            hard = 1.0 if _normalize(task.reference) in _normalize(response) else 0.0
            soft = max(hard, _keyword_soft(task.reference, response))
            return hard, soft, f"exact={'match' if hard else 'mismatch'}"

        # Outcome-derived
        return _judge_outcome(task, response)

    # ── reflect: propose edits from failures ────────────────────────────────

    @staticmethod
    def _most_similar_success(
        task: TaskRecord,
        successes: List[Tuple[TaskRecord, ReplayResult]],
    ) -> Tuple[TaskRecord, ReplayResult] | None:
        """Pick the success task most similar to *task* (by intent keyword overlap).

        Falls back to the first success if no overlap is found.
        """
        if not successes:
            return None

        def _tokens(s: str) -> set:
            return {t for t in (s or "").lower().split() if len(t) > 2}

        task_tokens = _tokens(task.intent)
        best, best_score = successes[0], 0
        for s_task, s_result in successes:
            overlap = len(task_tokens & _tokens(s_task.intent))
            if overlap > best_score:
                best, best_score = (s_task, s_result), overlap
        return best

    def reflect(
        self,
        failures: List[Tuple[TaskRecord, ReplayResult]],
        successes: List[Tuple[TaskRecord, ReplayResult]],
        skill: str,
        memory: str,
        *,
        edit_budget: int = 4,
    ) -> List[EditRecord]:
        """Call claude to analyze failures and propose skill/memory edits.

        Each failure is paired with the most similar success so the model can
        contrast the failed approach against a known-good approach.
        """
        if not failures:
            return []

        # Build comparison pairs: failure vs closest success
        pair_lines = []
        for i, (task, result) in enumerate(failures[:10], 1):
            best_match = self._most_similar_success(task, successes)
            block = [f"### Pair {i}"]
            block.append(
                f"FAILED — Intent: {task.intent[:200]}\n"
                f"         Reason: {result.fail_reason[:150]}\n"
                f"         Response: {result.response[:200]}"
            )
            if best_match is not None:
                s_task, s_result = best_match
                block.append(
                    f"SUCCESS — Intent: {s_task.intent[:200]}\n"
                    f"          Response: {s_result.response[:200]}"
                )
            else:
                block.append("SUCCESS — (no comparable success available)")
            pair_lines.append("\n".join(block))

        prompt = _REFLECT_PROMPT.format(
            budget=edit_budget,
            skill=skill[:1000],
            memory=memory[:1000],
            comparison_pairs="\n\n".join(pair_lines),
        )

        cmd = [self.claude_path, "-p", prompt, "--output-format", "text"]
        if self.reflect_model:
            cmd.extend(["--model", self.reflect_model])

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
