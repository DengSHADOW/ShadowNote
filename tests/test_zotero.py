"""Synthetic HTTP contract tests, not the user's live Zotero."""
import json
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from paperwiki.core import Project, WikiError, import_pdf
from paperwiki.zotero import Zotero
from test_workflow import synthetic_pdf

class ZoteroContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pdf = self.root / "中文 attachment.pdf"
        synthetic_pdf(self.pdf)
        self.requests, self.mode = [], "normal"
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
                    value = [item]
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
