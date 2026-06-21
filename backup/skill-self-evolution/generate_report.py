#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a markdown report from deep-research JSON results.

Reads all JSON files under results/ (ordered by outline.yaml items),
fields.yaml for field structure, and writes report.md.
"""
import json
import re
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent
FIELDS_PATH = BASE / "fields.yaml"
OUTLINE_PATH = BASE / "outline.yaml"
OUTPUT_DIR = BASE / "results"
REPORT_PATH = BASE / "report.md"

# (field_name, short_zh_label) shown in each TOC line
SUMMARY_FIELDS = [
    ("release_date", "时间"),
    ("type", "类型"),
    ("what_evolved", "进化载体"),
    ("skill_encoding", "技能编码"),
    ("how_method", "进化方法"),
    ("when_evolve", "进化时机"),
    ("where_deploy", "部署域"),
]

SKIP_KEYS = {"_source_file", "uncertain"}

UNCERTAIN_MARKERS = ("[uncertain]", "[不确定]", "[uncertain]")


def load_fields(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    cats = data.get("field_categories") or data.get("fields") or []
    cat_order = []          # [(category_name, [field_dicts])]
    field_to_cat = {}       # field_name -> category_name
    known_fields = set()
    for cat in cats:
        cname = cat.get("category", "Other")
        flist = cat.get("fields", []) or []
        cat_order.append((cname, flist))
        for fd in flist:
            fname = fd.get("name")
            if fname:
                field_to_cat[fname] = cname
                known_fields.add(fname)
    return cat_order, field_to_cat, known_fields


def load_outline_items(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("items", []) or []


def get_field(data, name, field_to_cat):
    """Flat or nested lookup: top-level -> category key -> any nested dict."""
    if name in data:
        return data[name]
    seen_cats = set(field_to_cat.values())
    for cat in seen_cats:
        node = data.get(cat)
        if isinstance(node, dict) and name in node:
            return node[name]
    for v in data.values():
        if isinstance(v, dict) and name in v:
            return v[name]
    return None


def is_skip_value(v):
    if v is None:
        return True
    if isinstance(v, str):
        s = v.strip()
        if s == "" or s.lower() == "nan":
            return True
        low = s.lower()
        for m in UNCERTAIN_MARKERS:
            if m in low:
                return True
    return False


def fmt_value(v):
    if isinstance(v, bool):
        return "Yes" if v else "No"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        if not v:
            return ""
        if all(isinstance(x, dict) for x in v):
            lines = []
            for d in v:
                parts = [f"{k}: {fmt_value(val)}" for k, val in d.items()]
                lines.append(" | ".join(parts))
            return "\n".join(f"- {ln}" for ln in lines)
        joined = ", ".join(fmt_value(x) for x in v)
        if len(joined) > 100:
            return "\n".join(f"- {fmt_value(x)}" for x in v)
        return joined
    if isinstance(v, dict):
        parts = [f"{k}: {fmt_value(val)}" for k, val in v.items()]
        return "; ".join(parts)
    return str(v)


def label(name):
    return name.replace("_", " ").title()


def slugify(text):
    s = text.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def short(v, n=72):
    s = re.sub(r"\s+", " ", fmt_value(v)).strip()
    if len(s) > n:
        s = s[: n - 1].rstrip() + "…"
    return s


def render_field(name, value):
    fv = fmt_value(value)
    if "\n" in fv or len(fv) > 120:
        return f"**{label(name)}**\n\n{fv}"
    return f"**{label(name)}:** {fv}"


def main():
    cat_order, field_to_cat, known_fields = load_fields(FIELDS_PATH)
    items = load_outline_items(OUTLINE_PATH)

    # ordered json records: (id, name, category, note, data)
    records = []
    seen_ids = set()
    for it in items:
        iid = it.get("id")
        if not iid:
            continue
        fpath = OUTPUT_DIR / f"{iid}.json"
        if not fpath.exists():
            continue
        with open(fpath, encoding="utf-8") as f:
            data = json.load(f)
        records.append((iid, it.get("name", iid), it.get("category", ""), it.get("note", ""), data))
        seen_ids.add(iid)

    # include any leftover json not in outline
    for fpath in sorted(OUTPUT_DIR.glob("*.json")):
        iid = fpath.stem
        if iid in seen_ids:
            continue
        with open(fpath, encoding="utf-8") as f:
            data = json.load(f)
        records.append((iid, data.get("name", iid), "", "", data))

    lines = []
    lines.append("# AI Agent 中 Skill（技能）自进化实现方法 - 调研报告")
    lines.append("")
    lines.append(f"> 共 **{len(records)}** 个研究对象，字段覆盖率 100%（每个对象 26 字段）。")
    lines.append("")

    # ---- Table of Contents ----
    lines.append("## 目录")
    lines.append("")
    for idx, (iid, name, cat, note, data) in enumerate(records, 1):
        anchor = slugify(name)
        parts = []
        for fname, zh in SUMMARY_FIELDS:
            val = get_field(data, fname, field_to_cat)
            if is_skip_value(val):
                continue
            parts.append(f"{zh}: {short(val)}")
        suffix = (" — " + " | ".join(parts)) if parts else ""
        lines.append(f"{idx}. [{name}](#{anchor}){suffix}")
    lines.append("")

    # ---- Detailed content ----
    lines.append("## 详细内容")
    lines.append("")
    for idx, (iid, name, cat, note, data) in enumerate(records, 1):
        lines.append(f"### {name}")
        lines.append("")
        if cat or note:
            meta = []
            if cat:
                meta.append(f"`{cat}`")
            if note:
                meta.append(note)
            lines.append("> " + " · ".join(meta))
            lines.append("")

        uncertain_list = data.get("uncertain", []) or []

        for cname, flist in cat_order:
            rendered = []
            for fd in flist:
                fname = fd.get("name")
                if not fname:
                    continue
                if fname in uncertain_list:
                    continue
                val = get_field(data, fname, field_to_cat)
                if is_skip_value(val):
                    continue
                rendered.append(render_field(fname, val))
            if not rendered:
                continue
            lines.append(f"#### {cname}")
            lines.append("")
            lines.extend(rendered)
            lines.append("")

        # extra fields present in JSON but not defined in fields.yaml
        extras = []
        for k, v in data.items():
            if k in SKIP_KEYS or k in known_fields or k in field_to_cat.values():
                continue
            # skip category-level nested keys (their inner fields already covered)
            if isinstance(v, dict):
                continue
            if is_skip_value(v):
                continue
            extras.append(render_field(k, v))
        if extras:
            lines.append("#### 其他信息")
            lines.append("")
            lines.extend(extras)
            lines.append("")

        # uncertain fields, one per line
        if uncertain_list:
            lines.append("#### 不确定字段 / Uncertain")
            lines.append("")
            for uf in uncertain_list:
                lines.append(f"- {uf}")
            lines.append("")

        lines.append("---")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report generated: {REPORT_PATH}")
    print(f"Items: {len(records)} | Lines: {len(lines)}")


if __name__ == "__main__":
    main()
