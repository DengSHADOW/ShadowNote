---
name: wiki-maintenance
description: 维护本项目 LLM Wiki 的来源页、概念页、图谱链接与结构；明确入库时才写入，知识问答默认不落盘。
---

先读 llm-wiki-data/wiki/index.md，再按当前问题读取相关来源页、概念页和原始 PDF；不要全量加载 Wiki。格式和所有权以 docs/architecture.md 为准。

- **ingest**：只在用户明确要求入库或更新 Wiki 时执行。先读目标页和直接图谱邻居，保留用户手改、条件、分歧和来源。首次单篇阅读默认只创建或更新 wiki/sources/ 中的一篇来源页；不因关键词相同自动创建共享概念或跨论文关系。
- **Zotero ingest**：用户指定 collection 或 item 时，先运行 zotero-wiki-plan --collection KEY --wiki-root llm-wiki-data --prepare（单篇用 --items KEY）。只处理输出中 ready 的项目，从本地 Zotero PDF 或 prepared cache 回查原文；脚本不复制 PDF、不会生成摘要。
- **页面结构**：来源、概念、实体、比较、综合和保存的问题分别放在 wiki/sources/、concepts/、entities/、comparisons/、synthesis/、queries/。内容页使用 type、title、source_id、content_version、sources frontmatter；链接使用可解析的 [[folder/page|label]] 或唯一名称。每个内容页从 wiki/index.md 链接。
- **query**：默认只在聊天回答。回答时区分作者 claim、原文证据、分析推断和用户想法；重要数字、比较和批评回查 PDF。用户明确要求保存时才创建 query、comparison 或 synthesis 页面。
- **lint**：修改后运行 lint-llm-wiki --wiki-root .\llm-wiki-data；它检查来源版本、wikilink 和索引，不能判定科学结论正确。对结构或语义修复先读现有页，保留人工编辑。

重要 claim、数字和批评要定位到 source_id、content_version、PDF 页序号及章节或图表。状态默认 draft；只有用户实际确认才设置 reviewed。生成来源页后，可运行该来源的 llm-wiki-review-context 检查直接图谱上下文。
