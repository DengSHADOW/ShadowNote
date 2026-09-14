---
type: concept
status: draft
title: 反馈注入位置
created: 2026-09-14
updated: 2026-09-14
tags: [prompting, ablation, feedback]
related: [2607.16387v2, AdaMAST, taxonomy-conditioned-consumer]
source_id: p-72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
content_version: sha256:72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
sources: ["raw/sources/2607.16387v2.pdf"]
---

# 反馈注入位置

反馈注入位置，是将分类体系产生的诊断结果加入变异提示词或评估过程的位置。

在 TheoremQA 中，将诊断附加到评估结果时准确率达到 `63.3%`，而内联代码注释为 `53.3%`，系统消息为 `46.7%`。在另一个小规模诊断实验中，自然语言摘要的搜索后平均准确率为 `61.1%`，结构化 AdaMAST 代码和原始轨迹摘录均为 `56.7%`。作者将其解释为“格式无显著影响”的结果，而不是自然语言表述普遍更优（PDF p. 37）。
