import argparse
import importlib.util
import json
import os
import platform
import shutil
import sys
from pathlib import Path

from .core import Project, WikiError, import_pdf, prepare_paper
from .review import build_review
from .llm_wiki import lint_llm_wiki, review_context
from .zotero import Zotero
from .zotero_wiki import build_ingest_plan


def doctor(project):
    checks = {"root": str(project.root), "python": platform.python_version(), "python_executable": sys.executable,
              "os": platform.platform(), "running_in_wsl": "microsoft" in platform.release().lower(),
              "dependencies": {name: importlib.util.find_spec(name) is not None for name in ("pymupdf", "yaml", "markdown_it")},
              "tools": {name: project.executable(name) for name in ("git", "latex")},
              "optional_pdf_tools": {name: shutil.which(name) for name in ("pdftoppm", "pdfinfo", "tesseract")},
              "paths": {name: {"exists": (project.root / name).is_dir(), "writable": os.access(project.root / name, os.W_OK)}
                        for name in ("sources/inbox", "sources/metadata", "llm-wiki-data", "reviews", ".cache")}}
    try:
        checks["zotero"] = Zotero(project).probe()
    except WikiError as exc:
        checks["zotero"] = {"reachable": False, "reason": str(exc)}
    checks["manual_pdf_ready"] = all(checks["dependencies"].values()) and checks["paths"]["sources/metadata"]["writable"]
    checks["review_pdf_ready"] = bool(checks["tools"]["latex"]) and checks["dependencies"]["pymupdf"]
    return checks


def parser():
    p = argparse.ArgumentParser(description="Paper research tools for an LLM Wiki project. Analysis and writing are performed by Codex.")
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Project root (default: this checkout)")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Report capabilities without displaying secrets")
    imp = sub.add_parser("import-pdf", help="Register immutable PDF and local path; does not generate analysis")
    imp.add_argument("pdf")
    for arg in ("title", "doi", "arxiv-id", "version", "source-url", "revision-of"):
        imp.add_argument("--" + arg)
    imp.add_argument("--author", dest="authors", action="append")
    imp.add_argument("--year", type=int)
    prep = sub.add_parser("prepare-paper", help="Extract per-page text; render only explicitly selected pages")
    prep.add_argument("source_id")
    prep.add_argument("--pages", help="1-based PDF page indices, e.g. 1,3-5")
    prep.add_argument("--dpi", type=int, default=120)
    resolve = sub.add_parser("resolve-pdf", help="Resolve and verify a local PDF path")
    resolve.add_argument("source_id")
    lint = sub.add_parser("lint-llm-wiki", help="Validate LLM Wiki provenance, wikilinks, and index; not scientific truth")
    lint.add_argument("--wiki-root", type=Path, required=True, help="LLM Wiki project root containing wiki/")
    review = sub.add_parser("build-review", help="Compile editable LaTeX; verify page count and logs")
    review.add_argument("tex")
    review.add_argument("--expected-pages", type=int)
    context = sub.add_parser("llm-wiki-review-context", help="List read-only LLM Wiki pages relevant to one PDF source")
    context.add_argument("--wiki-root", type=Path, required=True, help="LLM Wiki project root containing wiki")
    context.add_argument("--source", required=True, help="raw/sources path or zotero://users/0/items/ITEMKEY URI")
    context.add_argument("--wiki-page", dest="pages", action="append", help="Optional explicit Markdown page relative to that root")
    listing = sub.add_parser("zotero-list", help="Read a bounded explicit selection")
    selection = listing.add_mutually_exclusive_group(required=True)
    selection.add_argument("--collections", action="store_true")
    selection.add_argument("--collection")
    selection.add_argument("--items")
    listing.add_argument("--limit", type=int, default=20)
    listing.add_argument("--start", type=int, default=0)
    zs = sub.add_parser("zotero-selected", help="Show the current Zotero selection; requires the selection plugin")
    zs.add_argument("--view", choices=("auto", "library", "reader"), default="auto")
    zi = sub.add_parser("zotero-import", help="Import one paper and one existing local PDF attachment (GET only)")
    zi.add_argument("item", nargs="?")
    zi.add_argument("--selected", action="store_true", help="Import the currently selected paper or active PDF")
    zi.add_argument("--view", choices=("auto", "library", "reader"), default="auto")
    zi.add_argument("--attachment")
    zi.add_argument("--version")
    zi.add_argument("--revision-of")
    zw = sub.add_parser("zotero-wiki-plan", help="Register a bounded Zotero scope and plan Codex-authored LLM Wiki pages; never copies PDFs")
    zw_scope = zw.add_mutually_exclusive_group(required=True)
    zw_scope.add_argument("--collection")
    zw_scope.add_argument("--items", help="Comma-separated top-level Zotero item keys")
    zw.add_argument("--wiki-root", type=Path, required=True)
    zw.add_argument("--limit", type=int, default=20)
    zw.add_argument("--start", type=int, default=0)
    zw.add_argument("--prepare", action="store_true", help="Also extract per-page text into ignored ShadowNote cache")
    return p


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    args = vars(parser().parse_args(argv))
    root, command = args.pop("root"), args.pop("command")
    try:
        project = Project(root)
        code = 0
        if command == "doctor":
            output = doctor(project)
        elif command == "import-pdf":
            output = import_pdf(project, args.pop("pdf"), **args)
        elif command == "prepare-paper":
            output = prepare_paper(project, **args)
        elif command == "resolve-pdf":
            output = {"pdf": str(project.resolve_pdf(args["source_id"]))}
        elif command == "lint-llm-wiki":
            output = lint_llm_wiki(args["wiki_root"])
            code = 1 if output["errors"] else 0
        elif command == "build-review":
            if args["expected_pages"] is not None and args["expected_pages"] < 1:
                raise WikiError("expected-pages must be >= 1")
            output = build_review(project, **args)
        elif command == "llm-wiki-review-context":
            output = review_context(args["wiki_root"], args["source"], args["pages"], project)
        elif command == "zotero-list":
            output = Zotero(project).listing(**args)
        elif command == "zotero-selected":
            output = Zotero(project).selected(**args)
        elif command == "zotero-wiki-plan":
            output = build_ingest_plan(project, **args)
        else:
            item, selected, view = args.pop("item"), args.pop("selected"), args.pop("view")
            if bool(item) == selected:
                raise WikiError("Use either zotero-import ITEM_KEY or zotero-import --selected.")
            client = Zotero(project)
            if selected:
                output = client.import_selected(view=view, **args)
            else:
                if view != "auto":
                    raise WikiError("--view requires --selected.")
                output = client.import_item(item, **args)
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return code
    except (WikiError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
