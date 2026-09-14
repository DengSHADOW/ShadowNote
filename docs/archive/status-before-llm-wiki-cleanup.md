# 当前状态

用户已选择以 LLM Wiki 作为日常阅读、Markdown 编辑、搜索、图谱和 Chat 界面；Obsidian 已降为可选兼容工具，不再属于必要安装或验证步骤。主知识目录是 `llm-wiki-data/wiki/`，旧 `vault/` 暂不删除。

更新：2026-09-13。Zotero 单一 PDF 库的无复制桥接已实现；本节优先于后面的历史 Zotero 实现记录。

跨电脑交接入口：[`docs/cross-device-handoff.md`](cross-device-handoff.md)。该文档记录了当前方案、Git 同步边界、新电脑恢复步骤和仍需实机验证的事项。

## 当前实现：Zotero collection → Codex → LLM Wiki

- 新增 `zotero-wiki-plan --collection KEY|--items KEYS --wiki-root llm-wiki-data [--prepare]`。命令只调用 Zotero Local API GET，逐篇登记原附件路径和 SHA256，输出稳定 `zotero://` URI、source_id/content_version、目标 Wiki 页及 frontmatter；它不复制 PDF、不写 Wiki 页面、不生成摘要。
- `--prepare` 只把逐页文本写到 Git 忽略的 `.cache/papers/`。Codex 按 `wiki-maintenance` Skill 读取计划并维护 `llm-wiki-data/wiki/`，更新前必须读取已有页并保留用户或应用内的手改。
- `llm-wiki-review-context` 现同时支持 `raw/sources/...` 和 `zotero://users|groups/.../items/...`。对 Zotero URI 会从本机来源映射解析并重新校验原 PDF 哈希，再返回来源页与一层 wikilink/backlink。
- 已对真实 collection `LV8EWSVB` 以 `limit=1` 验证：成功登记 `SPADE: Self-Play in Adaptive Synthetic Executable Environments`（item `83RN9Q62`，attachment `E3RV4REV`），原 PDF 仍位于 Zotero storage；`llm-wiki-data/raw/sources/` 文件数为 0，可提交元数据不含 `C:\Users` 绝对路径，本机映射已被 Git 忽略。
- 同一真实 `zotero://users/0/items/83RN9Q62` 已经 `llm-wiki-review-context` 解析到原附件。尚未按用户指定范围精读或生成该论文 Wiki 页面，所以来源页/图谱列表仍为空；这不是失败，也不冒充已完成科学分析。
- Python 编译检查通过；自动测试现为 25 项全部通过，新增覆盖 collection 计划、GET-only、逐页缓存、零 PDF 复制、零脚本摘要写入及 Zotero URI 回查原文。

## LLM Wiki 桌面应用设置记录

- LLM Wiki v0.6.11 的 Codex CLI transport 已核对源码：它固定使用 `codex -a never exec ... --sandbox read-only --ephemeral`。因此应用内 Codex 会话不能自行写工作区、联网访问 Zotero 或申请升级；应用回复中“到 Codex 会话设置切换 Workspace write”不适用于这个由 LLM Wiki 创建的子进程。`Isolate local CLI configuration` 只控制是否忽略用户配置和 rules，不改变这组固定权限参数。
- 这个限制不妨碍 LLM Wiki 自身的 Sources ingest 流程在应用进程中写 Wiki；但它阻止 Codex CLI 子进程直接执行“访问 Zotero 并写 review 文件”的完整 Agent 工作流。若要全程应用内自动完成，需要改用具备工具调用权限的 API provider，或修改并自行构建 LLM Wiki。
- 2026-09-13 实机验证 Zotero Local API collection 路径：`zotero-list --collections` 成功读取 2 个 collection，随后分别用 `zotero-list --collection <KEY>` 读取到共 6 个顶层论文条目；全程仅 GET，不依赖当前选择扩展。这证明可用指定 Zotero collection 作为 LLM Wiki 导入队列，但 PDF 全文仍要求附件已下载到本机。
- LLM Wiki 已检测到 VS Code 扩展自带的 `codex-cli 0.153.4`，本机 CLI 状态为 ChatGPT 登录。应用预设的 `gpt-5.4-mini` 对该登录方式返回 HTTP 400（模型不受支持）；本机模型缓存列出 `gpt-5.5`、`gpt-5.6-luna`、`gpt-5.6-sol`、`gpt-5.6-terra` 和 `gpt-6-astra`，其中 `gpt-5.6-sol` 已用只读、ephemeral 的最小 `codex exec` 请求实测成功。LLM Wiki 中应通过 `Custom...` 使用 `gpt-5.6-sol`，不要继续用 `gpt-5.4-mini`。
- 已从 `nashsu/llm_wiki` 官方 v0.6.11 release 下载 Windows portable ZIP，SHA-256 实测为 `d9e3df15ac026d70c3e2716bd6d519ce67540943c1b998deef1f18c7cad2f8e6`，与 release API 摘要一致；解压到忽略目录 `.runtime/llm-wiki-app/`，`LLM Wiki.exe` 实测可启动（PID 31484）。
- 官方 MSI 同样已下载并校验（SHA-256 `89f2a5b33e551d1505b8dd70cb869c8c4f06fd1de556af09723ce16a391a08a7`），但安装日志显示 Windows Installer 错误 1925/1603：当前会话没有全机安装权限。因此未安装系统级版本，也没有把失败状态称为成功；portable 版可继续使用。
- 已创建 `llm-wiki-data/` 的可打开项目骨架，含 `schema.md`、`purpose.md`、`wiki/index.md`、`wiki/log.md`、`wiki/overview.md` 和标准目录。应用应以“打开已有项目”指向该子目录，绝不指向仓库根目录。
- Git 已忽略 `llm-wiki-data/raw/sources/`、媒体、本机 `.llm-wiki/` 和可选编辑器的工作区状态；计划跟踪 `wiki/`、`purpose.md`、`schema.md` 和 review。当前桥接不要求应用再次摄入 PDF；仍未验证应用对 Codex 生成的 `zotero://` 来源页进行索引和图谱显示。

| 新增验证 | 实测结果 |
| --- | --- |
| `python -m py_compile paperwiki/llm_wiki.py paperwiki/zotero_wiki.py paperwiki/cli.py` | 通过 |
| `paper_wiki.py zotero-wiki-plan --help` | 显示 collection/items、分页、prepare 参数 |
| Python 自动测试 | 25 项通过（含来源匹配、直接链接/backlink、只读 GET、无复制桥接、路径边界） |
| `llm-wiki-review-context` 对不存在 PDF | exit 2，明确报“source not found”，无猜测 |
| Git 忽略边界 | `.llm-wiki/state.json` 与 `raw/sources/paper.pdf` 被忽略；`wiki/*.md` 未被忽略 |
| Windows UI 自动化 | 未验证：CUA 内核因 `setup refresh had errors` 退出，无法代替用户点击应用；已改用启动进程验证 portable EXE |

## 下一步（需用户在已打开的应用窗口完成）

1. 选择“打开已有项目”，选 `D:\ShadowNote\llm-wiki-data`。
2. 在设置中自行填写模型 provider、API Key 和模型；不要把 Key 发给 Codex 或写入 Git。
3. 在 Zotero 建立或选择一个待处理 collection，并确认附件已下载到本机；告诉 Codex collection 名或 key，Codex 运行 `zotero-wiki-plan --prepare` 后按明确范围生成 Wiki 页。
4. 在 LLM Wiki 中重建/刷新索引，确认新 Markdown 的搜索和图谱显示；需要课堂 review 时再运行 `llm-wiki-review-context` 并调用 `$paper-review`。

---
更新：2026-09-10。本文件区分当前实测、历史验证与尚未完成的集成验收。

## 当前功能：读取 Zotero 选中论文

- 已重新读取客户端和本机 Zotero 10.0.1 安装包源码：旧客户端没有 GUI 选择读取逻辑；本次未发现原生“当前论文选择/阅读器”端点。原生按 item key 读取已可连接。
- 新增 `zotero-plugin/selection/` 小型只读扩展，识别列表选择、活动阅读标签、独立 PDF 窗口；返回目标 key、库和本机 PDF 可用性。无选择、多选、未加载阅读器及不支持条目均不猜目标。
- 新增 `zotero-selected [--view auto|library|reader]`、`zotero-import --selected [--view ...]`。按 key 导入继续可用。个人库/群组库按选择快照定位；活动 PDF 明确指定附件，避免从多个附件任取一个。
- 用户首次安装 0.1.0 XPI 失败；检查后发现 bootstrap 未等待 `Zotero.initializationPromise`，可能在 Zotero 尚未创建 Local API 时抛出启动异常，界面将其泛化为“可能不兼容”。已改为异步启动并重建 0.1.1；尚待真实安装复验。`strict_max_version: 10.0.*` 与 Zotero 当前官方 10.0 开发文档一致。
- 更正安装包：`dist/paper-wiki-selection-0.1.1.xpi`，SHA256 `57695b8c231447e23e99dadca3043783c24ae3d1786e0f25b965150974185555`。包内仅 manifest.json/bootstrap.js，dist 不进入 Git；新电脑可运行构建脚本重建。
- **真实集成尚差用户安装扩展**：本轮实际运行 zotero-selected，根 API 可达，新增端点返回 404，客户端正确提示扩展未安装。已请用户在 Zotero“工具 → 插件”拖入 XPI，然后返回列表选择论文。未冒充已识别/读取该论文。
- 安装/日常操作/同步说明见 [zotero-selection.md](zotero-selection.md)。长期需求已补入 requirements.md；AGENTS.md 已加入当前论文处理规则。三个科学工作 Skills 本轮未重写。
- 其他电脑同步来的论文可以用；当前电脑需已有可读 PDF。元数据同步不等于附件下载，按需下载可先在 Zotero 打开 PDF。文件已在本机时不必每次打开；无需复制到 inbox。

## 本轮实际验证

| 检查 | 结果 |
| --- | --- |
| Python 自动测试 | 22 项全部通过，12.862 秒 |
| 扩展 JavaScript | node --check 通过；6 项 node:test 模拟 Zotero 测试全部通过 |
| 选择功能覆盖 | 列表/阅读器优先级、独立窗口、未加载/无选择/多选、群组库、未下载 PDF、孤立附件/回收站提示、请求头和 GET 限制、卸载移除端点 |
| 客户端 HTTP 合约 | GET、server ID、单次快照、精确 PDF、群组路径、缺桥接端点、非法协议、选择冲突、未下载文件；使用合成本机 HTTP 服务 |
| 新功能独立 CLI | 合成 HTTP + 独立 CLI 子进程实际完成 zotero-selected → zotero-import --selected → prepare-paper，生成逐页文本；非法参数 exit 2 |
| 真实 Zotero doctor | reachable=true，api_version=3，server_id_available=true |
| 真实选中接口 | 未安装扩展，404 转为可操作提示；尚未读取实际论文 |
| 正式 Wiki lint | 0 错误、0 警告；2 页、0 来源，未写入测试分析 |
| 运行依赖 | manual_pdf_ready=true、review_pdf_ready=true；Node 20.17.0 用于开发测试，使用扩展无需 Node |
| Git | 本轮检查 diff --check 无空白错误；新增源码/文档/测试尚未提交或推送 |

模拟测试不是 Zotero 内真实安装验收。真实 PDF 还未导入，科学全文/图表/review 均未验证。本轮没有修改用户 Zotero 数据库、同步设置、条目或个人笔记，没有下载附件。

复验：

```powershell
& .venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -v
node --test tests/zotero_selection.test.cjs
& .venv/Scripts/python.exe scripts/build_zotero_plugin.py
& .venv/Scripts/python.exe scripts/paper_wiki.py doctor
& .venv/Scripts/python.exe scripts/paper_wiki.py zotero-selected
& .venv/Scripts/python.exe scripts/paper_wiki.py lint-wiki
```

## 已有第一版与历史验证

- 原始交接文件完整归档到 requirements.md；归档时与根文件 SHA256 均为 C53ED3FE47E0DF81B24FE1A5A904B926C97AC7212D217FA3C6FD49B6FB66768B。requirements.md 现在追加了后续需求，已不与原始归档哈希相同；根文件保留原文。
- 已实现 doctor、import-pdf、prepare-paper、resolve-pdf、zotero-list、zotero-import、lint-wiki、sync-index、build-review。按完整 SHA256 去重、显式版本关联、本机路径隔离、来源冲突保护、按页抽取/按需渲染、索引管理区和日志维护可用。
- 三个项目 Skills 当前环境已发现；独立新会话验证仍未另做。科学阅读由 Codex 执行，脚本不生成假分析。
- 初版 16 项测试全部通过；原 CLI 冒烟报告 `.cache/verification/latest-smoke.json` 验证导入/重复导入/渲染/解析/预期失败以及原文和用户笔记字节不变。该报告是历史合成验证，本轮新选择 CLI 流程由 unittest 独立子进程测试覆盖。
- 初版依赖 pip check、Skills 格式校验均通过。sync-index 当时为 0 条目、changed=false；本轮未因无内容变更而重复刷新索引。
- 合成 review：reviews/synthetic-demo/review.tex 实际编译为 1 页 letterpaper、11pt，最新当时缓存 `.cache/latex/build-wbey0d3j`；PNG 已实际查看，没有截断/重叠。LaTeX 无 overfull/undefined；有非致命 Fontconfig 配置警告。不是实际论文评价，本轮没有重新编译。
- Zotero 从初始不可达、403，到用户开启通信后根 API 成功；这些失败是历史记录，不再代表当前连接状态。
- Git 用户提交 `34023942fba23adedc220afc6a51b9677bed36be`（ver 1.0）已在前一任务按授权推送到 origin/main；本轮从干净 main 开始，新增选择功能未提交/推送。

## 环境与边界

| 项目 | 已观察状态 |
| --- | --- |
| 工作区 | D:/ShadowNote，Windows 11 / PowerShell 5.1，非 WSL |
| WSL | 早先检查未安装，本轮未修改 |
| Python | 项目 .runtime/.venv 内 Python 3.12.14 |
| Python 包 | PyMuPDF 1.28.2、PyYAML 6.0.3、markdown-it-py 4.2.0、mdurl 0.1.2；pip 26.2.1 |
| Git | C:/Program Files/Git/cmd/git.exe |
| LaTeX | 项目 .runtime/tectonic/tectonic.exe，0.17.0；未安装系统 TeX |
| PDF/OCR | PyMuPDF 可提取/渲染；Poppler/Tesseract 未发现，疑似 OCR 页仅标记 |
| Zotero | 10.0.1，Local API 根端点已连接 |
| LLM Wiki | 使用 D:/ShadowNote/llm-wiki-data 作为主要知识项目 |

本机 Codex 沙箱 helper 持续报 setup refresh had errors；本轮命令通过获准的本地执行完成。未为此重配系统。

仍有这些边界：扩展目前仅针对 Zotero 10.0.x；独立无父条目的 PDF 提示手动导入；真实 WSL 网络/挂载未验证；扫描/OCR 未实现；lint 仅验证结构，不能证明科学正确或用户确已 reviewed；文件写入为单文件原子替换加项目锁，不是跨文件数据库事务。

## 下一步

用户安装 XPI 后，运行 zotero-selected 验证真实标题、item/attachment key 与 available_locally；只针对该论文导入、prepare-paper，记录实际读取结果。如果缺附件，先在 Zotero 下载，再重试。只有用户提出精读/review/入库要求时，继续对应科学工作流。不要把工具读取成功称为全文或图表已核验。
# Verification update: Evolving Programmatic Skill Networks (2026-09-13)

- Zotero item `5RKUKLBV` and PDF attachment `GE9BCRAF` were resolved through the local GET API. The original 47-page PDF remains in Zotero storage and was not copied into `llm-wiki-data/raw/sources/`.
- Registered source ID `p-3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72` and content version `sha256:3105183fa039a8489e7f991631efa3c2010d9dfb8843b19fc0ae2eeb8e409d72`.
- Completed full-text close reading and visual inspection of Figures 1-17 and Tables 1-16. Wrote one draft source page at `llm-wiki-data/wiki/sources/zotero-users-0-5RKUKLBV.md`; no shared concept pages were created, and the paper's code was not executed.
- The source page remains `draft`; it has not been marked `reviewed`.
- Re-running `zotero-wiki-plan --items 5RKUKLBV --prepare` returned one ready top-level paper and an empty `unavailable` list; child attachment items are now filtered from the plan.
- `llm-wiki-review-context` resolved the original Zotero PDF, the source page, and backlinks from `wiki/index.md`, `wiki/log.md`, and `wiki/overview.md`.
- Automated tests: 25 passed in 9.285 seconds. `git diff --check` passed (line-ending warnings only), and `llm-wiki-data/raw/sources/` contains zero files.
- LLM Wiki UI refresh remains unverified in this run: after a Computer Use kernel reset and the permitted retry, the Windows helper still exited with `setup refresh had errors`. The Markdown project files themselves were verified through the CLI.

## Performance correction (2026-09-13)

- The first Evolving Programmatic Skill Networks trial was unnecessarily treated as a full close read: 47 pages, 17 figures, 16 tables, complete tests, and repeated UI recovery. This caused the long runtime and high token use.
- Project Skills and long-term requirements now default ambiguous “try/add to Wiki” requests to a focused quick ingest. Exhaustive appendix and figure/table coverage requires an explicit close-read/review request.
- Knowledge-page-only updates now use targeted context and formatting checks; full tests are reserved for code or data-rule changes. Repeated Windows UI helper failures stop after one recovery retry.
- Both changed Skills pass `quick_validate.py` under Python UTF-8 mode. The validator's first Windows-default run failed while decoding Chinese as cp1252; this was a validator locale issue, not an invalid Skill.

## LLM Wiki language and provenance repair (2026-09-13)

- The reported "garbled" generated pages were checked as UTF-8. Their Chinese text is intact; PowerShell's cp1252 console rendering made it appear mojibake. No Unicode replacement character was found in the 16 Wiki Markdown pages.
- Replaced the Greek query filename/reference with `red-bootstrap-updating-performance-2026-09-14-001220.md`, restored its index entry, and added an output-language rule to `llm-wiki-data/purpose.md` and `schema.md` for future generated content.
- `raw/sources/` contains only `.cache`; `2605.09998v1.pdf` is absent. The related source, 7 concept pages, 3 entity pages, and query page now carry `status: source-missing`; the source page has a visible warning that its claims have not been rechecked against the original PDF.
- Validation: all 16 pages decoded as UTF-8; 0 replacement characters; no stale Greek query reference; `git diff --check` reported no whitespace errors (only existing CRLF conversion notices).

## LLM Wiki source and graph repair (2026-09-13)

- User supplied `2605.09998v1.pdf`. It was copied to the intentionally Git-ignored `llm-wiki-data/raw/sources/` directory and registered as `p-50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e` / `sha256:50f60996b0d962cdbf01f5b6a262ccd68b149c8b67cc2594218453717ea0c45e` (28 PDF pages, arXiv:2605.09998v1). The portable metadata record is tracked under `sources/metadata/`; the PDF binary is not.
- Rechecked the Harness source, 7 concept pages, 3 entity pages, and saved query against extracted PDF text. Replaced `source-missing` with `draft`, added exact source/version metadata and project-relative raw-source references, and corrected the Red bootstrap-updating query: the main-text early comparison is qualified by the Appendix C.2 regression after inherited sub-agent use collapses.
- Added four source-linked knowledge nodes for Evolving Programmatic Skill Networks: Programmatic Skill Network, execution-trace-guided repair, reliability-aware updating, and validated structural refactoring. Rebuilt `wiki/index.md`, `overview.md`, and source-to-concept links; no speculative cross-paper edges were added.
- Validation: `prepare-paper` extracted all 28 Harness pages and rendered PDF pages 2, 4, 6–9, 22, 24, and 27. Both `llm-wiki-review-context` calls resolve their original source and linked pages. Local graph audit: 20 Markdown pages, 86 wikilinks, 0 broken/ambiguous targets. `git check-ignore` confirms the copied PDF is ignored. Image inspection via the Windows helper remains unavailable because its sandbox setup refresh fails; no claim of visual inspection is made for those renders.
