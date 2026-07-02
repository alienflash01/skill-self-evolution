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


class TestCCBackendName:

    def test_backend_name_is_cc(self):
        assert CCBackend().name == "cc"
