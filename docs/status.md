# 当前状态

更新：2026-09-13。

## 2026-09-14 Wiki 中英配对约定

- 已将“中文论述后紧跟英文证据”写入 `llm-wiki-data/purpose.md`、`llm-wiki-data/schema.md`、`docs/requirements.md` 和 `docs/architecture.md`。
- 逐字来源文字必须标记为“英文原文”并附 PDF 页序号及章节/图表；综合、分析或回译必须标记为“英文对应表述（非逐字原文）”，不得冒充原文。
- 本次只建立后续 ingest/维护规则；既有页面仍需逐篇回查原 PDF 后迁移，未批量生成伪“原文”。

## 2026-09-14 AdaMAST 页面语言修复

- 将 LLM Wiki 对 `2607.16387v2.pdf` 单次 ingest 误生成的希腊语来源页、2 个实体页、8 个概念页和 4 条 Review 建议翻译为简体中文。
- 希腊语概念文件名已改为稳定的英文 slug；缓存与 Review 中的受影响路径已同步更新。
- 新页面已改用 PDF SHA-256 对应的 `source_id`、`content_version` 和 `raw/sources/2607.16387v2.pdf` 来源路径，状态保持 `draft`。
- 验证：Wiki 与 Review 中无连续希腊语文本；Review 和 ingest cache JSON 均可解析；`git diff --check` 通过。
- `lint-llm-wiki` 当前识别 31 个页面；本批新页面无结构错误，但旧的 `raw/sources/2605.09998v1.pdf` 当前缺失，使依赖它的 12 个旧页面报告来源不存在。

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
