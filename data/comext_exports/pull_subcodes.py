#!/usr/bin/env python
"""Classification-break check: pull every HS6 and CN8 sub-code that the Comext product codelist lists under
HS 7204, 7207, 7208, 7304, 7306 (partner EXT_EU27_2020, reporter DE, both flows, 1999-2025) and record in which
years each code carries trade. Run after pull_comext.py:  python -I -X utf8 pull_subcodes.py
Writes only inside its own folder.
"""
import csv
import datetime
import hashlib
import json
import os
import urllib.parse
import urllib.request
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
API = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409"
YEARS = list(range(1999, 2026))
HEADINGS = ["7204", "7207", "7208", "7304", "7306"]
codes_doc = json.load(open(os.path.join(RAW, "product_codes_target_headings.json"), encoding="utf-8"))
CODES = codes_doc["codes"]


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


MAN = []
DATA = {}
for h in HEADINGS:
    subs = sorted(c for c in CODES if c.startswith(h) and len(c) in (6, 8))
    for flow in ("1", "2"):
        q = [("format", "JSON"), ("lang", "EN"), ("freq", "A"), ("reporter", "DE"), ("partner", "EXT_EU27_2020")]
        q += [("product", c) for c in [h] + subs]
        q += [("flow", flow), ("indicators", "VALUE_IN_EUROS"), ("indicators", "QUANTITY_IN_100KG"), ("sinceTimePeriod", "1999")]
        url = API + "?" + urllib.parse.urlencode(q)
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "inter-trade-present-datacheck/1.0"})
                with urllib.request.urlopen(req, timeout=180) as r:
                    body, status = r.read(), r.status
                break
            except Exception as e:  # noqa
                print("retry", h, flow, e)
                time.sleep(3 + 3 * attempt)
        else:
            raise SystemExit("failed " + h)
        name = "sub_%s_flow%s" % (h, flow)
        with open(os.path.join(RAW, name + ".json"), "wb") as f:
            f.write(body)
        d = json.loads(body.decode("utf-8"))
        MAN.append({"file": "raw/%s.json" % name, "url": url, "http_status": status,
                    "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(), "api_updated": d.get("updated"),
                    "codes_requested": len(subs) + 1})
        DATA.update({(h,) + k: v for k, v in parse(d).items()})
        print("pulled", name, "codes", len(subs), "cells", len(d["value"]), "bytes", len(body))
with open(os.path.join(RAW, "_manifest_subcodes.json"), "w", encoding="utf-8") as f:
    json.dump(MAN, f, indent=1)

# ---- per code: first/last year with a value, years count --------------------------------------------
rows = []
for h in HEADINGS:
    subs = sorted(c for c in CODES if c.startswith(h) and len(c) in (6, 8))
    for flow in ("1", "2"):
        for c in subs:
            ys = [y for y in YEARS if DATA.get((h, c, flow, "VALUE_IN_EUROS", y)) is not None]
            pos = [y for y in ys if DATA[(h, c, flow, "VALUE_IN_EUROS", y)] > 0]
            if not ys:
                continue
            tot = sum(DATA[(h, c, flow, "VALUE_IN_EUROS", y)] for y in ys)
            rows.append([h, "HS6" if len(c) == 6 else "CN8", "special (NES/confidential/plant components)" if not c.isdigit() else "regular",
                         c, CODES[c][:90], "import" if flow == "1" else "export",
                         min(ys), max(ys), len(ys), "%.0f" % tot])
with open(os.path.join(HERE, "subcodes_first_last_year.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["heading", "level", "code_type", "code", "description", "flow", "first_year_with_value", "last_year_with_value",
                "years_with_value", "cumulative_value_eur_1999_2025"])
    w.writerows(rows)
print("subcodes_first_last_year.csv", len(rows))

# ---- per heading/flow/year: consistency of heading total with sum of sub-codes -----------------------
rows = []
for h in HEADINGS:
    subs6 = [c for c in CODES if c.startswith(h) and len(c) == 6]
    subs8 = [c for c in CODES if c.startswith(h) and len(c) == 8]
    for flow in ("1", "2"):
        for y in YEARS:
            tot = DATA.get((h, h, flow, "VALUE_IN_EUROS", y))
            s6 = sum(DATA.get((h, c, flow, "VALUE_IN_EUROS", y), 0.0) for c in subs6)
            s8 = sum(DATA.get((h, c, flow, "VALUE_IN_EUROS", y), 0.0) for c in subs8)
            sp = sum(DATA.get((h, c, flow, "VALUE_IN_EUROS", y), 0.0) for c in subs8 if not c.isdigit())
            n6 = sum(1 for c in subs6 if DATA.get((h, c, flow, "VALUE_IN_EUROS", y)) is not None)
            n8 = sum(1 for c in subs8 if DATA.get((h, c, flow, "VALUE_IN_EUROS", y)) is not None)
            rows.append([h, "import" if flow == "1" else "export", y, "" if tot is None else "%.2f" % tot,
                         "%.2f" % s6, "%.2f" % s8, "" if tot is None else "%.4f" % (s6 / tot if tot else float("nan")),
                         "" if tot is None else "%.4f" % (s8 / tot if tot else float("nan")), n6, n8,
                         "%.2f" % sp, "" if not tot else "%.4f" % (sp / tot)])
with open(os.path.join(HERE, "subcodes_consistency_by_year.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["heading", "flow", "year", "heading_value_eur", "sum_hs6_value_eur", "sum_cn8_value_eur",
                "sum_hs6_over_heading", "sum_cn8_over_heading", "n_hs6_codes_with_value", "n_cn8_codes_with_value",
                "special_cn8_codes_value_eur", "special_cn8_share_of_heading"])
    w.writerows(rows)
print("subcodes_consistency_by_year.csv", len(rows))
