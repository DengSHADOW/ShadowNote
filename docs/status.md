# 当前状态

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
| Obsidian | 使用 D:/ShadowNote/vault，与 VS Code 共用 Markdown |

本机 Codex 沙箱 helper 持续报 setup refresh had errors；本轮命令通过获准的本地执行完成。未为此重配系统。

仍有这些边界：扩展目前仅针对 Zotero 10.0.x；独立无父条目的 PDF 提示手动导入；真实 WSL 网络/挂载未验证；扫描/OCR 未实现；lint 仅验证结构，不能证明科学正确或用户确已 reviewed；文件写入为单文件原子替换加项目锁，不是跨文件数据库事务。

## 下一步

用户安装 XPI 后，运行 zotero-selected 验证真实标题、item/attachment key 与 available_locally；只针对该论文导入、prepare-paper，记录实际读取结果。如果缺附件，先在 Zotero 下载，再重试。只有用户提出精读/review/入库要求时，继续对应科学工作流。不要把工具读取成功称为全文或图表已核验。
