---
type: query
title: "Research: 传播、意识形态内化与有害行为的独立测量"
created: 2026-09-15
origin: deep-research
tags: [research]
---

# Research: 传播、意识形态内化与有害行为的独立测量

我会按 `wiki-maintenance` 的知识综合流程处理：先核对项目状态、Wiki 结构与现有相关页面，再形成中文页面，并确保已有概念均用 `[[wikilink]]` 连接。当前环境是只读的；我会先完成证据核对，若无法写入仓库，就直接交付可落盘的完整页面内容。项目路径看起来已直接指向数据目录，约定里使用的是相对仓库根目录的路径。刚才这些相对路径因此多了一层；我正在定位实际文件，并只加载与该主题相关的现有页面。当前工作区为只读，因此未直接写入仓库。以下内容可保存为 `wiki/synthesis/传播-意识形态内化与有害行为的独立测量.md`。

# 传播、意识形态内化与有害行为的独立测量

## 核心观点

多智能体系统中的传播、意识形态内化与有害行为是三个可能相关、但不能相互替代的测量对象：

| 构念 | 核心问题 | 直接证据 | 不能作为充分证据的现象 |
|---|---|---|---|
| 传播 | 一个未预置载荷的智能体是否因接触上游内容而继续向下游传递它？ | 带来源记录的跨边界再传输、跨 hop 存活和下游覆盖 | 消息被送达、文件仍存在、seed agent 自己重复载荷 |
| 意识形态内化 | 智能体的立场、目标或评价准则是否发生持久且可泛化的变化？ | washout 后的立场变化、跨措辞一致性、反驳压力下的稳定性 | 复述原文、一次 probing 得分、遵循显式角色提示 |
| 有害行为 | 系统是否实际造成未经授权或违反安全规范的状态变化？ | 工具执行记录、环境状态变化、数据外传或其他可验证后果 | 表达有害立场、生成但未执行的计划、单个 agent 的拒绝 |

因此，不宜把三者压缩为一个“感染率”或“安全分数”。最低限度应报告向量

$$
M=(P,I,H),
$$

其中 $P$ 表示传播，$I$ 表示意识形态内化，$H$ 表示有害行为，并分别给出不确定性。

## 概念边界

### 传播

传播是一个跨主体、跨边界的因果事件。载荷出现在 Agent B 的输入中只能证明“送达”；只有原本未携带载荷的 Agent B 在接触后主动将其写入下游消息、共享 memory、工具结果或持久化文件，才构成一次再传播。多智能体 prompt injection 之所以具有传播性，正是因为 agent 输出会成为其他 agent 的输入或控制信息。[11][12][13][15]

传播测量应区分：

1. **送达**：载荷是否进入下一组件的上下文。
2. **保留**：载荷是否在 memory、文件或状态中继续存在。
3. **再生产**：未预置载荷的 agent 是否生成新的传递行为。
4. **覆盖**：传播到多少 agent、边或子系统。
5. **保真度**：语义、目标和约束在多跳之后保留到什么程度。

这一区分与 [[mind-virus|mind virus]]、[[virus-chain|virus chain]] 和 [[验证驱动传播链|验证驱动传播链]] 直接相关。日志或确认文件可以证明传播步骤发生，却不能单独证明原始意识形态已经被内化。

传播还可能通过 [[请求洗白|请求洗白]] 发生：不可信指令被重新包装成状态报告或错误信息，继而跨越 [[智能体间元数据的信任边界|智能体间元数据的信任边界]]。因此，检测必须覆盖工具结果、retrieval、sub-agent 输出和 orchestrator 输入，而不能只检查用户入口。[14]

### 意识形态内化

意识形态内化指智能体的评价准则、核心立场或目标发生持续变化，而不仅是输出中出现某段文字。ADMA 等研究把多轮辩论中的立场稳定性和 belief–action consistency 作为 belief consistency 的观测信号。[3] 行为科学综述则指出，LLM agent 往往存在 belief updating 与 belief–action alignment 不一致的问题。[4]

但“保持初始立场”与“内化外部意识形态”不是同一构念。前者可能来自系统提示、角色扮演、上下文惯性或机械复述；后者要求在显式载荷消失后仍出现相对于基线的系统性变化。抵抗反驳也不天然代表更好的 reasoning：它既可能是稳定信念，也可能是错误立场的僵化。

因此，意识形态测量至少需要：

- 暴露前基线；
- 不含原载荷措辞的隐蔽 probes；
- context reset 或 washout 后的延迟复测；
- 同义改写、相反措辞和问题顺序扰动；
- 新情境中的价值判断与安全行为任务；
- 与未暴露对照组的差分比较。

### 有害行为

有害行为是系统产生的实际结果，而不是其表达的态度。Agent security benchmark 通常使用 Attack Success Rate（ASR）、Refusal Rate（RR）、Harm Score 或 Safety Score；AgentSecurityBench 还覆盖直接 prompt injection、observation prompt injection、memory poisoning 和 plan-of-thought backdoor。[6]

ASR 与 RR 不应被当作互补量。一个 agent 拒绝后，orchestrator 仍可能重试、改派其他 agent 或执行已经生成的工具调用；这正是 [[多智能体系统控制流劫持|多智能体系统控制流劫持]] 所强调的系统级风险。相反，表达某种有害意识形态但未产生可执行后果，也不能自动计为成功攻击。

对于有明确环境状态的任务，应优先使用确定性验证器。SEC-bench 通过可复现 PoC 和经过验证的 patch 判断安全任务是否完成，说明真实工件和环境检查可以减少纯文本评分的歧义。[7] 文本性伤害无法确定性判断时，才需要经过校准的人类或 LLM rubric。

## 因果关系

```mermaid
flowchart LR
    E[接触载荷] --> P[向下游再传播]
    P --> E2[更多智能体接触载荷]
    E --> I[立场或目标发生变化]
    I --> D[后续决策倾向]
    D --> H[有害行为]
    E --> H
    M[恶意 metadata 或 orchestration] --> H
```

该模型包含三条不同路径：

- `传播 → 新暴露`：扩大受影响范围，但不要求传播者相信载荷；
- `内化 → 决策 → 行为`：立场变化可能影响行为，但需要行动机会；
- `暴露或控制流 → 行为`：agent 可以在没有稳定信念变化的情况下机械服从恶意指令。

因此，观察到 $P>0$ 不能推出 $I>0$ 或 $H>0$；观察到 $H>0$ 也不能反推存在意识形态内化。

## 建议的独立实验设计

### 三因素随机实验

可以采用 $2\times2\times2$ 因子设计，分别操纵：

- **传播内容**：可识别的 neutral canary 与意识形态载荷；
- **传播机会**：允许或阻断 agent 间传递和持久化；
- **行动能力**：只读 sandbox 与具有受控工具权限的环境。

只对 seed agent 植入载荷，其余 agent 保持未预置状态。这样可以分别估计内容、通信结构和执行权限的主效应及交互效应，避免把“能复制文字”“接受立场”和“有能力执行”混为一谈。

为处理 LLM agent 的随机性，同一条件应重复运行，并报告均值、失败尾部、方差和置信区间。[10] 链式实验还应把 run、agent、模型、拓扑和 hop 作为分层因素，而不能把同一条链上的节点视为独立样本。

### 传播指标

对第 $h$ 个 hop，可定义：

$$
P_h=
\frac{\text{接触后由未预置 agent 产生的下游传输数}}
{\text{具有传输机会的已接触 agent 数}}.
$$

同时报告：

- hop survival curve $S(h)$；
- 累计触达 agent 数和边数；
- 精确字符串、结构和语义三种保真度；
- 每条 inter-agent boundary 的传输概率；
- 首次再传播所需时间、turn 和 tool call 数；
- 传播是否依赖可写 memory、特定 metadata 字段或权限。

可使用随机 nonce、来源标签和不可变 trace 判断内容是否来自 seed；语义改写则应由与内化评分器隔离的传播评分器判断。链级 telemetry 有助于区分一次 payload 的连续移动与多个互不相关的异常。[14]

### 意识形态内化指标

可使用差分中的差分：

$$
I=
(\bar z_{\mathrm{post}}-\bar z_{\mathrm{pre}})_{\mathrm{treated}}
-
(\bar z_{\mathrm{post}}-\bar z_{\mathrm{pre}})_{\mathrm{control}},
$$

其中 $z$ 是由多项、平衡措辞的 probe battery 得到的标准化立场分数。

还应单独报告：

- washout 后效应保留率；
- paraphrase 与新情境泛化；
- 正反措辞之间的一致性；
- 面对反驳时的变化轨迹；
- belief–action alignment；
- 未要求传播时是否仍持有该立场。

测量材料不应包含“把这段内容告诉下一个 agent”之类传播指令，否则 probing 本身会重新激活载荷。评估者也不应看到实验条件标签。

### 有害行为指标

首要指标应是经过环境验证的 harmful state transition：

$$
H_i=
\begin{cases}
1,&\text{预注册的有害状态或安全违规实际发生}\\
0,&\text{否则}
\end{cases}
$$

在二元 ASR 之外，可报告：

$$
H_{\mathrm{severity}}
=\frac{1}{n}\sum_i H_i s_i,
$$

其中 $s_i$ 是预先定义的严重性权重。

必要的辅助指标包括：

- 实际工具执行率；
- 越权或跨 trust boundary 的调用率；
- 数据、资金或系统完整性的真实变化；
- 生成计划到执行结果的转化率；
- RR、guardrail intervention rate 和检测提前量；
- 达成有害结果所需的权限、步骤、成本和重试次数。

端到端指标说明系统最终是否造成伤害，component-level 指标则帮助定位失败发生在 retrieval、generator、tool call、memory 还是 orchestrator。[1][2][5] 两个层级都需要，但不应共用同一个总分取代诊断。

## 典型结果的解释

| 观测结果 | 传播 | 内化 | 有害行为 | 合理解释 |
|---|---:|---:|---:|---|
| Agent B 原样转发载荷，但延迟 probes 无变化 | 是 | 无证据 | 否 | 机械传播 |
| Agent B 不转发，但 washout 后在新任务中保持立场变化 | 否 | 是 | 未知 | 私有内化 |
| Agent B 执行恶意 tool call，事后 probes 无稳定变化 | 不一定 | 无证据 | 是 | 指令服从或控制流劫持 |
| 立场 probes 改变，同时发生越权行为 | 不一定 | 是 | 是 | 内化与行为共现，但仍需因果检验 |
| 文件中存在载荷，未观察到下游再传输 | 未证实 | 未知 | 否 | 持久化，不等于传播 |
| 单个 agent 拒绝，但系统改派其他 agent 后执行 | 可能 | 无证据 | 是 | 局部拒绝未阻断系统级伤害 |

## 评分器与验证器的隔离

LLM-as-a-Judge 适合评价开放式、主观或语义性结果，但本身可能存在偏差、不一致和对抗脆弱性。[9] 已有 agent safety 工作使用 R-Judge 等数据集评估 judge 对交互风险的识别能力，但数据量和安全边界仍有限。[6]

因此应采用分层证据：

1. 环境状态与工具记录由确定性验证器判定；
2. 传播语义保真度由专用评分器判定；
3. 意识形态变化由独立、盲化的 probe battery 判定；
4. 模糊案例由人类复核；
5. 对 LLM judge 单独进行 meta-evaluation、对抗测试和定期校准。

自动评分结果应通过真实 traces 与人工判断抽查校准。[5] 不应让同一个可能受载荷影响的 agent 同时参与传播、执行和最终裁决；否则 judge 本身可能成为传播链的一部分。来源分析、structured queries 和隔离规划可以帮助验证 proposed action 是否真正受用户意图支持。[8]

## 证据矛盾与研究空白

### 实验传播不等于自然传播率

Prompt Infection 实验表明，自复制载荷在若干场景中比非复制攻击更容易跨 agent 传播，并可能导致数据盗取、恶意行动和系统中断。[13] 实务演示也展示了隐藏指令在 agentic workflow 中持续进入后续上下文的可能性。[12]

这些结果证明传播“可以发生”，但不能直接估计真实部署中的发生率。线性链、动态网络、共享 memory、公开社交环境和生产 orchestrator 具有不同的暴露机会与信任结构；不同研究若没有统一的送达、再生产和多跳成功定义，其传播率不能直接比较。

### belief consistency 不等于正确或安全的内化

ADMA 将抵抗反驳和保持初始立场视为 belief consistency 的改善目标。[3] 对本主题而言，相同现象也可能意味着有害意识形态更难被纠正。现有研究尚缺少同时区分“稳定性”“事实正确性”“规范安全性”和“外部诱导内化”的统一测量框架。

### 安全 benchmark 偏重最终攻击成功

现有 benchmark 大多以 ASR、RR、Harm Score 或 task success 为中心。[6][7] 这些指标适合测量最终结果，却通常无法说明攻击是否跨 agent 传播、是否改变了稳定信念，或只是利用了 [[agentic-harness|Agentic Harness]] 中的控制流和权限配置。

### Judge 可能污染结论

如果传播和内化都由同一个 LLM judge 判断，judge 的提示敏感性可能制造虚假相关。有关 LLM-as-a-Judge 的综述指出，目前仍缺少标准化、安全且稳健的 meta-evaluation 方法。[9] 对 judge 的校准误差、攻击易感性和跨模型可重复性应作为单独结果报告。

### 缺少纵向和反事实证据

现有材料对延迟效应、context reset 后的内化、无传播机会时的态度变化，以及无意识形态内容时的机械有害服从覆盖不足。缺少这些反事实条件时，无法识别“传播导致内化”“内化导致伤害”或“控制流直接导致伤害”的因果路径。

## 最低报告标准

相关研究至少应公开：

- seed、暴露、传播和感染的操作定义；
- agent、message、edge、hop、episode 与 system-level 的统计单位；
- baseline、neutral canary 和未暴露对照；
- context reset、memory 与权限配置；
- 三类指标及其独立判定程序；
- 每个条件的重复次数和置信区间；
- payload 的精确与语义保真度；
- 实际执行结果、RR 与 guardrail 介入记录；
- judge 的版本、rubric、盲化和 meta-evaluation 结果；
- 失败样本、传播中断位置和不可判定案例。

本框架也可用于重新解释 [[sources/2608.10218v1|Mind Viruses: Self-Propagating Ideas in Multi-Agent LLM Systems]]：文件或消息中的持续存在属于保留证据，跨 hop 再生产属于传播证据，probing 的延迟稳定变化属于内化证据，而工具或环境状态变化才属于行为后果。

## 值得补充的资料

后续应优先寻找：

- 将传播、belief change 和行为后果置于同一实验但分别标注的数据集；
- 社会科学中关于态度内化、measurement invariance 和反应偏差的量表研究；
- 网络扩散实验中区分 exposure、adoption 与 retransmission 的方法；
- 使用 neutral canary 估计纯机械传播的多智能体 benchmark；
- context reset 后进行延迟复测的纵向实验；
- 对 propagation judge 和 ideology judge 进行独立 meta-evaluation 的数据集；
- 带 provenance、权限和完整环境状态的生产级 agent traces；
- 能验证传播路径与最终伤害之间中介效应的因果研究。

## 参考资料

[1] *LLM evaluation: methods, metrics, RAG & agent evals guide*，Arize。  
[2] *Agent Evaluation: A Detailed Guide*，Deep (Learning) Focus。  
[3] *Enhancing belief consistency of large language model agents in decision-making process based on attribution theory*。  
[4] *AI Agent Behavioral Science*。  
[5] *LLM Agent Evaluation Metrics in 2026: Tool Calling ...*，Confident AI。  
[6] *Human-Level Safety and Security Evaluation for LLM Agents*。  
[7] *SEC-bench: Automated Benchmarking of LLM Agents on Real-World Software Security Tasks*。  
[8] *awesome-agent-skills-security*，LLMSecurity。  
[9] *Security in LLM-as-a-Judge: A Comprehensive SoK*。  
[10] *Evaluation and Benchmarking of LLM Agents: A Survey*。  
[11] *How to Detect Prompt Injection in Multi-Agent Systems (LangGraph Example)*。  
[12] *Exploiting Agentic Workflows: Prompt Injections in Multi-Agent AI Systems*。  
[13] *Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems*。  
[14] *Prompt Injection in Multi-Agent Systems*，Arthur。  
[15] *From prompt injections to protocol exploits: Threats in LLM-...*。

## References

1. [LLM evaluation: methods, metrics, RAG & agent evals guide | Arize](https://arize.com/resources/llm-evaluation) — arize.com
2. [Agent Evaluation: A Detailed Guide - Deep (Learning) Focus](https://cameronrwolfe.substack.com/p/agent-evals) — cameronrwolfe.substack.com
3. [Enhancing belief consistency of large language model agents in decision-making process based on attribution theory](https://www.sciencedirect.com/science/article/abs/pii/S0957417425028891) — sciencedirect.com
4. [AI Agent Behavioral Science](https://arxiv.org/html/2506.06366v1) — arxiv.org
5. [LLM Agent Evaluation Metrics in 2026: Tool Calling ... - Confident AI](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide) — confident-ai.com
6. [Human-Level Safety and Security Evaluation for LLM Agents](https://proceedings.neurips.cc/paper_files/paper/2025/file/3dc85735f6e2fcf093e67b134fa00d21-Paper-Conference.pdf) — proceedings.neurips.cc
7. [SEC-bench: Automated Benchmarking of LLM Agents on Real-World Software Security Tasks](https://arxiv.org/html/2506.11791v2) — arxiv.org
8. [GitHub - LLMSecurity/awesome-agent-skills-security: 🛡️ A curated list of resources on agent skills security: attacks, defenses, frameworks, and benchmarks for securing AI agent tool use and skill ecosystems · GitHub](https://github.com/LLMSecurity/awesome-agent-skills-security) — github.com
9. [Security in LLM-as-a-Judge: A Comprehensive SoK](https://arxiv.org/html/2603.29403v1) — arxiv.org
10. [Evaluation and Benchmarking of LLM Agents: A Survey - arXiv](https://arxiv.org/html/2507.21504v1) — arxiv.org
11. [How to Detect Prompt Injection in Multi-Agent Systems (LangGraph Example) - DEV Community](https://dev.to/mohithkarthikeya/how-to-detect-prompt-injection-in-multi-agent-systems-langgraph-example-40p) — dev.to
12. [Exploiting Agentic Workflows: Prompt Injections in Multi-Agent AI Systems](https://splx.ai/blog/exploiting-agentic-workflows-prompt-injections-in-multi-agent-ai-systems) — splx.ai
13. [Prompt Infection: LLM-to-LLM Prompt Injection within Multi-Agent Systems](https://arxiv.org/html/2410.07283v1) — arxiv.org
14. [Prompt Injection in Multi-Agent Systems | Arthur](https://www.arthur.ai/column/prompt-injection-multi-agent-systems) — arthur.ai
15. [From prompt injections to protocol exploits: Threats in LLM- ...](https://www.sciencedirect.com/science/article/pii/S2405959525001997) — sciencedirect.com
