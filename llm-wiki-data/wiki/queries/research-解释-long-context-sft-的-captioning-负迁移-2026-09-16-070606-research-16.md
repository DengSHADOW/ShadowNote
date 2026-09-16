---
type: query
title: "Research: 解释 long-context SFT 的 captioning 负迁移"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: 解释 long-context SFT 的 captioning 负迁移

我会按 `wiki-maintenance` 的 query/综合写作流程处理：先核对项目约定与现有 Wiki 页面，再把证据强弱、机制解释、矛盾与待补来源分开写清；本次先输出可直接入库的中文页面，不擅自改动 Wiki 文件。当前工作目录看起来已经是 Wiki 数据目录，AGENTS.md 中的路径以仓库上一级为基准；我会先定位实际文件位置，再继续读取，避免把路径错误当成内容缺失。# long-context SFT 的 captioning 负迁移

## 定义与范围

long-context SFT 的 captioning 负迁移，是指模型接受长视频、长视觉序列或长 caption 的监督微调后，虽然更容易生成较长描述，却在下列一个或多个维度出现退化：

- 相同输入条件下，短 caption、通用视觉理解或其他指令任务的性能下降；
- 输入帧数增加时，事实相关性、时序一致性或多细节召回率下降；
- 输出长度增加，但单位命题的正确率降低，幻觉增多；
- 模型更倾向于冗长描述，难以遵循简洁、特定格式或其他任务指令。

必须区分两类现象：一是微调造成的参数级负迁移，即微调后旧能力在相同评测条件下下降；二是推理时的上下文退化，即模型面对更多帧或更长提示时表现下降。长视频性能随视频长度下降本身不能证明发生了 catastrophic forgetting。

## 核心结论

现有证据更支持一种复合解释：long-context SFT 的 captioning 负迁移并非单一的“上下文太长”，而是监督分布偏移、有效上下文不足、多细节干扰、caption 噪声以及 instruction-following 漂移共同作用的结果。

其典型因果链可以概括为：

> 更长的视频与标注  
> → 更多视觉 token、事件和文本命题  
> → 更高的检索、聚合与 grounding 难度  
> → 长样本在训练损失中占据更大影响，模型形成“默认详细描述”的输出先验  
> → 微调后的模型在长输入下同时遭受位置退化和干扰  
> → 表现为冗长、漏掉中段事件、事实密度下降、幻觉增加，以及原有指令能力退化。

因此，扩展 context window、训练长 caption 和保持原有能力是三个相互关联但不能互相替代的问题。

## 主要机制

### 监督目标诱导的输出先验迁移

LongCaptioning 的受控实验显示，在固定采样 64 帧的条件下，训练 caption 的标注长度从小于 300、500 增加到 700 token 时，模型生成的 caption 也随之变长。[11] 这说明 long-caption SFT 不只是赋予模型生成长文本的“能力”，还改变了其输出长度与描述粒度的先验。

在 token-level cross-entropy 训练中，如果损失没有按样本长度进行适当归一化，长 caption 会产生更多监督 token，从而对梯度具有更大的累计贡献。即使使用了归一化，长 caption 数据的大量出现也会改变条件输出分布。由此可以推断，模型可能把“视觉描述任务”与“尽可能详细地列举内容”绑定起来，在要求简短摘要、特定格式或高事实密度时产生负迁移。

LongCaptioning 使用 LoRA，仅更新 LLM 中一部分参数。[1] 这限制了参数改动范围，但不能排除输出策略或 instruction-following 行为发生迁移；小规模参数更新仍可能显著改变解码分布。

### 名义上下文长度不等于有效上下文长度

LongCaptioning 通过缩放视觉 token 位置编码的旋转频率来扩展视觉 context window，使模型可以输入更多采样帧。[1] 移除该扩展后，长度分数下降 8.6、质量分数下降 2.1、相关性分数下降 0.24，说明原始有效窗口确实是长视频 captioning 的一个瓶颈。[11]

但 context window 扩展主要解决“能否放入更多 token”，并不保证模型能够可靠利用这些 token。LongCaptioning 同时观察到：随着视频时长增加，输出长度反而逐渐下降，并将其归因于输入超过模型能够处理的有效 context window。[11] [[MLVU]] 类长视频评测也表明，多数 MLLM 在更长视频上明显退化，尤其难以完成 action order、action count 和需要综合多个细节的 summarization。[3]

因此，窗口扩展可以减轻硬容量不足，却不能自动解决：

- 中间位置的信息利用不足；
- 多帧之间的实体与事件对应；
- 重复或近似视觉 token 造成的注意力竞争；
- 多个分散事件的排序、计数和聚合。

关于 lost-in-the-middle 和 distractor interference 的材料进一步提出，中段信息可能被系统性弱化，而一个语义相近但无关的干扰项就可能造成非平滑的准确率下降。[2] 不过该来源属于综述性网页，所述幅度仍需回查其引用的原始实验。

### 多细节聚合负担与干扰累积

长视频 captioning 不是简单的长文本生成，而是从大量视觉观察中选择事件、建立时间顺序，并压缩成连贯叙述。[[MLVU]] 的结果显示，模型在单一细节任务上尚可工作的情况下，面对多细节 action order、action count 和 summarization 仍可能出现显著退化。[3]

帧数增加还会引入大量相似或重复信息。模型必须区分：

- 同一动作的连续帧与不同动作；
- 重复出现的同一实体与外观相似的不同实体；
- 叙事主线与短暂背景事件；
- 与 caption 目标相关的证据和视觉干扰项。

VIVECaption 认为，把 character detection 等子任务全部塞入 captioning VLM 的长上下文，会增加模型负担；将特定变量交给独立模型处理可以提升 caption 质量。[12] 这支持“模块化先验提取能够减少上下文干扰”的解释，但尚不能证明所有长上下文 captioning 都应采用分阶段架构。

### 长 caption 增加 grounding 与幻觉风险

caption 越长，其中包含的可验证命题通常越多。即使每个命题的错误概率不变，整段 caption 至少包含一个错误的概率也会上升。更现实的情况是，细粒度属性、空间关系和短暂动作本身就比粗粒度主题更难 grounding。

Bridging the Visual Gap 指出，小规模 VLM 在长而详细的 image caption 上微调时，难以同时保持描述丰富度与事实可靠性；简单缩短 caption 或使用常规数据筛选并不能完全解决幻觉问题。该工作因此提出按独立命题评估 caption 的 Decomposed NLI，而不是只给整段文本一个总体分数。[13]

LongCaptioning 的数据合成消融也提供了相关证据：

- 只使用 frame-level caption 时，模型较难捕捉动态变化与动作连续性，生成结果连贯性下降；
- 只使用 clip-level caption 时，标注和模型输出都会变短；
- 同时利用 frame-level 与 clip-level caption，可以在局部细节和时序连贯性之间取得更好的平衡。[1][11]

这说明负迁移可能源于监督信号本身的结构失衡：局部 caption 容易形成“细节清单”，全局 caption 则容易遗漏短暂事件。单纯增加 caption 长度不能保证新增文本具有可靠的视觉依据。

视频伪 caption 可以比 alt-text 或逐帧 caption 包含更多动作与时间信息，并具有良好的数据扩展性。[14] 但大规模合成也可能累积 teacher model 的幻觉、遗漏和叙事偏好。现有材料尚未给出伪标注规模、caption 长度与命题级错误率之间的受控关系。

### instruction-following 漂移与 catastrophic forgetting

连续 instruction tuning 研究发现，模型在学习新任务时可能失去原有领域知识、推理或阅读理解能力。[6][7] 然而，Instruction Vector 分析提出了更细的解释：性能下降主要由 instruction-following 概率发生变化驱动，微调通常引入新的专门化推理模式，而不一定真正删除原有知识。[8]

这一解释适用于 long-caption SFT：模型可能仍然具备短 caption 或简洁回答所需的视觉知识，却因为新的指令—输出映射更强，倾向于采用长篇、细节密集的回答模式。此时观察到的“遗忘”更接近行为选择或任务路由漂移，而非知识完全消失。

关于 continual [[visual-instruction-tuning]] 的二手资料还报告了 dual catastrophic forgetting：视觉理解与 instruction following 可能同时退化，并分别与视觉特征间的任务干扰、指令格式冲突有关。[10] 不过该结论在当前材料中来自 paper note，正式引用前应核对 SMoLoRA 原论文。

## 统一解释

long-context captioning 的性能由至少三个彼此独立的容量决定：

1. **输入容量**：模型能否接收足够多的帧和视觉 token。
2. **整合容量**：模型能否从长序列中检索、排序和聚合相关证据。
3. **输出与 grounding 容量**：模型能否生成更多命题，同时保持每个命题有视觉依据。

视觉 context window extension 主要改善第一项；LongCaption-10K 一类长标注主要改变第三项中的输出长度能力；frame-level 与 clip-level 联合标注有助于第二、第三项之间的平衡。[1][11] 如果只增强其中一项，便可能出现以下错配：

| 观察到的现象 | 更可能的机制 | 不能直接推出的结论 |
|---|---|---|
| 增加训练 caption 长度后输出更长 | 输出长度先验迁移 | 模型对视频理解更深入 |
| 增加帧数后性能下降 | 有效窗口不足、干扰或多细节聚合失败 | 参数级 catastrophic forgetting |
| 输出更长但事实错误更多 | 命题数量增加、监督噪声或 grounding 失败 | context window 本身太短 |
| 短 caption 或格式遵循能力下降 | instruction-following 漂移或参数级负迁移 | 原有视觉知识已经消失 |
| 关闭位置扩展后全面退化 | 输入容量确实构成瓶颈 | 继续无限扩展上下文必然继续获益 |
| 中段事件频繁遗漏 | lost-in-the-middle 或时间聚合失败 | 仅增加长 caption 训练即可修复 |

## 表面矛盾及其解释

### context window 扩展有益，但过长上下文又有害

LongCaptioning 表明窗口扩展能够提升输出长度、质量与相关性。[11] 其他来源则认为长上下文会引起位置偏差、recency bias 和干扰。[2][4][12]

二者并不矛盾。窗口扩展把模型从“输入被截断或严重越界”提升到“可以访问更多证据”，因此最初会带来收益；但随着 token 继续增加，检索和聚合难度仍会增长，边际收益可能转为负值。这里关键的是 effective context window，而不是模型声明的最大 token 数。

### 长 caption 更丰富，但也更容易幻觉

LongCaptioning 和大规模视频 pseudo-captioning 表明，长标注能够促进详细、具有时间信息的描述。[1][11][14] Bridging the Visual Gap 则强调详细 caption 与幻觉之间的张力。[13]

这意味着输出长度不是单调的质量指标。较长 caption 可以提高事件覆盖率，同时降低单位命题的精确率。若评估只奖励长度、词汇重叠或表面细节，可能掩盖 factuality 的恶化。

### catastrophic forgetting 可能是能力丢失，也可能是行为路由改变

传统 continual fine-tuning 结果将旧任务性能下降解释为 catastrophic forgetting。[6][7] Instruction Vector 研究则认为，instruction-following 变化通常比知识概率变化更能解释下降。[8]

因此，“long-context SFT 使 captioning 变差”至少包含两种需要实验区分的情况：模型不再拥有旧能力，以及模型拥有旧能力但不再选择正确的回答策略。

## 建议的验证实验

要确认是否存在真正的 captioning 负迁移，应采用匹配训练预算的因子实验，而不是只比较视频长度不同的结果。

### 训练条件

至少比较以下条件：

- 不进行 caption SFT 的 backbone；
- 使用短 caption SFT；
- 使用长 caption SFT；
- 使用长 caption SFT，并混入短 caption 与通用指令 replay；
- 分别开启和关闭视觉 context window extension。

各组应尽量匹配训练 token 数、优化步数、学习率、视频数量、采样帧数和 LoRA 配置，避免把额外训练量误认为 caption 长度效应。

### 评测维度

- **长度与压缩能力**：在相同视频上分别要求一句话、短段落和长描述，检查模型能否按指令控制长度。
- **命题级事实性**：将 caption 拆分为原子命题，采用 DNLI 或人工核验统计支持、矛盾和无法判断的命题。[13]
- **位置敏感性**：把关键事件安排在视频开头、中间和结尾，检测 lost-in-the-middle。
- **多细节理解**：使用 action order、action count 和 summarization 等任务区分检索失败与聚合失败。[3]
- **旧能力保持**：在完全相同的输入、提示和解码设置下，对比 SFT 前后短 caption、通用视觉问答与格式遵循能力。
- **输出效率**：同时报告总信息覆盖率和单位 token 的正确命题数，防止把单纯变长误判为质量提升。
- **长度外推**：分别改变训练 caption 长度、推理帧数和输出上限，确定退化来自输入长度还是输出分布。

如果长 SFT 模型只在增加推理帧数时退化，应优先归因于上下文利用问题；如果它在固定输入上仍比 SFT 前模型的短 caption 和通用任务更差，才构成较强的参数级负迁移证据。

## 缓解方向

现有证据支持以下方向，但尚不能确定哪一种具有普遍最优性：

- 混合短、中、长 caption，并显式加入长度控制指令，避免形成单一的冗长输出先验；
- 按样本或任务平衡训练损失，防止长 caption 因 token 数更多而主导更新；
- 联合 frame-level 与 clip-level 监督，同时覆盖局部事实和全局时序结构；[1][11]
- 对 caption 做命题级 grounding 与过滤，而不是只按整体相似度筛选；[13]
- 使用分段编码、层次化事件摘要或专用 character/event 模块，减少 captioning LLM 的上下文负担；[12]
- 通过 replay、正则化、adapter 隔离或 mixture-of-experts 路由保持旧任务与 instruction-following 能力；[6][8][10]
- 将“增加 nominal context window”与“提升有效证据利用率”作为两个独立优化目标。

## 证据局限

当前材料尚不足以证明“long-context SFT 必然造成 captioning 负迁移”。

首先，[1] 与 [11] 很可能是同一项 LongCaptioning 工作的不同标题或版本，应在正式入库前核对 arXiv 标识与版本。其消融主要证明视觉窗口扩展和 LongCaption-10K 对长 caption 有益，没有直接报告长 SFT 前后短 caption、通用视觉能力或 instruction following 的下降。

其次，[2]、[4]、[6]、[7]、[9] 和 [10] 包含网页综述、聚合页面或 paper note。它们可以形成机制假设，但不能替代原论文中的实验设置与数值。

最后，当前来源没有提供一个同时控制训练 token 数、caption 长度、帧数、位置编码扩展和伪标注质量的完整实验。因此，监督分布偏移、上下文退化和 catastrophic forgetting 各自贡献多大仍是开放问题。

## 值得补充的来源

后续应优先寻找：

- lost-in-the-middle、position bias 与 distractor interference 的原始论文；
- RoPE scaling、Position Interpolation 等 context extension 方法的长度外推实验；
- SMoLoRA 原论文及其他 continual [[visual-instruction-tuning]] 工作；
- LongCaptioning 的完整论文版本、附录、训练损失归一化方式和短任务保持性结果；
- 使用 proposition-level factuality、DNLI 或人工 grounding 评估长 caption 的研究；
- 同时报告短 caption、长 caption、视频问答和指令遵循性能的多任务受控实验；
- 比较 full fine-tuning、LoRA、adapter isolation 与 replay 对 captioning 负迁移影响的研究。

## 综合判断

现阶段最稳妥的解释是：long-context SFT 通过长标注强化了详细输出能力，但也改变了模型的回答策略；当这种策略变化与有效上下文不足、多细节干扰和长 caption 的 grounding 噪声叠加时，就会产生“更长但不一定更准”、中段事件遗漏、短任务退化以及 instruction-following 漂移。只有在固定输入和评测条件下证明 SFT 后旧能力下降，才能进一步把其中一部分明确归类为 catastrophic forgetting。

## References

1. [LongCaptioning: Unlocking the Power of Long Video Caption Generation in Large Multimodal Models](https://arxiv.org/html/2502.15393v2) — arxiv.org
2. [Long-Session Context Degradation: How Multi-Turn ...](https://tianpan.co/blog/2026/04/19/long-session-context-degradation-multi-turn) — tianpan.co
3. [MLVU: Benchmarking Multi-task Long Video Understanding](https://openaccess.thecvf.com/content/CVPR2025/papers/Zhou_MLVU_Benchmarking_Multi-task_Long_Video_Understanding_CVPR_2025_paper.pdf) — openaccess.thecvf.com
4. [Context Degradation in LLMs](https://www.emergentmind.com/topics/context-degradation-in-large-language-models) — emergentmind.com
6. [Catastrophic Forgetting in LLM Fine-tuning](https://www.emergentmind.com/papers/2308.08747) — emergentmind.com
7. [An Empirical Study of Catastrophic Forgetting in Large Language Models During Continual Fine-tuning | alphaXiv](https://www.alphaxiv.org/abs/2308.08747) — alphaxiv.org
8. [Interpretable Catastrophic Forgetting of Large Language Model Fine-tuning via Instruction Vector](https://arxiv.org/html/2406.12227v1) — arxiv.org
9. [Catastrophic Forgetting in LLMs](https://www.emergentmind.com/topics/catastrophic-forgetting-in-llms) — emergentmind.com
10. [[Paper Note] SMoLoRA: Exploring and Defying Dual Catastrophic Forgetting in Continual Visual Instruction Tuning](https://en.papernotes.org/ICCV2025/multimodal_vlm/smolora_exploring_and_defying_dual_catastrophic_forgetting_in_continual_visual_i) — en.papernotes.org
11. [LongCaptioning: Unlocking the Power of Long Caption Generation in Large Multimodal Models](https://arxiv.org/html/2502.15393v1) — arxiv.org
12. [VIVECaption: A Split Approach to Caption Quality Improvement](https://arxiv.org/html/2603.07401v1) — arxiv.org
13. [Bridging the Visual Gap: Fine-Tuning Multimodal Models with Knowledge-Adapted Captions](https://arxiv.org/html/2411.09018v3) — arxiv.org
14. [Distilling Vision-Language Models on Millions of Videos Yue Zhao1,2∗ Long Zhao1](https://zhaoyue-zephyrus.github.io/video-instruction-tuning/static/contents/viit_paper.pdf) — zhaoyue-zephyrus.github.io
