# Builds tidy tables from the raw EEX auction report and checks the Commission's published CBAM prices.
# Run: python -I -X utf8 scripts/build_tables.py   (from the cbam_price folder)
import csv, datetime as dt, collections, sys, warnings, os
warnings.filterwarnings("ignore")
import openpyxl

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "raw", "eex_emission_spot_primary_market_auction_report_2026.xlsx")

wb = openpyxl.load_workbook(RAW, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
h = [i for i, r in enumerate(rows) if r[1] == "Date"][0]
recs = []
for r in rows[h + 1:]:
    if r[1] is None:
        continue
    recs.append(dict(
        date=r[1].date().isoformat(),
        auction_name=r[3], contract=r[4], status=r[5],
        clearing_price_eur_per_tco2=r[6], volume_tco2=r[11], zone=r[25],
        total_revenue_eur=r[24]))
recs.sort(key=lambda x: (x["date"], x["auction_name"]))
assert all(x["status"] == "successful" for x in recs)
for x in recs:  # internal consistency: revenue = price * volume
    assert abs(x["total_revenue_eur"] - x["clearing_price_eur_per_tco2"] * x["volume_tco2"]) < 1.0, x

def w(name, fields, data):
    with open(os.path.join(BASE, name), "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=fields)
        wr.writeheader()
        wr.writerows(data)

w("eex_eua_auctions_2026_tidy.csv", list(recs[0].keys()), recs)
w("eua_auctions_october_2026.csv", list(recs[0].keys()), [x for x in recs if x["date"] >= "2026-10-01"])

def qkey(d):
    y, m, _ = map(int, d.split("-"))
    return f"{y}Q{(m - 1) // 3 + 1}"

published = {"2026Q1": (75.36, "2026-04-07"), "2026Q2": (75.28, "2026-07-06"), "2026Q3": (82.32, "2026-10-05")}
agg = collections.defaultdict(lambda: dict(pv=0.0, v=0.0, n=0, ps=0.0, last=""))
agg_eu = collections.defaultdict(lambda: dict(pv=0.0, v=0.0))
for x in recs:
    k = qkey(x["date"]); a = agg[k]
    a["pv"] += x["clearing_price_eur_per_tco2"] * x["volume_tco2"]; a["v"] += x["volume_tco2"]; a["n"] += 1
    a["ps"] += x["clearing_price_eur_per_tco2"]; a["last"] = max(a["last"], x["date"])
    if x["zone"] == "EU":
        b = agg_eu[k]; b["pv"] += x["clearing_price_eur_per_tco2"] * x["volume_tco2"]; b["v"] += x["volume_tco2"]
chk = []
for k in sorted(agg):
    a = agg[k]; vw = a["pv"] / a["v"]
    pub = published.get(k)
    chk.append(dict(
        quarter=k, auctions_n=a["n"], volume_tco2=int(a["v"]), last_auction_in_file=a["last"],
        eex_volume_weighted_avg_all_auctions=round(vw, 4),
        eex_volume_weighted_avg_rounded_2dp=round(vw, 2),
        eex_simple_mean=round(a["ps"] / a["n"], 4),
        eex_volume_weighted_avg_CAP3_EU_only=round(agg_eu[k]["pv"] / agg_eu[k]["v"], 4),
        commission_published_price=pub[0] if pub else "",
        matches_published_to_the_cent=("yes" if pub and round(vw, 2) == pub[0] else ("n/a - quarter not complete, no Commission price" if not pub else "NO")),
        note=("" if pub else "QUARTER IN PROGRESS: partial average for context only; NOT the CBAM certificate price")))
w("eex_quarterly_weighted_check.csv", list(chk[0].keys()), chk)
for c in chk:
    print(c)

# Date arithmetic for the legal timeline
def wd(s):
    return dt.date.fromisoformat(s).strftime("%A")
def week_mon(d):
    return d - dt.timedelta(days=d.weekday())
tl = []
for q, qstart, qend in [("2026Q1", "2026-01-01", "2026-03-31"), ("2026Q2", "2026-04-01", "2026-06-30"),
                         ("2026Q3", "2026-07-01", "2026-09-30"), ("2026Q4", "2026-10-01", "2026-12-31")]:
    nxt = dt.date.fromisoformat(qend) + dt.timedelta(days=1)       # first day of following quarter
    wk_start = week_mon(nxt)                                        # Monday of the calendar week containing it
    wk_end = wk_start + dt.timedelta(days=6)
    pub_monday = wk_start + dt.timedelta(days=7)                    # first day of the following calendar week
    tl.append(dict(quarter=q, quarter_end=qend, quarter_end_weekday=wd(qend),
                   first_calendar_week_of_following_quarter=f"{wk_start} to {wk_end} (Mon-Sun, week containing {nxt})",
                   earliest_first_day_of_next_week=f"{pub_monday} ({pub_monday.strftime('%A')})",
                   commission_publication_date=(published[q][1] if q in published else "4 January 2027 (scheduled on Commission page; price blank on 2026-10-22)" if q == "2026Q4" else "")))
w("publication_timing_check.csv", list(tl[0].keys()), tl)
for t in tl:
    print(t)
for s in ["2026-12-31", "2027-01-01", "2027-01-04", "2027-02-01", "2027-09-30", "2026-11-16", "2026-11-18", "2026-12-14"]:
    print(s, wd(s))
