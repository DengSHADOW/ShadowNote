---
type: concept
status: draft
title: 可靠解决转化
created: 2026-09-14
updated: 2026-09-14
tags: [reliability, SWE-bench, runtime-feedback]
related: [2607.16387v2, AdaMAST, phase-specific-taxonomy]
source_id: p-72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
content_version: sha256:72218053d1dace574e4fd257fbfb4ea63b165dd9d324f1d079ee6fac03c05f6e
sources: ["raw/sources/2607.16387v2.pdf"]
---

# 可靠解决转化

可靠解决转化描述这样一种收益：Base 偶尔成功的实例在 AdaMAST 下变成稳定成功，但不一定由此扩展出一组从根本上全新的可解实例。

在 Claude Code/SWE-bench 中，AdaMAST 在三个随机种子下都解决了 28 个实例，而 Base 为 27 个。不存在某个实例在所有 AdaMAST 种子下都能解决、却在所有 Base 种子下均不能解决的情况。因此，这一观察限制了将运行时收益解释为能力边界扩展的说法（PDF p. 37）。
