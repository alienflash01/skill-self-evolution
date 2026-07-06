"""Tests for CCBackend — real Claude Code replay backend.

TDD: tests first, implementation second. Mocks subprocess.run so no real
API calls are made during testing.
"""
import subprocess
import pytest
from unittest.mock import patch, MagicMock

from sleep.models import TaskRecord, EditRecord
from sleep.cc_backend import CCBackend


def _mock_cc_result(stdout="I did the task", returncode=0):
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=stdout, stderr="",
    )


class TestCCBackendAttempt:

    def test_attempt_calls_claude_cli(self):
        """CCBackend.attempt should call `claude -p` with skill+memory+task."""
        backend = CCBackend(model="test-model")
        task = TaskRecord(id="t1", intent="Fix the login bug", project="/proj")

        with patch("sleep.cc_backend.subprocess.run", return_value=_mock_cc_result()) as mock_run:
            response = backend.attempt(task, skill="# Rules\nAlways test", memory="# Context\nUse auth")

        assert "I did the task" in response
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]  # first positional arg = command list
        assert cmd[0] == "claude"
        assert "-p" in cmd
        assert "--model" in cmd
        assert "test-model" in cmd

    def test_attempt_includes_skill_in_prompt(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", intent="Write a test")

        with patch("sleep.cc_backend.subprocess.run", return_value=_mock_cc_result()) as mock_run:
            backend.attempt(task, skill="Always use pytest", memory="")

        prompt = mock_run.call_args[0][0][2]  # claude -p <prompt>
        assert "pytest" in prompt

    def test_attempt_includes_task_intent(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", intent="Refactor the auth module")

        with patch("sleep.cc_backend.subprocess.run", return_value=_mock_cc_result()) as mock_run:
            backend.attempt(task, skill="", memory="")

        prompt = mock_run.call_args[0][0][2]
        assert "Refactor the auth module" in prompt

    def test_attempt_returns_empty_on_failure(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", intent="Do X")

        with patch("sleep.cc_backend.subprocess.run",
                   return_value=_mock_cc_result(stdout="", returncode=1)):
            response = backend.attempt(task, skill="", memory="")

        assert response == ""

    def test_attempt_handles_timeout(self):
        backend = CCBackend(timeout=1)
        task = TaskRecord(id="t1", intent="Do X")

        with patch("sleep.cc_backend.subprocess.run",
                   side_effect=subprocess.TimeoutExpired(cmd="claude", timeout=1)):
            response = backend.attempt(task, skill="", memory="")

        assert response == ""


class TestCCBackendJudge:

    def test_exact_match_returns_full_score(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", reference_kind="exact", reference="42")
        hard, soft, rationale = backend.judge(task, "The answer is 42")
        assert hard == 1.0
        assert soft >= 0.5

    def test_exact_mismatch_returns_zero(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", reference_kind="exact", reference="42")
        hard, soft, rationale = backend.judge(task, "The answer is 99")
        assert hard == 0.0

    def test_outcome_success_returns_full(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", reference_kind="none", outcome="success")
        hard, soft, rationale = backend.judge(task, "any response")
        assert hard == 1.0

    def test_outcome_fail_returns_zero(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", reference_kind="none", outcome="fail")
        hard, soft, rationale = backend.judge(task, "any response")
        assert hard == 0.0

    def test_outcome_mixed_returns_half(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", reference_kind="none", outcome="mixed")
        hard, soft, rationale = backend.judge(task, "any response")
        assert hard == 0.5

    def test_unknown_outcome_returns_half(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", reference_kind="none", outcome="unknown")
        hard, soft, rationale = backend.judge(task, "any response")
        assert hard == 0.5


class TestCCBackendReflect:

    def test_reflect_returns_edit_list(self):
        """reflect should propose skill/memory edits based on failures."""
        backend = CCBackend()
        task = TaskRecord(id="t1", intent="Fix bug", outcome="fail")
        from sleep.replay import ReplayResult
        failures = [(task, ReplayResult(id="t1", hard=0.0, fail_reason="wrong approach"))]
        successes = []

        with patch("sleep.cc_backend.subprocess.run",
                   return_value=_mock_cc_result(stdout='[{"target":"skill","op":"add","content":"Always check return codes","rationale":"prevent crash"}]')):
            edits = backend.reflect(failures, successes, skill="# S\n", memory="# M\n", edit_budget=2)

        assert isinstance(edits, list)
        if edits:
            assert isinstance(edits[0], EditRecord)

    def test_reflect_respects_edit_budget(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", intent="Fix bug", outcome="fail")
        from sleep.replay import ReplayResult
        failures = [(task, ReplayResult(id="t1", hard=0.0))]

        # Return 10 edits — should be capped by budget
        big_response = "[" + ",".join(
            f'{{"target":"skill","op":"add","content":"rule {i}","rationale":"r{i}"}}'
            for i in range(10)
        ) + "]"

        with patch("sleep.cc_backend.subprocess.run",
                   return_value=_mock_cc_result(stdout=big_response)):
            edits = backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        assert len(edits) <= 2

    def test_reflect_returns_empty_on_invalid_json(self):
        backend = CCBackend()
        task = TaskRecord(id="t1", intent="Fix bug", outcome="fail")
        from sleep.replay import ReplayResult
        failures = [(task, ReplayResult(id="t1", hard=0.0))]

        with patch("sleep.cc_backend.subprocess.run",
                   return_value=_mock_cc_result(stdout="not json at all")):
            edits = backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        assert edits == []

    def test_reflect_strips_markdown_code_fence(self):
        """CC often wraps JSON in ```json ... ``` — must be stripped."""
        backend = CCBackend()
        task = TaskRecord(id="t1", intent="Fix bug", outcome="fail")
        from sleep.replay import ReplayResult
        failures = [(task, ReplayResult(id="t1", hard=0.0))]

        fenced = '```json\n[{"target":"skill","op":"add","content":"test rule","rationale":"r"}]\n```'
        with patch("sleep.cc_backend.subprocess.run",
                   return_value=_mock_cc_result(stdout=fenced)):
            edits = backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        assert len(edits) == 1
        assert edits[0].content == "test rule"

    def test_reflect_strips_trailing_code_fence(self):
        """CC sometimes appends ``` at the end without opening."""
        backend = CCBackend()
        task = TaskRecord(id="t1", intent="Fix bug", outcome="fail")
        from sleep.replay import ReplayResult
        failures = [(task, ReplayResult(id="t1", hard=0.0))]

        trailing = '[{"target":"skill","op":"add","content":"rule x","rationale":"r y"}]\n```'
        with patch("sleep.cc_backend.subprocess.run",
                   return_value=_mock_cc_result(stdout=trailing)):
            edits = backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        assert len(edits) == 1
        assert edits[0].content == "rule x"

    def test_reflect_empty_failures_returns_empty(self):
        backend = CCBackend()
        edits = backend.reflect([], [], skill="# S\n", memory="# M\n", edit_budget=2)
        assert edits == []

    # ── New tests: success-comparison in reflect prompt ──────────────────────

    def _make_failures_and_successes(self):
        """Helper: one failure with a distinct response, one success with a distinct response."""
        from sleep.replay import ReplayResult
        fail_task = TaskRecord(id="f1", intent="Fix the authentication bug in login.py", outcome="fail")
        fail_result = ReplayResult(
            id="f1", hard=0.0,
            response="I modified login.py but forgot to handle the edge case.",
            fail_reason="missing edge case",
        )
        succ_task = TaskRecord(id="s1", intent="Fix the authentication bug in auth.py", outcome="success")
        succ_result = ReplayResult(
            id="s1", hard=1.0,
            response="I modified auth.py and added comprehensive edge case handling.",
        )
        return [(fail_task, fail_result)], [(succ_task, succ_result)]

    def test_reflect_includes_success_comparison(self):
        """reflect prompt should contain BOTH failure and success info side by side for contrast."""
        backend = CCBackend()
        failures, successes = self._make_failures_and_successes()

        captured_prompt = []
        def capture(cmd, *a, **kw):
            # cmd is the full arg list: [claude_path, "-p", prompt, "--output-format", "text", ...]
            if isinstance(cmd, list) and len(cmd) > 2:
                captured_prompt.append(cmd[2])
            return _mock_cc_result(stdout="[]")

        with patch("sleep.cc_backend.subprocess.run", side_effect=capture):
            backend.reflect(failures, successes, skill="# S\n", memory="# M\n", edit_budget=2)

        assert len(captured_prompt) == 1
        prompt = captured_prompt[0]
        # The prompt must explicitly mention comparison / contrast between fail and success
        prompt_lower = prompt.lower()
        assert "differ" in prompt_lower or "contrast" in prompt_lower or "comparison" in prompt_lower

    def test_reflect_prompt_contains_failed_response(self):
        """reflect prompt must include the failed task's actual response text."""
        backend = CCBackend()
        failures, successes = self._make_failures_and_successes()
        failed_response_snippet = "forgot to handle the edge case"

        captured_prompt = []
        def capture(cmd, *a, **kw):
            if isinstance(cmd, list) and len(cmd) > 2:
                captured_prompt.append(cmd[2])
            return _mock_cc_result(stdout="[]")

        with patch("sleep.cc_backend.subprocess.run", side_effect=capture):
            backend.reflect(failures, successes, skill="# S\n", memory="# M\n", edit_budget=2)

        assert len(captured_prompt) == 1
        assert failed_response_snippet in captured_prompt[0]

    def test_reflect_prompt_contains_successful_response(self):
        """reflect prompt must include the successful task's actual response text."""
        backend = CCBackend()
        failures, successes = self._make_failures_and_successes()
        success_response_snippet = "added comprehensive edge case handling"

        captured_prompt = []
        def capture(cmd, *a, **kw):
            if isinstance(cmd, list) and len(cmd) > 2:
                captured_prompt.append(cmd[2])
            return _mock_cc_result(stdout="[]")

        with patch("sleep.cc_backend.subprocess.run", side_effect=capture):
            backend.reflect(failures, successes, skill="# S\n", memory="# M\n", edit_budget=2)

        assert len(captured_prompt) == 1
        assert success_response_snippet in captured_prompt[0]


class TestExitCodeJudge:
    """Tests for exit-code-based judging: exit 0 = hard 1.0, exit !=0 = hard 0.0."""

    def test_exit_code_zero_returns_full_score(self):
        """Task with reference_kind='exit_code' and exit_code=0 → hard 1.0."""
        backend = CCBackend()
        task = TaskRecord(
            id="t1",
            reference_kind="exit_code",
            exit_code=0,
            outcome="unknown",
        )
        hard, soft, rationale = backend.judge(task, "any response")
        assert hard == 1.0

    def test_exit_code_nonzero_returns_zero(self):
        """Task with reference_kind='exit_code' and exit_code=1 → hard 0.0."""
        backend = CCBackend()
        task = TaskRecord(
            id="t1",
            reference_kind="exit_code",
            exit_code=1,
            outcome="success",
        )
        hard, soft, rationale = backend.judge(task, "any response")
        assert hard == 0.0

    def test_no_exit_code_falls_back_to_outcome(self):
        """Task with reference_kind='exit_code' but no exit_code → outcome fallback."""
        backend = CCBackend()
        task = TaskRecord(
            id="t1",
            reference_kind="exit_code",
            outcome="success",
        )
        hard, soft, rationale = backend.judge(task, "any response")
        assert hard == 1.0  # falls back to outcome=success

    def test_exit_code_takes_priority_over_outcome(self):
        """Exit-code judging should override outcome even if they disagree."""
        backend = CCBackend()
        # exit_code=0 but outcome='fail' — exit code wins
        task_pass = TaskRecord(
            id="t1",
            reference_kind="exit_code",
            exit_code=0,
            outcome="fail",
        )
        hard, _, _ = backend.judge(task_pass, "response")
        assert hard == 1.0

        # exit_code=1 but outcome='success' — exit code wins
        task_fail = TaskRecord(
            id="t2",
            reference_kind="exit_code",
            exit_code=127,
            outcome="success",
        )
        hard, _, _ = backend.judge(task_fail, "response")
        assert hard == 0.0


class TestReflectModel:

    def test_reflect_uses_reflect_model_when_set(self):
        """When reflect_model is set, reflect() uses it instead of model."""
        backend = CCBackend(model="glm-4-flash", reflect_model="glm-4.6")
        task = TaskRecord(id="t1", intent="Fix bug", outcome="fail")
        from sleep.replay import ReplayResult
        failures = [(task, ReplayResult(id="t1", hard=0.0))]

        with patch("sleep.cc_backend.subprocess.run",
                   return_value=_mock_cc_result(stdout="[]")):
            backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        # Verify reflect used glm-4.6, not glm-4-flash
        from sleep.cc_backend import subprocess as sb
        # The mock_run captures the call
        import sleep.cc_backend as mod
        with patch.object(mod.subprocess, "run", return_value=_mock_cc_result(stdout="[]")) as mock_run2:
            backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)
            cmd = mock_run2.call_args[0][0]
            assert "glm-4.6" in cmd
            assert "glm-4-flash" not in cmd

    def test_attempt_uses_main_model(self):
        """attempt() always uses self.model, not reflect_model."""
        backend = CCBackend(model="glm-4-flash", reflect_model="glm-4.6")
        task = TaskRecord(id="t1", intent="Do something")

        with patch("sleep.cc_backend.subprocess.run", return_value=_mock_cc_result()) as mock_run:
            backend.attempt(task, skill="", memory="")

        cmd = mock_run.call_args[0][0]
        assert "glm-4-flash" in cmd
        assert "glm-4.6" not in cmd

    def test_reflect_defaults_to_main_model(self):
        """Without reflect_model, reflect() falls back to model."""
        backend = CCBackend(model="glm-4-flash")
        task = TaskRecord(id="t1", intent="Fix bug", outcome="fail")
        from sleep.replay import ReplayResult
        failures = [(task, ReplayResult(id="t1", hard=0.0))]

        with patch("sleep.cc_backend.subprocess.run",
                   return_value=_mock_cc_result(stdout="[]")) as mock_run:
            backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        cmd = mock_run.call_args[0][0]
        assert "glm-4-flash" in cmd


class TestCCBackendName:

    def test_backend_name_is_cc(self):
        assert CCBackend().name == "cc"


# ── Feedback History tests ──────────────────────────────────────────────────

class TestFeedbackHistory:

    def test_feedback_history_record_appends(self, tmp_path):
        """record() should append one line per edit to the markdown file."""
        from sleep.feedback_history import FeedbackHistory
        path = str(tmp_path / "feedback_history.md")
        fh = FeedbackHistory(path=path)
        edit = EditRecord(target="skill", op="add", content="使用祈使句写commit", rationale="clarity")

        fh.record(edit, outcome="rejected_no_improvement", score_delta=-0.02)

        entries = fh.load()
        assert len(entries) == 1
        assert entries[0]["content"] == "使用祈使句写commit"
        assert entries[0]["outcome"] == "rejected_no_improvement"
        assert entries[0]["score_delta"] == -0.02

    def test_feedback_history_get_summary_returns_recent(self, tmp_path):
        """get_summary should return the most recent N entries as markdown text."""
        from sleep.feedback_history import FeedbackHistory
        path = str(tmp_path / "feedback_history.md")
        fh = FeedbackHistory(path=path)

        for i in range(5):
            edit = EditRecord(target="skill", op="add", content=f"rule {i}", rationale="")
            fh.record(edit, outcome="rejected_low_score", score_delta=-0.01 * i)

        summary = fh.get_summary(max_entries=3)
        # Must be a string
        assert isinstance(summary, str)
        # Must contain only 3 entries (the most recent ones: rule 2, 3, 4)
        lines = [l for l in summary.strip().split("\n") if l.strip()]
        assert len(lines) == 3
        # Must contain the most recent entry
        assert "rule 4" in summary

    def test_feedback_history_clear_empties(self, tmp_path):
        """clear() should remove all entries from the file."""
        from sleep.feedback_history import FeedbackHistory
        path = str(tmp_path / "feedback_history.md")
        fh = FeedbackHistory(path=path)

        edit = EditRecord(target="skill", op="add", content="some rule", rationale="")
        fh.record(edit, outcome="accepted", score_delta=0.05)
        assert len(fh.load()) == 1

        fh.clear()
        assert fh.load() == []
        assert fh.get_summary() == ""


# ── Reflect improvement tests: feedback history + batch analysis ─────────────

class TestReflectFeedbackHistory:

    def test_reflect_prompt_contains_feedback_history(self):
        """reflect prompt should include feedback_history section."""
        backend = CCBackend()
        from sleep.replay import ReplayResult
        task = TaskRecord(id="t1", intent="Fix bug", outcome="fail")
        failures = [(task, ReplayResult(id="t1", hard=0.0))]

        captured_prompt = []
        def capture(cmd, *a, **kw):
            if isinstance(cmd, list) and len(cmd) > 2:
                captured_prompt.append(cmd[2])
            return _mock_cc_result(stdout="[]")

        with patch("sleep.cc_backend.subprocess.run", side_effect=capture):
            backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        assert len(captured_prompt) == 1
        prompt = captured_prompt[0]
        assert "feedback_history" in prompt.lower() or "past attempts" in prompt.lower()

    def test_reflect_prompt_says_avoid_repeating(self):
        """reflect prompt should contain instruction to avoid repeating rejected edits."""
        backend = CCBackend()
        from sleep.replay import ReplayResult
        task = TaskRecord(id="t1", intent="Fix bug", outcome="fail")
        failures = [(task, ReplayResult(id="t1", hard=0.0))]

        captured_prompt = []
        def capture(cmd, *a, **kw):
            if isinstance(cmd, list) and len(cmd) > 2:
                captured_prompt.append(cmd[2])
            return _mock_cc_result(stdout="[]")

        with patch("sleep.cc_backend.subprocess.run", side_effect=capture):
            backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        assert len(captured_prompt) == 1
        prompt = captured_prompt[0].lower()
        assert "avoid repeating" in prompt or "do not propose" in prompt


class TestReflectBatchAnalysis:

    def test_reflect_includes_all_failures_in_one_prompt(self):
        """All failures should be in a single prompt, not processed one-by-one."""
        backend = CCBackend()
        from sleep.replay import ReplayResult
        fail1 = TaskRecord(id="f1", intent="Fix login bug in auth.py", outcome="fail")
        fail2 = TaskRecord(id="f2", intent="Refactor the payment module", outcome="fail")
        failures = [
            (fail1, ReplayResult(id="f1", hard=0.0, response="resp1", fail_reason="reason1")),
            (fail2, ReplayResult(id="f2", hard=0.0, response="resp2", fail_reason="reason2")),
        ]

        captured_prompt = []
        call_count = {"n": 0}
        def capture(cmd, *a, **kw):
            call_count["n"] += 1
            if isinstance(cmd, list) and len(cmd) > 2:
                captured_prompt.append(cmd[2])
            return _mock_cc_result(stdout="[]")

        with patch("sleep.cc_backend.subprocess.run", side_effect=capture):
            backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        # Should make exactly ONE call to claude, not one per failure
        assert call_count["n"] == 1
        assert len(captured_prompt) == 1
        prompt = captured_prompt[0]
        # Both failures must be in the single prompt
        assert "Fix login bug" in prompt
        assert "Refactor the payment module" in prompt

    def test_reflect_prompt_contains_common_pattern_instruction(self):
        """Prompt should instruct CC to find COMMON patterns across multiple failures."""
        backend = CCBackend()
        from sleep.replay import ReplayResult
        fail1 = TaskRecord(id="f1", intent="Fix bug A", outcome="fail")
        fail2 = TaskRecord(id="f2", intent="Fix bug B", outcome="fail")
        failures = [
            (fail1, ReplayResult(id="f1", hard=0.0)),
            (fail2, ReplayResult(id="f2", hard=0.0)),
        ]

        captured_prompt = []
        def capture(cmd, *a, **kw):
            if isinstance(cmd, list) and len(cmd) > 2:
                captured_prompt.append(cmd[2])
            return _mock_cc_result(stdout="[]")

        with patch("sleep.cc_backend.subprocess.run", side_effect=capture):
            backend.reflect(failures, [], skill="# S\n", memory="# M\n", edit_budget=2)

        assert len(captured_prompt) == 1
        prompt = captured_prompt[0].lower()
        assert "common" in prompt
        assert "pattern" in prompt


# ── LLM Judge tests ────────────────────────────────────────────────────────────

class TestLLMJudge:
    """Tests for LLM-as-judge scoring of open-ended tasks."""

    _PRIME_TASK_INTENT = "Write a function to check if a number is prime"
    _GOOD_RESPONSE = (
        "def is_prime(n):\n"
        '    """Return True if n is prime."""\n'
        "    if n < 2:\n"
        "        return False\n"
        "    for i in range(2, int(n ** 0.5) + 1):\n"
        "        if n % i == 0:\n"
        "            return False\n"
        "    return True\n"
    )

    # ── 1. Good response → high score ──────────────────────────────────────────

    def test_llm_judge_returns_high_score_for_good_response(self):
        """A correct, complete response should receive a high score."""
        from sleep.llm_judge import LLMJudge
        from sleep.models import TaskRecord

        task = TaskRecord(id="t1", intent=self._PRIME_TASK_INTENT, reference_kind="none")
        judge = LLMJudge()

        with patch("sleep.llm_judge.subprocess.run",
                   return_value=_mock_cc_result(stdout="0.9")):
            score, rationale = judge.score(task, self._GOOD_RESPONSE)

        assert score >= 0.8

    # ── 2. Bad response → low score ────────────────────────────────────────────

    def test_llm_judge_returns_low_score_for_bad_response(self):
        """A non-answer should receive a low score."""
        from sleep.llm_judge import LLMJudge
        from sleep.models import TaskRecord

        task = TaskRecord(id="t1", intent=self._PRIME_TASK_INTENT, reference_kind="none")
        judge = LLMJudge()

        with patch("sleep.llm_judge.subprocess.run",
                   return_value=_mock_cc_result(stdout="0.1")):
            score, rationale = judge.score(task, "I dont know")

        assert score <= 0.2

    # ── 3. Empty response → zero, no CC call ──────────────────────────────────

    def test_llm_judge_returns_zero_for_empty_response(self):
        """Empty/whitespace response must return 0 without calling CC."""
        from sleep.llm_judge import LLMJudge
        from sleep.models import TaskRecord

        task = TaskRecord(id="t1", intent=self._PRIME_TASK_INTENT, reference_kind="none")
        judge = LLMJudge()

        with patch("sleep.llm_judge.subprocess.run") as mock_run:
            score, rationale = judge.score(task, "")

        assert score == 0.0
        mock_run.assert_not_called()

    # ── 4. Prompt contains rubric ──────────────────────────────────────────────

    def test_llm_judge_uses_rubric(self):
        """The prompt sent to CC must contain rubric/scoring criteria."""
        from sleep.llm_judge import LLMJudge
        from sleep.models import TaskRecord

        task = TaskRecord(id="t1", intent=self._PRIME_TASK_INTENT, reference_kind="none")
        judge = LLMJudge()

        captured_prompt = []

        def capture(cmd, *a, **kw):
            if isinstance(cmd, list) and len(cmd) > 2:
                captured_prompt.append(cmd[2])
            return _mock_cc_result(stdout="0.8")

        with patch("sleep.llm_judge.subprocess.run", side_effect=capture):
            judge.score(task, self._GOOD_RESPONSE)

        assert len(captured_prompt) == 1
        prompt = captured_prompt[0]
        # Rubric must define the scoring scale
        assert "0.0" in prompt and "1.0" in prompt
        # Should mention key rubric anchors
        prompt_lower = prompt.lower()
        assert "perfect" in prompt_lower or "correct" in prompt_lower
        assert "score" in prompt_lower or "rate" in prompt_lower
        # Task intent must appear in the prompt
        assert self._PRIME_TASK_INTENT in prompt

    # ── 5. CC failure → fallback (0.5) ─────────────────────────────────────────

    def test_llm_judge_fallback_on_cc_failure(self):
        """When CC times out or errors, return a neutral fallback score."""
        from sleep.llm_judge import LLMJudge
        from sleep.models import TaskRecord

        task = TaskRecord(id="t1", intent=self._PRIME_TASK_INTENT, reference_kind="none")
        judge = LLMJudge(timeout=5)

        with patch("sleep.llm_judge.subprocess.run",
                   side_effect=subprocess.TimeoutExpired(cmd="claude", timeout=5)):
            score, rationale = judge.score(task, self._GOOD_RESPONSE)

        assert score == 0.5
        assert "fallback" in rationale.lower()

    # ── 6. CCBackend.judge uses LLM when no exit_code/exact ────────────────────

    def test_judge_uses_llm_when_no_exit_code_or_exact(self):
        """CCBackend with judge_model should use LLM judge for open-ended tasks."""
        from sleep.models import TaskRecord

        backend = CCBackend(model="test", judge_model="glm-4.6")
        task = TaskRecord(
            id="t1",
            intent=self._PRIME_TASK_INTENT,
            reference_kind="none",
            outcome="unknown",
            exit_code=None,
        )

        with patch("sleep.llm_judge.subprocess.run",
                   return_value=_mock_cc_result(stdout="0.7")):
            hard, soft, rationale = backend.judge(task, self._GOOD_RESPONSE)

        assert hard == 0.7
