"""Offline sleep engine — Stage 1: harvest.

Read the user's local Claude Code records (read-only) and normalize them
into SessionDigest objects. NO writes, NO network calls.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

from sleep.models import SessionDigest

_NEGATIVE_FEEDBACK = (
    "still broken", "still not", "still wrong", "doesn't work", "does not work",
    "not working", "that's wrong", "thats wrong", "incorrect", "wrong",
    "no,", "nope", "fix it", "didn't", "did not", "broken", "error again",
    "still failing", "still fails", "not fixed", "revert", "undo",
    "不对", "错误", "还是不行", "没解决", "撤销",
)
_POSITIVE_FEEDBACK = (
    "thanks", "thank you", "perfect", "great", "works now", "fixed",
    "that works", "lgtm", "looks good", "nice", "awesome", "correct",
    "谢谢", "好的", "可以了", "正确", "搞定",
)

_REPLAY_PROMPT_MARKERS = (
    "## CURRENT SKILL", "## FAILED TASKS", "## SUCCESSFUL TASKS",
    "## OUTPUT FORMAT", "You are a strict grader", "Score the response",
    "You are SkillOpt", "You are evolving-skills", "## TASK\n", "## SKILL\n",
)


def _iter_jsonl(path: str) -> Iterable[Dict[str, Any]]:
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception:
                    continue
    except (FileNotFoundError, IsADirectoryError, PermissionError):
        return


def _text_from_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for b in content:
            if isinstance(b, dict) and b.get("type") == "text" and b.get("text"):
                parts.append(str(b["text"]))
        return "\n".join(parts)
    return ""


def _tool_names_from_content(content: Any) -> List[str]:
    names: List[str] = []
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name"):
                names.append(str(b["name"]))
    return names


def _detect_feedback(text: str) -> List[str]:
    low = text.lower()
    sig: List[str] = []
    for ph in _NEGATIVE_FEEDBACK:
        if ph in low:
            sig.append("neg:" + ph)
    for ph in _POSITIVE_FEEDBACK:
        if ph in low:
            sig.append("pos:" + ph)
    return sig


def _is_meta_prompt(text: str) -> bool:
    t = text.strip()
    if not t:
        return True
    if t.startswith("<") and t.endswith(">"):
        return True
    if t.startswith("/") and len(t.split()) <= 3:
        return True
    if t.startswith("[Pasted text") or t.startswith("Caveat:"):
        return True
    return False


def _is_headless_replay(digest: "SessionDigest") -> bool:
    if digest.n_user_turns > 1:
        return False
    if digest.n_user_turns == 0:
        return True
    prompt = digest.user_prompts[0] if digest.user_prompts else ""
    for marker in _REPLAY_PROMPT_MARKERS:
        if marker in prompt:
            return True
    if digest.started_at and digest.ended_at and len(prompt) < 200:
        try:
            fmt = "%Y-%m-%dT%H:%M:%S"
            start = datetime.strptime(digest.started_at[:19], fmt)
            end = datetime.strptime(digest.ended_at[:19], fmt)
            if (end - start).total_seconds() < 3:
                return True
        except (ValueError, TypeError):
            pass
    return False


def digest_transcript(path: str) -> Optional[SessionDigest]:
    session_id = os.path.splitext(os.path.basename(path))[0]
    project = ""
    started = ""
    ended = ""
    user_prompts: List[str] = []
    assistant_finals: List[str] = []
    tools: List[str] = []
    files: List[str] = []
    feedback: List[str] = []
    n_user = 0
    n_asst = 0

    for rec in _iter_jsonl(path):
        rtype = rec.get("type")
        ts = rec.get("timestamp")
        if isinstance(ts, str) and ts:
            if not started:
                started = ts
            ended = ts
        if rec.get("cwd") and not project:
            project = str(rec["cwd"])
        if rec.get("gitBranch"):
            pass
        if rtype == "file-history-snapshot":
            snap = rec.get("snapshot") or rec.get("files") or {}
            if isinstance(snap, dict):
                files.extend([str(k) for k in list(snap.keys())[:20]])
        msg = rec.get("message")
        if not isinstance(msg, dict):
            continue
        role = msg.get("role")
        content = msg.get("content")
        if role == "user":
            text = _text_from_content(content)
            if text and not _is_meta_prompt(text):
                n_user += 1
                user_prompts.append(text.strip())
                feedback.extend(_detect_feedback(text))
        elif role == "assistant":
            n_asst += 1
            tools.extend(_tool_names_from_content(content))
            text = _text_from_content(content)
            if text.strip():
                assistant_finals.append(text.strip())

    if n_user == 0 and n_asst == 0:
        return None

    def _dedup(xs: List[str]) -> List[str]:
        seen: set = set()
        out = []
        for x in xs:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    return SessionDigest(
        session_id=session_id,
        project=project,
        started_at=started,
        ended_at=ended,
        user_prompts=user_prompts,
        assistant_finals=assistant_finals[-5:],
        tools_used=_dedup(tools),
        files_touched=_dedup(files),
        feedback_signals=feedback,
        n_user_turns=n_user,
        n_assistant_turns=n_asst,
        raw_path=path,
    )


def _project_matches(project: str, scope: Any, invoked: str) -> bool:
    if scope == "all":
        return True
    if isinstance(scope, (list, tuple)):
        return any(os.path.abspath(project) == os.path.abspath(p) for p in scope)
    if not invoked:
        return True
    a = os.path.abspath(project)
    b = os.path.abspath(invoked)
    return a == b or a.startswith(b + os.sep) or b.startswith(a + os.sep)


def harvest(
    transcripts_dir: str,
    *,
    scope: Any = "all",
    invoked_project: str = "",
    since_iso: Optional[str] = None,
    limit: int = 0,
) -> List[SessionDigest]:
    digests: List[SessionDigest] = []
    if not os.path.isdir(transcripts_dir):
        return digests

    paths: List[str] = []
    for root, _dirs, files in os.walk(transcripts_dir):
        for fn in files:
            if fn.endswith(".jsonl"):
                paths.append(os.path.join(root, fn))
    paths.sort(key=lambda p: os.path.getmtime(p), reverse=True)

    for p in paths:
        d = digest_transcript(p)
        if d is None:
            continue
        if _is_headless_replay(d):
            continue
        if not _project_matches(d.project or "", scope, invoked_project):
            continue
        if since_iso and d.ended_at and d.ended_at < since_iso:
            continue
        digests.append(d)
        if limit and len(digests) >= limit:
            break
    return digests
