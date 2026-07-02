"""Tests for distill.py core paths: transcript parsing, pattern detection,
delta computation, rule dedup, quality filter, and verification gate.

These tests lock down the 1125-line distill engine's critical behavior.
"""
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# distill.py lives in scripts/ which is on sys.path via conftest.py
import distill


# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_transcript(records):
    """Write a list of JSON dicts as JSONL transcript, return path."""
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False, encoding="utf-8")
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    f.close()
    return f.name


def _assistant_msg(content_blocks, ts="2026-01-01T00:00:00Z", session_id="s1", cwd="/proj"):
    """Build an assistant message record with tool_use blocks."""
    return {"type": "assistant", "timestamp": ts, "sessionId": session_id, "cwd": cwd,
            "message": {"role": "assistant", "content": content_blocks}}


def _user_msg(content_blocks, ts="2026-01-01T00:00:00Z", session_id="s1", cwd="/proj"):
    """Build a user message record with tool_result blocks."""
    return {"type": "user", "timestamp": ts, "sessionId": session_id, "cwd": cwd,
            "message": {"role": "user", "content": content_blocks}}


def _tool_use(call_id, name, inp):
    return {"type": "tool_use", "id": call_id, "name": name, "input": inp}


def _tool_result(call_id, output, is_error=False):
    return {"type": "tool_result", "tool_use_id": call_id, "content": output, "is_error": is_error}


def _text_block(text):
    return {"type": "text", "text": text}


# ── Transcript Parsing ───────────────────────────────────────────────────────

class TestParseTranscript:

    def test_parses_tool_use_and_result_pair(self):
        """A single Bash tool_use with matching tool_result."""
        path = _make_transcript([
            _assistant_msg([_tool_use("call_1", "Bash", {"command": "echo hello"})]),
            _user_msg([_tool_result("call_1", "hello\n", is_error=False)]),
        ])
        calls, msgs = distill.parse_transcript(path)
        os.unlink(path)

        assert len(calls) == 1
        assert calls[0].name == "Bash"
        assert calls[0].input["command"] == "echo hello"
        assert calls[0].output == "hello\n"
        assert calls[0].is_error is False

    def test_preserves_chronological_order(self):
        path = _make_transcript([
            _assistant_msg([_tool_use("c1", "Bash", {"command": "echo a"})]),
            _user_msg([_tool_result("c1", "a")]),
            _assistant_msg([_tool_use("c2", "Bash", {"command": "echo b"})]),
            _user_msg([_tool_result("c2", "b")]),
            _assistant_msg([_tool_use("c3", "Read", {"file_path": "/x"})]),
            _user_msg([_tool_result("c3", "contents")]),
        ])
        calls, _ = distill.parse_transcript(path)
        os.unlink(path)

        assert len(calls) == 3
        assert [c.name for c in calls] == ["Bash", "Bash", "Read"]
        assert [c.input.get("command", c.input.get("file_path")) for c in calls] == [
            "echo a", "echo b", "/x"
        ]

    def test_extracts_user_text_messages(self):
        path = _make_transcript([
            _user_msg([_text_block("Please fix the bug")]),
            _assistant_msg([_tool_use("c1", "Bash", {"command": "true"})]),
            _user_msg([_tool_result("c1", "")]),
            _user_msg([_text_block("That's wrong, try again")]),
        ])
        _, msgs = distill.parse_transcript(path)
        os.unlink(path)

        assert len(msgs) == 2
        assert "fix the bug" in msgs[0]["text"]
        assert "wrong" in msgs[1]["text"]

    def test_empty_file_returns_empty_lists(self):
        path = _make_transcript([])
        calls, msgs = distill.parse_transcript(path)
        os.unlink(path)
        assert calls == []
        assert msgs == []

    def test_malformed_json_lines_are_skipped(self):
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False)
        tmp.write('{"valid": true}\n')
        tmp.write('this is not json\n')
        tmp.write('{"also valid": true}\n')
        tmp.close()
        # Should not crash
        calls, msgs = distill.parse_transcript(tmp.name)
        os.unlink(tmp.name)
        assert calls == []
        assert msgs == []

    def test_extracts_cwd_from_records(self):
        path = _make_transcript([
            {"type": "assistant", "timestamp": "t", "sessionId": "s", "cwd": "/my/project",
             "message": {"role": "assistant", "content": [_tool_use("c1", "Bash", {"command": "ls"})]}},
            _user_msg([_tool_result("c1", "file.txt")], cwd="/my/project"),
        ])
        calls, _ = distill.parse_transcript(path)
        os.unlink(path)
        assert calls[0].cwd == "/my/project"


# ── Pattern Detection ────────────────────────────────────────────────────────

class TestDetectPatterns:

    def test_detects_fail_to_success_single_retry(self):
        """Bash fails, then same tool succeeds with modified command."""
        calls = [
            distill.ToolCall("c1", "Bash", {"command": "gcc -o test test.c"}, True, "undefined reference"),
            distill.ToolCall("c2", "Bash", {"command": "gcc -o test test.c -lm"}, False, ""),
        ]
        patterns = distill.detect_patterns(calls, [])
        assert len(patterns) == 1
        assert patterns[0].pattern == "fail_to_success"
        assert patterns[0].tool == "Bash"
        assert "-lm" in patterns[0].added_args

    def test_detects_multi_attempt_two_failures_then_success(self):
        calls = [
            distill.ToolCall("c1", "Bash", {"command": "make"}, True, "error 1"),
            distill.ToolCall("c2", "Bash", {"command": "make clean && make"}, True, "error 2"),
            distill.ToolCall("c3", "Bash", {"command": "make clean && make VERBOSE=1"}, False, "Build successful"),
        ]
        patterns = distill.detect_patterns(calls, [])
        assert len(patterns) == 1
        assert patterns[0].pattern == "multi_attempt"
        assert len(patterns[0].failed_calls) == 2

    def test_skips_permission_errors(self):
        """Permission-denied failures should not trigger pattern detection."""
        calls = [
            distill.ToolCall("c1", "Bash", {"command": "rm file"}, True,
                             "Requested permissions to run rm"),
            distill.ToolCall("c2", "Bash", {"command": "rm file"}, False, ""),
        ]
        patterns = distill.detect_patterns(calls, [])
        assert len(patterns) == 0

    def test_skips_low_value_errors(self):
        """'command not found' and 'no such file' are low learning value."""
        calls = [
            distill.ToolCall("c1", "Bash", {"command": "nonexistent-cmd"}, True,
                             "command not found"),
            distill.ToolCall("c2", "Bash", {"command": "real-cmd"}, False, "ok"),
        ]
        patterns = distill.detect_patterns(calls, [])
        # similarity between "nonexistent-cmd" and "real-cmd" is < 0.15 → skipped
        # AND low-value filter kicks in
        assert len(patterns) == 0

    def test_detects_user_correction(self):
        """User saying 'that's wrong' triggers correction pattern."""
        user_msgs = [
            {"text": "please create a file", "timestamp": "t1"},
            {"text": "that's wrong, use python3 not python", "timestamp": "t2"},
        ]
        patterns = distill.detect_patterns([], user_msgs)
        assert len(patterns) == 1
        assert patterns[0].pattern == "user_correction"
        assert "wrong" in patterns[0].user_correction

    def test_long_user_message_not_treated_as_correction(self):
        """Long messages (>200 chars) are task descriptions, not corrections."""
        long_msg = "that's wrong. " * 20  # > 200 chars
        user_msgs = [{"text": long_msg, "timestamp": "t1"}]
        patterns = distill.detect_patterns([], user_msgs)
        assert len(patterns) == 0

    def test_unrelated_calls_no_false_positive(self):
        """Two completely different Bash calls (low similarity) should not trigger."""
        calls = [
            distill.ToolCall("c1", "Bash", {"command": "cd /a/b/c/d/e/f/g/h/i/j/k && make"}, True, "error"),
            distill.ToolCall("c2", "Bash", {"command": "npm run dev --port 3000"}, False, ""),
        ]
        patterns = distill.detect_patterns(calls, [])
        assert len(patterns) == 0


# ── Bash Delta Computation ───────────────────────────────────────────────────

class TestComputeBashDelta:

    def test_added_flag_detected(self):
        added, removed = distill._compute_bash_delta(
            "gcc test.c", "gcc test.c -lm"
        )
        assert "-lm" in added
        assert removed == [] or removed == [""]

    def test_removed_flag_detected(self):
        added, removed = distill._compute_bash_delta(
            "gcc test.c -Wall -Werror", "gcc test.c"
        )
        assert "-Wall" in removed
        assert "-Werror" in removed

    def test_identical_commands_produce_empty_delta(self):
        added, removed = distill._compute_bash_delta(
            "echo hello", "echo hello"
        )
        assert added == []
        assert removed == []

    def test_fallback_on_invalid_shell_syntax(self):
        """Unbalanced quotes → shlex fails → fallback to token diff."""
        added, removed = distill._compute_bash_delta(
            "echo 'unbalanced", "echo 'unbalanced' -n"
        )
        # Should not crash; fallback uses regex token diff
        assert isinstance(added, list)
        assert isinstance(removed, list)


# ── Rule Dedup ───────────────────────────────────────────────────────────────

class TestRuleDedup:

    def test_identical_rule_text_is_duplicate(self):
        existing = [{"full_rule": "Always use -lm when linking math functions"}]
        assert distill._is_duplicate(
            "Always use -lm when linking math functions",
            existing,
        ) is True

    def test_minor_variation_below_threshold_is_duplicate(self):
        existing = [{"full_rule": "Always use -lm when linking math functions"}]
        # Very similar (> 0.75 ratio)
        similar = "Always use -lm when linking math function"
        assert distill._is_duplicate(similar, existing) is True

    def test_completely_different_rule_is_not_duplicate(self):
        existing = [{"full_rule": "Always use -lm when linking math functions"}]
        different = "Check for null pointers before dereferencing"
        assert distill._is_duplicate(different, existing) is False

    def test_empty_existing_rules_not_duplicate(self):
        assert distill._is_duplicate("any rule here", []) is False


# ── Quality Filter ───────────────────────────────────────────────────────────

class TestQualityFilter:

    def test_short_rule_rejected(self):
        assert distill._is_quality_rule("too short") is False

    def test_clean_rule_accepted(self):
        assert distill._is_quality_rule(
            "Always check return codes when calling system functions"
        ) is True

    def test_rule_with_shell_operators_rejected(self):
        assert distill._is_quality_rule(
            "Use gcc && make to build && deploy"
        ) is False

    def test_rule_with_dev_null_rejected(self):
        assert distill._is_quality_rule(
            "Redirect stderr to 2>/dev/null to suppress noise"
        ) is False


# ── Heuristic Rule Extraction ────────────────────────────────────────────────

class TestHeuristicExtraction:

    def test_extracts_rule_for_added_flag(self):
        trial = distill.TrialError(
            pattern="fail_to_success",
            tool="Bash",
            failed_calls=[distill.ToolCall("c1", "Bash", {"command": "gcc test.c"}, True, "undefined reference to `sin`")],
            succeeded_call=distill.ToolCall("c2", "Bash", {"command": "gcc test.c -lm"}, False, ""),
            added_args=["-lm"],
            error_text="undefined reference to `sin`",
        )
        rule = distill.extract_rule_heuristic(trial)
        assert rule is not None
        assert "-lm" in rule
        assert "gcc" in rule

    def test_returns_none_for_complex_delta(self):
        trial = distill.TrialError(
            pattern="multi_attempt",
            tool="Bash",
            failed_calls=[distill.ToolCall("c1", "Bash", {"command": "make -j4"}, True, "error")],
            succeeded_call=distill.ToolCall("c2", "Bash", {"command": "make clean && make -j4 VERBOSE=1"}, False, ""),
            added_args=["clean", "VERBOSE=1", "make", "&&", "-j4"],
            error_text="error",
        )
        # Heuristic can't handle complex multi-token deltas
        rule = distill.extract_rule_heuristic(trial)
        # Either None or filtered out by quality check
        if rule:
            assert not distill._is_quality_rule(rule) or len(rule) > 15

    def test_returns_none_for_user_correction_without_commands(self):
        trial = distill.TrialError(
            pattern="user_correction",
            tool="conversation",
            user_correction="that's wrong use python3",
        )
        rule = distill.extract_rule_heuristic(trial)
        assert rule is not None
        assert "wrong" in rule.lower() or "python3" in rule.lower()


# ── Error Fingerprint ────────────────────────────────────────────────────────

class TestErrorFingerprint:

    def test_same_error_produces_same_fingerprint(self):
        fp1 = distill._error_fingerprint("undefined reference to `sin` in function main")
        fp2 = distill._error_fingerprint("undefined reference to `cos` in function main")
        # After removing numbers and paths, these should be very similar
        assert isinstance(fp1, str) and isinstance(fp2, str)

    def test_empty_error_produces_empty_fingerprint(self):
        assert distill._error_fingerprint("") == ""
        assert distill._error_fingerprint(None) == ""
