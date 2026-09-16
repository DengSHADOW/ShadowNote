---
type: source
title: Evolving Programmatic Skill Networks
description: PSN 将可执行程序技能组织为可持续修复和重构的调用网络，并在 Minecraft 与 Crafter 中研究持续技能学习。
status: draft
authors:
  - Haochen Shi
  - Xingdi Yuan
  - Bang Liu
year: 2026
doi: 10.48550/arXiv.2601.03509
arxiv: 2601.03509v2
source_id: p-3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
content_version: sha256:3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
zotero_item: 5RKUKLBV
zotero_attachment: GE9BCRAF
sources:
  - zotero://users/0/items/5RKUKLBV
---

# Evolving Programmatic Skill Networks

## 图谱连接

- [[programmatic-skill-network|程序化技能网络（PSN）]]
- [[trace-guided-skill-repair|执行轨迹引导的技能修复]]
- [[reliability-aware-skill-updating|可靠性门控的技能更新]]
- [[validated-structural-refactoring|可验证的结构重构]]

> 阅读状态：draft。2026-09-15 已按同一 SHA-256 版本重新核查全部 47 个 PDF 页面，并重新查看 Figure 1–17 与 Table 1–16 的实际页面；未运行作者代码或独立复现实验。原文为 *Preprint. Under review.*，版本为 arXiv:2601.03509v2。

## 复核结论

原有页面对 PSN 主流程的概括基本正确，但对证据强度偏乐观。此次修正了回滚率分母，补明跨模型图的非对称统计口径，并把“完成科技树”“架构而非模型带来收益”“组合泛化”“成本摊销”等强结论降到实验实际支持的范围。

**英文对应表述（非逐字原文）**：The previous page captured the PSN pipeline reasonably well, but it overstated several conclusions. This revision corrects the rollback denominator and narrows claims about full tech-tree completion, architecture-only causality, compositional generalization, and cost amortization.（PDF pp. 5, 8–13, 41–47）

## 一句话理解

论文提出 Programmatic Skill Network（PSN）：把智能体技能表示为带参数、前置/后置条件和子技能调用关系的可执行程序；失败时沿真实执行轨迹定位并修补相关程序，成功后尝试受检查、可回滚的结构重构。这里的 **skill 是 Minecraft/Crafter 智能体执行的 JavaScript 或 Python 程序**，不是 Codex 的 `SKILL.md` 指令文件。

**英文对应表述（非逐字原文）**：PSN represents skills as executable JavaScript or Python programs connected by invocation links. It performs trace-localized repair after failure and structural refactoring after success.（PDF pp. 1–5，Sections 1–2）

## 研究问题与贡献边界

作者针对扁平技能库和静态技能图的三个缺口展开：组合执行时如何分配失败责任、如何保护已经可靠的技能免受反复改写，以及如何在持续经验中压缩重复程序结构。PSN 的核心贡献是把规划、执行轨迹、局部代码修复和网络重构组织成一个在线循环，而不是提出新的基础模型训练算法。

**英文对应表述（非逐字原文）**：The paper targets credit assignment over hierarchical skill compositions, stabilization of reliable skills, and structural reorganization of an expanding executable skill library. Its contribution is architectural orchestration around prompted LLM operators.（PDF pp. 1–3，Introduction；Figure 1）

论文把这种循环类比为神经网络训练：轨迹故障定位类似 backpropagation，成熟度门控类似 learning-rate scheduling 或 freezing，结构重构类似 architecture search。该类比是解释框架，不是数学等价；系统使用离散程序编辑、二元任务反馈和 LLM 生成的修改建议，没有可微损失或收敛保证。

**英文原文**：“The neural network analogy is partial.”（PDF p. 6，Section 3, Scope of the analogy）

## 方法

### 技能表示、规划与执行

技能写成 $s=(C_s,P_s,E_s,\mathrm{CHILDREN}(s))$：$C_s$ 是控制流，$P_s$ 是参数，$E_s$ 是前置/后置条件，`CHILDREN` 是调用的子技能。网络 $N_t=(S_t,L_t)$ 的节点是技能，边是调用关系；前置/后置条件还会根据成功、失败状态和经验转移逐步校准。

**英文对应表述（非逐字原文）**：A skill contains control flow, parameters, preconditions and effects, and invoked subskills; the directed network records skills and invocation edges, while predicates are calibrated from observed transitions.（PDF pp. 2–4，Sections 2.1 and 2.3）

规划器先从目标谓词做 backward chaining，用技能后置条件递归满足子目标；多个候选依据经验可靠性 $V(s)$ 并通过 Boltzmann exploration 选择。现有网络无法缩减某个子目标时才调用 LLM forward planner；随后 `CODEGEN` 仍会根据计划、网络和历史合成一个候选技能，因此“复用规划”不等于完全不调用代码生成。

**英文对应表述（非逐字原文）**：The planner first searches backward through skill effects, uses reliability-weighted Boltzmann selection among candidates, and invokes LLM forward planning when no existing skill reduces a subgoal. A candidate skill is then synthesized from the plan and context.（PDF p. 3，Eq. 2–4）

### 失败后的两阶段修复

执行轨迹 $T_t$ 为每个实际调用记录技能、执行前后符号状态和状态码。按 Section 2.4，行为修复由任务失败（$\delta_t=0$）触发，只沿本次执行轨迹处理；未执行技能不更新。这里应注意论文 Section 3 又把快速修复描述为发生在“every execution”，与方法部分的失败触发条件不完全一致。

**英文原文**：“When execution fails (i.e., $\delta_t = 0$), the skill optimizer performs localized behavioral repair.”（PDF p. 4，Section 2.4）

REFLECT 分两阶段工作：先从失败根技能向下传播反馈并为相关节点产生结构化修改提议，此时不改代码；再按依赖后序从叶到根应用 patch，把子技能的优化报告传给父技能，降低调用契约错配。作者称修改提议为 symbolic gradient，但它不是数值梯度。

**英文对应表述（非逐字原文）**：Phase I propagates feedback top-down without changing code; Phase II applies program edits bottom-up and passes child optimization reports to parents. The “gradient” is a structured edit proposal rather than a numeric derivative.（PDF pp. 19–21，Appendix A；Algorithm 1）

### 成熟度门控

每个技能的 $V(s)=\hat p_s-u_s$ 综合带 Laplace smoothing 的成功率与随执行次数下降的不确定性。更新概率为：

$$
P(\mathrm{update}\ s)=(1-\epsilon)\,\sigma(\gamma(0.6-V(s)))+\epsilon,
$$

其中 $\gamma=5.0$、$\epsilon=0.1$。高 $V(s)$ 会降低而非禁止更新；最近 5 个修复提议组成 rolling buffer。论文说缓冲区能防止矛盾编辑，但没有给出独立消融来隔离这个部件。

**英文对应表述（非逐字原文）**：Update probability decreases sigmoidally around a maturity pivot of 0.6 but retains an epsilon floor. A five-proposal rolling buffer constrains edits; its separate causal effect is not evaluated.（PDF p. 4，Eq. 6）

### 成功后的结构重构

一次技能成功执行后，系统只搜索该技能的父/子节点及 embedding 最相近的 5 个技能，检测五类关系：参数覆盖、行为/子图覆盖、兄弟特化、公共子技能抽取和完全重复。对应 rewrite 包括 wrapper、调用替换、抽象技能合成、公共子程序抽取和 canonical merge。

**英文对应表述（非逐字原文）**：After a successful execution, refactoring searches parents, children, and the five nearest semantic neighbors, then applies one of five canonical graph-rewrite patterns.（PDF pp. 4–5、20–24；Table 2；Figures 10–14）

结构提议先经语法、类型安全和语义保持分析；通过后才应用，并在涉及受影响技能的最近 3 个任务上重测，成功率下降超过 20% 时回滚。论文称 rewrite 是 deterministic 且 semantics-preserving，但“语义保持分析 + 三任务窗口”仍是经验检查，不是形式化验证。

**英文对应表述（非逐字原文）**：Proposals face pre-application syntax, type, and semantic checks, followed by a three-task performance window and rollback for a drop exceeding 20%. The paper acknowledges that formal symbolic projection guarantees are absent.（PDF pp. 5, 19, 42–43；Tables 12–13）

## 实验设置

实验环境为 Minecraft 1.19.4（MineDojo + Mineflayer JavaScript API）和带 Mineflayer 风格 Python API 的 Crafter。主模型为 `gpt-5-mini-2025-08-07`；Minecraft 跨模型实验另用 Qwen3-Coder-Next（3B active / 80B total）。基线包括 ReAct、Reflexion、AutoGPT、Voyager 与 ADAM；ODYSSEY 主要在附录做架构和 SR@k 比较。

**英文对应表述（非逐字原文）**：The evaluation uses Minecraft 1.19.4 and Crafter, with GPT-5-mini as the main backend and Qwen3-Coder-Next for cross-model Minecraft runs. Baselines span prompting agents, flat skill libraries, and a causal planner over fixed skills.（PDF pp. 6–7、14，Section 4.1）

可复现性信息包括模型标识、主要超参数、任务序列、示例提示和若干代码 diff，但正文/附录没有完整报告 Crafter、Figure 4–6 等图的运行次数和统计检验；代码仓库也未在本次复核中运行。因此“提供材料”不能替代独立复现。

**英文对应表述（非逐字原文）**：The paper lists models, hyperparameters, task sequences, prompts, and representative diffs, but several plotted studies lack clearly stated run counts or inferential statistics. This audit did not execute the released code.（PDF pp. 8–14，Figures 3–6；Reproducibility Statement）

## 主要结果与可信范围

### Minecraft 科技树

使用 GPT-5-mini 时，PSN 在 6/6 次运行中到达 diamond tool，平均 $35\pm16$ 次迭代；同代码、同模型的 Voyager* 为 2/6，成功运行的迭代统计是 $99\pm36$。去掉 optimizer 的 PSN 在 wood、stone、iron 阶段接近 Voyager，但 0/3 到达 diamond，支持“完整优化循环对后期任务有用”，却没有分别隔离 REFLECT、门控和重构的贡献。

**英文对应表述（非逐字原文）**：PSN reaches Diamond Tool in all six GPT-5-mini runs at 35±16 iterations, while the matched Voyager reproduction succeeds in two of six at 99±36. The no-optimizer ablation fails at Diamond in all three runs but removes multiple mechanisms together.（PDF p. 5，Table 1）

使用 Qwen3-Coder-Next 时，PSN 仍在 6/6 次运行中到达 diamond，平均 $49\pm18$ 次；Voyager† 为 1/6，ADAM† 不能稳定超过 stone。这个结果支持架构在两个模型上均能工作，但不能单凭“同一架构”推出收益只来自架构，因为模型能力、生成代码、失败轨迹和知识补丁仍共同变化。

**英文对应表述（非逐字原文）**：Under Qwen3-Coder-Next, PSN reaches Diamond in six of six runs at 49±18, Voyager in one of six, and ADAM does not reliably pass Stone. The matched architecture is evidence of robustness, not a complete causal decomposition of model versus scaffold.（PDF pp. 5, 7–8, 12；Table 1）

论文多处说两个模型都“complete the tech tree”，但 Table 1 显示 obsidian 仅 GPT-5-mini PSN 1/6、Qwen3 PSN 0/6；因此可靠结论只能写成“到达 diamond tool”，不能写成完整科技树或稳定获得 obsidian。

**英文原文**：“The architecture absorbs the noise.”（PDF p. 12，Section 4.6）——但同页的 “both models complete the tech tree” 与 Table 1 的 Obsidian 列并不一致。

### 持续学习、复用与重构

Crafter 的 Figure 3 中，PSN 累计 reward 曲线高于 Voyager、AutoGPT、Reflexion 与 ReAct，短曲线表示提前死亡。不过图和正文未明确给出样本数或显著性检验；曲线长度又同时反映存活时长，所以它支持该设置下的相对趋势，不足以证明“跨开放任务分布的强泛化”。

**英文对应表述（非逐字原文）**：Figure 3 shows higher cumulative reward for PSN, while shorter traces denote earlier death. The figure does not state the number of runs or a significance test, and survival duration is entangled with accumulated reward.（PDF p. 8，Figure 3）

Figure 4 的固定科技树 curriculum 周期性重测显示 PSN 的保持率普遍高于 Voyager，但 PSN 在后两个里程碑也下降到 67% 和 50%。因此它是“相对减少遗忘”，而不是保持所有旧技能或在任意新任务分布上避免灾难性遗忘。

**英文对应表述（非逐字原文）**：On periodic re-evaluation in a fixed curriculum, PSN exceeds Voyager but its last two displayed retention rates fall to 67% and 50%. The result is relative retention, not zero forgetting.（PDF pp. 8–9，Figure 4）

Figure 6 中，“每任务总创建新技能”的变体持续增长，完整 PSN 后期约在 26–30 个技能间平台并略有下降，Voyager 最终约 53 个。这说明复用和重构与较小技能库相关；但该比较同时改变 backward chaining、代码生成频率和重构行为，不能单独量化某一机制的因果贡献。

**英文对应表述（非逐字原文）**：The full PSN library plateaus and slightly contracts, unlike the create-new-skill variant and Voyager. Because several behaviors differ between systems, the figure supports an aggregate system effect rather than a clean single-factor ablation.（PDF pp. 9–11，Figure 6）

离线重构把 Voyager 的 58 个原技能变成 65 个条目（7 generic、20 wrapper、38 unchanged），固定组合任务成功率报告为 0.6875；PSN 在线重构报告为 0.8462。Appendix H 只列出 9 个任务，正文没有说明这两个小数的试验次数、分母或误差，因此只能视为探索性对照。

**英文对应表述（非逐字原文）**：The offline-refactored Voyager library scores 0.6875 versus 0.8462 for online PSN, but the paper does not report the denominators, repetitions, or uncertainty behind these rates.（PDF p. 10，Section 4.4；PDF p. 40，Appendix H）

### LLM 噪声与跨模型分析

知识补丁在 Qwen3 的 synthetic tier-mismatch 诊断上提高 33 个百分点，在 GPT-5-mini 的 Phase-1 reflection cases 上只提高 2 个百分点。两者不是同一个明确配对的数据集，所以能说明弱模型更依赖显式领域知识，却不宜把 33pp 与 2pp 当作严格的跨模型效应量比较。

**英文对应表述（非逐字原文）**：The reported +33pp for Qwen3 comes from synthetic tier-mismatch failures, whereas the +2pp for GPT-5-mini is described on Phase-1 reflection cases; their cross-model comparability is therefore limited.（PDF pp. 8, 10–12, 28，Figure 7；Appendix E）

Table 9 显示 PSN 在一个六子目标设置中从 SR@1 67% 升至 SR@3 100%，说明重试与修复循环能纠正部分初次失败；它不是大样本收敛证明。静态引用检查与 API contract 在 $n=20$ 的 production-prompt replay 中把“任意接口 bug”从 65% 降到 35%。

**英文对应表述（非逐字原文）**：PSN rises from 67% at the first attempt to 100% by the third on six subgoals. Separately, a 20-case prompt replay lowers any interface-bug rate from 65% to 35%.（PDF pp. 11, 41，Figure 7；Table 9）

Table 11 中的 “LLM hallucination 0.3%”来自经过系统流程后的 1,059 条多标签优化记录，而 Figure 7 的 65%→35% 是 20 例接口 replay；分母、采集阶段和指标不同，两者并不矛盾，也不能合并成单一 hallucination rate。错误分类由系统内部 REFLECT 记录得到，论文未报告独立人工标注或一致性。

**英文对应表述（非逐字原文）**：The 0.3% hallucination figure is drawn from 1,059 post-pipeline optimization records, while the 65% and 35% rates use a 20-case interface replay. They measure different populations and stages.（PDF pp. 11, 42，Figure 7；Table 11）

多技能修复中，Qwen3 平均传播深度为 5.0、GPT-5-mini 为 2.7；多技能 episode 分别占 80.8%（63/78）和 56.9%（116/204）。这些是不同模型产生的失败 episode 的条件统计；更深传播可能表示需要更多修复，也可能受任务进度和失败构成影响，不能直接当作更准确的 credit assignment。

**英文对应表述（非逐字原文）**：Average depth is conditioned on multi-skill repair episodes, with unequal episode pools across models. Greater depth indicates broader repair propagation but does not by itself establish better fault attribution.（PDF pp. 41–42，Table 10）

Figure 8b 把 GPT-5-mini 的 **single hero run**（复用比例趋近 0.4）与 Qwen3 的六次运行均值±标准差（$0.15\pm0.07$）放在一起。这个非对称统计口径支持“存在差异”的示例，但不能作为严谨的跨模型方差比较。相比之下，Figure 9 对 Qwen3 的 PSN 与 Voyager 都按六次运行统计，较适合说明 PSN 形成了更多 fan-in≥1 的复用节点。

**英文原文**：“The stronger model (GPT-5-mini, single hero run) climbs toward ≈ 0.4; the weaker model ... mean±1σ over six runs ...” （PDF p. 12，Figure 8b caption）

### 回滚、结构检查与成本

139 个结构重构提议中有 96 个通过预检查并应用，43 个（31%）在写代码前被拒绝。Table 12 的 3.1% 和 6.7% **以全部训练 iterations（131 与 180）为分母**，分别对应 4 与 12 次 post-application rollback；它们不是“占已应用重构的比例”，也不能由表中信息直接换算成 proposal-level rollback rate。

**英文对应表述（非逐字原文）**：Ninety-six of 139 proposals pass pre-application checks. Post-application rollback rates are reported as 4/131 and 12/180 training iterations, not as fractions of applied proposals.（PDF p. 43，Tables 12–13）

PSN 平均每任务约 107K tokens，Voyager* 约 30K，约 3.5 倍。Table 14 的“到 diamond 总成本”采用 3-run 子集（PSN 3/3、Voyager* 0/3），而正文随后引用 Table 1 的六次运行（Voyager* 2/6）；两组样本不能直接混读。CODEGEN 调用从训练前 1/3 的 8.3 次/任务降到后 1/3 的 5.0 次/任务，只证明调用次数下降，没有展示累计成本何时追平 Voyager，因此“成本已经摊销”仍是作者解释而非实证 crossover。

**英文对应表述（非逐字原文）**：PSN uses about 107K tokens per task versus 30K for Voyager. The cost table uses a three-run subset, whereas the surrounding text switches to six-run success figures; declining CODEGEN calls do not establish a cost break-even point.（PDF p. 44，Table 14）

Appendix I 用六个子目标的 SR@3=100% 比较 PSN 的 30 个学习技能和 ODYSSEY 的 183 个手写技能，并称“技能数减少 6×且最终可靠性相同”。这个结论只适用于该六子目标评测；技能数量也不等同于代码量、覆盖面或工程成本。Table 15 还把 ODYSSEY 的 action space 标为 “Code generation”，而正文称其运行时主要是检索预制技能，术语存在内部不一致。

**英文对应表述（非逐字原文）**：The 30-versus-183 comparison is tied to a six-subgoal SR@k evaluation and does not normalize code volume or task coverage. The appendix also describes ODYSSEY as retrieval-based while its taxonomy table labels the action space as code generation.（PDF pp. 41, 44，Tables 8–9, 15）

## 对论文结论的综合评价

### 有说服力之处

- 把失败修复绑定到真实调用轨迹，并把责任分配与代码应用分离，系统边界比“让 LLM 反思后重写全部代码”更清楚。
  **英文对应表述（非逐字原文）**：Only executed trace nodes receive proposals, and feedback propagation is separated from dependency-ordered code updates.（PDF pp. 4, 19–21；Algorithm 1）
- optimizer ablation、跨模型运行、结构提议拒绝和回滚统计从不同侧面说明完整系统确实能持续修复并控制技能库增长。
  **英文对应表述（非逐字原文）**：The evaluation includes an end-to-end optimizer ablation, two LLM backends, and counts of rejected and rolled-back structural changes.（PDF pp. 5, 9–13, 42–43；Tables 1, 10–13）
- 论文公开任务序列、提示模板、算法和代表性代码 diff，便于追踪一次失败如何落到资源、前置条件及父子调用契约。
  **英文对应表述（非逐字原文）**：Appendices provide the task sequences, prompts, two-phase algorithm, and concrete before/after repair cases.（PDF pp. 19–40，Appendices A–H）

### 仍然存在的缺陷

- 关键 Minecraft 结果通常只有 3 或 6 次运行；Figure 17 只有 2 次，Figure 8b 甚至使用单次 strong-model hero run。多项图没有显著性检验，不能支持强泛化或稳定性结论。
  **英文对应表述（非逐字原文）**：Core results use small run counts, and some plots omit clear aggregation details; Figure 17 averages two runs and Figure 8b uses one GPT-5-mini hero run.（PDF pp. 5, 8–12, 46；Figures 3–8, 17）
- “compositional generalization”主要由固定 curriculum、技能数量平台和 fan-in 结构间接衡量，没有在明确 held-out 的组合分布上与等工程预算基线比较。
  **英文对应表述（非逐字原文）**：Reuse and library growth are measured on the training curriculum; a separately sampled held-out composition distribution is not reported.（PDF pp. 8–13，Sections 4.3–4.6）
- 与基线的支撑结构不完全等价。PSN 同时拥有 API contract、静态检查、知识补丁、反复执行、优化和重构验证，结果证明的是完整系统，而非单一 PSN 算子的独立因果效果。
  **英文对应表述（非逐字原文）**：The full PSN stack bundles contracts, static checking, iterative execution, repair, gating, and refactoring, so end-to-end gains do not isolate every component.（PDF pp. 6–12，Sections 4.1–4.6）
- $J(N)$ 是事后诊断量，不是训练目标；权重手工选择。原文说模块“reduce $R_{task}$/$R_{cons}$/$R_{struct}$”，但 Appendix O 又把这些量定义为越大越好的 reward，符号方向自相矛盾。Figure 17 中 $R_{task}$ 后期从接近 1 降到约 0.7、$R_{reliab}$ 几乎始终为 0，而加权和仍约 0.5；Table 16 甚至把 task-only 的 1.00→0.85 标为 “stable”。因此不能把 $J$ 的窄幅变化解释成收敛或稳定性的强证明。
  **英文对应表述（非逐字原文）**：The diagnostic $J$ is hand-weighted and never optimized. Its component direction conflicts with Section 3’s “reduce” wording, and “stable” includes a task-only decline from 1.00 to 0.85.（PDF pp. 5–6, 45–47；Eq. 7–8；Figure 17；Table 16）
- 语义保持依赖分析器、短窗口重测和回滚，没有 formal projection、convergence 或 optimality 保证；作者在 Limitations 中明确承认这一点。
  **英文原文**：“the theoretical properties of symbolic projection, convergence, and optimality remain to be established.”（PDF p. 19，Limitations）

## 覆盖记录

- 请求范围：复核整篇论文对应 Wiki，补齐遗漏并删除/修正错误。
- 已读范围：PDF pp. 1–47；正文 Sections 1–6、Ethics/Reproducibility、Limitations、Appendices A–O。无未读页，无 OCR 警告。
- 实际查看：Figure 1–17 与 Table 1–16 所在页面；重点复核 Figure 2–9、17 和 Table 1、8–16 的轴、图例、分母、模型条件与样本数。
- 未完成：未运行作者代码，未核对仓库 commit，未复现实验；论文中的系统日志分类和成本数据仍仅为作者报告。

## 来源定位

- Zotero：`zotero://users/0/items/5RKUKLBV`
- PDF 内容版本：`sha256:3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72`
- arXiv：[2601.03509v2](https://arxiv.org/abs/2601.03509)
- PDF 页序号与页面底部印刷页码在本文件中均为 1–47；PDF 内嵌 page label 为空。
