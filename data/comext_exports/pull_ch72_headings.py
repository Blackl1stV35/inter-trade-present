#!/usr/bin/env python
"""Decompose the extra-EU Chapter 72 series into its 29 four-digit headings (plus Comext's special 2-digit codes
72XX, 72CC, 72II, 72MM, 72SS, 72VV) so the movement of the aggregate can be traced to products.
Run after pull_comext.py:  python -I -X utf8 pull_ch72_headings.py
Writes only inside its own folder.
"""
import csv
import datetime
import hashlib
import html
import json
import os
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
API = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409"
YEARS = list(range(1999, 2026))
doc = json.load(open(os.path.join(RAW, "ch72_heading_codes.json"), encoding="utf-8"))
HEADS = sorted(doc["headings"])
SPECIAL = sorted(doc["non_numeric_4char_72_codes"])
NAMES = {k: html.unescape(v) for k, v in doc["headings"].items()}


def parse(d):
    ids, sizes = d["id"], d["size"]
    cats = {}
    for dim in ids:
        idx = d["dimension"][dim]["category"]["index"]
        if isinstance(idx, list):
            idx = {c: i for i, c in enumerate(idx)}
        cats[dim] = {i: c for c, i in idx.items()}
    strides, s = [], 1
    for n in reversed(sizes):
        strides.insert(0, s)
        s *= n
    out = {}
    vals = d["value"]
    items = vals.items() if isinstance(vals, dict) else enumerate(vals)
    for k, v in items:
        if v is None:
            continue
        k = int(k)
        c = {dim: cats[dim][(k // st) % n] for dim, n, st in zip(ids, sizes, strides)}
        out[(c["product"], c["flow"], c["indicators"], int(c["time"]))] = float(v)
    return out


DATA = {}
MAN = []
for flow in ("1", "2"):
    q = [("format", "JSON"), ("lang", "EN"), ("freq", "A"), ("reporter", "DE"), ("partner", "EXT_EU27_2020")]
    q += [("product", c) for c in ["72"] + HEADS + SPECIAL]
    q += [("flow", flow), ("indicators", "VALUE_IN_EUROS"), ("indicators", "QUANTITY_IN_100KG"), ("sinceTimePeriod", "1999")]
    url = API + "?" + urllib.parse.urlencode(q)
    req = urllib.request.Request(url, headers={"User-Agent": "inter-trade-present-datacheck/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        body, status = r.read(), r.status
    name = "ch72_headings_flow%s" % flow
    with open(os.path.join(RAW, name + ".json"), "wb") as f:
        f.write(body)
    d = json.loads(body.decode("utf-8"))
    MAN.append({"file": "raw/%s.json" % name, "url": url, "http_status": status,
                "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "api_updated": d.get("updated")})
    DATA.update({k: v for k, v in parse(d).items()})
    print("pulled", name, "cells", len(d["value"]))
json.dump(MAN, open(os.path.join(RAW, "_manifest_ch72_headings.json"), "w", encoding="utf-8"), indent=1)


def kt(p, f, y):
    v = DATA.get((p, f, "QUANTITY_IN_100KG", y))
    return None if v is None else v / 1e4


def em(p, f, y):
    v = DATA.get((p, f, "VALUE_IN_EUROS", y))
    return None if v is None else v / 1e6


def fm(x, nd=6):
    return "" if x is None else ("%." + str(nd) + "f") % x


rows = []
for flow, fl in (("1", "import"), ("2", "export")):
    for p in HEADS + SPECIAL:
        for y in YEARS:
            k, e = kt(p, flow, y), em(p, flow, y)
            rows.append([p, NAMES.get(p, "Comext special code (72 not elsewhere specified / confidential)")[:90], fl, y, fm(e), fm(k),
                         fm(None if (e is None or not k) else e * 1000.0 / k, 2)])
with open(os.path.join(HERE, "ch72_headings_extra_eu_long_1999_2025.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["heading", "description", "flow", "year", "value_eur_million", "net_mass_thousand_t", "unit_value_eur_per_t"])
    w.writerows(rows)

# reconciliation: sum of headings + special codes vs Chapter 72 total
chk = []
worst = 0.0
for flow in ("1", "2"):
    for y in YEARS:
        tot = DATA.get(("72", flow, "VALUE_IN_EUROS", y))
        s = sum(DATA.get((p, flow, "VALUE_IN_EUROS", y), 0.0) for p in HEADS + SPECIAL)
        totq = DATA.get(("72", flow, "QUANTITY_IN_100KG", y))
        sq = sum(DATA.get((p, flow, "QUANTITY_IN_100KG", y), 0.0) for p in HEADS + SPECIAL)
        sp = sum(DATA.get((p, flow, "VALUE_IN_EUROS", y), 0.0) for p in SPECIAL)
        chk.append([flow, y, tot, s, totq, sq, sp])
        worst = max(worst, abs(tot - s), abs(totq - sq))
print("max abs gap between Chapter 72 total and sum of headings+special codes (EUR or 100 kg):", worst)
with open(os.path.join(HERE, "ch72_headings_reconciliation.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["flow", "year", "ch72_value_eur", "sum_headings_and_special_value_eur", "ch72_quantity_100kg",
                "sum_headings_and_special_quantity_100kg", "special_codes_value_eur"])
    w.writerows(chk)

# contribution to the change in the aggregate, mass (kt) and value (EUR m)
def contrib(flow, y0, y1, fn):
    base0, base1 = fn("72", flow, y0), fn("72", flow, y1)
    out = []
    for p in HEADS + SPECIAL:
        a, b = fn(p, flow, y0) or 0.0, fn(p, flow, y1) or 0.0
        out.append((p, a, b, b - a))
    out.sort(key=lambda r: r[3])
    return base0, base1, out


rows = []
for flow, fl in (("1", "import"), ("2", "export")):
    for (y0, y1) in ((2004, 2007), (2017, 2025), (2021, 2025), (2019, 2025)):
        b0, b1, out = contrib(flow, y0, y1, kt)
        for p, a, b, dlt in out:
            if abs(dlt) < 1e-9 and a == 0 and b == 0:
                continue
            rows.append([fl, "%d-%d" % (y0, y1), p, NAMES.get(p, "special code")[:70], fm(a, 3), fm(b, 3), fm(dlt, 3),
                         fm(100.0 * dlt / (b1 - b0) if b1 != b0 else None, 1), fm(b0, 3), fm(b1, 3), fm(b1 - b0, 3)])
with open(os.path.join(HERE, "ch72_headings_change_contributions_mass.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["flow", "period", "heading", "description", "mass_start_kt", "mass_end_kt", "change_kt",
                "share_of_ch72_change_pct", "ch72_start_kt", "ch72_end_kt", "ch72_change_kt"])
    w.writerows(rows)
print("wrote contribution tables", len(rows))
