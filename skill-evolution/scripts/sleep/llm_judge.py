"""LLMJudge — LLM-as-judge scoring for open-ended tasks.

Uses ``claude -p`` (or any compatible CLI) to score a response on a 0..1
rubric.  Designed to be used standalone *or* wired into ``CCBackend`` via
the ``judge_model`` parameter.

Scoring contract:
    score(task, response) -> (score: float, rationale: str)

    - empty / whitespace-only response  ->  (0.0, 'empty_response')
    - CC call fails (timeout/error)     ->  (0.5, 'llm_judge_fallback')
    - CC returns a number               ->  (parsed_float, 'llm_judge')
    - CC returns garbage                ->  (0.5, 'llm_judge_parse_error')
"""
from __future__ import annotations

import re
import subprocess
from typing import Tuple

from sleep.models import TaskRecord

_LLM_JUDGE_PROMPT = """You are an expert code reviewer. Score the AI agent's response.

Task: {task_intent}

Response:
{response}

Score from 0.0 to 1.0:
- 1.0 = Perfect: completely solves the task correctly
- 0.7 = Good: mostly correct, minor issues
- 0.5 = Partial: incomplete or has significant issues
- 0.2 = Poor: mostly wrong or irrelevant
- 0.0 = No response or completely wrong

Reply with ONLY a decimal number (e.g. 0.8). No explanation."""

# Regex to extract the first float-looking token from CC output.
# Handles "0.8", "Score: 0.8", "0.8\nExplanation...", etc.
_FLOAT_RE = re.compile(r"(\d+\.?\d*)")


class LLMJudge:
    """LLM-as-judge scorer for open-ended task responses.

    Parameters
    ----------
    model : str
        Model name passed via ``--model`` to the CLI.
    claude_path : str
        Path or name of the CLI executable (default ``claude``).
    timeout : int
        Per-call timeout in seconds.
    """

    def __init__(
        self,
        model: str = "glm-4.6",
        claude_path: str = "claude",
        timeout: int = 30,
    ):
        self.model = model
        self.claude_path = claude_path
        self.timeout = timeout

    # ── public API ─────────────────────────────────────────────────────────────

    def score(self, task: TaskRecord, response: str) -> Tuple[float, str]:
        """Score *response* for *task*.

        Returns ``(score, rationale)`` where *score* is clamped to [0, 1].
        """
        # ── fast path: empty response → zero ──────────────────────────────────
        if not response or not response.strip():
            return 0.0, "empty_response"

        # ── build prompt ───────────────────────────────────────────────────────
        prompt = _LLM_JUDGE_PROMPT.format(
            task_intent=task.intent,
            response=response,
        )

        # ── call CLI ───────────────────────────────────────────────────────────
        cmd = [self.claude_path, "-p", prompt, "--output-format", "text"]
        if self.model:
            cmd.extend(["--model", self.model])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return 0.5, "llm_judge_fallback"

        raw = result.stdout.strip() if result.returncode == 0 else ""
        if not raw:
            return 0.5, "llm_judge_fallback"

        # ── parse score ────────────────────────────────────────────────────────
        score = self._parse_score(raw)
        if score is None:
            return 0.5, "llm_judge_parse_error"

        return score, "llm_judge"

    # ── helpers ────────────────────────────────────────────────────────────────

    @staticmethod
    def _parse_score(raw: str) -> float | None:
        """Extract a float from CC output and clamp to [0, 1].

        Returns ``None`` if no number can be parsed.
        """
        m = _FLOAT_RE.search(raw)
        if not m:
            return None
        try:
            val = float(m.group(1))
        except (ValueError, TypeError):
            return None
        return max(0.0, min(1.0, val))
