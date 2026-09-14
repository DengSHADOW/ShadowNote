# LLM Wiki 集成

在 LLM Wiki 中选择“打开已有项目”，项目目录必须是仓库内的 llm-wiki-data/，不能是仓库根目录。这样应用只接触 wiki、可选 raw/sources 和自己的本机状态，不会编辑代码、文档或 reviews。

LLM Wiki 生成和编辑的是 wiki/ 中可提交的 Markdown。raw/sources/、media/、.llm-wiki/ 和应用缓存只在本机保留。应用不会自动提交或推送 Git。

Codex 与应用可编辑同一批 Markdown，但不要并发修改同一页。使用 Codex 写入前先阅读该页、保留手改，写入后运行 lint-llm-wiki --wiki-root .\llm-wiki-data。

若应用使用本地 Codex CLI，它的会话是只读、ephemeral 子进程，不能替代这里的 Codex 工作区写入流程或本地 Zotero 访问。
