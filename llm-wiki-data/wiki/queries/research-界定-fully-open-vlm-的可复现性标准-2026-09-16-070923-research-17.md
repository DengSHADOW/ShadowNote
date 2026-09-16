---
type: query
title: "Research: 界定 fully open VLM 的可复现性标准"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: 界定 fully open VLM 的可复现性标准

我会使用 `wiki-maintenance` skill 按“知识问答/综合页”范围处理：先核对项目状态、长期约定、Wiki 索引与相关现有来源页，再基于给定材料形成中文、可入库的综合页面；不会擅自写入 Wiki，也不会把宣传性二手材料与论文原文赋予同等证据权重。当前目录是数据子目录，`AGENTS.md` 中的 `docs/` 与 `.agents/` 路径按仓库根目录书写，因此第一次读取未命中。我正在定位实际目录并继续按同一规范读取；这不会修改任何文件。# fully open VLM 的可复现性标准

## 定义

**fully open VLM** 应指这样一类 [[Molmo2|VLM]]：研究者不仅能够下载最终权重并运行推理，而且能够在法律许可、技术依赖和科学证据三个层面，审计并重新执行从原始数据到评测结果的完整过程。

这一概念应与以下术语区分：

- **open weights**：只保证模型参数可获得；通常不足以解释参数由哪些数据、代码和训练决策产生。[11][14][15]
- **可运行发布**：第三方可以按照说明完成推理，但不一定能重建训练数据或重新训练模型。
- **可复现训练发布**：第三方能够取得或确定性重建训练数据，执行训练流程，并在预先声明的容差内得到相当结果。
- **fully open VLM**：除训练可复现外，还要求关键上游组件、数据来源和自动生成监督的依赖具有闭合、可审计的开放谱系。
- **已独立复现**：已有与原作者相对独立的第三方完成重跑并公开结果。发布材料齐全只能证明“具备复现条件”，不能自动证明“已经复现”。

Open Source Initiative 同样指出，开放最终权重并不等于开放整个 AI 系统；但其定义也不必然要求集中发布全部原始训练数据，而强调理解、使用、修改和分享系统所需的信息与权利。[11][15] 因此，“开放性”和“可复现性”彼此相关但不等价：前者关注访问、审计和使用自由，后者关注能否重新执行并验证科学结果。

## 为什么 VLM 需要端到端标准

典型 VLM 至少包含视觉编码器、跨模态 connector 或 projection layer、语言模型，以及连接这些部分的数据处理和训练流程。[5] 仅开放最终组合模型的权重，无法回答以下问题：

- 视觉编码器是否用不可追溯的封闭数据预训练；
- 语言模型底座的训练来源是否可审计；
- caption、QA 或 grounding 标签是否由 proprietary model 生成；
- 数据过滤、去重、采样和混合比例能否重建；
- 论文中的成绩是否依赖未发布的 prompt、解析器或后处理；
- 当前下载到的代码、数据和权重是否就是生成论文结果的版本。

PerceptionLM 将 proprietary teacher 蒸馏视为科学测量上的障碍：即使学生模型和表面训练集被公开，未知 teacher 的训练数据与行为仍会进入监督信号，使性能提升难以归因于公开的方法或数据。[1][2][3][4] 这表明 fully open VLM 的审计对象必须是完整生成链，而不只是最终模型目录。

## 强制通过条件

下列项目适合作为“fully open”声明的最低门槛。任一关键条件不满足时，应使用更窄的标签，例如“open-weight VLM”“open-data VLM”或“训练代码待发布”，而不是笼统称为 fully open VLM。

| 维度 | 最低要求 | 不通过的典型情形 |
|---|---|---|
| 权重与架构 | 发布最终权重、完整架构定义、tokenizer、processor、配置和所有必要 adapter；标明精确版本与哈希 | 只有 API；缺少 connector；权重与代码版本无法对应 |
| 上游模型谱系 | 列出视觉编码器、语言模型和其他 pretrained components 的精确 checkpoint、版本、许可证及训练数据可审计程度 | 使用 closed-data encoder，却只因最终权重开放而宣称 fully open |
| 训练数据 | 提供数据本体，或提供能够合法、确定性重建同一训练语料的 manifest、来源标识、版本、哈希和脚本 | 只列数据集名称；URL 已失效；关键私有数据不可获得 |
| 数据变换 | 发布下载、解码、过滤、去重、清洗、切分、采样、混合和 augmentation 流程及参数 | 只发布整理后的统计量，无法恢复实际训练样本 |
| 监督信号谱系 | 标明每类人工、规则、模型生成和合成标签的来源；生成模型、prompt、采样参数和过滤规则可重放 | 关键标签来自不可访问的 proprietary VLM |
| 训练实现 | 发布实际使用的训练代码、配置、超参数、优化器、scheduler、随机种子、精度设置和 checkpoint 策略 | 只有伪代码或通用框架示例 |
| 运行环境 | 固定软件依赖、容器或 lockfile，并报告硬件、并行策略、训练时长和计算量 | 安装说明只覆盖推理，未描述训练环境 |
| 中间证据 | 发布日志、数据统计和足以定位偏差的 intermediate checkpoints，或说明无法发布的具体原因 | 只有最终 checkpoint，无法区分数据、训练和报告错误 |
| 评测链 | 发布 benchmark 版本、split、prompt、解码参数、解析器、后处理、指标实现和原始预测 | 只报告汇总分数；依赖私有 evaluator 或未公开后处理 |
| 法律可用性 | 分别说明代码、权重、数据及第三方组件的许可证、再分发限制和使用限制 | README 写“open source”，实际许可证禁止必要的修改或再分发 |
| 版本固定 | 为论文结果提供不可变 release、commit、数据快照、哈希和变更记录 | 持续更新的主分支取代论文使用版本 |
| 第三方验证 | 提供独立重跑所需材料；“已复现”声明必须附第三方环境、成本、偏差和失败记录 | 作者自行运行一次即称为独立复现 |

## 谱系闭合原则

fully open 的核心不是“发布物数量多”，而是**每个影响模型参数或论文结论的关键节点都能沿依赖图追溯到可访问、可审计的来源**。

应分别审计以下两条路径：

1. **参数谱系**：原始数据 → 数据变换 → 训练监督 → 上游 checkpoint → VLM 训练 → 最终权重。
2. **证据谱系**：测试数据 → prompt 和输入处理 → 模型输出 → 解析与后处理 → 指标 → 论文表格。

如果某个 closed component 只用于非实质性文案润色，不影响训练样本选择、标签、参数或评测结论，可以记录为外围依赖。若它决定了训练标签、数据过滤、难例选择或评价分数，则属于关键谱系，不能从 fully open 审计中排除。

## 数据无需集中再发布，但必须可重建

“开放数据”不应机械地等同于“把所有媒体文件重新打包上传”。版权、隐私和第三方许可可能禁止再分发原始图像或视频。[11][15] 在这种情况下，仍可通过以下材料满足较严格的可复现要求：

- 稳定的原始来源标识和取得日期；
- 样本级 manifest、文件哈希与许可证信息；
- 下载或访问脚本；
- 排除、过滤和去重规则；
- 确定性的训练、验证和测试切分；
- 对删除、失效或受限样本的数量与影响分析；
- 可验证的派生标注以及从原始内容到训练样本的转换脚本。

如果大量样本已不可取得，使第三方无法重建具有统计等价性的训练集，则该发布最多是“数据谱系透明”，不能视为严格的训练可复现。

## 合成数据和 proprietary teacher

合成数据本身不破坏开放性；问题在于其生成链是否可审计和重放。应至少公开：

- 生成模型及精确版本；
- system prompt、user prompt 和模板；
- decoding 参数、随机性设置和调用时间；
- 输入样本来源；
- 过滤、排序、人工修订及质量控制过程；
- 生成前后样本数量；
- proprietary service 的依赖比例。

如果核心监督由无法下载、版本可能漂移且训练来源未知的 proprietary VLM 生成，即使最终生成文本被发布，第三方也只能复用生成结果，不能完整重建数据生产过程。PerceptionLM 对黑箱蒸馏的批评正是针对这种不可观测依赖。[1][2][3][4]

因此可以采用以下命名：

- 数据由开放模型或确定性程序生成，完整过程可重放：**开放合成数据**。
- 发布生成结果和 prompt，但生成模型不可获得：**公开派生数据，生成链不闭合**。
- 未披露 teacher、prompt 或过滤过程：**不可审计蒸馏数据**。

只有第一种通常满足严格的 fully open 标准。

## 结果复现的判定方式

大规模训练往往无法做到逐 bit 一致，因此可复现性不应简单要求权重哈希相同。发布者应事先声明分层验收指标：

- **数据一致性**：样本数、模态分布、来源分布、去重率和 token 数处于预定容差内。
- **训练一致性**：loss 曲线、梯度统计、阶段性 checkpoint 指标没有无法解释的系统偏差。
- **任务一致性**：主要 benchmark 的绝对差值或置信区间不超过预先声明阈值。
- **结论一致性**：论文中的主要模型排序、消融方向和定性结论在重跑中保持。
- **成本一致性**：计算量、显存、训练时间和失败重启成本与报告基本相符。

只复现一次推理分数属于**评测复现**；从公开初始状态重新训练并得到相当结果，才属于**训练复现**；从原始来源重建数据和所有上游组件，则属于更严格的**端到端复现**。

## 建议的分级标签

| 等级 | 标签 | 含义 |
|---|---|---|
| R0 | API-only | 只能通过托管接口使用 |
| R1 | open weights | 可取得最终参数，但训练链不完整 |
| R2 | inference-reproducible | 推理环境、处理器和评测流程可重建 |
| R3 | training-reproducible | 数据、代码、配置和环境足以重跑主要训练 |
| R4 | lineage-complete fully open | 所有关键上游模型、监督和评测依赖均具有闭合开放谱系 |
| R5 | independently reproduced | 独立第三方已完成重跑并公开结果与偏差 |

R4 描述发布物的性质，R5 描述外部验证状态。没有第三方复现不应阻止一个项目被评为“具备 R4 条件”，但它不能被描述为“已经得到独立复现”。

## [[Molmo2]] 案例

[[2601.10611v4|Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding]] 展示了为什么需要按组件而不是按项目口号判定开放性。

论文将 [[Molmo2]] family 概括为开放权重、开放数据、无 proprietary VLM distillation，并报告开放代码。[6] 但同一论文也明确说明其视觉编码器 SigLIP 2 使用 closed data，并指出当时没有具有竞争力的 open-data encoder。[6] 因而，对 Molmo2-4B 和 Molmo2-8B 更准确的描述是“VLM 阶段具有开放数据和开放权重，但视觉编码器谱系没有完全开放”，而不是无条件的端到端 fully open。

Molmo2-O-7B 使用 OLMo 3 作为语言模型底座，缩小了语言侧的谱系缺口，但仍不能仅凭这一点消除 SigLIP 2 的视觉侧问题。[6][10] 视频解说将其描述为能够追溯每个参数的数据来源，这一表述与论文承认的 closed-data SigLIP 2 存在张力，不能替代论文和 artifact 的逐项审计。[6][10]

此外，Hugging Face 模型卡一方面强调开放科学，另一方面曾写明训练代码、评测和 intermediate checkpoints 将在之后发布。[8][9] “计划发布”不等于“当前可获得”，因此开放等级必须绑定审计日期和精确 release。若相关 artifact 后来确已发布，应更新审计结果，但不应把后来的状态倒推为论文发布时已经满足。

## PerceptionLM 案例

PerceptionLM 明确把“fully open and reproducible framework”作为研究目标，并尝试在不依赖 proprietary model distillation 的情况下研究标准训练流程与大规模合成数据。[1][2][3][4] 这一方向解决了 teacher 不透明造成的因果归因问题，但“研究目标是 fully open”仍不是充分证据。

对 PerceptionLM 的完整定级仍需检查：

- 实际发布的数据与数据生成程序；
- 合成数据生成模型及其训练谱系；
- 视觉编码器和语言模型底座；
- 训练与评测代码是否对应论文版本；
- 许可证和第三方数据的可取得性；
- 是否已有独立训练重跑。

现有摘要级材料可以支持其开放研究动机，却不足以单独证明所有 R4 条件已经满足。[1][2][3][4]

## 术语混用带来的风险

二手指南常把“权重可下载”“采用 Apache 2.0”或“能够本地运行”直接概括为 open source。[12][14] 这会忽略数据、上游 checkpoint 和训练过程的开放性。甚至同一项目在论文、模型卡、API 聚合页面和视频解说中也可能使用不同口径。[6][7][8][9][10]

Reddit 对 open weights 与 open source 的简化区分表达了常见直觉，但缺少正式定义和逐组件标准，不适合作为最终判定依据。[13] 实际审计应优先采用论文、官方仓库、数据卡、模型卡、许可证和不可变 release；第三方介绍只用于发现线索。

## 当前材料中的矛盾与证据缺口

1. **“fully open”与 closed-data encoder 冲突**：[[Molmo2]] 的开放数据主张主要覆盖 VLM 训练阶段，而 SigLIP 2 的训练数据并不开放。[6]
2. **“开放代码”与“稍后发布”存在时间差**：论文表格与模型卡可能描述目标状态，而 artifact 页面显示某些材料在当时尚未提供。[6][8][9]
3. **论文目标与实际发布状态未区分**：PerceptionLM 的摘要说明其研究方向，但给定材料没有形成完整 artifact 清单。[1][2][3][4]
4. **二手来源口径不稳定**：部分指南把 Community License、open weights 和 open source 混用，无法承担严格分类。[12][14][15]
5. **缺少独立端到端重跑**：现有材料主要来自作者或项目页面，没有给出第三方从数据重建到训练和评测的完整复现报告。
6. **缺少审计时间戳**：模型卡会更新；未绑定 commit、文件哈希和访问日期的结论可能迅速过时。[8][9]

## 推荐审计表述

为避免二元标签掩盖差异，模型发布或综述可以使用以下格式：

> 该模型在审计日期满足 R2/R3：最终权重、推理代码、部分训练数据和评测程序可获得。其视觉编码器依赖 closed-data checkpoint，部分训练 artifact 尚未发布，因此不满足 lineage-complete fully open 标准。当前未发现独立端到端训练复现。

这种表述同时回答“开放了什么”“缺少什么”“何时检查”以及“是否被第三方复现”，比单独使用“open source”或“fully open”更可验证。

## 值得补充的来源

后续应优先寻找以下一手证据：

- PerceptionLM 的正式论文 PDF、官方代码仓库、模型卡、数据卡和许可证；
- [[Molmo2]] 训练代码、evaluation commit、intermediate checkpoints 与数据 manifest 的实际发布日期和哈希；
- SigLIP 2 的模型卡、数据说明与许可证，用于确定 closed-data 依赖的准确边界；
- OLMo 3 与 Qwen3 的训练数据、许可证和 checkpoint 谱系；
- Open Source AI Definition 的正式版本，而非二手解释；
- ML reproducibility checklist、数据集文档标准和可复现训练报告；
- 与原作者无关的 clean-room reproduction，尤其是数据重建、完整训练成本和 benchmark 偏差；
- 对不可再分发视觉数据的长期可获取性研究，以区分“有来源列表”与“可实际重建”。

## 结论

fully open VLM 不应由最终权重、单一许可证或作者自述决定。严格标准应同时检查权重、架构、上游 checkpoint、训练数据、合成监督、训练代码、运行环境、评测链、版本固定和法律权利，并要求所有关键依赖形成可审计的闭合谱系。

在这一标准下，[[Molmo2]] 提供了显著高于普通 open-weight release 的开放数据和研究材料，但 closed-data SigLIP 2 以及部分 artifact 的延后发布，使其至少在相关审计时间点不能无条件归为端到端 fully open。[6][8][9] PerceptionLM 则明确提出更严格的开放、可复现研究目标，但仍需通过 artifact 级审计与第三方重跑来确认其实际等级。[1][2][3][4]

## References

1. [NeurIPS Poster PerceptionLM: Open-Access Data and Models for Detailed Visual Understanding](https://neurips.cc/virtual/2025/poster/119876) — neurips.cc
2. [PerceptionLM: Open-Access Data and Models for Detailed Visual Understanding | Research - AI at Meta](https://ai.meta.com/research/publications/perceptionlm-open-access-data-and-models-for-detailed-visual-understanding) — ai.meta.com
3. [Open-Access Data and Models for Detailed Visual Understanding](https://arxiv.org/html/2504.13180v3) — arxiv.org
4. [PerceptionLM: Open-Access Data and Models for Detailed Visual...](https://openreview.net/forum?id=5NkfjxMpWe) — openreview.net
5. [Vision Language Models Guide: The Complete Handbook for ML Teams](https://annotationbox.com/vision-language-models-guide) — annotationbox.com
6. [Molmo2 Open Weights and Data for Vision-Language ...](https://arxiv.org/html/2601.10611v4) — arxiv.org
7. [Molmo2 8B - API Pricing & Benchmarks | OpenRouter](https://openrouter.ai/allenai/molmo-2-8b/activity) — openrouter.ai
8. [allenai/Molmo2-8B](https://huggingface.co/allenai/Molmo2-8B) — huggingface.co
9. [Create README.md · allenai/Molmo2-8B at c0c2b8f](https://huggingface.co/allenai/Molmo2-8B/commit/c0c2b8f6fe93ebec69451f4c4452a9bf2d8a98e2) — huggingface.co
10. [Molmo2: Open Weights and Data for Vision-Language Models ...](https://www.youtube.com/watch?v=GgE_p7pP4Ig) — youtube.com
11. [Open Weights: not quite what you’ve been told – Open Source Initiative](https://opensource.org/ai/open-weights) — opensource.org
12. [Best Open-Source Vision Language Models of 2026](https://www.labellerr.com/blog/top-open-source-vision-language-models) — labellerr.com
13. [The Paradox of Open Weights, but Closed Source](https://www.reddit.com/r/LocalLLaMA/comments/1iw1xn7/the_paradox_of_open_weights_but_closed_source) — reddit.com
14. [Openness in Language Models: Open Source vs Open Weights vs Restricted Weights](https://promptengineering.org/llm-open-source-vs-open-weights-vs-restricted-weights) — promptengineering.org
15. [Kilo - Open Source vs Open Weight AI Models Explained](https://kilo.ai/open-source-vs-open-weight-models) — kilo.ai
