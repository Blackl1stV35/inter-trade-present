# Comext pull: German steel exports, balance, materiality, by-product series

Eurostat Comext dissemination API, dataset **DS-045409** ("EU trade since 1988 by HS2-4-6 and CN8"), reporter DE.
Retrieved **2026-10-22** (script clock, UTC 02:40-02:46). All numbers below come from the raw JSON files in `raw/`; nothing is recalled or estimated.

**Data vintage reported by Comext:** every response says `updated = 2026-10-16T11:00:00+0200`; the SDMX dataflow record gives the same timestamp for `UPDATE_DATA`, `UPDATE_STRUCTURE` and `DISSEMINATION_TIMESTAMP_DATA` (data structure version 6.6). The workbook's imports table was retrieved on the previous vintage (**15 September 2026**), so this pull is one monthly update newer.
Eurostat's metadata page (ESMS `ext_go_detail_sims`, metadata last updated 6 Oct 2025) says detailed data are revised whenever revisions arrive and are "considered final by October of the following reference year"; the date of the next update was not found and is not verified.

## Queries (exact parameters)

Base URL: `https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409`
Common parameters: `format=JSON&lang=EN&freq=A&reporter=DE&indicators=VALUE_IN_EUROS&indicators=QUANTITY_IN_100KG&sinceTimePeriod=1995`
Flow codes: 1 = import, 2 = export. Partner codes: `EXT_EU27_2020` (extra-EU27, fixed 2020 composition), `INT_EU27_2020` (intra-EU27), `WORLD`.

| Raw file | partner | product | flow |
| --- | --- | --- | --- |
| `ch72_ext_flow2.json` (task item 1) | EXT_EU27_2020 | 72 | 2 |
| `ch72_ext_flow1.json` (task item 2) | EXT_EU27_2020 | 72 | 1 |
| `ch72_int_flow1/2.json` (item 4) | INT_EU27_2020 | 72 | 1, 2 |
| `ch72_world_flow1/2.json` (item 4) | WORLD | 72 | 1, 2 |
| `byproduct_ext_flow1/2.json` (item 5) | EXT_EU27_2020 | 7204, 7207, 7208, 7304, 7306, 26011200 | 1, 2 |
| `ch72_headings_flow1/2.json` (extra: decomposition) | EXT_EU27_2020 | 72, 7201-7229, 72XX/72CC/72II/72MM/72SS/72VV | 1, 2 |
| `sub_<heading>_flow1/2.json` (extra: classification check) | EXT_EU27_2020 | every HS6 and CN8 code the codelist lists under 7204, 7207, 7208, 7304, 7306 | 1, 2 (`sinceTimePeriod=1999`) |
| `probe_pre1999_*.json` (extra: coverage) | EXT_EU27_2020, INT_EU27_2020, WORLD | 72 | 1, 2 (`sinceTimePeriod=1988&untilTimePeriod=1999`) |

Full URLs, UTC timestamps, byte counts and SHA-256 per file: `raw/_manifest.json`, `raw/_manifest_subcodes.json`, `raw/_manifest_ch72_headings.json`.
Other raw files: `dataflow_DS-045409.xml` and `datastructure_DS-045409.xml` (SDMX metadata, vintage), `product_codes_target_headings.json` and `ch72_heading_codes.json` (code subsets cut from the CXT_NC codelist, v11.0, `.../sdmx/2.1/codelist/ESTAT/CXT_NC/latest`; the 24.5 MB full list is not stored), `wco_correlation_check.md` (classification note with WCO sources).
Several `product=` / `flow=` parameters in one call work; the API returns category codes sorted, not in request order, so the script maps values through each dimension's category index.

## Units and conversions (same as the workbook)

- thousand tonnes = QUANTITY_IN_100KG / 10 / 1000 (= / 10,000)
- EUR million = VALUE_IN_EUROS / 1,000,000
- unit value EUR/t = VALUE_IN_EUROS / (QUANTITY_IN_100KG / 10)
- balance = exports - imports (X - M), same unit, same year; only computed when both are present
- values are nominal (current EUR); Comext statistical value is FOB for exports and CIF for imports (ESMS page)
- missing observations are empty cells; nothing is zero-filled. A genuine returned 0 stays 0.

## Results

### 1. Extra-EU Chapter 72 exports (DE -> EXT_EU27_2020, flow 2)
All 27 years 1999-2025 return both value and quantity. 1995-1998 and 2026 return nothing (the response lists time positions 0-3 and 31 as "no data"); nothing was filled. Files: `ch72_extra_eu_exports_1999_2025.csv`.
Key values (EUR million / thousand tonnes): 2017 6,073.5 / 7,217.1; 2019 5,623.5 / 6,356.4; 2021 6,036.4 / 5,689.5; 2022 7,628.1 (value peak) / 5,221.8; 2024 6,238.3 / 5,048.3; 2025 5,427.9 / 4,681.2 (tonnage minimum of the series; maximum was 8,250.9 kt in 2012).
Export unit value EUR/t: 842 (2017), 885 (2019), 1,461 (2022), 1,160 (2025).

### 2. Re-pulled imports versus the workbook's update-tab 4.2 table (`check_imports_vs_workbook_4_2.csv`)
26 of 27 years reproduce the workbook table exactly after rounding to 2 decimals (value and mass). **One year differs: 2023.**

| 2023 | Workbook | Re-pull (vintage 16 Oct 2026) | Diff |
| --- | --- | --- | --- |
| Value EUR million | 2,107.38 | 2,106.93 | -0.45 (-0.02%) |
| Net mass kt | 2,088.99 | 2,088.77 | -0.22 (-0.01%) |
| Unit value EUR/t (Dataset C) | 1,008.80 | 1,008.69 | -0.11 |

The likely cause is the newer vintage (revision of 2023 data in the 16 Oct update); the earlier vintage cannot be retrieved from the dissemination API, so the cause is not verified. The slide-level rounded figures (2,107 EUR m; 2,089 kt; 1,009 EUR/t) are unchanged. 2024 and 2025 match.
Other workbook tables re-checked (`check_other_workbook_tables.csv`): Dataset D (7208, 2019-2025) matches; section 6 (2025) matches for 7207, 7208 and 26011200 but not for 7304 (mass 87.37 vs 87.38 kt; value 233.30 vs 233.39 EUR m) and 7306 (value 232.37 vs 232.36 EUR m), again small revisions.

### 3. Extra-EU balance X - M (`ch72_extra_eu_balance_1999_2025.csv`)
Positive in **every** year 1999-2025, in both value and tonnes. Range: tonnes +903 kt (2007) to +4,523 kt (2003); value +EUR 1,286 m (2007) to +4,457 m (2022).

| Year | X kt | M kt | X - M kt | X EUR m | M EUR m | X - M EUR m |
| --- | --- | --- | --- | --- | --- | --- |
| 2017 | 7,217.1 | 4,623.5 | +2,593.6 | 6,073.5 | 2,890.1 | +3,183.4 |
| 2018 | 6,982.6 | 4,666.3 | +2,316.4 | 6,387.3 | 3,345.4 | +3,042.0 |
| 2019 | 6,356.4 | 3,342.0 | +3,014.4 | 5,623.5 | 2,459.5 | +3,164.0 |
| 2020 | 5,444.7 | 2,833.8 | +2,610.9 | 4,659.4 | 1,862.5 | +2,796.9 |
| 2021 | 5,689.5 | 3,337.4 | +2,352.1 | 6,036.4 | 2,762.7 | +3,273.8 |
| 2022 | 5,221.8 | 2,697.2 | +2,524.6 | 7,628.1 | 3,171.2 | +4,457.0 |
| 2023 | 5,044.1 | 2,088.8 | +2,955.3 | 6,435.5 | 2,106.9 | +4,328.6 |
| 2024 | 5,048.3 | 1,954.6 | +3,093.7 | 6,238.3 | 1,876.9 | +4,361.3 |
| 2025 | 4,681.2 | 1,463.6 | +3,217.6 | 5,427.9 | 1,591.0 | +3,837.0 |

2017 to 2025: exports -35.1% (tonnes), -10.6% (value); imports -68.3% (tonnes), -45.0% (value); balance +24.1% (tonnes), +20.5% (value). 2021 to 2025: exports -17.7%, imports -56.1% (tonnes). The surplus widened because imports fell much more than exports; exports are at a 27-year low in tonnes.

### 4. Materiality: extra-EU share of total German Chapter 72 trade (`ch72_materiality_shares_1999_2025.csv`, `slide_table_2017_2025.csv`)
WORLD = INT_EU27_2020 + EXT_EU27_2020 holds in every year/flow/indicator (max gap 0 EUR and 3e-8 x 100 kg). Share = EXT / WORLD.

| Year | Imports, mass % | Imports, value % | Exports, mass % | Exports, value % | X+M, mass % | X+M, value % |
| --- | --- | --- | --- | --- | --- | --- |
| 2017 | 13.4 | 11.3 | 21.5 | 26.1 | 17.4 | 18.3 |
| 2018 | 14.1 | 12.0 | 21.4 | 25.9 | 17.7 | 18.5 |
| 2019 | 11.4 | 10.1 | 20.2 | 24.7 | 15.9 | 17.1 |
| 2020 | 11.5 | 9.8 | 18.7 | 24.1 | 15.4 | 17.0 |
| 2021 | 11.1 | 9.2 | 18.1 | 21.7 | 14.7 | 15.2 |
| 2022 | 9.9 | 8.5 | 17.8 | 21.4 | 14.0 | 14.8 |
| 2023 | 8.7 | 7.2 | 17.3 | 21.2 | 13.4 | 14.4 |
| 2024 | 8.1 | 7.3 | 17.2 | 22.0 | 13.1 | 14.9 |
| 2025 | 6.1 | 6.6 | 16.0 | 20.6 | 11.5 | 13.9 |

All-partner Chapter 72 totals: imports 34,425 kt (2017) -> 24,029 kt (2024) -> 24,057 kt (2025); exports 33,520 -> 29,266 -> 29,203 kt. Extra-EU accounts for 30.5% of the 2017-2025 fall in all-partner import tonnes (3,160 of 10,368 kt) while holding 13.4% of 2017 import tonnes; for exports it accounts for 58.8% of the fall (2,536 of 4,316 kt). The like-for-like 2024 import share is 8.1% by mass (7.3% by value), not "a tenth": the 18.8 Mt in Dataset B is a different product universe (steel mill products), so 1,955 kt / 18.8 Mt = 10.4% mixes universes.
Balances by group are in `ch72_balance_by_partner_group_1999_2025.csv`. The sign of the extra-EU balance and of the all-partner balance differ in some years: 2017 extra-EU +2,594 kt, intra-EU -3,499 kt, all-partner -905 kt.

Comparison with Dataset B (`slide_table_2017_2025.csv`): Comext Chapter 72 all-partner balance -0.9 Mt (2017), -0.5 (2018), +2.2 (2019), +4.5 (2020), +1.4 (2021), +2.1 (2022), +5.2 (2023), +5.2 (2024); Dataset B (steel mill products, rounded inputs) -1.2, -1.6, +0.3, +1.4, -0.4, +0.4, +3.0, +4.1. Same direction over time but different levels, and the sign differs in 2021 (+1.4 vs -0.4 Mt): different product lists (Chapter 72 incl. scrap, pig iron, ferro-alloys; Dataset B = rolled/forged products, pipes etc. per the workbook), so do not mix them.

### 5. By-product series (extra-EU, DE; `byproduct_*_wide_1999_2025.csv`, `byproduct_ext_eu_trade_long_1999_2025.csv`)
All six codes return all 27 years for imports and exports, except export flow of **26011200**, which returns only 5 years (2008, 2016, 2023, 2024, 2025; values only EUR 635 to 93,871 a year, i.e. negligible; the other 22 years are missing, not zero). Coverage: `coverage_by_series_1999_2025.csv`.
Reference points (imports; kt / EUR m / EUR per t): 7204 scrap 2017 705.6 / 230.2 / 326 -> 2025 393.9 / 178.2 / 452; 7207 2008 1,104.0 -> 2025 175.2 / 88.6 / 506; 7208 1999 733.6 -> 2025 32.7 / 33.0 / 1,009; 7304 2025 87.4 / 233.3 / 2,670; 7306 2025 159.4 / 232.4 / 1,457; 26011200 2018 7,165.7 (peak) -> 2024 4,902.0 -> 2025 2,035.1 kt (-58% in 2025), 117 EUR/t.
Exports (kt): 7204 scrap 1,230.8 in 2025 (net exporter to non-EU: +837 kt vs imports 393.9); 7207 97.0; 7208 310.2; 7304 165.4; 7306 140.0.
HS 7304 and 7306 are Chapter 73 and 26011200 is Chapter 26, so they are not inside the Chapter 72 totals; 7204, 7207, 7208 are (check passed: their sum never exceeds the Chapter 72 total).

**Extra finding (not requested but material): heading 7203** (ferrous products obtained by direct reduction of iron ore / spongy ferrous products) is the single biggest mover of the Chapter 72 import series (`ch72_headings_*.csv`): imports 1,016 kt (22% of Chapter 72 extra-EU import tonnes) in 2017, 438 kt in 2024, **28 kt** in 2025. It accounts for 987 kt (31%) of the 3,160 kt fall 2017-2025, 667 kt (36%) of the 1,874 kt fall 2021-2025, and 410 of the 491 kt (84%) fall 2024-2025. The three by-product headings in Chapter 72 (7204, 7207, 7208) together explain only 720 kt (23%) of the 2017-2025 fall. Chapter 72 imports excluding 7203: 3,608 kt (2017), 2,623 (2019), 2,642 (2021), 2,012 (2022), 1,429 (2023), 1,516 (2024), 1,435 (2025).
For 2004 to 2005 (imports +838 kt), 7207 semi-finished products contributed +714 kt (85%); for 2004-2007 (+2,384 kt) 7207 contributed +769 kt (32%).
Heading-level unit values rose in 2022 as well as the aggregate (2021 -> 2022): 7203 +32%, 7204 +21%, 7207 +12%, 7208 +45%; aggregate 828 -> 1,176 EUR/t. Unit values are mix-affected and are not price indices. The cause of the 7203 collapse is not established here.

### 6. Classification notes
- **Partner boundary.** `EXT_EU27_2020` / `INT_EU27_2020` are fixed-composition aggregates (UK counts as extra-EU in all years) and exist only from 1999 for Germany (the pre-1999 probe returns values only for 1999); `WORLD` goes back to 1988. Extra-EU imports are assigned by country of origin, intra-EU imports by country of consignment (ESMS), so non-EU steel cleared in another member state reaches Germany as "intra-EU".
- **HS revisions** (WCO Table I for HS 2002, 2007, 2012, 2017, 2022; `raw/wco_correlation_check.md`): no entries for 7204, 7207, 7208 or 2601.12 in any edition; Chapter 72 changed only inside headings 7225/7226/7229 in HS 2007; headings 7304 and 7306 had subheadings subdivided in HS 2007 (still inside the same four-digit heading). Live Comext data agree: HS6 code sets under 7204, 7207 and 7208 are identical in every year 1999-2025 (`subcodes_first_last_year.csv`); under 7304/7306 the HS6 codes split in 2007. **So no classification break at heading level for the series used; a sub-heading break in 2007 for 7304 and 7306 only matters if someone uses HS6 detail.** The WCO tables are a guide with no legal status; heading-level moves between 2-digit chapters were checked only through the entries found.
- **Comext special codes.** Heading totals contain "not elsewhere specified / confidential" codes: `7304XX` is used 1999-2005 only and holds 6-14% of 7304 export value in those years (`subcodes_consistency_by_year.csv`: heading total = sum of sub-codes incl. special codes in every year). Heading series are therefore complete, but the sub-heading split of 7304 exports before 2006 is not.
- **CN8 codes** change every year (ESMS); the CN8 code 26011200 is stable. The number of CN8 codes with trade under 7208 imports drops from 27 (2003) to 17 (2004), with no effect on the heading totals (heading total = sum of sub-codes).
- **Visible jumps that are not classification:** 7207 imports rise from 280 kt (2004) to 994 kt (2005); 7203 imports collapse in 2025; 26011200 imports halve in 2025; 7304/7306 export unit values rise strongly from 2022. They are real series movements in the data; causes are not established.

## Checks performed
1. Independent spot check: raw JSON cell index arithmetic for exports 1999 and 2025 equals the CSV (5,427,925,766 EUR; 46,811,880.88 x 100 kg in 2025).
2. WORLD = INT + EXT for all years/flows/indicators.
3. Chapter 72 total = sum of its 29 headings + 6 special codes (max gap 7e-9).
4. For 7204/7207/7208/7304/7306: heading total = sum of HS6 = sum of CN8 codes incl. special codes, every year/flow.
5. 7204 + 7207 + 7208 <= Chapter 72 total, every year/flow.
6. Workbook tables parsed from `sources/text/` (read-only) and compared programmatically; mismatches listed above.
7. Every response carried `updated = 2026-10-16T11:00:00+0200`; no `status` flags were returned (all values are unflagged in the JSON).

## Caveats
- One vintage only (16 Oct 2026). Eurostat revises monthly; 2025 (and possibly 2024) can still change. **Re-run `pull_comext.py` after the next Comext update and before the freeze**; the 2023 and 2025 differences above show the series does move.
- Nominal EUR; no deflation. Chapter 72 includes scrap (7204), pig iron, ferro-alloys, DRI (7203) and semi-finished products, excludes Chapter 73 products and ore: not the CBAM base, not verified carbon content. Whether CBAM covers each heading was not checked here.
- Direct trade only: it misses non-EU-origin steel cleared elsewhere in the EU first, and German re-exports and transit effects are not separated.
- A trade surplus here is not by itself a competitiveness verdict (imports collapsed faster than exports; export tonnes are at a 27-year low). It is also not national-accounts NX (goods and services).
- The 2023 and 2025 revision cause is unverified; the earlier vintage is not retrievable.
- Eurostat says data are considered final by October of the following reference year, so 2025 is only now reaching that point; whether the 16 Oct 2026 vintage is already the final one for 2025 is not verified, so treat 2025 as possibly still revisable.
- No monthly or 2026 data were pulled (annual dataset has no 2026 values).

## Files
CSV (all with headers, 1999-2025 unless noted): `ch72_extra_eu_exports_*`, `ch72_extra_eu_imports_*`, `ch72_extra_eu_balance_*`, `check_imports_vs_workbook_4_2`, `check_other_workbook_tables`, `ch72_trade_by_partner_group_long`, `ch72_materiality_shares_*`, `ch72_balance_by_partner_group_*`, `slide_table_2017_2025`, `byproduct_ext_eu_trade_long_*`, `byproduct_imports_wide_*`, `byproduct_exports_wide_*`, `coverage_by_series_*`, `ch72_headings_extra_eu_long_*`, `ch72_headings_reconciliation`, `ch72_headings_change_contributions_mass`, `subcodes_first_last_year`, `subcodes_consistency_by_year`.
Scripts: `pull_comext.py` (main pull and all tables), `pull_subcodes.py` (HS6/CN8 classification check), `pull_ch72_headings.py` (Chapter 72 decomposition). Run each with `python -I -X utf8 <script>`; `pull_subcodes.py` and `pull_ch72_headings.py` read the code subsets in `raw/`. `run_log.txt` is the log of the last `pull_comext.py` run.
