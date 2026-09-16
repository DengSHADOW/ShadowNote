---
type: query
title: "Research: 核验 GPT-4.1 caption F1 与人工偏好的一致性"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: 核验 GPT-4.1 caption F1 与人工偏好的一致性

我会按项目的 Wiki 维护规范先核对现有索引、状态与写作约定，再基于给定来源产出中文综合页；重点会区分“论文明确报告的事实”与“现有材料不足以证明的一致性结论”。当前工作目录本身已是 `llm-wiki-data`，而会话说明中的相对路径以仓库上一级为基准；我正在定位实际文件位置后继续读取，不会据此猜测页面结构。现有材料已经显露出关键边界：Molmo2 论文同时报告 caption F1 与人工偏好，但“同时报告”不等于做过一致性验证。我会回查论文中对应表格与评测协议，确认能否从同一批模型、同一任务和配对样本上计算相关性。为核对 Table 15 的列含义与脚注，我会使用 PDF 工作流读取并校验原论文页面；这一步由 PDF 技能要求执行，因为纯文本摘录容易丢失表格列对齐。它只用于证据核验，不会修改 PDF 或 Wiki 文件。# GPT-4.1 裁判的 caption F1 与人工偏好是否一致

## 结论

现有证据支持一个有限结论：GPT-4.1 裁判生成的 caption F1 与人工 caption 偏好在跨模型总体排序上呈较强正相关，但尚不能证明两者在单条视频、单条 caption 或具体质量维度上具有可靠一致性。

根据 [[2601.10611v4|Molmo2 论文]] Tables 2、15 中共同出现的 21 个模型重新计算：

| 比较范围 | 模型数 | Pearson $r$ | Spearman $\rho$ | Kendall $\tau$ |
|---|---:|---:|---:|---:|
| 全部模型 | 21 | 0.815 | 0.822 | 0.657 |
| proprietary API 模型 | 6 | 0.519 | 0.143 | 0.067 |
| “Open weights only”模型 | 8 | 0.816 | 0.524 | 0.429 |

全部模型的 210 个模型对中，caption F1 与人工 caption Elo 对 174 对给出相同排序，配对一致率约为 82.9%。然而，相关性在 proprietary API 子组中几乎消失，说明总体相关可能部分来自“较弱模型在两项指标上都较低”的模型层级差异，而不是两个评测方法对相近模型具有同等辨别力。[1]

因此，较准确的判断是：**caption F1 可作为粗粒度模型筛选指标，但当前证据不足以支持用它替代人工偏好，尤其不宜据此判断能力接近的模型。**

## 两种评测测量的对象

### GPT-4.1 caption F1

Molmo2-CapTest 包含 693 个与训练集分离的 Creative Commons Vimeo 视频，每个视频至少有四条、最多五条人工 caption。评测首先让 GPT-4.1 将模型 caption 和人工 caption 分解为 distinct atomic statements，再由 GPT-4.1 判断陈述之间是否匹配：

- precision：模型 caption 中得到人工 caption 支持的陈述比例；
- recall：人工 caption 中被模型 caption 覆盖的陈述比例；
- F1：先跨视频平均 precision 和 recall，再取调和平均。[1]

这里的“GPT-4.1 caption F1”指由 GPT-4.1 充当分解器和裁判得到的指标，并不是 GPT-4.1 自己生成 caption 时的 F1。它属于 [[GPT-4-as-judge-多模态评估|LLM-as-a-judge 多模态评估]]。

### 人工 caption 偏好

人工研究使用 450 个开放式 QA 问题和另外 51 个 captioning 视频。标注者比较两个模型输出并给出成对偏好；研究对每个模型对收集 501 个判断，总计超过 105,000 个 ratings，再使用 Bradley–Terry model 和 1,000 轮 bootstrap 计算 Elo。Table 15 另行报告 captioning-specific Elo。[1]

两种评测不仅裁判不同，样本也不同：

- caption F1：693 个视频；
- captioning-specific Elo：51 个视频；
- F1 以事实陈述覆盖为中心；
- 人工偏好还可能考虑连贯性、重复、可读性、重点选择和整体观看体验。

所以，模型级相关不能直接解释为逐样本的一致率。

## 支持一致性的证据

全体 21 个模型的 Spearman $\rho=0.822$，表明两种指标通常能把明显较弱和较强的 caption 模型分开。[1] 若将问题限定为粗粒度 benchmark ranking，这是一项实质性的正面证据。

[[Molmo2]] 家族内部也给出相同排序：

| 模型 | caption F1 | 人工 caption Elo |
|---|---:|---:|
| Molmo2-8B | 43.2 | 1049 |
| Molmo2-O-7B | 40.1 | 1019 |
| Molmo2-4B | 39.9 | 1004 |

不过这里只有三个同源模型，不能据此估计一般化效度。[1]

## 不一致与排序反转

两项指标对若干接近或较强模型给出明显不同的排序。以下名次由本页直接按 Table 2 的 F1 和 Table 15 的 caption Elo 重新排序，而非照录论文的 Rank 列。[1]

| 模型 | F1 名次 | 人工偏好名次 | 名次差 |
|---|---:|---:|---:|
| GPT-5 mini | 1 | 6 | 5 |
| Gemini 2.5 Pro | 5 | 1 | 4 |
| Molmo2-8B | 4 | 8 | 4 |
| Gemini 3 Pro | 8 | 3 | 5 |
| Qwen3-VL-8B | 10 | 5 | 5 |
| Qwen3-VL-4B | 13 | 7 | 6 |
| GLM-4.1V-9B | 16 | 10 | 6 |

Qwen3-VL 与 Molmo2 的同规模比较尤其突出：Molmo2-4B/8B 的 caption F1 均高于 Qwen3-VL-4B/8B，但人工 caption Elo 则由两个 Qwen3-VL 模型领先。这说明 caption F1 对“事实覆盖较好但整体阅读体验较差”与“覆盖较少但更受人偏好”的输出可能作出不同判断。[1]

论文自己的定性分析也指出，Molmo2 的 caption 有时会在结尾产生重复或无意义内容，人工标注者会因此降低偏好。[1] 这与 [[自动指标与人工感知质量错位]]相符：如果 atomic-statement 分解没有充分惩罚重复、篇章失控或低价值细节，F1 就可能高估人工不喜欢的长 caption。

## 潜在偏差与未受控因素

### 长度和表面质量

既有 LLM-as-a-judge 研究报告 verbosity、fluency、formality 和 self-enhancement 等偏差。[6][7][8][9] Atomic-statement precision 理论上会惩罚没有依据的额外细节，但其实际效果取决于 GPT-4.1 如何切分、合并和匹配陈述。若冗余句被合并，或新增细节提高 recall 而只造成较小 precision 损失，长 caption 仍可能占优。

这些文献只能建立一般方法学风险，不能证明 GPT-4.1 在 Molmo2-CapTest 上实际产生了多大偏差。

### 同一家族裁判偏好

GPT-4.1 可能对 OpenAI 风格输出存在 self-enhancement bias，但当前表格不能识别该效应：没有替代 judge、盲化改写或风格控制实验。GPT-5 mini 的 F1 排名第一但人工偏好仅第六，也不支持把全部差异简单归因于稳定的 OpenAI-family 偏好。[1][8][9]

### atomic statement 的双重误差

分数同时依赖：

1. GPT-4.1 是否正确分解 atomic statements；
2. GPT-4.1 是否正确判断两个陈述语义匹配。

Atomic proposition 分解在信息抽取中可能提高 recall，但这类结果并不验证其作为视频 caption 质量指标的人工一致性。[11] 一般逻辑学中的 atomic proposition 定义也无法替代对自然语言分解协议的实证校准。[12][14][15]

## 来源之间的边界与矛盾

Allen Institute for AI 的介绍称 Molmo2-8B 在 open-weight human preference evaluation 中领先，并超过 GPT-5 和 Claude Sonnet 4.5。[4] 这与 Table 15 的 overall Elo 相符，却不适用于 captioning-specific Elo：在 caption 子评测中，GPT-5 为 1136，Molmo2-8B 为 1049；Qwen3-VL-8B 也以 1105 领先 Molmo2-8B。[1] 因此不能用 overall human preference 证明 caption F1 的有效性。

其他来源的证明力有限：

- Molmo2-Cap dataset card 提到 `annotation_score` 和 GPT-4.1/GPT-5 生成文本，但所给材料没有定义该字段，也没有提供与人工偏好的配对验证。[2]
- YouTube 摘要中的 F1 是 video pointing F1，不是 caption F1。[3]
- GPT-4.1 产品宣传文没有可核验的 judge-human alignment 实验。[5]
- Label Studio 与 LinkedIn 内容可提示已知偏差，但不是 Molmo2 caption 评测的直接证据。[8][10]
- 来源[6]与[9]基本对应同一项研究，不应作为两份独立复现证据。

## 证据缺口

现有资料没有提供以下关键分析：

- 693 个 F1 视频与 51 个人工偏好视频是否有重叠；
- 同一 caption 上 GPT-4.1 分数与人工选择的逐样本相关性；
- 人工标注者数量、agreement、tie 处理和质量控制细节；
- caption-specific Elo 的置信区间；
- GPT-4.1 的精确模型版本、prompt、随机性和重复运行稳定性；
- atomic-statement 分解与匹配的人工准确率；
- caption 长度、重复率和模型家族对相关性的影响；
- 使用独立 judge 或不同 judge ensemble 后的排名变化。

## 建议的核验实验

最有说服力的后续实验应在同一批视频和同一批模型输出上同时收集两种评价：

1. 公开每条 caption 的 GPT-4.1 precision、recall、F1、atomic statements 和匹配轨迹。
2. 让多名人工标注者分别评价事实正确性、细节覆盖、重复、连贯性和总体偏好。
3. 报告逐样本 Spearman、pairwise agreement、校准曲线及 bootstrap 置信区间。
4. 按模型家族、caption 长度和质量接近程度分层，避免由强弱模型混合产生虚高相关。
5. 使用 GPT-4.1、其他 proprietary judge、open-weight judge 和人工 atomic matching 进行交叉验证。
6. 对重复句、流畅但错误的细节、正确但简短的 caption 做受控扰动，以测量 precision、recall 与人工偏好的响应差异。

## 综合判断

目前最稳妥的表述是：

> GPT-4.1 caption F1 与人工 caption Elo 在 21 个模型的总体层面具有较强相关性，但在 proprietary 模型和若干能力接近的模型之间出现显著排序反转。由于两项评测使用不同视频集合，且缺少逐样本配对数据、judge 校准和人工一致性统计，现有证据只能支持粗粒度 convergent validity，不能证明 caption F1 是人工偏好的可靠替代指标。[1]

本页对 Table 2、Table 15 及评测协议的核对基于本地论文原文 :codex-file-citation{path="C:/ShadowNote/llm-wiki-data/raw/sources/2601.10611v4.pdf" purpose="source"}。

- :codex-followup[保存为综合页]{prompt="将这份综合内容保存到 Wiki 的 synthesis 目录，补齐 frontmatter、索引链接并运行 lint。"}
- :codex-followup[生成复算脚本]{prompt="创建一个可复现脚本，从 Molmo2 Tables 2 和 15 的录入数据计算相关系数、排序差和配对一致率。"}
- :codex-followup[设计核验协议]{prompt="把建议的逐样本核验实验写成可直接执行的标注协议和统计分析计划。"}

## References

1. [Molmo2 Open Weights and Data for Vision-Language ...](https://arxiv.org/html/2601.10611v4) — arxiv.org
2. [allenai/Molmo2-Cap · Datasets at Hugging Face](https://huggingface.co/datasets/allenai/Molmo2-Cap) — huggingface.co
3. [Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding (Jan](https://www.youtube.com/watch?v=GgE_p7pP4Ig) — youtube.com
4. [Molmo 2: State-of-the-art video understanding, pointing ...](https://allenai.org/blog/molmo2) — allenai.org
5. [GPT-4.1 Explained: Features, Model Types, Performance, and How to Use It - CertLibrary Blog](https://www.certlibrary.com/blog/gpt-4-1-explained-features-model-types-performance-and-how-to-use-it) — certlibrary.com
6. [Mitigating the Bias of Large Language Model Evaluation | alphaXiv](https://www.alphaxiv.org/abs/2409.16788) — alphaxiv.org
7. [Evaluating and Mitigating LLM-as-a-judge Bias in Communication Systems](https://arxiv.org/html/2510.12462v3) — arxiv.org
8. [In the Loop: LLM-as-a-Judge | Label Studio](https://labelstud.io/videos/in-the-loop-llm-as-a-judge) — labelstud.io
9. [Mitigating the Bias of Large Language Model Evaluation](https://arxiv.org/html/2409.16788v1) — arxiv.org
10. [Avoiding Biases in LLM Evaluation: Position, Verbosity ...](https://www.linkedin.com/posts/adaline_you-set-up-an-llm-judge-to-evaluate-your-activity-7469825666709065729-DEvP) — linkedin.com
11. [LLM-based Atomic Propositions Help Weak Extractors:Evaluation of a Propositioner for Triplet Extraction](https://arxiv.org/html/2604.02866v1) — arxiv.org
12. [Auditing Prospective Fundamental Principles Underlying Atomic Proposition Phenomenon](https://flyriver.com/s/atomic-proposition) — flyriver.com
14. [Atomic Propositions](https://ganelson.github.io/inform/calculus-module/4-ap.html) — ganelson.github.io
15. [Atomic Proposition - (Intro to Semantics and Pragmatics) - Vocab, Definition, Explanations | Fiveable](https://library.fiveable.me/key-terms/introduction-semantics-pragmatics/atomic-proposition) — library.fiveable.me
