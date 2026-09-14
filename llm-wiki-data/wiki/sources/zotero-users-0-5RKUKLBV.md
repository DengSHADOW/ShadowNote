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

- [[concepts/programmatic-skill-network|程序化技能网络（PSN）]]
- [[concepts/trace-guided-skill-repair|执行轨迹引导的技能修复]]
- [[concepts/reliability-aware-skill-updating|可靠性门控的技能更新]]
- [[concepts/validated-structural-refactoring|可验证的结构重构]]

> 阅读状态：draft。已通读 47 页正文与附录，并实际查看全部 Figure 1–17 和 Table 1–16 所在页面；尚未运行作者代码或复现实验。原文为 *Preprint. Under review.*，版本为 arXiv:2601.03509v2。

## 一句话理解

论文提出 Programmatic Skill Network（PSN）：把智能体技能表示为带参数、前置条件、后置条件和子技能调用关系的可执行程序；失败时沿真实执行轨迹定位并修补相关程序，成功后再做受验证、可回滚的结构重构，从而让技能库在持续任务流中复用、稳定和压缩。

这里的 **skill 是 Minecraft/Crafter 智能体执行的 JavaScript 或 Python 程序**，不是 Codex 的 `SKILL.md` 指令文件。PSN 的优化思想可供本项目参考，但论文没有证明提示文件能自动进化。

## 研究问题与动机

作者认为，现有 LLM 智能体常用扁平技能库或静态图：新任务来了就检索或生成代码，但缺少跨组合调用的责任分配、对可靠技能的稳定保护，以及随经验压缩重复结构的机制。PSN 试图回答：一个不断增长的可执行技能库，能否像神经网络训练那样在不同时间尺度上完成局部修复、稳定化和结构调整？（PDF pp. 1–2）

## 方法

### 技能网络与规划

一个技能写成 $s=(C_s,P_s,E_s,\mathrm{CHILDREN}(s))$：$C_s$ 是控制流，$P_s$ 是参数，$E_s$ 包含前置/后置条件，`CHILDREN` 是实际调用的子技能。网络 $N_t=(S_t,L_t)$ 的节点是技能，边是调用关系。（PDF p. 2）

规划器先从目标谓词做符号式 backward chaining，寻找后置条件可以满足当前子目标的技能；多个候选用经验可靠性 $V(s)$ 配合 Boltzmann exploration 选择。现有网络无法覆盖子目标时，才调用 LLM 做 forward planning，并把成功计划蒸馏为新技能。（PDF p. 3，Eq. 2–3）

### 执行轨迹与两阶段修复

执行产生环境反馈、成功标记和调用轨迹 $T_t$；每个轨迹节点记录技能、执行前后符号状态和状态码。失败后，REFLECT 只沿本次实际执行过的子图工作：（PDF pp. 3–4，Eq. 4–5）

1. **Top-down feedback propagation**：从失败根技能向子技能分解责任，生成每个节点的结构化修改提议；此阶段不改代码。
2. **Bottom-up gradient application**：按依赖后序从叶子技能向父技能应用 patch，并把子技能的修改报告传给父技能，减少调用契约不一致。（PDF pp. 19–21，Algorithm 1）

作者把这种离散修改提议称为 symbolic gradient，但它不是数值梯度，也没有可微损失。

### 成熟度门控

每个技能的 $V(s)=\hat p_s-u_s$ 综合带 Laplace smoothing 的成功率和随执行次数下降的不确定性。更新概率为：（PDF p. 4，Eq. 6）

$$
P(\mathrm{update}\ s)=(1-\epsilon)\,\sigma(\gamma(0.6-V(s)))+\epsilon,
$$

其中 $\gamma=5.0$、$\epsilon=0.1$。可靠技能逐渐少改，但始终保留最低更新概率；最近 5 次修复提议组成缓冲区，用来抑制相互矛盾的编辑。

### 在线结构重构与安全检查

成功执行后，系统只检查当前技能的父/子节点及 embedding 最相近的 5 个技能，并识别五类固定关系：参数覆盖、行为/子图覆盖、兄弟特化、公共子技能抽取和完全重复。对应 rewrite 包括 wrapper、调用替换、抽象技能合成、公共子程序抽取和 canonical merge。（PDF pp. 4–5、20–24，Figure 10–14）

结构修改先做语法、类型和语义保持检查；应用后再在涉及该技能的最近 3 个任务上检查成功率。下降超过 20% 就通过逆操作回滚。（PDF p. 5、pp. 42–43）

## “像神经网络训练”的含义与边界

作者建立三组类比：（PDF pp. 5–6）

- 沿执行路径的故障定位类似 backpropagation；未执行技能不更新。
- 成熟度门控类似 layer freezing 或 learning-rate scheduling。
- 合并、抽象和剪枝类似 neural architecture search；回滚类似 trust region。

这个视角主要是解释框架，不是等价性定理。PSN 操作离散程序、接收二元成败与文本反馈、由 LLM 生成编辑；论文也明确承认没有 symbolic projection、收敛或最优性保证（PDF p. 19）。附录定义的综合指标 $J(N)$ 只是诊断量，并未被系统直接优化；因此 Figure 17 的“目标稳定”不能视为优化收敛证明。（PDF pp. 45–47）

## 实验设置

- 环境：Minecraft 1.19.4，基于 MineDojo/Mineflayer；以及带 Mineflayer 风格 Python API 的 Crafter。（PDF pp. 6、14）
- 模型：`gpt-5-mini-2025-08-07`；跨模型实验使用 Qwen3-Coder-Next（3B active / 80B total）。（PDF pp. 6、14）
- 比较：ReAct、Reflexion、AutoGPT、Voyager、ADAM；ODYSSEY 主要在附录做架构与 SR@k 对照。（PDF pp. 6–7、40–41）
- 主要测量：解锁科技树所需迭代、成功次数、Crafter 累计 reward、Skill Retention Rate、技能库规模/复用结构、优化与回滚统计。

## 主要结果与证据

### Minecraft 科技树

使用 GPT-5-mini 时，PSN 在 6/6 次运行中到达 diamond tool，平均 $35\pm16$ 次迭代；同代码和模型下的 Voyager* 仅 2/6 成功，成功运行统计为 $99\pm36$ 次。去掉 optimizer 的 PSN 在木、石、铁阶段接近 Voyager，但 0/3 到达 diamond，说明程序表示本身不足以解释后期表现。（PDF p. 5，Table 1）

使用 Qwen3-Coder-Next 时，PSN 仍在 6/6 次运行中到达 diamond，平均 $49\pm18$ 次；Voyager† 仅 1/6，ADAM† 不能稳定超过 stone。两个模型下 PSN 都未稳定取得 obsidian：GPT-5-mini 为 1/6，Qwen3 为 0/6，所以“完成科技树”的表述应限定到 diamond tool。（PDF pp. 5、7–8，Table 1）

### 持续学习、复用与重构

- Crafter 的累计 reward 曲线中 PSN 高于 Voyager、AutoGPT 和 ReAct；图中同时编码了提前死亡导致的短曲线。论文没有在主文给出显著性检验或完整数值表。（PDF p. 8，Figure 3）
- Skill Retention Rate 图显示 PSN 对已掌握任务的保持高于 Voyager；但这是固定科技树 curriculum 上的周期性重测，不等于任意新任务分布上的抗遗忘。（PDF pp. 8–9，Figure 4）
- 强制每个任务创建新技能的变体持续膨胀；完整 PSN 后期趋于平台并有下降，支持“复用和合并减少技能增殖”的结构性结论。（PDF pp. 9–11，Figure 6）
- Voyager 的 58 个技能经 Claude Opus 4.5 离线重构后形成 65 个条目（7 generic、20 wrapper、38 unchanged），固定组合任务成功率为 0.6875；PSN 在线重构为 0.8462。这个对照支持执行反馈的重要性，但同时改变了算法流程，不能单独隔离所有混杂因素。（PDF p. 10）

### LLM 噪声与跨模型表现

作者把噪声分成知识、推理和接口三层：显式 `tool_tier_rules` 对 Qwen3 的合成 tier-mismatch 诊断提高 33 个百分点，对 GPT-5-mini 仅提高 2 个百分点；环境重执行把 PSN 的 SR@1 67% 提升到 SR@3 100%；静态引用检查和 API contract 在 $n=20$ 的 replay 中把接口错误率从 65% 降至 35%。（PDF pp. 10–11、28、41，Figure 7，Table 9）

弱模型的多技能修复平均传播深度为 5.0，强模型为 2.7；多技能修复分别占 80.8% 和 56.9%。强模型的结构复用比例约 0.4，弱模型为 $0.15\pm0.07$。这表明架构能让两种模型到达 diamond，但并没有消除模型能力对修复成本和网络形状的影响。（PDF pp. 12、41–42，Figure 8–9，Table 10）

### 修复、回滚与成本

- 1,059 条优化记录中，resource miscalculation 占 49.9%，API contract violation 27.8%，precondition gap 24.3%；每条记录可多标签，所以百分比总和超过 100%。作者报告 LLM hallucination 为 0.3%，但该分类来自系统内部记录，尚无独立标注一致性报告。（PDF p. 42，Table 11）
- 139 个结构重构提议中 96 个通过预检查并应用，31% 在改代码前被拒绝；应用后的回滚率为 GPT-5-mini 3.1%、Qwen3 6.7%。（PDF p. 43，Table 12–13）
- PSN 平均每任务约 107K tokens，Voyager* 约 30K，约 3.5 倍开销。作者报告到 diamond 的总成本约 $1.76（3/3 runs），而该表中的 Voyager* 因 0/3 到达而记为无穷；正文另一处引用 6-run Table 1 的 Voyager* 2/6 成功，因此两处 run subset 不同，不能直接混读。（PDF p. 44，Table 14）

## 评价

### 有说服力之处

- 把失败修复绑定到真实调用轨迹，并把责任分配与代码应用拆开，提供了比“让 LLM 反思后重写全部代码”更清楚的系统边界。
- optimizer ablation、在线/离线重构对照、双模型实验和回滚统计分别覆盖了行为修复、结构调整、模型依赖与安全门控，证据链比只展示最终成功率更完整。
- 论文公开算法、提示模板、任务序列和代表性代码 diff，便于理解一次修复如何落到资源计算、前置条件和跨技能契约上。

### 需要谨慎的地方

- 主要结果来自两个游戏环境，Minecraft 多数关键结果只有 3 或 6 次运行；Figure 17 仅平均 2 次 GPT-5-mini 运行。方差大时，强泛化结论仍需要更多种子和环境。
- “compositional generalization”主要由技能数量趋于平台、fan-in 和固定 curriculum 的复用行为支撑；它比在明确隔离的 held-out 组合分布上测试更间接。
- 与基线的工程投入并不完全等价：PSN 有 API contract、静态检查、知识补丁、优化循环和重构验证，Voyager 等系统的支撑结构不同。结果说明完整系统有效，但不完全等于单一 PSN 机制的因果效应。
- 作者把可靠性、结构复用和一致性写入诊断目标 $J$，但 $J$ 的权重手工指定且不参与优化。正文还说模块会“reduce $R_{task}$ 和 $R_{cons}$”，与二者作为正向 reward 分量的定义方向不一致，可能是表述错误。（PDF pp. 5、45）
- 语义保持主要依靠 LLM 分析、短窗口评测与回滚，没有形式保证；作者在 Limitations 中也承认 projection、convergence 和 optimality 尚未建立。（PDF p. 19）
- 本次没有运行代码、核对仓库 commit 或复现实验，不能把论文报告的数字视为独立复现结果。

## 图表覆盖记录

- **Figure 1–2（PDF pp. 3、7）**：实际查看；分别展示 PSN 数据流/网络循环和 Minecraft 科技树迭代曲线。Figure 2 的更低迭代更好，失败运行在 Table 1 中以 N/A 单独表示。
- **Figure 3–6（PDF pp. 8–11）**：实际查看；依次为 Crafter reward、技能保持率、成熟度门控累计成功率和技能库增长。曲线/柱图支持相对趋势，主文未给每点数值和显著性检验。
- **Figure 7–9（PDF pp. 11–13）**：实际查看；对应三层噪声防御、跨模型传播深度/复用比例和弱模型网络 fan-in 分布。
- **Figure 10–14（PDF pp. 22–24）**：实际查看；五种 canonical refactor 的 before/after 示意，是算法说明图，不是性能证据。
- **Figure 15–16（PDF pp. 26–27）**：实际查看；REFLECT 与 skill optimization 提示模板，是实现披露，不是独立实验。
- **Figure 17（PDF p. 46）**：实际查看；$R_{task}$、$R_{reliab}$、$R_{struct}$、$R_{cons}$ 和加权 $J$ 的轨迹。$R_{reliab}$ 几乎为零，$J$ 的稳定主要由其他分量抵消形成。
- **Table 1–16（PDF pp. 5、21、24–25、28、31、41–44、47）**：均实际查看。Table 1、9–14 是主要定量证据；Table 2–8、15 多为机制、案例或方法分类；Table 16 是 $J$ 的权重敏感性检查。

## 来源定位

- Zotero：`zotero://users/0/items/5RKUKLBV`
- PDF 内容版本：`sha256:3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72`
- arXiv：[2601.03509v2](https://arxiv.org/abs/2601.03509)
- PDF 页序号与页面底部印刷页码在本文件中均为 1–47；PDF 内嵌 page label 为空。
