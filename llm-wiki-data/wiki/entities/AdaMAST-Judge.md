---
type: entity
status: draft
title: AdaMAST-Judge
created: 2026-09-14
updated: 2026-09-14
tags: [trajectory-selection, verifier, agents]
related: [2607.16387v2, AdaMAST, actionable-verification-criterion, taxonomy-conditioned-consumer]
source_id: p-72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
content_version: sha256:72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
sources: ["raw/sources/2607.16387v2.pdf"]
---
# AdaMAST-Judge

AdaMAST-Judge 是 AdaMAST 中用于 best-of-N 轨迹选择的消费组件。它把失败模式转化为[[concepts/actionable-verification-criterion|可操作的验证标准]]，并结合选择器与验证器机制使用。

在 Terminal-Bench 2.0 上，论文报告的 best-of-5 准确率分别为：terminus-2 `73.0%`、claude-code `72.4%`、ForgeCode `89.9%`。这些结果不能只归因于分类体系质量，因为学习得到的选择器和验证器同样是系统的一部分（PDF pp. 1、17）。
