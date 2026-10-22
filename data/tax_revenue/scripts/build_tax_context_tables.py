"""Build the context table for the deck's tax row from Eurostat JSON responses saved in ../raw and the ETS table.

Inputs (all in ../raw): es_env_ac_tax_DE_raw.json, es_gov_10a_taxag_DE_S13_v2.json,
                        es_gov_10a_taxag_DE_S13_S212_totals.json, es_nama_10_gdp_DE_B1GQ.json
        and ../tables/ets1_auction_revenue_de_by_year.csv
Outputs: ../tables/de_tax_context_eurostat_1995_2025.csv   (one row per year, wide)
         ../tables/de_tax_context_eurostat_long.csv        (tidy long, with Eurostat status flags)
         ../tables/ets1_share_of_tax_context.csv           (ETS 1 auction revenue as share of context aggregates)
         ../tables/d29f_vs_ets1_lag_check.csv              (inference check, see README)
Run: python -I -X utf8 build_tax_context_tables.py
"""
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "raw"
OUT = HERE.parent / "tables"


def tidy(fn):
    d = json.load(open(RAW / fn, encoding="utf-8"))
    ids, size = d["id"], d["size"]
    dims = {k: list(d["dimension"][k]["category"]["index"]) for k in ids}
    status = d.get("status", {})
    rows = []
    for pos, v in d["value"].items():
        p = int(pos)
        coord = {}
        for k, s in reversed(list(zip(ids, size))):
            coord[k] = dims[k][p % s]
            p //= s
        coord["value"] = v
        coord["flag"] = status.get(pos, "")
        coord["dataset"] = d["extension"]["id"]
        coord["updated"] = d["updated"]
        rows.append(coord)
    return pd.DataFrame(rows)


env = tidy("es_env_ac_tax_DE_raw.json")
tax = tidy("es_gov_10a_taxag_DE_S13_v2.json")
tax2 = tidy("es_gov_10a_taxag_DE_S13_S212_totals.json")
gdp = tidy("es_nama_10_gdp_DE_B1GQ.json")

long_rows = []
for _, r in env.iterrows():
    long_rows.append(dict(dataset="env_ac_tax", year=int(r["time"]), sector="", item=r["tax"], unit=r["unit"], value=r["value"], flag=r["flag"], dataset_updated=r["updated"]))
for df in (tax, tax2):
    for _, r in df.iterrows():
        long_rows.append(dict(dataset="gov_10a_taxag", year=int(r["time"]), sector=r["sector"], item=r["na_item"], unit=r["unit"], value=r["value"], flag=r["flag"], dataset_updated=r["updated"]))
for _, r in gdp.iterrows():
    long_rows.append(dict(dataset="nama_10_gdp", year=int(r["time"]), sector="", item=r["na_item"], unit=r["unit"], value=r["value"], flag=r["flag"], dataset_updated=r["updated"]))
L = pd.DataFrame(long_rows).sort_values(["dataset", "item", "sector", "unit", "year"])
L.to_csv(OUT / "de_tax_context_eurostat_long.csv", index=False)


def series(dataset, item, unit, sector=""):
    s = L[(L.dataset == dataset) & (L["item"] == item) & (L.unit == unit) & (L.sector == sector)]
    return s.set_index("year")["value"]


def flags(dataset, item, unit, sector=""):
    s = L[(L.dataset == dataset) & (L["item"] == item) & (L.unit == unit) & (L.sector == sector)]
    return s.set_index("year")["flag"]


years = list(range(1995, 2026))
W = pd.DataFrame(index=years)
W.index.name = "year"
W["env_tax_total_meur"] = series("env_ac_tax", "ENV", "MIO_EUR")
W["env_tax_energy_meur"] = series("env_ac_tax", "NRG", "MIO_EUR")
W["env_tax_transport_meur"] = series("env_ac_tax", "TRA", "MIO_EUR")
W["env_tax_pollution_resources_meur"] = series("env_ac_tax", "POL_RES", "MIO_EUR")
W["env_tax_pct_gdp_eurostat"] = series("env_ac_tax", "ENV", "PC_GDP")
W["env_tax_pct_total_taxes_and_sc_incl_imputed_eurostat"] = series("env_ac_tax", "ENV", "PC_TSCO")
W["env_tax_pct_total_taxes_and_sc_excl_imputed_eurostat"] = series("env_ac_tax", "ENV", "PC_TSCO_X_ISCO")
W["taxes_d2_d5_d91_s13_meur"] = series("gov_10a_taxag", "D2_D5_D91", "MIO_EUR", "S13")
W["taxes_and_sc_incl_imputed_s13_s212_meur"] = series("gov_10a_taxag", "D2_D5_D91_D61_M_D995", "MIO_EUR", "S13_S212")
W["taxes_d2_d5_d91_s13_s212_meur"] = series("gov_10a_taxag", "D2_D5_D91", "MIO_EUR", "S13_S212")
W["d2_taxes_on_production_and_imports_s13_meur"] = series("gov_10a_taxag", "D2", "MIO_EUR", "S13")
W["d29f_taxes_on_pollution_s13_meur"] = series("gov_10a_taxag", "D29F", "MIO_EUR", "S13")
W["d5_current_taxes_on_income_wealth_s13_meur"] = series("gov_10a_taxag", "D5", "MIO_EUR", "S13")
W["d51b_c2_corporate_income_taxes_incl_holding_gains_s13_meur"] = series("gov_10a_taxag", "D51B_C2", "MIO_EUR", "S13")
W["d51a_c1_household_income_taxes_incl_holding_gains_s13_meur"] = series("gov_10a_taxag", "D51A_C1", "MIO_EUR", "S13")
W["d611_employers_actual_social_contributions_s13_meur"] = series("gov_10a_taxag", "D611", "MIO_EUR", "S13")
W["d613_households_actual_social_contributions_s13_meur"] = series("gov_10a_taxag", "D613", "MIO_EUR", "S13")
W["gdp_current_prices_meur"] = series("nama_10_gdp", "B1GQ", "CP_MEUR")
W["flag_env_tax"] = flags("env_ac_tax", "ENV", "MIO_EUR")
W["flag_taxes_s13"] = flags("gov_10a_taxag", "D2_D5_D91", "MIO_EUR", "S13")
W["flag_gdp"] = flags("nama_10_gdp", "B1GQ", "CP_MEUR")
W.reset_index().to_csv(OUT / "de_tax_context_eurostat_1995_2025.csv", index=False)

# checks on definitions
chk = (W["env_tax_total_meur"] / W["taxes_and_sc_incl_imputed_s13_s212_meur"] * 100).round(2)
diff = (chk - W["env_tax_pct_total_taxes_and_sc_incl_imputed_eurostat"]).abs()
print("ENV share of taxes+SC (own calc vs Eurostat PC_TSCO) max abs diff pp:", diff.max(), "years compared:", int(diff.notna().sum()))
chk2 = (W["env_tax_total_meur"] / W["gdp_current_prices_meur"] * 100).round(2)
diff2 = (chk2 - W["env_tax_pct_gdp_eurostat"]).abs()
print("ENV share of GDP (own calc vs Eurostat PC_GDP) max abs diff pp:", diff2.max(), "years compared:", int(diff2.notna().sum()))
parts = (W.env_tax_energy_meur + W.env_tax_transport_meur + W.env_tax_pollution_resources_meur - W.env_tax_total_meur).abs()
print("ENV = NRG + TRA + POL_RES, max abs diff MEUR:", parts.max())

# ETS shares
E = pd.read_csv(OUT / "ets1_auction_revenue_de_by_year.csv").set_index("year")
S = pd.DataFrame(index=sorted(E.index))
S.index.name = "year"
S["ets1_auction_revenue_eur_million"] = E["total_revenue_eur_million"]
S["taxes_d2_d5_d91_s13_meur"] = W["taxes_d2_d5_d91_s13_meur"]
S["taxes_and_sc_incl_imputed_s13_s212_meur"] = W["taxes_and_sc_incl_imputed_s13_s212_meur"]
S["env_tax_total_eurostat_meur"] = W["env_tax_total_meur"]
S["gdp_current_prices_meur"] = W["gdp_current_prices_meur"]
S["ets1_pct_of_taxes_d2_d5_d91"] = (S.ets1_auction_revenue_eur_million / S.taxes_d2_d5_d91_s13_meur * 100).round(3)
S["ets1_pct_of_taxes_and_sc"] = (S.ets1_auction_revenue_eur_million / S.taxes_and_sc_incl_imputed_s13_s212_meur * 100).round(3)
S["ets1_pct_of_env_tax_eurostat"] = (S.ets1_auction_revenue_eur_million / S.env_tax_total_eurostat_meur * 100).round(2)
S["ets1_pct_of_gdp"] = (S.ets1_auction_revenue_eur_million / S.gdp_current_prices_meur * 100).round(3)
S["note"] = ""
S.loc[2025, "note"] = "Eurostat tax aggregates and env_ac_tax have no 2025 observation in this vintage (blank, not zero); GDP 2025 available"
S.loc[2012, "note"] = "2012 ETS revenue includes 22 auctions derived as price x volume; see README"
S.reset_index().to_csv(OUT / "ets1_share_of_tax_context.csv", index=False)
print(S[["ets1_auction_revenue_eur_million", "ets1_pct_of_taxes_d2_d5_d91", "ets1_pct_of_taxes_and_sc", "ets1_pct_of_env_tax_eurostat", "ets1_pct_of_gdp"]].to_string())

# inference check: D29F(t) vs ETS1 revenue(t-1)
rows = []
for t in range(2013, 2026):
    d29f = W.loc[t, "d29f_taxes_on_pollution_s13_meur"]
    prev = E.loc[t - 1, "total_revenue_eur_million"] if (t - 1) in E.index else float("nan")
    cur = E.loc[t, "total_revenue_eur_million"] if t in E.index else float("nan")
    rows.append(dict(year=t, d29f_s13_meur=d29f, ets1_auction_revenue_same_year_meur=cur, ets1_auction_revenue_previous_year_meur=prev,
                     d29f_minus_previous_year_ets1_meur=(d29f - prev) if pd.notna(d29f) and pd.notna(prev) else None,
                     d29f_minus_same_year_ets1_meur=(d29f - cur) if pd.notna(d29f) and pd.notna(cur) else None))
R = pd.DataFrame(rows).round(2)
R.to_csv(OUT / "d29f_vs_ets1_lag_check.csv", index=False)
print(R.round(1).to_string(index=False))
