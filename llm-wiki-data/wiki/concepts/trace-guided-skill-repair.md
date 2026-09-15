---
type: concept
status: draft
title: 执行轨迹引导的技能修复
created: 2026-09-13
updated: 2026-09-13
tags: [agents, skills, debugging, execution-traces]
related: [programmatic-skill-network, reliability-aware-skill-updating, validated-structural-refactoring]
source_id: p-3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
content_version: sha256:3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72
sources: ["zotero://users/0/items/5RKUKLBV"]
---

# 执行轨迹引导的技能修复

> 来源：[[zotero-users-0-5RKUKLBV|Evolving Programmatic Skill Networks]]；PDF pp. 3–4，19–21，Algorithm 1。

PSN 在失败后只沿本次实际执行过的技能子图定位责任，不对未执行节点作推断。修复分两阶段：先从失败根技能向下传播结构化反馈，但不改代码；再按依赖后序由叶到根应用 patch，并将子技能修改报告回传给父技能。

论文把这类离散的修改建议称为 symbolic gradient。它不是可微数值梯度，也没有收敛或最优性保证。

关联：[[programmatic-skill-network|程序化技能网络（PSN）]]、[[validated-structural-refactoring|可验证的结构重构]]。
