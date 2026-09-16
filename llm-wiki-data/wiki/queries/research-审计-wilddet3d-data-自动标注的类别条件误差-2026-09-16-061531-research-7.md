---
type: query
title: "Research: 审计 WildDet3D-Data 自动标注的类别条件误差"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: 审计 WildDet3D-Data 自动标注的类别条件误差

我会按 `wiki-maintenance` 的 query/synthesis 流程处理：先核对本项目的状态、Wiki 索引与引用约定，再产出不落盘的中文页面草稿；重点会区分“来源明确支持的事实”和“建议采用的审计设计”。当前工作目录本身就是 `llm-wiki-data/`，因此仓库说明里的相对路径多了一层；我正在按实际目录结构定位这些文件，随后继续，不会据此猜测内容。---
type: synthesis
title: 审计 WildDet3D-Data 自动标注的类别条件误差
created: 2026-09-16
updated: 2026-09-16
status: draft
tags: [WildDet3D-Data, 3D-annotation, VLM, dataset-audit, category-conditional-error]
related: [WildDet3D-Data, WildDet3D-Bench, 多模型候选-人工-VLM-混合-3D-标注, 非穷举-3D-标注下的-ignore-region-suppression]
---

# 审计 WildDet3D-Data 自动标注的类别条件误差

## 摘要

[[WildDet3D-Data|WildDet3D-Data]]将 COCO、LVIS、Objects365 和 V3Det 的 2D annotations 扩展为开放词汇 3D bounding boxes。其训练数据包含约 `102,979` 张人工审核图像和 `896,004` 张经 VLM 自动筛选的图像；自动部分约有 `3.48M` 个 annotations，是数据集的主要组成部分。[1][2] 因此，对其质量的关键问题不只是“总体错误率多高”，而是错误是否随类别频率、物理尺度、形状、对称性、场景来源及文化背景系统性变化。

现有证据表明，VLM score 与人工接受率具有一定相关性，但只能提供中等强度的逐样本判别：论文报告 `AUC=0.66`，最高频的 score `10` 区间仍有 `16.7%` 的人工 rejection rate。不同候选生成器的 rejection rate 也从 `12.5%` 到 `42.9%` 不等。[1] 这些聚合结果不足以确定哪些类别受到的污染最严重，也不能排除多个自动筛选阶段共同造成类别选择偏差。

本页提出一个类别分层、双向覆盖且保留候选来源的审计方案。核心输出应同时包含：已发布 annotation 的 false-acceptance error、被过滤候选中的 false-rejection error，以及按类别与几何属性分解的 center、dimensions、rotation 和 semantic errors。

## 审计对象与误差定义

这里的“类别条件误差”不是单纯的 category-name classification error，而是任意标注错误在类别条件下的分布：

$$
P(E_k=1\mid C=c,G=g,S=s)
$$

其中：

- $E_k$ 表示第 $k$ 类错误，如语义、深度、尺寸或旋转错误；
- $C$ 是 category；
- $G$ 是几何或视觉属性，如尺度、对称性、遮挡与截断；
- $S$ 是数据来源、候选生成器、VLM score bin 或审核路径。

审计应覆盖三种不同问题：

1. **标注精度**：已保留的 3D box 是否正确。
2. **筛选召回率**：可接受的候选是否被自动流程错误删除。
3. **数据代表性**：某些类别是否因先验、过滤器或 VLM 判断而较少进入最终数据。

只检查发布后的 JSON 可以估计第一项，却无法估计第二、三项。后两项需要被拒绝候选、候选生成器身份和各阶段决策日志。

## 数据构建与潜在偏差路径

[[多模型候选-人工-VLM-混合-3D-标注|多模型候选—人工/VLM 混合 3D 标注]]首先使用五种方法生成候选：3D-MOOD、DetAny3D、SAM-3D、RANSAC-PCA 和 LabelAny3D。候选经过几何优化和规则过滤，随后进入人工选择或 VLM 自动选择路径。[1][3][4]

该结构可能产生以下类别条件误差：

| 阶段 | 潜在误差 | 容易受影响的类别 |
|---|---|---|
| 既有 2D annotation | category 错配、非穷举实例 | 长尾类别、小物体、密集物体 |
| depth 与 camera estimation | center depth、metric scale 偏差 | 透明、反光、细长及远距离物体 |
| 五种候选生成器 | 候选覆盖不足或几何模式偏差 | 非刚体、开放结构、非典型姿态物体 |
| 类别尺寸先验 | 过滤真实但少见的尺寸 | 玩具、微缩模型、巨型装置、幼体 |
| depicted/composite filter | 将真实目标误判为图像内图像 | 屏幕、海报、镜子、展品 |
| VLM selection | semantic、shape、rotation 判断偏差 | 细粒度类别、文化特定物体、对称物体 |
| 只保留最高分候选 | 模式坍缩式选择 | 存在多个几何上合理解释的类别 |

多级自动决策还可能形成“相关误差”：如果尺寸先验、过滤器与最终选择器共享相似的训练分布，前一阶段留下的偏差不会被后一阶段独立纠正。[[WildDet3D-Data|WildDet3D-Data]]使用 GPT-4.1-mini、Qwen3.5-9B 和 fine-tuned Molmo2 承担不同筛选任务，因此不能把这些阶段视为统计独立的质量保障。[1]

## 现有质量证据

### 总体人工复核结果

人工分支报告的候选 rejection rate 为：

| 候选生成器 | 人工 rejection rate |
|---|---:|
| RANSAC-PCA | 12.5% |
| SAM-3D | 17.3% |
| LabelAny3D | 21.3% |
| 3D-MOOD | 25.7% |
| DetAny3D | 42.9% |
| 总体 | 22.0% |

生成器间超过三倍的差距说明 candidate provenance 是必要的审计变量。[1] 如果某些类别主要由高拒绝率生成器覆盖，其最终噪声或缺失风险可能明显高于全局平均值。

VLM score 与人工 rejection rate 呈聚合单调关系：

| VLM score | 人工 rejection rate | 样本量 |
|---:|---:|---:|
| `<7` | 71.9% | 1,992 |
| `7` | 67.4% | 13,670 |
| `8` | 45.3% | 18,665 |
| `9` | 36.1% | 83,882 |
| `10` | 16.7% | 310,329 |
| `11` | 9.2% | 52,684 |

但 `AUC=0.66` 表明该分数的逐样本区分能力有限；即使高分区间也不能视为人工验证的等价替代。[1] 论文没有进一步报告 `rejection rate × category`、`generator × category` 或 `score × category` 的交叉结果。

### 外部证据的适用边界

其他 3D/VLM 工作提示了可能的错误机制，但不能替代对 WildDet3D-Data 的直接审计：

- VLM-Grounder 报告，相似外观实例会造成跨视图错误匹配，需要以 point-cloud Chamfer distance 过滤。[8]
- Objaverse annotation 研究指出，多视图之间可能产生不一致，而且有限的人类 ground truth 难以支持大规模 calibration。[9]
- VLM-3R 的结果显示，多种 VLM 在绝对距离、物体尺寸和空间关系任务上仍显著低于人类水平。[10]
- 文化遗产元数据研究发现，自动分类产生更多类别和更多离群错误，而人工分类更能识别名称、方法等复杂概念。[11]

这些结果支持开展类别与属性分层审计，但不证明相同错误率必然出现在 [[WildDet3D-Data|WildDet3D-Data]] 中。

## 建议的审计设计

### 构建独立 gold subset

从自动训练集分层抽取 annotation，由不知道原候选来源、VLM score 和选中结果的人工审核者重新判断。每个样本至少应由两名审核者独立标注，争议样本进入第三方 adjudication。

人工界面应同时展示：

- 原始 RGB image；
- 透视 3D box overlay；
- 至少三个正交 point-cloud views；
- category name 与原始 2D box；
- camera intrinsics 和 depth visualization；
- 可切换的全部候选，而非只显示被 VLM 选中的候选。

只判断“可接受/不可接受”不足以定位偏差。审核者还应重新给出最佳候选，必要时调整 center、dimensions 与 rotation。

### 分层抽样

不应按 annotation 均匀抽样，因为 frequent categories 会主导结果。建议组合以下 strata：

- category frequency：singleton、2–10、11–100、101–1,000、`>1,000`；
- 语义 superclass：动物、家具、车辆、工具、食物、植物、服饰等；
- 物理尺度与图像尺度；
- 刚体、非刚体、细长、空心、透明、反光与对称属性；
- COCO、LVIS、Objects365、V3Det 来源；
- 五种 candidate generator；
- VLM score bin；
- 室内、室外、自然与 composite scene；
- 遮挡、截断、极端视角和低 depth confidence。

类别内样本不足时，应报告精确置信区间或使用 hierarchical model 部分汇聚，不能把极小样本类别的点估计直接排序。

### 错误分类体系

每个 annotation 至少应标记以下错误：

1. **语义错误**：category 与目标不一致或粒度不一致。
2. **实例关联错误**：3D box 对应相邻的同类或异类对象。
3. **center/depth 错误**：位置或 metric depth 不合理。
4. **dimension 错误**：宽、高、长与物体不匹配。
5. **rotation 错误**：yaw、tilt 或完整姿态错误。
6. **形状近似错误**：3D cuboid 无法合理包围开放、弯曲或非刚体对象。
7. **投影一致性错误**：`bbox3D_cam` 投影与 `bbox2D_proj` 明显错位。
8. **有效性错误**：`valid3D=true`，但目标实际上不可恢复或严重截断。
9. **选择错误**：存在更好的候选，却选择了较差候选。
10. **覆盖错误**：所有候选均被拒绝，但至少一个候选经人工判断可接受。

第 10 类只能通过审核被丢弃的候选获得。发布 JSON 所列 `center_cam`、`dimensions`、`R_cam`、`bbox3D_cam` 和 `bbox2D_proj` 足以支持部分几何检查，但公开结构没有显示 candidate generator、原始候选集或 VLM 分项分数。[2]

### 指标

每个类别应至少报告：

$$
\operatorname{FAR}_c=
\frac{\#\text{自动保留但人工拒绝}}
{\#\text{自动保留且被审核}}
$$

$$
\operatorname{FRR}_c=
\frac{\#\text{自动拒绝但人工接受}}
{\#\text{自动拒绝且被审核}}
$$

几何质量可报告：

- normalized center error；
- depth relative error；
- log-dimension error；
- rotation geodesic error；
- projected 2D IoU；
- 3D IoU 或基于 half-diagonal 的 center matching；
- category-level median、90th percentile 和 catastrophic-error rate。

总体报告应同时包含 micro-average、macro-average、worst-group error 和 frequency-weighted estimate。仅使用 micro-average 会掩盖长尾类别错误；仅使用 macro-average 又可能被极少样本类别的不稳定估计支配。

VLM score 还应按类别计算 calibration curve、Brier score、expected calibration error，并检验相同 score 是否在不同类别上对应相似的真实接受概率。

## 数据量口径的矛盾

不同来源对 annotation 总数给出了 `3.7M`、`3,728,078` 和 `3,910,855` 等数字。[1][2][3][4] 根据公开 split：

- `Human train + Synthetic train + val + test = 3,728,078`；
- `Essential train + Synthetic train + val + test = 3,910,855`。

这是由所列数字推得的解释：Train (Human) 与 Train (Essential) 是重叠或替代性训练版本，而不是可直接相加的互斥 splits。[2] 因此，审计必须明确使用哪个 JSON 版本，并以 annotation ID 或稳定实例键去重。否则，同一批人工 annotation 可能被重复计数。

来源之间对 Human 与 Essential 的 category count 表述也不完全一致；类别数量又不能跨 split 简单求和。正式审计前需要从 `InTheWild_v3__class_map.json` 和各 annotation JSON 重新计算唯一 category、有效 annotation 及重叠关系。

## 与模型结果的关系

加入 WildDet3D-Data 后，[[WildDet3D|WildDet3D]]在 [[WildDet3D-Bench|WildDet3D-Bench]]上的 AP 明显提高。[1][3] 但训练配置同时加入了 `Others`，并且没有单独隔离 Human、Essential 与 Synthetic subsets 的边际贡献。因此，下游 AP 提升不能证明自动 annotation 在所有类别上同样可靠。

rare、common 和 frequent 是评估频率分组，不等同于 train-unseen、文化长尾或几何长尾。按频率报告的 AP 也无法识别“某类别 annotation 数量很多，但尺寸或姿态存在系统偏差”的情况。

此外，[[非穷举-3D-标注下的-ignore-region-suppression|非穷举 3D 标注下的 ignore-region suppression]]会减少已知 annotation gaps 对训练和评估的惩罚，但不能修复已保留 box 的错误几何，也不能恢复被自动筛选流程系统性删除的类别实例。

## 证据缺口

目前公开材料没有充分回答以下问题：

- 自动训练集各类别的人工 rejection rate；
- category、generator 与 VLM score 的联合分布；
- 各类别在候选生成、规则过滤和 VLM 选择阶段的存活率；
- 被删除候选的 false-rejection rate；
- VLM 六项评分的类别条件 calibration；
- 人工审核者之间的一致性；
- Human、Essential 和 Synthetic 中同一实例的重叠关系；
- 透明、反光、非刚体和对称物体的独立质量指标；
- 文化特定类别及非英语类别名称的错误率；
- 自动 annotation noise 对不同类别下游 AP 的因果影响。

来源 [6] 的采集内容为损坏或错误解码的二进制文本，不能作为审计证据使用。

## 建议补充获取的资料

优先级最高的新增材料是：

1. WildDet3D-Data 的 per-candidate provenance 与全部候选，而不只是最终 annotation。
2. Molmo2 的总分、六项分数、prompt、checkpoint 和 calibration 数据。
3. 每个规则过滤阶段的 accept/reject log。
4. Prolific 审核任务、gold questions、审核者一致性和 adjudication 记录。
5. `Human → Essential → Synthetic` 的稳定实例映射与去重规则。
6. 按 category、source dataset 和 candidate generator 分解的质量表。
7. 自动标注与独立人工修订版之间的几何差异数据。
8. 仅改变 Synthetic sampling 或清洗策略的下游 controlled ablation。

文化遗产领域的自动与半自动 3D annotation 系统可作为审核界面、可追溯性和多参与者标注设计的补充参考，但与开放词汇单目 3D detection 的数据分布差异较大，不应直接用于估计错误率。[12][13][14][15]

## 结论

现有材料能够支持三个结论。第一，[[WildDet3D-Data|WildDet3D-Data]]的大规模训练部分主要依赖 VLM 自动筛选，而不是逐项人工验证。[1][2] 第二，自动评分与人工判断相关，但 `AUC=0.66` 和高分区间仍存在的 rejection 表明残余噪声不可忽略。[1] 第三，当前公开结果只提供生成器和 score 层面的聚合质量，尚不足以判断误差是否集中于特定类别。

因此，可信的类别条件审计必须同时追踪已接受与已拒绝候选，保留生成器和筛选阶段 provenance，并以 category × geometry × source 的交叉分层报告 false acceptance、false rejection 和连续几何误差。若缺少这些数据，审计最多只能测量发布 annotation 的残余污染，不能评价自动标注流程对长尾类别的完整影响。

## 参考来源

[1] allenai/WildDet3D GitHub repository。  
[2] allenai/WildDet3D-Data，Hugging Face Datasets。  
[3] “Introducing WildDet3D: Open-world 3D detection from a single image”，Ai2。  
[4] “WildDet3D: Scaling Promptable 3D Detection in the Wild”，项目页面。  
[5] “Detect Anything 3D in the Wild”。  
[6] “Leveraging VLM-Based Pipelines to Annotate 3D Objects”；所提供内容损坏，未作为证据。  
[7] “Vision-language model”，Wikipedia。  
[8] “VLM-Grounder: A VLM Agent for Zero-Shot 3D Visual Grounding”。  
[9] “Evaluating VLMs for Score-Based, Multi-Probe Annotation ...”。  
[10] “VLM-3R: Vision-Language Models Augmented with Instruction-Aligned 3D Reconstruction”。  
[11] “Large-Scale Metadata Processing for 3D Cultural Heritage Objects”。  
[12] “Automated Scanning Technology for 3D Digitisation”。  
[13] “Aïoli: A reality-based 3D annotation cloud platform ...”。  
[14] “Ray-Based Textual Annotation on 3D Cultural Objects”。  
[15] “Automatic Extraction and Labelling of Memorial Objects ...”。

## References

1. [GitHub - allenai/WildDet3D: Allen Institute for AI: WildDet3D: Scaling Promptable 3D Detection in the Wild · GitHub](https://github.com/allenai/WildDet3D) — github.com
2. [allenai/WildDet3D-Data · Datasets at Hugging Face](https://huggingface.co/datasets/allenai/WildDet3D-Data) — huggingface.co
3. [Introducing WildDet3D: Open-world 3D detection from a single image | Ai2](https://allenai.org/blog/wilddet3d) — allenai.org
4. [WildDet3D: Scaling Promptable 3D Detection in the Wild](https://allenai.github.io/WildDet3D) — allenai.github.io
5. [Detect Anything 3D in the Wild](https://arxiv.org/html/2504.07958v1) — arxiv.org
6. [Leveraging VLM-Based Pipelines to Annotate 3D Objects](https://raw.githubusercontent.com/mlresearch/v235/main/assets/kabra24a/kabra24a.pdf) — raw.githubusercontent.com
7. [Vision-language model - Wikipedia](https://en.wikipedia.org/wiki/Vision-language_model) — en.wikipedia.org
8. [VLM-Grounder: A VLM Agent for Zero-Shot 3D Visual Grounding](https://arxiv.org/html/2410.13860v1) — arxiv.org
9. [Evaluating VLMs for Score-Based, Multi-Probe Annotation ...](https://openreview.net/pdf/b21b8f66491a4d009ef55fbc02422d7f145a9686.pdf) — openreview.net
10. [VLM-3R: Vision-Language Models Augmented with Instruction-Aligned 3D Reconstruction](https://vlm-3r.github.io) — vlm-3r.github.io
11. [Large-Scale Metadata Processing for 3D Cultural Heritage Objects](https://www.mdpi.com/2073-445X/15/5/751) — mdpi.com
12. [Automated Scanning Technology for 3D Digitisation](https://www.europeanheritageawards.eu/winners/cultlab3d-automated-scanning-technology-3d-digitisation) — europeanheritageawards.eu
13. [Aïoli: A reality-based 3D annotation cloud platform for the ...](https://hal.science/hal-04249650/file/DAACH_Aioli_DEF_05_2023_rev_full.pdf) — hal.science
14. [Ray-Based Textual Annotation on 3D Cultural Objects](https://www.semanticscholar.org/paper/ART3mis%3A-Ray-Based-Textual-Annotation-on-3D-Objects-Arampatzakis-Sevetlidis/bf3c5002f27952c2de68b656a0b2817767d7f8df) — semanticscholar.org
15. [Automatic Extraction and Labelling of Memorial Objects ...](https://journal.caa-international.org/articles/10.5334/jcaa.66) — journal.caa-international.org
