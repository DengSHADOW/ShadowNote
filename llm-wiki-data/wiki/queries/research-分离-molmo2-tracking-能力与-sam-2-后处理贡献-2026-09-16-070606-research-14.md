---
type: query
title: "Research: 分离 Molmo2 tracking 能力与 SAM 2 后处理贡献"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: 分离 Molmo2 tracking 能力与 SAM 2 后处理贡献

我会按 `wiki-maintenance` 的 query/synthesis 工作流处理：先核对项目约定与现有 Wiki 索引，再基于给定来源组织一页可直接入库的中文综合条目；当前请求只要求合成页面，因此不改写仓库文件。当前工作目录本身就是 `llm-wiki-data`，而项目约定中的路径以其父级仓库为基准；我正在按实际目录结构重新定位这些文件，避免把嵌套路径误当成缺失内容。# 分离 [[Molmo2]] tracking 能力与 SAM 2 后处理贡献

## 问题界定

[[Molmo2-Track]] 的 mask-based 评测并不直接测量单一模型。完整链条是：

> 视频与文本查询 → [[Molmo2]] 生成带 object ID 的离散 point tracks → SAM 2 将 points 转换为 segmentation masks → 以 J&F 评价 masks。

对部分基线，链条则是：

> 基线模型生成 bounding boxes → SAM 2 生成 masks；同时取 box center 计算 point-based 指标。[2]

因此，J&F 衡量的是“语义定位、跨帧身份关联、prompt 表示、SAM 2 mask 解码及可能的时序传播”的复合结果。把它直接称为 [[Molmo2]] 的 tracking 分数，会高估单一上游模型能够独立解释的贡献。相比之下，point F1 和 [[point-based-HOTA]] 不依赖 SAM 2 生成 mask，更接近 [[Molmo2]] 本身的定位与身份关联能力。[2]

## 能力归属

| 能力 | 主要归属 | 较直接的观测方式 |
|---|---|---|
| 根据文本选择正确对象 | [[Molmo2]] | query-level recall、point F1 |
| 跨帧定位对象 | [[Molmo2]] | point distance、point-in-mask accuracy |
| 维持 object ID | [[Molmo2]] | [[point-based-HOTA]]、identity switch |
| 恢复完整物体范围与边界 | SAM 2 | 在固定 prompt 下的 J、F |
| 遮挡后的 mask 传播与恢复 | SAM 2、prompt schedule 及其交互 | temporal propagation 与逐帧 segmentation 对照 |
| 最终 mask 质量 | 联合流水线 | J&F |

[[Molmo2]] 的 [[统一-point-based-grounding|统一 point-based grounding]]通过重复使用 object ID 表达[[身份保持的-point-tracking|身份保持的 point tracking]]。这种表示能证明模型在输出层面维护了轨迹身份，但不能单独证明像素边界准确，也不能排除 SAM 2 对最终排序的改变。[2]

## 已有证据

[[Molmo2]] 论文报告 Molmo2-4B、Molmo2-8B 和 Molmo2-O-7B 在 [[Molmo2-Track]] 上的 overall J&F 分别为 `56.7`、`56.2` 和 `53.7`。但这些 masks 来自 SAM 2 对模型 points 的转换，因此这些数值应表述为固定 SAM 2 后处理下的端到端结果。[2] Ai2 将 [[Molmo2]] 称为其评测中最强的 tracker，并指出其优于 Molmo + SAM 2 baseline；这一结论支持整体系统的竞争力，却没有单独量化 SAM 2 对 [[Molmo2]] 输出的增益。[4]

SAM 2 的 prompt 设计可能显著影响结果。在 Prompt Self-Correction 的 Table 6 中，无 re-inference 为 `90.25` mIoU，单 box 为 `90.28`，加入 tracking 后仅为 `90.29`；dual-box 加三个 negative points 达到 `90.35`。这说明在该实验中，边界抑制与 prompt 组合比单纯增加运动 tracking 更能解释收益。[1] 不过总差异只有约 `0.10` mIoU，且给定材料没有置信区间，因此不能据此估计 SAM 2 在 [[Molmo2-Track]] 上的具体贡献。

外科视频实验同样显示 prompt 类型和更新频率不可忽略：mask prompt 整体最佳，box 次之，三个随机 points 通常优于单点；30-frame reinitialization 又优于 60-frame 设置。[6] 这支持“后处理配置会改变 tracking 结果”，但医学视频的外观、遮挡和标注分布与 [[Molmo2-Track]] 不同，数值不能直接迁移。

此外，[[Molmo2-VideoTrack]] 的部分训练数据本身也经过 SAM 2：原始 bounding-box tracks 被首个可用 box 初始化为 mask tracklet，并在 box–mask 不一致时重新 prompt。[2] 因而 SAM 2 不仅是评测后处理器，也可能通过训练标签构造间接影响 [[Molmo2]]。严格归因必须同时区分训练数据依赖和推理时依赖。

## 建议的分层评测

### 第一层：不经过 SAM 2 的轨迹评测

直接评价 [[Molmo2]] 输出：

- point precision、recall 与 F1；
- [[point-based-HOTA]]；
- identity switch、track fragmentation 与对象覆盖率；
- 点到 ground-truth mask 或中心线的距离；
- 按遮挡、目标尺寸、视频长度和对象密度分层的结果。

这是判断 [[Molmo2]] 是否找到正确对象、是否持续定位、是否维持身份的主要证据。

### 第二层：固定 prompt 的 SAM 2 评测

向同一个 SAM 2 checkpoint 分别输入：

1. ground-truth points；
2. [[Molmo2]] predicted points；
3. 与 points 时间密度匹配的 ground-truth boxes；
4. baseline predicted boxes；
5. ground-truth masks，作为近似上界。

对每种输入分别报告逐帧 segmentation 与 temporal propagation 结果。ground-truth points 到 masks 的误差反映“point prompt 信息不足、SAM 2 解码及传播”的联合限制；predicted points 与 ground-truth points 的差值则反映在固定 SAM 2 条件下，上游预测误差对最终 masks 的影响。

### 第三层：后处理消融

至少比较：

- 单 positive point；
- 多 positive points；
- point 加 negative points；
- box；
- point 加 box；
- 无 temporal memory 的逐帧 SAM 2；
- 使用 temporal memory 的 SAM 2；
- 固定间隔 reinitialization；
- 基于置信度或不一致性的自适应 re-inference。

每种随机 point 或 negative-point 策略应运行多个 seeds。来源 [1] 和 [6] 都表明，少量 point 的位置与数量可以造成可测差异。

## 归因方式

令 $P_M$ 为 [[Molmo2]] points，$P_G$ 为匹配采样策略的 ground-truth points，$D$ 为固定 SAM 2 配置，则可报告：

$$
Q_{\mathrm{E2E}}=J\&F(D(P_M))
$$

$$
L_{\mathrm{upstream}\mid D}
=J\&F(D(P_G))-J\&F(D(P_M))
$$

$$
L_{\mathrm{prompt+downstream}}
=100-J\&F(D(P_G))
$$

第二项是在特定 SAM 2 条件下的上游损失；第三项不是纯粹的 SAM 2 模型误差，因为它还包含单点 prompt 无法完整表达对象范围的固有限制。因而不应把两项解释为完全可加、与配置无关的因果贡献。

还应分别计算：

$$
\Delta_{\mathrm{temporal}}(P)
=J\&F(D_{\mathrm{temporal}}(P))
-J\&F(D_{\mathrm{frame}}(P))
$$

并同时在 $P_M$ 与 $P_G$ 上报告。这样可以判断 temporal propagation 是普遍有效，还是只在高质量 prompt 下有效。

## 输出格式带来的公平性问题

points 与 boxes 携带的信息不同。points 更适合表达实例存在和身份，boxes 额外编码范围，却可能包含大量背景。[12] 将 baseline box 简单转换为 center point，可能让 point-native 方法在 point-in-mask 指标上占优；不规则对象尤其难被矩形公平表示。[11] 反过来，让 points 和 boxes 分别提示 SAM 2，又会引入不同的 segmentation prompt 效率。

因此不宜只给出一个跨格式总排名。更稳妥的报告方式是同时提供：

- 各模型原生输出格式上的结果；
- 统一格式转换后的结果；
- 固定 prompt budget 的结果；
- SAM 2 后处理前后的分层指标。

## 矛盾、边界与证据缺口

[[Molmo2]] 论文认为 off-the-shelf trackers（包括以 point prompt 使用的 SAM 2）不足以可靠生成 tracking 训练数据，同时又使用 SAM 2 把人工 box tracks 转换成 masks。[2] 两者并非直接矛盾：前者否定的是从稀疏 point 自动产生可靠轨迹，后者保留了人工 box tracks，并设置重新 prompting 与过滤机制。

来源 [1] 强调 prompt self-correction，来源 [6] 则发现 mask 和 box prompts 通常优于 points；这与 [[Molmo2]] 的 point tracking 优势也不构成直接矛盾，因为它们评价的任务、数据域、prompt 数量和指标不同。

当前材料仍缺少以下关键信息：

- [[Molmo2-Track]] 使用的确切 SAM 2 checkpoint、版本与 temporal-memory 配置；
- points 是逐帧输入、按固定间隔输入，还是仅用于初始化；
- 多点、多对象及身份冲突时的 SAM 2 prompt 编码方式；
- 不经过 SAM 2 的完整逐数据集 point F1 与 [[point-based-HOTA]] 明细；
- prompt 随机性、bootstrap 区间及逐视频配对显著性检验；
- 训练数据中经 SAM 2 转换的样本比例及其标签噪声。

## 结论

现有证据支持的最稳健结论是：[[Molmo2]] 的独立贡献主要体现在开放词汇对象选择、离散 point 定位和跨帧 object ID 关联；SAM 2 负责把这些稀疏提示转换为像素级 masks，并可能通过边界恢复、temporal propagation、reinitialization 或漂移显著改变最终 J&F。[1][2][6]

因此，[[Molmo2-Track]] 的 J&F 应称为“[[Molmo2]] 加 SAM 2 的端到端 tracking/segmentation 表现”。只有在同时报告原始 point 指标、ground-truth-prompt SAM 2 上界和 prompt-matched 消融后，才能把 [[Molmo2]] tracking 能力与 SAM 2 后处理贡献作出较可信的分离。

## 值得补充的来源

- [[Molmo2]] 官方评测代码及未经 SAM 2 转换的逐帧预测；
- [[Molmo2-Track]] annotations、prompt 构造与 evaluator 实现；
- SAM 2 官方论文、checkpoint 配置和 video predictor 消融；
- 同一 prompts 在 SAM 2、逐帧 [[SAM]] 及其他 segmentation decoder 上的交叉实验；
- 包含置信区间、多个 prompt seeds 和逐视频配对检验的复现实验。

## References

1. [Prompt Self-Correction for SAM2 Zero-Shot Video Object Segmentation](https://www.mdpi.com/2079-9292/14/18/3602) — mdpi.com
2. [Molmo2Open Weights and Data for Vision-Language Models with Video Understanding and Grounding](https://arxiv.org/html/2601.10611v4) — arxiv.org
4. [Molmo 2: State-of-the-art video understanding, pointing, and tracking | Ai2](https://allenai.org/blog/molmo2) — allenai.org
6. [Systematic evaluation and guidelines for segment anything model in surgical video analysis | npj Digital Surgery](https://www.nature.com/articles/s44484-025-00002-2) — nature.com
11. [Point-It-Out: Benchmarking Embodied Reasoning for Vision Language Models in Multi-Stage Visual Grounding](https://arxiv.org/html/2509.25794v1) — arxiv.org
12. [Thinking with Visual Grounding](https://arxiv.org/html/2606.16122v1) — arxiv.org
