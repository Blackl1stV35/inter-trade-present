"""Build German EU-ETS auction revenue tables (2012-2025) from the EEX annual auction files.

Input : ../raw/eex_emission_spot_primary_market_auction_report_2012-2025_data.zip  (EEX, public download)
Output: ../tables/ets1_auction_level_de_2012_2025.csv
        ../tables/ets1_auction_revenue_de_by_year.csv
Run   : python -I -X utf8 build_ets_revenue_tables.py   (from the scripts folder)
Rules : German auctions = rows flagged Country == 'DE' (2012-2015, 2017-2025) or Auction Name == 'DE' (2016).
        Revenue is the file's 'Total Revenue' cell. Where the cell is empty (22 German auctions in Jan-Jun 2012) the
        value is derived as auction price x auction volume and flagged; the identity is verified on all reported rows.
"""
import io, re, zipfile, warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "raw"
OUT = HERE.parent / "tables"
OUT.mkdir(exist_ok=True)
ZIP = RAW / "eex_emission_spot_primary_market_auction_report_2012-2025_data.zip"


def load(xbytes, fname):
    x = pd.read_excel(io.BytesIO(xbytes), sheet_name=0, header=None)
    hr = None
    for i in range(12):
        if "Date" in [str(v).strip() for v in x.iloc[i, :].tolist()]:
            hr = i
            break
    hdr = [re.sub(r"\s+", " ", str(x.iloc[hr, j]).replace("\n", " ")).strip() for j in range(x.shape[1])]
    d = x.iloc[hr + 1:].copy()
    d.columns = hdr
    return d.dropna(subset=["Date"])


rows = []
with zipfile.ZipFile(ZIP) as z:
    for name in sorted(n for n in z.namelist() if re.search(r"-(\d{4})-data\.xlsx?$", n)):
        yr = int(re.search(r"-(\d{4})-data\.xlsx?$", name).group(1))  # year from the file name, not the folder name
        d = load(z.read(name), name)
        revc = [c for c in d.columns if c.startswith("Total Revenue")][0]
        volc = [c for c in d.columns if c.startswith("Auction Volume")][0]
        prc = [c for c in d.columns if c.startswith("Auction Price")][0]
        isde = (d["Country"].astype(str).str.strip() == "DE") if "Country" in d.columns else (d["Auction Name"].astype(str).str.strip() == "DE")
        g = d[isde].copy()
        for _, r in g.iterrows():
            rows.append(dict(
                year=yr, date=pd.to_datetime(r["Date"]).date().isoformat(), contract=str(r["Contract"]).strip(),
                product="EUAA (aviation)" if str(r["Contract"]).startswith("EAA") else "EUA",
                status=str(r["Status"]).strip() if "Status" in g.columns else "not given in file",
                price_eur_per_t=pd.to_numeric(r[prc], errors="coerce"),
                volume_t=pd.to_numeric(r[volc], errors="coerce"),
                revenue_reported_eur=pd.to_numeric(r[revc], errors="coerce"),
                source_file=name.split("/")[-1]))
a = pd.DataFrame(rows).sort_values(["year", "date"]).reset_index(drop=True)

# identity check price x volume == reported revenue
rep = a.dropna(subset=["revenue_reported_eur", "price_eur_per_t", "volume_t"]).copy()
rep["calc"] = rep.price_eur_per_t * rep.volume_t
rep["absdiff"] = (rep.calc - rep.revenue_reported_eur).abs()
print("rows with reported revenue:", len(rep), "max |price*volume - reported| EUR:", round(rep.absdiff.max(), 2),
      "rows with diff > 1 EUR:", int((rep.absdiff > 1).sum()))

a["revenue_eur_used"] = a.revenue_reported_eur
mask = a.revenue_reported_eur.isna() & a.price_eur_per_t.notna() & a.volume_t.notna()
a.loc[mask, "revenue_eur_used"] = (a.loc[mask, "price_eur_per_t"] * a.loc[mask, "volume_t"]).round(2)
a["revenue_basis"] = "reported in EEX file"
a.loc[mask, "revenue_basis"] = "derived: price x volume (cell empty in EEX file)"
assert a.revenue_eur_used.notna().all()
bad = a[~a.status.isin(["successful", "not given in file"])]
assert bad.empty, bad
a.to_csv(OUT / "ets1_auction_level_de_2012_2025.csv", index=False)

# annual table
def agg(sub):
    return pd.Series(dict(n=len(sub), vol=sub.volume_t.sum(), rev=sub.revenue_eur_used.sum(),
                          rev_rep=sub.revenue_reported_eur.sum(min_count=1), n_derived=int(sub.revenue_reported_eur.isna().sum())))
recs = []
for yr, g in a.groupby("year"):
    e = agg(g[g["product"] == "EUA"]) if (g["product"] == "EUA").any() else None
    v = agg(g[g["product"] != "EUA"]) if (g["product"] != "EUA").any() else None
    tot_rev = g.revenue_eur_used.sum()
    tot_vol = g.volume_t.sum()
    rec = dict(
        year=yr,
        eua_auctions=int(e.n) if e is not None else 0, eua_volume_t=int(e.vol) if e is not None else 0,
        eua_revenue_eur=round(e.rev, 2) if e is not None else 0.0,
        euaa_auctions=int(v.n) if v is not None else 0, euaa_volume_t=int(v.vol) if v is not None else 0,
        euaa_revenue_eur=round(v.rev, 2) if v is not None else 0.0,
        total_auctions=len(g), total_volume_t=int(tot_vol), total_revenue_eur=round(tot_rev, 2),
        total_revenue_eur_million=round(tot_rev / 1e6, 3),
        avg_price_eur_per_t=round(tot_rev / tot_vol, 2),
        auctions_with_derived_revenue=int(g.revenue_reported_eur.isna().sum()),
        revenue_eur_reported_cells_only=round(g.revenue_reported_eur.sum(min_count=1), 2))
    recs.append(rec)
y = pd.DataFrame(recs)
y["euaa_share_of_total_revenue_pct"] = (y.euaa_revenue_eur / y.total_revenue_eur * 100).round(2)
# explicit note: no EUAA row in a year means no separate German EUAA auction in the EEX file (not zero revenue observed)
y["euaa_note"] = ["no separate German EUAA auction in EEX file" if r.euaa_auctions == 0 else "" for r in y.itertuples()]
y.loc[y.year == 2025, "euaa_note"] = "no EUAA contract in 2025 file (all German 2025 auctions carry contract T3PA = EUA)"
y.to_csv(OUT / "ets1_auction_revenue_de_by_year.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(y[["year", "eua_auctions", "eua_revenue_eur", "euaa_auctions", "euaa_revenue_eur", "total_revenue_eur", "total_volume_t", "avg_price_eur_per_t", "auctions_with_derived_revenue"]].to_string(index=False))
