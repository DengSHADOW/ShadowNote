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

- For an optional file copied into this project, use a project-relative path such as `raw/sources/paper.pdf`.
- For the default no-copy Zotero bridge, use `zotero://users/0/items/ABCD1234` (or a group-library URI) and also store `source_id`, `content_version`, `zotero_item`, and `zotero_attachment` from `zotero-wiki-plan`.
- Never store a machine-specific absolute PDF path in a Wiki page. Resolve it through ShadowNote when the original is needed.
