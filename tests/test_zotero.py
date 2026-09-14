"""Synthetic HTTP contract tests, not the user's live Zotero."""
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from paperwiki.core import Project, WikiError, import_pdf
from paperwiki.zotero import Zotero
from paperwiki.zotero_wiki import build_ingest_plan
from test_workflow import synthetic_pdf

class ZoteroContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pdf = self.root / "中文 attachment.pdf"
        synthetic_pdf(self.pdf)
        self.requests, self.mode = [], "normal"
        self.snapshot = {"schema_version": 1, "selection_kind": "reader-tab", "problem": None,
                         "items": [{"item_key": "PAPER123", "attachment_key": "ATTACH12",
                                    "library": "users/0", "problem": None}]}
        owner = self
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                owner.requests.append((self.command, self.path))
                path = urlsplit(self.path).path
                status = 200
                headers = {"Zotero-API-Version": "3", "Zotero-Server-ID": "synthetic-server"}
                item = {"key": "PAPER123", "version": 7, "data": {"itemType": "journalArticle",
                        "title": "Synthetic metadata fixture", "date": "2024-01-01",
                        "creators": [{"creatorType": "author", "firstName": "Test", "lastName": "Author"}]}}
                attachment = {"key": "ATTACH12", "data": {"itemType": "attachment",
                              "contentType": "application/pdf", "parentItem": "PAPER123"}}
                value = {}
                if owner.mode == "forbidden":
                    status = 403
                elif path == "/api/":
                    pass
                elif path == "/api/paper-wiki/selection":
                    if owner.mode == "no_bridge":
                        status = 404
                    elif self.headers.get("X-Paper-Wiki") != "1":
                        status = 403
                    else:
                        value = owner.snapshot
                elif path.endswith("/collections/COLLECT1/items/top"):
                    value = [item]
                elif path.endswith("/collections"):
                    value = [{"key": "COLLECT1", "data": {"name": "Synthetic collection"}}]
                elif path.endswith("/items/PAPER123"):
                    value = item
                elif path.endswith("/items/ATTACH12"):
                    value = attachment
                elif path.endswith("/items/PAPER123/children"):
                    value = [attachment]
                    if owner.mode == "multiple":
                        value.append({"key": "ATTACH34", "data": attachment["data"]})
                elif path.endswith("/file/view/url"):
                    if owner.mode == "redirect":
                        status = 404
                    else:
                        value = owner.pdf.as_uri()
                elif path.endswith("/file"):
                    status = 302
                    headers["Location"] = owner.pdf.as_uri()
                elif path.endswith("/items"):
                    value = [item, attachment]
                else:
                    status = 404
                body = value.encode() if isinstance(value, str) else json.dumps(value).encode()
                self.send_response(status)
                for key, value in headers.items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(body)
            def log_message(self, *args):
                pass
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.project = Project(self.root)
        self.project.config = {"zotero": {"base_url": f"http://127.0.0.1:{self.server.server_port}/api/"}}
    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
    def test_get_only_bounded_listing_and_alias_import(self):
        sid = import_pdf(self.project, self.pdf)["source_id"]
        client = Zotero(self.project)
        listing = client.listing(items="PAPER123", limit=1)
        self.assertEqual(listing["items"][0]["key"], "PAPER123")
        query = parse_qs(urlsplit(self.requests[-1][1]).query)
        self.assertEqual(query["limit"], ["1"])
        self.assertEqual(query["itemKey"], ["PAPER123"])
        result = client.import_item("PAPER123")
        self.assertEqual(result["source_id"], sid)
        self.assertTrue(result["duplicate"])
        record = self.project.record(sid)
        self.assertEqual(record["authors"], ["Test Author"])
        self.assertEqual(record["year"], 2024)
        self.assertEqual(record["zotero"][0]["server_id"], "synthetic-server")
        self.assertEqual(record["version"], "")
        self.assertTrue(all(method == "GET" for method, _ in self.requests))

    def test_collection_plan_registers_and_prepares_without_copying_pdf_or_wiki_text(self):
        wiki_root = self.root / "llm-wiki-data"
        (wiki_root / "wiki/sources").mkdir(parents=True)
        raw = wiki_root / "raw/sources"
        raw.mkdir(parents=True)
        result = build_ingest_plan(self.project, wiki_root, collection="COLLECT1", limit=1, prepare=True)
        self.assertFalse(result["pdf_copy_performed"])
        self.assertEqual(len(result["ready"]), 1)
        self.assertEqual(result["unavailable"], [])
        item = result["ready"][0]
        self.assertEqual(item["source_uri"], "zotero://users/0/items/PAPER123")
        self.assertEqual(Path(item["local_pdf"]), self.pdf)
        self.assertTrue(Path(item["prepared_cache"]).joinpath("page-0001.txt").is_file())
        self.assertEqual(list(raw.iterdir()), [])
        self.assertFalse((wiki_root / item["target_page"]).exists())
        self.assertTrue(all(method == "GET" for method, _ in self.requests))
    def test_redirect_resolved_locally(self):
        self.mode = "redirect"
        result = Zotero(self.project).import_item("PAPER123")
        self.assertEqual(self.project.resolve_pdf(result["source_id"]), self.pdf)
    def test_multiple_attachments_require_selection(self):
        self.mode = "multiple"
        with self.assertRaisesRegex(WikiError, "Select one PDF"):
            Zotero(self.project).import_item("PAPER123")
        self.assertEqual(len(self.project.records()), 0)
        self.assertTrue(Zotero(self.project).import_item("PAPER123", attachment="ATTACH12")["source_id"])
    def test_forbidden_and_missing_local_attachment(self):
        self.mode = "forbidden"
        with self.assertRaisesRegex(WikiError, "403.*Enable"):
            Zotero(self.project).probe()
        self.mode = "normal"
        self.pdf.unlink()
        with self.assertRaisesRegex(WikiError, "not available"):
            Zotero(self.project).import_item("PAPER123")
        self.assertEqual(len(self.project.records()), 0)

    def test_selected_reader_uses_exact_pdf_and_only_get(self):
        self.mode = "multiple"
        client = Zotero(self.project)
        result = client.import_selected(version="v2")
        record = self.project.record(result["source_id"])
        self.assertEqual(record["version"], "v2")
        self.assertEqual(record["zotero"][0]["attachment_key"], "ATTACH12")
        self.assertTrue(all(method == "GET" for method, _ in self.requests))
        self.assertFalse(any("/children" in path for _, path in self.requests))
        selection = [path for _, path in self.requests if "selection" in path]
        self.assertEqual(len(selection), 1)
        self.assertEqual(parse_qs(urlsplit(selection[0]).query), {"view": ["auto"]})

    def test_group_selection_scopes_requests_and_restores_client(self):
        self.snapshot["items"][0]["library"] = "groups/1234"
        client = Zotero(self.project)
        result = client.import_selected(view="library")
        self.assertEqual(self.project.record(result["source_id"])["zotero"][0]["library"], "groups/1234")
        self.assertEqual(client.library, "users/0")
        item_paths = [path for _, path in self.requests if "/items/" in path]
        self.assertTrue(all(path.startswith("/api/groups/1234/") for path in item_paths))

    def test_no_ambiguous_selection_or_invalid_target_is_imported(self):
        original = self.snapshot["items"][0].copy()
        for items, problem, message in [([], None, "exactly one"),
                ([original, original], None, "exactly one"),
                ([original], "No reader active", "No reader"),
                ([dict(original, problem="Standalone PDF")], None, "Standalone"),
                ([dict(original, library="../bad")], None, "unsupported library")]:
            with self.subTest(message=message):
                self.snapshot.update(items=items, problem=problem)
                self.requests.clear()
                with self.assertRaisesRegex(WikiError, message):
                    Zotero(self.project).import_selected()
                self.assertEqual(len(self.project.records()), 0)
                self.assertFalse(any("/items/" in path for _, path in self.requests))

    def test_bridge_missing_invalid_and_missing_file(self):
        client = Zotero(self.project)
        self.mode = "no_bridge"
        with self.assertRaisesRegex(WikiError, "bridge is not installed"):
            client.selected()
        self.mode = "normal"
        self.snapshot["schema_version"] = 99
        with self.assertRaisesRegex(WikiError, "Unsupported selection"):
            client.selected()
        self.snapshot["schema_version"] = 1
        self.pdf.unlink()
        self.assertEqual(client.selected()["items"][0]["item_key"], "PAPER123")
        with self.assertRaisesRegex(WikiError, "not available"):
            client.import_selected()
        self.assertEqual(len(self.project.records()), 0)

    def test_selected_pdf_cannot_be_overridden_silently(self):
        with self.assertRaisesRegex(WikiError, "conflicts"):
            Zotero(self.project).import_selected(attachment="ATTACH34")
        self.assertEqual(len(self.project.records()), 0)

    def test_selected_cli_round_trip_and_invalid_arguments(self):
        (self.root / "config.local.toml").write_text(
            f'[zotero]\nbase_url = "{self.project.config["zotero"]["base_url"]}"\n', encoding="utf-8")
        script = Path(__file__).resolve().parents[1] / "scripts/paper_wiki.py"
        def run(*args):
            return subprocess.run([sys.executable, str(script), "--root", str(self.root), *args],
                                  capture_output=True, encoding="utf-8", timeout=20)
        snapshot = run("zotero-selected")
        self.assertEqual(snapshot.returncode, 0, snapshot.stderr)
        self.assertEqual(json.loads(snapshot.stdout)["items"][0]["item_key"], "PAPER123")
        imported = run("zotero-import", "--selected")
        self.assertEqual(imported.returncode, 0, imported.stderr)
        source_id = json.loads(imported.stdout)["source_id"]
        prepared = run("prepare-paper", source_id)
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        self.assertTrue((self.root / ".cache/papers" / source_id / "page-0001.txt").is_file())
        for args in [("zotero-import",), ("zotero-import", "PAPER123", "--selected"),
                     ("zotero-import", "PAPER123", "--view", "library")]:
            result = run(*args)
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertIn("ERROR:", result.stderr)
