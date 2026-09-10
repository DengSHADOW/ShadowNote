"""Structural validation. Never claims to validate scientific truth."""
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .core import WikiError, atomic_write, now, read_json, safe_id


START = "<!-- paper-wiki:index:start -->"
END = "<!-- paper-wiki:index:end -->"


def libraries():
    try:
        import yaml
        from markdown_it import MarkdownIt
        return yaml, MarkdownIt("commonmark")
    except ImportError as exc:
        raise WikiError("PyYAML/markdown-it-py missing. Install project dependencies.") from exc


def frontmatter(path):
    yaml, _ = libraries()
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        return {}, text
    try:
        data = yaml.safe_load(match[1]) or {}
    except yaml.YAMLError as exc:
        raise WikiError(f"{path}: invalid YAML frontmatter") from exc
    if not isinstance(data, dict):
        raise WikiError(f"{path}: frontmatter must be a mapping")
    return data, text[match.end():]


def links_and_anchors(text):
    _, parser = libraries()
    tokens = parser.parse(text)
    links, anchors = [], set()
    seen = Counter()
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            heading = tokens[i + 1].content
            slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
            anchors.add(slug + (f"-{seen[slug]}" if seen[slug] else ""))
            seen[slug] += 1
        for child in token.children or []:
            if child.type in ("link_open", "image"):
                links.append(child.attrGet("href") if child.type == "link_open" else child.attrGet("src"))
    anchors.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', text))
    return links, anchors


def lint_wiki(project):
    errors, warnings = [], []
    records = {}
    required = {"schema_version", "source_id", "pdf_sha256", "content_version", "title", "authors", "year", "doi",
                "arxiv_id", "version", "source_url", "revision_of", "zotero", "page_count", "possible_same_paper"}
    for path in sorted(project.metadata.glob("*.json")):
        try:
            data = read_json(path)
            if not isinstance(data, dict):
                raise WikiError("source record must be a JSON object")
            missing = required - data.keys()
            if missing:
                errors.append(f"{path}: missing fields {sorted(missing)}")
                continue
            source_id = safe_id(data["source_id"])
            if source_id != path.stem or source_id != "p-" + data["pdf_sha256"] or data["content_version"] != "sha256:" + data["pdf_sha256"]:
                errors.append(f"{path}: source ID/hash/version mismatch")
            if not isinstance(data["authors"], list) or not isinstance(data["zotero"], list):
                errors.append(f"{path}: authors and zotero must be lists")
            if data["schema_version"] != 1 or not isinstance(data["page_count"], int) or data["page_count"] < 1:
                errors.append(f"{path}: unsupported schema or invalid page_count")
            if not isinstance(data["possible_same_paper"], list):
                errors.append(f"{path}: possible_same_paper must be a list")
                continue
            if data["revision_of"] is not None and not isinstance(data["revision_of"], str):
                errors.append(f"{path}: revision_of must be a source_id or null")
                continue
            records[source_id] = data
        except (WikiError, TypeError, KeyError) as exc:
            errors.append(f"{path}: {exc}")
    for source_id, data in records.items():
        if data.get("revision_of") and data["revision_of"] not in records:
            errors.append(f"sources/metadata/{source_id}.json: unknown revision_of")
        for candidate in data.get("possible_same_paper", []):
            if not isinstance(candidate, dict) or not isinstance(candidate.get("source_id"), str) or candidate.get("source_id") not in records:
                errors.append(f"sources/metadata/{source_id}.json: unknown candidate source")
    paths = sorted(project.vault.rglob("*.md"))
    pages, inbound, index_targets = {}, Counter(), []
    for path in paths:
        try:
            meta, body = frontmatter(path)
            links, anchors = links_and_anchors(body)
            pages[path.resolve()] = (meta, body, links, anchors)
        except WikiError as exc:
            errors.append(str(exc))
    for path, (meta, body, links, anchors) in pages.items():
        rel = path.relative_to(project.vault)
        knowledge = rel.parts[0] in ("papers", "concepts", "topics")
        if knowledge:
            for field in ("title", "status", "sources"):
                if not meta.get(field):
                    errors.append(f"{path}: missing {field} frontmatter")
            if meta.get("status") not in ("draft", "reviewed"):
                errors.append(f"{path}: status must be draft or reviewed")
            if meta.get("status") == "reviewed" and not meta.get("reviewed_by_user_at"):
                errors.append(f"{path}: reviewed needs actual reviewed_by_user_at confirmation")
            sources = meta.get("sources", [])
            if not isinstance(sources, list):
                errors.append(f"{path}: sources must be a list of source_id/version mappings")
                sources = []
            ids = []
            for source in sources:
                if not isinstance(source, dict):
                    errors.append(f"{path}: each source needs source_id and content_version")
                    continue
                sid = source.get("source_id")
                if not isinstance(sid, str):
                    errors.append(f"{path}: source_id must be a string")
                    continue
                if sid not in records:
                    errors.append(f"{path}: unknown source_id {sid}")
                elif source.get("content_version") != records[sid]["content_version"]:
                    errors.append(f"{path}: wrong/missing content_version for {sid}")
                ids.append(sid)
            if len(ids) != len(set(ids)):
                errors.append(f"{path}: repeated source is not independent evidence")
            if rel.parts[0] == "papers" and (len(rel.parts) < 3 or rel.parts[1] not in ids):
                errors.append(f"{path}: paper directory must match a declared source_id")
        for link in links:
            parsed = urlsplit(link)
            if parsed.scheme in ("http", "https", "mailto", "zotero", "obsidian"):
                continue
            if parsed.scheme or parsed.netloc or re.match(r"^[A-Za-z]:", link) or "\\" in link:
                errors.append(f"{path}: nonportable local link {link}")
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not target.is_relative_to(project.vault):
                errors.append(f"{path}: link leaves vault: {link}")
            elif not target.exists():
                errors.append(f"{path}: broken link: {link}")
            else:
                if target != path:
                    inbound[target] += 1
                if path == project.vault / "index.md" and target.suffix == ".md":
                    index_targets.append(target)
                if parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target][3]:
                    errors.append(f"{path}: missing heading anchor: {link}")
    index_path = project.vault / "index.md"
    if index_path not in pages:
        errors.append(f"{index_path}: missing index")
    for path in pages:
        rel = path.relative_to(project.vault)
        if rel.parts[0] in ("papers", "concepts", "topics") and path not in index_targets:
            errors.append(f"{path}: missing from index.md; run sync-index")
        if rel.name not in ("index.md", "log.md") and not inbound[path]:
            warnings.append(f"{path}: orphan page (no incoming links)")
    for path, count in Counter(index_targets).items():
        if count > 1:
            errors.append(f"{index_path}: duplicate entry for {path}")
    return {"errors": errors, "warnings": warnings, "pages": len(pages), "sources": len(records),
            "semantic_check": "not performed; claims, contradictions and staleness require source review by the agent"}


def sync_index(project):
    with project.lock():
        path = project.vault / "index.md"
        original = path.read_text(encoding="utf-8") if path.exists() else "# Paper Wiki\n\n" + START + "\n" + END + "\n"
        if original.count(START) != 1 or original.count(END) != 1 or original.index(START) > original.index(END):
            raise WikiError("index.md needs exactly one ordered managed block; user text has not been changed.")
        entries = []
        for folder in ("papers", "concepts", "topics"):
            for note in sorted((project.vault / folder).rglob("*.md")):
                meta, _ = frontmatter(note)
                title = str(meta.get("title") or note.stem).replace("\n", " ").replace("[", "\\[").replace("]", "\\]")
                description = str(meta.get("description", "")).replace("\n", " ")
                # Angle brackets permit spaces/Unicode in standard Markdown link targets.
                from urllib.parse import quote
                target = quote(note.relative_to(project.vault).as_posix(), safe="/-._~")
                entries.append(f"- [{title}](<{target}>)" + (f" — {description}" if description else ""))
        block = START + "\n" + "\n".join(entries) + "\n" + END
        updated = original[:original.index(START)] + block + original[original.index(END) + len(END):]
        if updated != original:
            atomic_write(path, updated)
            log = project.vault / "log.md"
            old_log = log.read_text(encoding="utf-8") if log.exists() else "# Wiki log\n"
            atomic_write(log, old_log + f"\n## [{now()}] index | Refreshed {len(entries)} page entries\n")
    return {"index": str(path), "entries": len(entries), "changed": updated != original}
