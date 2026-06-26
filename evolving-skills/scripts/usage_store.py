#!/usr/bin/env python3
"""Usage telemetry store for evolving-skills.

Tracks skill use/view/patch counts in ~/.evolving-skills/skill_usage.json.
Pure stdlib, atomic writes, best-effort.
"""

import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

STATE_DIR = os.path.expanduser("~/.evolving-skills")
USAGE_PATH = os.path.join(STATE_DIR, "skill_usage.json")

KIND_KEYS: Dict[str, Tuple[str, str]] = {
    "use": ("use_count", "last_used_at"),
    "view": ("view_count", "last_viewed_at"),
    "patch": ("patch_count", "last_patched_at"),
}


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def _load() -> Dict[str, Any]:
    try:
        with open(USAGE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(data: Dict[str, Any]) -> None:
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        tmp = USAGE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, USAGE_PATH)
    except Exception:
        pass


def _empty_record(created_by: str = "agent") -> Dict[str, Any]:
    return {
        "use_count": 0,
        "view_count": 0,
        "patch_count": 0,
        "last_used_at": None,
        "last_viewed_at": None,
        "last_patched_at": None,
        "created_at": _now_iso(),
        "state": "active",
        "pinned": False,
        "created_by": created_by,
        "absorbed_into": None,
    }


def _records(data: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
    return [
        (k, v)
        for k, v in data.items()
        if k != "_meta" and isinstance(v, dict)
    ]


def apply_events(
    events: List[Tuple[str, str, str]],
    session_id: str = "",
    new_offset: int = 0,
) -> None:
    """Apply telemetry events: [(skill_name, kind, created_by), ...]."""
    if not events and not session_id:
        return
    data = _load()
    ts = _now_iso()
    for name, kind, cb in events:
        if not name or kind not in KIND_KEYS:
            continue
        rec = data.get(name)
        if not rec or not isinstance(rec, dict):
            rec = _empty_record(cb or "agent")
            data[name] = rec
        count_key, ts_key = KIND_KEYS[kind]
        rec[count_key] = (rec.get(count_key, 0) or 0) + 1
        rec[ts_key] = ts
        if rec.get("state") == "stale":
            rec["state"] = "active"
    if session_id:
        data.setdefault("_meta", {}).setdefault("offsets", {})
        data["_meta"]["offsets"][session_id] = {"o": new_offset, "t": ts}
    _save(data)


def get_offset(session_id: str) -> int:
    data = _load()
    v = data.get("_meta", {}).get("offsets", {}).get(session_id)
    if isinstance(v, dict):
        return v.get("o", 0)
    return 0


def get_nudge_row(session_id: str) -> int:
    data = _load()
    v = data.get("_meta", {}).get("nudges", {}).get(session_id)
    if isinstance(v, dict):
        return v.get("r", 0)
    return 0


def record_nudge(session_id: str, row_count: int) -> None:
    if not session_id:
        return
    data = _load()
    data.setdefault("_meta", {}).setdefault("nudges", {})
    data["_meta"]["nudges"][session_id] = {"r": row_count, "t": _now_iso()}
    _save(data)


def set_fields(name: str, **fields: Any) -> None:
    if not name:
        return
    data = _load()
    rec = data.get(name)
    if not rec or not isinstance(rec, dict):
        rec = _empty_record()
        data[name] = rec
    rec.update(fields)
    _save(data)


def all_records() -> Dict[str, Dict[str, Any]]:
    data = _load()
    return {k: v for k, v in _records(data)}


def forget_missing(existing: set, grace_hours: int = 24) -> None:
    data = _load()
    now = time.time()
    changed = False
    for name, rec in list(_records(data)):
        if existing and name in existing:
            if "missing_since" in rec:
                del rec["missing_since"]
                changed = True
            continue
        if rec.get("state") == "archived":
            continue
        since = rec.get("missing_since")
        if not since:
            rec["missing_since"] = _now_iso()
            changed = True
        elif (now - _parse_ts(since)) / 3600 >= grace_hours:
            data.pop(name, None)
            changed = True
    if changed:
        _save(data)


def _parse_ts(ts: Optional[str]) -> float:
    if not ts:
        return 0.0
    try:
        return time.mktime(time.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S"))
    except Exception:
        return 0.0


if __name__ == "__main__":
    # CLI: print status
    records = all_records()
    if not records:
        print(json.dumps({"skills": 0, "note": "no telemetry yet"}))
    else:
        print(json.dumps({"skills": len(records), "records": records}, indent=2))
