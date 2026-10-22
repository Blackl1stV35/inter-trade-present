"""Save short text excerpts of the Eurostat pages that document revisions / provisional status / release timing.

Run:  python -I -X utf8 05_eurostat_policy_excerpts.py <raw_dir>
Writes raw/eurostat_sims_ext_go_detail_excerpt.txt and raw/eurostat_euroindicator_2026-10-16_excerpt.txt
"""
import hashlib
import html
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(sys.argv[1])
UA = {"User-Agent": "Mozilla/5.0 (inter-trade-present-research)"}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def to_text(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>|</li>|</tr>", "\n", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = html.unescape(h).replace("­", "")
    h = re.sub(r"[ \t\xa0]+", " ", h)
    return re.sub(r"\n\s*\n+", "\n", h)


def stamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# 1. SIMS metadata page
u1 = "https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm"
b1 = fetch(u1); t1 = to_text(b1.decode("utf-8", "replace")).split("\n")
def grab(lines, start_pat, stop_pat, last=False):
    idx = [i for i, l in enumerate(lines) if re.match(start_pat, l.strip())]
    i = idx[-1] if last else idx[0]
    out = []
    for l in lines[i:]:
        if out and re.match(stop_pat, l.strip()):
            break
        out.append(l.strip())
    return out
ex = []
ex += grab(t1, r"^2\.1\. Metadata last certified", r"^3\. Statistical presentation")
ex += [""] + grab(t1, r"^14\.1\. Timeliness", r"^14\.1\.1")
ex += [""] + grab(t1, r"^17\.1\. Data revision - policy", r"^17\.2\.1")
ex += [""] + grab(t1, r"^7\.2\. Confidentiality - data treatment", r"^7\.3|^8\. ")
(RAW / "eurostat_sims_ext_go_detail_excerpt.txt").write_text(
    f"URL: {u1}\nRETRIEVED_UTC: {stamp()}\nFULL_PAGE_SHA256: {hashlib.sha256(b1).hexdigest()}\n"
    "(Excerpt of sections 2.1-2.3, 14.1, 17.1-17.2, 7.2; text extracted from HTML, order preserved)\n\n" + "\n".join(ex), encoding="utf-8")

# 2. Euro indicator news release of 16 Oct 2026 (reference month August 2026)
u2 = "https://ec.europa.eu/eurostat/web/products-euro-indicators/w/6-16102026-bp"
b2 = fetch(u2); t2 = to_text(b2.decode("utf-8", "replace")).split("\n")
keep = []
for i, l in enumerate(t2):
    s = l.strip()
    if re.search(r"^(16 October 2026|Next release:|August 2026|Euro area international trade in goods deficit)", s) or \
       re.search(r"Revisions and timetable|This News Release is based|Figures are provisional|Statistics on trade in goods are transmitted monthly|These data are available within 40 days", s):
        keep.append(s)
(RAW / "eurostat_euroindicator_2026-10-16_excerpt.txt").write_text(
    f"URL: {u2}\nRETRIEVED_UTC: {stamp()}\nFULL_PAGE_SHA256: {hashlib.sha256(b2).hexdigest()}\n"
    "(Selected lines only: release date, next release, revisions/timetable note, methods note)\n\n" + "\n".join(keep), encoding="utf-8")
print("ok")
