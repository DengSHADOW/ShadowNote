# 当前状态

更新：2026-09-13。

## 2026-09-15 Evolving Programmatic Skill Networks 复核修复

- 已恢复该论文 Zotero 本机 PDF 的 `sources/local-paths.json` 映射；SHA-256 与既有 `source_id` 完全一致，47 页均可提取且无 OCR 警告。
- 已重新核查全文、Figure 1–17 与 Table 1–16；修正了回滚率分母（按 iterations，不是按 applied proposals），并明确 Figure 8b 的 single hero run 对六次运行均值的不对称口径。
- 已限制“完成科技树”“架构而非模型”“组合泛化”“成本摊销”等超出实验直接支持范围的表述，并补记 Figure 3–6 的样本/不确定性缺失、Table 14 的 3-run/6-run 混用以及 $J(N)$ 的方向矛盾。
- 来源页和四个概念页已按项目约定补充中英对应证据，状态保持 `draft`；未运行作者代码或把作者报告当作独立复现。

## 2026-09-15 LLM Wiki v0.6.11 图谱链接修复

- 已确认 v0.6.11 的可视化边只由内容页正文 `[[wikilink]]` 建立；`related: []` 和共同 `sources: []` 不会单独创建可见边，目录前缀链接也不能匹配其 basename 节点 ID。
- 内容页中的有效目录前缀链接已机械转换为裸文件名链接；`index.md` 仍保留目录前缀作为导航。
- 为 2503.12188v2、2608.10218v1 及 AdaMAST 页面补充了少量可解释的来源、概念、实体和跨论文关系，避免按共同来源生成全连接图。
- 2503.12188v2 与 2608.10218v1 生成页已补齐基于本地 PDF SHA-256 的 `source_id`、`content_version` 和 `raw/sources/` 路径。
- `schema.md` 与 `architecture.md` 已加入 v0.6.11 图谱兼容规则，防止后续 ingest 再生成不可解析的内容页链接。
- 按 v0.6.11 的 basename + 正文 wikilink 解析算法复算：50 个非 query 节点全部已连接，孤立节点为 0。`index.md` 仅连接到 `overview.md`，不会形成无意义的全库星形中心；Query 页在该版本图谱中默认隐藏。
- `git diff --check` 通过；`lint-llm-wiki` 识别 59 页，本次两篇新论文的内容页不再报告来源或 wikilink 错误。剩余错误来自旧的 `2605.09998v1.pdf` 缺失，以及 LLM Wiki 自动生成的 Deep Research/query 页缺少项目级来源身份或含占位链接，未在本次图谱修复中混改。

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
