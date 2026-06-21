#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a Simplified-Chinese markdown report from translated JSON results."""
import json
import re
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent
FIELDS_PATH = BASE / "fields.yaml"
OUTLINE_PATH = BASE / "outline.yaml"
OUTPUT_DIR = BASE / "results_zh"
REPORT_PATH = BASE / "report_zh.md"

# TOC summary fields: (field_name, short_zh_label)
SUMMARY_FIELDS = [
    ("release_date", "时间"),
    ("type", "类型"),
    ("what_evolved", "进化载体"),
    ("skill_encoding", "技能编码"),
    ("how_method", "进化方法"),
    ("when_evolve", "进化时机"),
    ("where_deploy", "部署域"),
]

# item category -> (chinese group name)
ITEM_CATEGORY = {
    "skill_library": "A. 技能库自动构建与进化",
    "experience_reflection": "B. 经验/记忆/反思驱动",
    "skill_mastery": "C. 技能/工具掌握与精炼",
    "engineering": "D. 工程级自进化框架",
}

CN_LABELS = {
    "name": "名称", "institution": "提出机构", "release_date": "发布时间",
    "paper_link": "论文链接", "code_link": "代码链接", "type": "类型",
    "what_evolved": "进化对象 (What)", "skill_as_artifact": "技能是否独立制品",
    "skill_encoding": "技能编码方式", "skill_granularity": "技能粒度",
    "how_method": "进化方法范式 (How)", "learning_signal_source": "学习信号来源",
    "reward_granularity": "奖励粒度", "learning_paradigm": "学习范式",
    "when_evolve": "进化时机 (When)", "trigger": "触发方式",
    "library_structure": "技能库结构", "retrieval_method": "检索/复用方式",
    "validation": "验证方式", "error_correction": "错误纠正",
    "test_env": "测试环境", "backbone_model": "底座模型",
    "where_deploy": "部署域 (Where)", "metrics": "评估指标",
    "key_results": "关键结论", "limitations": "局限与挑战",
}

CN_CATEGORY = {
    "基础信息": "基础信息",
    "进化对象_What": "进化对象 (What)",
    "技能表示": "技能表示",
    "自进化机制_How": "自进化机制 (How)",
    "进化时机_When": "进化时机 (When)",
    "存储与检索": "技能存储与检索",
    "验证与反馈": "验证与反馈",
    "环境与基座": "环境与基座",
    "评估指标": "评估指标",
    "局限与挑战": "局限与挑战",
}

SKIP_KEYS = {"_source_file", "uncertain"}
UNCERTAIN_MARKERS = ("[uncertain]", "[不确定]")


def load_fields(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    cats = data.get("field_categories") or data.get("fields") or []
    cat_order = []
    field_to_cat = {}
    known_fields = set()
    for cat in cats:
        cname = cat.get("category", "Other")
        cat_order.append((cname, cat.get("fields", []) or []))
        for fd in cat.get("fields", []) or []:
            fname = fd.get("name")
            if fname:
                field_to_cat[fname] = cname
                known_fields.add(fname)
    return cat_order, field_to_cat, known_fields


def load_outline_items(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return (yaml.safe_load(f) or {}).get("items", []) or []


def get_field(data, name, field_to_cat):
    if name in data:
        return data[name]
    for cat in set(field_to_cat.values()):
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
        if any(m in low for m in UNCERTAIN_MARKERS):
            return True
    return False


def fmt_value(v):
    if isinstance(v, bool):
        return "是" if v else "否"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        if not v:
            return ""
        if all(isinstance(x, dict) for x in v):
            lines = [" | ".join(f"{k}: {fmt_value(val)}" for k, val in d.items()) for d in v]
            return "\n".join(f"- {ln}" for ln in lines)
        joined = ", ".join(fmt_value(x) for x in v)
        if len(joined) > 100:
            return "\n".join(f"- {fmt_value(x)}" for x in v)
        return joined
    if isinstance(v, dict):
        return "; ".join(f"{k}: {fmt_value(val)}" for k, val in v.items())
    return str(v)


def slugify(text):
    s = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"\s+", "-", s.strip())


def short(v, n=60):
    s = re.sub(r"\s+", " ", fmt_value(v)).strip()
    return s[: n - 1].rstrip() + "…" if len(s) > n else s


def render_field(name, value):
    fv = fmt_value(value)
    lbl = CN_LABELS.get(name, name.replace("_", " "))
    if "\n" in fv or len(fv) > 100:
        return f"**{lbl}**\n\n{fv}"
    return f"**{lbl}：** {fv}"


def main():
    cat_order, field_to_cat, known_fields = load_fields(FIELDS_PATH)
    items = load_outline_items(OUTLINE_PATH)

    records = []
    seen = set()
    for it in items:
        iid = it.get("id")
        if not iid:
            continue
        fpath = OUTPUT_DIR / f"{iid}.json"
        if fpath.exists():
            with open(fpath, encoding="utf-8") as f:
                records.append((iid, it.get("name", iid), it.get("category", ""), it.get("note", ""), json.load(f)))
            seen.add(iid)
    for fpath in sorted(OUTPUT_DIR.glob("*.json")):
        if fpath.stem not in seen:
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
            records.append((fpath.stem, data.get("name", fpath.stem), "", "", data))

    L = []
    L.append("# AI Agent 中 Skill（技能）自进化实现方法 · 调研报告（中文版）")
    L.append("")
    L.append(f"> 共 **{len(records)}** 个研究对象，每个对象覆盖 26 个字段，字段覆盖率 100%。")
    L.append("> 字段框架融合系统综述《A Survey of Self-Evolving Agents》(arXiv:2507.21046) 的 What / When / How / Where 分类法。")
    L.append("")

    # category overview
    L.append("## 研究对象分类")
    L.append("")
    groups = {}
    for idx, (iid, name, cat, note, data) in enumerate(records, 1):
        groups.setdefault(cat, []).append((idx, name))
    for cat in ["skill_library", "experience_reflection", "skill_mastery", "engineering", ""]:
        if cat not in groups:
            continue
        gname = ITEM_CATEGORY.get(cat, "其他")
        L.append(f"**{gname}**")
        L.append("")
        for idx, name in groups[cat]:
            L.append(f"{idx}. {name}")
        L.append("")

    # TOC
    L.append("## 目录")
    L.append("")
    for idx, (iid, name, cat, note, data) in enumerate(records, 1):
        anchor = slugify(name)
        parts = []
        for fname, zh in SUMMARY_FIELDS:
            val = get_field(data, fname, field_to_cat)
            if is_skip_value(val):
                continue
            parts.append(f"{zh}：{short(val)}")
        suffix = (" — " + " | ".join(parts)) if parts else ""
        L.append(f"{idx}. [{name}](#{anchor}){suffix}")
    L.append("")

    # detailed
    L.append("## 详细内容")
    L.append("")
    for idx, (iid, name, cat, note, data) in enumerate(records, 1):
        L.append(f"### {name}")
        L.append("")
        if cat or note:
            meta = []
            if cat:
                meta.append(f"`{ITEM_CATEGORY.get(cat, cat)}`")
            if note:
                meta.append(note)
            L.append("> " + " · ".join(meta))
            L.append("")

        uncertain_list = data.get("uncertain", []) or []

        for cname, flist in cat_order:
            rendered = []
            for fd in flist:
                fname = fd.get("name")
                if not fname or fname in uncertain_list:
                    continue
                val = get_field(data, fname, field_to_cat)
                if is_skip_value(val):
                    continue
                rendered.append(render_field(fname, val))
            if rendered:
                L.append(f"#### {CN_CATEGORY.get(cname, cname)}")
                L.append("")
                L.extend(rendered)
                L.append("")

        extras = []
        for k, v in data.items():
            if k in SKIP_KEYS or k in known_fields or k in field_to_cat.values():
                continue
            if isinstance(v, dict) or is_skip_value(v):
                continue
            extras.append(render_field(k, v))
        if extras:
            L.append("#### 其他信息")
            L.append("")
            L.extend(extras)
            L.append("")

        if uncertain_list:
            L.append("#### 不确定字段")
            L.append("")
            for uf in uncertain_list:
                L.append(f"- {uf}")
            L.append("")

        L.append("---")
        L.append("")

    REPORT_PATH.write_text("\n".join(L), encoding="utf-8")
    print(f"Chinese report generated: {REPORT_PATH}")
    print(f"Items: {len(records)} | Lines: {len(L)}")


if __name__ == "__main__":
    main()
