# 翻译指南：results.zh/*.json 中文化

## 目标
把 `results/*.json`（英文）翻译为 `results.zh/*.json`（简体中文），用于生成 `report.zh.md`。
**风格与术语以 `results.zh/skillopt.json` 为标准范例**——先读它，对齐语气与术语。

## 铁律（不可违反）
1. **JSON 结构、键名、键顺序必须与原文逐一对应**，不得增删键、不得改键名。`name`、`type` 的枚举值原样保留（如 `academic`/`industry`/`blog_practice`）。
2. **只翻译 string 值**。列表里的每个元素、`uncertain` 数组、`takeaways` 数组都要翻译。
3. **输出必须是合法 JSON**（双引号、无尾逗号、无注释）。翻译完自检 `python3 -m json.tool`。
4. 不臆造内容、不补字段、不删字段。信息保真，数字/符号零改动。

## 保留英文（不译）的类别
- **模型名**：GPT-5.5、GPT-5.4、GPT-5.4-mini/nano、GPT-5.2、Claude(Sonnet/Haiku/Opus)、Codex、Copilot、Gemini、Qwen3.5-4B、Llama 等。
- **项目/产品名**：SkillOpt、SkillSmith、CoEvoSkills、EvoSkill、DRAFT、SkillWeaver、OpenSpace、AutoSkill、SkillEvo、claude-self-improving-skills、claude-evolving-skills、Homunculus、TextGrad、GEPA、OPRO、PromptBreeder、EvoPrompt、ExpeL、AWM、MUSE、Reflexion、Self-Refine、Voyager 等。
- **benchmark / 数据集名**：SkillsBench、SpreadsheetBench、OfficeQA、DocVQA、LiveMathematicianBench、ALFWorld、SearchQA、OlympiadBench、Omni-MATH、GDPVal、Minecraft、WebArena、GAIA、SWE-bench 等。
- **URL、arXiv 链接/编号、DOI、文件路径、代码标识符**（如 `best_skill.md`、`SKILL.md`、`CLAUDE.md`、`AGENTS.md`、`SLOW_UPDATE_START`、`openpyxl`、`codex_trace_summary.txt`、`L_t`、`D_sel`、`r(s)`）。
- **数字、百分比、指标串、版本号**：`+23.5pt`、`58.8->82.3`、`2:1:7`、`x2.5-x5.3`、`0.6M-3.6M/pt` 等原样保留。
- **受控枚举词（taxonomy tokens）**：`rollout_optimization`、`imitation_demonstration`、`population_evolutionary`、`co_evolutionary`、`reward-based`、`held-out`、`sleep-time`、`inter-test-time`、`intra-test-time`、`on-policy`、`off-policy`、`outcome`、`process`、`general`、`specialized`、`skill-only`、`skill-tool`、`skill-skill`、`generator-verifier`、`skill-prompt` 等。出现在句首或作分类标签时保留英文。
- **常见缩写**：DAG、LLM、RL、SFT、MCP、SOP、CLI、API、VQA、MCQ、QA。

## 统一术语表（中文译文）
| 英文 | 译文 |
|---|---|
| text-space optimization | 文本空间优化 |
| non-gradient | 非梯度 |
| rollout | rollout（保留） |
| reflection | 反思 |
| textual learning-rate | 文本学习率 |
| edit budget | 编辑预算 |
| bounded add/delete/replace | 有界 add/delete/replace |
| rejected-edit buffer | rejected-edit buffer |
| negative feedback | 负反馈 |
| anti-pattern | anti-pattern（保留） |
| inference-time | 推理期 |
| training-time | 训练期 |
| forward/backward pass | 前向 / 反向 |
| momentum | 动量 |
| epoch / minibatch | epoch / minibatch（保留） |
| held-out validation gate | 留出验证门控 |
| held-out (selection/test) split | 留出（选择/测试）集 |
| strict-improvement | strict-improvement（保留） |
| teacher / student model | teacher / 学生模型（或教师模型/学生模型） |
| optimizer | optimizer |
| (frozen) target model | （冻结）目标模型 |
| agent harness | agent harness |
| eval-hacking | eval-hacking（保留） |
| doc-bloat / doc_bloat | 文档膨胀 |
| regression (risk) | 回归（风险） |
| human-in-the-loop | 人工在环 |
| staging | 暂存 |
| backup / rollback | 备份 / 回滚 |
| Pareto front | Pareto 前沿 |
| cross-model / cross-harness / cross-benchmark | 跨模型 / 跨 harness / 跨基准 |
| general / specialized | general / specialized（保留枚举） |
| exact-match | exact-match（保留） |
| success_rate | success_rate（保留） |
| generalization | 泛化 |
| sample efficiency | 样本效率 |
| human-in-the-loop | 人工在环 |
| curator loop | curator loop（保留） |
| imitation / demonstration | 模仿 / 示范 |
| workflow | workflow（保留） |
| insight | insight（保留）或 见解 |

机构名：知名机构用其中文规范名（Microsoft→Microsoft、Google→Google、Anthropic→Anthropic、Shanghai Jiao Tong University→上海交通大学、Tongji University→同济大学、Fudan University→复旦大学 等）；保持自然即可。

## 风格
- 句末用中文句号「。」；并列用中文顿号「、」或「；」；括号用半角或全角均可但全文一致（范例用半角括号包英文标识符）。
- 保留原文的数字-箭头-数字写法（`41.8->80.7`）、范围号 `x2.5-x5.3`。
- 英文专有名词与中文之间不加空格也行，范例风格是「中英紧贴」（如「在 GPT-5.5 上」）。
- 长句可适当断句，但不丢信息。

## 自检
翻译写完后运行：
```
python3 -m json.tool results.zh/<file>.json > /dev/null && echo OK
```
失败则修正后重试，确保合法 JSON 再结束。
