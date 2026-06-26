"""Offline sleep engine — protected region editing for CLAUDE.md / SKILL.md.

Applies bounded EditRecords to a skill (SKILL.md body) or memory (CLAUDE.md)
document. All edits live inside a protected, clearly-marked region so the
sleep cycle never clobbers the user's hand-written content.

Markers (per evolving-skills DESIGN.md):
    <!-- EVOLVING-SKILLS:LEARNED START -->
    ... learned rules ...
    <!-- EVOLVING-SKILLS:LEARNED END -->

Within the region, rules are stored as markdown bullets (``- <rule text>``).
Edits are add / delete / replace on those bullets.
"""
from __future__ import annotations

import re
from typing import List, Tuple

from sleep.models import EditRecord

LEARNED_START = "<!-- EVOLVING-SKILLS:LEARNED START -->"
LEARNED_END = "<!-- EVOLVING-SKILLS:LEARNED END -->"
_BANNER = (
    "_This block is maintained by evolving-skills. Edits here are proposed "
    "offline, validated against your past tasks, and adopted only after you "
    "approve them. Hand-edits outside this block are never touched._"
)


# ── read the region ───────────────────────────────────────────────────────────

def extract_learned(doc: str) -> str:
    """Return the raw text inside the protected region, or '' if absent."""
    s = doc.find(LEARNED_START)
    e = doc.find(LEARNED_END)
    if s == -1 or e == -1:
        return ""
    return doc[s + len(LEARNED_START):e].strip()


def current_learned_lines(doc: str) -> List[str]:
    """Return learned rules as a list of bare rule strings (no leading '- ')."""
    inner = extract_learned(doc)
    lines: List[str] = []
    for ln in inner.splitlines():
        ln = ln.strip()
        if ln.startswith("- "):
            lines.append(ln[2:].strip())
    return lines


# ── write the region ──────────────────────────────────────────────────────────

def _strip_learned(doc: str) -> str:
    """Remove every protected region block from the doc."""
    while True:
        s = doc.find(LEARNED_START)
        if s == -1:
            break
        e = doc.find(LEARNED_END, s)
        if e == -1:                 # dangling start marker with no end: trim it
            doc = doc[:s]
            break
        doc = doc[:s] + doc[e + len(LEARNED_END):]
    while "\n\n\n" in doc:
        doc = doc.replace("\n\n\n", "\n\n")
    return doc.rstrip()


def set_learned(doc: str, learned_lines: List[str]) -> str:
    """Replace the protected learned region with the given bullet lines.

    The region is appended (after the user's content) if it didn't exist.
    """
    base = _strip_learned(doc)
    body = "\n".join(
        f"- {ln.strip().lstrip('- ').strip()}"
        for ln in learned_lines
        if ln and ln.strip()
    )
    block = (
        f"\n\n{LEARNED_START}\n"
        f"## Learned preferences & procedures\n\n{_BANNER}\n\n{body}\n"
        f"{LEARNED_END}\n"
    )
    return (base + block).lstrip("\n")


# ── apply edits ───────────────────────────────────────────────────────────────

def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def apply_edits(doc: str, edits: List[EditRecord]) -> Tuple[str, List[EditRecord]]:
    """Apply add/delete/replace edits to the protected learned region.

    Returns (new_doc, applied_edits). Dedup semantics:
      * ``add``       — skipped if a normalized-equal line already exists.
      * ``delete``    — removes every line whose normalized form contains the
                        normalized anchor (anchor defaults to content).
      * ``replace``   — in-place rewrites every matching line to ``content``.

    Edits that don't match anything, or that duplicate existing content, are
    silently dropped (and not returned in ``applied_edits``).
    """
    lines = current_learned_lines(doc)
    norm_set = {_norm(line) for line in lines}
    applied: List[EditRecord] = []

    for e in edits:
        op = (e.op or "add").lower()
        if op == "add":
            content = (e.content or "").strip()
            if not content or _norm(content) in norm_set:
                continue
            lines.append(content)
            norm_set.add(_norm(content))
            applied.append(e)
        elif op == "delete":
            anchor = _norm(e.anchor or e.content)
            if not anchor:
                continue
            keep = [line for line in lines if anchor not in _norm(line)]
            if len(keep) != len(lines):
                lines = keep
                norm_set = {_norm(line) for line in lines}
                applied.append(e)
        elif op == "replace":
            anchor = _norm(e.anchor)
            content = (e.content or "").strip()
            if not anchor or not content:
                continue
            new_lines: List[str] = []
            changed = False
            for line in lines:
                if anchor in _norm(line):
                    new_lines.append(content)
                    changed = True
                else:
                    new_lines.append(line)
            if changed:
                lines = new_lines
                norm_set = {_norm(line) for line in lines}
                applied.append(e)
        # unknown ops are ignored

    return set_learned(doc, lines), applied


# ── SKILL.md scaffold ─────────────────────────────────────────────────────────

def ensure_skill_scaffold(doc: str, *, name: str, description: str) -> str:
    """Ensure a SKILL.md has YAML frontmatter so local agents load it.

    If frontmatter already exists the doc is returned unchanged. Otherwise a
    minimal frontmatter + heading is prepended.
    """
    if doc.lstrip().startswith("---"):
        return doc
    fm = (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "metadata:\n"
        "  provenance: evolving-skills\n"
        "  origin: offline-sleep\n"
        "---\n\n"
        f"# {name}\n\n"
        "Preferences and procedures learned from your past local agent sessions.\n"
    )
    return fm + doc
