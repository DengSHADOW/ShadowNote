import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from .core import WikiError, atomic_write, pdf_module


def latex_escape(text):
    escaped = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
               "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(escaped.get(c, c) for c in text)


def build_review(project, tex, expected_pages=None):
    tex = Path(tex).resolve()
    if not tex.is_file() or tex.suffix.lower() != ".tex":
        raise WikiError(f"LaTeX source not found: {tex}")
    if not tex.is_relative_to(project.root / "reviews"):
        raise WikiError("Place editable LaTeX under reviews/<source_id>/review.tex (or reviews/synthetic-demo/).")
    compiler = project.executable("latex")
    if not compiler:
        raise WikiError("LaTeX compiler unavailable; .tex preserved and no PDF generated. Install MiKTeX (https://miktex.org/download), restart terminal or set tools.latex in config.local.toml; on Ubuntu: sudo apt install texlive-latex-base texlive-latex-recommended. Then rerun build-review.")
    pdf = pdf_module()
    expected_pages = expected_pages or project.config.get("review", {}).get("expected_pages", 1)
    timeout = project.config.get("review", {}).get("timeout", 120)
    with project.lock():
        parent = project.cache / "latex"
        parent.mkdir(parents=True, exist_ok=True)
        out = Path(tempfile.mkdtemp(prefix="build-", dir=parent))
        if "tectonic" in Path(compiler).stem.lower():
            command = [compiler, "--untrusted", "--keep-logs", "--keep-intermediates", "--outdir", str(out), str(tex)]
            passes = 1
        else:
            command = [compiler, "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
                       "-jobname=review", f"-output-directory={out}", str(tex)]
            passes = 2
        logs = []
        environment = os.environ.copy()
        environment['TECTONIC_CACHE_DIR'] = str(project.cache / 'tectonic')
        for _ in range(passes):
            try:
                result = subprocess.run(command, cwd=tex.parent, capture_output=True, text=True,
                                        encoding="utf-8", errors="replace", timeout=timeout, shell=False, env=environment)
            except subprocess.TimeoutExpired as exc:
                atomic_write(out / "build-output.txt", "\n".join(logs) + "\nCompilation timed out.\n")
                raise WikiError(f"LaTeX timed out after {timeout}s; editable .tex and previous PDF preserved. Logs: {out}") from exc
            logs.append(result.stdout + result.stderr)
            atomic_write(out / "build-output.txt", "\n".join(logs))
            if result.returncode:
                raise WikiError(f"LaTeX failed (exit {result.returncode}); see {out / 'build-output.txt'}. Previous PDF preserved.")
        compiled = out / (tex.stem + ".pdf" if "tectonic" in Path(compiler).stem.lower() else "review.pdf")
        if not compiled.exists():
            raise WikiError(f"Compiler reported success without a PDF; inspect {out}.")
        with pdf.open(compiled) as doc:
            page_count = len(doc)
            for i, page in enumerate(doc, 1):
                page.get_pixmap(dpi=120, alpha=False).save(out / f"review-{i:02}.png")
        log_content = "\n".join(logs) + "\n" + "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in out.glob("*.log"))
        warnings = list(dict.fromkeys(re.findall(r"(?:Overfull[^\n]*|LaTeX Warning:[^\n]*|Fontconfig[^\n]*|.*[Uu]ndefined[^\n]*)", log_content)))
        if page_count != expected_pages:
            raise WikiError(f"Compiled {page_count} pages; expected {expected_pages}. Shorten content, keep 11pt. Candidate PDF and renders: {out}; previous final PDF preserved.")
        if any("Overfull" in w or "undefined" in w.lower() for w in warnings):
            raise WikiError(f"LaTeX has overflow or undefined references. Inspect {out}; previous final PDF preserved.")
        target = tex.with_suffix(".pdf")
        fd, temp = tempfile.mkstemp(dir=tex.parent, suffix=".pdf")
        os.close(fd)
        try:
            shutil.copyfile(compiled, temp)
            os.replace(temp, target)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)
    return {"pdf": str(target), "pages": page_count, "logs_and_renders": str(out), "warnings": warnings,
            "visual_review": "pending: inspect rendered PNGs before claiming layout verified"}
