"""Offline sleep engine — validation gate (pure function).

A self-contained copy of the SkillOpt validation gate so the sleep engine
has ZERO dependency on any research package. The gate is what makes nightly
evolution *safe*: a candidate skill/memory is accepted only if it strictly
improves the held-out validation score over the current baseline.

Pure functions only — no I/O, no global state. Easy to unit-test.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateResult:
    action: str            # "accept_new_best" | "accept" | "reject"
    current_skill: str
    current_score: float
    best_skill: str
    best_score: float
    best_step: int


def select_gate_score(hard: float, soft: float, metric: str = "hard",
                      mixed_weight: float = 0.5) -> float:
    """Project (hard, soft) onto a single comparison metric.

    metric ∈ {"hard", "soft", "mixed"}:
      * hard  — use only the exact-match score
      * soft  — use only the partial-credit score
      * mixed — convex blend (1-w)*hard + w*soft
    """
    if metric == "hard":
        return float(hard)
    if metric == "soft":
        return float(soft)
    if metric == "mixed":
        w = max(0.0, min(1.0, float(mixed_weight)))
        return (1.0 - w) * float(hard) + w * float(soft)
    raise ValueError(f"unknown gate metric {metric!r}; expected hard/soft/mixed")


def evaluate_gate(candidate_skill: str, cand_hard: float, current_skill: str,
                  current_score: float, best_skill: str, best_score: float,
                  best_step: int, global_step: int, *, cand_soft: float = 0.0,
                  metric: str = "hard", mixed_weight: float = 0.5) -> GateResult:
    """Pure gate decision: compare candidate score to current/best.

    Acceptance contract (strict improvement):
      * candidate > current  => accept
        * candidate > best   => accept_new_best (also updates best pointer)
        * otherwise          => accept
      * otherwise            => reject

    Ties do NOT accept — this is deliberate so the gate is a genuine filter,
    not a no-op that lets any non-regressing edit through.
    """
    cand_score = select_gate_score(cand_hard, cand_soft, metric, mixed_weight)
    if cand_score > current_score:
        if cand_score > best_score:
            return GateResult(
                "accept_new_best", candidate_skill, cand_score,
                candidate_skill, cand_score, global_step,
            )
        return GateResult(
            "accept", candidate_skill, cand_score,
            best_skill, best_score, best_step,
        )
    return GateResult(
        "reject", current_skill, current_score,
        best_skill, best_score, best_step,
    )
