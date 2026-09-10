# 当前状态

更新：2026-09-10。本文件记录本次真实执行结果，不能代替未来重新检查。

## 最新连接复验

- 用户开启设置后，再次 doctor 已成功：zotero.reachable=true、api_version=3、server_id_available=true。此前连接不可达/403 为历史记录，当前连接问题已解决。
- 目前只验证了真实 Zotero API 根端点；还未读取/导入选定论文及本地附件。
- 当前项目客户端不读取 Zotero GUI 的选中条目或阅读器标签；需用户给论文标题、item key 或本地 PDF 路径来确定目标，不能把最近条目当作已选论文。
- 日常通过 Zotero API 导入时保持 Zotero 应用运行即可，不要求打开 PDF 阅读标签；附件必须已下载到本机。导入后若本地 PDF 路径仍有效，prepare-paper 直接读取文件，无需 Zotero 持续运行。

## 后续检查：用户已启动 Obsidian / Zotero

- 再次运行 doctor：Zotero 从连接不可达变为 HTTP 403，服务器已响应，但本机应用通信尚未获准；下一步在 Zotero 高级设置开启该权限。元数据/附件真实读取仍未验证。
- 本轮 Codex 可用 Skills 清单已经自动列出 paper-analysis、paper-review、wiki-maintenance 及本项目路径，确认当前环境能发现三个项目 Skills；仍未单独启动另一会话做跨会话验证。
- 当前 manual_pdf_ready=true、review_pdf_ready=true。待用户在 Obsidian 打开 D:/ShadowNote/vault，并选择第一篇论文。

## 已完成的第一版

- 已完整读取根目录 paper_wiki_codex_prompt.md，并原样归档到 docs/requirements.md；两文件 SHA256 相同：C53ED3FE47E0DF81B24FE1A5A904B926C97AC7212D217FA3C6FD49B6FB66768B。保留原文件及 README 原始介绍。
- 已创建简短 AGENTS.md、中文 README、architecture/sources 文档、配置示例与本机配置、Git 忽略规则、三个项目 Skills 和 11pt LaTeX 模板。
- 已实现 doctor、import-pdf、prepare-paper、resolve-pdf、zotero-list、zotero-import、lint-wiki、sync-index、build-review。所有命令可通过 .venv/Scripts/python.exe scripts/paper_wiki.py 运行。
- PDF 按完整 SHA256 去重；同标题不同内容保持独立；修订显式关联；手动/Zotero 别名可补充；书目冲突不静默改写。本机绝对路径只在忽略清单中。
- 按页文本抽取、选择性页面渲染和疑似 OCR 标记可用；未自动安装/执行 OCR。
- 单一 vault 已建立，Obsidian 打开 D:/ShadowNote/vault；用户笔记只读，索引管理区以外保留用户内容，日志只追加。
- Zotero 客户端只发 GET、限制选择范围、检查附件确实存在、解析 file URL/重定向；不访问 SQLite，不调用写 API，不转云端。
- review 实际编译、页数/日志检查、PNG 渲染和失败时保留旧 PDF 的逻辑已实现；本次合成样例实际编译一页并视觉检查。

## 实际环境

| 项目 | 本次观察 |
| --- | --- |
| 目录 | D:/ShadowNote，已有 Git 仓库 |
| Windows / shell | Windows 11（Python 报 10.0.26200），PowerShell 5.1；非 WSL |
| WSL | wsl --list --verbose 报未安装；未安装或修改 WSL |
| Git | C:/Program Files/Git/cmd/git.exe，可用但不在初始 PATH |
| Python | 初始 py 启动器无解释器；现为项目 .runtime + .venv 内 Python 3.12.14 |
| Python 包 | PyMuPDF 1.28.2、PyYAML 6.0.3、markdown-it-py 4.2.0、mdurl 0.1.2；已补项目 pip 26.2.1 |
| LaTeX | 初始无编译器；现有项目 .runtime/tectonic/tectonic.exe，Tectonic 0.17.0 |
| 排版缓存 | .cache/tectonic；未安装系统级 TeX |
| Poppler / Tesseract | 未发现；PyMuPDF 已承担页面渲染与页数检查，OCR 尚不可用 |
| Zotero | 已安装 10.0.1，真实 http://localhost:23119/api/ 探测不可达 |
| 原始论文 | sources/inbox 仅 .gitkeep，未提供真实 PDF |

下载项目 Python/依赖/便携编译器经过工具权限审批，没有重配系统环境。后续沙箱辅助程序出现 setup refresh had errors；项目命令通过获准的直接本地执行完成验证。图像查看工具也受影响，使用获准只读方式加载本项目 PNG 完成视觉查看。一项测试文件写入审批曾超时，拆分重试成功，没有遗留审批阻塞。

## 实际验证结果

| 验收 | 本次结果 |
| --- | --- |
| 自动测试 | 16 项全部通过，最终运行耗时 5.201 秒 |
| 测试风险覆盖 | 重复导入/中文空格路径/原文和用户内容不变/同标题隔离/修订保护/别名补充冲突/缺失或变化 PDF/坏 PDF/按需渲染/OCR 标记/索引幂等/断链与引用式链接/锚点/版本错误/孤立页/非法字段/锁和路径边界/编译器缺失 |
| Zotero HTTP 合约测试 | 合成本机 HTTP 服务验证 GET、分页限制、别名关联、server ID、本地 file URL/302、多个附件选择、403 和缺文件；不是用户 Zotero 实测 |
| 真实 CLI 子进程冒烟 | 导入、重复导入、选择性渲染、解析 PDF、缺失文件 exit 2、断链 lint exit 1 均符合预期；原文及用户笔记字节不变 |
| CLI 冒烟记录 | .cache/verification/latest-smoke.json；隔离合成资料位于该报告 root，不进入正式 vault |
| 当前正式 Wiki | lint-wiki：0 错误、0 警告，2 页，0 个来源；不代表已有科学内容 |
| 当前索引 | sync-index：0 个知识页条目，changed=false |
| 依赖一致性 | python -m pip check：No broken requirements found |
| Python 语法 | compileall 已通过；随后修改的模块由最终测试实际导入执行 |
| Skills 格式 | 官方 skill-creator quick_validate.py 对三个 Skill 全部通过；需 -X utf8，首次默认编码读取中文失败已解决 |
| doctor | manual_pdf_ready=true，review_pdf_ready=true，zotero.reachable=false |
| Git 检查 | diff --check 无空白错误；忽略规则实际验证了 .venv/.runtime/.cache、本机配置/路径与生成 PDF |

复验命令：

```powershell
& .venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -v
& .venv/Scripts/python.exe -X utf8 scripts/smoke_test.py
& .venv/Scripts/python.exe scripts/paper_wiki.py doctor
& .venv/Scripts/python.exe scripts/paper_wiki.py lint-wiki
& .venv/Scripts/python.exe scripts/paper_wiki.py build-review reviews/synthetic-demo/review.tex
```

## 合成 review 的真实结果

- 可编辑源文件：reviews/synthetic-demo/review.tex；与 Skill 模板一致，明确标记 Synthetic Layout Test，不是论文评价。
- 生成文件：reviews/synthetic-demo/review.pdf，实际 1 页，letterpaper，正文 11pt。
- 最新本次缓存：.cache/latex/build-wbey0d3j，包含编译日志、候选 PDF 与 review-01.png。
- 当前 Codex 实际查看了最新 PNG：标题、五段结构、三个问题完整，未见溢出、截断或重叠。
- LaTeX 无 overfull/undefined；进程 stderr 有非致命 Fontconfig 提示：Cannot load default config file。PDF 中模板字体显示正常，build-review 已将该提示纳入 warnings。其他自定义/系统字体仍需另行编译核查。
- 原本缺少 LaTeX 的阻碍已通过便携编译器解决；不把合成排版验证当作真实论文科学内容验证。

## 明确尚未验证/边界

1. **真实 Zotero 连接与附件**：当前不可达。启动 Zotero，开启官方确认的 Settings > Advanced > Allow other applications on this computer to communicate with Zotero，然后 doctor、有限列表并选一篇导入。没有改动该设置或用户库。
2. **真实论文精读/图表/课堂 review**：用户尚无 PDF；未编造分析、证据或概念页。将一篇放入 D:/ShadowNote/sources/inbox 后可执行完整流程。
3. **新会话 Skill 自动发现**：文件位置/格式经官方文档核对并校验；当前会话显式读取了三个 Skill，paper-review 执行合成排版验证、wiki-maintenance 执行结构 lint；paper-analysis 没有真实论文可执行。尚未用新会话验证自动发现，不能声称已经完成。
4. **真实 WSL 跨环境连接**：当前未安装 WSL；Windows 路径转换仅做合成测试，不保证特定网络/挂载配置可达。优先 Windows 同环境运行或手动 PDF 回退，不暴露 Zotero 端口。
5. **语义与人工确认**：lint 仅验证结构。来源真实性、图表结论、矛盾/过时内容及 reviewed 是否得到真实用户确认，仍需回原文/用户确认。
6. **PDF/OCR**：加密或损坏文件报错；扫描/稀疏文字只标记疑似 OCR。未安装 OCR 引擎，不声称扫描图表已读取。
7. **写入事务**：单文件原子替换 + 项目锁，非跨文件数据库事务；中断可按 architecture.md 恢复，不宣称整批全原子。

## Git 与接续

沿用已有 main，跟踪 origin/main，初始 HEAD c2386dd（Initial commit）。README 已修改，新增代码、说明、Skills、测试、配置示例、模板和 vault 文件待用户首次项目提交。未创建新远程仓库、未提交、未推送、未发布；未读取输出任何密钥。

第一次提交建议包含 README/AGENTS/交接归档、docs、.agents/skills、paperwiki、scripts、tests、pyproject.toml、requirements.lock.txt、config.example.toml、.gitignore、sources/vault 的可移植记录和目录保留文件、reviews/synthetic-demo/review.tex。不要提交 .venv/.runtime/.cache、config.local.toml、sources/local-paths.json 或 PDF。README 提供完整命令与示例。

下一步：用户放入一篇真实 PDF；新会话确认三个 Skills 可发现；Zotero 可达后选定一篇验证元数据与本地附件。新的验证结果应更新本文件，不能继续引用本次结果作为未来现状。
