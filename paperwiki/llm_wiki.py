"""Read-only helpers and structural validation for an LLM Wiki project."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from .core import Project, WikiError

WIKILINK = re.compile(r"\[\[([^\]|#]+)")
ZOTERO_SOURCE = re.compile(r"^zotero://((?:users|groups)/\d+)/items/([A-Z0-9]{8})$")
SOURCE_ID = re.compile(r"^p-([a-f0-9]{64})$")
CONTENT_VERSION = re.compile(r"^sha256:([a-f0-9]{64})$")
CONTENT_TYPES = {"source", "concept", "entity", "comparison", "synthesis", "query"}


def _relative(root: Path, value: str | Path, label: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise WikiError(f"{label} must be relative to the LLM Wiki project root.")
    resolved = (root / path).resolve()
    try:
        return resolved.relative_to(root)
    except ValueError as exc:
        raise WikiError(f"{label} must stay inside the LLM Wiki project root.") from exc


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    try:
        value = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


def _source_values(value):
    if isinstance(value, str):
        yield value.replace(chr(92), "/")
    elif isinstance(value, list):
        for item in value:
            yield from _source_values(item)
    elif isinstance(value, dict):
        for key in ("path", "file", "source", "source_path"):
            yield from _source_values(value.get(key))


def _wikilinks(path: Path) -> set[str]:
    return {
        match.group(1).strip()
        for match in WIKILINK.finditer(path.read_text(encoding="utf-8"))
        if match.group(1).strip()
    }


def _markdown_pages(wiki: Path) -> list[Path]:
    return sorted(path for path in wiki.rglob("*.md") if path.is_file())


def _relative_page(wiki: Path, path: Path) -> str:
    return path.relative_to(wiki).as_posix()


def _resolve_wikilink(wiki: Path, target: str, pages: list[Path]) -> Path | None:
    """Resolve root-relative or uniquely named LLM Wiki links."""
    value = target.strip().replace(chr(92), "/")
    if not value:
        return None
    if value.endswith(".md"):
        value = value[:-3]
    if "/" in value:
        candidate = (wiki / f"{value}.md").resolve()
        try:
            candidate.relative_to(wiki)
        except ValueError:
            return None
        return candidate if candidate in pages else None
    matches = [page for page in pages if page.stem == value]
    return matches[0] if len(matches) == 1 else None


def _linked_pages(wiki: Path, page: Path, pages: list[Path]) -> list[Path]:
    linked: list[Path] = []
    for target in _wikilinks(page):
        resolved = _resolve_wikilink(wiki, target, pages)
        if resolved is not None and resolved not in linked:
            linked.append(resolved)
    return linked


def _source_error(root: Path, source: str) -> str | None:
    if ZOTERO_SOURCE.fullmatch(source):
        return None
    try:
        relative = _relative(root, source, "source")
    except WikiError as exc:
        return str(exc)
    if not relative.as_posix().startswith("raw/sources/"):
        return "source must be inside raw/sources/ or be a zotero:// library item URI"
    if not (root / relative).is_file():
        return f"LLM Wiki source not found: {root / relative}"
    return None


def lint_llm_wiki(root: str | Path) -> dict:
    """Validate portable provenance and graph structure without writing files.

    Passing this check does not establish that a page's scientific statements
    are correct; those still require an original-PDF check.
    """
    root = Path(root).expanduser().resolve()
    wiki = root / "wiki"
    errors: list[str] = []
    warnings: list[str] = []
    if not wiki.is_dir():
        return {
            "wiki_root": str(root),
            "pages": 0,
            "errors": ["Expected an LLM Wiki project containing wiki/."],
            "warnings": warnings,
        }
    pages = _markdown_pages(wiki)
    index = wiki / "index.md"
    if not index.is_file():
        errors.append(f"{index}: required Wiki index is missing")
    indexed = set(_linked_pages(wiki, index, pages)) if index.is_file() else set()

    for page in pages:
        relative = _relative_page(wiki, page)
        frontmatter = _frontmatter(page)
        page_type = frontmatter.get("type")
        if page.name not in {"index.md", "log.md"}:
            if not isinstance(page_type, str) or not page_type:
                errors.append(f"{relative}: missing frontmatter type")
            if page_type in CONTENT_TYPES:
                if not isinstance(frontmatter.get("title"), str) or not frontmatter["title"].strip():
                    errors.append(f"{relative}: missing frontmatter title")
                source_id = frontmatter.get("source_id")
                version = frontmatter.get("content_version")
                if not isinstance(source_id, str) or not SOURCE_ID.fullmatch(source_id):
                    errors.append(f"{relative}: source_id must be p- followed by a SHA-256 digest")
                if not isinstance(version, str) or not CONTENT_VERSION.fullmatch(version):
                    errors.append(f"{relative}: content_version must be sha256: followed by a digest")
                elif isinstance(source_id, str) and SOURCE_ID.fullmatch(source_id) and version != f"sha256:{source_id[2:]}":
                    errors.append(f"{relative}: content_version does not match source_id")
                values = list(_source_values(frontmatter.get("sources")))
                if not values:
                    errors.append(f"{relative}: sources must name at least one source")
                for source in values:
                    problem = _source_error(root, source)
                    if problem:
                        errors.append(f"{relative}: {problem}")
            elif page_type not in {"overview", None}:
                warnings.append(f"{relative}: unrecognized page type {page_type!r}")

        for target in _wikilinks(page):
            if _resolve_wikilink(wiki, target, pages) is None:
                errors.append(f"{relative}: broken or ambiguous wikilink [[{target}]]")
        if page_type in CONTENT_TYPES and page not in indexed:
            warnings.append(f"{relative}: content page is not linked from index.md")

    return {"wiki_root": str(root), "pages": len(pages), "errors": errors, "warnings": warnings}


def matching_source_pages(root: str | Path, source: str) -> list[Path]:
    """Return Markdown pages whose frontmatter names one exact source value."""
    root = Path(root).expanduser().resolve()
    wiki = root / "wiki"
    if not wiki.is_dir():
        raise WikiError("Expected an LLM Wiki project containing wiki/.")
    return [
        path for path in _markdown_pages(wiki)
        if _frontmatter(path).get("type") == "source"
        and source in set(_source_values(_frontmatter(path).get("sources")))
    ]


def _zotero_record(project: Project, library: str, item_key: str, pages: list[Path]) -> dict:
    page_ids = {_frontmatter(path).get("source_id") for path in pages}
    page_ids = {value for value in page_ids if isinstance(value, str)}
    candidates = []
    for record in project.records():
        aliases = record.get("zotero", [])
        if any(alias.get("library") == library and alias.get("item_key") == item_key for alias in aliases):
            if not page_ids or record.get("source_id") in page_ids:
                candidates.append(record)
    if not candidates:
        raise WikiError("Zotero source is not registered locally. Run zotero-wiki-plan for this item or collection first.")
    if len(candidates) != 1:
        raise WikiError("Multiple PDF versions match this Zotero item. Set the source page's source_id to the intended version.")
    return candidates[0]


def review_context(root: str | Path, source: str, pages: list[str] | None = None, project: Project | None = None) -> dict:
    """Return related LLM Wiki pages and resolve the original PDF without writing."""
    root = Path(root).expanduser().resolve()
    wiki = root / "wiki"
    if not wiki.is_dir():
        raise WikiError("Expected an LLM Wiki project containing wiki/.")
    zotero_match = ZOTERO_SOURCE.fullmatch(source)
    if zotero_match:
        source_key, source_path, source_kind = source, None, "zotero"
    else:
        if not (root / "raw/sources").is_dir():
            raise WikiError("Expected an LLM Wiki project containing raw/sources/ for a file source.")
        relative_source = _relative(root, source, "source")
        if not relative_source.as_posix().startswith("raw/sources/"):
            raise WikiError("source must be inside raw/sources/ or be a zotero:// library item URI.")
        source_path = root / relative_source
        if not source_path.is_file():
            raise WikiError(f"LLM Wiki source not found: {source_path}")
        source_key, source_kind = relative_source.as_posix(), "file"

    markdown = _markdown_pages(wiki)
    requested: list[Path] = []
    for page in pages or []:
        relative_page = _relative(root, page, "wiki page")
        resolved = root / relative_page
        if not resolved.is_file() or wiki not in resolved.parents:
            raise WikiError("wiki page must be an existing Markdown file inside wiki/.")
        requested.append(resolved)
    primary = list(dict.fromkeys([*requested, *matching_source_pages(root, source_key)]))
    linked: list[Path] = []
    for primary_page in primary:
        for linked_page in _linked_pages(wiki, primary_page, markdown):
            if linked_page not in primary and linked_page not in linked:
                linked.append(linked_page)
    primary_set = set(primary)
    backlinks = [
        page for page in markdown
        if page not in primary_set and page not in linked
        and primary_set.intersection(_linked_pages(wiki, page, markdown))
    ]

    def output_path(path: Path) -> str:
        return path.relative_to(root).as_posix()

    source_id = None
    original = source_path
    if zotero_match:
        if project is None:
            raise WikiError("A ShadowNote project is required to resolve a zotero:// source.")
        record = _zotero_record(project, zotero_match[1], zotero_match[2], primary)
        source_id = record["source_id"]
        original = project.resolve_pdf(source_id)
    assert original is not None
    return {
        "wiki_root": str(root),
        "source": source_key,
        "source_kind": source_kind,
        "source_id": source_id,
        "original_pdf": str(original) if zotero_match else output_path(original),
        "source_pages": [output_path(path) for path in primary],
        "linked_pages": [output_path(path) for path in linked],
        "backlink_pages": [output_path(path) for path in backlinks],
        "suggested_read_order": [
            str(original) if zotero_match else output_path(original),
            *map(output_path, primary),
            *map(output_path, linked),
            *map(output_path, backlinks),
        ],
        "notice": "Wiki pages are context only. Verify review claims, numbers, and criticism against the original PDF.",
    }
