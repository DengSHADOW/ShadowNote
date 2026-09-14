---
name: paper-analysis
description: 中文精读研究论文、提取 claims、解释公式或逐张图表；按用户指定范围分析单篇 PDF，保留版本与原文证据。
---

先读 docs/architecture.md 的来源规范。仅导入或准备 PDF 不等于已经完成科学分析。

- 用户只说“看看”“试试”或“加入 Wiki”时，进行快速阅读：摘要、引言、核心方法、主要结果、结论与支撑这些结论的核心图表；不要声称精读全文。
- 用户要求“正式精读”“完整精读”“逐图逐表”、详细 claims/evidence 或 paper review 时，通读正文与附录，按 .agents/skills/paper-analysis/references/coverage.md 记录覆盖范围、缺页和图表核验。
- 手动 PDF 使用 import-pdf，Zotero 项目使用 zotero-import 或 zotero-wiki-plan。读取来源 JSON；嵌入式题名和作者只是候选元数据。用 prepare-paper SOURCE_ID 取得逐页文本，按需渲染实际引用的页面，不能只凭 caption 猜图。
- 分析时区分作者 claim、可定位的原文证据、分析推断、用户想法和外部后续材料。数字同时核对指标方向、单位、对照条件和百分比/百分点。
- 用户要求保存时，先读已有 llm-wiki-data/wiki/sources/ 目标页并在同一来源页内补充分析、证据和覆盖范围；内容页必须使用 source_id、content_version 与 sources frontmatter。保留用户手改，默认 draft，不自行改为 reviewed。
- 保存后按 wiki-maintenance 更新 index 和必要的直接图谱链接，并运行 lint-llm-wiki --wiki-root .\llm-wiki-data。首次单篇精读不自动创建共享概念页。

长论文可以记录已完成范围并继续，不要把文本提取成功说成图表或全文已核验。多篇论文分别分析，除非用户明确要求比较。
