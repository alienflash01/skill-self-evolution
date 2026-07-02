"""Tests for the SkillOpt-style validation gate (gate.py).

The gate is the academic foundation of the entire product:
candidate is accepted ONLY if it strictly improves over baseline.
Ties are rejected by design.
"""
import pytest
from sleep.gate import select_gate_score, evaluate_gate, GateResult


class TestSelectGateScore:
    """select_gate_score: project (hard, soft) onto a single metric."""

    def test_hard_metric_returns_hard_score(self):
        assert select_gate_score(hard=0.8, soft=0.6, metric="hard") == 0.8

    def test_soft_metric_returns_soft_score(self):
        assert select_gate_score(hard=0.8, soft=0.6, metric="soft") == 0.6

    def test_mixed_metric_blends_hard_and_soft(self):
        result = select_gate_score(hard=0.8, soft=0.6, metric="mixed", mixed_weight=0.5)
        assert result == pytest.approx(0.7)

    def test_mixed_weight_zero_is_all_hard(self):
        result = select_gate_score(hard=0.9, soft=0.1, metric="mixed", mixed_weight=0.0)
        assert result == pytest.approx(0.9)

    def test_mixed_weight_one_is_all_soft(self):
        result = select_gate_score(hard=0.1, soft=0.9, metric="mixed", mixed_weight=1.0)
        assert result == pytest.approx(0.9)

    def test_clamps_mixed_weight_above_one(self):
        result = select_gate_score(hard=0.1, soft=0.9, metric="mixed", mixed_weight=5.0)
        assert result == pytest.approx(0.9)

    def test_clamps_mixed_weight_below_zero(self):
        result = select_gate_score(hard=0.9, soft=0.1, metric="mixed", mixed_weight=-1.0)
        assert result == pytest.approx(0.9)

    def test_unknown_metric_raises_value_error(self):
        with pytest.raises(ValueError, match="unknown gate metric"):
            select_gate_score(hard=0.8, soft=0.6, metric="bogus")


class TestEvaluateGate:
    """evaluate_gate: the core acceptance decision."""

    def test_candidate_above_current_and_best_accepts_new_best(self):
        result = evaluate_gate(
            candidate_skill="new", cand_hard=0.9,
            current_skill="old", current_score=0.7,
            best_skill="old", best_score=0.7,
            best_step=0, global_step=1,
        )
        assert result.action == "accept_new_best"
        assert result.current_score == 0.9
        assert result.best_score == 0.9
        assert result.best_step == 1

    def test_candidate_above_current_but_below_best_accepts(self):
        result = evaluate_gate(
            candidate_skill="new", cand_hard=0.8,
            current_skill="old", current_score=0.7,
            best_skill="champ", best_score=0.95,
            best_step=5, global_step=10,
        )
        assert result.action == "accept"
        assert result.current_score == 0.8
        assert result.best_skill == "champ"
        assert result.best_score == 0.95

    def test_candidate_equal_to_current_is_rejected(self):
        """Ties do NOT accept — deliberate design."""
        result = evaluate_gate(
            candidate_skill="new", cand_hard=0.7,
            current_skill="old", current_score=0.7,
            best_skill="old", best_score=0.7,
            best_step=0, global_step=1,
        )
        assert result.action == "reject"
        assert result.current_skill == "old"

    def test_candidate_below_current_is_rejected(self):
        result = evaluate_gate(
            candidate_skill="new", cand_hard=0.3,
            current_skill="old", current_score=0.7,
            best_skill="old", best_score=0.7,
            best_step=0, global_step=1,
        )
        assert result.action == "reject"

    def test_uses_soft_score_when_metric_is_soft(self):
        """When metric='soft', the soft score drives the decision."""
        result = evaluate_gate(
            candidate_skill="new", cand_hard=0.3, cand_soft=0.9,
            current_skill="old", current_score=0.7,
            best_skill="old", best_score=0.7,
            best_step=0, global_step=1,
            metric="soft",
        )
        assert result.action == "accept_new_best"

    def test_gate_result_is_frozen_dataclass(self):
        """GateResult should be immutable."""
        result = evaluate_gate(
            candidate_skill="new", cand_hard=0.9,
            current_skill="old", current_score=0.7,
            best_skill="old", best_score=0.7,
            best_step=0, global_step=1,
        )
        with pytest.raises(AttributeError):
            result.action = "hacked"

    def test_zero_scores_candidate_above_zero_current_accepts(self):
        """Edge: both scores are zero, candidate is zero → tie → reject."""
        result = evaluate_gate(
            candidate_skill="new", cand_hard=0.0,
            current_skill="old", current_score=0.0,
            best_skill="old", best_score=0.0,
            best_step=0, global_step=1,
        )
        assert result.action == "reject"

    def test_mixed_metric_candidate_strictly_above_accepts(self):
        result = evaluate_gate(
            candidate_skill="new", cand_hard=0.8, cand_soft=0.7,
            current_skill="old", current_score=0.7,
            best_skill="old", best_score=0.7,
            best_step=0, global_step=1,
            metric="mixed", mixed_weight=0.5,
        )
        # candidate mixed = 0.5*0.8 + 0.5*0.7 = 0.75 > 0.7
        assert result.action == "accept_new_best"
        assert result.current_score == pytest.approx(0.75)
