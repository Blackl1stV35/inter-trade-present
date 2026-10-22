"""Compare the current (16 Oct 2026) Comext annual Chapter 72 / 7208 imports with the workbook tables.

Run:  python -I -X utf8 03_vintage_check.py <raw_dir> <out_dir> <workbook_txt>

The workbook (research-brief txt) quotes values retrieved 10-11 Oct 2026 from the 15 Sep 2026 source update.
A match to two decimals shows that the 2025 annual figures were not revised by the 16 Oct 2026 update.
"""
import csv
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAW = Path(sys.argv[1]); OUT = Path(sys.argv[2]); WB = Path(sys.argv[3])
BASE = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409"
url = (BASE + "?format=JSON&lang=EN&freq=A&reporter=DE&partner=EXT_EU27_2020&product=72&flow=1"
       "&indicators=VALUE_IN_EUROS&indicators=QUANTITY_IN_100KG&sinceTimePeriod=1999")
req = urllib.request.Request(url, headers={"User-Agent": "inter-trade-present-research/1.0", "Accept": "application/json"})
retrieved = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
body = urllib.request.urlopen(req, timeout=120).read()
(RAW / "vintagecheck_annual_72_flow1_imports_since1999.json").write_bytes(body)
d = json.loads(body.decode("utf-8"))
times = {v: k for k, v in d["dimension"]["time"]["category"]["index"].items()}
inds = {v: k for k, v in d["dimension"]["indicators"]["category"]["index"].items()}
nt = len(times)
cur = {}
for pos, v in d["value"].items():
    pos = int(pos)
    ind = inds[pos // nt]; yr = times[pos % nt]
    cur.setdefault(yr, {})[ind] = v

# workbook table (section 4.2): "Year | Import value / EUR million | Net mass / thousand tonnes"
txt = WB.read_text(encoding="utf-8").splitlines()
wb = {}
start = next(i for i, l in enumerate(txt) if l.startswith("Year | Import value / EUR million"))
for l in txt[start + 1:]:
    if l.startswith("[/TABLE]"):
        break
    y, v, m = [x.strip() for x in l.split("|")]
    wb[y] = (float(v), float(m))

rows = []
maxdiff_v = maxdiff_m = 0.0
for y in sorted(wb):
    c = cur.get(y, {})
    cv = None if c.get("VALUE_IN_EUROS") is None else c["VALUE_IN_EUROS"] / 1e6
    cm = None if c.get("QUANTITY_IN_100KG") is None else c["QUANTITY_IN_100KG"] / 10 / 1000
    dv = None if cv is None else cv - wb[y][0]
    dm = None if cm is None else cm - wb[y][1]
    if dv is not None:
        maxdiff_v = max(maxdiff_v, abs(dv))
    if dm is not None:
        maxdiff_m = max(maxdiff_m, abs(dm))
    rows.append([y, wb[y][0], f"{cv:.2f}" if cv is not None else "", f"{dv:+.2f}" if dv is not None else "",
                 wb[y][1], f"{cm:.2f}" if cm is not None else "", f"{dm:+.2f}" if dm is not None else ""])
with open(OUT / "vintage_check_annual_72_imports.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["year", "workbook_value_eur_m", "current_value_eur_m", "diff_value", "workbook_mass_kt", "current_mass_kt", "diff_mass"])
    w.writerows(rows)
print("retrieved", retrieved, "dataset updated", d.get("updated"))
print("years compared", len(rows), "| max |diff| value EUR m:", round(maxdiff_v, 4), "| max |diff| mass kt:", round(maxdiff_m, 4))
print("years in current pull not in workbook:", sorted(set(cur) - set(wb)))
(OUT / "vintage_check_meta.json").write_text(json.dumps(dict(url=url, retrieved_utc=retrieved, dataset_updated=d.get("updated"),
    max_abs_diff_value_eur_m=round(maxdiff_v, 4), max_abs_diff_mass_kt=round(maxdiff_m, 4), years_compared=len(rows)), indent=2), encoding="utf-8")
