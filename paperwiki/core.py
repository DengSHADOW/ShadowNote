from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import tempfile
import tomllib
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit


class WikiError(Exception):
    """An actionable user-facing failure."""


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path, default=None):
    if not path.exists() and default is not None:
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        raise WikiError(f"Cannot read JSON: {path}: {exc}") from exc


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".write-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def write_json(path, data):
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def safe_id(value):
    if not re.fullmatch(r"p-[0-9a-f]{64}", value):
        raise WikiError("Invalid source_id; use the p-<SHA256> returned by import-pdf.")
    return value


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pdf_module():
    try:
        import pymupdf
        return pymupdf
    except ImportError as exc:
        raise WikiError("PyMuPDF missing. Install project dependencies: python -m pip install -e .") from exc


def local_path(value, config=None, system=None):
    """Resolve local paths/file URLs, never fetch attachment URLs over HTTP."""
    system = system or platform.system()
    config = config or {}
    value = str(value).strip()
    if value.lower().startswith("file:"):
        parsed = urlsplit(value)
        if parsed.netloc not in ("", "localhost"):
            raise WikiError("Network file URL is unsupported; copy the PDF locally and use import-pdf.")
        value = unquote(parsed.path)
        if re.match(r"^/[A-Za-z]:/", value):
            value = value[1:]
    elif "://" in value:
        raise WikiError("Expected a local PDF path or file URL, not a download URL.")
    if value.startswith(("\\\\", "//")):
        raise WikiError("UNC paths are unsupported; use a local PDF copy.")
    if re.match(r"^[A-Za-z]:[\\/]", value) and system != "Windows":
        drive = value[0].upper()
        mounts = config.get("paths", {}).get("windows_drives", {})
        mount = mounts.get(drive)
        if not mount:
            raise WikiError(f"Windows drive {drive}: needs paths.windows_drives.{drive} in config.local.toml; or import a local PDF.")
        value = str(Path(mount) / value[3:].replace("\\", "/"))
    return Path(value).expanduser().resolve()


class Project:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.metadata = self.root / "sources/metadata"
        self.vault = self.root / "vault"
        self.cache = self.root / ".cache"
        self.paths = self.root / "sources/local-paths.json"
        config = self.root / "config.local.toml"
        try:
            self.config = tomllib.loads(config.read_text(encoding="utf-8-sig")) if config.exists() else {}
        except (ValueError, OSError) as exc:
            raise WikiError("Cannot read config.local.toml; check TOML syntax (single quotes for Windows paths).") from exc

    @contextmanager
    def lock(self):
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.root / ".paper-wiki.lock"
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise WikiError("Project is locked. Wait for the other command; after a crash, verify no command is running before removing .paper-wiki.lock.") from exc
        try:
            with os.fdopen(fd, "w") as stream:
                stream.write(str(os.getpid()))
            yield
        finally:
            path.unlink(missing_ok=True)

    def records(self):
        return [read_json(p) for p in sorted(self.metadata.glob("*.json"))]

    def record(self, source_id):
        path = self.metadata / f"{safe_id(source_id)}.json"
        if not path.exists():
            raise WikiError(f"Source not found: {source_id}")
        return read_json(path)

    def resolve_pdf(self, source_id):
        record = self.record(source_id)
        paths = read_json(self.paths, {}).get(source_id, [])
        for value in reversed(paths):
            path = local_path(value, self.config)
            if path.is_file() and file_hash(path) == record["pdf_sha256"]:
                return path
        raise WikiError(f"Missing or changed PDF for {source_id}. Re-import the original PDF to restore its local path; import a revision explicitly for changed content.")

    def executable(self, name):
        custom = self.config.get("tools", {}).get(name)
        if custom:
            return shutil.which(custom) or (str(Path(custom)) if Path(custom).is_file() else None)
        if name == "latex":
            return next((p for n in ("pdflatex", "xelatex", "lualatex", "tectonic") if (p := shutil.which(n))), None)
        found = shutil.which(name)
        if not found and name == "git" and os.name == "nt":
            fallback = Path("C:/Program Files/Git/cmd/git.exe")
            if fallback.is_file():
                found = str(fallback)
        return found


def import_pdf(project, path, *, title=None, authors=None, year=None, doi=None,
               arxiv_id=None, version=None, source_url=None, revision_of=None, zotero=None):
    path = local_path(path, project.config)
    if not path.is_file():
        raise WikiError(f"PDF not found: {path}")
    pdf = pdf_module()
    try:
        with pdf.open(path) as doc:
            if not doc.is_pdf or doc.needs_pass or not len(doc):
                raise WikiError("Expected a readable, unencrypted, nonempty PDF.")
            embedded = doc.metadata or {}
            page_count = len(doc)
    except (RuntimeError, ValueError) as exc:
        raise WikiError(f"Cannot open PDF: {path}: {exc}") from exc
    digest = file_hash(path)
    source_id = "p-" + digest
    supplied = {"title": title, "authors": authors, "year": year, "doi": doi,
                "arxiv_id": arxiv_id, "version": version, "source_url": source_url}
    if year is not None and not (1000 <= year <= 9999):
        raise WikiError("year must be a four-digit publication year.")
    if source_url and urlsplit(source_url).scheme not in ("https", "http"):
        raise WikiError("source_url must be an HTTP(S) source link.")
    with project.lock():
        existing = project.records()
        target = project.metadata / f"{source_id}.json"
        record = next((r for r in existing if r["source_id"] == source_id), None)
        duplicate = record is not None
        if duplicate:
            for key, value in supplied.items():
                if value not in (None, "", []) and record.get(key) not in (None, "", [], value):
                    raise WikiError(f"Metadata conflict for {key} on identical PDF; inspect {target} before editing. No changes written.")
            if revision_of and record.get("revision_of") != revision_of:
                raise WikiError("Existing revision relationship differs; inspect the source record.")
            for key, value in supplied.items():
                if value not in (None, "", []) and not record.get(key):
                    record[key] = value
        else:
            if revision_of:
                previous = project.record(revision_of)
                if revision_of == source_id or not version or version == previous.get("version"):
                    raise WikiError("A revision needs different PDF bytes and an explicit, different --version label.")
            record = {"schema_version": 1, "source_id": source_id, "pdf_sha256": digest,
                      "content_version": "sha256:" + digest, "title": title or "", "authors": authors or [],
                      "year": year, "doi": doi or "", "arxiv_id": arxiv_id or "", "version": version or "",
                      "source_url": source_url or "", "revision_of": revision_of,
                      "page_count": page_count, "zotero": [], "created_at": now(),
                      "pdf_metadata": {k: embedded.get(k, "") for k in ("title", "author", "creationDate")},
                      "possible_same_paper": []}
            # Candidates are hints, never identity decisions. Every byte revision stays separate.
            for old in existing:
                reasons = [key for key in ("doi", "arxiv_id", "title")
                           if record.get(key) and str(record[key]).casefold() == str(old.get(key, "")).casefold()]
                if reasons and old["source_id"] != revision_of:
                    record["possible_same_paper"].append({"source_id": old["source_id"], "matched_fields": reasons})
        if zotero and zotero not in record["zotero"]:
            record["zotero"].append(zotero)
        if not duplicate or record != read_json(target):
            record["updated_at"] = now()
            write_json(target, record)
        mapping = read_json(project.paths, {})
        values = mapping.setdefault(source_id, [])
        if str(path) not in values:
            values.append(str(path))
            write_json(project.paths, mapping)
    return {"source_id": source_id, "duplicate": duplicate, "metadata": str(target),
            "possible_same_paper": record["possible_same_paper"]}


def selected_pages(spec, count):
    selected = set()
    if not spec:
        return []
    for part in spec.split(","):
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", part.strip())
        if not match:
            raise WikiError("Pages must look like 1,3-5 (1-based PDF page indices).")
        first, last = int(match[1]), int(match[2] or match[1])
        if not 1 <= first <= last <= count:
            raise WikiError(f"Page range {part} outside 1..{count}.")
        selected.update(range(first, last + 1))
    return sorted(selected)


def prepare_paper(project, source_id, pages=None, dpi=120):
    if not 50 <= dpi <= 300:
        raise WikiError("dpi must be between 50 and 300.")
    path = project.resolve_pdf(source_id)
    pdf = pdf_module()
    with project.lock(), pdf.open(path) as doc:
        selected = selected_pages(pages, len(doc))
        out = project.cache / "papers" / source_id
        out.mkdir(parents=True, exist_ok=True)
        extracted = []
        for i, page in enumerate(doc, 1):
            content = page.get_text("text", sort=True)
            atomic_write(out / f"page-{i:04}.txt", content)
            info = {"pdf_page": i, "printed_page": None, "pdf_page_label": page.get_label(),
                    "characters": len(content.strip()), "possible_ocr_needed": len(content.strip()) < 40}
            if i in selected:
                pixmap = page.get_pixmap(dpi=dpi, alpha=False)
                image_path = out / f"page-{i:04}.png"
                temporary = image_path.with_suffix(".tmp.png")
                pixmap.save(temporary)
                os.replace(temporary, image_path)
                info["rendered"] = image_path.name
            extracted.append(info)
        manifest = {"source_id": source_id, "content_version": "sha256:" + file_hash(path),
                    "prepared_at": now(), "pages": extracted, "rendered_this_run": selected,
                    "warning": "Text extraction is not verified reading order. OCR flags are heuristics; figures/tables need visual inspection. Printed page numbers require agent verification."}
        write_json(out / "manifest.json", manifest)
    return {"cache": str(out), "page_count": len(extracted), "rendered": selected,
            "possible_ocr_pages": [p["pdf_page"] for p in extracted if p["possible_ocr_needed"]]}
