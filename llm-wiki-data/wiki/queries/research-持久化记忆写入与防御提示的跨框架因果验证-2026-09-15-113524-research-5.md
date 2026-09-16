---
type: query
title: "Research: 持久化记忆写入与防御提示的跨框架因果验证"
created: 2026-09-15
origin: deep-research
tags: [research]
---

# Research: 持久化记忆写入与防御提示的跨框架因果验证

我会按 `wiki-maintenance` 的 query/synthesis 流程处理：先核对项目约定与现有 Wiki 页面，再基于给定来源生成中文页面草稿；本次请求未明确要求入库，因此不改写仓库文件。当前工作目录是 Wiki 数据目录本身，约定中部分路径以仓库上级为基准。我正在定位这些文件的实际位置，并核对与本主题直接相关的安全页面，避免生成断链或重复概念。# 持久化记忆写入与防御提示的跨框架因果验证

## 概述

持久化记忆攻击把传统 prompt injection 从单次会话中的瞬时劫持，转化为跨会话状态污染：攻击载荷先经网页、文档、RAG 检索结果或工具输出进入智能体，再被摘要或记忆写入机制保存，最后由一个表面良性的未来请求触发。其安全影响不能用单一 attack success rate 描述，而应拆分为“注入、写入、留存、检索、执行和造成损害”六个阶段。[1][2][3]

现有材料已经证明，持久化记忆污染能够在 [[OpenClaw|OpenClaw]]、HERMES 和 Amazon Bedrock Agent 等不同系统中发生。[2][3][4] 然而，这些结果尚不足以证明某一段[[防御提示|防御提示]]具有可跨框架泛化的因果效果。当前证据混合了不同模型、记忆实现、攻击载荷、提示位置和成功判据；“在某个设置中阻止执行”也不能直接推出“阻止了恶意记忆写入”。

## 注入与执行的阶段分离

持久化攻击至少包含以下因果链：

```text
不可信内容暴露
    → 恶意指令被模型接受
    → 恶意内容写入持久化记忆
    → 跨会话留存
    → 在后续会话中被检索
    → 模型执行载荷
    → 工具调用或数据外传
```

可为每次试验定义：

- $W$：恶意内容是否成功写入；
- $S$：内容是否跨会话存活；
- $R$：后续会话是否检索到该内容；
- $E$：模型是否遵循其中的指令；
- $H$：是否发生数据外传、越权操作等实际损害。

这种分解体现了 [1] 所强调的 injection–execution dissociation。该研究摘录报告其测试中的注入率达到 100%，同时援引 GPT-5.5 上 99.8% 的对抗性记忆存储率；但未来对话 steering 的成功率为 60%–89%，RAG 注入导致数据外传的 ASR 为 60.3%。这些差异表明，成功写入不是成功执行的充分条件。[1]

因此，只报告最终 $H$ 会掩盖防御究竟作用于哪个阶段。例如，一段[[防御提示|防御提示]]可能不降低 $W$，却降低 $E$；检索分类器可能降低 $R$，但完全不清除已经存在的污染；tool-call validation 则主要作用于 $E \rightarrow H$，并不修复持久化状态。

## 跨框架证据

| 系统或框架 | 记忆或状态通道 | 已有证据 | 对因果验证的主要限制 |
|---|---|---|---|
| [[OpenClaw|OpenClaw]] | `MEMORY.md` 等持久化文件 | MPBench 对其进行记忆污染评估；其他 PoC 显示虚构规则可跨会话影响行为。[2][4][5] | 需要区分文件成功写入、启动时载入、模型服从和工具执行 |
| HERMES | 框架内记忆写入与检索机制 | MPBench 将其与 [[OpenClaw|OpenClaw]]并列评估，并认为更积极写入和检索记忆的系统更易受攻击。[2] | 摘录没有给出各攻击类别、写入通道和防御条件的完整分层结果 |
| Amazon Bedrock Agent | session summarization 与长期记忆 | 恶意网页能够影响摘要，使指令跨会话进入 orchestration prompt，并在以后外传对话历史；记忆保留期可配置到 365 天。[3] | 属于单一 PoC，且文章明确说明这不是 Amazon Bedrock 平台本身的漏洞 |
| AgentSys | 分层工作记忆、上下文隔离和 schema-bounded communication | 通过限制进入工作记忆的信息，降低 indirect prompt injection 的持续影响。[6] | 主要处理单次 workflow 的 working memory，并非对长期记忆数据库写入防御的等价检验 |
| MCP-based SOC 多智能体系统 | 三个持久化共享存储 | 中间件包含访问控制、输入输出验证和审计，并在恶意 MCP server 下进行可重复测试。[12] | 摘录没有隔离“持久化存储被污染”及其跨会话执行效果 |
| 一般多智能体系统 | 共享 context、agent metadata 或知识库 | 文献指出持久状态扩大暴露时间，建议 zero-trust communication、隔离记忆和 hardened orchestrator。[11][15] | 多为风险论证或设计建议，缺少随机化干预及逐阶段测量 |

这些结果支持“漏洞可跨实现出现”，但尚未支持“同一防御在各实现上具有相同效果”。框架间的记忆写入策略、摘要模板、检索规则、默认信任等级和工具权限都是潜在效应修饰因素。

## 防御提示与结构性防御

[[防御提示|防御提示]]属于行为层干预：它通过 instruction hierarchy、spotlighting、标签或警告文本，帮助模型区分数据与指令。[7][9][10] 这类方法成本较低，但依赖模型服从自然语言约束，缺少形式保证，并可能被改写、混淆或针对性优化的载荷绕过。[7][8]

现有 Wiki 中的 [[sources/2608.10218v1|Mind Viruses: Self-Propagating Ideas in Multi-Agent LLM Systems]] 提供了一个重要但范围有限的正面结果：附加到 [[OpenClaw|OpenClaw]] 默认 soul 后的[[防御提示|防御提示]]，在 Claude Haiku 4.5 的定向演化实验中阻止了超过一跳的 [[virus-chain|virus chain]] 传播。该实验衡量的是显式自传播，而不是 MPBench 式记忆污染或数据外传；作者也未排除更隐蔽或 jailbreak 型载荷。因此，它不能与“现有 prompt injection 防御没有覆盖 memory poisoning”这一结论直接互相否定。[1][2]

结构性防御则把安全边界放在模型之外，包括：

- 对来自网页、RAG 和工具输出的记忆候选项进行隔离；
- 仅允许预定义 schema 和记忆类型进入可信存储；
- 保存来源、写入者、会话和转换链等 provenance；
- 由独立组件批准记忆从 quarantine 晋升到长期存储；
- 分离处理不可信内容的模型与具有工具权限的 executor；
- 对敏感工具调用实施 allowlist、最小权限和人工确认。[5][6][7][8]

这些措施分别控制写入、检索和执行阶段。AgentSys 的 hierarchical context isolation 与 schema-bounded communication 提供了结构性方向，但仍需在真正跨会话的持久化数据库上验证。[6] 对多智能体系统而言，记忆条目还应继承其外部输入的信任等级，否则 agent 转述可能形成[[请求洗白|请求洗白]]，并越过[[智能体间元数据的信任边界|智能体间元数据的信任边界]]，最终演变为[[多智能体系统控制流劫持|多智能体系统控制流劫持]]。

## 建议的跨框架因果实验

### 干预条件

应在 [[OpenClaw|OpenClaw]]、HERMES 和至少一种托管型记忆系统上实施同一套析因实验：

| 条件 | [[防御提示|防御提示]] | 结构化写入门控 |
|---|---:|---:|
| 基线 | 无 | 无 |
| 提示干预 | 有 | 无 |
| 架构干预 | 无 | 有 |
| 组合干预 | 有 | 有 |

每次试验必须从相同的干净记忆快照开始，固定模型、framework 版本、记忆配置、工具权限和攻击语料，并随机分配干预条件。否则，持久化状态会在试验之间造成污染和顺序效应。

### 主要估计量

对框架 $f$ 的[[防御提示|防御提示]]效果可定义为：

$$
ATE_f = P(H=1\mid do(D=1),F=f)-P(H=1\mid do(D=0),F=f)
$$

其中 $D$ 表示是否启用提示，$H$ 表示最终危害。还应分别估计提示对 $W$、$S$、$R$ 和 $E$ 的影响，以判断效果是阻止写入、阻止检索，还是仅在执行阶段产生拒绝。

跨框架结论不能只依赖合并后的平均值。应报告每个 $ATE_f$、置信区间以及 $D \times F$ 交互项；如果某个框架中效果消失或反向，就不能宣称存在普遍防御效果。模型、攻击类别、写入通道和 prompt placement 也应作为预先指定的效应修饰因素。

### 成功判据

与 [[actionable-verification-criterion|可操作的验证标准]]一致，防御成功至少应同时满足：

1. 恶意写入率或最终危害率显著下降；
2. 效果在所有预注册框架中保持同向；
3. 对载荷改写、编码、延迟触发和针对性演化保持稳健；
4. 良性记忆写入、长期问答和工具任务的效用下降不超过预设非劣界值；
5. 实验能区分“拒绝当前请求”和“清除持久化污染”。

提示放在输入层、记忆写入器、检索结果或 executor 前，属于不同的[[feedback-injection-location|反馈注入位置]]，必须作为独立条件测试，不能笼统记为“启用了防御”。

## 表面矛盾及其解释

第一，AgentDojo、InjecAgent 和 ASB 中输入层防御效果较高，而 MPBench 和 [1] 认为现有防御未覆盖持久化攻击。这主要是威胁模型差异：前者测量当前会话中的 payload，后者测量由 RAG 或记忆数据库跨会话触发的 payload。[1][2]

第二，[[防御提示|防御提示]]曾阻断特定 [[mind-virus|mind virus]] 的多跳传播，但一般性文献认为 prompt-only defense 脆弱。[7][8] 两者可以同时成立，因为前一结果限定于特定模型、载荷和传播指标，后一判断针对开放攻击分布。

第三，受控环境中持久文件可支持跨 hop 行为，而 Moltbook、Clawstagram 等社交环境未必出现可靠的自然第二跳。这一差异已在 [[受控-virus-chain-存活与社交环境多跳失败-2026-09-15-113239|受控 virus chain 存活与社交环境多跳失败]] 中提出。它说明“存储能够持久化”不等于“载荷会在真实交互网络中持续传播”。

第四，AgentSys 宣称防止 attack persistence，但其 persistence 主要指指令在 workflow working memory 中持续存在；长期数据库污染则跨越独立会话。两者的时间边界和信任边界不同，不能使用同一个成功率直接比较。[2][6]

## 证据缺口

当前材料仍缺少以下关键证据：

- 同一攻击集、模型和判据下的跨框架随机对照实验；
- 对记忆写入、跨会话存活、检索和执行的逐阶段日志；
- [[防御提示|防御提示]]与 quarantine、provenance、schema validation 等结构性措施的析因比较；
- 防御提示经过针对性优化或长期演化后的稳健性结果；
- 防御对良性长期记忆质量、延迟、成本和误拒率的系统测量；
- 共享记忆中跨 agent、跨用户和跨租户污染的访问控制实验；
- 对真实部署发生率的估计，而不仅是受控 PoC 或固定 benchmark ASR。

[4][5][7][9][10][14][15] 主要属于数据库条目、视频、博客或行业论述，适合用于发现威胁与设计假设，不宜单独承担强因果结论。[13] 只有摘要性描述，无法据此评价 SAMEP 的具体安全机制和实验质量。

## 值得补充的来源

后续应优先寻找：

- [1]、[2] 与 [6] 的完整论文、附录、代码、攻击语料及逐配置结果；
- MPBench 关于四种写入通道、六种攻击类别和防御实现的完整定义；
- Cross-Session Stored Prompt Injection、MINJA 和 OEP 的原始论文与复现实验；
- Amazon Bedrock Agent 官方 memory、session summarization 和 prompt-template 文档；
- [[OpenClaw|OpenClaw]] 与 HERMES 被测版本的实际记忆写入、加载和删除代码；
- AgentDojo、InjecAgent、ASB 的防御实现，以便在持久化威胁模型中重新运行；
- 关于 provenance、information-flow control、capability security 和不可变审计日志的系统安全研究。

## 综合判断

现有证据足以支持“持久化记忆写入是独立于单会话 prompt injection 的攻击面”，也表明漏洞并非某一个框架的偶发现象。[1][2][3] 但[[防御提示|防御提示]]的跨框架因果有效性仍未建立。最关键的下一步不是再增加一个总 ASR，而是在多个真实记忆实现中随机化防御条件，分别测量 $W$、$S$、$R$、$E$ 和 $H$，并将提示层效果与结构性写入和执行控制分离。只有这种阶段化、跨框架且包含效用基线的实验，才能判断提示是在阻止污染、延迟触发，还是仅暂时压低可观察的危害率。

## References

1. [Injection–Execution Dissociation: A Mechanistic Evaluation of Persistent Memory Attacks and Defenses in Stateful LLM Agents](https://arxiv.org/html/2605.08442v5) — arxiv.org
2. [From Untrusted Input to Trusted Memory: A Systematic Study of Memory Poisoning Attacks in LLM Agents](https://arxiv.org/html/2606.04329v1) — arxiv.org
3. [When AI Remembers Too Much – Persistent Behaviors in Agents’ Memory](https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory) — unit42.paloaltonetworks.com
4. [Poisoning Research · Page 2 | LLM Security Database](https://www.promptfoo.dev/lm-security-db/tag/poisoning?tags=data-security%2Cinjection&sort=updated&page=2) — promptfoo.dev
5. [The Attack That Waits: Poisoning an AI Agent's Memory](https://www.youtube.com/watch?v=x5Jpp946fEE) — youtube.com
6. [AgentSys: Secure and Dynamic LLM Agents Through Explicit Hierarchical Memory Management](https://arxiv.org/html/2602.07398v1) — arxiv.org
7. [5 Practical Defenses for Prompt Injection in LLMs](https://blog.dailydoseofds.com/p/5-practical-defenses-for-prompt-injection) — blog.dailydoseofds.com
8. [Design Patterns for Securing LLM Agents against Prompt Injections | alphaXiv](https://www.alphaxiv.org/abs/2506.08837) — alphaxiv.org
9. [LLM Chronicles #6.9: Design Patterns for Securing LLM ...](https://www.youtube.com/watch?v=2Er7bmyhPfM) — youtube.com
10. [Medium](https://gregrobison.medium.com/the-crisis-of-agency-a-comprehensive-analysis-of-prompt-injection-and-the-security-architecture-of-d274524b3c11) — gregrobison.medium.com
11. [Advancing Multi-Agent Systems Through Model Context ...](https://arxiv.org/html/2504.21030v1) — arxiv.org
12. [Design of a Security Framework for Multi-Agent Systems Based on Model Context Protocol in SOC Environments](https://www.mdpi.com/2076-3417/16/16/7915) — mdpi.com
13. [(PDF) SAMEP: A Secure Protocol for Persistent Context ...](https://www.researchgate.net/publication/393724266_SAMEP_A_Secure_Protocol_for_Persistent_Context_Sharing_Across_AI_Agents) — researchgate.net
14. [Multi-Agent Architecture for Automated Penetration Testing](https://www.redfoxsec.com/blog/multi-agent-architecture-for-automated-penetration-testing) — redfoxsec.com
15. [Securing Multi-Agent AI Development Systems](https://www.knostic.ai/blog/multi-agent-security) — knostic.ai
