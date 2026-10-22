# German industrial electricity price series (slide 5, appendix A10) - verified at source

Retrieval date: 2026-10-22. Scope: the series in workbook BaseNotes-3 (sources/text/inter-trade-present-base.txt lines 750-765). Primary sources: Bundesnetzagentur (SMARD, Monitoringbericht with Bundeskartellamt), Destatis, Eurostat, BDEW. Nothing here comes from memory; every number was read in a document or data file opened on the retrieval date (exact URLs, pages and tables in `sources.csv`).

## 1. Result in five lines

1. The five "without reductions" values 2021-2024 and Jan 2025 in the workbook (21.77, 35.70, 19.63, 16.77, 17.99) match the SMARD article of 11 Feb 2025 word for word.
2. The workbook's 2020 value 5.92 is NOT a "without reductions" value. In the SMARD article 5.92 is the 2020 average of the series WITH all possible reductions. The no-reductions 2020 average is 17.29 ct/kWh (derived from the article's own monthly chart data; the article text does not print it). This one mislabelled cell spreads into S5, the "Bottom line" bullet (L826) and Appendix C (L988).
3. The "+77%" is arithmetically right and like-for-like: 10.47 (2024) over 5.92 (2020), both from the with-reductions series. The earlier worry in the outline ("eligible 10.47 vs no-concession 5.92 base") came from the mislabel. In the no-reductions series 2024 (16.77) is 3% BELOW 2020 (17.29), so "nearly triple the 2020 level" is wrong.
4. The SMARD series has since been re-modelled. The current SMARD data file (read 2026-10-22) differs from the Feb 2025 article by up to about 0.8 ct/kWh in single months (Jan 2025: 17.99 became 17.47; 2024 annual mean: 16.77 became 16.12). Use ONE vintage on a slide.
5. Extension from the current file: 2025 annual mean 16.49 (without reductions) and 10.10 (with); Jan-Sep 2026 mean 17.26 and 11.33; latest month in the file Sep 2026 = 20.44 and 14.51 ct/kWh (Aug 2026, 18.69 and 12.76, is confirmed by a SMARD news item of 7 Sep 2026).

## 2. What the series is (definition)

- Name on SMARD: "Industriestrompreise - Modellierte Industriestrompreise seit 2020" (Energiedaten kompakt, Strom). Monthly, ct/kWh, nominal, Jan 2020 to Sep 2026 in the file read; plus an index with Jan 2021 = 100. Two cases: "Preis ohne Vergünstigungen" and "Preis mit Vergünstigungen".
- It is a Bundesnetzagentur MODEL, not a price survey and not invoiced prices. Components: (a) levies, taxes, network charges and fees, taken yearly from the Monitoring and held constant within a year (mid-year changes adjusted); (b) sales cost and margin, estimated at about 5% of the price from expert talks; (c) procurement cost, computed monthly from suppliers' procurement strategies (day-ahead, month, quarter and 1-3 year futures weighted by their share; base and peak 0.8 to 0.2). Source: SMARD user guide, Sept 2026, section 5.1 (PDF pp. 58-59).
- "Without reductions" = a company that cannot claim reductions of network charges, electricity tax, concession fee or levies. "With reductions" = the price including ALL possible reductions (SMARD news item 7 Sep 2026: "inklusive aller möglichen Vergünstigungen"). The Monitoringbericht says it does not survey whether firms can use all maximum reductions in practice (2025 report, PDF pp. 166 and 168; same sentence in the 2024 report). So "with reductions" is a modelled best case, not an observed price of energy-intensive firms.
- Eligibility thresholds in the user guide table: network charge reduction up to 90% for more than 10 GWh at one connection and at least 6,000 full-load hours; full electricity-tax refund for producing trades (section 9a StromStG); concession fee refund; reduced KWKG, offshore and section 19 StromNEV levies.
- Consumption band: the SMARD pages do not state one. The model is fed by the Monitoring, whose industrial case is "Industriekunde, Abnahmefall 24 GWh/Jahr": 6,000 hours of use, 4,000 kW peak load, medium voltage 10 or 20 kV, price without VAT because VAT is deductible, answered by 127 suppliers (2025 report) (2024 report PDF p. 188; 2025 report PDF pp. 166-168). SMARD's yearly constant components are of the same size as the Monitoring tables (no reductions 7.43 vs 7.12 ct/kWh in 2024; with all reductions 1.10 vs 0.95 ct/kWh in 2024; 7.53 vs 7.64 and 1.14 vs 1.16 in 2025), so the 24 GWh case is the best available match, but this link is my reading, not a SMARD statement. Medium confidence.
- VAT: the user guide sentence in section 5.1 says VAT is calculated and added, which is ambiguous for a VAT-deductible customer. The constant components (about 7.4 ct/kWh in 2024) add up to the Monitoring table without VAT, so treat the series as excluding VAT.
- Not steel-specific: a 24 GWh customer is far smaller than an integrated steelworks or a DRI-EAF plant. Destatis and Eurostat show the class of 150,000 MWh and above separately (section 5).

## 3. Verification of every workbook number (full table: `workbook_verification.csv`)

| Workbook (BaseNotes-3) | Source value | Status |
| --- | --- | --- |
| 2020 = 5.92, "without reductions" | 5.92 = with reductions. Without reductions 2020 = 17.29 (derived, article data) | series mislabelled |
| 2021 = 21.77 | 21.77 printed | match |
| 2022 = 35.70 | 35.70 printed | match |
| 2023 = 19.63 | 19.63 printed | match |
| 2024 = 16.77 | 16.77 printed | match |
| Jan 2025 = 17.99 | 17.99 printed | match |
| Eligible 2024 = 10.47 | 10.47 printed (with reductions) | match; wording must say "modelled, all possible reductions" |
| "+77%" (10.47 vs 5.92) | +76.9%, both with reductions | match, like-for-like |
| Eligible Jan 2025 = 11.69; index 165.45 | printed 11.69 and 165.45 | match |
| 2024 "nearly triple the 2020 level of 5.92" | no-reductions 2024 is 3.0% below 2020 | contradicted |
| Jan-Sep 2025 about 16 (Agora) | SMARD current file: 16.40 | consistent (Agora not opened) |

"Printed" means printed in the SMARD article "Entwicklung der Industriestrompreise" (11.02.2025; the SMARD article listing carries a later date, 10 March 2025, but the text is dated 11 Feb 2025 and the embedded chart data end in Jan 2025). Check: the article's monthly chart data reproduce all nine printed annual figures within 0.01 ct/kWh when averaged simply (run `reproduce.py`), so the annual figure = simple mean of 12 monthly values, and I use the same rule for years the article does not print.

Like-for-like growth, Feb 2025 vintage: without reductions 17.29 (2020) to 35.70 (2022) = x2.06, to 16.77 (2024) = -3.0%; with reductions 5.92 to 29.01 = x4.90, to 10.47 = +76.9%. Current file: without 17.13 to 35.92 to 16.12 (-5.9%); with 5.95 to 29.10 to 9.79 (+64.5%).

## 4. Extension to 2025 and 2026 (current SMARD data file, vintage "V2")

| ct/kWh, annual mean of monthly values | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (Jan-Sep) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Without reductions, V2 derived | 17.13 | 22.05 | 35.92 | 19.89 | 16.12 | 16.49 | 17.26 |
| With reductions, V2 derived | 5.95 | 11.05 | 29.10 | 14.39 | 9.79 | 10.10 | 11.33 |
| Without, V1 printed (2020 derived) | 17.29 | 21.77 | 35.70 | 19.63 | 16.77 | - | - |
| With, V1 printed | 5.92 | 10.94 | 29.01 | 14.23 | 10.47 | - | - |

Monthly anchors (V2): peak Aug 2022 = 56.32 without and 51.27 with reductions; Jan 2025 = 17.47 and 11.08; Aug 2026 = 18.69 and 12.76 (confirmed by SMARD news item 7 Sep 2026); Sep 2026 = 20.44 and 14.51 (last point in the data file; no news item for it was found on 2026-10-22, so it may be revised). Index (Jan 2021 = 100) Sep 2026: 112.50 without and 202.33 with reductions.

Vintage trap: mixing V1 for 2020-2024 and V2 for 2025 would show 2024 to 2025 falling (16.77 to 16.49) while on one vintage it rises (16.12 to 16.49). Do not mix.

## 5. Cross-checks (invoiced or surveyed prices, different definitions; compare direction and size, not decimals)

| Series (ct/kWh) | 2020 | 2022 | 2024 | 2025 | 2026 | 2024 vs 2020 |
| --- | --- | --- | --- | --- | --- | --- |
| SMARD without reductions (V2) | 17.13 | 35.92 | 16.12 | 16.49 | 17.26 (Jan-Sep) | -5.9% |
| BDEW/VEA industry 160 MWh-20 GWh, new contracts, medium voltage, incl. reduced electricity tax | 17.7 | 43.3 | 17.3 | 17.6 | 17.2 (to Aug) | -2.3% |
| SMARD with reductions (V2) | 5.95 | 29.10 | 9.79 | 10.10 | 11.33 (Jan-Sep) | +64.5% |
| Destatis/Eurostat, class 150,000 MWh and above, excl. VAT | 6.88 | 19.02 | 13.01 | 13.23 | 12.67 (H1, prov.) | +89.1% |
| Destatis/Eurostat, class 2,000-19,999 MWh | 15.22 | 19.39 | 20.47 | 19.27 | 17.42 (H1, prov.) | +34.5% |
| Destatis, all non-household | 14.99 | 20.29 | 20.14 | 19.28 | 17.64 (H1, prov.) | +34.4% |

Reading: (a) the no-reductions level around 16-18 ct/kWh in 2020 and again in 2024-2025 is supported by BDEW. (b) The large 2020-to-2024 rise exists only in the best-case (with reductions) and the very-large-consumer classes; it is +89% in the invoiced 150,000 MWh class. (c) The invoiced and surveyed series show a much smaller 2022 peak (19-20 ct/kWh in Destatis) than SMARD's 35.7-35.9, because SMARD models wholesale-driven procurement, while invoices carry earlier contracts. (d) For the same 24 GWh case, the Monitoring survey is higher than SMARD's model: 1 Apr 2023 23.25 vs 20.74; 1 Apr 2024 20.16 vs 15.42; 1 Apr 2025 19.09 vs 15.70 (`crosscheck_smard_model_vs_monitoring_survey_24GWh.csv`). So SMARD gives direction and timing well, but its level is on the low side of the survey.

Destatis table 61243-0006 (components) was read but not used: its three components add up to the gross price including VAT (equals price type PRE-BRUTTO in table 61243-0005), so it does not compare with the excl. VAT series. Destatis headline for H1 2026 (press release 345 of 30 Sep 2026): 17.64 ct/kWh, provisional, without VAT and other deductible taxes; class 150,000 MWh and above 12.67; the planned "Industriestrompreis" relief is not yet included (BAFA applications from year-end 2026), and SMARD's with-reductions case does not list it either.

## 6. Clean series and safest wording for slide 5

File: `slide5_strip_series.csv`. Recommended strip, one vintage (SMARD data file of 22 Oct 2026), annual means of SMARD monthly modelled values:

- Header: "Modelled industrial electricity price, companies without network-charge/tax reductions (Bundesnetzagentur, SMARD), ct/kWh excl. VAT".
- BEFORE (to Sep 2023): 17.1 (2020) to 22.0 (2021) to 35.9 (2022); monthly peak 56.3 in Aug 2022.
- DURING (reporting Oct 2023-Dec 2025): 16.1 (2024), 16.5 (2025); monthly range 14.6-19.0. 2023 (19.9) straddles the start of reporting; leave it out or mark it.
- AFTER (2026): Jan-Sep average 17.3; Sep 2026 20.4 (latest in the file, provisional).
- Footnote: "Model output, not invoiced prices; SMARD states no consumption band; not steel-specific." If a second line is wanted: "with all possible reductions (modelled best case): 6.0 (2020), 29.1 (2022), 9.8 (2024), 10.1 (2025)".

Safest phrases: "companies without reductions" or "modelled price without network-charge and tax reductions". Avoid: "steelmakers paid", "energy-intensive firms' price", "eligible firms paid", "triple the 2020 level", and any link to CBAM (it is context, not a CBAM effect; SMARD itself attributes the pattern to wholesale procurement costs and the end of the EEG levy). Say "companies with all possible reductions (modelled)" instead of "eligible energy-intensive companies". If the team prefers the verbatim published numbers (21.77, 35.70, 19.63, 16.77), use them for 2021-2024 only, label them "SMARD, Feb 2025", and give no 2025 or 2026 annual value.

## 7. Method, units, conversions

- Units: ct/kWh as published by SMARD; Eurostat and Destatis publish EUR/kWh, multiplied by 100. Nominal values, no inflation adjustment, no currency conversion.
- Annual mean = simple arithmetic mean of the monthly values (Decimal arithmetic, half-up rounding to 0.01). 2026 is Jan-Sep only. Eurostat and Destatis annual values = simple mean of the two half-years (derived); 2026 = first half only, provisional.
- Index = monthly modelled price divided by the January 2021 price, times 100 (SMARD guide and index chart); index columns in the file are copied as published.
- SMARD file blocks: s-ind_stpr-1-1 (both totals), 1-2 (components, without reductions), 1-3 (components, with reductions), 2-1 (index; column order in the file: with, then without). Totals agree across blocks and components add up to totals within 0.01 (asserted in the build step).
- Missing observations stay empty (Destatis 2019 H1 and 2026 H2 are blank, not zero).

## 8. Access log and limits

- The WebFetch tool could not reach smard.de or bundesnetzagentur.de (connection refused). curl from this machine reset or timed out on many attempts to smard.de and data.bundesnetzagentur.de and then succeeded on retry; the Browser pane worked. No login, cookie wall, captcha or bot challenge was met or bypassed. The Destatis GENESIS table view calls public endpoints (/genesis/api/rest/tables/...) which were read without credentials; no guest account was used.
- Web search was used only to find URLs; its summaries are not evidence. One search summary claimed the 2020 figure of 5.92 belongs to the with-reductions series; I confirmed it in the SMARD text before using it.
- PDFs (SMARD user guide, two Monitoringberichte, BDEW) were read in a scratch folder outside the repo and are not archived here. BDEW values for 2020-2025 were read from a chart image (the 2025 and 2026 values, 17.6 and 17.2, are confirmed in the page text); treat the other years as read to one decimal.
- Not done: Agora Energiewende (secondary), the Monitoring tables for years before 2023, and any steel-sector price. The SMARD value for Sep 2026 is the last point in the data file and may be revised, as the whole series has been before.
- Annual SMARD values for 2025 and 2026 are my derivation from the monthly file; SMARD prints no annual value after 2024 in the pages read.

## 9. Files

- `smard_industrial_price_monthly_V2_live_2026-10-22.csv`: current monthly series, prices, components and index.
- `smard_industrial_price_monthly_V1_article_2025-02-11.csv`: monthly series behind the SMARD article (Jan 2020-Jan 2025).
- `smard_industrial_price_annual_means_both_vintages.csv`: derived annual means and printed figures.
- `slide5_strip_series.csv`, `workbook_verification.csv`, `sources.csv`.
- `crosscheck_*.csv`: Eurostat nrg_pc_205 (Germany, half-yearly, three tax levels, all bands), Destatis 61243-0005, summary of all series, model versus Monitoring survey.
- `reproduce.py`: recomputes the checks from the CSV files (`python -I -X utf8 reproduce.py`, no network).
