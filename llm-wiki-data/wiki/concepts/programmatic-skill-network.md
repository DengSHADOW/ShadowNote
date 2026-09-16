---
type: concept
status: draft
title: 程序化技能网络（PSN）
created: 2026-09-13
updated: 2026-09-15
tags: [agents, skills, programs, planning]
related: [trace-guided-skill-repair, reliability-aware-skill-updating, validated-structural-refactoring]
source_id: p-3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
content_version: sha256:3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
sources: ["zotero://users/0/items/5RKUKLBV"]
---

# 程序化技能网络（PSN）

> 来源：[[zotero-users-0-5RKUKLBV|Evolving Programmatic Skill Networks]]；PDF pp. 2–3，Sections 2–3。

PSN 将一个技能表示为带控制流、参数、前置/后置条件和子技能调用的可执行程序；网络的节点是技能，边是实际调用关系。规划优先用后置条件做 backward chaining；当已有网络不能覆盖子目标时，才调用 LLM 做 forward planning，并把成功计划蒸馏成新技能。

**英文对应表述（非逐字原文）**：A PSN skill is an executable program with control flow, parameters, pre/postconditions, and invoked children. Planning first backward-chains through effects and falls back to LLM forward planning when the network cannot reduce a subgoal.（PDF pp. 2–3，Sections 2.1–2.3）

这个概念强调“技能”的可执行与可诊断性：它不是本项目的 `SKILL.md` 指令文件，也不等于仅靠向量相似度检索到的一段文本。

**英文对应表述（非逐字原文）**：In this paper, a skill is executable JavaScript or Python connected by invocation edges, not an instruction document or a retrieved text fragment.（PDF pp. 1–3）

证据边界：Figure 6 和 Figure 9 显示 PSN 的技能库更紧凑并形成更多复用节点，但这来自完整系统对照，不是单独隔离“网络表示”的实验；所谓 compositional generalization 也没有在独立 held-out 组合分布上检验。

**英文对应表述（非逐字原文）**：Library-size and fan-in results support reuse under the evaluated curriculum, but they do not isolate network representation or test a separately sampled held-out compositional distribution.（PDF pp. 9–13，Figures 6 and 9）

关联：[[trace-guided-skill-repair|执行轨迹引导的技能修复]]、[[reliability-aware-skill-updating|可靠性门控的技能更新]]。
