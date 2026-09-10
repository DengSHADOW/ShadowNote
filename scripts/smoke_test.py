"""Run real CLI commands against isolated synthetic PDFs; never write real notes."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pymupdf
from paperwiki.core import write_json

def main():
    repo = Path(__file__).resolve().parents[1]
    parent = repo / ".cache/verification"
    parent.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="synthetic-", dir=parent))
    for folder in ("sources/inbox", "sources/metadata", "vault/notes", "reviews", ".cache"):
        (root / folder).mkdir(parents=True)
    (root / "vault/index.md").write_text("# Synthetic test\n", encoding="utf-8")
    notes = root / "vault/notes/user.md"
    notes.write_text("User-owned text; preserve exactly.\n", encoding="utf-8")
    original_notes = notes.read_bytes()
    pdf_path = root / "sources/inbox/合成 测试.pdf"
    with pymupdf.open() as pdf:
        page = pdf.new_page(width=612, height=792)
        page.insert_text((54, 60), "SYNTHETIC TOOL TEST - NOT A RESEARCH PAPER", fontsize=15)
        page.insert_text((54, 95), "This page verifies text extraction and selective rendering.", fontsize=11)
        page.draw_rect(pymupdf.Rect(54, 125, 300, 235), color=(0.15, 0.25, 0.35))
        page.insert_text((65, 155), "Synthetic Figure: rectangle only.", fontsize=11)
        pdf.new_page(width=612, height=792)
        pdf.save(pdf_path)
    before_pdf = pdf_path.read_bytes()
    outputs = []
    def run(*args, expected=0):
        result = subprocess.run([sys.executable, str(repo / "scripts/paper_wiki.py"), "--root", str(root), *args],
                                cwd=repo, capture_output=True, encoding="utf-8", shell=False)
        outputs.append({"command": list(args), "exit_code": result.returncode,
                        "stdout": result.stdout, "stderr": result.stderr})
        if result.returncode != expected:
            raise RuntimeError(f"{args}: expected {expected}, got {result.returncode}: {result.stderr}")
        return json.loads(result.stdout) if result.stdout else None
    first = run("import-pdf", str(pdf_path))
    second = run("import-pdf", str(pdf_path))
    assert first["source_id"] == second["source_id"] and second["duplicate"]
    sid = first["source_id"]
    prepared = run("prepare-paper", sid, "--pages", "1")
    assert prepared["rendered"] == [1] and 2 in prepared["possible_ocr_pages"]
    assert len(list(Path(prepared["cache"]).glob("*.png"))) == 1
    run("resolve-pdf", sid)
    run("import-pdf", str(root / "missing.pdf"), expected=2)
    (root / "vault/notes/broken.md").write_text("[Broken](missing.md)\n", encoding="utf-8")
    lint = run("lint-wiki", expected=1)
    assert any("broken link" in e for e in lint["errors"])
    assert pdf_path.read_bytes() == before_pdf
    assert notes.read_bytes() == original_notes
    report = {"synthetic_only": True, "passed": True, "root": str(root),
              "rendered_page": str(Path(prepared["cache"]) / "page-0001.png"), "commands": outputs}
    write_json(parent / "latest-smoke.json", report)
    print(json.dumps({"passed": True, "report": str(parent / "latest-smoke.json"),
                      "rendered_page": report["rendered_page"]}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
