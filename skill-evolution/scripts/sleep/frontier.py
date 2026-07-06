"""Offline sleep engine — Frontier (top-N candidate pool).

Maintains a pool of the best *N* candidate skill/memory snapshots produced
across sleep nights, inspired by the EvoSkill frontier concept.

Instead of tracking a single *best* skill (where one bad night can wipe
progress), the Frontier keeps multiple high-quality versions and lets the
next sleep cycle pick a parent from the pool via round-robin / best / random
selection.  This adds evolutionary resilience.

Pure data + file I/O only — no network, no external deps.
"""
from __future__ import annotations

import json
import os
import random as _random
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class FrontierEntry:
    """One snapshot in the frontier pool.

    *skill* and *memory* are the full text of the candidate.
    Scores are from the validation gate replay.
    *lineage* is the parent chain (skill names) back to the root.
    """

    skill: str = ""
    memory: str = ""
    hard_score: float = 0.0
    soft_score: float = 0.0
    mixed_score: float = 0.0
    added_at_night: int = 0
    lineage: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FrontierEntry":
        known = set(cls.__dataclass_fields__)  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in d.items() if k in known})


class Frontier:
    """Bounded pool of the top-N best candidate snapshots.

    * add() — insert a candidate; automatically evicts the worst entry
              if the pool is full and the newcomer is better.
    * select() — pick a parent for the next sleep cycle.
    * best / best_score — the highest-scoring entry.

    The pool is sorted descending by ``mixed_score`` so ``entries[0]``
    is always the current best.
    """

    def __init__(self, max_size: int = 3, min_threshold: float = 0.0):
        self.max_size = max(1, int(max_size))
        self.min_threshold = float(min_threshold)
        self._entries: List[FrontierEntry] = []
        # round-robin cursor
        self._rr_index = 0

    # ── core API ────────────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        return len(self._entries)

    @property
    def entries(self) -> List[FrontierEntry]:
        """Return entries as a list (sorted descending by score)."""
        return list(self._entries)

    def add(self, entry: FrontierEntry) -> bool:
        """Try to insert *entry*.

        Returns True if accepted, False if rejected.
        Rejection happens when:
          * score < min_threshold, or
          * pool is full and entry is not better than the worst member.
        """
        score = entry.mixed_score

        # Absolute floor
        if score < self.min_threshold:
            return False

        if len(self._entries) < self.max_size:
            self._entries.append(entry)
            self._sort()
            return True

        # Pool full — replace worst if newcomer is strictly better
        worst = self._entries[-1]
        if score > worst.mixed_score:
            self._entries[-1] = entry
            self._sort()
            return True

        return False

    def select(self, strategy: str = "round_robin") -> Optional[FrontierEntry]:
        """Pick a parent entry from the pool.

        Strategies:
          * ``round_robin`` — cycle through entries in order (default).
          * ``best``        — always return the highest-scoring entry.
          * ``random``      — uniformly random pick.

        Returns ``None`` if the pool is empty.
        """
        if not self._entries:
            return None

        if strategy == "best":
            return self._entries[0]

        if strategy == "random":
            return _random.choice(self._entries)

        # round_robin (default)
        idx = self._rr_index % len(self._entries)
        self._rr_index = (self._rr_index + 1) % len(self._entries)
        return self._entries[idx]

    @property
    def best(self) -> Optional[FrontierEntry]:
        """The highest-scoring entry, or None if empty."""
        return self._entries[0] if self._entries else None

    @property
    def best_score(self) -> float:
        """Score of the best entry, or 0.0 if empty."""
        return self._entries[0].mixed_score if self._entries else 0.0

    # ── internals ───────────────────────────────────────────────────────────

    def _sort(self) -> None:
        """Keep entries sorted descending by mixed_score."""
        self._entries.sort(key=lambda e: e.mixed_score, reverse=True)

    # ── serialisation ───────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_size": self.max_size,
            "min_threshold": self.min_threshold,
            "entries": [e.to_dict() for e in self._entries],
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Frontier":
        f = cls(
            max_size=d.get("max_size", 3),
            min_threshold=d.get("min_threshold", 0.0),
        )
        for ed in d.get("entries", []):
            f._entries.append(FrontierEntry.from_dict(ed))
        f._sort()
        return f

    def save(self, path: str) -> None:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, ensure_ascii=False, indent=2)
        os.replace(tmp, path)

    @classmethod
    def load(cls, path: str) -> "Frontier":
        if not os.path.exists(path):
            return cls()
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                return cls.from_dict(data)
        except Exception:
            pass
        return cls()
