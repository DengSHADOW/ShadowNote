# Project Purpose

## Goal

Build a source-grounded research wiki from papers managed in Zotero.

Zotero remains the source of truth for metadata and PDF files. Codex reads explicitly selected Zotero collections or items and writes source-linked Markdown here without copying the PDF into this project.

## Key Questions

1. What does each paper claim and show?
2. Which concepts, methods, and findings connect across papers?
3. What evidence supports limitations and classroom review questions?

## Scope

Research papers and their evidence. Keep original PDFs immutable and verify important review claims against them.

## Output Language

Write all generated Wiki pages, query titles, summaries, and log entries in Simplified Chinese unless the user explicitly asks for another language. Keep paper titles, proper nouns, code, formulas, and standard technical terms in their original form when that improves precision. Do not switch to Greek or another language because of source text or model preference.

For source-grounded content, place the corresponding English evidence immediately after each Chinese paragraph or bullet. Label a verbatim passage as `英文原文` and include its PDF page and section, figure, or table location. If a Chinese paragraph synthesizes several passages and has no single verbatim counterpart, label the following text `英文对应表述（非逐字原文）`; never present a translation or reconstruction as a quotation from the source. Keep English evidence concise and sufficient for verification rather than copying entire pages.
