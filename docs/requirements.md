# 长期需求

更新：2026-09-13。

- LLM Wiki 是唯一的知识库界面和 Markdown 图谱：项目根是 llm-wiki-data/，可由 LLM Wiki、Codex 或普通编辑器直接编辑。Obsidian 不属于工作流。
- Zotero 是论文库和 PDF 的权威位置。工具只用本地 Zotero API GET，不修改 SQLite、不调用云 API、不复制 Zotero PDF。
- Codex 负责科学阅读、解释与写作；确定性脚本只处理来源登记、逐页提取、PDF 校验、Zotero 解析、图谱上下文和结构 lint，绝不生成假摘要。
- 用户明确要求精读、入库或 review 才写文件。默认首次阅读只写单篇来源页；共同关键词不自动产生概念页或跨论文边。
- 所有重要 claim、数字、公式解释、图表结论和批评要记录 source_id、content_version、PDF 页序号与章节或图表。Wiki 只能提供上下文，review 必须回查原 PDF。
- 保留用户的 Markdown 手改。状态默认 draft；只有用户明确确认时才标记 reviewed。
- Git 同步 wiki/、元数据、代码、文档、Skills 和 reviews；不提交 PDF、缓存、密钥、LLM Wiki 本机数据库或聊天状态。
- 不自动提交、推送、发布或创建远程仓库。

历史的初始交接与过往状态保留在 docs/archive/，不再作为执行规范。
