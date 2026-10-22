"""Convert Eurostat JSON-stat 2.0 responses to tidy CSV with observation status flags.

Usage (isolated mode, UTF-8):
    python -I -X utf8 jsonstat_tidy.py OUT.csv IN1.json [IN2.json ...]

Each output row: source_file, dataset, dataset_updated, <dimension columns...>, time, value, flag
Missing observations (no value in the response) are NOT written as zero; they are written with an
empty value only if they are explicitly present in the dimension grid and a flag exists for them.
Rows with no value and no flag are omitted (the API simply does not return them).
"""
import csv
import itertools
import json
import os
import sys


def tidy(path):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    ids = d["id"]
    sizes = d["size"]
    cats = {}
    for dim in ids:
        c = d["dimension"][dim]["category"]
        idx = c["index"]
        if isinstance(idx, list):
            idx = {k: i for i, k in enumerate(idx)}
        inv = {v: k for k, v in idx.items()}
        cats[dim] = [inv[i] for i in range(len(inv))]
    status = d.get("status", {}) or {}
    updated = d.get("updated", "")
    ext = d.get("extension", {}) or {}
    ds_id = ext.get("id", "")
    upd_data = ""
    for a in ext.get("annotation", []) or []:
        if a.get("type") == "UPDATE_DATA":
            upd_data = a.get("date", "")
    values = d.get("value", {}) or {}
    if isinstance(values, list):
        values = {str(i): v for i, v in enumerate(values) if v is not None}
    # strides
    strides = []
    acc = 1
    for s in reversed(sizes):
        strides.append(acc)
        acc *= s
    strides = list(reversed(strides))
    rows = []
    keys = set(values.keys()) | set(status.keys())
    for k in sorted(keys, key=int):
        flat = int(k)
        coords = []
        rem = flat
        for st in strides:
            coords.append(rem // st)
            rem = rem % st
        rec = {dim: cats[dim][c] for dim, c in zip(ids, coords)}
        rec["value"] = values.get(k, "")
        rec["flag"] = status.get(k, "")
        rec["source_file"] = os.path.basename(path)
        rec["dataset"] = ds_id
        rec["dataset_updated_api"] = updated
        rec["UPDATE_DATA"] = upd_data
        rows.append(rec)
    return ids, rows


def main():
    out = sys.argv[1]
    allrows = []
    dims_seen = []
    for p in sys.argv[2:]:
        ids, rows = tidy(p)
        for i in ids:
            if i not in dims_seen:
                dims_seen.append(i)
        allrows.extend(rows)
    cols = ["source_file", "dataset", "dataset_updated_api", "UPDATE_DATA"] + [
        c for c in dims_seen if c != "time"
    ] + ["time", "value", "flag"]
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in allrows:
            w.writerow(r)
    print(f"wrote {len(allrows)} rows to {out}")


if __name__ == "__main__":
    main()
