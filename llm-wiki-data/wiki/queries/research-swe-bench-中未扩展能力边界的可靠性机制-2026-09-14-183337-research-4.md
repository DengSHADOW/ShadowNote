---
type: query
title: "Research: SWE-bench 中未扩展能力边界的可靠性机制"
created: 2026-09-14
origin: deep-research
tags: [research]
---

# Research: SWE-bench 中未扩展能力边界的可靠性机制

我会按本项目的 Wiki 维护规范核对既有结构与来源边界，再整理成一页中文综合条目；当前工作区是只读模式，因此若无法落盘，我会提供可直接写入的完整 Markdown。工作区为只读，无法将页面写入 `wiki/synthesis/`。以下是可直接保存为 `swe-bench-reliability-without-capability-expansion.md` 的中文草案。

```markdown
# SWE-bench 中未扩展能力边界的可靠性机制

## 范围与定义

这里的“未扩展能力边界”指保持基础模型、任务输入权限和目标问题范围不变，不通过训练更强模型、泄露隐藏测试或把任务拆给额外的人类开发者来提高结果；改进对象是 [[concepts/agentic-harness|Agentic Harness]] 的验证、执行控制、候选选择、回归防护与运行时治理。该区分重要：任务成功率提高并不自动意味着行为更一致、更可预测或更可控。[6]

SWE-bench 的基本判定是：智能体获得 PR 合并前的代码库与 issue 文本，提交补丁后由对应 PR 的 Fail-to-Pass 测试判定是否修复问题。[15] 因而，可靠性机制应优先减少“同一实例、同一能力配置下，因搜索、执行、测试或发布流程差异而产生的失败”，而不是把一次偶然成功等同于能力提升。

## 可靠性机制

### 以可复现测试作为提交闸门

智能体应在修改前建立复现步骤，修改后运行最相关的回归测试与必要的邻近测试；补丁只有在隔离环境中通过预先定义的测试集合后才可作为候选提交。[1][5][15] Multi-SWE-bench 对测试状态迁移的筛选提供了更严格的模板：保留可观察到失败后通过的实例，排除异常或含混的测试迁移，并分别记录 `f2p_tests`、`s2p_tests`、`n2p_tests` 与完整运行结果。[12][14]

这一机制不提升模型对代码的理解上限，但把“生成了看似合理的补丁”转换为“补丁在可观察行为上满足验证条件”。它也对应 [[concepts/schema-fragility|工具调用智能体的模式脆弱性]]：测试命令、环境准备和结果解析本身都必须被结构化记录与检查，否则模型的正确推理可能因执行接口错误而失效。

### 将随机 rollout 转化为受控的候选选择

同一模型对同一问题的多次 rollout 可能得到不同结果；Augment Code 报告其样本中不同 rollout 的成功结论不稳定，并称集成方法可带来 3–8 个百分点的增益。[5] 因此，可在固定模型与固定输入权限下生成有限数量的独立候选，以统一测试、静态检查和最小变更原则排序，而不是直接采纳第一个补丁。

候选数量、温度、时间预算、总 token、测试次数与选择规则必须事先固定并随结果报告。否则，集成只是以更多计算换取更高的 Pass@k，不能被表述为相同成本下的 Pass@1 可靠性提升。[5]

### 独立代码审查与反证检查

将“生成补丁”和“寻找补丁缺陷”分离，可以降低单一路径的确认偏误。一个 Reddit 小样本报告称，在 100 个实例上加入第二个代码审查智能体后，解决率从 80% 升至 90%，但平均用时从 3.5 分钟增至 7.8 分钟；作者也明确说明这不是完整 500 题评测。[2]

实践上，审查者应在不知道生成过程偏好的条件下检查：

- issue 的关键行为是否确实被覆盖；
- 修改是否破坏相邻接口、错误处理或向后兼容性；
- 测试是否只是迎合单个复现样例；
- 是否存在更小且更可维护的补丁。

该机制应报告额外模型、计算和时延。若审查者是额外的强模型，它提高的是系统层面的冗余与选择能力，而非“零资源增加”的可靠性。

### 隐藏评测与回归集隔离

SWE-bench 的正式评测不应向智能体公开 Fail-to-Pass 测试名称、测试代码或 test patch；一个遵循官方协议的公开实验也明确采用这种隔离。[2][15] 本地开发可使用自写复现测试和公开项目测试，但最终验收集应与补丁生成过程隔离，避免测试泄漏导致的表面可靠性。

随着能力评测中的任务逐渐变成已掌握功能，应把已通过实例纳入稳定的回归集：新版本不仅要追求解决新 issue，也不得降低既有实例的通过率。[7] 这把可靠性定义为跨版本保持，而不只是单次最高分。

### 执行韧性、权限约束与可审计性

对长时运行的编码智能体，可靠性还取决于任务中断后的状态恢复、工作目录隔离、资源上限与审计记录。运行时可持久化检查点，在进程或虚拟机故障后恢复到已知状态；同时为命令、网络、密钥和文件写入配置最小权限、超时、步骤上限与人工批准点。[9][10]

部署流程应把离线评测、线上可观测性和发布决策连接到同一套评分与追踪逻辑。[8] 对 SWE-bench 而言，这意味着保留每次补丁的基线 commit、命令轨迹、测试日志、依赖版本、候选选择理由和最终 diff，支持失败复现与回归定位。

## 建议的最小评测协议

1. 固定基础模型、prompt、工具集、容器镜像、实例集合与每题资源预算。
2. 在不暴露 Fail-to-Pass 测试的条件下，让智能体自行定位代码、编写复现步骤并生成补丁。[5][15]
3. 对每题运行固定次数的独立 rollout，报告 Pass@1、通过率方差、首次通过时间、平均成本与超时率，而非只报告最佳结果。
4. 对通过本地测试的候选执行独立审查；审查结论必须附带可执行的反证测试、风险说明或拒绝理由。
5. 在隔离的官方评测环境运行隐藏测试，并分别记录修复成功、回归失败、环境失败与超时。
6. 将已确认通过的实例冻结为回归集；后续配置变更必须同时报告新能力集与回归集的结果。
7. 在生产环境中使用沙箱、最小权限、检查点、日志和高风险操作审批；这些控制不能由离线 benchmark 分数替代。[8][9][10]

## 适用边界

SWE-bench 的 Fail-to-Pass 测试是强而有限的行为判据：它能验证目标 PR 所覆盖的功能，却不能充分证明补丁的安全性、可维护性、性能、设计质量或真实组织环境中的正确性。[15] 因此，测试通过应是发布闸门的一部分，而不是自动部署的充分条件。

跨基准分数也不能直接比较。Multi-SWE-bench 覆盖多语言、多难度和不同类型问题；其榜单中的总体解决率明显受语言、难度与系统配置影响。[11][13][14] 该基准发现长 issue 描述通常更有利，而大于 600 tokens 的修复补丁或多文件修改会显著增加难度，说明验证与执行机制不能消除 [[concepts/capability-floor|自我改进智能体的能力下限]]。[14]

## 证据强度、矛盾与缺口

- [6] 提供“能力与可靠性应分开评估”的直接研究论据，但不是针对 SWE-bench 专门设计的机制消融。
- [15]、[12]、[13]、[14] 是基准定义、数据结构与评测规则的主要依据。
- [1] 与 [5] 说明真实 SWE-bench agent 的测试、搜索和 scaffold 做法，但均来自模型或工具提供方，不应单独作为中立效果比较。
- [2] 的双智能体结果具有启发性，但仅覆盖 100 个实例、来自自述实验，且时延增加 2.2 倍；不能外推为通用增益。
- [3] 与 [4] 报告了很高分数或明显的分布外落差，但所给材料缺少可复核的完整协议、日志和独立复现，应视为待验证线索。
- [7]–[10] 主要提出通用工程与治理建议，尚未证明这些运行时机制会在 SWE-bench 上带来独立、可量化的增益。
- 不同分数——例如 Claude 3.5 Sonnet 的 49% 报告值、样本实验的 80%/90%，以及其他宣传性高分——使用的模型、日期、harness、样本范围、预算和评测设置不同，不能构成同一排行榜上的因果比较。[1][2][3]

## 值得补充的来源

- SWE-bench 官方评测代码、版本说明与污染控制文档，以核对隐藏测试和容器复现细节。
- 在完整 SWE-bench Verified 集上预注册的消融实验：单智能体、重复 rollout、独立审查、测试闸门各自的 Pass@1、方差、成本与时延。
- 真实软件仓库中的前瞻性研究，用于测量 benchmark 通过、代码审查接受、线上回归和安全缺陷之间的相关性。
- 关于测试充分性、补丁过拟合、benchmark contamination 与语义等价修复的同行评审研究。
- 将 [[concepts/agentic-harness|Agentic Harness]] 的运行时日志与可重复评测统一起来的研究，以比较执行故障、推理失败和验证缺失各自对失败率的贡献。

## 参考来源

[1] Claude SWE-Bench Performance  
[2] I ran 100 SWE-bench tests comparing 1 agent vs 2 agents  
[3] From 80% to 93.9%: Why the Claude Mythos SWE-Bench Jump Matters | MindStudio  
[4] Claude Opus 4.1 scores 80% on SWE-Bench...  
[5] #1 open-source agent on SWE-Bench Verified by combining Claude 3.7 and O1 | Augment Code  
[6] Towards a Science of AI Agent Reliability  
[7] Medium  
[8] AI agent reliability tools expose the gap between evals and runtime  
[9] AI Agent Runtime | Guild.ai  
[10] Sector Deep Dive #6: AGENT RUNTIME  
[11] Multi-SWE-bench  
[12] ByteDance-Seed/Multi-SWE-bench_mini · Datasets at Hugging Face  
[13] Multi-SWE-bench: A Multilingual Benchmark for Issue ...  
[14] Multi-SWE-bench: A Multilingual Benchmark for Issue Resolving  
[15] Can Language Models Resolve Real-world Github Issues
```

## References

1. [Claude SWE-Bench Performance](https://www.anthropic.com/engineering/swe-bench-sonnet) — anthropic.com
2. [I ran 100 SWE-bench tests comparing 1 agent vs 2 agents](https://www.reddit.com/r/ClaudeAI/comments/1qi2gh0/i_ran_100_swebench_tests_comparing_1_agent_vs_2) — reddit.com
3. [From 80% to 93.9%: Why the Claude Mythos SWE-Bench Jump Matters | MindStudio](https://www.mindstudio.ai/blog/claude-mythos-benchmark-results-swe-bench-agentic-coding) — mindstudio.ai
4. [Claude Opus 4.1 scores 80% on SWE-Bench. Give it code ...](https://www.reddit.com/r/ClaudeAI/comments/1rp6j4w/claude_opus_41_scores_80_on_swebench_give_it_code) — reddit.com
5. [#1 open-source agent on SWE-Bench Verified by combining Claude 3.7 and O1 | Augment Code](https://www.augmentcode.com/blog/1-open-source-agent-on-swe-bench-verified-by-combining-claude-3-7-and-o1) — augmentcode.com
6. [Towards a Science of AI Agent Reliability](https://arxiv.org/html/2602.16666v2) — arxiv.org
7. [Medium](https://medium.com/@dave-patten/eval-driven-agent-development-what-actually-makes-ai-agents-work-13fb7d4e1e77) — medium.com
8. [AI agent reliability tools expose the gap between evals and runtime](https://nhimg.org/articles/ai-agent-reliability-tools-expose-the-gap-between-evals-and-runtime) — nhimg.org
9. [AI Agent Runtime | Guild.ai](https://www.guild.ai/glossary/ai-agent-runtime) — guild.ai
10. [Sector Deep Dive #6: AGENT RUNTIME - by Prateek Joshi](https://www.infrastartups.com/p/sector-deep-dive-6-agent-runtime) — infrastartups.com
11. [Multi-SWE-bench](https://multi-swe-bench.github.io) — multi-swe-bench.github.io
12. [ByteDance-Seed/Multi-SWE-bench_mini · Datasets at Hugging Face](https://huggingface.co/datasets/ByteDance-Seed/Multi-SWE-bench_mini) — huggingface.co
13. [Multi-SWE-bench: A Multilingual Benchmark for Issue ...](https://github.com/multi-swe-bench/multi-swe-bench) — github.com
14. [Multi-SWE-bench: A Multilingual Benchmark for Issue Resolving](https://arxiv.org/html/2504.02605v1) — arxiv.org
15. [Can Language Models Resolve Real-world Github Issues](https://www.swebench.com/original.html) — swebench.com
