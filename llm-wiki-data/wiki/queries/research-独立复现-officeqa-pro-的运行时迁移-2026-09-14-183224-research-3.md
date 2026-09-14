---
type: query
title: "Research: 独立复现 OfficeQA Pro 的运行时迁移"
created: 2026-09-14
origin: deep-research
tags: [research]
---

# Research: 独立复现 OfficeQA Pro 的运行时迁移

我会按项目 Wiki 规范先核对当前状态与知识图谱，再基于给定来源形成中文综合页；当前环境是只读的，因此若无法落盘，我会交付可直接保存的 Markdown 内容。当前工作区为只读，无法写入。以下为可保存至 `wiki/synthesis/officeqa-pro-runtime-migration.md` 的完整草稿：

```markdown
---
type: synthesis
status: draft
title: "独立复现 OfficeQA Pro 的运行时迁移"
created: 2026-09-14
updated: 2026-09-14
source_id: p-72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
content_version: sha256:72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
sources: ["raw/sources/2607.16387v2.pdf"]
tags: [OfficeQA-Pro, grounded-reasoning, runtime-migration, reproducibility, evaluation]
related: [AdaMAST, adaptive-failure-taxonomy, taxonomy-conditioned-consumer, phase-specific-taxonomy, actionable-verification-criterion, reliable-resolution-conversion, feedback-injection-location]
---

# 独立复现 OfficeQA Pro 的运行时迁移

## 范围与核心判断

此处的“运行时迁移”应被限定为：将一个既有的、由失败轨迹归纳出的运行时反馈流程，移植到 OfficeQA Pro 的文档问答智能体中；它不是迁移模型权重，也不能仅凭更换底座模型或解析器后分数上升而宣称迁移成功。较合适的对象是 [[entities/AdaMAST|AdaMAST]] 所代表的流程：通过 [[concepts/adaptive-failure-taxonomy|自适应失败分类体系]] 诊断轨迹，并由 [[concepts/taxonomy-conditioned-consumer|分类体系条件化消费组件]] 在规划、检索、计算或验证检查点使用这些诊断。[14]

OfficeQA Pro 面向跨文档、可核验的 grounded reasoning：其语料为近百年的 U.S. Treasury Bulletins，约含 89,000 页及超过 2,600 万个数值；133 个问题同时要求文档解析、检索和定量分析。[1] 因而该任务适合检验反馈机制是否能跨越软件工程与金融文档推理的领域差异，但不能将其简化为普通的文本检索评测。

现有 Wiki 中对 [[sources/2607.16387v2|Fantastic Adaptive Taxonomies and How to Use Them]] 的整理记录了一个直接相关但证据有限的结果：在匹配的 gate 条件下，OfficeQA Pro 的严格准确率从 control 的 44.4%（59/133）升至含 AdaMAST 的 51.9%（69/133）；配对 McNemar 检验为 `p ≥ 0.10`。[14] 这应视为待独立验证的效应估计，而不是已确证的普遍改进。

## 复现问题与成功标准

主要问题应预先注册为：

> 在冻结的 OfficeQA Pro 语料、题目、模型、工具接口、检索与解析管线、预算和评分器下，运行时反馈是否比不含该反馈的匹配 harness 更稳定地提高严格准确率？

成功不应只定义为单次总分更高，而应同时满足：

- 133 题上的严格准确率及配对题目结果可复算；
- 多个随机种子或独立重复中，增益方向保持一致；
- 基线与迁移组的模型、解析表示、检索资源、工具权限、上下文窗口、最大轮数、重试次数及预算匹配；
- 每个答案保留证据定位、计算过程、工具调用与终止理由；
- 报告 token、成本、墙钟时间、失败率与方差，而不只报告最佳分数。[9][13]

这一设计用于区分 [[concepts/reliable-resolution-conversion|可靠解决转化]] 与能力边界扩展：若迁移组主要让原本偶尔答对的问题变得稳定答对，则属于可靠性收益；若稳定解决基线在所有重复中均无法解决的问题，才可谨慎讨论能力边界变化。[14]

## 冻结的评测条件

复现前应登记并校验以下版本：

| 对象 | 必须冻结的信息 |
|---|---|
| 基准 | OfficeQA Pro 题目 JSON、参考答案、评分器、语料清单及各文件哈希 |
| 解析表示 | 原始 PDF 或解析后结构化表示；表格序列化格式、解析器版本与失败处理 |
| 智能体 | 模型名称与 API 版本、system prompt、温度、最大 token、工具定义与重试策略 |
| 检索 | 索引构建脚本、分块规则、嵌入模型、`grep`/文件搜索接口、排序与重排规则 |
| 预算 | 单题 token 上限、调用数、并发度、超时、成本上限与是否允许投票 |
| 评分 | 严格匹配规则、数值容差、单位和舍入规则、无答案与超时的计分方式 |

OfficeQA 的公开说明将任务描述为：智能体获得问题及可由 bash 工具访问的 Treasury Bulletin 解析文本，并产出精确数值、文本或结构化答案。[5] 因此，若迁移实验改用了不同的文件接口、网页搜索、人工挑选上下文或额外专有索引，就不再是对该条件下运行时反馈的独立复现。

解析表示必须单列为实验因素。原始报告称，`ai_parse_document` 产生的结构化表示带来平均 16.1% 的相对性能增益。[2] 这说明“反馈有效”与“输入表示更好”是可混淆的两种解释，不能在迁移组单独启用高质量解析。

## 建议的最小实验矩阵

建议先做以下三组，而非直接比较不同厂商模型：

| 组别 | 运行时行为 | 用途 |
|---|---|---|
| A：固定基线 | 固定 [[concepts/agentic-harness|Agentic Harness]]；无分类反馈 | 建立可复算的原始表现 |
| B：匹配 gate | 与 C 相同的监测、gate 和额外开销，但不注入分类诊断 | 隔离“多一次检查”本身的影响 |
| C：运行时迁移 | 与 B 相同，加入分类诊断、对应修复提示和验证检查点 | 估计反馈内容的增量效应 |

每组应至少在多个种子下完整运行 133 题。题目顺序、并发策略和缓存命中也应固定或随机化平衡；否则上下文泄漏、服务波动或缓存暖启动可能制造虚假的组间差异。

若资源允许，可增加两个消融组：将结构化代码替换为语义等价的自然语言摘要，以及改变反馈注入位置。已有结果表明，反馈内容相同而表达格式变化时，结构化代码未被证明普遍优于自然语言；[[concepts/feedback-injection-location|反馈注入位置]] 本身也可能显著改变表现。[14]

## 面向 OfficeQA Pro 的运行时诊断

迁移时不应原封不动复用软件工程中的失败代码。应保持 [[concepts/phase-specific-taxonomy|阶段特定分类体系]] 的结构，而使具体代码适应 OfficeQA Pro 的任务链：

| 阶段 | 候选诊断 | 可操作修复或验证 |
|---|---|---|
| 规划 | 未分解跨年、跨文件或多表问题 | 明确所需年份、报表类型、指标定义和运算链 |
| 检索 | 命中同名但错误期间、版本或表格 | 要求至少一条独立证据；记录文档日期、表题和行列标签 |
| 解析 | 表头层级、单位、负号、脚注或 OCR 读取错误 | 回看原始页面或结构化表格，保留单元格坐标和单位 |
| 计算 | 分母、总体/样本定义、舍入时机或时间口径错误 | 输出中间量；用独立计算或脚本复核 |
| 验证 | 仅验证数值而未验证来源、时间或修订状态 | 将答案、证据、单位、年份及运算逐项对照题意 |

上述“修订状态”尤其重要：二手总结指出，早期报告中的数值可能是估计值，而后续报告可能给出修订值；该说法应在原始 OfficeQA Pro 论文及题目轨迹中逐题复核，不应直接当作基准的已验证失败分类。[8]

每个诊断都必须映射到 [[concepts/actionable-verification-criterion|可操作的验证标准]]，例如“引用单元格的年份与题目年份一致”“答案单位与表头一致”“公式中的所有输入均可追溯”。仅记录抽象标签而不改变后续行动，不能构成可测试的运行时迁移。

## 记录、统计与审计

每题应保存机器可读轨迹，至少包括：题目 ID、模型和 harness 配置哈希、检索到的文件与片段、表格表示、诊断代码、触发的修复动作、最终证据位置、中间计算、答案、评分结果、token、成本和耗时。可以借鉴 CocoaBench 对失败轨迹进行紧凑重构和多标签分类的做法，但不应把截断日志替代为原始可审计轨迹。[11]

主报告应含有：

- 每组的 `correct / 133`、严格准确率、置信区间及每种子的结果；
- A–C 与 B–C 的逐题配对列联表，以及双侧精确 McNemar 检验；
- 解析模式、题型和阶段诊断下的分层结果；
- token、成本、延迟、工具调用次数和超时率；
- 仅 C 成功、仅 B 成功、双方成功、双方失败的题目计数；
- 失败轨迹样本及其对应证据，而非只展示成功案例。

成本、延迟、成功率和方差的联合披露是必要的：长时运行的智能体可通过额外尝试或并发获得分数，但这不等价于更高效或更可靠的系统。[9][13]

## 已知不确定性与不应比较的结果

OfficeQA Pro、OfficeQA 与 OfficeQA Pro V2 不是可互换的评测对象。V2 使用约 120,000 页 U.S. Treasury Accounts of Receipts and Expenditures 与 90 道问题；其默认 harness 与专门开发智能体的结果不能与原版 133 题的迁移结果直接横向比较。[3]

原始来源的结论也随访问条件变化：仅依赖参数知识的前沿模型准确率低于 5%，加入网页访问后低于 12%，直接获得语料后平均为 34.1%。[1] 这并不与部分模型在特定 raw-PDF 或解析配置下得到更高分矛盾，但要求报告准确的模型、harness、解析格式和预算。[8]

llm-stats.com 给出的 0–1 排行分数及模型排名缺少与论文实验相同的 harness、语料版本和评分配置说明，且其对 OfficeQA Pro 的任务描述比主要来源更宽泛。[6] 它可作为外部观察，不能作为独立复现的基线或目标分数。

当前证据最大的缺口是：研究来源中没有提供完整的运行时迁移实现、逐题轨迹、随机种子重复和严格预算匹配的原始工件。因此，44.4% 到 51.9% 的差异应报告为待验证假设，而非已完成的因果归因。[14]

## 建议补充的来源与工件

优先获取：

1. OfficeQA Pro 原始论文 PDF、附录、官方代码仓库、题目与评分器版本；
2. 产生 `ai_parse_document` 表示的确切配置、版本和表格序列化规则；
3. [[sources/2607.16387v2|Fantastic Adaptive Taxonomies and How to Use Them]] 中 OfficeQA Pro 实验的完整 prompt、gate、失败代码、逐题输出和预算；
4. 运行模型的 API 版本、采样参数、服务日期和工具版本；
5. Grounded Reasoning Cup 的评测协议及任何可公开的提交工件；
6. 原始 PDF 页面与结构化解析结果的配对样本，用于审计表格和修订值错误。

## 参考来源

[1] OfficeQA Pro: An Enterprise Benchmark for End-to-End Grounded Reasoning，arXiv。  
[2] OfficeQA Pro: An Enterprise Benchmark for End-to-End Grounded Reasoning，Hugging Face 论文页。  
[3] Introducing OfficeQA Pro V2: A New Benchmark for Enterprise Grounded-Reasoning，Databricks Blog。  
[4] Introducing OfficeQA: A benchmark for end-to-end grounded reasoning，Databricks Blog。  
[5] OfficeQA，EvalScope 文档。  
[6] OfficeQA Pro Leaderboard，llm-stats.com。  
[8] OfficeQA Pro: Why Your Frontier Model Fails at Real-World Enterprise Reasoning，WisPaper。  
[9] Benchmark Is Only Half the Story，Medium。  
[11] CocoaBench: Evaluating unified digital agents in the wild，arXiv。  
[13] From benchmarks to deployment: a comprehensive review of agentic AI evaluation，Artificial Intelligence Review。  
[14] [[sources/2607.16387v2|Fantastic Adaptive Taxonomies and How to Use Them]]。
```

## References

1. [OfficeQA Pro: An Enterprise Benchmark for End-to-End Grounded Reasoning](https://arxiv.org/html/2603.08655v1) — arxiv.org
2. [Paper page - OfficeQA Pro: An Enterprise Benchmark for End-to-End Grounded Reasoning](https://huggingface.co/papers/2603.08655) — huggingface.co
3. [Introducing OfficeQA Pro V2: A New Benchmark for Enterprise Grounded-Reasoning | Databricks Blog](https://www.databricks.com/blog/introducing-officeqa-pro-v2-new-benchmark-enterprise-grounded-reasoning) — databricks.com
4. [Introducing OfficeQA: A benchmark for end-to-end grounded reasoning | Databricks Blog](https://www.databricks.com/blog/introducing-officeqa-benchmark-end-to-end-grounded-reasoning) — databricks.com
5. [OfficeQA | EvalScope](https://evalscope.readthedocs.io/en/v1.10.0/benchmarks/officeqa.html) — evalscope.readthedocs.io
6. [OfficeQA Pro Leaderboard](https://llm-stats.com/benchmarks/officeqa-pro) — llm-stats.com
8. [OfficeQA Pro: An Enterprise Benchmark for End-to-End Grounded Reasoning](https://www.wispaper.ai/en/blog/officeqa-pro-enterprise-benchmark-end-to-end-grounded-reasoning-20260312/eng) — wispaper.ai
9. [Medium](https://medium.com/@bijit211987/benchmark-is-only-half-the-story-a20255d0098a) — medium.com
11. [CocoaBench: Evaluating unified digital agents in the wild](https://arxiv.org/html/2604.11201v2) — arxiv.org
13. [From benchmarks to deployment: a comprehensive review of agentic AI evaluation | Artificial Intelligence Review | Springer Nature Link](https://link.springer.com/article/10.1007/s10462-026-11571-0) — link.springer.com
