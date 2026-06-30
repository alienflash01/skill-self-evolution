#!/usr/bin/env python3
"""
Agent Experience Distillation Engine

Core logic for:
1. Parsing Claude Code transcripts into structured tool-call sequences
2. Detecting trial-and-error patterns (fail → retry → success)
3. Computing diffs between failed and succeeded attempts
4. Extracting reusable rules via LLM
5. Storing and deduplicating rules
6. Generating CLAUDE.md pitfall sections

Usage:
    python3 distill.py offline --project /path/to/project [--dry-run]
    python3 distill.py online --tool Bash --failed-cmd "..." --error "..." --succeeded-cmd "..."
    python3 distill.py status
    python3 distill.py report
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Paths ────────────────────────────────────────────────────────────────────

PLUGIN_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PLUGIN_DIR / "data"
TRACES_DIR = DATA_DIR / "traces"
RULES_PATH = DATA_DIR / "rules.json"
STAGING_DIR = DATA_DIR / "staging"

CLAUDE_DIR = Path.home() / ".claude"
CLAUDE_PROJECTS_DIR = CLAUDE_DIR / "projects"


# ── Data Types ───────────────────────────────────────────────────────────────

@dataclass
class ToolCall:
    """One tool invocation extracted from a transcript."""
    tool_use_id: str
    name: str          # Bash, Write, Edit, Read, etc.
    input: Dict[str, Any]
    is_error: bool = False
    output: str = ""
    timestamp: str = ""
    session_id: str = ""
    cwd: str = ""


@dataclass
class TrialError:
    """A detected trial-and-error pattern: failed attempt → succeeded attempt."""
    pattern: str           # "fail_to_success" | "multi_attempt" | "user_correction"
    tool: str
    failed_calls: List[ToolCall] = field(default_factory=list)
    succeeded_call: Optional[ToolCall] = None
    user_correction: str = ""
    # computed delta
    added_args: List[str] = field(default_factory=list)
    removed_args: List[str] = field(default_factory=list)
    error_text: str = ""
    # metadata
    session_id: str = ""
    cwd: str = ""
    timestamp: str = ""


@dataclass
class Rule:
    """One extracted reusable rule."""
    id: str
    pattern: str           # trial-error pattern type
    tool: str
    trigger: str           # error pattern or condition
    action: str            # what to do differently
    full_rule: str         # human-readable rule text
    confidence: float = 0.8
    status: str = "pending"  # pending → verified → trusted | deprecated
    source: Dict[str, Any] = field(default_factory=dict)
    times_observed: int = 1
    times_applied: int = 0     # how many times this rule matched new errors
    created_at: str = ""
    last_updated: str = ""
    verified_at: str = ""      # when it first got verified


# ── Transcript Parser ─────────────────────────────────────────────────────────

def parse_transcript(path: str) -> Tuple[List[ToolCall], List[Dict]]:
    """Parse one Claude Code transcript JSONL file.

    Returns (tool_calls, user_messages) where tool_calls are in chronological
    order and user_messages include role/text/correction signals.
    """
    tool_calls: List[ToolCall] = []
    user_messages: List[Dict] = []

    # First pass: collect all tool_use blocks and tool_result blocks
    tool_use_map: Dict[str, Dict] = {}    # id → tool_use block
    tool_result_map: Dict[str, Dict] = {} # tool_use_id → result content

    records: List[Dict] = []
    session_id = Path(path).stem
    cwd = ""

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
                records.append(d)
            except (json.JSONDecodeError, ValueError):
                continue

    for d in records:
        if d.get("cwd") and not cwd:
            cwd = d["cwd"]
        if d.get("sessionId") and not session_id:
            session_id = d["sessionId"]

        t = d.get("type", "")
        msg = d.get("message", {})
        if not isinstance(msg, dict):
            continue

        content = msg.get("content", "")
        ts = d.get("timestamp", "")

        # Collect tool_use blocks from assistant messages
        if t == "assistant" and isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    tool_use_map[block["id"]] = {
                        "name": block.get("name", ""),
                        "input": block.get("input", {}),
                        "timestamp": ts,
                        "session_id": session_id,
                        "cwd": cwd,
                    }

        # Collect tool_result blocks from user messages
        if t == "user" and isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    tid = block.get("tool_use_id", "")
                    result_text = _extract_text(block.get("content", ""))
                    tool_result_map[tid] = {
                        "is_error": block.get("is_error", False),
                        "output": result_text,
                    }

        # Collect user text messages (for correction detection)
        if t == "user" and isinstance(content, str) and content.strip():
            user_messages.append({
                "text": content.strip(),
                "timestamp": ts,
            })
        elif t == "user" and isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    txt = block.get("text", "").strip()
                    if txt:
                        user_messages.append({"text": txt, "timestamp": ts})

    # Second pass: merge into ToolCall list in the order tool_use appeared
    call_order: List[str] = []
    for d in records:
        msg = d.get("message", {})
        if not isinstance(msg, dict):
            continue
        content = msg.get("content", "")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    call_id = block["id"]
                    if call_id not in call_order:
                        call_order.append(call_id)

    for call_id in call_order:
        tu = tool_use_map.get(call_id, {})
        tr = tool_result_map.get(call_id, {})
        tool_calls.append(ToolCall(
            tool_use_id=call_id,
            name=tu.get("name", ""),
            input=tu.get("input", {}),
            is_error=tr.get("is_error", False),
            output=tr.get("output", ""),
            timestamp=tu.get("timestamp", ""),
            session_id=tu.get("session_id", ""),
            cwd=tu.get("cwd", ""),
        ))

    return tool_calls, user_messages


def _extract_text(content: Any) -> str:
    """Extract text from tool_result content (str or list of blocks)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "tool_result":
                    parts.append(_extract_text(block.get("content", "")))
        return "\n".join(parts)
    return str(content)


# ── Trial-and-Error Pattern Detector ──────────────────────────────────────────

# Heuristic: user messages that indicate correction
_CORRECTION_SIGNALS = (
    "not right", "not correct", "that's wrong", "thats wrong",
    "no, that", "nope", "incorrect",
    "不对", "错了", "不是这", "不正确", "不行", "重新来", "改一下",
    "should be using", "supposed to be", "i meant", "actually, use",
    "应该是用", "意思是用", "其实应该",
)

# Corrections must be short (not a full task description) and start with a signal
_MAX_CORRECTION_LEN = 200

# Errors that are just permission denials or sandbox blocks (low learning value)
_PERMISSION_ERRORS = (
    "requested permissions", "haven't granted", "permission",
    "requires approval", "was blocked",
)

# Additional low-value errors (environment/sandbox issues, not coding mistakes)
_LOW_VALUE_ERRORS = (
    "no such file or directory",
    "command not found",
    "no module named",
    "executable file not found",
    "file exists",
)


def _is_permission_error(output: str) -> bool:
    """Check if error is just a permission denial (low learning value)."""
    low = output.lower()
    return any(sig in low for sig in _PERMISSION_ERRORS)


def _is_low_value_error(output: str) -> bool:
    """Check if error is a low-value environment issue (missing file/binary/module)."""
    low = output.lower().strip()
    # Take first line only (exit codes like "Exit code 1" are noise)
    first_line = low.split("\n")[-1].strip() if "\n" in low else low
    return any(sig in first_line for sig in _LOW_VALUE_ERRORS)


def _is_user_correction(text: str) -> bool:
    """Check if a user message is correcting the agent.

    Filters:
    - Must be short (< _MAX_CORRECTION_LEN chars) — long messages are task descriptions
    - Must START with a correction signal — avoids matching "actually" in the middle
    - Checked word-by-word at the start of the text
    """
    stripped = text.strip()
    if len(stripped) > _MAX_CORRECTION_LEN:
        return False
    low = stripped.lower()
    # Check if the text STARTS with any correction signal
    for sig in _CORRECTION_SIGNALS:
        if low.startswith(sig):
            return True
    # Also check Chinese patterns that may appear mid-sentence but short
    short_cn = ("不对", "错了", "不是这", "不正确", "不行", "改一下", "重新来")
    if len(stripped) < 80 and any(sig in low for sig in short_cn):
        return True
    return False


def _same_tool_type(a: ToolCall, b: ToolCall) -> bool:
    """Check if two calls are the same tool type."""
    return a.name == b.name


def _command_similarity(a: str, b: str) -> float:
    """Compute similarity between two command strings (0..1)."""
    return SequenceMatcher(None, a, b).ratio()


def _compute_bash_delta(failed_cmd: str, succeeded_cmd: str) -> Tuple[List[str], List[str]]:
    """Compute added/removed shell arguments between failed and succeeded commands."""
    try:
        args1 = set(shlex.split(failed_cmd))
        args2 = set(shlex.split(succeeded_cmd))
        added = sorted(args2 - args1)
        removed = sorted(args1 - args2)
        return added, removed
    except ValueError:
        # Fallback: token-level diff
        tokens1 = set(re.findall(r"\S+", failed_cmd))
        tokens2 = set(re.findall(r"\S+", succeeded_cmd))
        return sorted(tokens2 - tokens1), sorted(tokens1 - tokens2)


def detect_patterns(
    tool_calls: List[ToolCall],
    user_messages: List[Dict],
) -> List[TrialError]:
    """Detect trial-and-error patterns from a sequence of tool calls.

    Detects three patterns:
      1. fail_to_success: one failed call followed by a similar succeeded call
      2. multi_attempt:   2+ failed calls then a succeeded call (same tool)
      3. user_correction: user message correcting the agent
    """
    patterns: List[TrialError] = []

    # ── Pattern 1 & 2: Tool-call-based detection ──────────────────────────
    for i, call in enumerate(tool_calls):
        if call.is_error or not call.name:
            continue

        # Skip permission-only errors
        # (this call succeeded, check backwards for failures)

        # Look backwards for consecutive failures of the same tool type
        consecutive_failures: List[ToolCall] = []
        for j in range(i - 1, max(i - 8, -1), -1):  # look back up to 8 steps
            prev = tool_calls[j]
            if not _same_tool_type(prev, call):
                break
            if not prev.is_error:
                break
            if _is_permission_error(prev.output):
                # Skip permission errors, keep looking back
                continue
            if _is_low_value_error(prev.output):
                # Skip low-value errors (missing files/binaries), keep looking back
                continue
            consecutive_failures.append(prev)

        if not consecutive_failures:
            continue

        consecutive_failures.reverse()  # chronological order

        # Check similarity: succeeded call should be related to failures
        failed_cmd = _get_command(consecutive_failures[0])
        succeeded_cmd = _get_command(call)
        if failed_cmd and succeeded_cmd:
            sim = _command_similarity(failed_cmd, succeeded_cmd)
            if sim < 0.15:
                continue  # too different, probably unrelated

        # Compute delta
        added_args: List[str] = []
        removed_args: List[str] = []
        error_text = consecutive_failures[0].output[:500]
        if failed_cmd and succeeded_cmd:
            added_args, removed_args = _compute_bash_delta(failed_cmd, succeeded_cmd)

        pattern_type = "multi_attempt" if len(consecutive_failures) >= 2 else "fail_to_success"

        patterns.append(TrialError(
            pattern=pattern_type,
            tool=call.name,
            failed_calls=consecutive_failures,
            succeeded_call=call,
            added_args=added_args,
            removed_args=removed_args,
            error_text=error_text,
            session_id=call.session_id,
            cwd=call.cwd,
            timestamp=call.timestamp,
        ))

    # ── Pattern 3: User correction detection ──────────────────────────────
    for i, msg in enumerate(user_messages):
        text = msg.get("text", "")
        if _is_user_correction(text):
            patterns.append(TrialError(
                pattern="user_correction",
                tool="conversation",
                user_correction=text[:300],
                session_id="",
                timestamp=msg.get("timestamp", ""),
            ))

    return patterns


def _get_command(call: ToolCall) -> str:
    """Extract the command string from a tool call."""
    if call.name == "Bash":
        return call.input.get("command", "")
    return json.dumps(call.input, sort_keys=True, ensure_ascii=False)


# ── Rule Extraction ───────────────────────────────────────────────────────────

# Prompt for LLM-based rule extraction
_EXTRACT_PROMPT = """You are analyzing a trial-and-error sequence from an AI coding agent.
The agent tried something, failed, then tried again with a modification and succeeded.
Extract ONE concise, general, reusable rule that will prevent the same error in the future.

Rules:
- Be general (not tied to specific file names or paths)
- Be actionable (state exactly what to do differently)
- Be concise (1-2 sentences max)
- If the error was a permission denial, output SKIP
- Output ONLY the rule text, nothing else

Trial-and-error details:
- Tool: {tool}
- Failed attempt: {failed_cmd}
- Error message: {error_text}
- Succeeded attempt: {succeeded_cmd}
- Arguments added: {added_args}
- Arguments removed: {removed_args}

Reusable rule:"""


def extract_rule_llm(trial: TrialError, model: str = "") -> Optional[str]:
    """Use Claude CLI (headless) to extract a rule from a trial-and-error pattern."""
    failed_cmd = _get_command(trial.failed_calls[0]) if trial.failed_calls else ""
    succeeded_cmd = _get_command(trial.succeeded_call) if trial.succeeded_call else ""

    prompt = _EXTRACT_PROMPT.format(
        tool=trial.tool,
        failed_cmd=failed_cmd[:300],
        error_text=trial.error_text[:300],
        succeeded_cmd=succeeded_cmd[:300],
        added_args=", ".join(trial.added_args),
        removed_args=", ".join(trial.removed_args),
    )

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True, text=True, timeout=60,
        )
        rule_text = result.stdout.strip()
        if not rule_text or rule_text.upper() == "SKIP":
            return None
        return rule_text
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def _is_quality_rule(text: str) -> bool:
    """Check if a heuristic-generated rule is high enough quality to save.
    
    Rejects rules where the delta produced garbage (long arg fragments,
    shell operators, paths leaking into the rule text).
    """
    if not text or len(text.strip()) < 15:
        return False
    # Reject if rule contains shell operators or pipes (delta leaked raw tokens)
    bad_tokens = ("&&", "||", "|", ">", "<", "2>/dev/null", "/dev/null")
    if any(t in text for t in bad_tokens):
        return False
    # Reject if the "add:" part is just a jumble of flags and paths
    # (heuristic produces these when shlex diff on complex commands yields noise)
    if "add:" in text.lower():
        after_add = text.lower().split("add:")[-1].strip()
        # Count tokens that look like flags/paths vs words
        tokens = after_add.split()
        if tokens:
            flag_like = sum(1 for t in tokens if t.startswith("-") or "/" in t or "\\" in t)
            if flag_like / len(tokens) > 0.6:
                return False
    return True


def extract_rule_heuristic(trial: TrialError) -> Optional[str]:
    """Heuristic rule extraction without LLM (fallback when no API)."""
    if not trial.failed_calls or not trial.succeeded_call:
        if trial.pattern == "user_correction":
            return f"When the user says something is wrong, check: {trial.user_correction[:150]}"
        return None

    failed_cmd = _get_command(trial.failed_calls[0])
    succeeded_cmd = _get_command(trial.succeeded_call)

    # For simple single-token additions, heuristic works well
    if trial.tool == "Bash" and trial.added_args:
        # Only use heuristic for short, clean deltas (1-3 tokens, all short)
        clean_adds = [a for a in trial.added_args if len(a) < 30 and "/" not in a and "\\" not in a]
        if clean_adds and len(clean_adds) == len(trial.added_args):
            cmd_name = failed_cmd.split()[0] if failed_cmd else "command"
            return (
                f"When `{cmd_name}` fails with "
                f"'{trial.error_text.split(chr(10))[0][:80]}', "
                f"add: {' '.join(clean_adds)}"
            )
        # Complex delta → heuristic can't produce quality rule
        return None
    elif trial.tool == "Bash" and trial.removed_args:
        clean_rems = [a for a in trial.removed_args if len(a) < 30 and "/" not in a]
        if clean_rems and len(clean_rems) == len(trial.removed_args):
            cmd_name = failed_cmd.split()[0] if failed_cmd else "command"
            return f"Avoid using {' '.join(clean_rems)} with `{cmd_name}`"
        return None
    elif trial.pattern == "multi_attempt":
        # For multi-attempt, just note the approach change
        return None  # too complex for heuristic
    return None


def extract_rule(trial: TrialError, use_llm: bool = False) -> Optional[str]:
    """Extract a rule from a trial-and-error pattern.
    
    With use_llm=True: always tries LLM first, falls back to heuristic.
    With use_llm=False: uses heuristic, but returns None for complex patterns
    (caller can decide to retry with LLM).
    """
    if use_llm:
        rule = extract_rule_llm(trial)
        if rule:
            return rule
        # LLM failed, try heuristic as fallback
        return extract_rule_heuristic(trial)
    
    # Non-LLM mode: try heuristic
    rule = extract_rule_heuristic(trial)
    if rule and _is_quality_rule(rule):
        return rule
    # Heuristic failed or quality too low → skip (caller can retry with --llm)
    return None


# ── Rule Storage ──────────────────────────────────────────────────────────────

def load_rules() -> Dict[str, Any]:
    """Load the rules database."""
    if RULES_PATH.exists():
        try:
            return json.loads(RULES_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"rules": []}


def save_rules(data: Dict[str, Any]) -> None:
    """Save the rules database."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RULES_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _rule_id(trigger: str, action: str) -> str:
    """Generate a stable ID for a rule."""
    raw = f"{trigger}|{action}"
    return "rule_" + hashlib.sha256(raw.encode()).hexdigest()[:12]


def _normalize_text(s: str) -> str:
    """Normalize text for dedup comparison."""
    return re.sub(r"\s+", " ", s.lower().strip())


def _is_duplicate(rule_text: str, existing_rules: List[Dict]) -> bool:
    """Check if a rule text is similar to any existing rule."""
    norm_new = _normalize_text(rule_text)
    for existing in existing_rules:
        norm_old = _normalize_text(existing.get("full_rule", ""))
        if not norm_old:
            continue
        ratio = SequenceMatcher(None, norm_new, norm_old).ratio()
        if ratio > 0.75:
            return True
    return False


def add_rule(
    trial: TrialError,
    rule_text: str,
    confidence: float = 0.8,
) -> Optional[Rule]:
    """Add a rule to the database (with dedup). Returns the Rule if added."""
    data = load_rules()
    rules = data.get("rules", [])

    if _is_duplicate(rule_text, rules):
        return None

    failed_cmd = _get_command(trial.failed_calls[0]) if trial.failed_calls else ""
    succeeded_cmd = _get_command(trial.succeeded_call) if trial.succeeded_call else ""

    now = datetime.now().isoformat()
    rule = Rule(
        id=_rule_id(trial.error_text[:100], rule_text),
        pattern=trial.pattern,
        tool=trial.tool,
        trigger=trial.error_text[:200] or trial.user_correction[:200],
        action=" ".join(trial.added_args) or succeeded_cmd[:200],
        full_rule=rule_text,
        confidence=confidence,
        source={
            "session_id": trial.session_id,
            "timestamp": trial.timestamp,
            "failed_command": failed_cmd[:200],
            "succeeded_command": succeeded_cmd[:200],
            "added_args": trial.added_args,
            "removed_args": trial.removed_args,
        },
        times_observed=1,
        created_at=now,
        last_updated=now,
    )
    rules.append(asdict(rule))
    data["rules"] = rules
    save_rules(data)
    return rule


# ── Verification Gate ─────────────────────────────────────────────────────────
#
# Rules start as "pending". The offline scan cross-checks new trial-and-error
# patterns against existing rules:
#   - Same error + same fix → verify the rule (pending → verified)
#   - Same error + different fix → record alternative, lower confidence
#   - 3+ observations → promote to "trusted"
#   - Verified rules get higher confidence and appear first in CLAUDE.md

def _error_fingerprint(error_text: str) -> str:
    """Create a normalized fingerprint from error text for matching."""
    # Take first meaningful line, strip paths/numbers
    lines = [l.strip() for l in (error_text or "").split("\n") if l.strip()]
    if not lines:
        return ""
    # Use the most informative line (longest non-exit-code line)
    best = max(lines, key=len) if lines else ""
    # Remove specific paths, numbers, exit codes
    best = re.sub(r"/\S+", "", best)       # paths
    best = re.sub(r"\b\d+\b", "N", best)    # numbers
    best = re.sub(r"\s+", " ", best).strip().lower()
    return best[:150]


def verify_rules(patterns: List[TrialError]) -> Dict[str, int]:
    """Cross-check observed patterns against existing rules.
    
    Returns stats: {verified, reinforced, deprecated, unchanged}
    """
    data = load_rules()
    rules = data.get("rules", [])
    if not rules or not patterns:
        return {"verified": 0, "reinforced": 0, "deprecated": 0, "unchanged": len(rules)}

    stats = {"verified": 0, "reinforced": 0, "deprecated": 0, "unchanged": 0}
    now = datetime.now().isoformat()

    # Build fingerprint → rule mapping
    rule_by_trigger: Dict[str, List[Dict]] = {}
    for r in rules:
        fp = _error_fingerprint(r.get("trigger", ""))
        if fp:
            rule_by_trigger.setdefault(fp, []).append(r)

    # Check each pattern against existing rules
    for trial in patterns:
        if not trial.error_text:
            continue
        fp = _error_fingerprint(trial.error_text)
        if not fp or fp not in rule_by_trigger:
            continue

        for r in rule_by_trigger[fp]:
            r["times_applied"] = r.get("times_applied", 0) + 1
            r["last_updated"] = now
            cur_status = r.get("status", "pending")

            if cur_status == "pending":
                # Same error seen again and was solved → verify
                r["status"] = "verified"
                r["verified_at"] = now
                r["confidence"] = min(0.95, r.get("confidence", 0.8) + 0.1)
                stats["verified"] += 1
            elif cur_status in ("verified", "trusted"):
                r["times_observed"] = r.get("times_observed", 1) + 1
                if r["times_observed"] >= 3 and cur_status != "trusted":
                    r["status"] = "trusted"
                    r["confidence"] = min(0.99, r.get("confidence", 0.8) + 0.1)
                stats["reinforced"] += 1

    # Count unchanged
    stats["unchanged"] = len(rules) - stats["verified"] - stats["reinforced"] - stats["deprecated"]

    save_rules(data)
    return stats


def get_rules_for_claude_md(min_confidence: float = 0.5, statuses: tuple = ("pending", "verified", "trusted")) -> List[Dict]:
    """Get rules filtered by confidence and status, sorted by trust level."""
    data = load_rules()
    rules = data.get("rules", [])
    status_order = {"trusted": 3, "verified": 2, "pending": 1, "deprecated": 0}
    filtered = [r for r in rules 
                if r.get("confidence", 0) >= min_confidence 
                and r.get("status", "pending") in statuses]
    filtered.sort(key=lambda r: (-status_order.get(r.get("status", "pending"), 0), 
                                  -r.get("confidence", 0)))
    return filtered

def find_transcripts(project_path: str, lookback_hours: int = 72) -> List[str]:
    """Find Claude Code transcript files for a project, within the lookback window."""
    if not CLAUDE_PROJECTS_DIR.exists():
        return []

    # Normalize project path for matching
    proj_abs = os.path.abspath(project_path)

    # Claude Code stores transcripts in a slugified directory name
    # e.g., -home-fanwei-project
    slug = proj_abs.replace("/", "-").replace("\\", "-").strip("-")
    # Also try with leading dash
    slug_with_dash = "-" + slug if not slug.startswith("-") else slug

    cutoff_ts = time.time() - lookback_hours * 3600
    paths: List[str] = []

    # Search all project dirs — the cwd field inside the transcript
    # is the authoritative source
    for project_dir in CLAUDE_PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        for jsonl in project_dir.glob("*.jsonl"):
            try:
                mtime = jsonl.stat().st_mtime
                if mtime < cutoff_ts:
                    continue
            except OSError:
                continue
            paths.append(str(jsonl))

    # Filter by actual cwd inside the transcript
    filtered: List[str] = []
    for path in paths:
        tool_calls, _ = parse_transcript(path)
        if not tool_calls:
            # Fall back to checking any record's cwd
            matched = False
            try:
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        try:
                            d = json.loads(line)
                            cwd = d.get("cwd", "")
                            if cwd and os.path.abspath(cwd) == proj_abs:
                                matched = True
                                break
                        except (json.JSONDecodeError, ValueError):
                            continue
            except OSError:
                pass
            if matched:
                filtered.append(path)
            continue
        # If any call's cwd matches the project, include it
        for call in tool_calls:
            if call.cwd and os.path.abspath(call.cwd) == proj_abs:
                filtered.append(path)
                break

    return filtered


def run_offline_distill(
    project_path: str,
    lookback_hours: int = 72,
    use_llm: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Run offline distillation over recent transcripts.

    Returns a summary dict.
    """
    transcripts = find_transcripts(project_path, lookback_hours)
    print(f"Found {len(transcripts)} transcript(s) for {project_path}")

    all_patterns: List[TrialError] = []
    total_calls = 0

    for path in transcripts:
        tool_calls, user_msgs = parse_transcript(path)
        total_calls += len(tool_calls)
        patterns = detect_patterns(tool_calls, user_msgs)
        all_patterns.extend(patterns)
        if patterns:
            print(f"  {Path(path).name}: {len(tool_calls)} calls, {len(patterns)} patterns")

    print(f"\nTotal: {total_calls} tool calls, {len(all_patterns)} trial-and-error patterns detected")

    if not all_patterns:
        return {"transcripts": len(transcripts), "patterns": 0, "rules_added": 0}

    # Extract rules
    rules_added: List[Dict] = []
    rules_skipped = 0

    for i, trial in enumerate(all_patterns):
        print(f"\n[{i+1}/{len(all_patterns)}] Pattern: {trial.pattern} ({trial.tool})")
        if trial.error_text:
            print(f"  Error: {trial.error_text[:120]}")

        rule_text = extract_rule(trial, use_llm=use_llm)
        if not rule_text:
            hint = "" if use_llm else " (try --llm for LLM extraction)"
            print(f"  → No rule extracted{hint}, skipped")
            rules_skipped += 1
            continue

        print(f"  Rule: {rule_text}")

        if dry_run:
            print(f"  → (dry-run, not saved)")
            continue

        rule = add_rule(trial, rule_text)
        if rule:
            print(f"  → Saved as {rule.id}")
            rules_added.append(asdict(rule))
        else:
            print(f"  → Duplicate, skipped")
            rules_skipped += 1

    # Verification gate: cross-check patterns against existing rules
    if not dry_run:
        v_stats = verify_rules(all_patterns)
        if v_stats["verified"] or v_stats["reinforced"]:
            print(f"\n  Gate: {v_stats['verified']} verified, {v_stats['reinforced']} reinforced, {v_stats['unchanged']} unchanged")

    summary = {
        "transcripts": len(transcripts),
        "total_calls": total_calls,
        "patterns": len(all_patterns),
        "rules_added": len(rules_added),
        "rules_skipped": rules_skipped,
        "dry_run": dry_run,
    }

    # Write staging report
    if rules_added and not dry_run:
        _write_report(summary, rules_added, all_patterns)

    return summary


def _write_report(
    summary: Dict,
    rules_added: List[Dict],
    all_patterns: List[TrialError],
) -> None:
    """Write a human-readable report to staging."""
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    report_path = STAGING_DIR / f"report_{date_str}.md"

    lines = [
        f"# Experience Distillation Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"- Transcripts scanned: {summary['transcripts']}",
        f"- Tool calls analyzed: {summary['total_calls']}",
        f"- Trial-and-error patterns: {summary['patterns']}",
        f"- Rules added: {summary['rules_added']}",
        f"- Rules skipped (duplicates): {summary['rules_skipped']}",
        "",
    ]

    if rules_added:
        lines.append("## New Rules")
        lines.append("")
        for r in rules_added:
            lines.append(f"### {r['full_rule']}")
            lines.append(f"- **Tool**: {r['tool']}")
            lines.append(f"- **Pattern**: {r['pattern']}")
            lines.append(f"- **Trigger**: `{r['trigger'][:100]}`")
            lines.append(f"- **Action**: `{r['action'][:100]}`")
            src = r.get("source", {})
            if src.get("failed_command"):
                lines.append(f"- **Failed**: `{src['failed_command'][:120]}`")
            if src.get("succeeded_command"):
                lines.append(f"- **Succeeded**: `{src['succeeded_command'][:120]}`")
            lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to: {report_path}")


# ── CLAUDE.md Generation ──────────────────────────────────────────────────────

def generate_claude_md_section() -> str:
    """Generate a markdown section for CLAUDE.md from the rules database."""
    rules = get_rules_for_claude_md()
    if not rules:
        return ""

    lines = [
        "",
        "<!-- BEGIN AGENT-EXPERIENCE -->",
        "## ⚠️ Known Pitfalls (Auto-distilled)",
        "",
        "<!-- These rules were extracted from trial-and-error patterns. -->",
        "<!-- Status: ✓=trusted(3+obs) ★=verified(2nd obs) ·=pending(1st obs) -->",
        "<!-- To update, run: /distill offline -->",
        "",
    ]

    # Group by tool
    by_tool: Dict[str, List[Dict]] = {}
    for r in rules:
        by_tool.setdefault(r.get("tool", "other"), []).append(r)

    status_icon = {"trusted": "✓", "verified": "★", "pending": "·", "deprecated": "✗"}

    for tool, tool_rules in sorted(by_tool.items()):
        lines.append(f"### {tool}")
        lines.append("")
        for r in tool_rules:
            icon = status_icon.get(r.get("status", "pending"), "·")
            lines.append(f"- {icon} {r['full_rule']}")
        lines.append("")

    lines.append("<!-- END AGENT-EXPERIENCE -->")
    lines.append("")

    return "\n".join(lines)


def apply_to_claude_md(project_path: str) -> bool:
    """Apply distilled rules to a project's CLAUDE.md."""
    section = generate_claude_md_section()
    if not section:
        print("No rules to apply.")
        return False

    claude_md = Path(project_path) / "CLAUDE.md"
    BLOCK_START = "<!-- BEGIN AGENT-EXPERIENCE -->"
    BLOCK_END = "<!-- END AGENT-EXPERIENCE -->"

    existing = ""
    if claude_md.exists():
        existing = claude_md.read_text(encoding="utf-8")

    # Replace existing block or append
    pattern = re.compile(
        re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END) + r"\n*",
        re.DOTALL,
    )
    if pattern.search(existing):
        new_content = pattern.sub(section, existing)
    else:
        new_content = existing.rstrip("\n") + "\n\n" + section if existing else section

    # Backup
    if existing:
        backup = claude_md.with_suffix(".md.bak")
        backup.write_text(existing, encoding="utf-8")

    claude_md.write_text(new_content, encoding="utf-8")
    print(f"Updated {claude_md} ({len(load_rules().get('rules', []))} rules)")
    return True


# ── CLI ───────────────────────────────────────────────────────────────────────

def cmd_status() -> None:
    """Show current status."""
    data = load_rules()
    rules = data.get("rules", [])
    print(f"═══ Agent Experience Distillation Status ═══")
    print(f"  Rules: {len(rules)}")
    print(f"  Data:  {DATA_DIR}")

    transcripts = list(CLAUDE_PROJECTS_DIR.rglob("*.jsonl")) if CLAUDE_PROJECTS_DIR.exists() else []
    print(f"  Available transcripts: {len(transcripts)}")

    if rules:
        print(f"\n  Recent rules:")
        for r in rules[-5:]:
            print(f"    [{r['tool']}] {r['full_rule'][:80]}")


def cmd_offline(args: argparse.Namespace) -> None:
    """Run offline distillation."""
    project = args.project or os.getcwd()
    summary = run_offline_distill(
        project_path=project,
        lookback_hours=args.lookback,
        use_llm=args.llm,
        dry_run=args.dry_run,
    )

    if summary["rules_added"] > 0 and not args.dry_run:
        print("\nTo apply rules to CLAUDE.md, run:")
        print(f"  python3 {__file__} apply --project '{project}'")


def cmd_online(args: argparse.Namespace) -> None:
    """Online distillation from a single fail→success pair (called by hook)."""
    # Reconstruct a minimal TrialError from CLI args
    trial = TrialError(
        pattern="fail_to_success",
        tool=args.tool or "Bash",
        error_text=args.error or "",
    )
    trial.failed_calls = [ToolCall(
        tool_use_id="hook_failed",
        name=args.tool or "Bash",
        input={"command": args.failed_cmd} if args.failed_cmd else {},
        is_error=True,
        output=args.error or "",
    )]
    trial.succeeded_call = ToolCall(
        tool_use_id="hook_succeeded",
        name=args.tool or "Bash",
        input={"command": args.succeeded_cmd} if args.succeeded_cmd else {},
        is_error=False,
        output="",
    )
    if args.failed_cmd and args.succeeded_cmd:
        trial.added_args, trial.removed_args = _compute_bash_delta(
            args.failed_cmd, args.succeeded_cmd,
        )

    rule_text = extract_rule(trial, use_llm=args.llm)
    if rule_text:
        rule = add_rule(trial, rule_text, confidence=0.7)
        if rule:
            print(f"[distill] Rule saved: {rule.full_rule}", file=sys.stderr)
        else:
            print(f"[distill] Duplicate rule, skipped", file=sys.stderr)
    else:
        print(f"[distill] No rule extracted", file=sys.stderr)


def cmd_apply(args: argparse.Namespace) -> None:
    """Apply rules to CLAUDE.md."""
    project = args.project or os.getcwd()
    apply_to_claude_md(project)


def cmd_report(args: argparse.Namespace) -> None:
    """Show all distilled rules."""
    data = load_rules()
    rules = data.get("rules", [])
    if not rules:
        print("No rules yet. Run 'offline' to distill from transcripts.")
        return
    print(f"═══ Distilled Rules ({len(rules)}) ═══\n")
    for i, r in enumerate(rules, 1):
        print(f"{i}. [{r['tool']}] {r['full_rule']}")
        print(f"   Pattern: {r['pattern']} | Confidence: {r['confidence']}")
        src = r.get("source", {})
        if src.get("failed_command"):
            print(f"   Failed:  {src['failed_command'][:100]}")
        if src.get("succeeded_command"):
            print(f"   Fixed:   {src['succeeded_command'][:100]}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agent Experience Distillation Engine",
    )
    sub = parser.add_subparsers(dest="command")

    # offline
    p_offline = sub.add_parser("offline", help="Run offline distillation over transcripts")
    p_offline.add_argument("--project", default=None, help="Project path (default: cwd)")
    p_offline.add_argument("--lookback", type=int, default=72, help="Lookback hours (default: 72)")
    p_offline.add_argument("--llm", action="store_true", help="Use LLM for rule extraction")
    p_offline.add_argument("--dry-run", action="store_true", help="Don't save rules")
    p_offline.set_defaults(func=cmd_offline)

    # online (for hook usage)
    p_online = sub.add_parser("online", help="Online distillation from a fail→success pair")
    p_online.add_argument("--tool", default="Bash")
    p_online.add_argument("--failed-cmd", default="")
    p_online.add_argument("--error", default="")
    p_online.add_argument("--succeeded-cmd", default="")
    p_online.add_argument("--llm", action="store_true")
    p_online.set_defaults(func=cmd_online)

    # apply
    p_apply = sub.add_parser("apply", help="Apply rules to CLAUDE.md")
    p_apply.add_argument("--project", default=None)
    p_apply.set_defaults(func=cmd_apply)

    # status
    p_status = sub.add_parser("status", help="Show current status")
    p_status.set_defaults(func=lambda a: cmd_status())

    # report
    p_report = sub.add_parser("report", help="Show all distilled rules")
    p_report.set_defaults(func=lambda a: cmd_report(args))

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
