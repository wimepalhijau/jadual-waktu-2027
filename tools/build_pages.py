#!/usr/bin/env python3
"""Bina docs/index.html (versi GitHub Pages) daripada kod halaman + data terkini.

Guna:  python3 tools/build_pages.py

- Kod sumber : src/jadual-waktu-aktif/index.html
- Data       : data/jadual-waktu-aktif/plan/jadual.json  ({"data": {...}, "savedAt": n})
- Keluaran   : docs/index.html  (+ docs/.nojekyll)

Halaman memuatkan data daripada `window.__SNAP={...}` yang tertanam dalam HTML.
Skrip ini menggantikan snapshot itu dengan data terkini dan menaikkan savedAt
supaya pelayar yang pernah membuka halaman memuat semula data baharu
(halaman membandingkan savedAt dengan localStorage 'jw-snap-at').
"""
import json, pathlib, time, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src/jadual-waktu-aktif/index.html"
DATA = ROOT / "data/jadual-waktu-aktif/plan/jadual.json"
OUT = ROOT / "docs/index.html"
TAG = "window.__SNAP="


def main():
    html = SRC.read_text(encoding="utf-8")
    doc = json.loads(DATA.read_text(encoding="utf-8"))
    plan = doc["data"] if "data" in doc and "lessons" in doc["data"] else doc
    i = html.find(TAG)
    if i < 0:
        sys.exit("Tidak jumpa window.__SNAP dalam " + str(SRC))
    i += len(TAG)
    _, n = json.JSONDecoder().raw_decode(html[i:])
    snap = {"savedAt": int(time.time() * 1000), "data": plan}
    html = html[:i] + json.dumps(snap, ensure_ascii=False) + html[i + n:]
    if 'name="robots"' not in html:
        html = html.replace("<head>", '<head><meta name="robots" content="noindex,nofollow">', 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    (OUT.parent / ".nojekyll").write_text("", encoding="utf-8")
    print(f"OK: {OUT.relative_to(ROOT)}  ({len(plan['lessons'])} pelajaran, "
          f"{len(plan['teachers'])} guru, {len(plan['classes'])} kelas)")


if __name__ == "__main__":
    main()
