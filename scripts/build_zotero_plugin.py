"""Build the reviewed local Zotero extension; no automatic installation."""
import hashlib
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / "zotero-plugin/selection"
manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
out = root / "dist" / f"paper-wiki-selection-{manifest['version']}.xpi"
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in ("manifest.json", "bootstrap.js"):
        info = zipfile.ZipInfo(name, date_time=(2026, 9, 10, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, (source / name).read_bytes())
print(json.dumps({"xpi": str(out), "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                  "files": ["manifest.json", "bootstrap.js"]}, indent=2))
