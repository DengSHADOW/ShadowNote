# ShadowNote

这是一个本地、可追溯的论文阅读工作流：Zotero 保存文献和 PDF，LLM Wiki 管理可编辑 Markdown、搜索和图谱，Codex 读取原文并写分析或英文课堂 review。Python 命令只做本地导入、PDF 文本准备、来源解析和结构校验；它们不生成论文摘要。

知识库只有一份：llm-wiki-data/wiki/。LLM Wiki、Codex 和普通文本编辑器都编辑同一批 Markdown。PDF 不进入 Git：Zotero PDF 留在 Zotero，本地手动导入的 PDF 位于被忽略的 llm-wiki-data/raw/sources/。

## 日常使用

1. 在 LLM Wiki 中打开现有项目目录 D:\ShadowNote\llm-wiki-data。
2. 在 Zotero 下载需要阅读的附件。另一台电脑上的 Zotero 同步条目不代表 PDF 已下载。
3. 指定一个 collection 或 item 给 Codex。项目会只读查询 Zotero Local API，登记来源而不复制 PDF：

~~~
& .venv\Scripts\python.exe scripts\paper_wiki.py zotero-wiki-plan --collection COLLECTION_KEY --wiki-root .\llm-wiki-data --prepare
~~~

4. 让 Codex 按明确范围快速阅读、正式精读、入库或写 review。重要 claim、数字和批评都会回查原 PDF。
5. 在 LLM Wiki 中编辑、搜索或浏览图谱；完成后检查结构：

~~~
& .venv\Scripts\python.exe scripts\paper_wiki.py lint-llm-wiki --wiki-root .\llm-wiki-data
~~~

若要为课堂 review 取得只读 Wiki 上下文并验证原 PDF：

~~~
& .venv\Scripts\python.exe scripts\paper_wiki.py llm-wiki-review-context --wiki-root .\llm-wiki-data --source 'zotero://users/0/items/ITEMKEY'
~~~

## 本机准备与检查

Windows：

~~~
py -m venv .venv
& .venv\Scripts\python.exe -m pip install -r requirements.lock.txt
& .venv\Scripts\python.exe scripts\paper_wiki.py doctor
& .venv\Scripts\python.exe -m unittest discover -s tests -v
node --test tests/zotero_selection.test.cjs
~~~

Zotero 的“当前选中论文”桥是可选的本地扩展；安装、构建和限制见 docs/zotero-selection.md。没有安装时，直接指定 collection 或 item 即可。

## 同步

提交 Markdown、来源元数据、代码、文档和 Skills；忽略 PDF、缓存、模型密钥、LLM Wiki 本机状态与构建产物。两台电脑分别安装 LLM Wiki、登录模型和 Zotero；随后打开同一仓库中的 llm-wiki-data。详细恢复步骤见 docs/cross-device-handoff.md。

更多约定：docs/requirements.md、docs/architecture.md、docs/status.md。历史交接文档在 docs/archive/。
