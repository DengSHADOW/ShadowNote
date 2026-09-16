---
type: concept
title: virus chain
created: 2026-09-15
updated: 2026-09-15
tags: [multi-agent-systems, experiment, persistent-memory, propagation]
related: [mind-virus, SOUL-md, 防御提示, 验证驱动传播链]
source_id: p-377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
content_version: sha256:377e957a7fd25aefc56f62e702d6bf257d236814276e074e8e49cefd95121be0
sources: ["raw/sources/2608.10218v1.pdf"]
---
# virus chain

virus chain 是一种成对、短时的智能体交互实验：每个 hop 后清除感染者的对话上下文，仅保留 sandbox 文件，并将感染者重新分配给下一批目标。因此，跨 hop 存活依赖可持久化工件而非对话历史。（PDF p.9–11；p.31，§B.2–B.3）

> **英文对应表述（非逐字原文）：** Virus chains reset conversational context between pairwise interactions, retaining sandbox files as the channel for cross-hop persistence.

其演化程序以 2-hop、batch size 3 的最佳 chain 计算 fitness，初始种群为 $B=9$，每代保留 $E=3$ 个 elite 并各生成 3 个 mutation，通常最多运行 14 代。该选择目标偏向最佳个例而非平均表现，可能高估偶然成功。（PDF p.31–32，§B.4）

> **英文对应表述（非逐字原文）：** The evolutionary procedure selects on the best two-hop chain rather than average performance, which can favor chance successes.

## 图谱关系

- 来源：[[2608.10218v1|Mind Viruses]]
- 载荷与持久化：[[mind-virus|mind virus]]、[[SOUL-md|SOUL.md]]
- 传播验证：[[验证驱动传播链]]
