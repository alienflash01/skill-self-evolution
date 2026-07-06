"""FeedbackHistory — cross-iteration memory for the reflect stage.

Records which edits were proposed, accepted, or rejected so that subsequent
reflect() calls can avoid re-proposing the same dead-end edits.

Persistence format: one markdown line per entry, e.g.
    - [rejected_no_improvement] "使用祈使句写commit" (delta=-0.02)
"""
from __future__ import annotations

import os
from typing import List

from sleep.models import EditRecord

# Valid outcome labels
_VALID_OUTCOMES = frozenset({
    "accepted",
    "rejected_no_improvement",
    "rejected_low_score",
})


class FeedbackHistory:
    """Append-only log of edit proposals and their outcomes.

    Parameters
    ----------
    path:
        Filesystem path to the markdown file used for persistence.
        Parent directories are created lazily on first ``record()``.
    """

    def __init__(self, path: str = "data/feedback_history.md"):
        self.path = path

    # ── public API ────────────────────────────────────────────────────────

    def record(self, edit: EditRecord, outcome: str, score_delta: float) -> None:
        """Append one entry to the history file.

        Parameters
        ----------
        edit:
            The EditRecord that was proposed (and accepted or rejected).
        outcome:
            One of 'accepted', 'rejected_no_improvement', 'rejected_low_score'.
        score_delta:
            The change in validation score caused by this edit
            (negative for harmful edits, positive for helpful ones).
        """
        if outcome not in _VALID_OUTCOMES:
            raise ValueError(
                f"Invalid outcome '{outcome}'. Must be one of {sorted(_VALID_OUTCOMES)}."
            )

        # Ensure parent dir exists
        parent = os.path.dirname(self.path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        # Escape quotes in content for readability
        content = edit.content.replace('"', "'")
        line = f'- [{outcome}] "{content}" (delta={score_delta:+.4f})\n'

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line)

    def get_summary(self, max_entries: int = 20) -> str:
        """Return the most recent *max_entries* entries as markdown text.

        If the history is empty or the file does not exist, returns ``""``.
        """
        entries = self.load()
        if not entries:
            return ""

        recent = entries[-max_entries:]
        lines = []
        for e in recent:
            content = e["content"].replace('"', "'")
            delta = e["score_delta"]
            lines.append(f'- [{e["outcome"]}] "{content}" (delta={delta:+.4f})')
        return "\n".join(lines)

    def load(self) -> List[dict]:
        """Load all entries from the history file.

        Returns a list of dicts with keys: ``outcome``, ``content``,
        ``score_delta``.  Returns ``[]`` if the file does not exist.
        """
        if not os.path.exists(self.path):
            return []

        entries: List[dict] = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parsed = self._parse_line(line)
                if parsed is not None:
                    entries.append(parsed)
        return entries

    def clear(self) -> None:
        """Remove all entries by deleting (or truncating) the file."""
        if os.path.exists(self.path):
            os.remove(self.path)

    # ── internal helpers ──────────────────────────────────────────────────

    @staticmethod
    def _parse_line(line: str) -> dict | None:
        """Parse one markdown line back into a dict.

        Expected format: ``- [outcome] "content" (delta=±0.0000)``
        """
        import re

        pattern = r'^-\s*\[(\w+)\]\s*"(.*)"\s*\(delta=([+-]?[\d.]+)\)\s*$'
        m = re.match(pattern, line)
        if not m:
            return None
        return {
            "outcome": m.group(1),
            "content": m.group(2),
            "score_delta": float(m.group(3)),
        }
