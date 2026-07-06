"""Tests for the SkillOpt-style validation gate (gate.py).

The gate is the academic foundation of the entire product:
candidate is accepted ONLY if it strictly improves over baseline.
Ties are rejected by design.
"""
import pytest
from sleep.gate import select_gate_score, evaluate_gate, GateResult
from sleep.frontier import Frontier, FrontierEntry


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


# ── Frontier (top-N candidate pool) ───────────────────────────────────────────


def _entry(skill: str, score: float, **kw) -> FrontierEntry:
    """Build a FrontierEntry with sensible defaults."""
    return FrontierEntry(
        skill=skill,
        memory=kw.get("memory", ""),
        hard_score=score,
        soft_score=kw.get("soft_score", score),
        mixed_score=kw.get("mixed_score", score),
        added_at_night=kw.get("added_at_night", 0),
        lineage=kw.get("lineage", []),
    )


class TestFrontier:
    """Frontier: top-N candidate pool for evolutionary resilience."""

    def test_frontier_starts_empty(self):
        f = Frontier()
        assert f.size == 0
        assert f.best is None

    def test_frontier_add_first_candidate(self):
        f = Frontier()
        assert f.add(_entry("A", 0.8)) is True
        assert f.size == 1
        assert f.best is not None
        assert f.best.skill == "A"

    def test_frontier_keeps_top_n(self):
        f = Frontier(max_size=3)
        for i, s in enumerate([0.5, 0.9, 0.7, 0.8, 0.6]):
            f.add(_entry(f"skill_{i}", s))
        assert f.size == 3
        scores = sorted(e.mixed_score for e in f.entries)
        # top 3 of [0.5,0.9,0.7,0.8,0.6] are 0.9, 0.8, 0.7
        assert scores == [0.7, 0.8, 0.9]

    def test_frontier_replaces_worst(self):
        f = Frontier(max_size=3)
        f.add(_entry("A", 0.8))
        f.add(_entry("B", 0.7))
        f.add(_entry("C", 0.6))
        # add 0.75 → should replace C (0.6)
        accepted = f.add(_entry("D", 0.75))
        assert accepted is True
        skills = {e.skill for e in f.entries}
        assert "D" in skills
        assert "C" not in skills
        assert f.size == 3

    def test_frontier_rejects_below_threshold(self):
        f = Frontier(max_size=3)
        f.add(_entry("A", 0.8))
        f.add(_entry("B", 0.7))
        f.add(_entry("C", 0.6))
        # add 0.5 → below all existing → rejected
        accepted = f.add(_entry("E", 0.5))
        assert accepted is False
        assert f.size == 3
        skills = {e.skill for e in f.entries}
        assert "E" not in skills

    def test_frontier_select_returns_one_candidate(self):
        f = Frontier(max_size=5)
        f.add(_entry("A", 0.9))
        f.add(_entry("B", 0.8))
        f.add(_entry("C", 0.7))
        selected = f.select()
        assert selected is not None
        assert selected.skill in {"A", "B", "C"}

    def test_frontier_select_round_robin(self):
        f = Frontier(max_size=5)
        f.add(_entry("A", 0.9))
        f.add(_entry("B", 0.8))
        f.add(_entry("C", 0.7))
        # Select 3 times round-robin — each candidate should appear once
        picks = [f.select(strategy="round_robin").skill for _ in range(3)]
        assert sorted(picks) == ["A", "B", "C"]

    def test_frontier_best_score(self):
        f = Frontier(max_size=5)
        f.add(_entry("A", 0.7))
        f.add(_entry("B", 0.9))
        f.add(_entry("C", 0.8))
        assert f.best_score == pytest.approx(0.9)
        assert f.best.skill == "B"

    def test_frontier_select_best_strategy(self):
        f = Frontier(max_size=5)
        f.add(_entry("A", 0.7))
        f.add(_entry("B", 0.9))
        f.add(_entry("C", 0.8))
        for _ in range(3):
            assert f.select(strategy="best").skill == "B"

    def test_frontier_select_random_strategy(self):
        f = Frontier(max_size=5)
        f.add(_entry("A", 0.9))
        selected = f.select(strategy="random")
        assert selected is not None
        assert selected.skill == "A"

    def test_frontier_select_empty_returns_none(self):
        f = Frontier()
        assert f.select() is None

    def test_frontier_min_threshold(self):
        f = Frontier(max_size=3, min_threshold=0.6)
        # below threshold → rejected even when not full
        assert f.add(_entry("low", 0.5)) is False
        assert f.size == 0
        # at threshold → accepted
        assert f.add(_entry("ok", 0.6)) is True
        assert f.size == 1

    def test_frontier_persistence_roundtrip(self, tmp_path):
        f = Frontier(max_size=3)
        f.add(_entry("A", 0.8, memory="mem A", lineage=["root"]))
        f.add(_entry("B", 0.9, memory="mem B", lineage=["root", "A"]))
        path = str(tmp_path / "frontier.json")
        f.save(path)
        f2 = Frontier.load(path)
        assert f2.size == 2
        assert f2.best.skill == "B"
        assert f2.best_score == pytest.approx(0.9)
        assert f2.best.memory == "mem B"
        assert f2.best.lineage == ["root", "A"]

    def test_frontier_to_dict_roundtrip(self):
        f = Frontier(max_size=3)
        f.add(_entry("A", 0.8))
        d = f.to_dict()
        f2 = Frontier.from_dict(d)
        assert f2.size == 1
        assert f2.best.skill == "A"

    def test_frontier_load_missing_file_returns_empty(self, tmp_path):
        f = Frontier.load(str(tmp_path / "nonexistent.json"))
        assert f.size == 0
