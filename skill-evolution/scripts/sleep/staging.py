"""Offline sleep engine — Stage 5/6: staging and adoption.

Write proposals + report into a staging dir; separate adopt step copies
over live files after backup. Never touches live files until adopt.
"""
from __future__ import annotations

import json
import os
import shutil
import time
from typing import List, Optional

from sleep.models import SleepReport


def _ts_dir() -> str:
    return time.strftime("%Y%m%d-%H%M%S", time.localtime())


def staging_root(project: str) -> str:
    return os.path.join(project, ".evolving-skills", "staging")


def latest_staging(project: str) -> Optional[str]:
    root = staging_root(project)
    if not os.path.isdir(root):
        return None
    subs = sorted(
        (os.path.join(root, d) for d in os.listdir(root)),
        key=lambda p: os.path.getmtime(p),
        reverse=True,
    )
    return subs[0] if subs else None


def write_staging(
    project: str,
    *,
    report: SleepReport,
    proposed_skill: Optional[str],
    proposed_memory: Optional[str],
    live_skill_path: str,
    live_memory_path: str,
    report_md: str,
) -> str:
    out = os.path.join(staging_root(project), _ts_dir())
    os.makedirs(out, exist_ok=True)

    manifest = {
        "live_skill_path": live_skill_path,
        "live_memory_path": live_memory_path,
        "has_skill": proposed_skill is not None,
        "has_memory": proposed_memory is not None,
        "accepted": report.accepted,
    }
    if proposed_skill is not None:
        with open(os.path.join(out, "proposed_SKILL.md"), "w", encoding="utf-8") as f:
            f.write(proposed_skill)
    if proposed_memory is not None:
        with open(os.path.join(out, "proposed_CLAUDE.md"), "w", encoding="utf-8") as f:
            f.write(proposed_memory)
    with open(os.path.join(out, "report.json"), "w", encoding="utf-8") as f:
        json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
    with open(os.path.join(out, "report.md"), "w", encoding="utf-8") as f:
        f.write(report_md)
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    return out


def _backup(path: str, backup_dir: str) -> None:
    if os.path.exists(path):
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copy2(path, os.path.join(backup_dir, os.path.basename(path)))


def adopt(staging_dir: str) -> List[str]:
    with open(os.path.join(staging_dir, "manifest.json")) as f:
        manifest = json.load(f)
    backup_dir = os.path.join(staging_dir, "backup")
    updated: List[str] = []

    if manifest.get("has_skill"):
        live = manifest["live_skill_path"]
        os.makedirs(os.path.dirname(live), exist_ok=True)
        _backup(live, backup_dir)
        shutil.copy2(os.path.join(staging_dir, "proposed_SKILL.md"), live)
        updated.append(live)
    if manifest.get("has_memory"):
        live = manifest["live_memory_path"]
        os.makedirs(os.path.dirname(live), exist_ok=True)
        _backup(live, backup_dir)
        shutil.copy2(os.path.join(staging_dir, "proposed_CLAUDE.md"), live)
        updated.append(live)
    return updated
