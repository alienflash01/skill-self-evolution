"""Offline sleep engine — persistent cross-night state.

~/.evolving-skills/sleep_state.json tracks:
  - night counter
  - last harvest timestamp per project
  - per-night history (scores, accept/reject)
"""
from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional

STATE_DIR = os.path.expanduser("~/.evolving-skills")
STATE_PATH = os.path.join(STATE_DIR, "sleep_state.json")

DEFAULT_STATE: Dict[str, Any] = {
    "version": 1,
    "night": 0,
    "last_harvest": {},
    "history": [],
}


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


class SleepState:
    def __init__(self, path: str = STATE_PATH, data: Optional[Dict] = None):
        self.path = path
        self.data = data if data is not None else dict(DEFAULT_STATE)

    @classmethod
    def load(cls, path: str = STATE_PATH) -> "SleepState":
        if os.path.exists(path):
            try:
                with open(path) as f:
                    data = json.load(f)
                merged = dict(DEFAULT_STATE)
                merged.update(data if isinstance(data, dict) else {})
                return cls(path, merged)
            except Exception:
                pass
        return cls(path, dict(DEFAULT_STATE))

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    @property
    def night(self) -> int:
        return int(self.data.get("night", 0))

    def begin_night(self) -> int:
        self.data["night"] = self.night + 1
        return self.night

    def last_harvest_for(self, project: str) -> Optional[str]:
        return self.data.get("last_harvest", {}).get(project)

    def set_last_harvest(self, project: str, iso_ts: str) -> None:
        self.data.setdefault("last_harvest", {})[project] = iso_ts

    def record_night(self, summary: Dict[str, Any]) -> None:
        self.data.setdefault("history", []).append(summary)

    @property
    def last_run(self) -> str:
        history = self.data.get("history", [])
        if history:
            return history[-1].get("ran_at", "unknown")
        return "never"
