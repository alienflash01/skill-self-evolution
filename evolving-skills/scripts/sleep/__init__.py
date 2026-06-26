"""evolving-skills offline sleep engine.

A self-contained, stdlib-only implementation of the offline sleep cycle:

    harvest -> mine -> replay -> consolidate(gate) -> stage -> (adopt)

All modules use intra-package imports (``from sleep.types import ...``), so
the package is importable when ``scripts/`` is on ``sys.path`` (the hook
scripts already do ``sys.path.insert(0, os.path.dirname(...))``).

The default ``mock`` backend runs with zero external dependencies and is the
deterministic smoke path used by tests and CI.
"""
from __future__ import annotations

__all__ = [
    "types",
    "gate",
    "memory",
    "harvest",
    "mine",
    "replay",
    "consolidate",
    "staging",
    "state",
    "cycle",
]

__version__ = "0.1.0"
