---
type: query
title: "Research: VLM 筛选标注的分类别可靠性与偏差"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: VLM 筛选标注的分类别可靠性与偏差

我会按项目的 Wiki 维护规范处理这次“知识问答式综合”：先核对现有页面与证据规范，再输出可直接入库的中文 Wiki 页面；本轮不会擅自写入仓库。当前工作目录本身就是 `llm-wiki-data/`，而项目约定中的路径按上一级仓库根目录书写；我会修正路径，并只读取与本主题直接相关的现有页面。# VLM 筛选标注的分类别可靠性与偏差

## 概述

[[WildDet3D-Data]]采用[[多模型候选-人工-VLM-混合-3D-标注|多模型候选—人工/VLM 混合 3D 标注]]流程：先从 COCO、LVIS、Objects365 和 V3Det 的既有 2D annotations 生成多个候选 3D boxes，再通过几何与语义规则过滤，最后由人工或 fine-tuned Molmo2 选择候选。[1][3][5][6]

现有证据表明，VLM score 能够在总体上区分较好与较差的候选，但尚不足以证明这种可靠性在不同类别、尺度、场景和频率分组中保持一致。公开材料主要报告全局数据规模、score 分组质量和最终检测 AP，没有公布逐类别 false-acceptance rate、false-rejection rate 或 calibration。因此，[[WildDet3D-Data]]的“分类别可靠性”目前属于尚未充分测量的问题，而不是已经验证的属性。

## 数据组成与自动筛选占比

公开数据页给出的主要训练划分如下：[2][4]

| 划分 | 图像数 | 标注数 | 类别数 | 选择方式 |
|---|---:|---:|---:|---|
| Train (Human) | 102,979 | 229,934 | 11,879 | 人工审核 |
| Train (Essential) | 102,979 | 412,711 | 12,064 | 人工核心加 VLM-qualified small objects |
| Train (Synthetic) | 896,004 | 3,483,292 | 11,896 | VLM 自动选择 |
| Val | 2,470 | 9,256 | 785 | 人工标注 |
| Test | 2,433 | 5,596 | 633 | 人工标注 |

按 repository 的 `3,910,855` 条总标注口径，Train (Synthetic) 约占 `89.1%`；若再计入 Train (Essential) 中相对 Train (Human) 新增的 `182,777` 个 VLM-qualified small objects，则约 `93.7%` 的最终标注经过 VLM 自动选择或资格判定。[2][4] 因此，整体数据质量在很大程度上取决于 VLM 筛选，而人工核心集和人工 val/test 不能直接代表其余约 90% 自动标注的分类别质量。

## 已获得支持的可靠性结论

### 总体排序具有信息量

论文报告的人工复核结果显示，VLM score 越高，候选被人工拒绝的比例总体越低：score 小于 `7` 时 rejection rate 为 `71.9%`，score 为 `9` 时为 `36.1%`，score 为 `10` 时为 `16.7%`，score 为 `11` 时为 `9.2%`。这种单调趋势说明 VLM score 可用于总体质量排序。[3][6]

但候选级区分能力并不强：已有 Wiki 来源页记录的 AUC 仅为 `0.66`，而进入主要保留区间的 score `10` 候选仍有约六分之一被人工拒绝。由此更合理的结论是：VLM 可压缩人工审核范围，但尚不能视为人工验证的等价替代。这个现象也属于广义的[[自动指标与人工感知质量错位]]。

### 候选来源显著影响质量

不同 3D candidate generator 的人工 rejection rate 从 RANSAC-PCA 的 `12.5%` 到 DetAny3D 的 `42.9%`，相差超过三倍。这说明最终标注可靠性不仅取决于 VLM，还取决于某一类别更容易由哪种 candidate generator 产生可用候选。

如果某些类别主要依赖高拒绝率生成器，其残余标注噪声可能高于主要由低拒绝率生成器覆盖的类别。现有材料没有给出“类别 × 生成器 × VLM score”的联合统计，因此无法判断 VLM 是否真正消除了这种来源偏差。

### 检测性能不能替代标注审计

在 [[WildDet3D-Bench]] 上，使用扩大训练数据后的 [[WildDet3D]]取得 `AP_r=28.3`、`AP_c=21.6`、`AP_f=18.7`；加入 depth 后分别为 `47.4`、`40.7` 和 `37.2`。[2][6] 这些结果表明大规模训练对 rare evaluation categories 有效，但不能据此推出 rare-category annotations 更准确。

AP 同时受到模型架构、训练样本数、类别难度、prompt、depth 和评估匹配规则影响。这里的 rare、common 和 frequent 是评估频率分组，也不等同于 train-unseen categories。分类别标注可靠性必须通过独立人工审计测量，而不能从下游 AP 反推。

## 主要偏差来源

| 环节 | 可能产生的分类别偏差 | 当前证据状态 |
|---|---|---|
| 2D 数据起点 | 原始数据集中缺失、低频或标注不完整的类别无法被后续流程恢复 | 已知数据来自四个既有 2D datasets，但未报告覆盖缺口[1][2] |
| 候选生成 | 不同形状、姿态或场景的类别可能依赖不同 generator，而 generator rejection rate 差异很大 | 有总体 generator 统计，无逐类别交叉表 |
| depicted-object filter | 海报、屏幕、绘画和真实物体之间的边界可能随类别变化 | VLM 用于过滤 depicted objects，但无分类别误杀率[6] |
| 物理尺寸先验 | 非典型尺度、玩具、模型、雕塑及文化特定物体可能被当作不合理候选 | LLM 提供类别尺寸范围，但无先验覆盖率与错误率[6] |
| small-object qualification | 小目标在 Train (Essential) 中由 VLM 补充，可能形成与较大目标不同的噪声分布 | 划分明确，未见独立 small-object 精度审计[2][4] |
| Molmo2 排序 | 长尾类别、细粒度类别或视觉相似类别可能获得系统性偏低或偏高的 score | 仅有总体 score calibration，无逐类别结果[3] |
| 缺失 3D 标注 | 未获得有效 3D box 的真实对象可能被误当背景 | [[非穷举-3D-标注下的-ignore-region-suppression]]缓解训练惩罚，但不能恢复缺失标注 |
| 人工验证 | 人工审核可提高精度，但标注者一致性及其分类别差异未披露 | 只确认存在人工验证流程[1][5][8] |

其中，尺寸先验和 depicted-object filtering 尤其可能影响类别分布：规则对常见、尺度稳定、外观典型的物体较容易奏效，却可能系统性排除玩具车、巨型装饰物、透明容器、折叠家具、艺术装置或图像中的边界案例。这是一项由流程设计推导出的风险，公开结果尚未量化其实际强度。

相关长尾 3D detection 研究发现，细粒度类别容易被同一 superclass 中的主导类别吸收，例如 truck、construction-vehicle 和 emergency-vehicle 被预测为 car，细粒度 pedestrian categories 被预测为 adult。[7] 该研究不是对 [[WildDet3D-Data]] 的直接审计，但说明只报告总体质量可能掩盖类别层级和共现关系造成的系统性错误。

## 来源陈述与数字口径的不一致

部分项目介绍将 [[WildDet3D-Data]]概括为“retaining only human-verified annotations”或“3.7 million verified annotations”。[1][5] 但 repository 和 Hugging Face 数据页明确区分人工、VLM-qualified 和 VLM auto-selected 标注。[2][4] 因而，“全部标注均经人工验证”并不受公开划分支持。

总标注数也存在两个可解释但容易混淆的口径：

- 约 `3.728M` 对应 Train (Human)、Train (Synthetic)、val 和 test 的合计。
- `3,910,855` 对应 Train (Essential)、Train (Synthetic)、val 和 test 的合计；Train (Human) 是 Train (Essential) 的子集，不应重复相加。[2][4]

此外，Train (Human) 的类别数在 repository 表格中为 `11,879`，而部分论文整理材料记为 `12,064`；后者也可能实际对应 Train (Essential)。在获得原始 class map 和划分生成脚本前，应保留这一口径差异。

## 当前可以与不可以得出的结论

现有资料支持以下判断：

- VLM score 与总体人工接受率存在正相关。
- 自动筛选承担了绝大多数训练标注的质量控制。
- 不同 candidate generator 的质量差异显著。
- 人工 val/test 能提供较可信的下游评估，但不能直接证明 synthetic train 的逐类别质量。
- [[WildDet3D]]在 rare frequency split 上的较高 AP 表明长尾训练具有实用价值，但不是分类别标注准确率的直接证据。

现有资料尚不支持以下判断：

- 所有 `13.5K` categories 具有近似一致的标注可靠性。
- VLM 对 rare categories 的筛选与 frequent categories 同样校准。
- 高 VLM score 在每个类别中都对应低 rejection rate。
- VLM 过滤不存在尺度、文化、场景或 superclass 偏差。
- `VLM auto-selected` 可以与 `human-verified` 互换表述。

## 建议补充的验证

最优先需要获得的是按 category frequency、object size、scene type、source dataset 和 candidate generator 分层的人工复核样本。每个分层至少应报告：

$$
\text{误接收率}
=
\frac{\text{人工拒绝但被 VLM 保留的候选数}}
{\text{被 VLM 保留并复核的候选数}}
$$

$$
\text{误拒绝率}
=
\frac{\text{人工接受但被 VLM 排除的候选数}}
{\text{被人工接受并纳入比较的候选数}}
$$

还应补充逐类别 calibration curve、score threshold sensitivity、人工标注者一致性、被拒绝候选的完整审计样本，以及包含玩具、depicted objects、非典型尺度和文化特定物体的对抗测试集。若数据发布能够加入 candidate generator、VLM score、过滤原因和人工审核状态等 provenance 字段，就可以直接研究偏差来源；当前公开 COCO3D JSON 主要提供最终 3D geometry 和 `valid3D`，不足以重建完整筛选过程。[4]

## 证据局限

来源 [1]、[2]、[4] 和 [5] 均来自项目作者或其发布平台；[3] 与 [6] 是对同一工作的二次整理，[8] 与 [9] 是媒体或社交平台摘要。因此，多数材料并非相互独立的验证。[7] 提供了相关长尾分类错误的独立背景，但研究对象与筛选流程不同。关于分类别可靠性的核心结论仍需要独立人工审计或第三方复现。

## 参考来源

[1] *WildDet3D: Scaling Promptable 3D Detection in the Wild*，项目网站。  
[2] `allenai/WildDet3D`，GitHub repository。  
[3] *WildDet3D: Scaling Promptable 3D Detection in the Wild*，alphaXiv 方法摘要。  
[4] `allenai/WildDet3D-Data`，Hugging Face 数据页。  
[5] *Introducing WildDet3D: Open-world 3D detection from a ...*，Allen Institute for AI。  
[6] *WildDet3D: Scaling Promptable 3D Detection in the Wild*，alphaXiv 数据流程与实验摘要。  
[7] *Towards Long-Tailed 3D Detection*。  
[8] *WildDet3D Wants to Break 3D Detection Out of the ...*，HackerNoon。  
[9] *Allen AI just dropped WildDet3D on Hugging Face A ...*，X。

## References

1. [WildDet3D: Scaling Promptable 3D Detection in the Wild](https://allenai.github.io/WildDet3D) — allenai.github.io
2. [WildDet3D: Scaling Promptable 3D Detection in the Wild](https://github.com/allenai/WildDet3D) — github.com
3. [WildDet3D: Scaling Promptable 3D Detection in the Wild | alphaXiv](https://www.alphaxiv.org/overview/2604.08626) — alphaxiv.org
4. [allenai/WildDet3D-Data · Datasets at Hugging Face](https://huggingface.co/datasets/allenai/WildDet3D-Data) — huggingface.co
5. [Introducing WildDet3D: Open-world 3D detection from a ...](https://allenai.org/blog/wilddet3d) — allenai.org
6. [WildDet3D: Scaling Promptable 3D Detection in the Wild | alphaXiv](https://www.alphaxiv.org/abs/2604.08626) — alphaxiv.org
7. [[PDF] Towards Long-Tailed 3D Detection](https://proceedings.mlr.press/v205/peri23a/peri23a.pdf) — proceedings.mlr.press
8. [WildDet3D Wants to Break 3D Detection Out of the ...](https://hackernoon.com/wilddet3d-wants-to-break-3d-detection-out-of-the-benchmark-box) — hackernoon.com
9. [Allen AI just dropped WildDet3D on Hugging Face A ...](https://x.com/HuggingPapers/status/2041518836168479157) — x.com
