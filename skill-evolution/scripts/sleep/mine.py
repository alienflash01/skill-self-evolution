"""Offline sleep engine — Stage 2: mine.

Turn SessionDigests into TaskRecords (training units). Deterministic heuristic
miner — no API calls. Detects retry chains, extracts recurring intents, and
labels outcomes from feedback signals.
"""
from __future__ import annotations

import hashlib
from typing import List, Optional

from sleep.models import SessionDigest, TaskRecord


def _tid(project: str, intent: str) -> str:
    h = hashlib.sha256((project + "::" + intent).encode("utf-8")).hexdigest()[:12]
    return "task_" + h


def _short(text: str, n: int = 600) -> str:
    text = (text or "").strip()
    return text if len(text) <= n else text[:n] + " …"


def _looks_negative(signals: List[str]) -> bool:
    return any(s.startswith("neg:") for s in signals)


def _looks_positive(signals: List[str]) -> bool:
    return any(s.startswith("pos:") for s in signals)


def heuristic_mine(
    digests: List[SessionDigest],
    *,
    max_tasks: int = 40,
) -> List[TaskRecord]:
    tasks: List[TaskRecord] = []
    for d in digests:
        if not d.user_prompts:
            continue
        intent = d.user_prompts[0]
        if len(intent.strip()) < 8:
            continue
        if _looks_positive(d.feedback_signals) and not _looks_negative(d.feedback_signals):
            outcome = "success"
        elif _looks_negative(d.feedback_signals):
            outcome = "fail"
        elif d.n_user_turns >= 3:
            outcome = "mixed"
        else:
            outcome = "unknown"

        attempted = d.assistant_finals[-1] if d.assistant_finals else ""
        context = ""
        if len(d.user_prompts) > 1:
            context = "Follow-up constraints:\n- " + "\n- ".join(
                _short(p, 200) for p in d.user_prompts[1:4]
            )
        tags = []
        if d.tools_used:
            tags.append("tools:" + "+".join(d.tools_used[:4]))

        tasks.append(
            TaskRecord(
                id=_tid(d.project, intent),
                project=d.project,
                intent=_short(intent, 800),
                context_excerpt=_short(context, 600),
                attempted_solution=_short(attempted, 600),
                outcome=outcome,
                reference_kind="none",
                tags=tags,
                source_sessions=[d.session_id],
            )
        )
        if len(tasks) >= max_tasks:
            break
    return tasks


def dedup_tasks(tasks: List[TaskRecord]) -> List[TaskRecord]:
    by_id: dict = {}
    for t in tasks:
        if t.id in by_id:
            ex = by_id[t.id]
            ex.source_sessions = list(dict.fromkeys(ex.source_sessions + t.source_sessions))
            order = {"success": 3, "fail": 2, "mixed": 1, "unknown": 0}
            if order.get(t.outcome, 0) > order.get(ex.outcome, 0):
                ex.outcome = t.outcome
        else:
            by_id[t.id] = t
    return list(by_id.values())


def assign_splits(
    tasks: List[TaskRecord],
    *,
    val_fraction: float = 0.34,
    seed: int = 42,
) -> List[TaskRecord]:
    val_cut = int(round(val_fraction * 100))
    for t in tasks:
        bucket = int(hashlib.sha256((str(seed) + t.id).encode()).hexdigest(), 16) % 100
        t.split = "val" if bucket < val_cut else "train"
    if len(tasks) >= 2 and not any(t.split == "val" for t in tasks):
        tasks[-1].split = "val"
    if not any(t.split == "train" for t in tasks) and len(tasks) >= 2:
        tasks[0].split = "train"
    return tasks


def mine(
    digests: List[SessionDigest],
    *,
    max_tasks: int = 40,
    holdout_fraction: float = 0.34,
    seed: int = 42,
) -> List[TaskRecord]:
    tasks = heuristic_mine(digests, max_tasks=max_tasks)
    tasks = dedup_tasks(tasks)
    tasks = tasks[:max_tasks]
    tasks = assign_splits(tasks, val_fraction=holdout_fraction, seed=seed)
    return tasks
