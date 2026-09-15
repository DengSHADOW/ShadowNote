---
type: concept
status: draft
title: 可靠性门控的技能更新
created: 2026-09-13
updated: 2026-09-13
tags: [agents, skills, reliability, continual-learning]
related: [programmatic-skill-network, trace-guided-skill-repair]
source_id: p-3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
content_version: sha256:3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
sources: ["zotero://users/0/items/5RKUKLBV"]
---

# 可靠性门控的技能更新

> 来源：[[zotero-users-0-5RKUKLBV|Evolving Programmatic Skill Networks]]；PDF p. 4，Eq. 6。

论文以技能成功率的平滑估计和不确定性构造成熟度 (V(s))，再用带 ε 下限的 sigmoid 决定是否更新。可靠技能会较少被改动，但不会被冻结；最近五次修复建议还被用作缓冲区，以抑制互相矛盾的编辑。

这是保护已有效组件的启发式策略，不能理解为对更新安全性或稳定性的数学证明。

关联：[[programmatic-skill-network|程序化技能网络（PSN）]]、[[trace-guided-skill-repair|执行轨迹引导的技能修复]]。
