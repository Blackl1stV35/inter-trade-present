#!/usr/bin/env python
"""Pull German steel trade series from the live Eurostat Comext dissemination API
(dataset DS-045409) and build the tidy CSV tables in this folder.

Run (from anywhere):  python -I -X utf8 pull_comext.py
Writes only inside its own folder (data/comext_exports). Reads the workbook text dumps in
sources/text/ read-only, to compare the re-pulled import series with the workbook tables.

Conventions (same as the workbook):
  mass:  thousand tonnes = QUANTITY_IN_100KG / 10 / 1000
  value: EUR million     = VALUE_IN_EUROS / 1e6
  unit value EUR/t       = VALUE_IN_EUROS / (QUANTITY_IN_100KG / 10)
  Missing observations stay missing (empty cell); nothing is zero-filled.
"""
import csv
import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC_BRIEF = os.path.join(REPO, "sources", "text", "inter-trade-present-2-revised-research-brief.txt")
SRC_BASE = os.path.join(REPO, "sources", "text", "inter-trade-present-base.txt")

API = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409"
INDS = ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"]
YEARS = list(range(1999, 2026))  # 1999-2025 inclusive
FLOWLAB = {"1": "import", "2": "export"}
PRODLAB = {
    "72": "Chapter 72 iron and steel",
    "7204": "7204 ferrous waste and scrap",
    "7207": "7207 semi-finished products of iron/non-alloy steel",
    "7208": "7208 flat-rolled iron/non-alloy steel, hot-rolled, width >= 600 mm",
    "7304": "7304 seamless tubes, pipes and hollow profiles of iron/steel",
    "7306": "7306 other tubes, pipes and hollow profiles of iron/steel (welded, riveted etc.)",
    "26011200": "26011200 agglomerated iron ores and concentrates (CN8)",
}
BYPROD = ["7204", "7207", "7208", "7304", "7306", "26011200"]

MANIFEST = []
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def build_url(partner, products, flows, since=1995):
    q = [("format", "JSON"), ("lang", "EN"), ("freq", "A"), ("reporter", "DE"), ("partner", partner)]
    q += [("product", p) for p in products]
    q += [("flow", f) for f in flows]
    q += [("indicators", i) for i in INDS]
    q.append(("sinceTimePeriod", str(since)))
    return API + "?" + urllib.parse.urlencode(q)


def fetch(name, url):
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "inter-trade-present-datacheck/1.0"})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
                status = r.status
            break
        except Exception as e:  # noqa
            last = e
            time.sleep(2 + 3 * attempt)
    else:
        raise RuntimeError("fetch failed for %s: %s" % (name, last))
    path = os.path.join(RAW, name + ".json")
    with open(path, "wb") as f:
        f.write(body)
    d = json.loads(body.decode("utf-8"))
    nodata = d.get("extension", {}).get("positions-with-no-data", {})
    MANIFEST.append({
        "file": "raw/" + name + ".json",
        "url": url,
        "http_status": status,
        "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "api_updated": d.get("updated"),
        "has_status_flags": "status" in d,
        "time_positions_with_no_data": nodata.get("time"),
    })
    return d


def parse(d):
    """JSON-stat -> {(partner, product, flow, indicator, year): value}. Uses the category index of each
    dimension (the API sorts category codes, not in request order)."""
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
        out[(c["partner"], c["product"], c["flow"], c["indicators"], int(c["time"]))] = float(v)
    return out


def pull(name, partner, products, flows):
    url = build_url(partner, products, flows)
    d = fetch(name, url)
    log("pulled", name, "updated:", d.get("updated"), "cells:", len(d["value"]))
    return parse(d)


# ----------------------------------------------------------------------------------------------
os.makedirs(RAW, exist_ok=True)
DATA = {}  # (partner, product, flow, indicator, year) -> value

# 1-2 and 4: Chapter 72 for extra-EU, intra-EU and world, both flows (one request per partner/flow)
for partner, tag in (("EXT_EU27_2020", "ext"), ("INT_EU27_2020", "int"), ("WORLD", "world")):
    for flow in ("1", "2"):
        DATA.update(pull("ch72_%s_flow%s" % (tag, flow), partner, ["72"], [flow]))

# 5: by-product series, extra-EU, both flows (all six products in one request per flow)
for flow in ("1", "2"):
    DATA.update(pull("byproduct_ext_flow%s" % flow, "EXT_EU27_2020", BYPROD, [flow]))

# Dataset-level metadata (SDMX dataflow) for the vintage
req = urllib.request.Request(
    "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/dataflow/ESTAT/DS-045409/latest",
    headers={"User-Agent": "inter-trade-present-datacheck/1.0"})
with urllib.request.urlopen(req, timeout=60) as r:
    body = r.read()
with open(os.path.join(RAW, "dataflow_DS-045409.xml"), "wb") as f:
    f.write(body)
m = re.findall(r"<c:AnnotationTitle>([^<]*)</c:AnnotationTitle><c:AnnotationType>(UPDATE_DATA|UPDATE_STRUCTURE|DISSEMINATION_TIMESTAMP_DATA)</c:AnnotationType>", body.decode("utf-8"))
log("dataflow annotations:", m)

with open(os.path.join(RAW, "_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(MANIFEST, f, indent=1)


# ----------------------------------------------------------------------------------------------
def get(partner, product, flow, ind, year):
    return DATA.get((partner, product, flow, ind, year))


def conv(v_eur, q100):
    """-> (eur_m, kt, unit value EUR/t); None where missing."""
    em = None if v_eur is None else v_eur / 1e6
    kt = None if q100 is None else q100 / 10.0 / 1000.0
    uv = None
    if v_eur is not None and q100 not in (None, 0):
        uv = v_eur / (q100 / 10.0)
    return em, kt, uv


def fmt(x, nd=6):
    if x is None:
        return ""
    return ("%." + str(nd) + "f") % x


def write_csv(name, header, rows):
    with open(os.path.join(HERE, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    log("wrote", name, len(rows), "rows")


EXT = "EXT_EU27_2020"

# --- 1/2 exports and imports, Chapter 72, extra-EU -----------------------------------------------
for flow, fname in (("2", "ch72_extra_eu_exports_1999_2025.csv"), ("1", "ch72_extra_eu_imports_1999_2025.csv")):
    rows = []
    for y in YEARS:
        v = get(EXT, "72", flow, "VALUE_IN_EUROS", y)
        q = get(EXT, "72", flow, "QUANTITY_IN_100KG", y)
        em, kt, uv = conv(v, q)
        stat = "both" if (v is not None and q is not None) else ("value_only" if v is not None else ("quantity_only" if q is not None else "missing"))
        rows.append([y, fmt(v, 2), fmt(q, 2), fmt(em), fmt(kt), fmt(uv, 2), stat])
    write_csv(fname, ["year", "value_eur", "quantity_100kg", "value_eur_million", "net_mass_thousand_t",
                      "unit_value_eur_per_t", "status"], rows)

# --- 3 balance X - M, extra-EU, Chapter 72 ------------------------------------------------------
rows = []
BAL = {}
for y in YEARS:
    xv, xq = get(EXT, "72", "2", "VALUE_IN_EUROS", y), get(EXT, "72", "2", "QUANTITY_IN_100KG", y)
    mv, mq = get(EXT, "72", "1", "VALUE_IN_EUROS", y), get(EXT, "72", "1", "QUANTITY_IN_100KG", y)
    xe, xk, xu = conv(xv, xq)
    me, mk, mu = conv(mv, mq)
    bv = None if (xe is None or me is None) else xe - me
    bk = None if (xk is None or mk is None) else xk - mk
    BAL[y] = (xe, me, bv, xk, mk, bk, xu, mu)
    rows.append([y, fmt(xe), fmt(me), fmt(bv), fmt(xk), fmt(mk), fmt(bk),
                 fmt(None if (xe is None or not me) else xe / me, 4),
                 fmt(None if (xk is None or not mk) else xk / mk, 4), fmt(xu, 2), fmt(mu, 2)])
write_csv("ch72_extra_eu_balance_1999_2025.csv",
          ["year", "exports_value_eur_million", "imports_value_eur_million", "balance_value_eur_million_X_minus_M",
           "exports_mass_thousand_t", "imports_mass_thousand_t", "balance_mass_thousand_t_X_minus_M",
           "export_import_ratio_value", "export_import_ratio_mass", "export_unit_value_eur_per_t",
           "import_unit_value_eur_per_t"], rows)

# --- 2 reproduction check of the workbook update-tab 4.2 table ------------------------------------
wb_imp = {}
txt = open(SRC_BRIEF, encoding="utf-8").read().splitlines()
start = next(i for i, l in enumerate(txt) if l.startswith("## 4.2 Germany's direct extra-EU Chapter 72 imports"))
for l in txt[start:start + 45]:
    m = re.match(r"^(\d{4}) \| ([\d.]+) \| ([\d.]+)$", l.strip())
    if m:
        wb_imp[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
log("workbook 4.2 rows parsed:", len(wb_imp), min(wb_imp), max(wb_imp))

rows, differing = [], []
for y in YEARS:
    wv, wm = wb_imp.get(y, (None, None))
    v, q = get(EXT, "72", "1", "VALUE_IN_EUROS", y), get(EXT, "72", "1", "QUANTITY_IN_100KG", y)
    em, kt, _ = conv(v, q)
    dv = None if (em is None or wv is None) else em - wv
    dm = None if (kt is None or wm is None) else kt - wm
    ok_v = dv is not None and round(em, 2) == wv
    ok_m = dm is not None and round(kt, 2) == wm
    ok = ok_v and ok_m
    if not ok:
        differing.append((y, wv, em, dv, wm, kt, dm))
    rows.append([y, fmt(wv, 2), fmt(em), fmt(dv), fmt(wm, 2), fmt(kt), fmt(dm),
                 "yes" if ok_v else "NO", "yes" if ok_m else "NO"])
write_csv("check_imports_vs_workbook_4_2.csv",
          ["year", "workbook_value_eur_million", "api_value_eur_million", "diff_value_api_minus_workbook",
           "workbook_mass_thousand_t", "api_mass_thousand_t", "diff_mass_api_minus_workbook",
           "value_matches_after_rounding_2dp", "mass_matches_after_rounding_2dp"], rows)
log("years differing beyond 2-dp rounding:", [(y, round(dv, 4) if dv is not None else None, round(dm, 4) if dm is not None else None) for (y, wv, em, dv, wm, kt, dm) in differing])

# --- 4 materiality: Chapter 72 by partner group ---------------------------------------------------
long_rows = []
for partner, tag in ((EXT, "EXT_EU27_2020"), ("INT_EU27_2020", "INT_EU27_2020"), ("WORLD", "WORLD")):
    for flow in ("1", "2"):
        for y in YEARS:
            v, q = get(partner, "72", flow, "VALUE_IN_EUROS", y), get(partner, "72", flow, "QUANTITY_IN_100KG", y)
            em, kt, uv = conv(v, q)
            long_rows.append([tag, FLOWLAB[flow], y, fmt(v, 2), fmt(q, 2), fmt(em), fmt(kt), fmt(uv, 2)])
write_csv("ch72_trade_by_partner_group_long.csv",
          ["partner", "flow", "year", "value_eur", "quantity_100kg", "value_eur_million", "net_mass_thousand_t",
           "unit_value_eur_per_t"], long_rows)


def trio(flow, y):
    out = {}
    for tag, p in (("ext", EXT), ("int", "INT_EU27_2020"), ("world", "WORLD")):
        v, q = get(p, "72", flow, "VALUE_IN_EUROS", y), get(p, "72", flow, "QUANTITY_IN_100KG", y)
        em, kt, _ = conv(v, q)
        out[tag] = (em, kt, v, q)
    return out


def share(a, b):
    return None if (a is None or not b) else 100.0 * a / b


rows = []
MAT = {}
max_gap_v = max_gap_q = 0.0
for y in YEARS:
    t1, t2 = trio("1", y), trio("2", y)
    rec = [y]
    sh = {}
    for lab, t in (("imports", t1), ("exports", t2)):
        for k in ("ext", "int", "world"):
            rec.append(fmt(t[k][0]))
        for k in ("ext", "int", "world"):
            rec.append(fmt(t[k][1]))
        # identity check world = ext + int on the raw units
        gv = gq = None
        if None not in (t["ext"][2], t["int"][2], t["world"][2]):
            gv = t["world"][2] - t["ext"][2] - t["int"][2]
            max_gap_v = max(max_gap_v, abs(gv))
        if None not in (t["ext"][3], t["int"][3], t["world"][3]):
            gq = t["world"][3] - t["ext"][3] - t["int"][3]
            max_gap_q = max(max_gap_q, abs(gq))
        rec += [fmt(gv, 2), fmt(gq, 2)]
        sv, sk = share(t["ext"][0], t["world"][0]), share(t["ext"][1], t["world"][1])
        rec += [fmt(sv, 3), fmt(sk, 3)]
        sh[lab] = (sv, sk)
    # two-way turnover share (X+M)
    def tw(idx):
        vals = [t1["ext"][idx], t2["ext"][idx], t1["world"][idx], t2["world"][idx]]
        if None in vals:
            return None
        return 100.0 * (vals[0] + vals[1]) / (vals[2] + vals[3])
    sh["turnover"] = (tw(0), tw(1))
    rec += [fmt(sh["turnover"][0], 3), fmt(sh["turnover"][1], 3)]
    MAT[y] = (sh, t1, t2)
    rows.append(rec)
hdr = ["year"]
for lab in ("imports", "exports"):
    hdr += ["%s_%s_value_eur_million" % (lab, k) for k in ("ext_eu", "intra_eu", "world")]
    hdr += ["%s_%s_mass_thousand_t" % (lab, k) for k in ("ext_eu", "intra_eu", "world")]
    hdr += ["%s_world_minus_ext_minus_int_value_eur" % lab, "%s_world_minus_ext_minus_int_quantity_100kg" % lab,
            "%s_extra_eu_share_of_world_value_pct" % lab, "%s_extra_eu_share_of_world_mass_pct" % lab]
hdr += ["twoway_X_plus_M_extra_eu_share_value_pct", "twoway_X_plus_M_extra_eu_share_mass_pct"]
write_csv("ch72_materiality_shares_1999_2025.csv", hdr, rows)
log("max |WORLD-EXT-INT| gap  value (EUR):", max_gap_v, " quantity (100 kg):", max_gap_q)

# balances by partner group
rows = []
for y in YEARS:
    sh, t1, t2 = MAT[y]
    rec = [y]
    for k in ("ext", "int", "world"):
        for idx in (0, 1):
            a, b = t2[k][idx], t1[k][idx]
            rec.append(fmt(None if (a is None or b is None) else a - b))
    rows.append(rec)
write_csv("ch72_balance_by_partner_group_1999_2025.csv",
          ["year", "extra_eu_balance_value_eur_million", "extra_eu_balance_mass_thousand_t",
           "intra_eu_balance_value_eur_million", "intra_eu_balance_mass_thousand_t",
           "world_balance_value_eur_million", "world_balance_mass_thousand_t"], rows)

# --- 5 by-product series --------------------------------------------------------------------------
long_rows = []
SER = {}
for p in BYPROD:
    for flow in ("1", "2"):
        for y in YEARS:
            v, q = get(EXT, p, flow, "VALUE_IN_EUROS", y), get(EXT, p, flow, "QUANTITY_IN_100KG", y)
            em, kt, uv = conv(v, q)
            SER[(p, flow, y)] = (v, q, em, kt, uv)
            long_rows.append([p, PRODLAB[p], FLOWLAB[flow], y, fmt(v, 2), fmt(q, 2), fmt(em), fmt(kt), fmt(uv, 2),
                              "value" if v is not None else "missing_value", "quantity" if q is not None else "missing_quantity"])
write_csv("byproduct_ext_eu_trade_long_1999_2025.csv",
          ["product", "description", "flow", "year", "value_eur", "quantity_100kg", "value_eur_million",
           "net_mass_thousand_t", "unit_value_eur_per_t", "value_status", "quantity_status"], long_rows)

for flow, nm in (("1", "imports"), ("2", "exports")):
    hdr = ["year"]
    for p in BYPROD:
        hdr += ["%s_value_eur_million" % p, "%s_mass_thousand_t" % p, "%s_unit_value_eur_per_t" % p]
    rows = []
    for y in YEARS:
        rec = [y]
        for p in BYPROD:
            _, _, em, kt, uv = SER[(p, flow, y)]
            rec += [fmt(em), fmt(kt), fmt(uv, 2)]
        rows.append(rec)
    write_csv("byproduct_%s_wide_1999_2025.csv" % nm, hdr, rows)

# subset consistency: 7204 + 7207 + 7208 are inside Chapter 72 (7304/7306 are Chapter 73, 26011200 Chapter 26)
viol = []
for flow in ("1", "2"):
    for y in YEARS:
        tot = get(EXT, "72", flow, "VALUE_IN_EUROS", y)
        parts = [SER[(p, flow, y)][0] for p in ("7204", "7207", "7208")]
        totq = get(EXT, "72", flow, "QUANTITY_IN_100KG", y)
        partsq = [SER[(p, flow, y)][1] for p in ("7204", "7207", "7208")]
        if tot is not None and sum(x for x in parts if x is not None) > tot * 1.0000001:
            viol.append(("value", flow, y))
        if totq is not None and sum(x for x in partsq if x is not None) > totq * 1.0000001:
            viol.append(("quantity", flow, y))
log("subset-consistency violations (7204+7207+7208 > Ch72):", viol)

# --- coverage table -------------------------------------------------------------------------------
rows = []
keys = [(EXT, "72", "2"), (EXT, "72", "1"), ("INT_EU27_2020", "72", "1"), ("INT_EU27_2020", "72", "2"),
        ("WORLD", "72", "1"), ("WORLD", "72", "2")] + [(EXT, p, f) for p in BYPROD for f in ("1", "2")]
for (pt, p, f) in keys:
    vy = [y for y in YEARS if get(pt, p, f, "VALUE_IN_EUROS", y) is not None]
    qy = [y for y in YEARS if get(pt, p, f, "QUANTITY_IN_100KG", y) is not None]
    both = [y for y in YEARS if y in vy and y in qy]
    miss = [y for y in YEARS if y not in both]
    rows.append([pt, p, FLOWLAB[f], len(vy), len(qy), len(both), min(both) if both else "", max(both) if both else "",
                 " ".join(str(y) for y in miss)])
write_csv("coverage_by_series_1999_2025.csv",
          ["partner", "product", "flow", "years_with_value", "years_with_quantity", "years_with_both",
           "first_year_both", "last_year_both", "years_missing_value_or_quantity"], rows)

# --- other workbook tables reproduced -------------------------------------------------------------
rows = []
# brief section 6: 2025 profiles (mass, value)
for l in txt:
    m = re.match(r"^(7207|7208|7209|7210|7219|7304|7306|26011200) \| [^|]+ \| ([\d.]+) \| ([\d.]+)$", l.strip())
    if m:
        code, wm, wv = m.group(1), float(m.group(2)), float(m.group(3))
        if code in BYPROD:
            _, _, em, kt, _ = SER[(code, "1", 2025)]
            rows.append(["brief section 6, 2025", code, "mass_kt", fmt(wm, 2), fmt(kt), fmt(None if kt is None else kt - wm, 4),
                         "yes" if kt is not None and round(kt, 2) == wm else "NO"])
            rows.append(["brief section 6, 2025", code, "value_eur_m", fmt(wv, 2), fmt(em), fmt(None if em is None else em - wv, 4),
                         "yes" if em is not None and round(em, 2) == wv else "NO"])
        else:
            rows.append(["brief section 6, 2025", code, "not re-pulled (not in task list)", m.group(2), "", "", ""])
base = open(SRC_BASE, encoding="utf-8").read().splitlines()
# Dataset C (Ch72 imports 2019-2025 with unit value) and Dataset D (7208)
def dataset_rows(header_prefix):
    i = next(k for k, l in enumerate(base) if l.startswith(header_prefix))
    out = {}
    for l in base[i:i + 14]:
        m = re.match(r"^(\d{4}) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+)$", l.strip())
        if m:
            out[int(m.group(1))] = tuple(float(m.group(k)) for k in (2, 3, 4))
    return out
dsC = dataset_rows("## Dataset C")
dsD = dataset_rows("## Dataset D")
for nm, ds, prod in (("Dataset C (Ch72 imports)", dsC, "72"), ("Dataset D (7208 imports)", dsD, "7208")):
    for y, (wv, wm, wu) in sorted(ds.items()):
        if prod == "72":
            v, q = get(EXT, "72", "1", "VALUE_IN_EUROS", y), get(EXT, "72", "1", "QUANTITY_IN_100KG", y)
            em, kt, uv = conv(v, q)
        else:
            _, _, em, kt, uv = SER[("7208", "1", y)]
        for lab, w, a, nd in (("value_eur_m", wv, em, 2), ("mass_kt", wm, kt, 2), ("unit_value_eur_t", wu, uv, 2)):
            rows.append([nm + " " + str(y), prod, lab, fmt(w, 2), fmt(a), fmt(None if a is None else a - w, 4),
                         "yes" if a is not None and round(a, nd) == w else "NO"])
write_csv("check_other_workbook_tables.csv",
          ["table_and_year", "product", "measure", "workbook", "api_unrounded", "diff_api_minus_workbook",
           "matches_after_2dp_rounding"], rows)
bad = [r for r in rows if r[-1] == "NO"]
log("other-table mismatches:", len(bad))
for r in bad:
    log("   ", r)

# --- Dataset B (German Steel Federation, steel mill products, all partners) vs Comext Chapter 72 WORLD -----
dsB = {}
i = next(k for k, l in enumerate(base) if l.startswith("## Dataset B"))
for l in base[i:i + 14]:
    m = re.match(r"^(\d{4}) \| ([\d.]+) \| ([\d.]+)$", l.strip())
    if m:
        dsB[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
log("Dataset B rows parsed:", len(dsB), min(dsB), max(dsB))
rows = []
for y in range(2017, 2026):
    xe, me, bv, xk, mk, bk, xu, mu = BAL[y]
    sh, t1, t2 = MAT[y]
    wx, wm = t2["world"][1], t1["world"][1]
    bx, bm = dsB.get(y, (None, None))
    rows.append([y, fmt(xk, 1), fmt(mk, 1), fmt(bk, 1), fmt(xe, 1), fmt(me, 1), fmt(bv, 1),
                 fmt(None if wx is None else wx / 1000.0, 3), fmt(None if wm is None else wm / 1000.0, 3),
                 fmt(None if (wx is None or wm is None) else (wx - wm) / 1000.0, 3),
                 fmt(bx, 1), fmt(bm, 1), fmt(None if bx is None else bx - bm, 1),
                 fmt(sh["imports"][1], 2), fmt(sh["exports"][1], 2), fmt(sh["imports"][0], 2), fmt(sh["exports"][0], 2)])
write_csv("slide_table_2017_2025.csv",
          ["year", "extra_eu_ch72_exports_kt", "extra_eu_ch72_imports_kt", "extra_eu_ch72_balance_kt",
           "extra_eu_ch72_exports_eur_m", "extra_eu_ch72_imports_eur_m", "extra_eu_ch72_balance_eur_m",
           "comext_ch72_world_exports_mt", "comext_ch72_world_imports_mt", "comext_ch72_world_balance_mt",
           "datasetB_steel_mill_products_exports_mt", "datasetB_imports_mt", "datasetB_balance_mt_rounded_inputs",
           "extra_eu_share_of_ch72_world_imports_mass_pct", "extra_eu_share_of_ch72_world_exports_mass_pct",
           "extra_eu_share_of_ch72_world_imports_value_pct", "extra_eu_share_of_ch72_world_exports_value_pct"], rows)

with open(os.path.join(HERE, "run_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(LOG) + "\n")
