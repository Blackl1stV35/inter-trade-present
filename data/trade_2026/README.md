# data/trade_2026 — 2026 trade data vs the same months of 2025

Retrieved 2026-10-22 (02:33-02:45 UTC) from live primary sources. Scope: Germany, extra-EU27 (2020 composition) trade in iron and steel, Comext monthly, January 2025 to the latest month in 2026; plus, labelled separately, German crude steel output from the WV Stahl press releases. Nothing here is estimated or interpolated; missing observations would stay empty (none occurred in the pulled series).

## 1. Headline

- Latest month in Comext for Germany / extra-EU27: **August 2026** (all six monthly series have 2026-01 to 2026-08; 2026-09 onward returns no data).
- Dataset DS-045409 "last updated" stamp in the API: **2026-10-16T11:00:00+02:00** (same date as the Eurostat euro-indicator news release for August 2026).
- Next scheduled Eurostat release (September 2026 data plus revisions): **13 November 2026**, i.e. three days before the 16-18 November presentations (date from the euro-indicator page; the Comext detailed data are published on the release date per the metadata, section 14.1).
- Like-for-like **January-August 2026 vs January-August 2025, Chapter 72, extra-EU27** (provisional 2026):

| Flow | EUR m 2025 | EUR m 2026 | chg | kt 2025 | kt 2026 | chg | EUR/t 2025 | EUR/t 2026 | chg |
|---|---|---|---|---|---|---|---|---|---|
| Imports | 1,127.34 | 1,119.30 | -0.7% | 1,028.43 | 1,108.09 | +7.7% | 1,096 | 1,010 | -7.9% |
| Exports | 3,930.90 | 3,206.62 | -18.4% | 3,371.59 | 2,821.87 | -16.3% | 1,166 | 1,136 | -2.5% |
| Net (X - M) | 2,803.56 | 2,087.32 | -25.5% | 2,343.17 | 1,713.78 | -26.9% | | | |

Reading: in tonnes, direct extra-EU Chapter 72 imports are 7.7% higher than in the same eight months of 2025, so the 2021-2025 fall did not continue in the first eight months of 2026 (2025 was the lowest annual value in the 1999-2025 series, 1,463.59 kt). In euros imports are flat (-0.7%) because the unit value fell 7.9% (unit value is a product-mix indicator, not a price index). Exports to non-EU countries are down 16.3% in tonnes. These are descriptive comparisons of provisional data, not policy effects.

## 2. Exact queries (all HTTP 200)

Base: `https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409`

Common parameters: `format=JSON&lang=EN&reporter=DE&partner=EXT_EU27_2020&indicators=VALUE_IN_EUROS&indicators=QUANTITY_IN_100KG`

| Raw file in `raw/` | freq | product | flow | sinceTimePeriod |
|---|---|---|---|---|
| monthly_72_flow1_imports.json | M | 72 | 1 | 2025-01 |
| monthly_72_flow2_exports.json | M | 72 | 2 | 2025-01 |
| monthly_7208_flow1_imports.json | M | 7208 | 1 | 2025-01 |
| monthly_7208_flow2_exports.json | M | 7208 | 2 | 2025-01 |
| monthly_7204_flow1_imports.json | M | 7204 | 1 | 2025-01 |
| monthly_7204_flow2_exports.json | M | 7204 | 2 | 2025-01 |
| annual_72_flow1_imports.json, annual_72_flow2_exports.json | A | 72 | 1 / 2 | 2024 |
| annual_7208_flow1_imports.json, annual_7208_flow2_exports.json | A | 7208 | 1 / 2 | 2024 |
| vintagecheck_annual_72_flow1_imports_since1999.json | A | 72 | 1 | 1999 |

Full URLs, retrieval times, SHA-256 and the dataset `updated` stamp of every call are in `raw/manifest.json`. Example: `...DS-045409?format=JSON&lang=EN&freq=M&reporter=DE&partner=EXT_EU27_2020&product=72&flow=1&indicators=VALUE_IN_EUROS&indicators=QUANTITY_IN_100KG&sinceTimePeriod=2025-01`. An independent SDMX 2.1 call (`/sdmx/2.1/data/DS-045409/M.DE.EXT_EU27_2020.72.1.VALUE_IN_EUROS?startPeriod=2026-07&endPeriod=2026-08`, saved as `raw/sdmx21_crosscheck_72_imports_2026-07_08.xml`) returned the same July and August 2026 import values (137,379,306 and 108,029,822 EUR). The API returns no per-observation status flags, so provisional status cannot be read cell by cell.

Scripts (run with `python -I -X utf8`): `scripts/01_pull_comext.py`, `02_compute_ytd.py`, `03_vintage_check.py`, `04_wvstahl_crude_steel.py`, `05_eurostat_policy_excerpts.py`.

## 3. Units and conversions (same as the workbook)

Tonnes = QUANTITY_IN_100KG / 10; thousand tonnes (kt) = tonnes / 1,000; EUR million = EUR / 1e6; unit value EUR/t = EUR / tonnes (computed from the summed value and summed mass of the window, not as an average of monthly unit values). Percentage changes are 2026 over the same months of 2025. Values are nominal, not seasonally or calendar adjusted.

## 4. Other products (same window, January-August)

| CN | Flow | EUR m 2025 | EUR m 2026 | chg | kt 2025 | kt 2026 | chg | EUR/t 2025 | EUR/t 2026 | chg |
|---|---|---|---|---|---|---|---|---|---|---|
| 7208 hot-rolled flat | imports | 10.66 | 55.90 | +424.6% | 9.76 | 57.35 | +487.8% | 1,092 | 975 | -10.7% |
| 7208 | exports | 207.16 | 147.53 | -28.8% | 249.64 | 175.48 | -29.7% | 830 | 841 | +1.3% |
| 7204 ferrous scrap | imports | 118.87 | 141.98 | +19.4% | 251.65 | 293.69 | +16.7% | 472 | 483 | +2.3% |
| 7204 | exports | 314.92 | 358.75 | +13.9% | 830.14 | 886.40 | +6.8% | 379 | 405 | +6.7% |

7208 imports are a very small base: 9.8 kt in January-August 2025 against 57.4 kt in 2026, which already exceeds the whole of 2025 (32.72 kt, workbook Dataset D) and is close to 2024 (62.42 kt). The monthly pattern is lumpy (20.4 kt in February 2026, 0.9 kt in August 2026), so quote kilotonnes, not the +488% change.

## 5. Monthly tables

Chapter 72 imports (extra-EU27):

| Month | EUR m 2025 | EUR m 2026 | chg | kt 2025 | kt 2026 | chg | EUR/t 2025 | EUR/t 2026 |
|---|---|---|---|---|---|---|---|---|
| 01 | 161.26 | 166.82 | +3.4% | 122.30 | 180.89 | +47.9% | 1,319 | 922 |
| 02 | 113.90 | 133.80 | +17.5% | 94.04 | 139.72 | +48.6% | 1,211 | 958 |
| 03 | 120.00 | 115.66 | -3.6% | 103.41 | 122.43 | +18.4% | 1,160 | 945 |
| 04 | 167.13 | 200.65 | +20.1% | 137.28 | 180.67 | +31.6% | 1,217 | 1,111 |
| 05 | 149.19 | 105.18 | -29.5% | 157.89 | 88.90 | -43.7% | 945 | 1,183 |
| 06 | 121.50 | 151.78 | +24.9% | 129.12 | 164.58 | +27.5% | 941 | 922 |
| 07 | 193.48 | 137.38 | -29.0% | 182.98 | 106.22 | -42.0% | 1,057 | 1,293 |
| 08 | 100.88 | 108.03 | +7.1% | 101.40 | 124.68 | +23.0% | 995 | 866 |

Chapter 72 exports (extra-EU27):

| Month | EUR m 2025 | EUR m 2026 | chg | kt 2025 | kt 2026 | chg | EUR/t 2025 | EUR/t 2026 |
|---|---|---|---|---|---|---|---|---|
| 01 | 550.34 | 356.06 | -35.3% | 499.32 | 329.55 | -34.0% | 1,102 | 1,080 |
| 02 | 532.02 | 370.32 | -30.4% | 454.77 | 344.47 | -24.3% | 1,170 | 1,075 |
| 03 | 514.09 | 439.34 | -14.5% | 451.60 | 378.00 | -16.3% | 1,138 | 1,162 |
| 04 | 482.82 | 407.20 | -15.7% | 392.64 | 376.74 | -4.1% | 1,230 | 1,081 |
| 05 | 506.23 | 406.53 | -19.7% | 452.71 | 384.21 | -15.1% | 1,118 | 1,058 |
| 06 | 455.79 | 425.97 | -6.5% | 387.85 | 335.75 | -13.4% | 1,175 | 1,269 |
| 07 | 475.17 | 445.26 | -6.3% | 374.70 | 364.47 | -2.7% | 1,268 | 1,222 |
| 08 | 414.44 | 355.94 | -14.1% | 358.00 | 308.67 | -13.8% | 1,158 | 1,153 |

Full monthly levels for 2025-01 to 2026-08 (all products, both flows): `tables/monthly_series.csv`. Year-over-year table: `tables/monthly_yoy.csv`. Cumulative comparison for every cutoff month: `tables/ytd_by_cutoff.csv`. Monthly import tonnage swings by -44% to +49% against the same month of 2025, so single months should not be quoted; use the cumulative window.

Sub-windows (descriptive only; `tables/ytd_subwindows.csv`): Chapter 72 imports January-June 2026 are +17.9% in tonnes (877 vs 744 kt) and July-August 2026 are -18.8% (231 vs 284 kt). WV Stahl reports that the EU's new steel trade-defence instrument (country quotas with an out-of-quota duty, separate from CBAM) started on 1 July 2026, so July-August are its first two months; two noisy months cannot show an effect and this split must not be presented as one. Exports: January-June -18.6%, July-August -8.1% in tonnes.

## 6. Provisional status and revisions (what Eurostat says)

- Eurostat metadata for the dataset (ESMS ext_go_detail, sections 17.1-17.2, metadata page last updated 6 October 2025): previously published data are revised whenever revised national data arrive; revisions are routine and also unscheduled, driven mainly by late declarations (chiefly intra-EU) and by corrections of errors and omissions that can touch extra-EU data; monthly data are generally considered final in October of the year after the reference year; the month in which the final release happens varies by country (annual quality report). Revised monthly data feed the annual series automatically. Excerpt saved in `raw/eurostat_sims_ext_go_detail_excerpt.txt`.
- The euro-indicator release of 16 October 2026 states that its figures are provisional and are based on information received before 13 October 2026 (`raw/eurostat_euroindicator_2026-10-16_excerpt.txt`).
- Practical reading for the deck: January-August 2026 is provisional and will be restated in the 13 November 2026 update and later ones; 2025 monthly data are at or near the "final by October 2026" point (Eurostat does not flag it per observation, so say "2025: at or close to final", not "final").
- Evidence from the data itself (`tables/vintage_check_annual_72_imports.csv`): the 27 annual Chapter 72 import values 1999-2025 pulled now (update of 16 Oct 2026) match the workbook table (retrieved 10-11 Oct 2026 from the 15 Sep 2026 update) to within 0.01 for 26 of 27 years, including 2024 and 2025 (2005 mass differs by 0.01 kt, rounding). Only 2023 moved: EUR 2,106.93 m (workbook 2,107.38) and 2,088.77 kt (workbook 2,088.99), a revision of -0.02% and -0.01%; the rounded 2,089 kt used on the slides is unchanged. The 2025 monthly values sum exactly to the annual figures (`tables/annual_crosscheck_2025.csv`).
- Cautions from the same metadata: no data set of millions of records is perfectly accurate; confidential trade is hidden at detailed product level but kept in the chapter total, so very small CN lines (7208) are more exposed than Chapter 72.

## 7. WV Stahl crude steel (separate source: German Steel Federation, not Eurostat)

German crude steel is a production measure; do not combine it with the Comext flows.

| | kt | Source |
|---|---|---|
| Jan-Aug 2026 (preliminary) | 23,902 | WV Stahl press release 22 Sep 2026 |
| Jan-Aug 2025 (revised, sum of months) | 22,493 | WV Stahl revision table, August 2026 |
| Change | +6.3% (6.26% from our sum; WV Stahl also prints +6.3%) | |
| Latest month, August 2026 | 2,594 (+1.7% vs 2,550 in Aug 2025 revised) | |

Monthly 2026 (kt): Jan 3,083; Feb 2,833; Mar 3,345; Apr 3,233; May 3,202; Jun 2,934; Jul 2,679; Aug 2,594. Growth against the revised 2025 months is positive from January to June and turns negative in July (-1.8%), then +1.7% in August (`tables/wvstahl_crude_steel_jan_aug_like_for_like.csv`). Route split, January-August: oxygen steel (blast furnace / converter) 16,464 kt (+7.2%), electric steel 7,438 kt (+4.3%); the electric share is 31.1% in 2026 against 31.7% in the same months of 2025 (`tables/wvstahl_route_split_jan_aug.csv`). The route share counts tonnes, not emissions per tonne.

Revision: the first 2025 estimate (WV Stahl, 21 Jan 2026) was 34,090 kt (34.1 Mt, the figure the workbook uses); the August 2026 revision table gives **34,267 kt (34.3 Mt)**; the printed total is 34,267 and the months add to 34,268 (rounding). WV Stahl states that its monthly press-release figures are always preliminary and that the final status is fixed in the middle of the following year. 2026 press releases issued before 10 August appear to use the unrevised 2025 base (the half-year release of 21 July shows +8.9% for January-June; against the revised 2025 months it is +8.2%, 18,629 vs 17,215 kt); the releases of 9 and 22 September reproduce the revised base (+6.8% and +6.3%). The September 2026 figure was not yet published at retrieval (the newest crude-steel release on the press page is 22 Sep 2026); WV Stahl published the earlier months between the 9th and the 26th of the following month.

Destatis was checked only for context: its press release No. 356 of 8 October 2026 (German foreign trade, August 2026) carries all-goods totals, no iron and steel line, and says the first provisional figures would be updated on 20 October 2026. It is not used here.

## 8. Checks performed

1. Monthly sums of 2025 equal the separately pulled annual 2025 value and mass for 72 and 7208, imports and exports, to 4 decimals.
2. The annual 2025 and 2024 Chapter 72 and 7208 import values equal the workbook (Dataset C, Dataset D, section 4.2) to two decimals; only 2023 differs slightly (section 6).
3. Hand re-addition of the eight monthly values for imports (value and mass, both years) and 2026 export mass reproduced the script totals.
4. SDMX 2.1 cross-check of two monthly values (section 2).
5. No missing cells: each monthly series has 20 months x 2 indicators = 40 values; the API lists 2026-09 to 2026-12 as positions with no data, so no later month is used.
6. WV Stahl: the monthly values reproduce the printed cumulative totals (for example 12,493 + 3,202 = 15,695 for January-May; the August cumulative is 23,902 against 23,903 from rounded months); the revised-2025 table parsed with a table extractor (a plain text extraction misaligns the January row).

## 9. Caveats

- Provisional 2026 data; the 13 November 2026 release will restate January-August and add September. Re-run `scripts/01_pull_comext.py` and `02_compute_ytd.py` after it (the 2026 window is detected automatically as the months present in all six series).
- Scope: direct extra-EU27 trade of Germany (partner EXT_EU27_2020, a fixed composition). Chapter 72 includes scrap and omits Chapter 73 products and ore; it is not the CBAM base and not national-accounts NX. Steel first cleared in another EU state and then moved to Germany is not counted as an import. Exports to non-EU countries are not the same universe as the all-partner "steel mill products" in Dataset B (WV Stahl); do not subtract one from the other. For scale: 2024 Chapter 72 extra-EU exports were 5,048.33 kt against 22.9 Mt of all-partner steel-mill exports (about 22%), and imports 1,954.63 kt against 18.8 Mt (about 10%).
- Data are not seasonally or calendar adjusted; a same-months comparison removes most of the seasonality. Value is nominal euros.
- Unit values mix products and are not a price index.
- No causal reading: the window mixes the definitive CBAM period (from 1 January 2026), the new steel trade-defence instrument (from 1 July 2026, per WV Stahl), the weak domestic steel demand WV Stahl describes, and energy and macro effects. No CBAM certificate has been paid in the window (certificate sales start 1 February 2027 per the workbook, U35).
- Eurostat's metadata page was last updated 6 October 2025, a year before retrieval; the revision policy text is the latest Eurostat statement found, not verified against a 2026 quality report.
- Not read in full, noted only as a pointer: WV Stahl press releases of 13 October 2026 (worldsteel outlook, German demand lagging) and 16 October 2026 (automotive-package steel credit versus the German-French proposal for an electric-vehicle super-credit), listed on the WV Stahl press page.
