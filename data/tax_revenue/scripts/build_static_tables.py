"""Write the hand-curated (document-sourced) tables: budget lines, CBAM revenue rules, tax-channel measurability,
cross-checks and the source register. Every value is copied from a document saved in ../raw (see the 'source_file'
columns); nothing here is estimated.
Run: python -I -X utf8 build_static_tables.py   (after build_ets_revenue_tables.py)
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "tables"
E = pd.read_csv(OUT / "ets1_auction_revenue_de_by_year.csv").set_index("year")

# ---------------------------------------------------------------- A. budget lines
A = [
    # document, location, title_no, description, ist_2025, soll_2026, soll_2027, note, source_file
    ("KTF Wirtschaftsplan 2027 (6092)", "Anl. 3 zu Kap. 6002, p. 78 Einnahmen", "132 02", "Erlöse aus der Versteigerung von Berechtigungen gemäß TEHG (EU-ETS 1)", 5403354, 4265000, 2509790, "Source note: 'Weniger wegen Umschichtung in Kap. 6002 Tit. 132 03'", "bt_drs_21_7300_page3474_ktf_einnahmen.png"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Anl. 3 zu Kap. 6002, p. 78 Einnahmen", "132 03", "Erlöse aus der Veräußerung von Zertifikaten im nationalen und europäischen Brennstoffemissionshandel", 15987887, 16713426, 20029080, "Fuel ETS (nEHS now, EU-ETS 2 later); not steel-process emissions", "bt_drs_21_7300_page3474_ktf_einnahmen.png"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Anl. 3 zu Kap. 6002, p. 78 Einnahmen", "334 01", "Zuweisungen aus dem Sondervermögen Infrastruktur und Klimaneutralität", 10000000, 10000000, 10000000, "", "bt_drs_21_7300_page3474_ktf_einnahmen.png"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Anl. 3 zu Kap. 6002, p. 78 Einnahmen", "119 99", "Vermischte Einnahmen", 67558, None, None, "dash in source = no entry", "bt_drs_21_7300_page3474_ktf_einnahmen.png"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Anl. 3 zu Kap. 6002, p. 77 overview", "total", "Verwaltungseinnahmen", 21458799, 20978426, 22538870, "= 119 99 + 132 02 + 132 03 for Ist 2025 (checked)", "bt_drs_21_7300_page3473_ktf_overview.png"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Anl. 3 zu Kap. 6002, p. 77 overview", "total", "Übrige Einnahmen", 15957706, 13825197, 16399142, "", "bt_drs_21_7300_page3473_ktf_overview.png"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Anl. 3 zu Kap. 6002, p. 77 overview", "total", "Gesamteinnahmen", 37416505, 34803623, 38938012, "", "bt_drs_21_7300_page3473_ktf_overview.png"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Anl. 3 zu Kap. 6002, p. 77 overview", "total", "Gesamtausgaben", 35193883, 34803623, 38938012, "", "bt_drs_21_7300_page3473_ktf_overview.png"),
    ("Einzelplan 60, Kap. 6002 Allgemeine Bewilligungen (core budget)", "p. 27, Einnahmen", "132 02", "Erlöse aus dem CO2-Grenzausgleich (CBAM)", None, None, 377736, "Managed by BMUKN; Soll 2026 and Ist 2025 cells empty in the source; booked in Kap. 6002, not in Kap. 6001 'Steuern'", "bt_drs_21_7300_page3423_kap6002_titel132_02_CBAM.png"),
    ("Einzelplan 60, Kap. 6002 Allgemeine Bewilligungen (core budget)", "p. 27, Einnahmen", "132 03", "Erlöse aus der Versteigerung von Berechtigungen gemäß TEHG (share booked in core budget instead of KTF)", None, None, 2700000, "Needs the KTFG change in Haushaltsbegleitgesetz 2027 (draft, not enacted)", "bt_drs_21_7300_page3423_kap6002_titel132_02_CBAM.png"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Ausgaben, PDF p. 3479", "683 03", "Zuschüsse an stromintensive Unternehmen zum Ausgleich von emissionshandelsbedingten Strompreiserhöhungen", 2785602, 4000000, 5000000, "Spending line, shown for 'where the money goes'; text extract only", "bt_drs_21_7300_extract_pages.txt"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Ausgaben, PDF p. 3502", "892 01", "Dekarbonisierung der Industrie", None, 699000, 664207, "Ist 2025 not read; 2026 includes 54,000 for CO2-Differenzverträge (per Bundestag hib 646/2026)", "bt_drs_21_7300_extract_pages.txt"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Ausgaben, PDF p. 3503", "892 02", "Wasserstoffeinsatz in der Industrieproduktion", 402983, 1259000, 1619508, "2027 line also absorbs the former IPCEI hydrogen title (per hib 646/2026)", "bt_drs_21_7300_extract_pages.txt"),
    ("KTF Wirtschaftsplan 2027 (6092)", "Ausgaben, PDF p. 3510", "892 14", "CO2-Differenzverträge (carbon contracts for difference)", None, None, 100000, "New own title in 2027; largest single commitment authorisation 8.73 bn to 2048 (hib 646/2026)", "bt_drs_21_7300_extract_pages.txt"),
]
dfA = pd.DataFrame(A, columns=["budget_document", "location", "title_no", "description", "ist_2025_keur", "soll_2026_keur", "soll_2027_keur", "note", "source_file"])
dfA["unit"] = "thousand EUR (1 000 EUR)"
dfA.to_csv(OUT / "budget_lines_ktf_and_core_2025_2027.csv", index=False)
# internal consistency: Verwaltungseinnahmen Ist 2025
chk = 67558 + 5403354 + 15987887
assert chk == 21458799, chk
assert 21458799 + 15957706 == 37416505
assert 22538870 + 16399142 == 38938012 and 20978426 + 13825197 == 34803623

# ---------------------------------------------------------------- B. CBAM revenue rules
B = [
    ("Who sells certificates", "A Member State sells CBAM certificates on a common central platform to authorised declarants established in that Member State.", "Reg. (EU) 2023/956 Art. 20(1), as amended by Reg. (EU) 2025/2083 Art. 1(16)(a)", "in force", "cbam_omnibus_reg_2025_2083.txt; cbam_reg_2023_956_original.txt"),
    ("First sales date", "From 1 February 2027 (Art. 20(1), (3), (4), (5) apply from 1 Feb 2027).", "Reg. (EU) 2025/2083 Art. 1(16)(a) and Art. 1(27) (new Art. 36(2)(d))", "in force", "cbam_omnibus_reg_2025_2083.txt"),
    ("First surrender", "30 September 2027 for the 2026 declaration year; certificates bought in 2027 for 2026 may only be repurchased in 2027; unsurrendered 2026-year certificates are cancelled on 1 Nov 2027.", "Reg. (EU) 2025/2083 Art. 1(18) (Art. 22(1)), Art. 1(19) (Art. 23(2a)), Art. 1(20) (Art. 24(2))", "in force", "cbam_omnibus_reg_2025_2083.txt"),
    ("Price", "Weekly average of EU ETS auction closing prices (Art. 21(1)); for the 2026 declaration year the price is the quarterly average of the quarter of importation (new Art. 21(1a)).", "Reg. (EU) 2023/956 Art. 21(1); Reg. (EU) 2025/2083 Art. 1(17)", "in force", "cbam_omnibus_reg_2025_2083.txt"),
    ("Where the revenue accrues", "To the selling Member State: the Regulation makes Member States responsible for 'correctly establishing and collecting revenues' (recital 64); there is no article assigning certificate revenue to the Union budget or earmarking its use.", "Reg. (EU) 2023/956 recital 64, Art. 20(1); no revenue-use article found by full-text search", "in force", "cbam_reg_2023_956_original.txt"),
    ("Own-resource status today", "Not an EU own resource. Recital 74 only says the Union is working towards a new own resource based on CBAM certificate sales.", "Reg. (EU) 2023/956 recital 74", "in force", "cbam_reg_2023_956_original.txt"),
    ("Platform fees (different flow)", "Fees paid by declarants for the central platform are Union internal assigned revenue (first procurement contract), not Member State revenue; any remainder goes to the Union budget.", "Reg. (EU) 2025/2083 Art. 1(16)(c) (new Art. 20(5a))", "in force", "cbam_omnibus_reg_2025_2083.txt"),
    ("Commission own-resource proposal", "Uniform call rate of 75% of revenues from the sale of CBAM certificates to the EU budget; Commission estimate EUR 1.4 bn a year on average in the next MFF (EUR 1.5 bn in current prices, per the ECA).", "COM(2025) 574 final of 16 Jul 2025 (Art. 3(1)(h), recital 15, application from [1 January 2028]); ECA Opinion 04/2026 para 22-23", "proposal, not adopted", "com_2025_574_own_resources_decision.txt; eca_opinion_2026_04_own_resources.txt"),
    ("Council negotiating position", "Negotiating Box of 10 Oct 2026 keeps CBAM as new own resource with the call rate in square brackets at [90]% (not agreed); Presidency note of 4 Sep 2026: CBAM is the most consensual of the five proposed new own resources, many Member States open to a higher call rate. New system would apply retroactively from 1 Jan 2028 once adopted and ratified.", "Council docs 13922/26 (para 133, 137 v) and 12596/26", "negotiation, no agreement found", "council_st_13922_2026.txt; council_st_12596_2026.txt"),
    ("Approval route", "Own Resources Decision needs unanimity in the Council after consulting the European Parliament, then ratification by every Member State; Parliament's interim report of 28 Apr 2026 (370-201-84) backs the basket approach and about EUR 60 bn a year of new own resources, with no CBAM-specific rate in the press release.", "ECA Opinion 04/2026; Council 13922/26; EP press release 23 Apr 2026 (read via WebFetch, not saved)", "pending", "eca_opinion_2026_04_own_resources.txt; council_st_13922_2026.txt"),
    ("Germany: budget treatment (draft 2027)", "Federal draft budget 2027 books CBAM receipts of EUR 377.736 million as non-tax receipts in Einzelplan 60, Kap. 6002 Tit. 132 02 (managed by BMUKN); the tax chapter is Kap. 6001 'Steuern'; Kap. 6002 shows no 2026 Soll and no 2025 Ist for this title. The Bundesrat statement rounds the figure to 400 million and notes it is the first time such receipts go to the core budget.", "BT-Drs. 21/7300 (Einzelplan 60) pp. 27 and TOC; BR-Drs. 442/26 (B) / BT-Drs. 21/8534 item 3", "government draft; Bundestag final vote planned 27 Nov 2026", "bt_drs_21_7300_page3423_kap6002_titel132_02_CBAM.png; bt_drs_21_8534.txt"),
    ("Germany: earmark", "No CBAM line in KTFG section 4(1) (revenue of the Klima- und Transformationsfonds); the draft KTF Wirtschaftsplan 2027 lists no CBAM receipt.", "KTFG section 4(1); KTF Wirtschaftsplan 2027 p. 78", "in force / draft", "ktfg_par4_gesetze_im_internet.html; bt_drs_21_7300_page3474_ktf_einnahmen.png"),
    ("Is it German tax revenue?", "No. It is the sale price of certificates (a non-tax receipt of the selling Member State), not a tax or customs duty on the euro value of steel, and the German draft budget does not book it under 'Steuern'. National-accounts (ESA) classification of CBAM receipts: no Eurostat/Destatis guidance found, left open.", "synthesis of the rows above", "as of 2026-10-22", ""),
]
dfB = pd.DataFrame(B, columns=["topic", "rule_or_fact", "legal_basis_or_document", "status_2026_10_22", "source_file"])
dfB.to_csv(OUT / "cbam_revenue_rules.csv", index=False)

# ---------------------------------------------------------------- C. tax channels
C = [
    ("EU-ETS 1 auction receipts (federal/KTF)", "Measurable (annual, EUR)", "EEX/DEHSt auction results 2012-2025; KTF Ist 2025 EUR 5.403 bn", "Auction receipts are not split by paying sector; steel installations get free allocation, so the series says nothing about steel's own payments.", "Show as context for G and Tax, never as a steel or CBAM effect."),
    ("CBAM certificate receipts", "Not yet observable", "First sales 1 Feb 2027; only a budget estimate (EUR 377.7 m, 2027 draft, all CBAM goods)", "No realised receipt exists; the estimate covers every CBAM good (steel, aluminium, cement, fertilisers, hydrogen, electricity), not steel alone.", "Say 'first receipts from Feb 2027; draft budget EUR 0.38 bn for 2027'."),
    ("Corporate income tax (Körperschaftsteuer, Gewerbesteuer)", "Not measurable for this question", "Eurostat gov_10a_taxag: national total only (D51B_C2 EUR 125.1 bn in 2024); D51B (excluding holding gains) not populated for Germany", "No breakdown by industry or product, no firm-level data, no counterfactual; profits move with energy prices, demand and COVID. A fall or rise in the total cannot be tied to ETS or CBAM.", "Say 'corporate tax effects not measurable with these sources'."),
    ("Payroll taxes and social contributions", "Not measurable for this question", "Eurostat: D29C (payroll taxes) not populated for Germany; D611 employers' social contributions EUR 302.3 bn in 2024 (national total)", "Wage tax sits inside income tax (D51A_C1); no industry or firm split; announced job cuts (about 5,000 at Thyssenkrupp Steel) are plans, not realised tax changes.", "Say 'payroll tax effects not measurable'; link to jobs plans only as announcements."),
    ("VAT and excise (price pass-through to buyers)", "Not measurable for this question", "Eurostat D211 VAT EUR 298.8 bn and D214A excise EUR 36.3 bn in 2024 (national totals)", "No product-level view and no pass-through estimate for steel-using goods.", "Say 'consumption-tax effects not measurable'."),
    ("Energy and environmental taxes", "Measurable only as national context", "Eurostat env_ac_tax: EUR 75.8 bn (2024), 1.75% of GDP, 4.29% of taxes and social contributions; UBA/Destatis broader series EUR 76.7 bn incl. emissions-trading receipts", "Definitions differ between Eurostat and UBA; neither isolates steel.", "Label 'context only'; do not subtract or add to ETS receipts."),
    ("Subsidies and transfers financed by the receipts (G side)", "Measurable as budget plans", "KTF Wirtschaftsplan 2027: EUR 38.9 bn; industry decarbonisation EUR 0.66 bn, hydrogen in industry EUR 1.62 bn, carbon contracts for difference EUR 0.10 bn (2027 Soll), electricity-intensive firms EUR 5.0 bn", "Plans, not delivered; subsidies and transfers are not all government consumption (G) in the GDP identity.", "Keep S10 G row wording: 'subsidies are not all G'."),
    ("Net budget effect of the policy", "Not measurable", "-", "Would need receipts minus support minus administration minus lost revenue elsewhere with a counterfactual; none of the sources provides it.", "Say 'net fiscal effect not estimated'."),
]
dfC = pd.DataFrame(C, columns=["tax_channel", "measurability", "what_exists", "why_effect_not_identified", "wording_for_slide"])
dfC.to_csv(OUT / "tax_channels_measurability.csv", index=False)

# ---------------------------------------------------------------- D. cross-checks
y = lambda yr, c: float(E.loc[yr, c])
D = [
    ("EEX Jan-Sep 2023 German EUA revenue", 5778097060, 5778097060, "DEHSt Auktionierung Q3 2023 report, Tabelle 2 (source EEX, DEHSt)", "exact"),
    ("EEX Q3 2023 German EUA revenue (13 auctions)", 1892192440, 1892192440, "same report, Tabelle 1", "exact"),
    ("EEX 2021 German EUA+EUAA revenue, EUR bn", round(y(2021, "total_revenue_eur") / 1e9, 2), 5.31, "same report, Abbildung 1 label 'Gesamt 2021'", "matches at 2 decimals"),
    ("EEX 2022 German EUA+EUAA revenue, EUR bn", round(y(2022, "total_revenue_eur") / 1e9, 2), 6.81, "same report, Abbildung 1 label 'Gesamt 2022'", "matches at 2 decimals"),
    ("2021 average price EUR/t", y(2021, "avg_price_eur_per_t"), 52.50, "UBA press release 01/2025 (7 Jan 2025)", "exact"),
    ("2023 average price EUR/t", y(2023, "avg_price_eur_per_t"), 83.66, "UBA press release 01/2025", "exact"),
    ("2023 volume, million", round(y(2023, "total_volume_t") / 1e6, 1), 92, "UBA press release 01/2025 ('92 Millionen')", "rounded match (91.5 m)"),
    ("2024 average price EUR/t", y(2024, "avg_price_eur_per_t"), 65.00, "UBA press release 01/2025", "exact"),
    ("2024 volume, million", round(y(2024, "total_volume_t") / 1e6, 1), 85, "UBA press release 01/2025", "rounded match (85.05 m)"),
    ("2024 revenue EUR bn", round(y(2024, "total_revenue_eur") / 1e9, 1), 5.5, "UBA press release 01/2025; EEA indicator (Germany EUR 5.5 bn, 2024)", "rounded match"),
    ("2025 volume, million", round(y(2025, "total_volume_t") / 1e6, 1), 73.5, "UBA press release 01/2026 (7 Jan 2026)", "match"),
    ("2025 average price EUR/t", y(2025, "avg_price_eur_per_t"), 73.86, "UBA press release 01/2026 ('rund 74 (73,86) Euro')", "exact"),
    ("2025 revenue EUR bn", round(y(2025, "total_revenue_eur") / 1e9, 1), 5.4, "UBA press release 01/2026", "rounded match"),
    ("2025 revenue: EEX auctions vs KTF Ist booking, EUR", y(2025, "total_revenue_eur"), 5403354000, "KTF Wirtschaftsplan 2027, Tit. 132 02 Ist 2025 = 5 403 354 thousand EUR", "NOT equal: KTF is 25.64 m (0.47%) lower; reason not stated in the documents read (KTFG section 4 lets DEHSt costs be deducted; settlement timing possible)"),
    ("KTF Ist 2025 ETS 1 + fuel ETS, EUR m", (5403354 + 15987887) / 1e3, 21400, "UBA press release 01/2026 ('21,4 Milliarden Euro')", "rounded match"),
    ("Price x volume = reported revenue (637 German auction rows)", 0.0, 0.0, "max absolute difference in EUR across all reported rows", "exact; used to derive the 22 empty 2012 cells"),
    ("Eurostat ENV / (taxes + social contributions incl. imputed, S13+S212) vs Eurostat PC_TSCO", 0.0, 0.0, "max abs difference in percentage points, 30 years", "exact; confirms the denominator Eurostat uses"),
    ("Eurostat ENV 2024 vs UBA/Destatis environmental taxes 2024, EUR bn", 75.794, 76.7, "UBA indicator WIRT-04 (Destatis Genesis)", "NOT equal: 0.9 bn (1.2%); definitions differ, UBA explicitly includes ETS auction receipts and nEHS"),
    ("UBA share 7.6% of total taxes vs own ratio 76.7 / D2+D5+D91 (S13) 2024", round(76.7 / 1006.603 * 100, 2), 7.6, "UBA indicator WIRT-04", "match: UBA denominator is taxes without social contributions"),
    ("Eurostat D29F (taxes on pollution) in year t vs German ETS 1 auction revenue in year t-1, 2017-2021, max abs diff EUR m", 1.2, 0.0, "tables/d29f_vs_ets1_lag_check.csv", "within 1.2 m in all five years; inference that national accounts book ETS 1 receipts with a one-year lag (see README)"),
]
dfD = pd.DataFrame(D, columns=["check", "our_value", "published_or_reference_value", "reference_source", "result"])
dfD.to_csv(OUT / "crosschecks.csv", index=False)

# ---------------------------------------------------------------- E. source register
S = [
    ("S1", "UBA press release 01/2026: Emissionshandel 21 Milliarden Euro fliessen in den KTF", "Umweltbundesamt / DEHSt", "2026-01-07", "https://www.umweltbundesamt.de/presse/pressemitteilungen/emissionshandel-21-milliarden-euro-fliessen-in-den", "uba_pm_2025_revenue.html"),
    ("S2", "UBA press release 01/2025: Einnahmen aus dem Emissionshandel erneut auf Rekordniveau", "Umweltbundesamt / DEHSt", "2025-01-07", "https://www.umweltbundesamt.de/presse/pressemitteilungen/einnahmen-aus-dem-emissionshandel-erneut-auf", "uba_pm_2025_01_revenue_2024.html"),
    ("S3", "EEX Emission Spot Primary Market Auction Report 2012-2025 (data archive)", "European Energy Exchange (auctioneer for the German auctions)", "published 2026 (2025 file complete)", "https://www.eex.com/fileadmin/EEX/Downloads/Markets/Environmentals/EUA_Emission_Spot_Primary_Market_Auction_Report/Archive_Reports/emission-spot-primary-market-auction-report-2012-2025-data.zip", "eex_emission_spot_primary_market_auction_report_2012-2025_data.zip"),
    ("S4", "DEHSt: Auktionierung (EU-ETS) Deutsche Versteigerungen, Drittes Quartal 2023 (mirror on openUmwelt)", "DEHSt im Umweltbundesamt", "2023-10", "https://openumwelt.de/server/api/core/bitstreams/9f789715-6339-4ff0-9f59-cea1dac2d340/content", "openumwelt_auktionierung.pdf"),
    ("S5", "UBA chart 'Erlöse aus dem nationalen und europäischen Emissionshandel (2008-2025)' (no data labels)", "Umweltbundesamt", "2026-01-07", "https://www.umweltbundesamt.de/system/files/medien/11867/bilder/diagramm_100mrd.jpg", "uba_chart_erloese_2008_2025.jpg"),
    ("S6", "KTFG section 4 Einnahmen des Sondervermögens (law is filed as EKFG on gesetze-im-internet.de)", "Bundesministerium der Justiz", "retrieved 2026-10-22", "https://www.gesetze-im-internet.de/ekfg/__4.html", "ktfg_par4_gesetze_im_internet.html"),
    ("S7", "BT-Drs. 21/7300 Haushaltsgesetz 2027, Einzelplan 60 incl. KTF Wirtschaftsplan (3,562 pages; 275 MB PDF not kept; SHA-256 of the download 7b3b82fd11328de78dd72fdfdaf2e2cea1f144627341d22113758bb4652c0980)", "Deutscher Bundestag / Bundesregierung", "2026-08-14 (received by Bundestag)", "https://dserver.bundestag.de/btd/21/073/2107300.pdf", "bt_drs_21_7300_page*.png; bt_drs_21_7300_extract_pages.txt"),
    ("S8", "BT-Drs. 21/7860 Entwurf eines Haushaltsbegleitgesetzes 2027 (KTFG change, Art. 6)", "Bundesregierung", "2026-09-07", "https://dserver.bundestag.de/btd/21/078/2107860.pdf", "bt_drs_21_7860_haushaltsbegleitgesetz_2027.pdf; bt_drs_21_7860.txt"),
    ("S9", "BT-Drs. 21/8534 Stellungnahme des Bundesrates und Gegenäusserung der Bundesregierung", "Bundesrat / Bundesregierung", "2026-10-14", "https://dserver.bundestag.de/btd/21/085/2108534.pdf", "bt_drs_21_8534.pdf; bt_drs_21_8534.txt"),
    ("S10", "BR-Drs. 442/26 (Beschluss) Stellungnahme zum Haushaltsbegleitgesetz 2027", "Bundesrat", "2026-09-25", "https://dserver.bundestag.de/brd/2026/0442-26B.pdf", "br_drs_442_26B.pdf; br_drs_442_26B.txt"),
    ("S11", "Bundestag hib 646/2026: Etat 2027 KTF-Ausgaben steigen auf 38,9 Milliarden Euro", "Deutscher Bundestag (hib)", "2026-08-17", "https://www.bundestag.de/presse/hib/kurzmeldungen-1205230", "bt_hib_646_2026.html"),
    ("S12", "Bundestag hib 826/2026: Bundesrat kritisiert Haushaltsbegleitgesetz 2027", "Deutscher Bundestag (hib)", "2026-10-14", "https://www.bundestag.de/presse/hib/kurzmeldungen-1224770", "bt_hib_826_2026.html"),
    ("S13", "Bundestag: Haushalt 2027 Ablauf (Bereinigungssitzung 12 Nov, final vote 27 Nov 2026)", "Deutscher Bundestag", "retrieved 2026-10-22", "https://www.bundestag.de/dokumente/textarchiv/2026/kw34-haushalt-2027-ablauf-1187766", "bt_textarchiv_haushalt_2027_ablauf.html"),
    ("S14", "Regulation (EU) 2023/956 (CBAM), OJ L 130, 16.5.2023 (as published)", "European Parliament and Council", "2023-05-10", "https://eur-lex.europa.eu/eli/reg/2023/956/oj/eng", "cbam_reg_2023_956_original.xhtml"),
    ("S15", "Regulation (EU) 2025/2083 amending Regulation (EU) 2023/956, OJ 17.10.2025", "European Parliament and Council", "2025-10-08", "https://eur-lex.europa.eu/eli/reg/2025/2083/oj/eng", "cbam_omnibus_reg_2025_2083.xhtml"),
    ("S16", "COM(2025) 574 final, proposal for a Council Decision on the system of own resources", "European Commission", "2025-07-16", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0574", "com_2025_574_own_resources_decision.pdf"),
    ("S17", "ECA Opinion 04/2026 on the own resources proposal", "European Court of Auditors", "2026-01-22", "https://www.eca.europa.eu/ECAPublications/OP-2026-04/OP-2026-04_EN.pdf", "eca_opinion_2026_04_own_resources.pdf"),
    ("S18", "Council 13922/26 MFF 2028-2034 Negotiating Box", "Council of the EU (General Secretariat)", "2026-10-10", "https://data.consilium.europa.eu/doc/document/ST-13922-2026-INIT/en/pdf", "council_st_13922_2026.pdf"),
    ("S19", "Council 12596/26 Presidency note, MFF revenue policy debate (marked LIMITE; retrievable from the public register)", "Council of the EU (Presidency)", "2026-09-04", "https://data.consilium.europa.eu/doc/document/ST-12596-2026-INIT/en/pdf", "council_st_12596_2026.pdf"),
    ("S20", "Council 12922/26 Presidency note, revenue and expenditure", "Council of the EU (Presidency)", "2026-09-14", "https://data.consilium.europa.eu/doc/document/ST-12922-2026-INIT/en/pdf", "council_st_12922_2026.pdf"),
    ("S21", "Commission Q&A on the MFF 2028-2034 own resources (QANDA/25/1848)", "European Commission", "2025-07-16", "https://ec.europa.eu/commission/presscorner/api/files/document/print/en/qanda_25_1848/QANDA_25_1848_EN.pdf", "ec_qanda_25_1848_mff_own_resources.pdf"),
    ("S22", "EEA indicator: Use of auctioning revenues generated under the EU ETS", "European Environment Agency", "2025-12-17", "https://www.eea.europa.eu/en/analysis/indicators/use-of-auctioning-revenues-generated", "eea_use_of_auctioning_revenues.html"),
    ("S23", "Eurostat env_ac_tax (Environmental tax revenues), geo=DE", "Eurostat", "dataset updated 2026-02-10", "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/env_ac_tax?format=JSON&lang=EN&geo=DE", "es_env_ac_tax_DE_raw.json"),
    ("S24", "Eurostat gov_10a_taxag (Main national accounts tax aggregates), geo=DE", "Eurostat", "dataset updated 2026-10-21", "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/gov_10a_taxag?format=JSON&lang=EN&geo=DE&unit=MIO_EUR&sector=S13", "es_gov_10a_taxag_DE_S13_v2.json; es_gov_10a_taxag_DE_S13_S212_totals.json"),
    ("S25", "Eurostat nama_10_gdp B1GQ CP_MEUR, geo=DE", "Eurostat", "dataset updated 2026-10-21", "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?format=JSON&lang=EN&geo=DE&unit=CP_MEUR&na_item=B1GQ", "es_nama_10_gdp_DE_B1GQ.json"),
    ("S26", "Eurostat ESMS metadata for env_ac_tax", "Eurostat", "retrieved 2026-10-22", "https://ec.europa.eu/eurostat/cache/metadata/en/env_ac_tax_esms.htm", "es_env_ac_tax_esms.html"),
    ("S27", "UBA indicator: Umweltbezogene Steuern (Destatis Genesis data)", "Umweltbundesamt", "2026-08-03 (indicator PDF)", "https://www.umweltbundesamt.de/daten/umweltindikatoren/indikator-umweltbezogene-steuern", "uba_indikator_umweltbezogene_steuern.html; uba_indikator_wirt04_umweltbezogene_steuern_2026-08-03.pdf"),
]
dfS = pd.DataFrame(S, columns=["id", "title", "publisher", "document_date", "url", "saved_as_in_raw"])
dfS["retrieved"] = "2026-10-22"
dfS.to_csv(OUT / "source_register.csv", index=False)
print("written:", sorted(p.name for p in OUT.glob("*.csv")))
