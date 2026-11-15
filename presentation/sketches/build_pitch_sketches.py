"""Render the final-deck slide sketches (presentation/sketches/src/P<n>.html) to presentation/sketches/png/P<n>.png.

Uses the deck renderer scripts/build_sketches.py and its style (outline/sketches/style.css), so the
frame, chapter ribbon, evidence label, chips and overflow checks match the presenting deck.

usage (from the repo root):
    python -I -X utf8 presentation/sketches/build_pitch_sketches.py            # all pages
    python -I -X utf8 presentation/sketches/build_pitch_sketches.py P3 P7      # selected pages
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "scripts"))

import build_sketches as b  # noqa: E402

b.ROOT = REPO
b.SRC = os.path.join(HERE, "src")
b.OUT = os.path.join(HERE, "png")
b.CSS = os.path.join(REPO, "outline", "sketches", "style.css")

if __name__ == "__main__":
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not ids:
        ids = sorted((f[:-5] for f in os.listdir(b.SRC) if f.endswith(".html")),
                     key=lambda s: int(re.sub(r"\D", "", s)))
    b.render(ids)
