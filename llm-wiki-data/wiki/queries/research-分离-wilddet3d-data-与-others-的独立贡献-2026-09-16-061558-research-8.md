---
type: query
title: "Research: 分离 WildDet3D-Data 与 Others 的独立贡献"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: 分离 WildDet3D-Data 与 Others 的独立贡献

我会按 `wiki-maintenance` 的 query/synthesis 规范处理：先核对项目状态、Wiki 索引与已有 WildDet3D 页面，再基于给定来源写出中文综合页；除非请求明确要求入库，本轮不改写 Wiki 文件。当前工作目录本身就是 `llm-wiki-data`，而项目说明中的路径是从上一级仓库根目录书写的；我已据此纠正路径，继续读取所需规范与现有页面。现有论文页已明确记录核心识别问题：公开表格只比较 `Omni3D` 与 `Omni3D + Others + WildDet3D-Data`，没有单独的 `+ Others` 或 `+ WildDet3D-Data` 行。因此最终页面会把“可计算的联合增益”和“无法识别的独立贡献”严格分开。现在我补查 `Others` 的具体组成及三阶段训练细节。# 分离 WildDet3D-Data 与 Others 的独立贡献

## 结论摘要

现有公开结果**不能识别** [[WildDet3D-Data]] 与 `Others` 对 [[WildDet3D]] 性能的独立贡献。[[WildDet3D-Bench]] 只报告了两端配置：

- `Omni3D`
- `Omni3D + Others + WildDet3D-Data`

缺少同一模型、同一训练流程下的 `Omni3D + Others` 和 `Omni3D + WildDet3D-Data` 两个关键对照。因此，表中可以确定的是扩展训练流程的**联合增益**，不能把该增益单独归因于 [[WildDet3D-Data]]、`Others`，也不能估计二者的交互作用。[3]

此外，完整模型并非简单地向 Omni3D-only 训练加入一些样本：公开训练说明显示它经过三阶段训练，并在数据比例、训练轮数和 prompt collator 上同时发生变化。[6] 因而当前对比更准确地衡量：

> `新增数据 + 多阶段 fine-tuning + 数据重采样 + prompt 训练策略变化`

的总体效果，而不是单纯的数据集效应。

## 需要分离的训练数据

论文与代码资料将最终训练数据概括为三个部分：

| 数据组 | 大致内容 | 在现有实验中的角色 |
|---|---|---|
| Omni3D | KITTI、nuScenes、SUNRGBD、Hypersim、ARKitScenes、Objectron 等标准 3D 数据 | 基础训练数据 |
| `Others` | 当前训练文档中的 CA-1M、Waymo、3EED-det、3EED-ref、FoundationPose | 补充的传统或任务特定 3D 数据 |
| [[WildDet3D-Data]] | 从 COCO、LVIS、Objects365、V3Det 扩展出的 in-the-wild 大词汇 3D annotations | 扩展场景、类别与长尾覆盖 |

当前代码文档把 Stage 2 描述为八数据集混合：Omni3D `80%`、CA-1M `3%`、Waymo `2%`、3EED-det `1%`、3EED-ref `1%`、FoundationPose `6%`、ITW human `5%`、V3Det human `2%`。据此，`Others` 可以操作性地理解为 CA-1M、Waymo、3EED 和 FoundationPose，而 ITW human 与 V3Det human 属于 [[WildDet3D-Data]]。[6]

这一解释来自当前代码文档；论文版本与代码版本的训练配方并不完全一致，不能默认二者描述的是完全相同的数据快照。

## 可直接计算的联合增益

以下差值均为 `Omni3D + Others + WildDet3D-Data` 减去 `Omni3D`，因此只能称为**联合增益**。[3]

| Prompt | Depth | APrare 增益 | APcommon 增益 | APfrequent 增益 | 总 AP 增益 |
|---|---|---:|---:|---:|---:|
| Text | 无 | +19.3 | +15.1 | +13.5 | +15.8 |
| Text | 有 | +24.4 | +19.2 | +21.1 | +20.9 |
| Box | 无 | +18.0 | +16.3 | +15.0 | +16.4 |
| Box | 有 | +27.3 | +21.7 | +22.9 | +23.3 |

在无 depth 条件下：

- Text prompt 从 `6.8 AP` 提升到 `22.6 AP`，增加 `15.8` 点。
- Box prompt 从 `8.4 AP` 提升到 `24.8 AP`，增加 `16.4` 点。[3]

在有 depth 条件下：

- Text prompt 从 `20.7 AP` 提升到 `41.6 AP`，增加 `20.9` 点。
- Box prompt 从 `23.9 AP` 提升到 `47.2 AP`，增加 `23.3` 点。[3]

四种条件下，APrare 的绝对增益均高于 APcommon 和 APfrequent。该模式与 [[WildDet3D-Data]] 扩展长尾类别和 in-the-wild 场景的设计目标一致，但它只能构成相关性证据：`Others`、训练阶段变化和数据采样也可能贡献这些增益。此外，rare 是按 [[WildDet3D-Bench]] 中的评价频次划分，并不等于训练阶段未见类别。

## 为什么不能从基线反推出独立贡献

### 缺少同模型的必要对照

要估计独立效应，至少需要以下四个同构实验：

$$
M_{00}=f(\text{Omni3D})
$$

$$
M_{10}=f(\text{Omni3D}+\text{Others})
$$

$$
M_{01}=f(\text{Omni3D}+\text{WildDet3D-Data})
$$

$$
M_{11}=f(\text{Omni3D}+\text{Others}+\text{WildDet3D-Data})
$$

由此才能计算：

$$
\Delta_{\text{Others}}=M_{10}-M_{00}
$$

$$
\Delta_{\text{WildDet3D-Data}}=M_{01}-M_{00}
$$

以及二者的交互项：

$$
I=M_{11}-M_{10}-M_{01}+M_{00}
$$

当前只公开了 $M_{00}$ 与 $M_{11}$，所以只有联合差值 $M_{11}-M_{00}$ 可观测。[3]

### DetAny3D 不是 `Others` 消融

表中 DetAny3D 使用 `Omni3D + Others`，其 box-prompt AP 为 `7.8`；但它与 Omni3D-only [[WildDet3D]] 的 `8.4 AP` 来自不同模型、初始化、检测头和训练流程。[3] 因此不能用：

$$
7.8-8.4
$$

估计 `Others` 的贡献，更不能据此认为 `Others` 没有作用。该比较同时改变了模型与数据，违反了单变量消融的基本条件。

### 训练阶段也是混杂因素

公开训练流程包括：[6]

1. Stage 1：Omni3D-only，12 epochs。
2. Stage 2：八数据集 dense fine-tuning，12 epochs。
3. Stage 3：Omni3D `90%` 与 ITW human `10%` 的高质量混合，3 epochs。

Stage 2 使用 text 与 box prompts；Stage 3 还引入从 masks 采样的 point prompts。[6] 因此，Stage 1 与最终 checkpoint 之间不仅数据不同，还存在额外训练步数、采样分布和 prompt curriculum 的差异。

## 对 [[WildDet3D-Data]] 贡献的有限推断

尽管无法进行因果分离，现有证据仍允许提出若干受限判断。

### 类别与场景覆盖可能是主要作用机制

[[WildDet3D-Data]] 从 COCO、LVIS、Objects365 和 V3Det 扩展到约一百万张 in-the-wild 图像，覆盖约 13.5K categories。[2][3][5] 相比主要覆盖驾驶和室内家具类别的 Omni3D，它显著扩大了对象词汇与场景分布。完整训练在 APrare 上取得最大的绝对增益，与这种覆盖扩张方向相符。[3]

不过，[[WildDet3D-Bench]] 本身来源于 [[WildDet3D-Data]] 的人工 validation subset。训练和评价数据虽然没有直接使用相同图像，但共享 COCO、LVIS、Objects365 等上游来源及其类别体系。这可能产生明显的 domain-alignment 优势；它不等同于对完全独立外部数据域的普遍泛化。

### 人工数据可能承担最终校准作用

当前训练说明中的 Stage 3 只使用 Omni3D 与 ITW human，并明确称为 high-quality fine-tuning。[6] 这说明最终模型可能依赖 [[WildDet3D-Data]] 的人工子集来校准自动或异构数据阶段获得的表示。

但由于没有 Stage 2 与 Stage 3 在相同 benchmark 上的系统对照，无法量化这一步贡献了多少 AP，也无法判断增益来自数据质量、prompt mix，还是额外优化步骤。

### 与 depth 的互补关系尚未被解释

扩展训练的联合增益在有 depth 条件下更大。例如 box prompt 的联合增益从无 depth 的 `+16.4 AP` 增加到有 depth 的 `+23.3 AP`。[3] 这表明扩大训练分布可能改善模型利用几何输入的能力。

然而，这仍可能来自 `Others` 中带有更强 metric geometry supervision 的数据，或来自 [[WildDet3D-Data]] 的 depth、camera 与 3D annotations。现有表格不能区分两种解释。相关结果也应与[[不同-depth-条件下的-WildDet3D]]所总结的 depth source 差异结合阅读。

## 来源之间的矛盾与版本差异

### 训练配方不一致

论文记录的三阶段流程把 Stage 2 概括为：

- `Omni3D + Others + WildDet3D-Data (H+S)`

Stage 3 则使用：

- `Omni3D + WildDet3D-Data (H)`

但当前 GitHub 训练说明将 Stage 2 描述为八个 **human-only** 数据集，并未列入大规模 synthetic split。[6] 可能的解释包括：

- 论文实验与后来发布代码采用了不同配方；
- `H+S` 是论文层面的概括，而公开配置只复现后续 human-only checkpoint；
- 文档或论文表述存在未同步更新。

在确认具体 checkpoint、commit 与数据版本之前，不应把论文中的 `H+S` 与当前代码中的 human-only recipe 当作同一处理。

### 数据集规模不一致

Ai2 介绍材料使用约 `3.7M` annotations 的概数。[2] 论文页记录 `3,728,078`，而当前 GitHub 表格报告 `3,910,855`。[3] 这可能来自数据版本更新、`valid3D` 过滤口径或 Human/Essential/Synthetic split 定义变化。[7]

因此，任何新的贡献消融都应记录：

- 使用的 annotation 文件名；
- dataset revision 或 commit；
- 是否仅保留 `valid3D=true`；
- Human、Essential、Synthetic 的具体组合；
- 实际参与训练的 image 与 annotation 数量。

### “human-verified”表述过宽

[[WildDet3D-Data]] 的主要训练规模由 VLM auto-selected synthetic split 提供，而人工审核训练集约为 103K images。[3][7] 将全部约一百万张图像描述为逐项 human-verified 会掩盖两类监督质量的差异，也使贡献分析无法区分规模效应与人工质量效应。

## 建议的最小消融方案

要回答研究问题，最低限度应在同一代码版本、模型初始化和训练预算下运行一个 $2\times2$ factorial design：

| 实验 | Omni3D | `Others` | [[WildDet3D-Data]] |
|---|:---:|:---:|:---:|
| A | ✓ |  |  |
| B | ✓ | ✓ |  |
| C | ✓ |  | ✓ |
| D | ✓ | ✓ | ✓ |

每个实验应保持：

- 相同总 optimization steps；
- 相同 batch size、学习率与 scheduler；
- 相同 prompt sampling；
- 相同 backbone initialization 与冻结策略；
- 相同 depth 输入分布；
- 至少三个随机种子；
- 同时报告 APrare、APcommon、APfrequent 和总 AP。

为避免“更多数据等于更多计算”的混杂，还应增加一个等样本量版本：从 `Others` 与 [[WildDet3D-Data]] 分别采样相同数量的 images、objects 或 optimizer exposures。

随后可把 [[WildDet3D-Data]] 进一步拆为：

- Human only；
- Synthetic/VLM only；
- Human + Synthetic；
- 不含 V3Det；
- 与 benchmark 上游来源去重或类别去重的版本。

这组实验能够分别检验人工质量、自动数据规模、长尾词汇覆盖和 evaluation-domain alignment。

## 仍待回答的问题

1. Table 3 的最终结果对应论文所述 `H+S` 配方，还是当前发布的 human-only Stage 2 配方？
2. `Others` 在论文实验中的精确定义、样本数量及采样权重是什么？
3. Stage 1、Stage 2 和 Stage 3 checkpoints 在同一 [[WildDet3D-Bench]] 配置上的逐阶段结果是多少？
4. Human、Essential 与 Synthetic splits 各自贡献多少？
5. APrare 的增益来自训练频次增加、类别词汇覆盖，还是更接近 benchmark 的图像分布？
6. 去除与 COCO、LVIS、Objects365 和 V3Det 的上游分布重叠后，增益还能保留多少？
7. 各消融结果是否在多个随机种子下稳定？

## 建议补充查找的来源

- 论文实验所使用 commit 对应的 `configs/training/stage2_alldata.py` 与数据加载配置。
- Stage 1、Stage 2、Stage 3 已发布 checkpoints 的逐一重评结果。
- 作者对 `Others` 定义及 paper/code recipe 差异的 issue、commit message 或补充材料。
- [[WildDet3D-Data]] dataset card 的版本历史和 annotation changelog。
- 分别使用 Human、Essential、Synthetic splits 的训练日志。
- 在与 [[WildDet3D-Data]] 无共同上游图像来源的外部 benchmark 上进行的数据消融。

## 综合判断

当前证据支持的最强结论是：**从 Omni3D-only 训练转向完整的多阶段混合训练，能在 [[WildDet3D-Bench]] 上带来约 `15.8–23.3 AP` 的联合增益，并且 rare categories 的绝对增益最大。[3]**

当前证据不支持以下更强表述：

- 该增益主要由 [[WildDet3D-Data]] 产生；
- `Others` 的贡献很小或为负；
- synthetic split 优于 human split；
- 增益完全代表跨数据域的开放词汇泛化。

只有补齐同模型的 `Omni3D + Others` 与 `Omni3D + WildDet3D-Data` 对照，并控制训练预算和 curriculum，才能分离二者的独立贡献。

## 参考来源

[1] [WildDet3D: Scaling Promptable 3D Detection in the Wild](https://allenai.github.io/WildDet3D/)  
[2] Ai2，*Introducing WildDet3D: Open-world 3D detection from a single image*。  
[3] [allenai/WildDet3D GitHub repository](https://github.com/allenai/WildDet3D)  
[4] alphaXiv，*WildDet3D: Scaling Promptable 3D Detection in the Wild*。  
[5] alphaXiv，WildDet3D dataset 与 architecture 综述。  
[6] [WildDet3D Training Guide](https://github.com/allenai/WildDet3D/blob/main/docs/TRAINING.md)  
[7] [allenai/WildDet3D-Data dataset card](https://huggingface.co/datasets/allenai/WildDet3D-Data)  
[8] theresanaiforthat.com，allenai/WildDet3D repository listing。  
[9] [allenai/WildDet3D model card](https://huggingface.co/allenai/WildDet3D)

## References

1. [WildDet3D: Scaling Promptable 3D Detection in the Wild](https://allenai.github.io/WildDet3D) — allenai.github.io
2. [Introducing WildDet3D: Open-world 3D detection from a ...](https://allenai.org/blog/wilddet3d) — allenai.org
3. [WildDet3D: Scaling Promptable 3D Detection in the Wild](https://github.com/allenai/WildDet3D) — github.com
4. [WildDet3D: Scaling Promptable 3D Detection in the Wild | alphaXiv](https://www.alphaxiv.org/overview/2604.08626) — alphaxiv.org
5. [WildDet3D: Scaling Promptable 3D Detection in the Wild | alphaXiv](https://www.alphaxiv.org/abs/2604.08626) — alphaxiv.org
6. [WildDet3D/docs/TRAINING.md at main - GitHub](https://github.com/allenai/WildDet3D/blob/main/docs/TRAINING.md) — github.com
7. [allenai/WildDet3D-Data · Datasets at Hugging Face](https://huggingface.co/datasets/allenai/WildDet3D-Data) — huggingface.co
8. [allenai/WildDet3D | Repositories](https://theresanaiforthat.com/company/allenai/repository/WildDet3D) — theresanaiforthat.com
9. [allenai/WildDet3D](https://huggingface.co/allenai/WildDet3D) — huggingface.co
