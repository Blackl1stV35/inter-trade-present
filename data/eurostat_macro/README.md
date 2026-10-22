# data/eurostat_macro: provisional-GVA flag check, EU27 comparator, sub-industry jobs, 2025 macro vintage

Retrieved 2026-10-22 (first API call 02:32:37 UTC, last 02:42 UTC; folder written the same day). Scope: Germany (DE), NACE Rev. 2 Section C manufacturing, plus the 2025 national-accounts growth context used on slide S10. Everything here was pulled live; nothing is recalled from memory, estimated or interpolated. Missing observations are left missing.

## 1. Short answers

1. Revisions versus the workbook table (update tab 4.1): none. All 93 values (31 years x real GVA index, production index, GVA share) match the workbook exactly. The three employment values in [U28] (7,490 / 7,415 / 7,262 thousand, 2023-25) also match. The datasets were refreshed after the workbook pull (nama_10_a64 on 21 Oct 2026 11:00 CEST, nama_10_a64_e on 21 Oct 23:00, sts_inpr_a on 15 Oct 11:00; the workbook cites 9 and 10 Oct) but those cells did not move. File: `tidy/revision_check_vs_workbook.csv`.
2. Provisional flag today (flag code `p`): real GVA index (CLV_I20), GVA share (PC_TOT) and employment Section C all carry `p` for 2023, 2024 and 2025. The production index (sts_inpr_a, 1995-2025) carries no flag at all. The 19.4% (2025) and 19.9% (2024) shares and the 104.13 (2025) index are unchanged and still provisional; 2024 is provisional too, not only 2025. File: `tidy/provisional_flag_audit.csv`.
3. EU27_2020 manufacturing share of total GVA (PC_TOT): 15.9% for 2024 (no flag; recomputed 15.93% from CP_MEUR). 2025 is not available: Eurostat publishes no EU27_2020 aggregate for 2025 yet because Bulgaria and Latvia have no 2025 value (25 of 27 members have). Germany sub-industry employment is available only to 2024 (flag `p` for 2023-24); the 2025 detail is not published.
4. Macro context (slide S10): the workbook's Dataset F (15 Jan 2026 first estimate) is superseded. Current vintage (Eurostat nama_10_gdp 21 Oct 2026, matching Destatis after its summer revision of 25 Aug 2026), 2025 real growth: GDP 0.2 (unchanged), household and NPISH consumption 1.3 (was 1.4), government consumption 1.7 (was 1.5), gross fixed capital formation -0.6 (was -0.5), exports -0.9 (was -0.3), imports 2.9 (was 3.6). Net exports contribute -1.5 percentage points to 2025 GDP growth in both vintages. All 2023-25 values are flagged `p`.

## 2. Files

- `raw/` responses relied on (JSON-stat and SDMX-CSV from Eurostat, saved Destatis HTML pages, Eurostat catalogue extract).
- `tidy/` header-bearing CSV tables derived from raw/ (value plus flag columns).
- `scripts/` Python used for parsing and checks. Run as `python -I -X utf8 scripts/<name>.py <args>` (arguments are in each script's docstring).
- `retrieval_utc.txt` first-call timestamp.

Key tables in `tidy/`:
- `de_manufacturing_1995_2025_live.csv` live values and flags for the three core series, one row per year.
- `workbook_table_4_1.csv` the workbook table parsed from `sources/text/inter-trade-present-2-revised-research-brief.txt` (lines 50-81).
- `revision_check_vs_workbook.csv` year, series, workbook value, live value, difference, flag, status.
- `provisional_flag_audit.csv` first and last period, flagged periods and codes for 103 series.
- `eu27_vs_de_mfg_share.csv` DE and EU27_2020 share 1995-2025, plus recomputed C/TOTAL from current-price levels for 2015 onward.
- `emp_sub_industries_2015_2025.csv`, `emp_sub_industries_changes.csv` employment (thousand persons) for TOTAL, B-E, C, C24, C24_C25, C25, C26, C27, C28, C29, C29_C30, C30 and the EMP_DC, SAL_DC, SELF_DC concepts; `emp_de_subind_tidy.csv` has the same from 1995.
- `datasetF_vs_current_vintage.csv` workbook Dataset F against the live Eurostat values.
- `destatis_summer_revision_2026_old_vs_new.csv` Destatis old (May 2026) and new (Aug 2026) real growth, 2022-2025; `destatis_use_of_gdp_2023_2025.csv` nominal and chain-index use of GDP (Stand 25 Aug 2026).
- `nama_10_gdp_DE_tidy.csv` (annual, three units), `namq_10_gdp_DE_tidy.csv` (quarterly 2025-Q1 to 2026-Q2), `nama_10_gdp_pct_from_levels_check.csv`.

## 3. Exact queries

Base URL for JSON-stat: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<dataset>?format=JSON&lang=EN&<filters>`. SDMX-CSV base: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/<dataset>/<key>?startPeriod=1995&format=SDMX-CSV`. Status flags appear in the JSON-stat `status` object and in the SDMX-CSV `OBS_FLAG` column; the update stamp is `updated` / `extension.annotation[UPDATE_DATA]` and the SDMX-CSV `LAST UPDATE` column.

Core series (workbook replication, sinceTimePeriod=1995):
- `nama_10_a64?freq=A&geo=DE&nace_r2=C&na_item=B1G&unit=CLV_I20&sinceTimePeriod=1995`
- `nama_10_a64?freq=A&geo=DE&nace_r2=C&na_item=B1G&unit=PC_TOT&sinceTimePeriod=1995`
- `sts_inpr_a?freq=A&indic_bt=PRD&nace_r2=C&s_adj=NSA&unit=I21&geo=DE&sinceTimePeriod=1995`
- `nama_10_a64_e?freq=A&geo=DE&nace_r2=C&na_item=EMP_DC&unit=THS_PER&sinceTimePeriod=1995`
- Cross-check via SDMX-CSV keys: `nama_10_a64/A.CLV_I20.C.B1G.DE`, `nama_10_a64/A.PC_TOT.C.B1G.DE`, `sts_inpr_a/A.PRD.C.NSA.I21.DE`, `nama_10_a64_e/A.THS_PER.C.EMP_DC.DE`.

Comparator and employment:
- `nama_10_a64?freq=A&geo=EU27_2020&geo=DE&nace_r2=C&na_item=B1G&unit=PC_TOT&sinceTimePeriod=1995`
- `nama_10_a64?freq=A&geo=EU27_2020&geo=DE&nace_r2=C&nace_r2=TOTAL&na_item=B1G&unit=CP_MEUR&sinceTimePeriod=2015`
- `nama_10_a64?freq=A&geo=EU27_2020&nace_r2=C&na_item=B1G&unit=CLV_I20&sinceTimePeriod=1995`
- `nama_10_a64?freq=A&nace_r2=C&na_item=B1G&unit=PC_TOT&time=2024&time=2025` (all geos, to count member states with a 2025 value)
- `nama_10_a64_e?freq=A&geo=DE&unit=THS_PER&na_item=EMP_DC&na_item=SAL_DC&na_item=SELF_DC&nace_r2=TOTAL&nace_r2=B-E&nace_r2=C&nace_r2=C24_C25&nace_r2=C24&nace_r2=C25&nace_r2=C26&nace_r2=C27&nace_r2=C28&nace_r2=C29_C30&nace_r2=C29&nace_r2=C30&sinceTimePeriod=1995`

National accounts (items B1GQ, P3, P3_S13, P31_S14, P31_S14_S15, P51G, P5G, P6, P61, P62, P7, P71, P72, P6X7; geo=DE; sinceTimePeriod=2015):
- `nama_10_gdp?freq=A&unit=CLV_PCH_PRE`, `...&unit=CLV20_MEUR`, `...&unit=CP_MEUR`
- `namq_10_gdp?freq=Q&geo=DE&s_adj=SCA&unit=CLV_PCH_PRE&unit=CLV_PCH_SM&sinceTimePeriod=2025-Q1` and `s_adj=NSA&unit=CLV_PCH_SM` (items B1GQ, P31_S14_S15, P3_S13, P51G, P6, P7)
- Catalogue: `https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en` (relevant rows saved in `raw/eurostat_toc_extract_2026-10-22.txt`: nama_10_a64 and nama_10_a64_e last data update 21.10.2026, sts_inpr_a 15.10.2026, nama_10_gdp 21.10.2026, namq_10_gdp 20.10.2026; data end 2025 for the annual tables, 2026-Q2 for namq_10_gdp).

Destatis pages saved (read as HTML, then parsed by `scripts/destatis_extract.py`):
- `https://www.destatis.de/DE/Themen/Wirtschaft/Volkswirtschaftliche-Gesamtrechnungen-Inlandsprodukt/sommerueberarbeitung-2026.html` (published 25.08.2026, updated 30.09.2026)
- `https://www.destatis.de/DE/Themen/Wirtschaft/Volkswirtschaftliche-Gesamtrechnungen-Inlandsprodukt/Tabellen/inlandsprodukt-verwendung-bip.html` (Stand 25. August 2026)
- `https://www.destatis.de/EN/Press/2026/01/PE26_017_811.html` (press release 017 of 15 Jan 2026, the source of Dataset F)
- `https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/08/PD26_303_811.html` (Q2 2026 detail, correction of 30 Sep 2026)
- `https://www.destatis.de/DE/Themen/Wirtschaft/Volkswirtschaftliche-Gesamtrechnungen-Inlandsprodukt/_inhalt.html` (publication list and revision-policy text)

## 4. Units and conversions

- Real GVA: chain-linked volume index, 2020 = 100. Production: annual unadjusted index, 2021 = 100. GVA share: percent of total GVA at current prices (PC_TOT), not of GDP.
- Employment: thousand persons, domestic concept, national accounts (EMP_DC total; SAL_DC employees; SELF_DC self-employed).
- National accounts growth: CLV_PCH_PRE = percentage change on previous period (annual: year on year), chain-linked volumes, one decimal as published. Levels: CLV20_MEUR (chain-linked 2020 prices, EUR million) and CP_MEUR (current prices, EUR million). Destatis tables are in EUR billion, chain index 2020 = 100.
- No trade-unit conversion was needed in this folder (the 100 kg to thousand tonnes rule applies to the Comext folders).

## 5. Findings in detail

### 5.1 Workbook table versus live (task items 1 and 2)

- Dataset stamps: nama_10_a64 21 Oct 2026 11:00 (+0200); sts_inpr_a 15 Oct 2026 11:00; nama_10_a64_e 21 Oct 2026 23:00; nama_10_gdp 21 Oct 2026 23:00; namq_10_gdp 20 Oct 2026 23:00. JSON-stat and SDMX-CSV agree on every value and every flag for the four core series (`scripts/crosscheck_sdmx.py`: 0 value mismatches, 0 flag mismatches).
- Flags seen anywhere in the pulled series are only `p` (provisional). No `e`, `b` or other codes appear.
- Flagged `p`: nama_10_a64 DE Section C, B1G in CLV_I20, PC_TOT and CP_MEUR (also TOTAL): 2023, 2024, 2025. nama_10_a64_e DE: Section C, B-E and TOTAL 2023-2025; the C24-C30 detail 2023-2024 (2025 missing). nama_10_gdp DE: all items 2023-2025. namq_10_gdp DE: every quarter 2025-Q1 to 2026-Q2. Not flagged: sts_inpr_a (all years), EU27_2020 PC_TOT 2023-2024.
- Selected current values (2025): real GVA 104.13 (2020 = 100), share 19.4% (recomputed 19.42%, i.e. C 797,190 over total 4,104,359 EUR million), production 92.8 (2021 = 100), employment Section C 7,262 thousand. Implied year-on-year changes: real GVA -3.07% (2023), -1.58% (2024), -1.43% (2025); production -1.2% (2023), -4.9% (2024), -1.1% (2025); Section C employment +0.05%, -1.0%, -2.1%.
- Why 2025 stays provisional (Destatis, summer revision article): the 2026 summer revision integrated structural statistics up to 2024; for the latest year (2025) such results do not exist yet. Destatis also states that German national accounts count as "final" only after about four years. The publication list names the August 2026 spreadsheet for 2025 "endgueltige Ergebnisse", which sits oddly with that statement; Eurostat's flag is the operative signal and it says provisional. Inference, not a stated date: the next regular structural benchmark of 2025 is the August 2027 summer revision.
- The workbook table (pulled 11 Oct 2026) already follows Destatis' 25 Aug 2026 summer revision. That revision raised manufacturing value added for 2024 and switched the main extrapolation indicator for manufacturing from the production index to the price-adjusted turnover index. Hence real GVA (turnover-based) and the production index (physical output) diverge in 2024 (-1.6% against -4.9%). The 15 Jan 2026 first estimate had shown manufacturing real GVA at -4.3% (2024) and -1.3% (2025), so any figure copied from January sources is stale.

### 5.2 EU27 comparator (task item 3)

- PC_TOT manufacturing share of total GVA, EU27_2020: 16.5% (2023), 15.9% (2024), no 2025. Germany: 20.4% p, 19.9% p, 19.4% p. Recomputed from current-price levels: EU27 2024 2,581,075.5 over 16,198,877.6 = 15.93%.
- No EU27 2025 aggregate exists because 25 of 27 members report 2025 (missing: BG, LV). The Eurostat metadata (page last updated 28 Jan 2025) says Eurostat may use unpublished estimates to impute missing country data for aggregates; no such figure is released here, so none is used.

### 5.3 Jobs by sub-industry (Member D's request)

Germany, EMP_DC, thousand persons, domestic concept (`tidy/emp_sub_industries_2015_2025.csv`). 2015, 2019, 2022 and the latest value:

| NACE | 2015 | 2019 | 2022 | latest | change 2015 to latest | change 2019 to latest |
| --- | --- | --- | --- | --- | --- | --- |
| C Manufacturing | 7,512 | 7,773 | 7,486 | 7,262 (2025 p) | -250 (-3.3%) | -511 (-6.6%) |
| C24 Basic metals | 268 | 271 | 249 | 245 (2024 p) | -23 (-8.6%) | -26 (-9.6%) |
| C25 Fabricated metal products | 905 | 937 | 873 | 844 (2024 p) | -61 (-6.7%) | -93 (-9.9%) |
| C28 Machinery and equipment | 1,135 | 1,210 | 1,146 | 1,164 (2024 p) | +29 (+2.6%) | -46 (-3.8%) |
| C29 Motor vehicles, trailers | 872 | 916 | 858 | 858 (2024 p) | -14 (-1.6%) | -58 (-6.3%) |
| TOTAL economy | 43,137 | 45,291 | 45,622 | 45,878 (2025 p) | +2,741 (+6.4%) | +587 (+1.3%) |

Shares of Section C in 2024: C24 3.3%, C28 15.7%, C29 11.6%. Section C is 7,262 thousand in 2025 and 7,415 thousand in 2024. C26, C27, C30 and the SAL_DC and SELF_DC splits are in the CSV. Employment concept is national-accounts persons including self-employed; it is not the structural-business-statistics figure of [U27].

### 5.4 2025 national-accounts growth (task item 4)

Real growth 2025, percent (`tidy/datasetF_vs_current_vintage.csv`, `tidy/destatis_summer_revision_2026_old_vs_new.csv`):

| Item | Dataset F (15 Jan 2026) | May 2026 vintage (Destatis "old") | Current (Aug 2026 revision; Eurostat 21 Oct 2026) |
| --- | --- | --- | --- |
| GDP | 0.2 | 0.2 | 0.2 |
| Household and NPISH consumption | 1.4 | 1.3 | 1.3 (households only P31_S14: 1.4) |
| Government consumption | 1.5 | 1.5 | 1.7 |
| Gross fixed capital formation | -0.5 | -0.2 | -0.6 |
| Exports of goods and services | -0.3 | not published by Destatis | -0.9 (Eurostat; -0.95 from the rounded Destatis index) |
| Imports of goods and services | 3.6 | not published by Destatis | 2.9 |
| Net exports, contribution to GDP growth (pp) | -1.5 | -1.5 | -1.5 |

- Destatis revised 2024 much more than 2025: GDP 2024 from -0.5 to 0.0, government consumption 2.6 to 3.9, GFCF -3.3 to -2.1, private consumption 0.5 to 1.4. 2023 GDP -0.9 to -1.0. Dataset F's 2025 row therefore differs in five of six cells.
- Definition: the January table row "household consumption" is "households and NPISH" (Destatis "Privater Konsum"); the like-for-like current value is 1.3, not the households-only 1.4.
- Nominal use of GDP 2025 (Destatis, EUR billion, Stand 25 Aug 2026): GDP 4,529.710; private consumption 2,449.116; government consumption 1,012.805; gross fixed capital formation 915.092; inventories and valuables 52.376; exports 1,815.983; imports 1,715.662; net exports 100.321 (2024: 156.738). The five components add to GDP exactly. Shares of GDP: C 54.1%, G 22.4%, GFCF 20.2%, NX 2.2% (2024 NX share 3.6%).
- Quarterly context (namq_10_gdp, not seasonally adjusted, year on year): GDP +0.8% (2026-Q1) and +1.0% (2026-Q2); exports +0.5% and +3.7%; imports +1.6% and +2.5%. These match the Destatis release of 25 Aug 2026. They are 2026 observations and must not be read as a CBAM effect (definitive regime began 1 Jan 2026, first payments 2027).

## 6. Checks performed

- JSON-stat against SDMX-CSV, all values and flags, four core series: identical.
- Workbook table parsed from the source text and compared cell by cell: 93 of 93 unchanged, 3 of 3 employment values unchanged.
- CLV_PCH_PRE recomputed from CLV20_MEUR levels for 12 items, 2016-2025: maximum difference 0.05 percentage points (rounding).
- Approximate net-export contribution from chain-linked levels: -1.47 pp, consistent with Destatis -1.5.
- Eurostat total GVA 2025 (4,104,359 EUR million) equals Destatis total GVA (4,104.359 EUR billion).
- Destatis table values for 2025 (index changes) equal the Eurostat percentages after rounding for GDP, consumption, government, GFCF and imports; exports -0.95 against -0.9 is a rounding effect of the published two-decimal index.
- Destatis January table, summer-revision tables and use-of-GDP table were parsed from the saved HTML by script, not read from a summary.
- Accounting identity C + G + GFCF + inventories + NX = GDP holds exactly in the nominal 2025 data.

## 7. Caveats

- All 2023-2025 German values are provisional and can still change; Eurostat tables update whenever Germany transmits. Re-pull around 10-14 November, before the freeze. Destatis' own page gives t+30 for the first quarterly GDP estimate, so a Q3 2026 flash is likely at the end of October (date not confirmed); the detailed Q3 results (t+55) should fall after the 16-18 Nov talks.
- The EU27 2025 comparator does not exist yet; the like-for-like comparison stays at 2024, where the German numerator is itself provisional and the EU27 figure includes it.
- C24 "basic metals" includes non-ferrous metals and metal casting; it is not a steel-only job count. Sub-industry detail ends in 2024.
- Manufacturing real GVA and the production index are not the same indicator (see 5.1); the two S6 panels can diverge for methodological reasons as well as economic ones.
- The Destatis exports and imports growth rates are not printed in the revision article (it says only that they were revised moderately); the Eurostat values were checked against the Destatis chain index instead.
- The Eurostat metadata page consulted was last updated 28 Jan 2025; it was used only for the general revision policy.
- These are descriptive statistics, not estimates of an ETS or CBAM effect.
