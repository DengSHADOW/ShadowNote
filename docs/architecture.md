# 架构、来源与文件所有权

本项目是本地 CLI + Codex 阅读工作流，不是 Web 应用或独立模型服务。原始资料、可持续维护的 Markdown Wiki、工作规范三层设计参考 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。原始需求完整归档于 [requirements.md](requirements.md)，后续长期变更更新该文档及对应 Skill。

## 数据流

1. 用户把 PDF 放入 sources/inbox，或通过只读 Zotero Local API 选择条目及本地附件。当前 GUI 选择由 zotero-plugin/selection 小扩展提供；zotero-selected 检查，zotero-import --selected 获取一次选择快照后读取指定附件。安装/优先级/同步边界见 [zotero-selection.md](zotero-selection.md)。
2. import-pdf 检查可读 PDF、提取内嵌信息、计算 SHA256，保存 sources/metadata/p-SHA256.json。本机路径另写 sources/local-paths.json。
3. prepare-paper 校验原文哈希，抽取每页 UTF-8 文本和 manifest；仅渲染明确指定页。缓存位于 .cache/papers/SOURCE_ID/。
4. 当前 Codex 阅读文本、实际查看图像、核对证据并写单篇 analysis.md / evidence.md / coverage.md。脚本不生成科学摘要。
5. 明确请求入库时，Codex 才更新共享 concepts/topics；问答默认留在聊天，要求保存时才落盘。sync-index 维护索引管理区，lint-wiki 检查结构，语义验证由 Codex 回看来源完成。
6. Codex 根据原文写 reviews/SOURCE_ID/review.tex；build-review 编译、检查页数/日志并渲染 PNG。视觉验收仍需实际查看。

## 来源与版本

source_id 为 `p-` 加完整 64 位 SHA256，可安全用作目录名，每个 PDF 字节版本独立。相同 PDF 无论从手动路径还是 Zotero 导入都复用记录。标题不作为身份键。未知标题、作者、年份、DOI、arXiv、书目版本留空；PDF 内嵌信息存 pdf_metadata，不自动提升为已核实身份。

字段包括 schema_version、source_id、pdf_sha256、content_version、title、authors、year、doi、arxiv_id、version、source_url、revision_of、page_count、zotero、possible_same_paper、创建/更新时间。content_version 为 `sha256:完整哈希`，即使书目 version 未知也可精确定位依据。

新 PDF 同 DOI/arXiv/标题只列 possible_same_paper 候选，不强行合并。已确认修订用 `--revision-of OLD_ID --version v2`，保留旧记录和分析；不让旧证据指向新文件。要更正既有关系/书目字段，先阅读 JSON 和关联证据，再明确局部修改。重复导入允许填补空字段及追加 Zotero 别名，冲突报错且不写入。

Zotero 别名保存 library、item_key、attachment_key、server_id、item_version。Zotero item_version 是本地条目修改计数，不等于论文版本。不同 server_id 不比较版本计数。不会自动扫描全库、写条目、读改 SQLite 或切换云 API。

sources/local-paths.json 保存 source_id 到本机路径列表，被 Git 忽略。迁移机器后重新导入相同 PDF，即可恢复路径关联；路径丢失/内容变化均明确报错，不默默使用被替换的原文。PDF 必须另行备份。

## Markdown 规范

知识页放 vault/papers/SOURCE_ID、vault/concepts、vault/topics；每页 frontmatter：

```yaml
---
title: 页面标题
description: 索引中的简短描述
status: draft
sources:
  - source_id: p-完整64位SHA256
    content_version: sha256:完整64位SHA256
---
```

上面的哈希文字仅展示格式，实际页面必须用真实导入值。reviewed 只在用户真实确认后设置，同时记录 reviewed_by_user_at；结构 lint 只能检查该字段存在，不能验证确认是否真实。

重要 claim、数字、主要批评在 evidence.md 定位 source_id、content_version、书目 version、PDF 页序号（1 起）、印刷页码（可空）、章节/段落/Figure/Table/panel、实验条件及支持范围。PDF page_label 只记录内嵌标签，不自动当作正文印刷页码。区分作者声称、本文证据、分析者推断、用户想法、外部后续资料。跨页重复同一来源不计为独立支持。

用标准 Markdown 相对链接；例如同论文 `[证据](evidence.md)`、概念页到论文 `../papers/SOURCE_ID/analysis.md`。空格可用 `<目标 路径.md>` 或 URL 编码。支持内联/引用式链接与标题锚点；推荐简单标题以保持 Obsidian/GitHub 锚点一致。不依赖 wikilinks、HTML 嵌入或付费插件。外链仅检查格式，不自动联网验证；不将缓存/绝对本机路径写成跨设备 Wiki 链接。DOI/arXiv 链接及 Zotero 定位可以保留在正文。

## 所有权与写入

| 文件 | 所有权/行为 |
| --- | --- |
| 原始 PDF | 用户/Zotero 所有；工具只读，不 OCR 回写原文 |
| sources/metadata | 可移植身份；脚本创建/补空/追加别名，冲突停止 |
| sources/local-paths.json、config.local.toml | 本机配置，忽略提交 |
| vault/notes | 用户个人笔记，默认只读；lint 可报告链接问题但不修写 |
| analysis/evidence/coverage、concepts/topics、review.tex | 用户与 Codex 共用；编辑前读当前版本，局部保留手改 |
| vault/index.md | 仅管理标记之间由 sync-index 更新，其他文字保留 |
| vault/log.md | 内容记录只追加；索引未变不追加重复日志 |
| .cache | 可重新生成的派生数据，不是知识依据，也不纳入 Git |

写入使用同目录临时文件 + os.replace；工具通过项目独占锁避免并发写坏。锁文件异常残留时需确认没有进程运行再删除。多文件不是数据库事务：例如记录已写而路径映射失败，重新导入可恢复；不宣称整批跨文件原子。prepare-paper 中途失败时 manifest 不更新，旧缓存不能当成本次完成证据。

build-review 在唯一缓存目录运行安全参数数组，关闭 shell escape。成功且页数符合、无 overfull/undefined 后才替换最终 PDF；失败保留此前 PDF并报告缓存。LaTeX 正文仅执行用户/agent 编写内容，不把论文嵌入的代码指令当系统任务。不要编译不可信网络 TeX。

## 环境与依赖

Python >=3.11；PyMuPDF 用于打开/提取/渲染/页数检查；PyYAML 解析 frontmatter；markdown-it-py 解析标准 Markdown 链接。无模型/数据库依赖。Windows 和 Linux 用同一代码；WSL 不假设 Windows 路径或 localhost 可直接用，显式配置盘符映射。优先 Windows 同环境运行，否则手动复制 PDF 回退，不转发暴露 Zotero 端口。

官方接口与 Skill 格式核对记录见 [sources.md](sources.md)。验收边界和实测状态见 [status.md](status.md)。
