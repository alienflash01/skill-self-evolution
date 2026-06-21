#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a markdown report from JSON results (SKILL.md self-evolution survey)."""
import json
import re
import textwrap
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent
FIELDS_PATH = BASE / "fields.yaml"
OUTLINE_PATH = BASE / "outline.yaml"
RESULTS_DIR = BASE / "results"
REPORT_PATH = BASE / "report.md"

# TOC summary fields: (field_name, short_label)
SUMMARY_FIELDS = [
    ("release_date", "时间"),
    ("type", "类型"),
    ("skill_as_doc", "文档载体"),
    ("edit_granularity", "编辑粒度"),
    ("version_gating", "版本门控"),
    ("when_evolve", "进化时机"),
    ("how_method", "进化方法"),
    ("where_deploy", "部署域"),
]

# item category -> chinese group name
ITEM_CATEGORY = {
    "academic_doc_skill": "A. 学术框架｜直接以 SKILL.md / 技能文档为进化载体",
    "engineering_practice": "B. 工程实践｜SKILL.md / CLAUDE.md 自改进 agent",
    "idea_text_opt": "C. 思想来源｜文本空间优化范式",
    "idea_distill": "D. 思想来源｜经验/记忆蒸馏为文档",
    "contrast": "E. 对照组｜非文档载体",
}

CN_LABELS = {
    "name": "名称", "institution": "提出机构", "release_date": "发布时间",
    "paper_link": "论文链接", "code_link": "代码链接", "type": "类型",
    "what_evolved": "进化对象 (What)", "skill_as_artifact": "技能是否独立制品",
    "skill_as_doc": "是否文档载体", "skill_encoding": "技能编码方式",
    "skill_granularity": "技能粒度",
    "doc_form": "文档形态", "edit_granularity": "编辑粒度",
    "version_gating": "版本与门控", "doc_provenance": "文档来源",
    "cross_transfer": "跨载体迁移", "library_governance": "技能库治理",
    "failure_memory": "失败记忆", "safety_guardrails": "编辑安全",
    "coevolution": "协同进化",
    "how_method": "进化方法范式 (How)", "learning_signal_source": "学习信号来源",
    "reward_granularity": "奖励粒度", "learning_paradigm": "学习范式",
    "when_evolve": "进化时机 (When)", "trigger": "触发方式",
    "library_structure": "技能库结构", "retrieval_method": "检索/复用方式",
    "validation": "验证方式", "error_correction": "错误纠正",
    "test_env": "测试环境", "backbone_model": "底座模型",
    "where_deploy": "部署域 (Where)", "metrics": "评估指标",
    "key_results": "关键结论", "limitations": "局限与挑战",
    "takeaways": "可借鉴要点",
}

SKIP_KEYS = {"_source_file", "uncertain"}
UNCERTAIN_MARKERS = ("[uncertain]", "[不确定]")


def load_fields(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    cats = data.get("field_categories") or []
    cat_order = [(c.get("category", "Other"), c.get("fields", []) or []) for c in cats]
    field_to_cat = {fd["name"]: c.get("category", "Other") for c in cats for fd in (c.get("fields") or []) if fd.get("name")}
    known_fields = set(field_to_cat)
    return cat_order, field_to_cat, known_fields


def load_outline(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("topic", ""), data.get("items", [])


def is_uncertain(value):
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, str):
        return any(m in value for m in UNCERTAIN_MARKERS)
    return False


def slugify(name):
    s = name.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s


def shorten(value, limit=70):
    """Compact a value for the TOC line."""
    if isinstance(value, list):
        value = "; ".join(str(v) for v in value)
    s = str(value).replace("\n", " ").strip()
    s = re.sub(r"\s+", " ", s)
    if len(s) > limit:
        s = s[: limit - 1].rstrip() + "…"
    return s


def fmt_value(value, indent=""):
    """Format a field value into markdown lines."""
    if isinstance(value, list):
        if not value:
            return [f"{indent}- (empty)"]
        out = []
        for i, v in enumerate(value):
            if isinstance(v, dict):
                parts = [f"`{k}`: {shorten(val, 120)}" for k, val in v.items()]
                out.append(f"{indent}- {' | '.join(parts)}")
            else:
                out.append(f"{indent}- {v}")
        return out
    if isinstance(value, dict):
        out = []
        for k, v in value.items():
            out.append(f"{indent}- `{k}`: {shorten(v, 200)}")
        return out
    s = str(value).strip()
    # long text -> wrap with blockquote-ish line breaks
    if len(s) > 160:
        wrapped = textwrap.wrap(s, width=120, break_long_words=False, break_on_hyphens=False)
        return [indent + line for line in wrapped]
    return [indent + s]


def get_field(data, name):
    """Flat lookup with nested fallback."""
    if name in data:
        return data[name]
    for k, v in data.items():
        if isinstance(v, dict) and name in v:
            return v[name]
    return None


def main():
    cat_order, field_to_cat, known_fields = load_fields(FIELDS_PATH)
    topic, items = load_outline(OUTLINE_PATH)

    # group items by category preserving outline order
    grouped = {}
    for it in items:
        grouped.setdefault(it.get("category", "other"), []).append(it)

    lines = []
    lines.append(f"# {topic} · 调研报告\n")
    lines.append(f"> 共 **{len(items)}** 个研究对象，每对象覆盖 {sum(len(f) for _, f in cat_order)} 个字段。")
    lines.append(f"> 字段框架融合《A Survey of Self-Evolving Agents》(arXiv:2507.21046) What/When/How/Where 分类法 + 新增「SKILL.md 专属维度」与「可借鉴要点」。\n")

    # ---- classification overview ----
    lines.append("## 研究对象分类\n")
    idx = 1
    numbering = {}
    for cat_key, group_name in ITEM_CATEGORY.items():
        if cat_key not in grouped:
            continue
        lines.append(f"**{group_name}**\n")
        for it in grouped[cat_key]:
            numbering[it["id"]] = idx
            lines.append(f"{idx}. {it['name']}")
            idx += 1
        lines.append("")

    # ---- TOC ----
    lines.append("## 目录\n")
    for cat_key, group_name in ITEM_CATEGORY.items():
        if cat_key not in grouped:
            continue
        lines.append(f"### {group_name}\n")
        for it in grouped[cat_key]:
            data = json.loads((RESULTS_DIR / f"{it['id']}.json").read_text(encoding="utf-8"))
            slug = slugify(it["name"])
            num = numbering[it["id"]]
            title = f"{num}. [{it['name']}](#{slug})"
            # summary field pairs, two per line via <br>
            pairs = []
            for fname, label in SUMMARY_FIELDS:
                val = get_field(data, fname)
                if is_uncertain(val) or val is None:
                    continue
                pairs.append(f"**{label}**: {shorten(val, 65)}")
            line1 = pairs[:3]
            line2 = pairs[3:6]
            line3 = pairs[6:]
            segs = []
            if line1:
                segs.append(" | ".join(line1))
            if line2:
                segs.append(" | ".join(line2))
            if line3:
                segs.append(" | ".join(line3))
            lines.append(f"{title} — {'<br>'.join(segs)}")
        lines.append("")

    # ---- details ----
    lines.append("## 详细内容\n")
    for cat_key, group_name in ITEM_CATEGORY.items():
        if cat_key not in grouped:
            continue
        for it in grouped[cat_key]:
            data = json.loads((RESULTS_DIR / f"{it['id']}.json").read_text(encoding="utf-8"))
            slug = slugify(it["name"])
            num = numbering[it["id"]]
            lines.append(f"### {it['name']}\n")
            lines.append(f"> `{cat_key}` · {it.get('note', '').split(chr(10))[0][:200]}\n")
            # by category
            for cat_name, fields in cat_order:
                cat_lines = []
                for fd in fields:
                    fname = fd["name"]
                    val = get_field(data, fname)
                    if fname in SKIP_KEYS:
                        continue
                    if is_uncertain(val):
                        continue
                    if fname in (data.get("uncertain") or []):
                        continue
                    label = CN_LABELS.get(fname, fname)
                    cat_lines.append(f"**{label}**")
                    cat_lines.extend(fmt_value(val, indent=""))
                    cat_lines.append("")
                if cat_lines:
                    lines.append(f"#### {cat_name}\n")
                    lines.extend(cat_lines)
            # uncertain array
            unc = data.get("uncertain") or []
            if unc:
                lines.append("#### 不确定字段\n")
                for u in unc:
                    lines.append(f"- {u}")
                lines.append("")
            lines.append("---\n")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Report written: {REPORT_PATH}")
    print(f"Items: {len(items)} | Lines: {len(lines)}")


if __name__ == "__main__":
    main()
