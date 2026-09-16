---
type: query
title: "Research: 核查 LLaVA 数据与评测的重叠及评价闭环"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: 核查 LLaVA 数据与评测的重叠及评价闭环

我会按 `wiki-maintenance` 的 query/综合规则处理：先核对项目约定与现有 Wiki 索引，再基于给定来源写成中文页面；本次只返回页面正文，不自行写入仓库。当前工作目录与说明中的相对路径不一致，首轮读取没有找到文件。我会先定位实际仓库结构，再按同一规则继续，不会改动任何内容。# 核查 LLaVA 数据与评测的重叠及评价闭环

## 结论摘要

现有证据支持 [[LLaVA]] 生态中存在三类明确的结构性重叠：

1. **数据集家族重叠**：训练与评测多次使用 COCO、VQAv2、GQA、TextVQA、VisualGenome 等相同数据集家族。
2. **任务与输出协议重叠**：训练和评测采用相近的任务模板及答案格式，例如“单词或短语”“直接输出选项字母”。
3. **生成器与评价者重叠**：GPT-4 同时参与训练数据生成、参考答案生成、开放式回答评分和 [[ScienceQA]] ensemble 裁决，形成明显的 [[GPT-4-as-judge-多模态评估|GPT-4-mediated 评价闭环]]。

但给定来源**不足以证明训练集与测试集存在逐图像或逐样本泄漏**。目前能够确认的是 dataset-level、task-level 和 evaluator-level 的依赖；若要断言 contamination，仍需比较数据清单中的 image ID、question ID、annotation ID，以及近重复图像和文本。

因此，最准确的结论是：

> LLaVA 的主要问题不是已经证实的 train–test 样本泄漏，而是训练数据、任务格式和评价模型之间缺乏充分独立性。这会削弱部分成绩作为开放世界泛化证据的解释力，但不能据此直接判定成绩无效。

## 审计对象与判定标准

本文区分四种容易混淆的“重叠”：

| 类型 | 判定条件 | 方法学含义 |
|---|---|---|
| 数据集家族重叠 | 训练和测试来自同一数据集名称或数据生态 | 可能仅为标准 train/test split，也可能隐藏样本泄漏 |
| 样本级重叠 | 相同图像、问题、答案或近重复样本同时进入训练与测试 | 构成直接 contamination 风险 |
| 任务与格式重叠 | 训练和测试采用相同任务定义、提示模板或输出格式 | 衡量域内适配能力，不一定代表未知指令泛化 |
| 生成—评价闭环 | 同一模型或模型家族既生成训练监督，又生成参考答案或承担评分 | 可能产生风格偏好、标准自洽和共同错误 |

只有第二类可以直接支持“测试集泄漏”的结论。其余三类属于评价独立性问题，应单独报告。

## 原始 LLaVA 的数据来源

[[2304.08485v2|Visual Instruction Tuning]] 通过 [[GPT-assisted-visual-instruction-data-generation]] 构建 [[LLaVA-Instruct-158K]]。其图像来自 COCO，text-only GPT-4 不读取原始像素，而是根据 captions 和带类别、位置的 bounding boxes 生成三类指令数据：

- 58K conversation；
- 23K detailed description；
- 77K complex reasoning。

合计为 158K language-image instruction-following samples。人工标注主要限于少量 seed examples，其余内容通过 few-shot in-context learning 扩展。[1]

这种生成方式意味着监督信号不仅依赖图像，还依赖 COCO captions、object annotations 和 GPT-4 的表达偏好。caption 或 bounding box 中遗漏的内容通常无法可靠进入生成数据；其中的错误或偏差也可能沿生成链传递。[1][4]

后续 [[visual-instruction-tuning]] 数据规模明显扩大。LLaVA-1.5 的 665K mixture 包含 LLaVA 158K、ShareGPT、VQAv2、GQA、OKVQA、OCRVQA、A-OKVQA、TextCaps、RefCOCO 和 VisualGenome 等组成部分。[2] Safe-LLaVA 对该 mixture 的描述还明确列出 COCO、GQA、OCR-VQA、TextVQA 和 VisualGenome。[8][10] 两种清单存在命名或汇总口径差异，说明审计时不能只依据论文中的简表，而应以发布的训练 JSON 和构建脚本为准。

## COCO 图像是否与 LLaVA-Bench 重叠

### 已确认的重叠

[[LLaVA-Instruct-158K]] 使用 COCO 图像生成指令数据，而 [[LLaVA-Bench]] (COCO) 从 COCO-Val-2014 随机选择 30 张图，并为每张图构建 conversation、detailed description 和 complex reasoning 三类问题，共 90 个问题。[1][7]

因此可以确认：

- 训练与评测来自同一 COCO 数据生态；
- 训练和评测采用相同的三类任务结构；
- 两者共享相近的 captions、bounding boxes 和场景语义体系。

这是明确的 dataset-family 与 task-schema 重叠。

### 尚未确认的重叠

来源 [7] 将这 30 张图称为“unseen images”，但它是二手网页，未提供 image ID、训练清单或交集计算。给定材料也没有说明 LLaVA-Instruct-158K 究竟使用哪些 COCO split，以及是否排除了 LLaVA-Bench 的 30 张图。

因此，不能仅凭“都来自 COCO”推断相同图像进入了训练和测试。若 instruction data 使用 COCO train split，而 benchmark 使用 COCO-Val-2014，则可能不存在完全相同的 image ID；但即使 split 严格分离，也仍可能存在近重复场景、共享 caption 模式或同分布对象组合。

“30 张 unseen images”应视为作者或二手来源的声明，而不是经过独立清单审计的结论。[7]

## LLaVA-1.5 的训练—评测数据集重合

LLaVA-1.5 的训练 mixture 与评测套件存在多处数据集名称重合：

| 数据集或任务 | 出现在训练 mixture | 出现在评测 | 当前可得结论 |
|---|---:|---:|---|
| VQAv2 | 是 | 是 | dataset-family 重叠；未证明 train/test 样本交叉 |
| GQA | 是 | 是 | dataset-family 重叠；需核查 question/image ID |
| TextVQA | 来源 [8][10] 称是 | 是 | 清单口径存在差异，需以发布数据为准 |
| A-OKVQA | 是 | 未在 [2] 的主要评测格式表中列出 | 可用于后续方法的域内或下游评估 |
| RefCOCO | 是 | 未在该评测表中列出 | 属于 region-level instruction 数据 |
| VisualGenome | 是 | 间接影响多个视觉任务 | 需检查与 COCO、GQA 的共享图像关系 |
| ScienceQA | 主要作为评测或专项微调数据 | 是 | 必须区分 zero-shot、专项微调与 ensemble 成绩 |

相同数据集名称同时出现在训练与测试中，并不自动构成泄漏，因为多数 benchmark 本来就设有标准训练集和测试集。但它会使成绩更接近“同任务、同分布的监督迁移”，而不是对未知任务的纯泛化测试。[2]

VisualGenome、GQA 与 COCO 之间还可能通过共享图像产生跨数据集连接。即使 question ID 不重复，模型仍可能在训练中见过测试图像本身或其其他 annotations。给定来源没有提供足以排除这种 image-level exposure 的交集报告。

## 输出格式形成的协议闭环

LLaVA-1.5 在训练时为不同数据源附加任务特定格式提示，例如：

- VQAv2、GQA、OKVQA、OCRVQA：只输出一个单词或短语；
- A-OKVQA：直接输出选项字母；
- TextCaps：输出一句 caption；
- RefCOCO：输出区域描述或 bounding box。[2]

评测时又对 VQAv2、GQA、TextVQA、MME、POPE 使用“单词或短语”格式，对 [[ScienceQA]]、MMBench、SEED-Bench 使用“直接输出选项字母”格式。[2]

这不是传统意义上的数据泄漏，而是**训练协议与评分协议的对齐**。其可能影响包括：

- 降低 exact-match evaluation 中由冗余解释造成的误判；
- 让模型熟悉 benchmark-specific answer convention；
- 将“理解问题”与“遵循固定 verbalizer”混合在同一分数中；
- 使模型在已知格式上的成绩不能完全代表任意新格式下的指令遵循能力。

独立研究发现，visual instruction tuning 后，backbone LLM 原有的格式遵循能力可能下降；加入少量明确的输出格式指令能够缓解这种下降。[13] 因此，格式提示本身具有合理的训练目的，但报告成绩时应把“内容能力”和“格式适配收益”分开。

## GPT-4 评价闭环

### 角色重叠

在原始 LLaVA 流程中，GPT-4 至少承担四个角色：

1. 根据 COCO captions 和 bounding boxes 生成训练指令与回答；[1]
2. 根据文本化视觉信息生成 [[LLaVA-Bench]] reference answer；
3. 比较候选回答和 reference answer，并依据 helpfulness、relevance、accuracy 与 detail 打分；
4. 在 [[ScienceQA]] 中，当 LLaVA 与 GPT-4 答案不一致时，再次作为 judge 选择最终答案。

这形成如下依赖链：

```text
COCO captions / bounding boxes
        ↓
      GPT-4
        ↓
LLaVA-Instruct-158K
        ↓
      LLaVA
        ↓
候选回答 ───────────────┐
                        ↓
文本化视觉信息 → GPT-4 reference → GPT-4 judge → 最终分数
```

同一模型家族参与监督生成、参考标准生成和评分，不等于答案被直接泄漏给 LLaVA，但会造成评价标准缺少独立性。[[GPT-assisted-visual-instruction-data-generation]] 可能让 LLaVA 学到 GPT-4 偏好的组织方式、详细程度和推理风格；[[GPT-4-as-judge-多模态评估]] 又按相近偏好评分，从而产生潜在的 style affinity。

### LLaVA-Bench 分数的解释边界

LLaVA-Bench (COCO) 中，完整 instruction tuning 的总体相对分数为 85.1，无 instruction tuning 版本为 21.5。[7] 85.1 不是常规任务准确率，而是候选模型相对于 text-only GPT-4 reference 的评分比例。

该数字不应表述为“LLaVA 达到 GPT-4 视觉能力的 85.1%”，原因包括：

- reference GPT-4 获取的是 ground-truth captions 和 bounding boxes，而不是原始图像；
- GPT-4 同时参与 reference generation 和评分；
- benchmark 只有 30 张图和 90 个问题；
- 训练数据与评测问题共享 COCO 和三类任务结构；
- 来源没有给出独立人工评价与 GPT-4 judge 的系统相关性。

因此，85.1 更适合解释为：在一个小型、COCO 域内、由 GPT-4 主导评分的开放式问答集合上，LLaVA 的回答接近该流程生成的 reference。

### ScienceQA 的 ensemble 闭环

在 [[ScienceQA]] 上，LLaVA 单模型 accuracy 为 90.92%，简单 complement 为 90.97%，GPT-4 judge ensemble 为 92.53%。后者比 LLaVA 单模型高 1.61 个百分点，但应归属于组合系统，而不是 LLaVA 单模型能力。[7]

这里的 GPT-4 不仅评价答案，还直接决定最终输出，因而已经从 evaluator 变成 ensemble component。相关结果应与 [[LLaVA-与-ScienceQA-基线及-GPT-4-ensemble|LLaVA 单模型成绩]]分开报告。

## 后续 LLaVA 衍生工作的继承效应

### Grounded Visual Chat

Grounded Visual Chat 使用 LLaVA 158K 支持不带 grounding 的对话，并基于 LLaVA instruction data 与 COCO bounding boxes 构建新的 grounded conversation 数据。[3][4] 这会继承原始数据的三个依赖：

- COCO 图像和 annotations；
- GPT-4 生成的语言风格；
- LLaVA 的三类 instruction schema。

若衍生模型随后在 COCO、GQA、RefCOCO 或相关数据上评测，就需要重新执行跨数据集 image-ID 审计，不能仅假定新数据集名称意味着数据独立。

### LLaVA-c

LLaVA-c 的 continual pretraining 数据包括 COCO、OCRQA、TextVQA、GQA 和 VisualGenome，continual fine-tuning 又加入 IconQA、Super 与 Clevr-Math；评测覆盖 POPE、MME、MMBench、SEED-Bench、LLaVA-Bench 和 MM-Vet。[5]

其表格显示出广泛的任务家族复用，但给定材料没有列出完整 split、图像清单和去重程序。因此可以确认域与任务的连续重叠，不能确认具体测试样本是否被训练使用。

### Safe-LLaVA

Safe-LLaVA 从 LAION-CC-SBU-558k 和 LLaVA-v1.5-mix665k 中检测并清理 biometric attributes，清理过程本身使用 GPT-4o。[8][10] 随后的 PRISM 评测又使用 GPT-4 和 Gemini-2.0-flash 判断 refusal 与 implicit leakage。[6][8]

这同样构成“LLM 生成或清理监督—LLM 评价结果”的闭环，但其设计包含两项缓解措施：

- 使用 GPT-4 与 Gemini 两个 evaluator；
- 对 500 个随机样本进行人工审计，并对模型—prompt 组合运行三次。[6][8]

这比单一 GPT-4 judge 更具交叉验证性，但仍不能替代完整人工盲评。人工审计主要验证数据清理质量，而不是直接校准所有自动 evaluator 的判断。

## 来源中的矛盾与不确定性

### “泄漏率”与“保护分数”混用

来源 [6] 将 Safe-LLaVA 的 97.1% 和 90.7% 称为“average leakage rate”，同时又把更高数值解释为更好的表现。来源 [10] 则将相近指标称为 implicit biometric leakage protection，并明确认为越高越好。

两者在术语上矛盾。若指标越高代表越安全，更合理的名称应是 protection score、non-leakage rate 或 refusal accuracy，而不是 leakage rate。引用 Safe-LLaVA 数字时必须保留具体指标定义，不能只写“泄漏率”。

### LLaVA-1.5 mixture 清单不完全一致

来源 [2] 的训练表列出 OCRVQA、TextCaps 等数据，而来源 [8][10] 概括 mix665k 时列出 TextVQA。差异可能来自表格节选、命名误差或 mixture 版本不同。在没有官方 JSON、配置文件和 commit hash 的情况下，不能据此重建唯一的数据组成。

### “unseen images”缺乏清单证据

来源 [7] 称 LLaVA-Bench 使用 30 张 unseen images，但没有提供与训练清单求交集的结果。原始 benchmark 来自 COCO-Val-2014，而 instruction data 也来自 COCO；因此“未见过”至少需要由 image-ID 或文件哈希验证。

### 二手来源的证据权重

Medium 与商业博客来源 [1][7][9][15] 可用于发现线索，但不应承担 split、指标定义或 contamination 结论的最终证据。关键判断应优先依据论文、官方代码、数据 manifest 和可复现的交集计算。

## 对成绩解释的影响

现有证据不支持将所有 LLaVA 结果视为无效，但要求收窄结论范围：

- LLaVA-Bench 主要支持模型在小规模、GPT-4-mediated 开放式问答上的表现。
- LLaVA-1.5 在 VQAv2、GQA 等任务上的成绩同时包含任务内监督、输出格式适配和模型能力。
- [[ScienceQA]] 的 92.53% 是 LLaVA 与 GPT-4 judge 的组合成绩，不能归因于 LLaVA 单模型。
- 数据集家族重合并不等于样本泄漏；是否 contamination 必须通过 ID 和内容级去重确定。
- GPT-4 闭环提出的是 construct validity 与 evaluator independence 问题，而不是已经证明的分数操纵。
- 多 benchmark 一致提升能减轻单一 benchmark 偶然性的担忧，但不能自动消除共同训练数据、共同图像来源或共同 judge 的依赖。

来源 [11] 报告 instruction-data 质量指标与下游表现存在相关性，来源 [14] 则显示只选择 LLaVA-665K 的部分数据也可能保持 clean performance 并提升 robustness。这些结果说明“更多数据”不是唯一解释；数据选择和质量确实重要。但它们没有直接回答测试样本是否进入训练集，因此不能替代 contamination audit。[11][14]

## 建议的实证核查流程

要把“结构性重叠”进一步判定为“样本级泄漏”，至少需要取得以下材料：

1. LLaVA-Instruct-158K、LLaVA-1.5-mix665k 和各衍生 mixture 的完整训练 JSON。
2. LLaVA-Bench (COCO) 的 30 个 COCO image ID 和 90 个问题。
3. VQAv2、GQA、TextVQA、ScienceQA 等评测所使用的准确 split 与 question ID。
4. 数据下载和预处理脚本对应的 commit hash。
5. GPT-4 judge 的完整 prompt、模型 snapshot、temperature、采样次数和解析逻辑。

随后应执行：

- image ID 精确求交集；
- question ID、annotation ID 和 caption ID 求交集；
- 对重新编码或裁剪图像计算 perceptual hash；
- 对 prompt、question 和 answer 做文本近重复检索；
- 检查 VisualGenome、GQA、COCO 之间共享的底层图像；
- 按“见过图像但未见过问题”“见过问题模板”“完全未见过图像”分层报告；
- 用盲法人工评价和异构 evaluator 复核 GPT-4 judge；
- 增加非 COCO、非 GPT-generated、非固定格式的外部测试集。

## 值得补充查找的来源

- 官方 LLaVA 数据仓库中的 `conversation_58k.json`、`detail_23k.json`、`complex_reasoning_77k.json` 及对应 image ID。
- LLaVA-Bench (COCO) 和 In-the-Wild 的完整问题、reference 与评测脚本。
- LLaVA-1.5 `mix665k` 的版本化 manifest 与数据构建脚本。
- COCO、VisualGenome 和 GQA 的共享图像映射表。
- 对 LLaVA 系列进行 image-level 或 semantic-near-duplicate decontamination 的独立研究。
- GPT-4 judge 与人工盲评之间的相关性、偏好一致性和 position/style bias 研究。
- 将固定格式成绩与 verbalizer-manipulation 成绩分开报告的评测。[13]
- 使用多 evaluator、人工 calibration set 和 evaluator disagreement 分析的多模态 benchmark。

## 综合判断

当前证据可以确认 [[LLaVA]] 存在显著的训练—评测**结构性耦合**：COCO 等数据生态被反复使用，训练与测试共享任务和输出模板，GPT-4 又横跨数据生成、reference generation、评分和 ensemble。这个闭环使部分结果更像“在 GPT-4 和 COCO 所定义的任务体系内完成 alignment”，而不是完全独立地测量开放世界视觉理解。

然而，结构性耦合不能与样本级 contamination 画等号。在取得 image ID、question ID、数据 manifest 和去重结果之前，最稳妥的表述仍是：

> 已发现数据来源、任务协议和评价者的多层重叠；尚未发现足以证明训练样本与测试样本直接交叉的证据。LLaVA 的成绩应在这些依赖条件下解释，并通过清单级去重、外部分布评测和独立人工校准进一步核查。

## References

1. [Medium](https://ritvik19.medium.com/papers-explained-102-llava-1-eb0a3db7e43c) — ritvik19.medium.com
2. [Improved Baselines with Visual Instruction Tuning](https://static.hliu.cc/files/llava/improved_llava.pdf) — static.hliu.cc
3. [Grounded Visual Chat with Large Multimodal Models](https://arxiv.org/html/2312.02949v1) — arxiv.org
4. [[PDF] Grounded Visual Chat with Large Multimodal Models](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/05918.pdf) — ecva.net
5. [LLaVA-c: Continual Improved Visual Instruction Tuning](https://arxiv.org/html/2506.08666v1) — arxiv.org
6. [Safe-LLaVA: A Privacy-Preserving Vision-Language Dataset and Benchmark for Biometric Safety](https://arxiv.org/html/2509.00192v1) — arxiv.org
7. [GPT-4 Vision vs LLaVA](https://encord.com/blog/gpt-vision-vs-llava) — encord.com
8. [Safe-LLaVA: A Privacy-Preserving Vision Language Dataset and Benchmark for Biometric Safety](https://arxiv.org/html/2509.00192v2) — arxiv.org
9. [GPT-Vision and LLaVA](https://medium.com/@yash43forall/gpt-vision-and-llava-17309bfa5bdb) — medium.com
10. [Safe-LLaVA: A Privacy-Preserving Vision Language Dataset ...](https://openaccess.thecvf.com/content/CVPR2026F/papers/Kim_Safe-LLaVA_A_Privacy-Preserving_Vision_Language_Dataset_and_Benchmark_for_Biometric_CVPRF_2026_paper.pdf) — openaccess.thecvf.com
11. [Vision-Language Instruction Tuning:A Review and Analysis](https://arxiv.org/html/2311.08172v2) — arxiv.org
13. [Instruction-Following Evaluation of Large Vision-Language Models | New Generation Computing | Springer Nature Link](https://link.springer.com/article/10.1007/s00354-025-00308-2) — link.springer.com
14. [Towards Robust Instruction Tuning of Large Multimodal ...](https://papers.nips.cc/paper_files/paper/2025/file/0d77ccb50a558035f19089096f933e8e-Paper-Conference.pdf) — papers.nips.cc
15. [Medium](https://medium.com/@nandinilreddy/inside-llava-how-visual-instruction-tuning-powers-the-future-of-multi-modal-ai-assistants-4631428bfd82) — medium.com
