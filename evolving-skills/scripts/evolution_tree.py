#!/usr/bin/env python3
"""Evolution tree tracker — tree-structured history of all skill changes.

Records each online distillation and offline sleep cycle as a node in a
JSONL tree, enabling future retrospective analysis and AFlow-style selection.

Format: one JSON object per line in ~/.evolving-skills/evolution-tree.jsonl
"""

import json
import os
import time
from typing import Any, Dict, List, Optional

STATE_DIR = os.path.expanduser("~/.evolving-skills")
TREE_PATH = os.path.join(STATE_DIR, "evolution-tree.jsonl")


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def _last_node_id() -> Optional[str]:
    """Read the last node_id from the tree (the current parent)."""
    try:
        with open(TREE_PATH, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        if lines:
            last = json.loads(lines[-1])
            return last.get("node_id")
    except Exception:
        pass
    return None


def append_node(
    *,
    source: str,           # "online" | "offline"
    changes: List[Dict[str, Any]],
    metrics: Optional[Dict[str, Any]] = None,
    notes: str = "",
) -> str:
    """Append a new node to the evolution tree. Returns the node_id."""
    os.makedirs(STATE_DIR, exist_ok=True)

    node_id = f"{source}-{_now_iso().replace(':', '').replace('-', '')}"
    parent_id = _last_node_id()

    node = {
        "node_id": node_id,
        "parent_id": parent_id,
        "date": _now_iso(),
        "source": source,
        "changes": changes,
        "metrics": metrics or {},
        "notes": notes,
    }

    try:
        with open(TREE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(node, ensure_ascii=False) + "\n")
    except Exception:
        pass

    return node_id


def read_tree() -> List[Dict[str, Any]]:
    """Read the entire evolution tree."""
    try:
        with open(TREE_PATH, encoding="utf-8") as f:
            return [json.loads(l) for l in f if l.strip()]
    except Exception:
        return []


def summary() -> Dict[str, Any]:
    """Quick summary of the tree."""
    tree = read_tree()
    if not tree:
        return {"nodes": 0, "online": 0, "offline": 0}

    online = sum(1 for n in tree if n.get("source") == "online")
    offline = sum(1 for n in tree if n.get("source") == "offline")
    total_changes = sum(len(n.get("changes", [])) for n in tree)

    return {
        "nodes": len(tree),
        "online": online,
        "offline": offline,
        "total_changes": total_changes,
        "last_node": tree[-1].get("node_id", ""),
        "last_date": tree[-1].get("date", ""),
    }


if __name__ == "__main__":
    print(json.dumps(summary(), indent=2))
