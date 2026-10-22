"""Pull monthly (and annual cross-check) Comext DS-045409 series for the 2026 YTD comparison.

Run:  python -I -X utf8 01_pull_comext.py <raw_dir>

Writes one raw JSON-stat file per query plus raw/manifest.json (URL, HTTP status, UTC retrieval time,
sha256, dataset 'updated' stamp). Nothing is interpolated or filled.
"""
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409"
RAW = Path(sys.argv[1])
RAW.mkdir(parents=True, exist_ok=True)

queries = []
# Monthly: product x flow, both indicators in one call
for product in ("72", "7208", "7204"):
    for flow, flow_name in (("1", "imports"), ("2", "exports")):
        queries.append(
            dict(
                name=f"monthly_{product}_flow{flow}_{flow_name}",
                params=[
                    ("format", "JSON"), ("lang", "EN"), ("freq", "M"), ("reporter", "DE"),
                    ("partner", "EXT_EU27_2020"), ("product", product), ("flow", flow),
                    ("indicators", "VALUE_IN_EUROS"), ("indicators", "QUANTITY_IN_100KG"),
                    ("sinceTimePeriod", "2025-01"),
                ],
            )
        )
# Annual cross-check for 2024 and 2025 (to reconcile monthly sums against the workbook annual figures)
for product in ("72", "7208"):
    for flow, flow_name in (("1", "imports"), ("2", "exports")):
        queries.append(
            dict(
                name=f"annual_{product}_flow{flow}_{flow_name}",
                params=[
                    ("format", "JSON"), ("lang", "EN"), ("freq", "A"), ("reporter", "DE"),
                    ("partner", "EXT_EU27_2020"), ("product", product), ("flow", flow),
                    ("indicators", "VALUE_IN_EUROS"), ("indicators", "QUANTITY_IN_100KG"),
                    ("sinceTimePeriod", "2024"),
                ],
            )
        )

manifest = []
for q in queries:
    qs = "&".join(f"{k}={v}" for k, v in q["params"])
    url = f"{BASE}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": "inter-trade-present-research/1.0", "Accept": "application/json"})
    retrieved = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with urllib.request.urlopen(req, timeout=120) as r:
        body = r.read()
        status = r.status
    out = RAW / f"{q['name']}.json"
    out.write_bytes(body)
    d = json.loads(body.decode("utf-8"))
    manifest.append(
        dict(
            file=out.name,
            url=url,
            http_status=status,
            retrieved_utc=retrieved,
            sha256=hashlib.sha256(body).hexdigest(),
            bytes=len(body),
            dataset_updated=d.get("updated"),
            n_values=len(d.get("value", {})),
            positions_with_no_data=d.get("extension", {}).get("positions-with-no-data"),
        )
    )
    print(out.name, status, len(body), d.get("updated"), len(d.get("value", {})))

(RAW / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
