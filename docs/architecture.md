# 架构与数据规范

## 目录

~~~
llm-wiki-data/
  purpose.md, schema.md
  wiki/
    index.md, log.md, overview.md
    sources/, concepts/, entities/, comparisons/, synthesis/, queries/
  raw/sources/              # 可选本地 PDF，Git 忽略
  .llm-wiki/                # 应用本机状态，Git 忽略
sources/metadata/           # 可提交的 PDF 身份与 Zotero 映射
sources/local-paths.json    # 本机路径，Git 忽略
reviews/SOURCE_ID/          # 可提交的 LaTex review
~~~

每个内容页的 YAML frontmatter 使用 type、title、source_id、content_version、sources。source_id 格式为 p- 加 PDF SHA-256；content_version 必须为同一哈希的 sha256: 前缀形式。sources 只允许 raw/sources/ 下的相对路径或 zotero://users|groups/.../items/... URI。

type 可以是 source、concept、entity、comparison、synthesis、query；overview 不要求来源。index.md 必须 wikilink 到所有内容页。链接使用 [[folder/page|label]]；不带目录的名称只有在全库唯一时才有效。

## 工作流

1. 手动 PDF 使用 import-pdf；Zotero collection/item 使用 zotero-wiki-plan。两者都登记稳定来源身份。
2. prepare-paper 在 .cache/papers/ 中生成逐页文本，按需渲染图页；PDF 内容不被修改。
3. Codex 读取原文和相关 Wiki 页，按用户范围写来源页或指定的共享页面。
4. lint-llm-wiki 检查 frontmatter、来源存在性、版本、wikilink 和 index；它不验证科学真实性。
5. llm-wiki-review-context 返回来源页、直接链接与 backlink，并为 Zotero URI 回查注册的原 PDF。

LLM Wiki 和 Codex 不应并发编辑同一页。每次修改前先读现有内容，保留人工编辑。
