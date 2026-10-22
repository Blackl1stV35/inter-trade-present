# Tax variable (CH2) - German ETS auction receipts, CBAM revenue rules, tax context

Prepared 2026-10-22 for the Germany / EU ETS + CBAM / iron and steel presentation. All figures were taken from documents opened on 2026-10-22 and saved in `raw/`. Nothing was estimated or recalled from memory. Where a figure could not be verified it is marked as such below.

Short answer for the slide:

- German EU-ETS 1 auction receipts were **EUR 5.43 bn in 2025** (EUR 5.53 bn in 2024, peak EUR 7.66 bn in 2023). By law they go to the Klima- und Transformationsfonds (KTF); the 2027 government draft would divert EUR 2.7 bn of them to the core budget (not yet enacted).
- **CBAM receipts are not German tax revenue.** They are the sale price of certificates, sold by the Member State to declarants established there, from 1 February 2027. Under current law they are not an EU own resource (a 75% EU share is only proposed, from 2028). The German draft budget 2027 books EUR 377.7 million of CBAM receipts in the core budget (not in the tax chapter, not in the KTF).
- Corporate-tax, payroll-tax and consumption-tax effects of ETS or CBAM **cannot be measured** with these sources.

## Folder contents

| Path | What it is |
| --- | --- |
| `raw/` | Documents and API responses relied on (see "Retrieval log"). Large files were not kept: the 275 MB budget PDF (BT-Drs. 21/7300) is replaced by page images and a text extract; its SHA-256 is in `tables/source_register.csv`. |
| `scripts/` | `build_ets_revenue_tables.py`, `build_tax_context_tables.py`, `build_static_tables.py`, `probe_eurostat_availability.py` (run with `python -I -X utf8`). The first two regenerate their tables from `raw/`; `build_static_tables.py` holds hand-copied document values (each row names its source file). |
| `tables/ets1_auction_revenue_de_by_year.csv` | German EU-ETS 1 auction receipts by year 2012-2025 (EUA, EUAA aviation, total, volume, average price, flags). |
| `tables/ets1_auction_level_de_2012_2025.csv` | 659 German auctions with price, volume, revenue and whether the revenue cell was reported or derived. |
| `tables/budget_lines_ktf_and_core_2025_2027.csv` | KTF revenue lines and the core-budget CBAM and ETS lines (thousand EUR, as printed). |
| `tables/cbam_revenue_rules.csv` | CBAM revenue rules with legal basis, status on 2026-10-22 and the file where each was read. |
| `tables/de_tax_context_eurostat_1995_2025.csv`, `..._long.csv` | Eurostat context series for Germany (EUR million) with status flags. |
| `tables/ets1_share_of_tax_context.csv` | ETS 1 receipts as a share of tax aggregates and GDP (context only). |
| `tables/tax_channels_measurability.csv` | Which tax channels can and cannot be measured. |
| `tables/crosschecks.csv`, `tables/d29f_vs_ets1_lag_check.csv`, `tables/source_register.csv` | Checks and the source list. |

## 1. German EU-ETS 1 auction receipts by year

**Table consulted.** The DEHSt page that carries the annual "Versteigerung" table (`https://www.dehst.de/DE/Themen/EU-ETS-1/EU-ETS-1-Informationen/Versteigerung/versteigerung_node.html`) and its annual reports could not be opened: on 2026-10-22 every dehst.de URL returned an HTTP 200 "Maintenance Page" of 188 bytes (retried several times between about 09:33 and 10:05; the Wayback Machine was also offline). I therefore did **not** see DEHSt's own table. The series below is rebuilt from the source DEHSt itself cites ("Quelle: EEX, DEHSt"): the European Energy Exchange's annual auction files for 2012-2025 (`raw/eex_emission_spot_primary_market_auction_report_2012-2025_data.zip`), keeping the German auctions (Country = DE; 2016 file: Auction Name = DE). Year coverage 2012-2025, calendar years, auction-date basis.

Unit EUR million, EUA = ordinary allowances, EUAA = aviation allowances (separate German auction in the file only in the years shown). Total = EUA + EUAA, which is the basis of UBA's headline "Erlöse EU-ETS 1".

| Year | EUA auctions (EUR m) | EUAA aviation (EUR m) | Total (EUR m) | Volume (m allowances) | Avg price (EUR/t) | Share of GDP (%) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2012 * | 286.3 | 17.5 | **303.8** | 42.10 | 7.22 | 0.011 |
| 2013 | 791.3 | none in file | **791.3** | 182.56 | 4.33 | 0.028 |
| 2014 | 750.0 | none in file | **750.0** | 127.13 | 5.90 | 0.025 |
| 2015 | 1,093.3 | 16.9 | **1,110.2** | 146.12 | 7.60 | 0.036 |
| 2016 | 845.7 | 4.6 | **850.4** | 161.63 | 5.26 | 0.027 |
| 2017 | 1,141.7 | 5.1 | **1,146.8** | 197.50 | 5.81 | 0.034 |
| 2018 | 2,565.3 | 16.3 | **2,581.7** | 173.02 | 14.92 | 0.075 |
| 2019 | 3,146.1 | 17.9 | **3,164.0** | 128.36 | 24.65 | 0.089 |
| 2020 | 2,641.8 | 20.6 | **2,662.4** | 108.20 | 24.61 | 0.077 |
| 2021 | 5,270.9 | 35.2 | **5,306.2** | 101.06 | 52.50 | 0.143 |
| 2022 | 6,772.4 | 40.2 | **6,812.6** | 84.82 | 80.32 | 0.170 |
| 2023 | 7,582.5 | 74.1 | **7,656.6** | 91.52 | 83.66 | 0.180 |
| 2024 | 5,460.7 | 68.1 | **5,528.7** | 85.05 | 65.00 | 0.126 |
| 2025 | 5,429.0 | none in file | **5,429.0** | 73.50 | 73.86 | 0.120 |

\* 2012: the EEX file leaves the revenue cell empty for 22 of the 55 German auctions (weekly phase-2 auctions of 300,000 allowances, 3 Jan - 5 Jun 2012). They are derived as price x volume (EUR 47.2 m). The identity price x volume = reported revenue holds exactly (maximum difference EUR 0.00) on all 637 auctions that do have a revenue cell, so the derivation is exact in rule but it is still derived. Reported cells only: EUR 256.6 m. The 2012 figure is the least certain number in the series (medium confidence) and no published 2012 total was available to compare.

Aviation (EUAA) share is below 1.3% of the total in every year except 2012 (5.8%) and 2015 (1.5%); 2024 is 1.2%. "None in file" means no separate German EUAA auction appears in the EEX file, not that revenue was observed as zero. In 2025 all German auctions carry contract T3PA (EUA); UBA says EU-ETS 1 also covers intra-European aviation and shipping, so aviation receipts after 2024 cannot be separated here.

Cumulative 2012-2025: EUR 44.1 bn. Auction receipts are not split by paying sector, so nothing in this series can be attributed to steel. Steel installations also receive free allocation, which produces no auction receipt.

## 2. Where the money goes

- **By law, to the KTF.** KTFG section 4(1) no. 1 (law filed as EKFG on gesetze-im-internet.de): the fund receives auction receipts "soweit diese Einnahmen nicht zur Finanzierung der Deutschen Emissionshandelsstelle benötigt werden". DEHSt's Q3-2023 report: auction receipts have flowed fully into the climate fund since 2012 (until July 2022 under its former name Energie- und Klimafonds, EKF). UBA press release 7 Jan 2026: the 2025 receipts of EUR 21.4 bn (ETS 1 about EUR 5.4 bn plus national fuel ETS about EUR 16 bn) "fliessen vollstaendig" into the KTF.
- **Booked in the KTF 2025 (BT-Drs. 21/7300, KTF Wirtschaftsplan, Tit. 132 02):** Ist 2025 EUR 5,403.354 m for ETS 1 auctions, Soll 2026 EUR 4,265.0 m, Soll 2027 EUR 2,509.790 m; fuel ETS (Tit. 132 03) Ist 2025 EUR 15,987.887 m. The KTF's total receipts are EUR 37,416.5 m (Ist 2025) and EUR 38,938.0 m (Soll 2027).
- **2027 change (government draft, not law).** The Haushaltsbegleitgesetz 2027 (BT-Drs. 21/7860, 7 Sep 2026, Art. 6) amends KTFG section 4(1) no. 1 so that auction receipts reach the KTF only above the amount budgeted in the federal budget. The draft budget books EUR 2,700 m of ETS 1 receipts in the core budget in 2027 (Kap. 6002 Tit. 132 03); with the KTF's EUR 2,509.8 m this implies EUR 5.21 bn ETS 1 receipts expected for 2027 (derived sum). The Bundesrat (25 Sep 2026) calls it "Zweckentfremdung" and says over EUR 13 bn is planned through 2030; the government rejected the objection on 14 Oct 2026 (BT-Drs. 21/8534). Timetable (Bundestag, retrieved 22 Oct): committee final session (Bereinigungssitzung) 12 Nov, final vote 27 Nov 2026 - after the 16 and 18 Nov presentation days. Re-check before presenting.
- **What the KTF money funds (2027 draft Soll, EUR million):** industry decarbonisation 664.2; hydrogen in industrial production 1,619.5; carbon contracts for difference 100.0 (commitment authorisation 8.73 bn to 2048, per the Bundestag service); compensation for electricity-intensive firms for ETS-related power price increases 5,000 (Soll 2026 4,000; Ist 2025 2,785.6). These are plans, not delivered tonnes or payments.

## 3. CBAM revenue rules (status 2026-10-22)

Full table with legal basis: `tables/cbam_revenue_rules.csv`.

- **First date revenue can arise: 1 February 2027.** Regulation (EU) 2025/2083 (OJ 17.10.2025), Art. 1(16)(a) and 1(27): "From 1 February 2027, a Member State shall sell CBAM certificates on a common central platform to authorised CBAM declarants established in that Member State." The workbook date is confirmed. First surrender is 30 September 2027 for 2026 imports. No receipt exists in 2026.
- **Who keeps the revenue.** The Member State that sells to declarants established on its territory. Regulation (EU) 2023/956 has no article assigning certificate revenue to the Union or earmarking its use (full-text search; recital 64 makes Member States responsible for "correctly establishing and collecting revenues"; recital 74 only says the Union is working towards a CBAM own resource). Germany's receipts therefore depend on German-established declarants, not on German customs entries or German steel use.
- **Own-resource status.** Not an EU own resource today. The Commission proposed (COM(2025) 574, 16 Jul 2025, Art. 3(1)(h)) a uniform call rate of 75% of CBAM certificate revenue for the EU budget, applying from [1 January 2028]; the Commission expects about EUR 1.4 bn a year on average in 2028-2034 (EUR 1.5 bn current prices, ECA Opinion 04/2026). The Council Negotiating Box of 10 Oct 2026 (13922/26) puts the call rate at [90]% in square brackets (open); the Presidency note of 4 Sep 2026 calls CBAM the most consensual of the new own resources. Adoption needs unanimity, Parliament's consultation and ratification by all Member States; I found no agreement. Parliament's interim report (28 Apr 2026, 370-201-84) backs the basket approach (read via WebFetch of the press release, not saved: medium confidence). The October 2026 European Council outcome was not available on 22 Oct.
- **Platform fees are a different flow:** fees paid by declarants for the central platform are Union internal assigned revenue (Art. 20(5a)), not national receipts.
- **Germany.** The government draft budget 2027 (BT-Drs. 21/7300, Einzelplan 60, Kap. 6002, Tit. 132 02, managed by BMUKN) shows CBAM receipts of **EUR 377.736 m** for 2027 and no entry for 2026 or 2025. The Bundesrat statement rounds this to "400 Millionen" and says it is the first time such receipts go to the core budget. KTFG section 4 lists no CBAM revenue and the KTF plan has no CBAM line. The figure is a budget estimate for all CBAM goods (steel, aluminium, cement, fertilisers, hydrogen, electricity), not a steel number; the method behind it is not stated on the pages read.
- **Is it German tax revenue? No.** It is a non-tax receipt (sale of certificates), not a tax or customs duty on the euro value of steel, and the draft budget books it outside the tax chapter (Kap. 6001 "Steuern"). I found no Eurostat or Destatis guidance on how national accounts classify CBAM receipts; that point is left open. It is also not government consumption (G) by itself.

## 4. Context series for the tax row (context only)

Source and units: Eurostat API, EUR million; `tables/de_tax_context_eurostat_1995_2025.csv`.

| Series (Germany) | 2022 | 2023 | 2024 | 2025 |
| --- | ---: | ---: | ---: | ---: |
| Taxes D2+D5+D91, general government (S13), gov_10a_taxag | 974,600 p | 971,326 p | 1,006,603 p | not available |
| Taxes and social contributions incl. imputed, S13+S212 (the denominator Eurostat uses for env_ac_tax) | 1,651,943 | 1,690,430 | 1,768,737 | not available |
| Environmental taxes, total (env_ac_tax ENV) | 73,177 | 70,791 | 75,794 | not available |
| of which energy / transport | 62,510 / 10,667 | 59,767 / 11,024 | 64,249 / 11,545 | |
| Environmental taxes, % of GDP / % of taxes and social contributions | 1.83 / 4.43 | 1.68 / 4.19 | 1.75 / 4.29 | |
| GDP, current prices (nama_10_gdp) | 4,010,630 | 4,254,930 p | 4,386,940 p | 4,529,710 p |
| ETS 1 auction receipts (section 1) | 6,812.6 | 7,656.6 | 5,528.7 | 5,429.0 |
| ETS 1 as % of taxes D2+D5+D91 | 0.70 | 0.79 | 0.55 | n/a |
| ETS 1 as % of Eurostat environmental taxes | 9.3 | 10.8 | 7.3 | n/a |
| ETS 1 as % of GDP | 0.170 | 0.180 | 0.126 | 0.120 |

p = Eurostat provisional flag. The gov_10a_taxag tax aggregates for 2025 are empty in the 2026-10-21 vintage and env_ac_tax ends in 2024 (vintage of 2026-02-10); they are left blank, not zero.

Definition warnings:

- Two environmental-tax totals exist. Eurostat (ESA based) gives EUR 75.8 bn for 2024, 4.29% of taxes plus social contributions. UBA/Destatis give EUR 76.7 bn for 2024, 7.6% of total taxes, and say explicitly that auction receipts from emissions trading are shown together with environmental taxes (UBA indicator, Aug 2026). The 0.9 bn gap is unreconciled. Do not add ETS receipts to either total.
- National accounts versus budget. In the federal budget ETS receipts are non-tax receipts of the KTF. In Eurostat's table the item D29F "taxes on pollution" in year t equals German ETS 1 auction receipts of year t-1 within EUR 1.2 m in every year 2017-2021 (`tables/d29f_vs_ets1_lag_check.csv`). **This is my inference** (medium confidence, not stated by Eurostat or Destatis; Eurostat's metadata only lists "proceeds from emission permits recorded as taxes in the national accounts" inside greenhouse-gas taxes): national accounts appear to book ETS auction receipts as taxes on pollution one year later. From 2022 D29F also contains fuel-ETS receipts and no longer reconciles.
- The 2024 ratios use 2024 denominators for 2024 receipts; 2025 receipts have no matching tax denominator yet.

## 5. Tax channels the sources do not let us measure

Full table: `tables/tax_channels_measurability.csv`. Wording for the slide: "Corporate-tax and payroll-tax effects are not measurable with these sources."

- **Corporate income tax.** Eurostat has only the national total (D51B_C2: EUR 125.1 bn in 2024; D51B excluding holding gains has no observations for Germany). No industry, product or firm split and no counterfactual; profits also move with energy prices, demand and COVID.
- **Payroll taxes and social contributions.** D29C (payroll taxes) has no observations for Germany; employers' social contributions D611 are a national total (EUR 302.3 bn in 2024). Announced job cuts (about 5,000 at Thyssenkrupp Steel) are plans, not realised tax changes.
- **Consumption taxes (price pass-through).** VAT D211 (EUR 298.8 bn in 2024) and excise D214A (EUR 36.3 bn) are national totals with no product view.
- **CBAM receipts before 2027, and any net fiscal effect** (receipts minus support, administration and revenue lost elsewhere): not observable and not estimated.
- Measurable as context only: ETS 1 auction receipts, KTF budget lines, national environmental-tax totals.

## Retrieval log (exact queries)

All retrieved 2026-10-22 unless stated. Browser-style user agent for plain downloads.

| What | Query / URL | Saved as |
| --- | --- | --- |
| EEX auction data 2012-2025 | `https://www.eex.com/fileadmin/EEX/Downloads/Markets/Environmentals/EUA_Emission_Spot_Primary_Market_Auction_Report/Archive_Reports/emission-spot-primary-market-auction-report-2012-2025-data.zip` (link found on `https://www.eex.com/en/downloads`) | `eex_..._2012-2025_data.zip` (SHA-256 c3ff6ffa...0231) |
| UBA press releases | `https://www.umweltbundesamt.de/presse/pressemitteilungen/emissionshandel-21-milliarden-euro-fliessen-in-den` (7 Jan 2026) and `.../einnahmen-aus-dem-emissionshandel-erneut-auf` (7 Jan 2025) | `uba_pm_*.html` |
| Eurostat env_ac_tax | `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/env_ac_tax?format=JSON&lang=EN&geo=DE` (all tax, unit and time values; dataset updated 2026-02-10) | `es_env_ac_tax_DE_raw.json` |
| Eurostat gov_10a_taxag | `.../data/gov_10a_taxag?format=JSON&lang=EN&geo=DE&unit=MIO_EUR&sector=S13&na_item=D2_D5_D91&na_item=D2_D5_D91_D61_M_D995&na_item=D2&na_item=D5&na_item=D29&na_item=D29F&na_item=D51&na_item=D51A_C1&na_item=D51B_C2&na_item=D61&na_item=D611&na_item=D613&na_item=D211&na_item=D214A` and the same with `sector=S13_S212&na_item=D2_D5_D91_D61_M_D995&na_item=D2_D5_D91` (updated 2026-10-21) | `es_gov_10a_taxag_DE_S13_v2.json`, `es_gov_10a_taxag_DE_S13_S212_totals.json` |
| Eurostat GDP | `.../data/nama_10_gdp?format=JSON&lang=EN&geo=DE&unit=CP_MEUR&na_item=B1GQ` | `es_nama_10_gdp_DE_B1GQ.json` |
| Availability probe | gov_10a_taxag, geo=DE, unit=MIO_EUR, sector=S13, one na_item per call (D51B, D51A, D29C empty) | `eurostat_availability_probe.json` |
| CBAM regulation texts | Publications Office Cellar, `https://publications.europa.eu/resource/celex/32023R0956` and `.../32025R2083` with header `Accept: application/xhtml+xml`, `Accept-Language: eng` (EUR-Lex itself was behind a bot check) | `cbam_reg_2023_956_original.xhtml`, `cbam_omnibus_reg_2025_2083.xhtml` (+ `.txt`) |
| Own-resources proposal | Cellar `http://publications.europa.eu/resource/cellar/176f6907-626d-11f0-bf4e-01aa75ed71a1.0001.02/DOC_1` (COM(2025) 574) | `com_2025_574_own_resources_decision.pdf` |
| Council documents | `https://data.consilium.europa.eu/doc/document/ST-13922-2026-INIT/en/pdf`, `ST-12596-2026`, `ST-12922-2026` | `council_st_*.pdf` |
| German budget documents | `https://dserver.bundestag.de/btd/21/073/2107300.pdf` (pages 27, 77, 78 and others kept as images/text), `.../21/078/2107860.pdf`, `.../21/085/2108534.pdf`, `https://dserver.bundestag.de/brd/2026/0442-26B.pdf` | `bt_drs_*`, `br_drs_*` |
| KTFG | `https://www.gesetze-im-internet.de/ekfg/__4.html` | `ktfg_par4_gesetze_im_internet.html` |

The full list with publishers and dates is in `tables/source_register.csv`. Web searches were used only to find documents; every number above comes from a document listed there. The Parliament press release (23 Apr 2026) was read through a fetch tool summary and is the only item not saved.

Units and conversions: allowances = tCO2e (1 allowance = 1 t); EEX revenue in EUR; EUR million = EUR / 1,000,000; budget tables are printed in thousand EUR, so EUR million = value / 1,000; Eurostat MIO_EUR is already EUR million; shares are my own ratios of the stated numerators and denominators.

## Checks performed (`tables/crosschecks.csv`)

- EEX German EUA revenue Jan-Sep 2023 (EUR 5,778,097,060) and Q3 2023 (EUR 1,892,192,440, 22,379,500 allowances) equal DEHSt's Q3-2023 report to the euro; 2021 and 2022 totals match DEHSt's chart labels (5.31 and 6.81 bn).
- 2021, 2023, 2024 and 2025 average prices (52.50, 83.66, 65.00, 73.86) and the 2023-2025 volumes and totals match UBA's press releases; EEA gives Germany EUR 5.5 bn for 2024. This also shows UBA's headline includes EUAA.
- Price x volume reproduces reported revenue on all 637 rows. Eurostat ENV = energy + transport + pollution/resources; ENV share of taxes and social contributions reproduced exactly with the S13+S212 denominator.
- KTF receipts Ist 2025 (ETS 1 plus fuel ETS) = EUR 21,391 m, matching UBA's EUR 21.4 bn.
- **Unreconciled:** KTF Ist 2025 for ETS 1 (EUR 5,403.4 m) is EUR 25.6 m (0.47%) below the EEX auction total (EUR 5,429.0 m); the documents read do not say why (KTFG lets DEHSt costs be deducted; settlement timing is possible). UBA/Destatis 76.7 bn versus Eurostat 75.8 bn environmental taxes. Bundesrat "400 million" versus budget EUR 377.736 m for CBAM.

## Caveats and unresolved

- DEHSt's own annual table was not opened (maintenance page); 2012 is partly derived; auction-date basis differs from cash booking and from national-accounts timing.
- The EUR 377.7 m CBAM figure is a draft budget estimate; the 2027 budget and the KTFG change are not law until the Bundestag votes (planned 27 Nov 2026).
- Own-resource negotiations were still open in the latest Council text found (10 Oct 2026); the call rate shown there is bracketed.
- National-accounts classification of CBAM receipts is unknown. The D29F timing pattern is an inference.
- Eurostat 2022-2024 tax aggregates are provisional; the ETS 1 share of 2025 tax revenue cannot be computed yet.
- UBA's 2025 press release dates the start of the EU fuel ETS (ETS 2) as 2027 and its 2026 release as 2028; irrelevant for steel and not followed up.
- No source gives auction receipts by paying sector, by German state or for steel.

## Differences from the workbook and the outline

The workbook has no tax numbers; its tax statements are qualitative. Findings that sharpen or change them:

1. Outline S10 Tax row says ETS auction receipts and tax series were "not pulled": they now are (sections 1 and 4).
2. Workbook 2.8 warns against treating "the full EU receipts as revenue retained by Germany": under current law no pooled EU receipt exists; each Member State keeps the receipts from declarants established on its territory, and the EU share (75% proposed, [90]% in the Council box) would start only from 2028 if adopted.
3. Workbook 2.8 asks to check the "current budget framework" before assuming an earmark: checked. EU law has no earmark for CBAM receipts; the German draft books them in the core budget, not the KTF; ETS 1 receipts are earmarked to the KTF by KTFG section 4 but the 2027 draft diverts EUR 2.7 bn.
4. "Receipts are not automatically German tax revenue" (S10) is confirmed for CBAM; for ETS 1 it depends on the definition (federal budget: non-tax; national accounts: probably taxes on pollution with a one-year lag).
5. Certificate sales from 1 Feb 2027 [U35] is confirmed in the legal text.

## Outline changes proposed

- **S10, Tax row.** Theory expects: "CBAM receipts are sale proceeds, not tax". What we can show: "ETS auctions EUR 5.4 bn (2025), all to KTF". Chip: Observed (ETS) / Gap (CBAM, corporate, payroll). Add a short line under the table: "CBAM: first sales 1 Feb 2027; 2027 draft budget EUR 0.38 bn. Corporate and payroll tax effects: not measurable."
- **S10, G row.** What we can show: "Gov. consumption +1.5% real (2025); KTF plan 2027: EUR 38.9 bn". Keep "subsidies are not all G" and add "KTF is mostly ETS-funded; transfers, not consumption".
- **S13.** Add CHANGE item (5): "Keep carbon receipts working for transition: ETS 1 receipts go to the KTF by law (EUR 5.4 bn, 2025); the 2027 draft diverts EUR 2.7 bn to the core budget; CBAM receipts (EUR 0.38 bn planned) have no earmark." Add "27 Nov 2026 budget vote" to the next-data-points strip and "use of carbon receipts" to the monitor strip.
- **A6.** Extend with a tax half-page: (a) ETS 1 receipts 2012-2025 table or bar (section 1); (b) CBAM rules box (who sells, 1 Feb 2027, own-resource status, German EUR 377.7 m); (c) the not-measurable list (section 5); (d) definition note on the two environmental-tax totals. S10's footer "Does not show: any estimated effect" already points here.
- Also: A1 gets "Is CBAM revenue German tax revenue?"; A4 "who pays" gets "the Member State where the declarant is established collects"; S12 NOT SHOWN list adds "tax and net budget effects"; A15 gets sources S1-S27 of `tables/source_register.csv`; open item 7 gains "Bundestag vote on the 2027 budget and own-resource talks".
