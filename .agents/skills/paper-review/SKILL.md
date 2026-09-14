---
name: paper-review
description: 根据一篇论文原文与证据写英文课堂 paper review，默认一页 11pt LaTeX/PDF；也可按请求仅改一句或写课堂问题，不自动扩大为文件重写或模拟审稿评分。
---

先读本篇来源记录、LLM Wiki 来源页与已有 review，回查原文关键 claims/数字。详细写作和编译要求读 [review-guide.md](references/review-guide.md)。

若知识页位于 `llm-wiki-data/`，先用 `llm-wiki-review-context --source zotero://users/0/items/ITEMKEY` 读取来源页和直接图谱邻居；命令返回的 `original_pdf` 才是事实核验依据。Wiki 内容可提供概念关系与用户修改，不能替代 PDF 证据。

默认 Summary、Strengths、Weaknesses、Questions for the Presenter（3 个简短问题）、Overall Assessment；简单自然的学术英语。不泛泛赞美，不要求演讲者补跑实验，不默认 accept/reject。根据论文当时背景与作者实际 claim 范围评价，不把未控制的比较当成因果。

用户要求文件时，每篇保存 `reviews/SOURCE_ID/review.tex`；采用 [review-template.tex](assets/review-template.tex)，11pt、单栏、letterpaper。约 450–550 词是起始目标，实际页数为准；先压缩冗余，不减到 10pt。特殊字符用 `paperwiki.review.latex_escape` 或正确手工转义。用户课程模板优先。

`build-review reviews/SOURCE_ID/review.tex` 必须实际执行；检查输出页数/日志，并打开缓存的每页 PNG 看溢出或截断。缺编译器时保留 .tex、报告 PDF 未生成及 README 安装步骤；多页或溢出不能称为合格一页 PDF。模板测试仅验证排版，不能当作科学验证。

保留手改，更新证据映射；draft 不自动升级为人工 reviewed。每篇独立文件，明确要求合并时才每篇另起页。仅聊天改句或写问题不自动修改文件。
