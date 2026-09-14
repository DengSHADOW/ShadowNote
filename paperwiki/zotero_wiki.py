"""Build bounded Zotero-to-LLM-Wiki ingest plans without copying PDFs."""

from __future__ import annotations

import re
from pathlib import Path

from .core import Project, WikiError, prepare_paper
from .llm_wiki import matching_source_pages
from .zotero import Zotero


def zotero_source_uri(library: str, item_key: str) -> str:
    if not re.fullmatch(r"(?:users|groups)/\d+", library):
        raise WikiError("Unsupported Zotero library identifier.")
    return f"zotero://{library}/items/{Zotero.key(item_key)}"


def _target_page(root: Path, library: str, item_key: str) -> Path:
    library_slug = library.replace("/", "-")
    return root / "wiki" / "sources" / f"zotero-{library_slug}-{item_key}.md"


def build_ingest_plan(project: Project, wiki_root, *, collection=None, items=None,
                      limit=20, start=0, prepare=False):
    """Register a bounded Zotero scope and describe pages Codex may create.

    Zotero is accessed with GET only. PDF bytes stay at Zotero's local attachment
    path; this function only writes ShadowNote source records/local path mappings
    and, when requested, ignored extraction cache files.
    """
    root = Path(wiki_root).expanduser().resolve()
    wiki = root / "wiki"
    if not wiki.is_dir():
        raise WikiError("Expected an LLM Wiki project containing wiki/.")
    if bool(collection) == bool(items):
        raise WikiError("Use exactly one of collection or items for a bounded Zotero scope.")

    client = Zotero(project)
    listing = client.listing(collection=collection, items=items, limit=limit, start=start)
    planned = []
    unavailable = []
    for listed in listing["items"]:
        key = listed.get("key")
        if listed.get("parent_item"):
            continue
        if listed.get("item_type") in {"attachment", "annotation", "note"}:
            unavailable.append({"item_key": key, "title": listed.get("title"),
                                "reason": "Use a top-level paper item, not a child attachment, annotation, or note."})
            continue
        try:
            imported = client.import_item(key)
            source_id = imported["source_id"]
            record = project.record(source_id)
            pdf = project.resolve_pdf(source_id)
            source_uri = zotero_source_uri(client.library, key)
            matches = matching_source_pages(root, source_uri)
            target = matches[0] if matches else _target_page(root, client.library, key)
            prepared = prepare_paper(project, source_id) if prepare else None
            alias = next((value for value in record.get("zotero", [])
                          if value.get("library") == client.library and value.get("item_key") == key), {})
            planned.append({
                "status": "ready",
                "item_key": key,
                "attachment_key": alias.get("attachment_key"),
                "title": record.get("title") or listed.get("title") or "",
                "authors": record.get("authors", []),
                "year": record.get("year"),
                "source_id": source_id,
                "content_version": record.get("content_version"),
                "source_uri": source_uri,
                "local_pdf": str(pdf),
                "prepared_cache": prepared["cache"] if prepared else None,
                "target_page": target.relative_to(root).as_posix(),
                "page_exists": target.is_file(),
                "frontmatter": {
                    "type": "source",
                    "title": record.get("title") or listed.get("title") or "",
                    "source_id": source_id,
                    "content_version": record.get("content_version"),
                    "zotero_item": key,
                    "zotero_attachment": alias.get("attachment_key"),
                    "sources": [source_uri],
                },
            })
        except WikiError as exc:
            unavailable.append({"item_key": key, "title": listed.get("title"), "reason": str(exc)})

    return {
        "schema_version": 1,
        "scope": {"library": client.library, "collection": collection, "items": items,
                  "start": start, "limit": limit},
        "wiki_root": str(root),
        "pdf_copy_performed": False,
        "prepared": bool(prepare),
        "ready": planned,
        "unavailable": unavailable,
        "next_start_if_more": listing["next_start_if_more"],
        "instructions": (
            "For each ready item, Codex reads local_pdf (and prepared_cache when present), "
            "then creates or locally updates target_page while preserving user edits. "
            "Use the supplied frontmatter. This deterministic command does not write wiki pages or summaries."
        ),
    }
