"""Fetch WV Stahl (Wirtschaftsvereinigung Stahl) monthly crude steel press releases for 2026, the Aug-2026
revision table for 2025, and build tidy tables.

Run:  python -I -X utf8 04_wvstahl_crude_steel.py <raw_dir> <out_dir>

Primary source: wvstahl.de press releases (monthly figures are preliminary; WV Stahl states the final
status for a year is fixed by mid of the following year). German number format: '.' thousands, ',' decimal.
"""
import csv
import hashlib
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(sys.argv[1]) / "wvstahl"; OUT = Path(sys.argv[2])
RAW.mkdir(parents=True, exist_ok=True); OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (inter-trade-present-research)"}
P = "https://www.wvstahl.de/pressemitteilungen/"
RELEASES = [  # (reference month, slug)
    ("2025-12", "jahresbilanz-der-stahlproduktion-2025-viertes-krisenjahr-in-folge"),
    ("2026-01", "rohstahlproduktion-in-deutschland-steigt-zum-jahresbeginn"),
    ("2026-02", "rohstahlproduktion-in-deutschland-steigt-im-februar-leicht"),
    ("2026-03", "leichte-erholung-der-rohstahlproduktion-in-deutschland-im-ersten-quartal-2026"),
    ("2026-04", "rohstahlerzeugung-im-april-2026-produktionsplus-aber-noch-keine-rueckkehr-zur-normalitaet"),
    ("2026-05", "rohstahlerzeugung-im-mai-2026-fuenftes-plus-in-folge-aber-noch-keine-entwarnung"),
    ("2026-06", "halbjahresbilanz-stahl-produktion-steigt-nachfrage-bleibt-auf-krisenniveau"),
    ("2026-07", "rohstahlerzeugung-im-juli-2026-aufwaertstrend-geraet-ins-stocken"),
    ("2026-08", "rohstahlerzeugung-im-august-2026-weiterhin-verhaltene-erholung"),
]
REV_PDF = "https://www.wvstahl.de/wp-content/uploads/20260810_Rohstahlerzeugung_Deutschland_Revision_2025.pdf"
INDEX = "https://www.wvstahl.de/pressemitteilungen/"


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read(), r.status


def to_text(h):
    m = re.search(r"(?is)<main.*?</main>", h)
    if m:
        h = m.group(0)
    h = re.sub(r"(?is)<(script|style|nav|header|footer).*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>|</li>|</tr>", "\n", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = html.unescape(h).replace("­", "")
    h = re.sub(r"[ \t\xa0]+", " ", h)
    return re.sub(r"\n\s*\n+", "\n", h)


def num(s):
    return float(s.replace(".", "").replace(",", "."))


manifest = []
parsed = {}
for ref, slug in RELEASES:
    url = P + slug + "/"
    body, st = get(url)
    h = body.decode("utf-8", "replace")
    date = (re.findall(r'(?i)datePublished"\s*:\s*"([^"]+)"', h) or [""])[0]
    pdfs = sorted(set(re.findall(r'href="([^"]+PM_[^"]+\.pdf)"', h)))
    txt = to_text(h)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    # keep only the title, the dateline and the statistics table (not the full press-release prose)
    lines = [l.strip() for l in txt.split("\n") if l.strip()]
    title = lines[0] if lines else ""
    tstart = next((i for i, l in enumerate(lines) if l.startswith("Stahlproduktion in Deutschland im") or l.startswith("in 1.000 t")), None)
    tend = next((i for i, l in enumerate(lines) if tstart is not None and i > tstart and l.startswith("Quelle:")), None)
    table = lines[tstart:tend + 1] if tstart is not None and tend is not None else []
    dateline = next((l[:60] for l in lines if re.match(r"^(Berlin|Br.ssel)", l)), "")
    (RAW / f"pm_{ref}.txt").write_text(
        f"URL: {url}\nRETRIEVED_UTC: {stamp}\nPUBLISHED: {date}\nPDF: {pdfs}\nTITLE: {title}\nDATELINE: {dateline}\n"
        "(Statistics table only; press-release prose omitted)\n\n" + "\n".join(table) + "\n", encoding="utf-8")
    manifest.append(dict(ref_month=ref, url=url, http_status=st, retrieved_utc=stamp, published=date, pdf=pdfs,
                         sha256_html=hashlib.sha256(body).hexdigest()))
    line = next((l for l in txt.split("\n") if l.strip().startswith("Rohstahl gesamt")), None)
    # also table header 'in 1.000 t* ...' ; row numbers: month kt, month %, [ytd kt, ytd %]
    toks = re.findall(r"-?[\d.]+(?:,\d+)?%?", line.replace("Rohstahl gesamt", "")) if line else []
    def row_tokens(label):
        ln = next((l for l in txt.split("\n") if re.match(rf"^\s*{label}\s+[\d.]", l)), None)
        return re.findall(r"-?[\d.]+(?:,\d+)?%?", ln.replace(label, "")) if ln else []
    parsed[ref] = dict(line=line.strip() if line else None, tokens=toks, published=date[:10], url=url,
                       oxy_tokens=row_tokens("Oxygenstahl"), eaf_tokens=row_tokens("Elektrostahl"))

# Revision table 2025 (PDF)
rev_body, st = get(REV_PDF)
(RAW / "Rohstahlerzeugung_Deutschland_Revision_2025.pdf").write_bytes(rev_body)
manifest.append(dict(ref_month="2025 (revision table)", url=REV_PDF, http_status=st,
                     retrieved_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), sha256_html=hashlib.sha256(rev_body).hexdigest()))
(RAW / "manifest_wvstahl.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

import pdfplumber  # noqa: E402  (installed in the local interpreter)

months_de = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
rev = {}; rev_oxy = {}; rev_eaf = {}
with pdfplumber.open(RAW / "Rohstahlerzeugung_Deutschland_Revision_2025.pdf") as pdf:
    for tbl in pdf.pages[0].extract_tables():
        for row in tbl:
            if row[0] in months_de:
                mi = months_de.index(row[0]) + 1
                rev[mi] = num(row[1]); rev_oxy[mi] = num(row[2]); rev_eaf[mi] = num(row[3])
            if row[0] == "SUMME":
                rev_sum = num(row[1]); rev_oxy_sum = num(row[2]); rev_eaf_sum = num(row[3])
assert len(rev) == 12, rev
print("revised 2025: sum of months =", sum(rev.values()), "| printed SUMME =", rev_sum)

# 2026 monthly crude steel and YTD as published
rows = []
for ref, d in parsed.items():
    t = d["tokens"]
    if not t:
        continue
    month_kt = num(t[0]); month_pct = num(t[1].rstrip("%")) if len(t) > 1 else None
    ytd_kt = num(t[2]) if len(t) > 2 else None; ytd_pct = num(t[3].rstrip("%")) if len(t) > 3 else None
    rows.append(dict(ref=ref, month_kt=month_kt, month_pct=month_pct, ytd_kt=ytd_kt, ytd_pct=ytd_pct, pub=d["published"], url=d["url"]))

with open(OUT / "wvstahl_crude_steel_published.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["reference_month", "crude_steel_kt_as_published", "yoy_pct_published", "ytd_kt_published", "ytd_yoy_pct_published", "release_date", "source_url"])
    for r in rows:
        w.writerow([r["ref"], f"{r['month_kt']:.0f}", "" if r["month_pct"] is None else f"{r['month_pct']:.1f}",
                    "" if r["ytd_kt"] is None else f"{r['ytd_kt']:.0f}", "" if r["ytd_pct"] is None else f"{r['ytd_pct']:.1f}",
                    r["pub"], r["url"]])

# Like-for-like Jan-Aug: 2026 monthly vs revised 2025 monthly
m26 = {int(r["ref"][5:]): r["month_kt"] for r in rows if r["ref"].startswith("2026")}
assert sorted(m26) == list(range(1, 9)), m26
with open(OUT / "wvstahl_crude_steel_jan_aug_like_for_like.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["month", "crude_steel_kt_2025_revised_Aug2026", "crude_steel_kt_2026_published", "yoy_pct_vs_revised_2025"])
    for m in range(1, 9):
        w.writerow([f"{m:02d}", f"{rev[m]:.0f}", f"{m26[m]:.0f}", f"{(m26[m]/rev[m]-1)*100:+.1f}"])
    s25 = sum(rev[m] for m in range(1, 9)); s26 = sum(m26[m] for m in range(1, 9))
    w.writerow(["Jan-Aug (sum of monthly values)", f"{s25:.0f}", f"{s26:.0f}", f"{(s26/s25-1)*100:+.1f}"])
    ytd_pub = next(r["ytd_kt"] for r in rows if r["ref"] == "2026-08")
    w.writerow(["Jan-Aug (published YTD 2026 / revised 2025)", f"{s25:.0f}", f"{ytd_pub:.0f}", f"{(ytd_pub/s25-1)*100:+.1f}"])
print("Jan-Aug 2025 revised:", s25, "| Jan-Aug 2026 sum of months:", s26, "| published YTD:", ytd_pub, "| pct:", round((ytd_pub/s25-1)*100, 2))

# Route split (oxygen/BF-BOF vs electric steel) Jan-Aug: descriptive route share, NOT an emissions measure
oxy26 = {int(k[5:]): num(parsed[k]["oxy_tokens"][0]) for k in parsed if k.startswith("2026")}
eaf26 = {int(k[5:]): num(parsed[k]["eaf_tokens"][0]) for k in parsed if k.startswith("2026")}
oy25 = sum(rev_oxy[m] for m in range(1, 9)); ey25 = sum(rev_eaf[m] for m in range(1, 9))
oy26 = sum(oxy26[m] for m in range(1, 9)); ey26 = sum(eaf26[m] for m in range(1, 9))
oy26_pub = num(parsed["2026-08"]["oxy_tokens"][2]); ey26_pub = num(parsed["2026-08"]["eaf_tokens"][2])
with open(OUT / "wvstahl_route_split_jan_aug.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["measure", "jan_aug_2025_revised_kt", "jan_aug_2026_kt", "pct_change", "note"])
    w.writerow(["oxygen steel (BF-BOF route)", f"{oy25:.0f}", f"{oy26:.0f}", f"{(oy26/oy25-1)*100:+.1f}", f"published YTD 2026 = {oy26_pub:.0f}"])
    w.writerow(["electric steel (EAF)", f"{ey25:.0f}", f"{ey26:.0f}", f"{(ey26/ey25-1)*100:+.1f}", f"published YTD 2026 = {ey26_pub:.0f}"])
    w.writerow(["crude steel total", f"{oy25+ey25:.0f}", f"{oy26+ey26:.0f}", f"{((oy26+ey26)/(oy25+ey25)-1)*100:+.1f}", "oxygen + electric"])
    w.writerow(["EAF share of crude steel (%)", f"{ey25/(oy25+ey25)*100:.1f}", f"{ey26/(oy26+ey26)*100:.1f}", "", "share of tonnes, not emissions per tonne"])
    w.writerow(["EAF share, full-year 2025 revised (%)", f"{rev_eaf_sum/(rev_oxy_sum+rev_eaf_sum)*100:.1f}", "", "", f"electric {rev_eaf_sum:.0f} kt of {rev_oxy_sum+rev_eaf_sum:.0f} kt"])
print("route: oxygen", oy25, oy26, oy26_pub, "| eaf", ey25, ey26, ey26_pub, "| EAF share", round(ey25/(oy25+ey25)*100, 2), round(ey26/(oy26+ey26)*100, 2))

with open(OUT / "wvstahl_crude_steel_2025_revised.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["month_2025", "crude_steel_kt_revised_Aug2026"])
    for m in range(1, 13):
        w.writerow([f"{m:02d}", f"{rev[m]:.0f}"])
    w.writerow(["printed total (SUMME)", f"{rev_sum:.0f}"])

(OUT / "wvstahl_parsed_debug.json").write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
