# 当前状态

更新：2026-09-13。

项目已完成从旧 vault 工作流到单一 LLM Wiki 工作流的迁移。

- 已新增 docs/other-computer-codex-prompt.md：可直接复制给另一台电脑 Codex 的恢复与运行指令。

- 主知识库为 llm-wiki-data/wiki/：现有 20 页（2 个来源、11 个概念、3 个实体、1 个 query、index/log/overview）。
- 新命令 lint-llm-wiki 检查内容页 frontmatter、source_id/content_version、来源位置、wikilink、索引覆盖和重复名称；它不判断科学结论真实性。
- llm-wiki-review-context 只读地收集来源页、直接链接与 backlink；Zotero URI 会解析并验证登记的本地原 PDF。review 仍以原 PDF 为证据。
- Zotero collection/item 桥接仍是 GET-only，不复制 PDF；“当前选中论文”扩展仍是可选功能。
- 已删除旧 vault 代码、旧 lint/sync 命令、合成演示 review、旧 smoke 脚本和生成缓存；历史资料在 docs/archive/。

本轮验证：

- Python 编译检查通过。
- lint-llm-wiki --wiki-root .\llm-wiki-data：20 pages，0 errors，0 warnings。
- Python 自动测试：20 项通过。
- 3 个项目 Skill 均通过 skill-creator quick_validate。
- CLI help 已确认只提供 lint-llm-wiki，不再提供 lint-wiki 或 sync-index。

仍需由用户在桌面应用中验证：打开 llm-wiki-data 后刷新索引，确认该应用版本能显示现有 wiki 的图谱与搜索。应用内 Codex CLI 是只读子进程，不能直接写本项目文件。
