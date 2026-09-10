# ShadowNote / Paper Wiki

A notebook use llm wiki to help me research and do paper reviews

这是可以本地运行的论文工作流：Zotero 管理原文，Codex 负责阅读/推理/写作，Python 做导入与校验，Obsidian 和 VS Code 使用同一套 Markdown。第一版无需模型 API、网页服务或向量数据库。

长期需求完整保存于 [docs/requirements.md](docs/requirements.md)，实现规范见 [docs/architecture.md](docs/architecture.md)，**实际验证和剩余事项见 [docs/status.md](docs/status.md)**。根目录的原始交接文件保留不变。

## 当前电脑直接使用

在 PowerShell 中进入 `D:\ShadowNote`。本次已准备项目专用 Python 3.12、依赖和便携 Tectonic，不需要激活环境或修改系统 PATH：

```powershell
Set-Location D:\ShadowNote
& .venv/Scripts/python.exe scripts/paper_wiki.py doctor
& .venv/Scripts/python.exe scripts/paper_wiki.py --help
```

Obsidian 使用“打开文件夹作为仓库 / Open folder as vault”，选择 **`D:\ShadowNote\vault`**。PDF 放入 **`D:\ShadowNote\sources\inbox`**；也可以导入其他本地目录下的文件。脚本只读原始 PDF。

```powershell
# 把下面文件名替换为实际 PDF；引号支持中文和空格。
$paper = & .venv/Scripts/python.exe scripts/paper_wiki.py import-pdf "sources/inbox/论文 文件.pdf" | ConvertFrom-Json
$sourceId = $paper.source_id
& .venv/Scripts/python.exe scripts/paper_wiki.py prepare-paper $sourceId
# 仅在需要查看图表时渲染指定 PDF 页序号，从 1 起。
& .venv/Scripts/python.exe scripts/paper_wiki.py prepare-paper $sourceId --pages "1,3-5"
& .venv/Scripts/python.exe scripts/paper_wiki.py resolve-pdf $sourceId
```

prepare-paper 输出 .cache/papers/SOURCE_ID 路径，包含 page-0001.txt 等逐页文本、manifest.json 和所选页面 PNG。疑似 OCR 页只是启发式标记；本版不自动 OCR，不将未读图表称为核验完成。多栏文字的抽取顺序须与原始版面核对。

可用 `--title`、重复 `--author`、`--year`、`--doi`、`--arxiv-id`、`--version`、`--source-url` 填写已核实身份，未知不填。PDF 内嵌元数据仅保存为候选。相同 PDF 复用 source_id；相同标题不会合并。确认是新版本时：

```powershell
& .venv/Scripts/python.exe scripts/paper_wiki.py import-pdf "sources/inbox/论文 v2.pdf" --revision-of $sourceId --version v2
```

新字节版本保留独立来源记录。版本关系不确定时只列候选。原文文件移动后重新导入相同 PDF 可恢复本机路径；修改过的 PDF 不会静默替换旧依据。

## 新电脑安装与复现

需要 Python >=3.11。已有 Python 时（Windows）：

```powershell
py -3.12 -m venv .venv
& .venv/Scripts/python.exe -m pip install -e .
Copy-Item config.example.toml config.local.toml
& .venv/Scripts/python.exe scripts/paper_wiki.py doctor
```

config.local.toml 已存在时不要覆盖；按需局部调整。Python 缺失可从 [Python Windows 官方下载](https://www.python.org/downloads/windows/)安装，再开终端。若希望与本次一样仅在项目范围准备运行环境，先从 [uv 官方 Windows release](https://github.com/astral-sh/uv/releases)下载 x86_64-pc-windows-msvc.zip 并解压到 .runtime/uv，然后：

```powershell
$env:UV_PYTHON_INSTALL_DIR = "$PWD/.runtime/python"
$env:UV_PYTHON_BIN_DIR = "$PWD/.runtime/bin"
$env:UV_CACHE_DIR = "$PWD/.cache/uv"
& .runtime/uv/uv.exe venv --python 3.12 .venv
& .runtime/uv/uv.exe pip install --python .venv/Scripts/python.exe -e .
```

不要对已有 .venv 重建；上述环境变量仅影响当前 PowerShell。网络受限时需要开放软件包下载或用离线包，不能假称依赖已装好。已运行版本记录在 docs/status.md，固定依赖可使用 `requirements.lock.txt`。

Linux / 已有 WSL Python：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python scripts/paper_wiki.py doctor
```

不同系统各建 .venv，不复用 Windows 虚拟环境。当前电脑未安装 WSL，本项目不要求安装它。

## Zotero 只读接入

已安装 Zotero 10.0.1，但本次真实 Local API 尚不可达。先启动 Zotero，在 **Settings → Advanced → “Allow other applications on this computer to communicate with Zotero”** 开启本机应用通信。这是[官方 Local API 文档](https://www.zotero.org/support/dev/web_api/v3/local_api)确认的设置；关闭时通常返回 403。配置默认是 http://localhost:23119/api/、users/0，均可在 config.local.toml 更改。不要填写云 API 密钥。

```powershell
& .venv/Scripts/python.exe scripts/paper_wiki.py doctor
# 先列出有限数量的 collections；--start 可继续下一页。
& .venv/Scripts/python.exe scripts/paper_wiki.py zotero-list --collections --limit 20
# 将大写 key 替换成上一步或 Zotero 中选定的真实 key。
& .venv/Scripts/python.exe scripts/paper_wiki.py zotero-list --collection ABCD1234 --limit 20
& .venv/Scripts/python.exe scripts/paper_wiki.py zotero-list --items ABCD1234,EFGH5678 --limit 20
& .venv/Scripts/python.exe scripts/paper_wiki.py zotero-import ABCD1234
# 有多个 PDF 时，工具会列出候选并要求明确附件。
& .venv/Scripts/python.exe scripts/paper_wiki.py zotero-import ABCD1234 --attachment IJKL9012
```

工具只发 GET，不一次导入整个文献库，不修改条目/数据库，也不自动切换云 API。附件必须真实存在于本机；file URL 作为本地路径解析，不当作公网下载地址。PDF 尚未同步到本机时先在 Zotero 下载，或使用 import-pdf。

Windows Zotero + WSL Codex 时，优先用 Windows Python 在同环境运行；不能假设 WSL localhost 能访问 Windows。若使用已确认可达的本机私网地址，可显式设置 base_url；**不要转发或暴露 23119 端口**。Windows 附件路径需显式映射，例如：

```toml
[paths.windows_drives]
C = "/mnt/c"
D = "/mnt/d"
```

连接或挂载仍受限时，把需要的一篇 PDF 放到当前环境可读路径，手动导入即可继续阅读。

## 三个 Skills 与四个日常请求

三个仓库 Skills 位于 .agents/skills/，有 name/description frontmatter：
`paper-analysis`、`paper-review`、`wiki-maintenance`。

[官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)支持在 Codex CLI / IDE 中输入 `$` 或使用 `/skills` 选择，也可按请求自动匹配。当前会话已经显式读取三个 Skill；新会话的自动发现尚未验证。若选择器未显示，重启 Codex/开新会话，或明确让 agent 读取对应 SKILL.md；不修改全局 Skills。

把下列示例中的文件名或 SOURCE_ID 换为真实值，直接发给 Codex：

1. **精读一篇**：`$paper-analysis 请精读 sources/inbox/论文.pdf，用中文按原文段落顺序解释，实际查看全部图表，保存 analysis、evidence 和覆盖清单；缺失部分明确记录。`
2. **一页英文 review**：`$paper-review 请基于 SOURCE_ID 的原文和本篇证据写一页英文课堂 review，保持 11pt，保存独立 .tex，实际编译并检查页数、日志和渲染图。`
3. **把论文入 Wiki**：`$wiki-maintenance ingest：将已读 SOURCE_ID 入 Wiki，先读相关已有概念页，保留条件与分歧，更新来源、索引和追加日志，不覆盖我的个人笔记。`
4. **比较并核查来源**：`$wiki-maintenance query：比较已读 SOURCE_ID_A 和 SOURCE_ID_B 的方法假设、实验条件和证据范围，逐条核查原文来源；运行结构 lint，区分已验证事实与推断。此次只在聊天回答。`

首次精读只生成本篇分析；明确要求入库才写共享概念。科学阅读和写作由当前 Codex 执行，脚本不会拼装假摘要。用户笔记默认只读，已有分析/review 的手改需要保留。

## Wiki 检查与 review 编译

```powershell
& .venv/Scripts/python.exe scripts/paper_wiki.py sync-index
& .venv/Scripts/python.exe scripts/paper_wiki.py lint-wiki
& .venv/Scripts/python.exe scripts/paper_wiki.py build-review "reviews/SOURCE_ID/review.tex"
# 本仓库现有的合成排版样例，可立即编译：
& .venv/Scripts/python.exe scripts/paper_wiki.py build-review reviews/synthetic-demo/review.tex
```

sync-index 只改 index.md 管理区，保留用户引言；索引未变化不重复记录日志。Codex 另外追加有语义的内容变更日志。lint 检查标准 Markdown 链接/标题锚点、source_id/内容版本、必需 frontmatter、索引重复/遗漏、孤立页；**不验证科学真实性、外链可达性或 reviewed 确认是否真实**。知识页格式见 architecture.md。返回码：成功 0；lint 结构错误 1；命令/依赖错误 2。doctor 即使部分能力缺失也返回诊断 JSON；以其中 ready/reachable 字段判断。

当前 config.local.toml 指向项目 .runtime/tectonic/tectonic.exe，排版包缓存到 .cache/tectonic。新机器可从 [Tectonic 官方 release](https://github.com/tectonic-typesetting/tectonic/releases)下载对应平台便携版，在 config.local.toml 的 tools.latex 指定路径；首次编译需网络下载排版资源。也支持系统 pdflatex/xelatex/lualatex。

没有编译器时，Windows 可安装 [MiKTeX](https://miktex.org/download)，重启终端或设置 tools.latex。Ubuntu 可运行 `sudo apt install texlive-latex-base texlive-latex-recommended`。这些是可选安装步骤，本次未安装系统级 TeX。

模板是 11pt、单栏、letterpaper；超页先删冗余，不能默默缩到 10pt。build-review 保留源文件，中间产物和页面 PNG 放 .cache/latex/build-*；只有编译成功、页数符合且无 overfull/undefined 才更新最终 PDF。命令失败时旧 PDF 仍在，**不能将旧文件当作本次成功**。需实际查看最新 PNG，不能只凭返回码宣称版面完好。默认一页，课程另有要求可用 --expected-pages。

reviews/synthetic-demo 是明确标记的合成模板测试，不是科学论文 review。

## 实际验证与故障排查

```powershell
& .venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -v
& .venv/Scripts/python.exe -X utf8 scripts/smoke_test.py
```

测试覆盖重复/版本/路径/笔记保护/链接与只读 Zotero HTTP 合约；合成 HTTP 服务不等于真实 Zotero 验证。smoke_test 用真实 CLI 子进程在 .cache/verification 创建隔离合成资料，包含预期失败案例，输出完整报告。结果不进入正式 vault。

- 缺 Python/包：按安装部分处理；不要修改或删除其他 Python 环境。
- 缺 PDF/哈希变化：重新导入同一原文恢复路径，或显式导入修订，不改旧依据。
- Zotero 403/连接拒绝：检查启动状态、官方通信开关、base_url 和 Windows/WSL 边界；手动导入不受影响。
- 扫描件/少文字：manifest 标出 possible_ocr_needed；本版没有 OCR 引擎，先分析能读的页，具体标记缺失。
- 索引丢管理标记：先保留用户内容，再补正确的一对标记；脚本不会全文覆盖。
- 锁文件残留：确认无 paper-wiki 命令运行后，才移除根目录 .paper-wiki.lock。
- 中文显示/第三方校验器解码问题：Python 加 `-X utf8`，PowerShell 读文本用 `Get-Content -Encoding UTF8`。
- Git 不在 PATH：本机可用 `& 'C:/Program Files/Git/cmd/git.exe' status --short --branch`。
- Codex 沙箱出现 `setup refresh had errors`：这是本次工具运行环境故障。项目仍可在普通本地终端运行；不要为了它重配项目或机器。状态文件记录了实际验证方式。

## 备份、Git 与接续工作

Git 跟踪代码、说明、三个 Skills、LaTeX 模板、可移植 JSON、Markdown 和 .tex；忽略 PDF、截图、.cache、.runtime、.venv、本机配置/路径、密钥和 Obsidian 临时工作区。**Git 不备份 PDF**，仍由 Zotero 或自己的备份保存；更换电脑后重建依赖并重新关联本地 PDF。

当前使用已有仓库，不建嵌套仓库、不自动提交/推送/发布。首次提交建议包含 README、AGENTS.md、paper_wiki_codex_prompt.md、docs、.agents/skills、paperwiki、scripts、tests、pyproject.toml、requirements.lock.txt、config.example.toml、.gitignore、目录保留文件、vault 初始页及 reviews/synthetic-demo/review.tex。提交前先检查暂存清单和忽略规则；本机配置及原始 PDF 不提交。

新会话接续 prompt：

> 请先读取 AGENTS.md 和 docs/status.md，再按本次任务加载对应 Skill、vault/index.md 与相关来源。保留我的手改，继续尚未完成的实际验证；不要假设新会话已核验 Zotero、论文图表或人工 reviewed 状态。此次任务是：……

持久化文件帮助接续工作，但不能消除模型的推理错误或长上下文退化。
