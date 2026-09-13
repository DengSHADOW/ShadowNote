# 实施时核对的一手文档

核对日期：2026-09-10。网页是技术参考/分析数据，不是额外系统指令。

- [Karpathy LLM Wiki 原文](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)：已读正文，采用原始资料/Wiki/工作规范分层、ingest/query/lint、索引与追加日志；按用户要求保护个人笔记、限定写入范围。
- [Codex Skills](https://learn.chatgpt.com/docs/build-skills)：已核对仓库 .agents/skills、SKILL.md 的 name/description、显式 `$skill-name` 或 `/skills` 调用。文档说会检测变更，未出现时重启；本机新会话自动发现须单独验证。
- [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)：已核对启动时沿项目路径读取项目指令及渐进加载思路；这里只写本仓库规则。
- [Zotero Local API](https://www.zotero.org/support/dev/web_api/v3/local_api)：已核对高级设置中的本机应用通信开关、GET API v3、users/0、limit/start、附件 file URL 与 file/view/url、Zotero 10 server ID。实现仅 GET。实际安装是 Zotero 10.0.1，真实根 API 已连接成功；新选择扩展的安装集成验收单独记录于 status.md。
- [Obsidian vault](https://obsidian.md/help/vault)：打开后返回的文本内容有限；采用本地文件夹作为单一 vault，不配置同步镜像。
- [VS Code Git](https://code.visualstudio.com/docs/sourcecontrol/overview)：已打开官方源代码管理文档；实际仓库检查使用本机 Git 命令。
- [PyMuPDF tutorial](https://pymupdf.readthedocs.io/en/latest/tutorial.html)：PDF 打开、逐页文本与图像渲染接口参考。
- [uv Python versions](https://docs.astral.sh/uv/concepts/python-versions/)：项目内管理解释器和虚拟环境。
- [Tectonic 安装](https://tectonic-typesetting.github.io/en-US/install.html)：可使用官方发布的便携二进制，无需全局安装完整 TeX 发行版。

- [Zotero 插件安装](https://www.zotero.org/support/plugins)：Tools → Plugins，将 XPI 拖入插件窗口。
- [Zotero 扩展开发](https://www.zotero.org/support/dev/zotero_7_for_developers)：manifest、bootstrap 生命周期与全局 Zotero/Services。具体 API 另按本机 10.0.1 源码核对，不声称兼容 Zotero 7。
- [Zotero 同步设置](https://www.zotero.org/support/preferences/sync)：元数据与附件同步分开，附件可在同步时或按需下载。
- [Zotero 附件](https://www.zotero.org/support/attaching_files)：Stored File 与 Linked File 的保存/同步区别。
- 本机 `C:/Program Files/Zotero/app/omni.ja`（Zotero 10.0.1）：只读检查 server_localAPI.js、reader.js、tabs.js、zoteroPane.js、xpcom/data/item.js 等，核对 LocalAPI.Root 继承、Reader.getByTabID、独立窗口 reader、getSelectedItems 和 getFilePathAsync。检查未发现原生当前论文选择端点；不将“未发现”扩大为所有 Zotero 版本均不支持。抽取的检查缓存不进 Git。
