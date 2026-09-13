# Zotero 当前论文识别与跨电脑使用

这项功能由项目内的小扩展提供。现有 Zotero 10.0.1 原生 Local API 能按 key 读取论文，但本次检查安装包源码，没有找到“当前选中论文/当前阅读器”端点。不能把最近添加的论文当作选中的论文。

## 安装一次

1. 构建安装包：`.venv/Scripts/python.exe scripts/build_zotero_plugin.py`。
2. 在 Zotero 的 **工具 → 插件（Tools → Plugins）** 打开插件窗口，把 `dist/paper-wiki-selection-0.1.1.xpi` 拖入并完成安装。也可用该窗口的“从文件安装插件”。返回文献库窗口。
3. 保持 Zotero 高级设置中 **Allow other applications on this computer to communicate with Zotero** 开启。
4. 在文献列表选中一篇论文，或激活其 PDF 阅读器，然后运行下面的检查命令。

安装方式见 [Zotero 官方插件说明](https://www.zotero.org/support/plugins)。扩展源码在 `zotero-plugin/selection/`，安装包是这两个源文件的 ZIP，无远程脚本或依赖。当前版本限定 Zotero 10.0.x；实际集成验证状态见 [status.md](status.md)。新电脑需要重新构建并安装，Git 不同步 Zotero 插件安装状态。

## 日常使用

```powershell
# 只查看目标和附件是否已在本机，不创建来源或分析。
& .venv/Scripts/python.exe scripts/paper_wiki.py zotero-selected
# 导入当前目标的 PDF，输出 source_id。
& .venv/Scripts/python.exe scripts/paper_wiki.py zotero-import --selected
# 用上一步的 source_id 提取逐页原文。
& .venv/Scripts/python.exe scripts/paper_wiki.py prepare-paper SOURCE_ID
```

然后可以告诉 Codex：“请精读我在 Zotero 选中的论文。”Codex 应读取当前选择、导入、提取原文，再按 paper-analysis 执行真实阅读。工具导入本身不会生成分析或写共享概念页；明确要求入 Wiki 后再执行 wiki-maintenance。

`zotero-import --selected` 在这一次命令开始时取得选择快照；之后导入该快照中的 key，不会中途跟随用户切换到其他论文。单独运行查看与导入属于两次快照；希望锁定先前查看的目标时用返回的 item_key 明确导入。

| 当前 Zotero 状态 | 默认 auto 的目标 |
| --- | --- |
| 文献库标签激活 | 列表中选中的条目，不必打开 PDF |
| PDF 阅读标签激活 | 当前 PDF 及其父论文，优先于后台列表选择 |
| 独立 PDF 窗口最近激活 | 该窗口的 PDF 及其父论文 |
| 设置等其他 Zotero 窗口最近激活 | 提示回到文献库/阅读器，避免读取旧选择 |
| 无选择或多选 | 提示明确选一篇，不任取第一篇 |

用 `--view library` 强制读取文献列表选择；`--view reader` 只接受活动阅读器。两个选项均适用于 zotero-selected 和 zotero-import --selected。阅读器尚未加载时不会回退到另一篇列表论文。

一篇有多个 PDF 时，打开或选中目标 PDF 附件，或在选中父条目时用 `--attachment KEY`。直接选中 PDF 后不能用另一个 attachment key 静默覆盖。当前支持个人库和群组库中的父论文及其 PDF 附件；独立、没有父条目的 PDF 会给出手动 import-pdf 或在 Zotero 中建立父条目的提示。笔记/批注不是论文目标。

## PDF 和跨电脑同步

**其他电脑同步过来的论文可以使用，PDF 需要在运行工具的电脑上可读。** 不必复制到 sources/inbox；Zotero 自己的本地附件目录即可。

- **仅同步元数据**：可识别标题和 key，但没有 PDF 就不能全文阅读。
- **附件已同步下载**：选中列表条目即可，不必打开 PDF。
- **按需下载附件**：先在 Zotero 打开 PDF，等待下载完成，再导入；以后文件仍在本机就无需每次打开。
- **链接文件（Linked File）**：Zotero 文件同步不负责传输它。需外部同步工具把文件带到本机，并正确设置链接附件路径。
- **迁移本项目**：Git 保存 Markdown/来源身份，忽略 PDF 和本机路径映射。新电脑重新导入同一 PDF，可按完整 SHA256 复用 source_id、补充本机路径；不依赖另一台电脑的绝对路径。

依据：[Zotero 同步设置](https://www.zotero.org/support/preferences/sync)、[存储附件与链接文件](https://www.zotero.org/support/attaching_files)。扩展只检查附件存在性，不替你启动下载。导入后，prepare-paper 直接读本机文件，只要路径有效，不要求 Zotero 一直运行。

## 协议与排错

扩展增加 `GET /api/paper-wiki/selection?view=auto`，客户端带 `X-Paper-Wiki: 1`。响应包含 schema_version=1、bridge_version、selection_kind、问题说明、条目 key、库路径、PDF key 和 available_locally；不返回用户整库或绝对附件路径。导入时另外用原生 Local API 核实附件归属和本地文件。

端点继承已安装 Zotero 10 的 LocalAPI.Root，沿用本机通信开关、API 版本、server ID 校验与原生浏览器访问限制；不开放 CORS，不另开端口。额外请求头用于限制普通网页请求，不是身份密钥。扩展只注册 GET，不写条目/数据库、不下载附件。禁用/卸载时移除端点。

- `Selection bridge is not installed`：扩展未安装、未启用或加载失败。先检查插件窗口，必要时重启 Zotero。
- `403`：检查高级设置本机应用通信开关。
- `available_locally: false`：先下载/修复该附件；单有同步条目不是 PDF 已到本机。
- `Select exactly one`：清除多选，选一篇或一个 PDF。
- `Select one PDF with --attachment`：该父条目无 PDF 或有多个 PDF，按提示明确附件。
- 原生按 key 的 zotero-import 和手动 import-pdf 不依赖该扩展。

验证命令：

```powershell
node --test tests/zotero_selection.test.cjs
& .venv/Scripts/python.exe -X utf8 -m unittest discover -s tests -v
& .venv/Scripts/python.exe scripts/paper_wiki.py zotero-selected
```

Node 仅用于扩展开发测试，使用安装包时不需要 Node。模拟测试不能替代在用户 Zotero 中安装后识别真实论文的验收。
