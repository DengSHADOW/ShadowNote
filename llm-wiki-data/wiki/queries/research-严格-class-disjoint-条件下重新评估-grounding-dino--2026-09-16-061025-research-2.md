---
type: query
title: "Research: 严格 class-disjoint 条件下重新评估 Grounding DINO 的 zero-shot 能力"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: 严格 class-disjoint 条件下重新评估 Grounding DINO 的 zero-shot 能力

我会按 `wiki-maintenance` 的 query/synthesis 规范组织这页：先核对项目约定与现有 [[Grounding-DINO]] 相关页面，再基于你提供的 12 个来源写出可直接入库的中文 Wiki 正文；本次只生成内容，不改动仓库。当前工作目录已是 `llm-wiki-data/`，而约定中的技能与 `docs/` 位于其上级仓库；我已纠正路径。接下来会特别核对现有页面对 “zero-shot” 与数据泄漏的用词，避免把 COCO 类别已被 O365 近乎覆盖的迁移结果误写成严格 class-disjoint 证据。# 严格 class-disjoint 条件下重新评估 Grounding DINO 的 zero-shot 能力

## 结论摘要

现有证据支持 [[Grounding-DINO]] 具有较强的文本条件化跨数据集检测能力，但不足以证明其在严格 class-disjoint 条件下具有论文中通常所暗示的 zero-shot 类别泛化能力。核心原因是：原论文把 zero-shot 定义为“不使用目标数据集的训练 split”，而不是“训练阶段从未出现测试类别”；Objects365（O365）又几乎覆盖全部 COCO 类别。因此，COCO 上报告的 `52.5 AP` 主要衡量跨数据集、跨标注体系迁移，而非严格的 unseen-category 检测。[2]

截至这些来源所提供的证据，不能给出 Grounding DINO 在严格 class-disjoint COCO 48-base/17-novel 协议下的可信 AP。要完成这种重新评估，需要重新训练或获得经过完整语义泄漏审计的 checkpoint；仅在现有 checkpoint 上更换测试集或 prompt，不足以建立严格 class-disjoint 条件。

## 问题定义

### 三种容易混淆的 zero-shot

| 评估含义 | 训练阶段允许什么 | Grounding DINO 现有 COCO 结果是否满足 |
|---|---|---|
| 目标数据集 split-disjoint | 不使用目标 benchmark 的训练图像，但可以使用其他数据集中的同类对象 | 是，部分 checkpoint 满足 |
| 类别标注 class-disjoint | 训练检测标注不包含测试 novel classes | 尚未得到证明 |
| 语义与语料 corpus-audited class-disjoint | detection、grounding、caption、伪标注及类别映射均不暴露 novel concepts | 没有证据表明满足 |

[[2303.05499v5 (1)|Grounding DINO 原论文]]采用第一种定义：只要没有使用 COCO training split，便把 COCO 评估称为 zero-shot。[2] 这与严格 [[开放集目标检测|open-set object detection]] 文献常用的 class-disjoint 问题不同。严格协议要求训练类别集合 $C_{\mathrm{train}}$ 与 novel 类别集合 $C_{\mathrm{novel}}$ 分离，而且训练时不能获得 novel vocabulary；测试时则需要检测 $C_{\mathrm{train}}\cup C_{\mathrm{novel}}$。[6]

标准 OV-COCO 协议通常将 65 个 COCO 类别划分为 48 个 base classes 和 17 个 novel classes，并分别报告 $AP^{50}_{base}$、$AP^{50}_{novel}$ 和整体 $AP^{50}$。[6][10] 这些指标与 Grounding DINO 原论文在完整 COCO 类别集合上报告的 COCO AP 并非同一评估，不能直接横向排序。

## 现有结果能够说明什么

### COCO 结果是跨数据集迁移证据

Grounding DINO T 使用 O365、GoldG 和 Cap4M 训练时报告 `48.4 AP`；Grounding DINO L 使用 Swin-L、O365、OpenImages 和 GoldG 时达到 `52.5 AP`。[2] 官方代码仓库给出的 Grounding DINO T 示例结果为 `48.5 AP`，与论文的 `48.4 AP` 基本一致，但仍需固定 checkpoint、代码版本和评估配置后才能解释这一差异。[5]

这些结果证明 [[grounded-pre-training]]、[[tight-modality-fusion]]、[[language-guided-query-selection]] 和 [[sub-sentence-level-text-representation]] 可以产生有竞争力的文本条件化检测器，却不能证明模型从未在训练中接触 COCO 类别。原论文明确指出，O365 “几乎覆盖”全部 COCO 类别，并承认 O365 与 COCO 之间的类别映射包含近似处理。[2]

因此，更准确的表述是：

> Grounding DINO 在没有使用 COCO training images 的条件下实现了较强的 COCO 跨数据集迁移；该结果不是严格 class-disjoint novel-category 泛化的测量。

### 不同 checkpoint 不能混为同一 zero-shot 结果

官方仓库还列出 Grounding DINO B 的 `56.7 AP`，但其训练数据包含 COCO、O365、GoldG、Cap4M、OpenImages、ODinW-35 和 RefCOCO。[5] 因为训练时直接使用了 COCO，该数字不应作为 COCO zero-shot 证据。

同样，`52.5 AP` 与 `48.4/48.5 AP` 的差别主要来自 backbone、模型规模和预训练数据不同，而非同一模型在不同复现中的直接矛盾。[2][5] 二次资料把 `52.5 AP` 简化为“没有任何 COCO 训练数据的 zero-shot”时虽然符合数据集级定义，却省略了 O365 类别覆盖这一关键限制。[3][11]

## 领域迁移不等同于类别新颖性

农业和遥感实验提供了有价值的外部分布证据，但同样没有完成严格的预训练类别审计。

农业研究直接在目标测试集上使用预训练 Grounding DINO，不进行 fine-tuning，并报告 prompt 选择困难：单词和短语模板会改变结果，模型难以区分外观相近的 crop 与 weed，也难以处理相互遮挡的叶片。在 DIOR Split-1 上，使用类名 prompt 的 zero-shot mAP 为 `22.8`，3-shot adaptation 后升至 `40.0`。[4] 这表明未经适配的检测能力可能显著弱于标准 COCO 结果，也表明 prompt engineering 是重要混杂变量；但来源没有证明 DIOR 类别及其语义近邻未出现在 Grounding DINO 的大规模预训练数据中。

抓取系统研究同样把“目标数据集上不 retrain 或 fine-tune”称为 zero-shot，并将 Grounding DINO 与 EdgeSAM 组合，用前者提供语义框、后者提供像素级分割。[1] 该实验支持下游可用性，却不能单独证明严格 unseen-category 泛化。

## 数据泄漏风险

Grounding DINO 的训练资源不只包含检测类别标签，还包括 grounding pairs、caption data 和由其他模型生成的伪标注。[2] 因此，只比较检测数据集的类别表是不充分的。潜在泄漏至少包括：

1. **精确名称泄漏**：novel class 名称直接出现在训练类别或 caption 中。
2. **别名泄漏**：复数、拼写变体、品牌名、学名或同义词暴露同一类别。
3. **层级泄漏**：训练数据包含 novel class 的上位、下位或近邻类别。
4. **视觉实例泄漏**：相同或近重复图像跨越训练与测试数据。
5. **教师模型泄漏**：caption pseudo-labeler 或其他预训练组件已经使用目标类别或目标数据集。
6. **评估映射泄漏**：通过人工类别映射把训练类别直接转换为测试标签。

细粒度 OVD 工作指出，不同模型使用不同规模和组成的预训练语料，使所谓 novel classes 很可能已经被模型直接或间接观察过。[7][9] OV-VG 也把这种数据泄漏与严格 zero-shot/open-vocabulary 定义区分开来。[8]

需要注意的是，即使清除了检测标注和 caption，通用文本或视觉 backbone 的预训练语料通常也无法被完全审计。因此，实验报告应区分“检测监督 class-disjoint”“所有任务语料 vocabulary-disjoint”和“包括 foundation backbone 在内的概念完全未见”三个强度等级，而不应笼统称为严格 zero-shot。

## 建议的重新评估协议

### 数据与训练控制

建议以 OV-COCO 的 48-base/17-novel 划分为基础，并执行以下控制：[6][10]

- 仅使用 48 个 base classes 的检测标注训练 Grounding DINO。
- 训练期间不向模型提供 17 个 novel class 的名称或测试 prompt。
- 对 O365、OpenImages、GoldG、Cap4M、RefCOCO 及其他训练资源建立类别和短语清单。
- 删除 novel class 的精确名称、同义词、别名和明确的细粒度派生词。
- 审计 pseudo-labeler、数据生成器和教师模型是否使用过 COCO 或 novel classes。
- 对训练图像与 COCO validation/test images 做精确哈希及近重复检查。
- 保留图像 backbone 和文本 backbone 的预训练信息，但单独声明其数据来源及无法排除的先验知识。

若无法完成上述过滤，则实验只能标记为“目标数据集 split-disjoint”，不能标记为“语料审计后的严格 class-disjoint”。

### 对照模型

至少需要比较：

- 仅在 base classes 上训练的闭集 DINO；
- 具有相同 backbone、训练图像和训练预算的 Grounding DINO；
- 去除额外 grounding/caption data 的 Grounding DINO；
- 加入经过过滤的 grounding/caption data 的 Grounding DINO；
- 使用未过滤大规模数据的公开 checkpoint，作为弱 zero-shot 上限而非严格结果。

这种设计可以区分收益究竟来自 [[Grounding-DINO]] 的跨模态结构、额外训练数据，还是测试类别已经出现在预训练语料中。

### Prompt 控制

由于 prompt 形式会显著影响类别判定，[4] 应在测试前固定至少一个主协议：

- 每类只使用规范类名；
- 所有类别使用相同模板；
- 不根据测试结果逐类调 prompt；
- 类别同义词 ensemble 仅作为单独的 oracle 或 sensitivity 实验；
- 同时记录 text threshold、box threshold 和 NMS 设置。

对于 [[Referring-Expression-Comprehension|Referring Expression Comprehension]] 式详细描述，应与纯类别名称检测分开报告，避免把额外人工属性描述带来的信息增益归因于模型的 class-disjoint 泛化。

### 指标

建议同时报告：

- $AP^{50}_{novel}$、$AP^{50}_{base}$ 和 $AP^{50}_{all}$，以对齐 OV-COCO 文献；[6][10]
- COCO-style $AP_{novel}$，避免只依赖 IoU 0.5；
- novel-class recall 与定位 recall，用于区分“没有找到目标”和“找到但分类失败”；
- 每类 AP 及宏平均，防止少数常见类别主导总体结果；
- 至少三个随机种子的均值、标准差或置信区间；
- 参数量、输入尺寸、训练数据量和计算预算。

## False positive 与开放词汇干扰

COCO-FP 结果显示，开放词汇能力并不自动带来对背景干扰的稳健性。Grounding DINO T 在普通 COCO Val 上为 `48.5 AP`，在 COCO-FP 上降至 `44.6 AP`；加入预先给定的 false-positive category prompts 后，普通 COCO Val 为 `45.4 AP`，COCO-FP 仍为 `44.5 AP`。[12]

这提示严格评估不应只包含合法类别 prompt，还应加入：

- 图像中不存在的 distractor categories；
- 视觉上与 novel classes 相近的类别；
- 上位词、下位词和同义词；
- 背景中容易产生伪框的概念。

应分别报告增加 distractor prompts 前后的 precision、recall 和 AP，以衡量类别词表扩张是否造成竞争性抑制或错误 grounding。

## 细粒度评估的补充价值

细粒度类别具有较小的类间差异和较大的类内差异，因此比通用 COCO 类别更难依靠宽泛语义先验解决。[7] 3F-OVD 提议使用稳定、类别特定的详细描述，并通过细粒度车型和零售商品等类别降低明显类别泄漏的风险。[7][9]

不过，细粒度或 temporal split 主要减少实例重复和粗粒度类别捷径，不能自动保证预训练语料 class-disjoint。模型仍可能在 caption、商品网页或视觉 backbone 预训练数据中见过相同车型或产品。因此，这类 benchmark 适合作为补充压力测试，而不能替代训练语料审计。

## 证据矛盾与未决问题

- `52.5 AP`、`48.4 AP` 和 `48.5 AP` 对应不同模型或记录精度，不应视为同一配置的直接冲突。[2][5]
- “没有 COCO training data”与“O365 几乎覆盖 COCO 类别”可以同时成立；前者描述数据集 split，后者揭示类别并不新颖。[2]
- 官方 Grounding DINO B checkpoint 使用 COCO，却经常与真正未使用 COCO images 的 checkpoint 一同列出，容易造成错误比较。[5]
- OV-COCO 主要报告 novel-class $AP^{50}$，而 Grounding DINO 原论文报告完整 COCO AP，两者的类别集合和 IoU 汇总方式都不同。[2][6][10]
- 现有来源没有报告经过语义过滤和完整训练资源审计的 Grounding DINO 结果，因此不能估计严格协议会造成多大性能下降。
- 现有研究也没有分离文本 backbone 的语言先验、视觉 backbone 的类别知识和 [[grounded-pre-training]] 检测监督各自的贡献。

## 综合判断

对 Grounding DINO 的合理结论应分为两层：

1. **已经得到支持的结论**：Grounding DINO 是有效的文本条件化 [[开放集目标检测]] 架构，能在不使用目标 benchmark 训练图像的条件下实现较强的跨数据集检测，并能通过 prompt 接受外部类别词表。[1][2][4][5]

2. **尚未得到支持的结论**：现有 `52.5 AP` 或 `48.4/48.5 AP` 不能证明模型在严格 class-disjoint、训练语料经过 novel-concept 审计的条件下仍具有相同性能。[2][6][7]

因此，重新评估的关键不是再次运行公开 checkpoint 的 COCO 脚本，而是建立一个可审计的 class-disjoint 训练管线，并把数据集未见、类别未见、语料未见和 foundation prior 分别报告。

## 建议补充的来源

- Grounding DINO 各公开 checkpoint 的完整训练 manifest、数据版本和去重记录。
- O365、OpenImages 与 COCO 之间的精确类别映射及同义词表。
- GoldG、Cap4M 和伪标注 caption 的 novel-class phrase 审计结果。
- Grounding DINO 在标准 OV-COCO 48/17 划分上的独立复现。
- EdaDet 严格设置的完整实验表、训练资源限制和实现代码。[6]
- OV-VG 与 3F-OVD 的完整论文、数据构建规则和泄漏审计方法。[7][8][9]
- 多随机种子、固定 prompt 和 distractor-prompt 条件下的复现实验。
- 对文本 backbone、图像 backbone 和 grounding supervision 分别进行冻结或替换的消融研究。

## 参考来源

[1] *A Multi-Step Grasping Framework for Zero-Shot Object Detection in Everyday Environments Based on Lightweight Foundational General Models*  
[2] *Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection*  
[3] alphaXiv：*Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection*  
[4] *Few-Shot Adaptation of Grounding DINO for Agricultural Domain*  
[5] IDEA-Research/GroundingDINO 官方代码仓库  
[6] *EdaDet: Open-Vocabulary Object Detection Using Early Dense Alignment*  
[7] *Fine-Grained Open-Vocabulary Object Detection with Fined-Grained Prompts: Task, Dataset and Benchmark*  
[8] *OV-VG: A Benchmark for Open-Vocabulary Visual Grounding*  
[9] alphaXiv：*Fine-Grained Open-Vocabulary Object Detection with Fined-Grained Prompts*  
[10] *NoOVD: Novel Category Discovery and Embedding for Open-Vocabulary Object Detection*  
[11] *Fine-Tuning Grounding DINO – Object Detection*  
[12] *From COCO to COCO-FP: A Deep Dive into Background False Positives for COCO Detectors*

## References

1. [A Multi-Step Grasping Framework for Zero-Shot Object Detection in Everyday Environments Based on Lightweight Foundational General Models](https://pmc.ncbi.nlm.nih.gov/articles/PMC12694047) — pmc.ncbi.nlm.nih.gov
2. [[PDF] Marrying DINO with Grounded Pre-Training for Open-Set Object ...](https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06319.pdf) — ecva.net
3. [Grounding DINO: Marrying DINO with Grounded Pre-Training for ...](https://www.alphaxiv.org/abs/2303.05499) — alphaxiv.org
4. [Few-Shot Adaptation of Grounding DINO for Agricultural Domain](https://arxiv.org/html/2504.07252v1) — arxiv.org
5. [IDEA-Research/GroundingDINO: [ECCV 2024] Official ...](https://github.com/idea-research/groundingdino) — github.com
6. [EdaDet: Open-Vocabulary Object Detection Using Early ...](https://openaccess.thecvf.com/content/ICCV2023/papers/Shi_EdaDet_Open-Vocabulary_Object_Detection_Using_Early_Dense_Alignment_ICCV_2023_paper.pdf) — openaccess.thecvf.com
7. [Fine-Grained Open-Vocabulary Object Detection with Fined-Grained Prompts: Task, Dataset and Benchmark](https://arxiv.org/html/2503.14862v2) — arxiv.org
8. [OV-VG: A benchmark for open-vocabulary visual grounding](https://www.sciencedirect.com/science/article/pii/S0925231224005095) — sciencedirect.com
9. [Fine-Grained Open-Vocabulary Object Detection with Fined-Grained Prompts: Task, Dataset and Benchmark | alphaXiv](https://www.alphaxiv.org/abs/2503.14862) — alphaxiv.org
10. [NoOVD: Novel Category Discovery and Embedding for Open-Vocabulary Object Detection](https://arxiv.org/html/2603.21069v1) — arxiv.org
11. [Fine-Tuning Grounding DINO - Object Detection](https://learnopencv.com/fine-tuning-grounding-dino) — learnopencv.com
12. [From COCO to COCO-FP: A Deep Dive into Background False Positives for COCO Detectors](https://arxiv.org/html/2409.07907v1) — arxiv.org
