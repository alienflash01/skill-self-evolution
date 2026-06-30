"""Offline sleep engine — Stage 4: consolidate (one epoch).

reflect on failures → propose bounded edits → apply → GATE on held-out val.
Only a candidate that strictly improves the held-out score is accepted.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from sleep.gate import evaluate_gate, select_gate_score
from sleep.memory import apply_edits
from sleep.replay import Backend, aggregate_scores, replay_batch
from sleep.models import EditRecord, ReplayResult, TaskRecord


@dataclass
class ConsolidationResult:
    accepted: bool
    gate_action: str
    baseline_score: float
    candidate_score: float
    new_skill: str
    new_memory: str
    applied_edits: List[EditRecord]
    rejected_edits: List[EditRecord]


def _split(tasks: List[TaskRecord]) -> Tuple[List[TaskRecord], List[TaskRecord]]:
    train = [t for t in tasks if t.split == "train"]
    val = [t for t in tasks if t.split == "val"]
    if not val:
        val = train or tasks
    if not train:
        train = val
    return train, val


def consolidate(
    backend: Backend,
    tasks: List[TaskRecord],
    skill: str,
    memory: str,
    *,
    edit_budget: int = 4,
    gate_metric: str = "mixed",
    gate_mixed_weight: float = 0.5,
    evolve_skill: bool = True,
    evolve_memory: bool = True,
) -> ConsolidationResult:
    train_tasks, val_tasks = _split(tasks)

    # baseline on val
    base_pairs = replay_batch(backend, val_tasks, skill, memory)
    base_hard, base_soft = aggregate_scores(base_pairs)
    base_score = select_gate_score(base_hard, base_soft, gate_metric, gate_mixed_weight)

    # reflect on train failures/successes
    train_pairs = replay_batch(backend, train_tasks, skill, memory)
    failures = [(t, r) for t, r in train_pairs if r.hard < 1.0]
    successes = [(t, r) for t, r in train_pairs if r.hard >= 1.0]

    original_base = base_score  # preserve for final comparison
    best_so_far = base_score   # running best (for sequential gate within one epoch)
    cand_skill, cand_memory = skill, memory
    all_applied: List[EditRecord] = []
    all_rejected: List[EditRecord] = []

    def _gate_apply(doc, edits, which):
        nonlocal cand_skill, cand_memory, best_so_far, all_applied, all_rejected
        if not edits:
            return doc
        new_doc, applied = apply_edits(doc, edits)
        if not applied:
            return doc
        trial_skill = new_doc if which == "skill" else cand_skill
        trial_memory = new_doc if which == "memory" else cand_memory
        pairs = replay_batch(backend, val_tasks, trial_skill, trial_memory)
        h, s = aggregate_scores(pairs)
        cand_score = select_gate_score(h, s, gate_metric, gate_mixed_weight)
        if cand_score > best_so_far:
            best_so_far = max(best_so_far, cand_score)
            all_applied.extend(applied)
            return new_doc
        all_rejected.extend(applied)
        return doc

    if evolve_skill:
        edits = backend.reflect(failures, successes, cand_skill, cand_memory, edit_budget=edit_budget)
        cand_skill = _gate_apply(cand_skill, edits, "skill")

    if evolve_memory:
        train_pairs2 = replay_batch(backend, train_tasks, cand_skill, cand_memory)
        failures2 = [(t, r) for t, r in train_pairs2 if r.hard < 1.0]
        successes2 = [(t, r) for t, r in train_pairs2 if r.hard >= 1.0]
        edits_m = backend.reflect(failures2, successes2, cand_skill, cand_memory, edit_budget=edit_budget)
        # swap target to memory
        for e in edits_m:
            e.target = "memory"
        cand_memory = _gate_apply(cand_memory, edits_m, "memory")

    # final gate
    final_pairs = replay_batch(backend, val_tasks, cand_skill, cand_memory)
    final_hard, final_soft = aggregate_scores(final_pairs)
    final_score = select_gate_score(final_hard, final_soft, gate_metric, gate_mixed_weight)

    gate = evaluate_gate(
        candidate_skill=cand_skill, cand_hard=final_hard,
        current_skill=skill, current_score=base_score,
        best_skill=skill, best_score=base_score,
        best_step=0, global_step=1,
        cand_soft=final_soft, metric=gate_metric, mixed_weight=gate_mixed_weight,
    )
    accepted = bool(all_applied) and final_score > original_base

    return ConsolidationResult(
        accepted=accepted,
        gate_action=gate.action,
        baseline_score=original_base,
        candidate_score=final_score,
        new_skill=cand_skill if accepted else skill,
        new_memory=cand_memory if accepted else memory,
        applied_edits=all_applied,
        rejected_edits=all_rejected,
    )
