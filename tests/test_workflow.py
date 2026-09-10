import json
import tempfile
import unittest
from pathlib import Path

import pymupdf

from paperwiki.core import Project, WikiError, import_pdf, local_path, prepare_paper
from paperwiki.review import build_review, latex_escape
from paperwiki.wiki import lint_wiki, sync_index
from paperwiki.zotero import Zotero


def synthetic_pdf(path, text="Synthetic fixture, not a research paper."):
    path.parent.mkdir(parents=True, exist_ok=True)
    with pymupdf.open() as doc:
        page = doc.new_page()
        page.insert_text((72, 72), text)
        doc.new_page()
        doc.set_metadata({"title": "Synthetic fixture", "author": "Test generator"})
        doc.save(path)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = Project(self.root)
        for folder in ("sources/inbox", "sources/metadata", "vault/notes", "vault/papers", "vault/concepts", "vault/topics", "reviews", ".cache"):
            (self.root / folder).mkdir(parents=True)
        (self.root / "vault/index.md").write_text("# Index\n\nUser introduction\n<!-- paper-wiki:index:start -->\n\n<!-- paper-wiki:index:end -->\n", encoding="utf-8")
        self.path = self.root / "sources/inbox/中文 空格.pdf"
        synthetic_pdf(self.path)

    def imported(self, **kwargs):
        return import_pdf(self.project, self.path, **kwargs)["source_id"]

    def note(self, sid, name="analysis", link=""):
        content = "---\ntitle: Synthetic test\nstatus: draft\ndescription: Tool verification only\nsources:\n  - source_id: " + sid + "\n    content_version: sha256:" + sid[2:] + "\n---\n# Synthetic test\n" + link
        path = self.root / f"vault/papers/{sid}/{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_duplicate_unicode_path_and_user_content_unchanged(self):
        notes = self.root / "vault/notes/我的笔记.md"
        notes.write_text("My manual notes: keep unchanged.", encoding="utf-8")
        before = self.path.read_bytes()
        sid = self.imported()
        analysis = self.note(sid)
        analysis_before = analysis.read_bytes()
        metadata_before = (self.project.metadata / f"{sid}.json").read_bytes()
        second = import_pdf(self.project, self.path)
        self.assertTrue(second["duplicate"])
        self.assertEqual(sid, second["source_id"])
        self.assertEqual(len(self.project.records()), 1)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(analysis.read_bytes(), analysis_before)
        self.assertEqual((self.project.metadata / f"{sid}.json").read_bytes(), metadata_before)
        self.assertEqual(notes.read_text(encoding="utf-8"), "My manual notes: keep unchanged.")
        self.assertEqual(self.project.resolve_pdf(sid), self.path)
        self.assertNotIn(str(self.root), json.dumps(self.project.record(sid)))

    def test_same_title_separate_hashes_candidate_not_merge(self):
        first = self.imported(title="Same title", doi="10.test/one")
        other = self.root / "second.pdf"
        synthetic_pdf(other, "Different paper content, synthetic only.")
        result = import_pdf(self.project, other, title="Same title", doi="10.test/two")
        self.assertNotEqual(first, result["source_id"])
        self.assertEqual(len(self.project.records()), 2)
        self.assertEqual(result["possible_same_paper"][0]["source_id"], first)

    def test_explicit_revision_preserves_original_and_validates_label(self):
        old = self.imported(version="v1")
        other = self.root / "revision.pdf"
        synthetic_pdf(other, "A revised synthetic document.")
        with self.assertRaisesRegex(WikiError, "explicit"):
            import_pdf(self.project, other, revision_of=old)
        new = import_pdf(self.project, other, revision_of=old, version="v2")["source_id"]
        self.assertEqual(self.project.record(new)["revision_of"], old)
        self.assertEqual(self.project.record(old)["version"], "v1")
        self.assertEqual(self.project.resolve_pdf(old), self.path)

    def test_duplicate_alias_enrichment_and_conflict(self):
        sid = self.imported()
        alias = {"library": "users/0", "item_key": "ABCD1234", "server_id": "test-only"}
        import_pdf(self.project, self.path, title="Verified title", zotero=alias)
        import_pdf(self.project, self.path, title="Verified title", zotero=alias)
        self.assertEqual(self.project.record(sid)["zotero"], [alias])
        with self.assertRaisesRegex(WikiError, "Metadata conflict"):
            import_pdf(self.project, self.path, title="Conflicting title")
        self.assertEqual(self.project.record(sid)["title"], "Verified title")

    def test_extract_only_and_selective_render_and_missing_pdf(self):
        sid = self.imported()
        result = prepare_paper(self.project, sid)
        cache = Path(result["cache"])
        self.assertEqual(list(cache.glob("*.png")), [])
        self.assertIn(2, result["possible_ocr_pages"])
        self.assertIn("Synthetic fixture", (cache / "page-0001.txt").read_text())
        prepare_paper(self.project, sid, pages="1")
        self.assertEqual(len(list(cache.glob("*.png"))), 1)
        with self.assertRaisesRegex(WikiError, "outside"):
            prepare_paper(self.project, sid, pages="3")
        self.path.unlink()
        with self.assertRaisesRegex(WikiError, "Missing or changed"):
            self.project.resolve_pdf(sid)
        with self.assertRaisesRegex(WikiError, "PDF not found"):
            import_pdf(self.project, self.path)

    def test_changed_pdf_and_corrupt_pdf_rejected(self):
        sid = self.imported()
        self.path.write_bytes(b"not a PDF")
        with self.assertRaisesRegex(WikiError, "Missing or changed"):
            prepare_paper(self.project, sid)
        with self.assertRaises(WikiError):
            import_pdf(self.project, self.path)

    def test_index_idempotent_preserves_user_text_and_detects_links(self):
        sid = self.imported()
        path = self.note(sid, link="[Missing](missing.md)\n")
        sync_index(self.project)
        result = lint_wiki(self.project)
        self.assertTrue(any("broken link" in e and str(path) in e for e in result["errors"]))
        self.note(sid, link="[Heading](#synthetic-test)\n")
        sync_index(self.project)
        log_before = (self.project.vault / "log.md").read_bytes()
        self.assertFalse(sync_index(self.project)["changed"])
        self.assertEqual((self.project.vault / "log.md").read_bytes(), log_before)
        self.assertIn("User introduction", (self.project.vault / "index.md").read_text())
        self.assertEqual(lint_wiki(self.project)["errors"], [])

    def test_reference_links_anchors_versions_and_orphans(self):
        sid = self.imported()
        path = self.note(sid, link="[wrong][ref]\n\n[ref]: evidence.md#absent\n")
        self.note(sid, "evidence")
        orphan = self.project.vault / "notes/孤立 页.md"
        orphan.write_text("# User note", encoding="utf-8")
        sync_index(self.project)
        result = lint_wiki(self.project)
        self.assertTrue(any("missing heading anchor" in e for e in result["errors"]))
        self.assertTrue(any(str(orphan) in e for e in result["warnings"]))
        path.write_text(path.read_text().replace("sha256:", "wrong:").replace("#absent", "#synthetic-test"))
        self.assertTrue(any("content_version" in e for e in lint_wiki(self.project)["errors"]))

    def test_path_traversal_lock_and_file_urls(self):
        with self.assertRaises(WikiError):
            self.project.record("../../escape")
        with self.project.lock():
            with self.assertRaisesRegex(WikiError, "locked"):
                self.imported()
        self.assertEqual(local_path(self.path.as_uri()), self.path)
        with self.assertRaises(WikiError):
            local_path("https://example.com/test.pdf")
        with self.assertRaisesRegex(WikiError, "needs paths"):
            local_path("C:\\Zotero\\paper.pdf", system="Linux")
        mapped = local_path("file:///C:/Zotero/a%20b.pdf", {"paths": {"windows_drives": {"C": "/mnt/c"}}}, system="Linux")
        self.assertTrue(str(mapped).replace("\\", "/").endswith("mnt/c/Zotero/a b.pdf"))

    def test_latex_missing_preserves_editable_content(self):
        tex = self.root / "reviews/demo/review.tex"
        tex.parent.mkdir()
        tex.write_text("Editable content", encoding="utf-8")
        self.project.config = {"tools": {"latex": str(self.root / "missing.exe")}}
        with self.assertRaisesRegex(WikiError, "compiler unavailable"):
            build_review(self.project, tex)
        self.assertEqual(tex.read_text(), "Editable content")
        self.assertFalse(tex.with_suffix(".pdf").exists())
        self.assertEqual(latex_escape("10% & a_b"), r"10\% \& a\_b")


    def test_malformed_source_fields_report_file_instead_of_crashing(self):
        sid = self.imported()
        note = self.note(sid)
        note.write_text(note.read_text(encoding="utf-8").replace(sid, "[]"), encoding="utf-8")
        self.assertTrue(any("source_id must be a string" in e for e in lint_wiki(self.project)["errors"]))
        meta_path = self.project.metadata / f"{sid}.json"
        meta = self.project.record(sid)
        meta["possible_same_paper"] = None
        meta_path.write_text(json.dumps(meta), encoding="utf-8")
        self.assertTrue(any(str(meta_path) in e and "must be a list" in e for e in lint_wiki(self.project)["errors"]))

    def test_zotero_rejects_remote_endpoint(self):
        self.project.config = {"zotero": {"base_url": "https://api.zotero.org/"}}
        with self.assertRaisesRegex(WikiError, "local/private"):
            Zotero(self.project)


if __name__ == "__main__":
    unittest.main()
