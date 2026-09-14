# 给另一台电脑 Codex 的工作指令

复制下面整段发送给该电脑上的 Codex：

~~~
你正在维护 ShadowNote。先完整阅读 AGENTS.md、docs/status.md、docs/requirements.md、docs/architecture.md、docs/cross-device-handoff.md 和本文件；然后检查当前目录、Git 状态、Windows/WSL 环境与依赖。不要假定历史实现仍存在。

本项目只有一个知识库：llm-wiki-data/wiki/。LLM Wiki 是 Markdown、搜索和图谱界面；Zotero 是论文和 PDF 的权威库。不要创建 vault、Obsidian 副本或第二套 Wiki。

先执行：
1. Windows：& .venv\Scripts\python.exe scripts\paper_wiki.py doctor
2. Windows：& .venv\Scripts\python.exe -m unittest discover -s tests -v
3. Windows：& .venv\Scripts\python.exe scripts\paper_wiki.py lint-llm-wiki --wiki-root .\llm-wiki-data
Linux 使用 .venv/bin/python。缺少依赖时说明并继续不受影响的只读检查。

知识任务先读 llm-wiki-data/wiki/index.md，再只读相关来源页和原 PDF；不要全量加载 Wiki。精读、claims 或图表任务先读 .agents/skills/paper-analysis/SKILL.md；英文课堂 review 先读 .agents/skills/paper-review/SKILL.md；入库、query 或图谱维护先读 .agents/skills/wiki-maintenance/SKILL.md。

用户指定 Zotero collection 或 item 时，先运行 zotero-wiki-plan 得到明确范围。工具只允许本地 Zotero API GET：不修改 SQLite，不用云 API，不暴露端口，不复制 Zotero PDF。用户说“当前选中论文”时，先运行 zotero-selected；多选、无选中或无本地 PDF 时不要猜测目标。

Codex 负责阅读、论证和写作；脚本只处理确定性工作，绝不生成假摘要。重要 claim、数字、公式、图表结论和批评必须回查原 PDF，并写明 source_id、content_version、PDF 页序号以及章节或图表。Wiki 提供上下文，不能替代原文证据。写 review 前使用 llm-wiki-review-context 获取相关 Wiki 页和原 PDF。

修改 Wiki 前先读目标文件，保留用户手改；默认 draft，绝不自行标记 reviewed。内容页使用 type、title、source_id、content_version、sources frontmatter，修改后运行 lint-llm-wiki。首次单篇阅读只写来源页，除非用户明确要求，不创建共享概念页或跨论文关系。

不要自动 git add、commit、push、发布或创建远程仓库。不要将 PDF、缓存、密钥、LLM Wiki 本机状态或 Zotero 本机路径提交到 Git。代码或结构规则改动后运行相关测试，把真实结果和缺失依赖更新到 docs/status.md。
~~~

该指令假定另一台电脑已自行安装 LLM Wiki、Python 和 Zotero，并在 LLM Wiki 中打开仓库内的 llm-wiki-data/。
