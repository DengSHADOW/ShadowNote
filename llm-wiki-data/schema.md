# Wiki Schema

## Purpose

This project organizes research papers and their evidence. Keep generated pages source-linked, distinguish author claims from verified evidence, and preserve user edits.

## Page types

- `wiki/sources/`: paper and source summaries
- `wiki/concepts/`: methods and concepts
- `wiki/entities/`: people, organizations, datasets, and systems
- `wiki/comparisons/` and `wiki/synthesis/`: explicit cross-source analysis

Use YAML frontmatter with `type`, `title`, and `sources`.

## Language

Use Simplified Chinese for human-facing page titles and prose unless the user explicitly requests another language. Preserve exact paper titles, proper nouns, code, formulas, identifiers, and unambiguous English technical terms. Wikilink filenames may remain ASCII, but their visible labels must follow the requested language.

Use paired bilingual blocks for source-grounded prose:

```markdown
中文论述。（PDF p. 12，§4.2）

> **英文原文：** “A short, exact supporting passage from the source.”
```

If the Chinese text combines multiple source passages or is analysis rather than a direct translation, use:

```markdown
中文综合或分析。

> **英文对应表述（非逐字原文）：** A faithful English counterpart or synthesis.
```

Never label generated English, back-translation, or multi-passage synthesis as `英文原文`. For tables, preserve the source's English labels in the same table where practical and add the precise PDF page plus table/figure identifier. Frontmatter, headings, navigation-only lists, filenames, code, formulas, and log metadata do not require duplicated English.

## Math

For compatibility with LLM Wiki v0.6.11, delimit inline math with `$...$` and display math with `$$...$$`. Do not use `\(...\)` or `\[...\]`. Within math delimiters, write normal LaTeX such as `N_q`, `X_I X_T^\top`, and `\operatorname{Top}_{N_q}` without Markdown-escaping `_` or `^`.

## Graph links

LLM Wiki v0.6.11 builds visible graph edges from body `[[wikilinks]]`. In source, concept, entity, comparison, and synthesis page bodies, link to the unique bare filename without its directory prefix, for example `[[virus-chain|virus chain]]`, not `[[concepts/virus-chain|virus chain]]`. The `related: []` frontmatter field is descriptive metadata and does not replace body links in this version.

Every concept and entity page should link back to its source page and to one to three directly relevant knowledge pages. Source pages should link to their principal concepts and entities. Prefer a small number of meaningful relationships; do not make every page from the same paper link to every other page. `wiki/index.md` may retain directory-prefixed links for deterministic navigation and lint coverage.

- For an optional file copied into this project, use a project-relative path such as `raw/sources/paper.pdf`.
- For the default no-copy Zotero bridge, use `zotero://users/0/items/ABCD1234` (or a group-library URI) and also store `source_id`, `content_version`, `zotero_item`, and `zotero_attachment` from `zotero-wiki-plan`.
- Never store a machine-specific absolute PDF path in a Wiki page. Resolve it through ShadowNote when the original is needed.
