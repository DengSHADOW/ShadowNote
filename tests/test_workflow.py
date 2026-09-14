import json
import tempfile
import unittest
from pathlib import Path

import pymupdf

from paperwiki.core import Project, WikiError, import_pdf, local_path, prepare_paper
from paperwiki.llm_wiki import lint_llm_wiki, review_context
from paperwiki.review import build_review, latex_escape
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
        for folder in (
            "sources/inbox", "sources/metadata", "reviews", ".cache",
            "llm-wiki-data/wiki/sources", "llm-wiki-data/wiki/concepts",
            "llm-wiki-data/raw/sources",
        ):
            (self.root / folder).mkdir(parents=True)
        self.path = self.root / "sources/inbox/unicode file.pdf"
        synthetic_pdf(self.path)
        self.wiki_root = self.root / "llm-wiki-data"
        self.wiki_source = self.wiki_root / "raw/sources/paper.pdf"
        self.wiki_source.write_bytes(self.path.read_bytes())
        (self.wiki_root / "wiki/index.md").write_text("# Index\n\n- [[sources/paper]]\n", encoding="utf-8")

    def imported(self, **kwargs):
        return import_pdf(self.project, self.path, **kwargs)["source_id"]

    def page(self, sid, name="paper", page_type="source", link=""):
        content = (
            "---\n"
            f"type: {page_type}\n"
            "title: Synthetic test\n"
            "status: draft\n"
            f"source_id: {sid}\n"
            f"content_version: sha256:{sid[2:]}\n"
            "sources:\n  - raw/sources/paper.pdf\n"
            "---\n# Synthetic test\n"
            + link
        )
        folder = "sources" if page_type == "source" else "concepts"
        path = self.wiki_root / f"wiki/{folder}/{name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_duplicate_import_preserves_user_content_and_paths(self):
        manual = self.wiki_root / "wiki/user-notes/manual.md"
        manual.parent.mkdir(parents=True)
        manual.write_text("Keep this manual note unchanged.", encoding="utf-8")
        before = self.path.read_bytes()
        sid = self.imported()
        first_page = self.page(sid)
        page_before = first_page.read_bytes()
        metadata_before = (self.project.metadata / f"{sid}.json").read_bytes()
        second = import_pdf(self.project, self.path)
        self.assertTrue(second["duplicate"])
        self.assertEqual(sid, second["source_id"])
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(first_page.read_bytes(), page_before)
        self.assertEqual((self.project.metadata / f"{sid}.json").read_bytes(), metadata_before)
        self.assertEqual(manual.read_text(encoding="utf-8"), "Keep this manual note unchanged.")
        self.assertEqual(self.project.resolve_pdf(sid), self.path)
        self.assertNotIn(str(self.root), json.dumps(self.project.record(sid)))

    def test_revisions_and_conflicting_metadata_are_explicit(self):
        old = self.imported(version="v1")
        other = self.root / "revision.pdf"
        synthetic_pdf(other, "A revised synthetic document.")
        with self.assertRaisesRegex(WikiError, "explicit"):
            import_pdf(self.project, other, revision_of=old)
        new = import_pdf(self.project, other, revision_of=old, version="v2")["source_id"]
        self.assertEqual(self.project.record(new)["revision_of"], old)
        alias = {"library": "users/0", "item_key": "ABCD1234", "server_id": "test-only"}
        import_pdf(self.project, self.path, title="Verified title", zotero=alias)
        with self.assertRaisesRegex(WikiError, "Metadata conflict"):
            import_pdf(self.project, self.path, title="Conflicting title")

    def test_prepare_extracts_text_without_copying_or_guessing_pages(self):
        sid = self.imported()
        result = prepare_paper(self.project, sid)
        cache = Path(result["cache"])
        self.assertEqual(list(cache.glob("*.png")), [])
        self.assertIn(2, result["possible_ocr_pages"])
        self.assertIn("Synthetic fixture", (cache / "page-0001.txt").read_text(encoding="utf-8"))
        prepare_paper(self.project, sid, pages="1")
        self.assertEqual(len(list(cache.glob("*.png"))), 1)
        with self.assertRaisesRegex(WikiError, "outside"):
            prepare_paper(self.project, sid, pages="3")

    def test_llm_lint_detects_broken_and_ambiguous_graph_links(self):
        sid = self.imported()
        paper = self.page(sid, link="[[missing]]\n")
        result = lint_llm_wiki(self.wiki_root)
        self.assertTrue(any("broken or ambiguous" in error for error in result["errors"]))
        paper.write_text(paper.read_text(encoding="utf-8").replace("[[missing]]", "[[duplicate]]"), encoding="utf-8")
        for folder in ("concepts", "entities"):
            duplicate = self.wiki_root / f"wiki/{folder}/duplicate.md"
            duplicate.parent.mkdir(exist_ok=True)
            duplicate.write_text(paper.read_text(encoding="utf-8").replace("type: source", "type: concept"), encoding="utf-8")
        result = lint_llm_wiki(self.wiki_root)
        self.assertTrue(any("broken or ambiguous" in error for error in result["errors"]))
        self.assertTrue(any("not linked from index" in warning for warning in result["warnings"]))

    def test_llm_lint_validates_provenance_and_index(self):
        sid = self.imported()
        paper = self.page(sid)
        self.assertEqual(lint_llm_wiki(self.wiki_root)["errors"], [])
        paper.write_text(paper.read_text(encoding="utf-8").replace("sha256:", "wrong:"), encoding="utf-8")
        self.assertTrue(any("content_version" in error for error in lint_llm_wiki(self.wiki_root)["errors"]))
        paper.write_text(paper.read_text(encoding="utf-8").replace("wrong:", "sha256:").replace(sid, "[]", 1), encoding="utf-8")
        self.assertTrue(any("source_id must be p-" in error for error in lint_llm_wiki(self.wiki_root)["errors"]))

    def test_llm_review_context_is_read_only_and_follows_direct_links(self):
        wiki_root = self.root / "context-wiki"
        source = wiki_root / "raw/sources/paper.pdf"
        source.parent.mkdir(parents=True)
        source.write_bytes(b"fixture")
        pages = wiki_root / "wiki"
        (pages / "sources").mkdir(parents=True)
        (pages / "concepts").mkdir(parents=True)
        (pages / "sources/paper.md").write_text("---\ntype: source\nsources:\n  - raw/sources/paper.pdf\n---\n# Paper\n[[concepts/method]]\n", encoding="utf-8")
        (pages / "concepts/method.md").write_text("# Method\n", encoding="utf-8")
        (pages / "concepts/uses-paper.md").write_text("# Uses\n[[sources/paper]]\n", encoding="utf-8")
        before = {path: path.read_bytes() for path in wiki_root.rglob("*") if path.is_file()}
        result = review_context(wiki_root, "raw/sources/paper.pdf")
        self.assertEqual(result["source_pages"], ["wiki/sources/paper.md"])
        self.assertEqual(result["linked_pages"], ["wiki/concepts/method.md"])
        self.assertEqual(result["backlink_pages"], ["wiki/concepts/uses-paper.md"])
        self.assertEqual(before, {path: path.read_bytes() for path in wiki_root.rglob("*") if path.is_file()})

    def test_llm_zotero_context_resolves_original_without_raw_copy(self):
        alias = {"library": "users/0", "item_key": "PAPER123", "attachment_key": "ATTACH12"}
        sid = import_pdf(self.project, self.path, zotero=alias)["source_id"]
        wiki_root = self.root / "zotero-wiki"
        page = wiki_root / "wiki/sources/paper.md"
        page.parent.mkdir(parents=True)
        uri = "zotero://users/0/items/PAPER123"
        page.write_text(f"---\ntype: source\nsource_id: {sid}\nsources:\n  - {uri}\n---\n# Paper\n", encoding="utf-8")
        result = review_context(wiki_root, uri, project=self.project)
        self.assertEqual(result["source_kind"], "zotero")
        self.assertEqual(result["source_id"], sid)
        self.assertEqual(Path(result["original_pdf"]), self.path)
        self.assertFalse((wiki_root / "raw").exists())

    def test_path_lock_and_latex_errors_preserve_input(self):
        with self.assertRaises(WikiError):
            self.project.record("../../escape")
        with self.project.lock():
            with self.assertRaisesRegex(WikiError, "locked"):
                self.imported()
        self.assertEqual(local_path(self.path.as_uri()), self.path)
        with self.assertRaises(WikiError):
            local_path("https://example.com/test.pdf")
        tex = self.root / "reviews/demo/review.tex"
        tex.parent.mkdir()
        tex.write_text("Editable content", encoding="utf-8")
        self.project.config = {"tools": {"latex": str(self.root / "missing.exe")}}
        with self.assertRaisesRegex(WikiError, "compiler unavailable"):
            build_review(self.project, tex)
        self.assertEqual(tex.read_text(encoding="utf-8"), "Editable content")
        self.assertEqual(latex_escape("10% & a_b"), r"10\% \& a\_b")

    def test_zotero_rejects_remote_endpoint(self):
        self.project.config = {"zotero": {"base_url": "https://api.zotero.org/"}}
        with self.assertRaisesRegex(WikiError, "local/private"):
            Zotero(self.project)


if __name__ == "__main__":
    unittest.main()
