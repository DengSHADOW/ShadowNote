---
type: query
title: "Research: 追踪后续 LLaVA 对视觉局限的改进"
created: 2026-09-16
origin: deep-research
tags: [research]
---

# Research: 追踪后续 LLaVA 对视觉局限的改进

我会按项目的 Wiki 维护流程处理：先核对现有索引、来源页和写作规范，再判断应新增 synthesis 页面还是补充现有 LLaVA 页面，并保留所有已有人工编辑。当前工作目录是数据子目录，而 `AGENTS.md` 中部分路径相对于上一级项目根目录书写；我正在定位实际目录结构后继续，不会据此猜测文件位置。现有页面已经把原始 LLaVA 的关键失败明确为“局部元素可识别，但关系组合错误”。本次综合会把后续工作按四条路线区分：分辨率与视觉 token、训练数据、语言模型规模与多模态扩展、专门的幻觉抑制；同时单列哪些改进只是总体 benchmark 提升，尚未直接证明解决了关系/组合语义失败。当前工作区为只读，无法写入 `wiki/synthesis/` 或更新索引。以下为可直接保存的 Wiki 页面正文。

# 追踪后续 LLaVA 对视觉局限的改进

## 结论摘要

后续 LLaVA 系列主要沿四条路线改进原始 [[LLaVA]] 的视觉局限：

1. LLaVA-1.5 与 LLaVA-NeXT 提高输入分辨率，并通过 AnyRes 保留局部细节，以改善 OCR、细粒度感知和由低分辨率引起的幻觉。[1][5][6]
2. LLaVA-NeXT 扩展视觉 token、训练数据和语言模型规模，增强结构化文本理解、world knowledge 与逻辑推理。[8][9]
3. LLaVA-NeXT-Interleave 将单图、多图、视频和 3D 数据统一为 interleaved format，扩大视觉输入与跨任务迁移范围。[7]
4. HALVA 与 retrieve-then-compare decoding（RCD）不再只依赖通用扩展，而是分别从训练目标和解码过程直接抑制视觉幻觉。[3][4]

这些工作对细节辨认、OCR、输入分辨率和对象幻觉给出了较明确的改进证据，但尚未充分证明原始 [[bag-of-patches-组合语义失败|“bag of patches”组合语义失败]]已经解决。LLaVA-1.5 的 relationship hallucination 仍比 object hallucination 严重，而高分辨率、更多视觉 token 或更强语言模型带来的总体 benchmark 提升，不能自动等同于关系理解和组合推理能力的提高。[2][3]

## 原始问题：从对象识别到关系理解的断层

[[2304.08485v2|Visual Instruction Tuning]]中的原始 [[LLaVA]] 能够识别图像中的草莓和酸奶，却错误推断存在“草莓味酸奶”。这一案例表明，模型可能把图像处理为彼此松散的局部特征集合，而没有正确表示属性、归属和对象间关系，即 [[bag-of-patches-组合语义失败]]。

这一问题不同于单纯“没有看清对象”。它至少包含三个可能的瓶颈：

- **视觉信息缺失：** 分辨率或视觉 token 不足，使文字、小物体和局部属性不可辨认。
- **视觉—语言对齐错误：** 图像中存在正确证据，但 [[多模态-feature-alignment|多模态 feature alignment]] 或语言解码过程错误地支持了其他候选。
- **关系与组合推理失败：** 对象分别被识别，但属性、空间关系或复合概念被错误组合。

后续工作对第一类问题的改进最明确；对第二类问题已有专门的 hallucination mitigation 方法；对第三类问题的直接证据仍然有限。

## 演进路线

| 阶段或方法 | 主要改动 | 主要针对的局限 | 当前证据边界 |
|---|---|---|---|
| LLaVA-1.5 | 336×336 输入、更多任务类型和训练数据 [1] | OCR、细粒度内容、区域感知 | 来源 [1] 为二手介绍；“新增 158K”与原始 [[LLaVA-Instruct-158K]] 的关系不清楚 |
| LLaVA-NeXT | AnyRes、最高约四倍像素、动态网格 [5][6] | 小目标、文字、复杂场景细节、低分辨率幻觉 | 官方页面声称改善 reasoning、OCR 和 hallucination，但给定材料缺少对应消融数值 |
| LLaVA-NeXT scaling | 扩展分辨率、视觉 token、文档/OCR 数据和 LLM [8] | 结构化文本、多语言和视觉细节 | 说明哪些扩展通常有效，但不能证明关系推理问题已经解决 |
| LLaVA-NeXT stronger LLMs | 引入 LLaMA3、Qwen-1.5 72B/110B [9] | world knowledge、逻辑推理、开放场景问答 | 语言能力提高不必然意味着答案更受图像约束 |
| LLaVA-NeXT-Interleave | 统一单图、多图、视频与 3D；M4-Instruct 含 1177.6K 样本 [7] | 多输入、时间信息、跨视角与 3D 场景 | 证明能力范围扩大，尚不能直接推出单图关系理解更可靠 |
| HALVA | 生成错误对象或属性作为负例，进行 contrastive tuning [4] | 对象存在、数量、位置和颜色幻觉 | MME-Hall 有直接增益，但主要覆盖 object-related hallucination |
| RCD | 在解码阶段比较视觉证据，抑制错误候选 [3] | 对象、属性及空间关系幻觉 | 跨多个 benchmark 有效，但不能消除视觉分支本身对错误候选的支持 |
| CREME | 定位并编辑与隐式组合推理相关的 MHSA 参数 [11] | LLM compositional reasoning | 研究对象是文本 LLM；尚无证据表明可直接迁移到 LLaVA 的视觉关系错误 |

## 分辨率与视觉表征

### 从固定分辨率到 AnyRes

LLaVA-1.5 将输入分辨率扩展至 336×336，以保留文字和场景细节。[1] LLaVA-NeXT 进一步采用 AnyRes：根据图像宽高比选择 $2\times2$、$1\times\{2,3,4\}$ 或 $\{2,3,4\}\times1$ 等网格，使模型能处理不同形状的高分辨率图像。[5] 项目仓库将这一变化概括为最多处理约四倍像素。[6]

高分辨率主要缓解“证据在缩放过程中消失”的问题。若模型原先因无法读取文字、颜色或小物体而依赖语言先验，保留更多像素确实可能减少猜测式回答。[5] 但若错误源于已经可见的对象被错误组合，例如把“草莓”和“酸奶”合成为“草莓味酸奶”，增加分辨率未必足够。

### 分辨率与视觉 token 的相对作用

LLaVA-NeXT 的 scaling 分析认为，原始像素分辨率和特征空间中的视觉 token 数量都能提高需要视觉细节的任务表现，但在成本相近时，扩展分辨率通常比单纯增加 token 更有效；作者因此推荐结合 pooling 的 AnyRes。[8]

这一区分很重要：更多像素提高输入证据的可见性，更多 token 提高保留和传递这些证据的容量。二者改善的是视觉带宽，并不直接保证模型能够正确绑定对象、属性与关系。

## 数据与训练任务的扩展

来源 [1] 将 LLaVA-1.5 的进步归因于更广泛的数据，以及 OCR、VQA 和 region-level perception 等任务。不过，其“额外加入 158K multimodal instruction-following examples”的说法存在来源歧义：原始 [[visual-instruction-tuning]] 工作已经发布 [[LLaVA-Instruct-158K]]。在缺少 LLaVA-1.5 technical report 原文的情况下，不能确定这里指新增样本、复用原始数据，还是二手文章对两个版本的混淆。

LLaVA-NeXT 的后续分析提供了更具体的数据方向：

- UReader 100K 与 SynDOG EN/CN 1M 对文档和结构化文本理解有显著帮助。[8]
- ShareGPT4V Chinese Caption data 改善中文图像理解，并反映在 Image-DC 与 CMMU 等指标上。[8]
- M4-Instruct 汇集 1177.6K 个单图、多图、视频和 3D 样本，用统一的 interleaved format 训练 LLaVA-NeXT-Interleave。[7]

这些结果支持“针对性数据能补足特定视觉任务”的判断，但没有直接回答模型是否学会了可靠的关系绑定。OCR 数据可以改善文字读取，多图数据可以改善跨图比较；要证明组合语义进步，还需要专门控制对象共现、属性交换和空间关系的评测。

## 更强语言模型的贡献与边界

LLaVA-NeXT 将相同的基本训练方案应用于 LLaMA3 8B、Qwen-1.5 72B 和 Qwen-1.5 110B。官方结果将改进归因于更强 LLM 所继承的 world knowledge 和 logical reasoning。[9] 相关 scaling 分析也认为，扩展 LLM 比单纯扩展 vision encoder 参数规模更有效，而 vision encoder 的收益更依赖分辨率和 token 配置。[8]

这一结论说明多模态表现并非完全由视觉编码器决定。不过，更强的语言先验具有双重解释：

- 当图像证据充分时，更强 LLM 可能更好地组织推理与表达。
- 当图像证据不充分或对齐错误时，更强 LLM 也可能生成更流畅、但未必更 grounded 的答案。

给定来源没有提供足以分离这两种情况的因果实验。因此，“更强 LLM 提高总体多模态分数”不能直接改写为“更强 LLM 解决视觉幻觉”。

## 从能力扩展到直接幻觉抑制

### LLaVA-1.5 仍存在关系幻觉

二手来源 [2] 报告，LLaVA-1.5 的 object hallucination F1 为 82.12，而 relationship hallucination F1 为 77.28。虽然缺少原论文实验设置，不能据此作精确的跨模型比较，但结果方向表明：对象是否存在通常比对象之间的关系更容易判断。

这与 [[bag-of-patches-组合语义失败]]一致。即使对象识别有所改善，关系、属性和空间结构仍可能成为独立瓶颈。

### HALVA：通过对比负例改变训练信号

HALVA 以 LLaVA-v1.5 为基础，根据正确视觉问答样本生成 hallucinated response，并选择性改变真实对象及其属性，再通过 contrastive tuning 拉开正确回答与错误回答的表示或生成偏好。[4]

在 MME-Hall 的 existence、count、position 和 color 四项测试中，HALVA-13B 得到 675/800，比基础 LLaVA-v1.5 高 31.7 分。[4] 这说明专门构造幻觉负例比单纯扩大模型更直接地改善 object-related grounding。

其证据边界也很明确：MME-Hall 主要测量对象存在、数量、位置和颜色，并不能覆盖所有高阶关系、因果理解或复合概念错误。

### RCD：在解码时重新利用视觉证据

RCD 的分析发现，LLaVA-1.5 在产生错误颜色词时并非完全没有获得正确视觉线索。视觉分支会为正确候选 “gray” 增加 $+5.008$ 的置信度，却同时为错误候选 “green” 和 “brown” 分别增加 $+3.898$ 与 $+4.250$。语义或外观相似的图像还可能诱发相似幻觉。[3]

这一结果表明，部分幻觉不是“视觉信息不存在”，而是视觉分支对多个候选提供了混杂支持，之后的解码没有可靠选择正确候选。RCD 在 MME、POPE、WHOOPS 和 [[LLaVA-Bench]] (In-the-Wild) 上改善 LLaVA-NeXT、LLaVA-1.5 与 InstructBLIP，并优于相关 hallucination-mitigation decoding 方法。[3]

因此，RCD 与 AnyRes 处理的是不同层级：

- AnyRes 尽量保留原始视觉证据。
- RCD 处理已有视觉证据在生成过程中被错误利用的问题。

二者可能互补，但给定资料没有提供联合消融，不能判断收益是否可叠加。

## 多图、视频和 3D 扩展

LLaVA-NeXT-Interleave 将单图、多图、视频和 3D 数据统一为交错的视觉—语言序列，并报告在多图 benchmark 上达到领先结果，同时维持单图能力并改善视频任务。[7] 联合训练还产生一定 cross-task transfer，使一个场景中的能力迁移到其他视觉输入形式。

这一进展扩大了“视觉理解”的范围：模型不再只处理单张静态图像，而能够比较多张图、利用时间信息或接触 3D 表示。然而，能力范围扩大与单项可靠性提高是两个不同命题。来源 [7] 没有证明 interleaved training 已解决细粒度关系幻觉，也没有给出不同模态混合对单图组合语义错误的专门消融。

## 组合推理研究的间接启示

CREME 研究发现，文本 LLM 的 compositional reasoning failures 往往与隐式推理结果没有被正确生成或利用有关；相关信息会在中间层出现，并由部分 MHSA 模块因果性地影响最终答案。该方法通过定位和编辑这些参数来修复失败。[11]

这一发现为 LLaVA 的关系错误提供了一个可检验假设：视觉 token 中可能已经包含必要对象信息，但中间层没有正确生成或利用对象间的隐式关系。然而，CREME 研究的是文本 LLM，而不是视觉—语言模型；给定来源也没有把它应用于 LLaVA。因此它只能作为后续机制研究的候选方法，不能视为已经实现的 LLaVA 改进。[11–14]

## 评测体系的变化

原始 [[LLaVA-Bench]] (In-the-Wild) 只有 24 张图像和 60 个问题，并依赖 [[GPT-4-as-judge-多模态评估]]。LLaVA-NeXT 后续提出 LLaVA-Bench (Wilder)，包括用于快速评估的 120 个样本版本和用于综合评估的 1020 个样本版本，覆盖数学问题、图像理解和代码等场景。[9]

扩大样本量有助于降低原始小规模 benchmark 的偶然性，但仍需区分：

- 总体视觉对话质量；
- 对象与属性识别；
- OCR 与细粒度感知；
- relationship hallucination；
- 组合语义和反事实关系；
- 回答是否真正依赖图像，而非语言先验。

如果只报告总体分数，某一领域的显著进步可能掩盖关系推理上的持续失败。

## 综合判断

| 原始局限 | 后续变化 | 判断 |
|---|---|---|
| 低分辨率导致文字和小物体不可见 | 336×336、AnyRes、约四倍像素 [1][5][6] | 有实质改进，但需要精确 benchmark 与消融量化 |
| OCR 与结构化文档理解不足 | UReader、SynDOG 及更高分辨率 [8] | 有针对性的正面证据 |
| 对象幻觉 | HALVA 和 RCD [3][4] | 已出现直接、可量化的缓解方法，但尚未消除 |
| 属性和颜色幻觉 | 高分辨率、HALVA、RCD [3–5] | 有所改善；视觉分支仍可能支持错误候选 |
| 对象关系与组合语义错误 | relationship hallucination 仍低于 object hallucination [2] | 尚无充分证据证明解决 |
| world knowledge 与逻辑推理不足 | 更强 LLM [9] | 总体能力提高，但视觉 grounding 的独立贡献不清楚 |
| 仅支持单图 | LLaVA-NeXT-Interleave [7] | 能力范围明显扩展至多图、视频和 3D |
| 小规模、单一总体评测 | LLaVA-Bench (Wilder)、MME、POPE、WHOOPS [3][9] | 评测覆盖扩大，但仍缺少统一的关系与组合推理诊断 |

总体而言，后续 LLaVA 工作已经显著改善“看不清”和“视觉任务覆盖不足”，并开始直接处理“看到了却说错”的幻觉问题；但“识别出局部对象后能否稳定地组合其关系”仍是没有被充分关闭的能力缺口。

## 证据中的矛盾与缺口

### 158K 数据的版本归属不清

来源 [1] 把 158K multimodal instruction examples 描述为 LLaVA-1.5 的新增数据，但原始工作已经包含 [[LLaVA-Instruct-158K]]。在查阅 LLaVA-1.5 technical report 与训练配置前，不应把该数字计为相对于原始模型的净新增量。

### 官方性能主张缺少给定摘录中的完整数值

LLaVA-NeXT 官方页面声称改善 reasoning、OCR、world knowledge 与 hallucination，并称 LLaVA-NeXT-34B 在部分 benchmark 上超过 Gemini Pro。[5][6] 现有材料没有列出这些 benchmark 的完整表格、置信区间或对照配置，因而只能支持方向性结论。

### 总体性能与视觉 grounding 混合

更强 LLM、更多数据和更大输入同时变化，使总体提升难以归因于单一因素。[8][9] 尤其需要控制语言模型仅凭题目和常识作答的情况；原始 [[ScienceQA]] 结果已经表明，部分视觉问题可以不依赖图像得到正确答案。

### 对象幻觉与关系幻觉覆盖不均

HALVA 的 MME-Hall 结果重点覆盖 existence、count、position 和 color。[4] 这些任务比任意对象关系、角色绑定、事件结构或复合概念更容易形式化。来源 [2] 所示的 object/relationship F1 差距提示，关系层面的可靠性仍需独立评估。

### 来源质量不均

来源 [5–9] 多为项目博客或 GitHub 发布说明，适合确认发布内容与作者主张，但不能替代论文中的方法、消融和误差分析。来源 [1][2][10][12] 是二手介绍、索引或讲解材料。CREME 的论文来源较完整，但其研究对象不是多模态模型。[11–14]

## 建议补充的资料

1. LLaVA-1.5 technical report 原文及训练数据清单，以解决 158K 数据归属和版本差异。
2. LLaVA-NeXT、LLaVA-NeXT-Interleave 的完整论文、附录和 benchmark 表格。
3. relationship hallucination 研究原文，以确认来源 [2] 中 F1 的数据集、阈值和评分方法。
4. HALVA 与 RCD 的完整论文，包括不同模型规模、任务类别和解码成本的消融。
5. AnyRes 的固定分辨率对照实验，用于分离像素数、视觉 token 数、图像切片和计算成本。
6. 同一基础 LLM 下的 vision encoder、resolution、token count 与训练数据因果消融。
7. Winoground、ARO、SugarCrepe 或同类组合性 benchmark 上的 LLaVA-1.5、LLaVA-NeXT、HALVA 与 RCD 对比。
8. 对“草莓与酸奶”等受控属性绑定案例进行 counterfactual evaluation：保持对象不变，只交换颜色、位置、所属关系或复合属性。
9. 独立人工评测及其与 [[GPT-4-as-judge-多模态评估]] 的一致性分析。
10. 针对“视觉证据已编码但未被正确利用”的中间层 causal tracing，以验证 CREME 所揭示的文本机制是否存在于视觉—语言模型中。

## 参考来源

[1] *Medium*：LLaVA 与 LLaVA-1.5 介绍。  
[2] *Evaluating and Analyzing Relationship Hallucinations in ...*  
[3] *Retrieve-then-compare mitigates visual hallucination in multi-modal large language models*  
[4] *HALVA: Hallucination Attenuated Language and Vision Assistant*  
[5] *LLaVA-NeXT: Improved reasoning, OCR, and world knowledge*  
[6] *LLaVA-VL/LLaVA-NeXT* GitHub repository  
[7] *LLaVA-NeXT: Tackling Multi-image, Video, and 3D in Large Multimodal Models*  
[8] *LLaVA-NeXT: What Else Influences Visual Instruction Tuning Beyond Data?*  
[9] *LLaVA-NeXT: Stronger LLMs Supercharge Multimodal Capabilities*  
[10] *LLaVA paper - Comprehensive dissection*  
[11] *Understanding and Patching Compositional Reasoning in LLMs*  
[12] *Understanding and Patching Compositional Reasoning in ...*，Liner 条目  
[13] *Understanding and Patching Compositional Reasoning in ...*，ACL Anthology 条目  
[14] *Understanding and Patching Compositional Reasoning in ...*，arXiv 条目

## References

1. [Medium](https://medium.com/@EleventhHourEnthusiast/llava-and-llava-1-5-1cf8be377245) — medium.com
2. [Evaluating and Analyzing Relationship Hallucinations in ...](https://liner.com/review/evaluating-and-analyzing-relationship-hallucinations-in-large-visionlanguage-models) — liner.com
3. [Retrieve-then-compare mitigates visual hallucination in multi-modal large language models](https://www.oaepublish.com/articles/ir.2025.13) — oaepublish.com
4. [HALVA: Hallucination Attenuated Language and Vision Assistant](https://research.google/blog/halva-hallucination-attenuated-language-and-vision-assistant) — research.google
5. [LLaVA-NeXT: Improved reasoning, OCR, and world knowledge | LLaVA](https://llava-vl.github.io/blog/2024-01-30-llava-next) — llava-vl.github.io
6. [GitHub - LLaVA-VL/LLaVA-NeXT · GitHub](https://github.com/LLaVA-VL/LLaVA-NeXT) — github.com
7. [LLaVA-NeXT: Tackling Multi-image, Video, and 3D in Large Multimodal Models](https://llava-vl.github.io/blog/2024-06-16-llava-next-interleave) — llava-vl.github.io
8. [LLaVA-NeXT: What Else Influences Visual Instruction Tuning Beyond Data?](https://llava-vl.github.io/blog/2024-05-25-llava-next-ablations) — llava-vl.github.io
9. [LLaVA-NeXT: Stronger LLMs Supercharge Multimodal ...](https://llava-vl.github.io/blog/2024-05-10-llava-next-stronger-llms) — llava-vl.github.io
10. [LLaVA paper - Comprehensive dissection](https://www.youtube.com/watch?v=xVfBOUfntss) — youtube.com
11. [Understanding and Patching Compositional Reasoning in LLMs](https://arxiv.org/html/2402.14328v2) — arxiv.org
12. [Understanding and Patching Compositional Reasoning in ...](https://liner.com/review/understanding-and-patching-compositional-reasoning-in-llms) — liner.com
13. [Understanding and Patching Compositional Reasoning in ...](https://aclanthology.org/2024.findings-acl.576) — aclanthology.org
14. [Understanding and Patching Compositional Reasoning in ...](https://arxiv.org/abs/2402.14328) — arxiv.org
