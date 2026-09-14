---
type: concept
status: draft
title: 失败压缩
created: 2026-09-14
updated: 2026-09-14
tags: [compression, execution-traces, failure-codes]
related: [2607.16387v2, AdaMAST, adaptive-failure-taxonomy]
source_id: p-72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
content_version: sha256:72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
sources: ["raw/sources/2607.16387v2.pdf"]
---

# 失败压缩

失败压缩使用少量已触发的失败代码和签名，表示一个较大的执行轨迹池。

对于 223 条 SWE-bench 运行时轨迹，作者报告了约 `18×` 的压缩率；每条轨迹触发代码数的中位数为 5，且 89% 的代码签名是唯一的。该测量证明了表示的紧凑性，但本身不能证明它对修复或任务成功具有因果作用（PDF p. 1）。
