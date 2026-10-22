"""Probe which Eurostat gov_10a_taxag lines are populated for Germany (D51B, D29C etc.) and save the result.
Output: ../raw/eurostat_availability_probe.json
Run: python -I -X utf8 probe_eurostat_availability.py
"""
import json
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "raw"
BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10a_taxag?format=JSON&lang=EN&geo=DE&unit=MIO_EUR&sector={sector}&na_item={item}"
items = ["D51B", "D51A", "D29C", "D51", "D51B_C2", "D51A_C1", "D611", "D613", "D29F", "D211", "D214A"]
out = {"retrieved": "2026-10-22", "query_template": BASE, "results": []}
for sector in ("S13",):
    for it in items:
        url = BASE.format(sector=sector, item=it)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research; student project)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        times = list(d["dimension"]["time"]["category"]["index"])
        vals = d.get("value", {})
        idx = sorted(int(k) for k in vals)
        out["results"].append({"sector": sector, "na_item": it, "observations": len(vals),
                               "first": times[idx[0]] if idx else None, "last": times[idx[-1]] if idx else None,
                               "dataset_updated": d.get("updated")})
(RAW / "eurostat_availability_probe.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
for r in out["results"]:
    print(r)
