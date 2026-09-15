---
type: concept
status: draft
title: 程序化技能网络（PSN）
created: 2026-09-13
updated: 2026-09-13
tags: [agents, skills, programs, planning]
related: [trace-guided-skill-repair, reliability-aware-skill-updating, validated-structural-refactoring]
source_id: p-3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
content_version: sha256:3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
sources: ["zotero://users/0/items/5RKUKLBV"]
---

# 程序化技能网络（PSN）

> 来源：[[zotero-users-0-5RKUKLBV|Evolving Programmatic Skill Networks]]；PDF pp. 2–3，Sections 2–3。

PSN 将一个技能表示为带控制流、参数、前置/后置条件和子技能调用的可执行程序；网络的节点是技能，边是实际调用关系。规划优先用后置条件做 backward chaining；当已有网络不能覆盖子目标时，才调用 LLM 做 forward planning，并把成功计划蒸馏成新技能。

这个概念强调“技能”的可执行与可诊断性：它不是本项目的 `SKILL.md` 指令文件，也不等于仅靠向量相似度检索到的一段文本。

关联：[[trace-guided-skill-repair|执行轨迹引导的技能修复]]、[[reliability-aware-skill-updating|可靠性门控的技能更新]]。
