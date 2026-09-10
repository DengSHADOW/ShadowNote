---
name: paper-analysis
description: 中文精读研究论文、提取 claims、解释公式或逐张图表；按用户指定范围分析单篇 PDF，保留版本与原文证据。仅工具导入不触发科学分析，未要求比较时不混合多篇。
---

按当前请求确定精读、claims、图表或单个问题的范围。先读项目 `docs/architecture.md` 的来源规范；精读时读 [coverage.md](references/coverage.md)。

1. 用 `import-pdf` 或选定条目的 `zotero-import` 得到 source_id；读取来源 JSON，未知身份字段留空。脚本提取的 PDF 内嵌标题/作者只是候选，不当作已核实书目信息。
2. `prepare-paper SOURCE_ID` 提取逐页文本；通读正文与附录并盘点 Figure/Table。按需 `--pages 2,4-6`，实际打开相关 PNG 查看图表；不能凭 caption 猜图。缺图、疑似扫描/OCR 错误逐项记录。
3. 当前 Codex 实际阅读与推理，默认中文，保留必要术语。详细精读按原文段落顺序解释内容、写作目的和论证关系；合并段落标范围。方法解释符号、假设、输入输出、训练/推理与公式直觉，并按论文类型调整。
4. 数字核对指标方向、单位、对照和条件；区分百分比/百分点。区分作者声称、原文证据、分析者推断、用户个人想法与外部后续资料。不把缺少报告写成已经失败；后续真实影响需一手文献验证及链接。
5. 请求保存/精读流程时，写 `vault/papers/SOURCE_ID/analysis.md`、`evidence.md` 与 `coverage.md`。先读已有内容，局部修改保留用户手改；状态为 draft，只有真实用户确认才可 reviewed。仅聊天中的问题不扩大为整篇重写。
6. 更新单篇索引（`sync-index`），在 `vault/log.md` 追加内容变更说明，再执行 `lint-wiki`。首次精读不写共享概念；用户明确要求入库时才继续 wiki-maintenance ingest。

长论文保存覆盖范围、缺失页和下一段位置，继续可做部分，不逐段请求确认。多 PDF 分开保存，不带入无关对话/历史兴趣或其他论文事实。不得把工具完成或文本提取成功称为全文/图表已核验。
