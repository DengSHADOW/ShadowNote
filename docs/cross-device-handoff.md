# 跨电脑交接

可提交并同步的是 llm-wiki-data/wiki/、purpose.md、schema.md、sources/metadata/、代码、文档、Skills 和 reviews/。PDF、缓存、模型密钥、LLM Wiki 本机状态和 Zotero 本机路径不进入 Git。

在另一台 Windows 电脑上：

1. 克隆或拉取仓库，创建 .venv，并按 requirements.lock.txt 安装依赖。
2. 单独安装 LLM Wiki，在应用中打开仓库里的 llm-wiki-data/。
3. 单独登录模型提供商；密钥不写入仓库。
4. 登录 Zotero 并等待条目和需要的附件下载完成。运行 zotero-wiki-plan 重新登记这台电脑的本地附件路径；无需重新生成已同步的 Wiki Markdown。
5. 运行 Python 测试和 lint-llm-wiki --wiki-root .\llm-wiki-data。

日常同步时先拉取，再在 LLM Wiki 完成写入后检查 Git diff。两台电脑不要同时编辑同一 Markdown；发生冲突时以人工合并保留用户编辑。当前只有 llm-wiki-data/wiki/ 一份知识库，没有 vault 兼容目录。

桌面应用需要由用户实际确认能建立索引、搜索和图谱；其本地 Codex CLI 子进程是只读的，不能代替本项目的工作区写入流程。
