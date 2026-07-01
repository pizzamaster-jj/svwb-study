#!/usr/bin/env python3
"""Bundle template.html + cards.js into a self-contained index.html.

Workflow:
  1. Edit app code in template.html (it uses <script src="cards.js">).
  2. Update card data with generate.py (produces cards.js).
  3. Run: python3 build.py  -> writes a single-file index.html with data inlined.
"""
import pathlib

here = pathlib.Path(__file__).parent
tpl = (here / "template.html").read_text(encoding="utf-8")
data = (here / "cards.js").read_text(encoding="utf-8")

marker = '<script src="cards.js"></script>'
if marker not in tpl:
    raise SystemExit("marker not found in template.html: " + marker)

inlined = "<script>\n" + data + "\n</script>"
out = tpl.replace(marker, inlined)
(here / "index.html").write_text(out, encoding="utf-8")
print("built index.html (self-contained), %d bytes" % len(out))
