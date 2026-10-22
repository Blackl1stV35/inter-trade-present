"""Extract tables from the saved Destatis HTML pages (read-only parsing, no network).

Usage:
    python -I -X utf8 destatis_extract.py RAW_DIR OUT_DIR

Inputs (saved earlier with curl):
    RAW_DIR/destatis_sommerueberarbeitung_2026.html   (article of 25.08.2026, updated 30.09.2026)
    RAW_DIR/destatis_verwendung_bip_tabelle.html      (use-of-GDP table, 'Stand 25. August 2026')
    RAW_DIR/destatis_PE26_017_2026-01-15_en.html      (press release 17/2026 of 15 Jan 2026, first 2025 estimate)
Outputs:
    OUT_DIR/destatis_summer_revision_2026_old_vs_new.csv
    OUT_DIR/destatis_use_of_gdp_2023_2025.csv
"""
import csv
import html
import re
import sys

RAW, OUT = sys.argv[1], sys.argv[2]


def text(f):
    s = open(f"{RAW}/{f}", encoding="utf-8", errors="replace").read()
    s = re.sub(r"(?is)<(script|style).*?</\1>", "", s)
    s = re.sub(r"(?i)</(tr|p|h\d|li|div|table|caption)>", "\n", s)
    s = re.sub(r"(?i)</t[dh]>", " | ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s


def num(x):
    x = x.strip().replace("−", "-").replace(" ", "")
    return float(x.replace(",", "."))


# ---- summer revision article ----
t = text("destatis_sommerueberarbeitung_2026.html")
blocks = [
    ("GDP, real, % vs previous year", "Bruttoinlandsprodukt, preisbereinigte Veränderung gegenüber dem Vorjahr"),
    ("Private consumption (households + NPISH), real, % vs previous year", "Privater Konsum, preisbereinigte Veränderung gegenüber dem Vorjahr"),
    ("Government consumption, real, % vs previous year", "Konsumausgaben des Staates, preisbereinigte Veränderung gegenüber dem Vorjahr"),
    ("Gross fixed capital formation, real, % vs previous year", "Bruttoanlageinvestitionen, preisbereinigte Veränderung gegenüber dem Vorjahr"),
    ("Gross value added (total economy), real, % vs previous year", "Bruttowertschöpfung, preisbereinigte Veränderung gegenüber dem Vorjahr"),
]
rows = []
for label, head in blocks:
    i = t.find(head)
    seg = t[i:i + 600].split("\n")
    years = [y.strip() for y in seg[1].split("|") if y.strip().isdigit()]
    new = [num(v) for v in seg[2].split("|")[1:] if v.strip()]
    old = [num(v) for v in seg[3].split("|")[1:] if v.strip()]
    for y, n, o in zip(years, new, old):
        rows.append([label, y, o, n, round(n - o, 1)])
with open(f"{OUT}/destatis_summer_revision_2026_old_vs_new.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["indicator", "year", "old_result_pct_May2026_vintage", "new_result_pct_Aug2026_vintage", "difference_pp"])
    w.writerows(rows)
for r in rows:
    if r[1] == "2025":
        print(r)

# ---- use of GDP table ----
u = text("destatis_verwendung_bip_tabelle.html")
lines = [ln.strip() for ln in u.split("\n")]
cur = {}
real = {}
mode = None
for ln in lines:
    if ln.startswith("in jeweiligen Preisen"):
        mode = "cur"
    elif ln.startswith("preisbereinigt, Kettenindex"):
        mode = "real"
    if mode and "|" in ln:
        parts = [p.strip() for p in ln.split("|") if p.strip()]
        if len(parts) == 4 and parts[0] in (
            "Konsumausgaben", "Private Konsumausgaben", "Konsumausgaben des Staates", "Bruttoanlageinvestitionen",
            "Exporte", "Importe", "Bruttoinlandsprodukt", "Außenbeitrag (Exporte minus Importe)"):
            try:
                vals = [num(p) for p in parts[1:]]
            except ValueError:
                continue
            (cur if mode == "cur" else real)[parts[0]] = vals
stand = re.search(r"Stand \d+\. \w+ \d{4}", u)
with open(f"{OUT}/destatis_use_of_gdp_2023_2025.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["position", "current_prices_bn_eur_2023", "2024", "2025",
                "chain_index_2020_100_2023", "2024", "2025",
                "real_chg_2024_pct_from_rounded_index", "real_chg_2025_pct_from_rounded_index", "page_stand"])
    for k in cur:
        r = real.get(k)
        if r:
            c24 = round((r[1] / r[0] - 1) * 100, 2)
            c25 = round((r[2] / r[1] - 1) * 100, 2)
            w.writerow([k, *cur[k], *r, c24, c25, stand.group(0) if stand else ""])
        else:
            w.writerow([k, *cur[k], "", "", "", "", "", stand.group(0) if stand else ""])
print("use-of-GDP stand:", stand.group(0) if stand else None)

# ---- Jan 2026 first estimate ----
e = text("destatis_PE26_017_2026-01-15_en.html")
for kw in ("0.2%", "1.4%", "1.5%", "0.3%", "3.6%"):
    pass
m = re.search(r"Press release No\. 017 of 15 January 2026", e)
print("PE26_017 header found:", bool(m))
for ln in e.split("\n"):
    if re.search(r"(exports|imports|household final consumption|government final consumption|gross fixed|price.adjusted gross domestic)", ln, re.I) and len(ln) < 700:
        print("PE26_017>>", ln.strip()[:400])
