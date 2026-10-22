"""Builds the CSV tables in this folder from hand-curated extractions.

Run:  python -I -X utf8 build_tables.py <output_dir>

Every row below was read by the analyst in the cited source on 2026-10-22.
Nothing is estimated from memory. Arithmetic is recomputed in checks_output.csv.
Units: EUR million unless the column says otherwise; Mt = million tonnes.
"""
import csv
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
RET = "2026-10-22"


def write(name, header, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            assert len(r) == len(header), (name, r)
            w.writerow(r)
    print("wrote", path, len(rows), "rows")


EC = "https://ec.europa.eu/commission/presscorner/detail/en/"

# ---------------------------------------------------------------- verified facts
H = ["id", "topic", "item", "workbook_claim", "verified_value", "unit", "as_of",
     "who_funds", "status", "source_type", "source_title", "source_url",
     "doc_ref", "quoted_label_de_or_en", "retrieved", "confidence", "note"]

F = [
 ["F01", "tkH2Steel", "Direct grant", "EUR 550 m direct grant",
  "up to 550", "EUR m", "2023-07-20", "Bund (BMWK/BMWE) with NRW; see F04", "verified",
  "European Commission press release",
  "State aid: Commission approves German 550 million direct grant and conditional payment mechanism of up to 1.45 billion (ThyssenKrupp Steel Europe)",
  EC + "ip_23_3928", "IP/23/3928, SA.105244, paragraph 'The German measures'",
  "direct grant of up to 550 million", RET, "high",
  "Grant supports construction/installation of a direct reduction plant and two melting units in Duisburg replacing a blast furnace."],
 ["F02", "tkH2Steel", "Conditional payment mechanism", "up to EUR 1.45 bn for first ten years",
  "up to 1,450", "EUR m", "2023-07-20", "Bund with NRW", "verified",
  "European Commission press release", "IP/23/3928", EC + "ip_23_3928",
  "IP/23/3928, paragraph 'The German measures'",
  "during the first ten years of operation", RET, "high",
  "Covers additional cost of renewable instead of low-carbon hydrogen; yearly verification by independent expert on volumes and price paid."],
 ["F03", "tkH2Steel", "Total commitment", "up to about EUR 2 bn",
  "about 2,000 (550 + 1,450); BMWE: 'knapp 2 Mrd' approved 27 Jul 2023 for construction and operation", "EUR m",
  "2026-09-01", "Bund + NRW", "verified",
  "Bundesregierung (BMWE written answer, State Secretary Wetzel)",
  "Bundestag Drucksache 21/7837 (4 Sep 2026), written question 58 (Komning)",
  "https://dserver.bundestag.de/btd/21/078/2107837.pdf", "printed p. 39 (PDF p. 45)",
  "knapp 2 Mrd. Euro ... bewilligt", RET, "high",
  "BMWE adds: no further commitments beyond the approved amount since project start; project 'in Umsetzung'."],
 ["F04", "tkH2Steel", "Split Bund / NRW", "not stated in workbook",
  "NRW 30% (BMWE) = about 600; NRW 'up to 700' (company and NRW title of Landtag report); Bund then about 1,300-1,400",
  "EUR m", "2026-09-01", "Bund and Land NRW", "verified (small inconsistency between 30% and 700)",
  "Bundesregierung; company press release; NRW ministry",
  "Drs 21/7837 q.58; thyssenkrupp Steel release 26 Jul 2023; NRW Vorlage 18/5029",
  "https://www.thyssenkrupp-steel.com/de/newsroom/pressemitteilungen/thyssenkrupp-steel-erhaelt-foerderung-in-einer-gesamthoehe-von-rund-zwei-milliarden-euro-durch-bund-und-land.html",
  "Drs 21/7837 p.39; tk release paragraph 2; Vorlage 18/5029 subject line",
  "30 Prozent ... Kofinanzierung / bis zu 700 Millionen Euro", RET, "medium",
  "30% of 'knapp 2 bn' is about 0.6 bn, not 0.7 bn. Report both; ask NRW if exact split is needed."],
 ["F05", "tkH2Steel", "Dates of approval", "not stated",
  "EC decision 20 Jul 2023; federal commitment confirmed 26 Jul 2023; BMWE Bescheid dated 27 Jul 2023", "date",
  "2023-07-27", "Bund + NRW", "verified", "EC; company; Bundesregierung",
  "IP/23/3928; tk release 26 Jul 2023; Drs 21/7837", EC + "ip_23_3928",
  "see F01, F03", "Zuwendungsbescheid wird in den naechsten Tagen uebersandt", RET, "high", ""],
 ["F06", "tkH2Steel", "Fuel path in the State-aid decision", "targets full hydrogen operation by 2029",
  "EC: natural gas used initially then gradually phased out; plant operated only with renewable hydrogen as of 2037; start of operation 'envisioned' 2026; 2.3 Mt hot metal per year",
  "text", "2023-07-20", "n/a", "workbook 2029 claim is NOT in the EC decision text", "European Commission press release",
  "IP/23/3928", EC + "ip_23_3928", "IP/23/3928 paragraphs 'The German measures'",
  "as of 2037, the plant will be operated using only renewable hydrogen", RET, "high",
  "2029 is a company target (Feb 2024), not a State-aid condition in the press text."],
 ["F07", "tkH2Steel", "Company hydrogen timetable (historic)", "full hydrogen operation by 2029",
  "first hydrogen 2028; ramp-up to full hydrogen operation to be completed 2029; 143,000 t H2 per year (5.6 TWh); 2.5 Mt DRI per year",
  "text", "2024-02-16", "n/a", "SUPERSEDED (see F08)", "Company press release (thyssenkrupp Steel)",
  "thyssenkrupp Steel press release 16 Feb 2024 (hydrogen supply tender)",
  "https://www.thyssenkrupp-steel.com/media/content_1/presse/dokumente/2024_1/februar_6/20240216_pm_h2-ausschreibung.pdf",
  "p. 1", "Wasserstoffeinsatz soll 2028 starten, 100 % Wasserstoffbetrieb in 2029", RET, "high",
  "Same 2029 wording appears in the 26 Jul 2023 release. This is the origin of the workbook line."],
 ["F08", "tkH2Steel", "Hydrogen timetable now", "full hydrogen operation by 2029",
  "Company says green hydrogen unlikely to be available at start-up; plant designed to run on natural gas as bridge. Funding rules amended: EC approved (Aug 2026), Germany must still adjust Bescheid. NRW ministry (23 Apr 2026): EC examining adjustment because hydrogen ramp-up slower than expected.",
  "text", "2026-09-24", "Bund + NRW", "updated; 2029 target no longer a reliable date",
  "Company web page; NRW ministry report; trade press (Reuters relayed)",
  "tk climate-strategy page; NRW Vorlage 18/5029; Eurometal 17 and 20 Aug 2026; EUToday 14 Aug 2026; Gasworld 24 Sep 2026",
  "https://www.thyssenkrupp-steel.com/en/company/sustainability/climate-strategy/climate-strategy.html",
  "tk page 'Important for the transition phase'; Vorlage 18/5029 Bericht p. 2 of 3 (PDF p. 4)",
  "Green hydrogen is unlikely to be available when the DR plant ... start up", RET, "medium",
  "The EC approval of the amendment is reported only via Reuters/trade press quoting CFO Axel Hamann (GMK spells 'Gammann'); no EC or BMWE text could be opened. Treat as medium confidence."],
 ["F09", "tkH2Steel", "Commissioning date", "VW MoU: commissioning from 2027 (workbook line 127)",
  "company: commissioning starts 2027; plant manager: planned production start end 2027; SMS group CEO (Mar 2025): gradual ramp-up from end 2027; original plan end 2026",
  "year", "2026-06-10", "n/a", "verified (company statements); date still planned, not achieved",
  "Company web page; trade press",
  "tk transformation site FAQ; Ingenieur.de 10 Jun 2026; dpa-AFX 20 Jun 2025",
  "https://transformation.thyssenkrupp-steel.com/", "FAQ 'Wann ist die Direktreduktionsanlage betriebsbereit?'",
  "Die Inbetriebnahme der DR-Anlage startet 2027", RET, "medium",
  "VW MoU release 22 Oct 2024: plant to be commissioned in 2027, natural gas first, then hydrogen; deliveries from 2028. No date conflict with F09; the conflict is with the 2029 full-hydrogen line (F07)."],
 ["F10", "tkH2Steel", "Construction status", "n/a", "DR tower construction continues; pre-assembly of the two smelters almost complete (9M FY25/26)", "text",
  "2026-06-30", "n/a", "verified", "Company interim report",
  "thyssenkrupp Interim report 9 months 2025/2026",
  "https://ucpcdn.thyssenkrupp.com/_binary/UCP5thyssenkruppAG/9e9a9a77-7ffb-4d70-8a17-1803288b00e6/thyssenkrupp_Q3_2025_2026_EN_web.pdf",
  "PDF p. 19 (Steel Europe, Investments)", "construction of the DR tower continued", RET, "high", ""],
 ["F11", "tkH2Steel", "Cash received (company, group level)", "n/a",
  "Proceeds from government grants (group cash-flow line): FY22/23 154; FY23/24 417; FY24/25 346; 9M FY24/25 205; 9M FY25/26 252 (stated as DR-plant grants)",
  "EUR m", "2026-06-30", "Bund + NRW", "verified as reported; NOT a clean tkH2Steel-only series",
  "Company annual and interim reports",
  "thyssenkrupp AR 2023/24 (PDF p. 183), AR 2024/25 (PDF p. 232), Interim report 9M 2025/26 (PDF p. 41)",
  "https://ucpcdn.thyssenkrupp.com/_binary/UCP5thyssenkruppAG/9e9a9a77-7ffb-4d70-8a17-1803288b00e6/thyssenkrupp_Q3_2025_2026_EN_web.pdf",
  "9M note 09: 'received payments of EUR 252 million under government grants'", "payments of EUR 252 million under government grants",
  RET, "medium",
  "Sum FY23/24 + FY24/25 + 9M FY25/26 = 1,015 (checks_output.csv). Exceeds the EUR 550 m 'direct grant' ceiling, so payout is not limited to the EC's direct-grant tranche; consistent with the federal statement that IPCEI-type aid is paid out early pro rata to eligible investment costs (Drs 20/12166 q.21-22, p. 9)."],
 ["F12", "tkH2Steel", "NRW payout statement", "n/a",
  "NRW minister: 'a high two-digit million amount' of state money had flowed by 10 Oct 2024; Handelsblatt had reported about 500 m in total (not confirmed by government)",
  "text", "2024-10-10", "Land NRW", "verified (qualitative)", "NRW Landtag committee protocol",
  "Landtag NRW Ausschussprotokoll APr 18/703", "https://www.landtag.nrw.de/portal/WWW/dokumentenarchiv/Dokument/MMA18-703.pdf",
  "PDF p. 10 (Minister Neubaur)", "hoher zweistelliger Millionenbetrag abgeflossen", RET, "medium",
  "Aid is paid along project progress ('entlang tatsaechlich erfolgter Arbeit')."],
 ["F13", "payout transparency", "Federal payout status is not public", "n/a",
  "Bundesregierung classified the project-by-project 'Bewilligungs- und Auszahlungsstand' for Salzgitter, thyssenkrupp, ArcelorMittal, SHS as VS-Vertraulich (8 Jan 2026); NRW ministry also withholds detail (23 Apr 2026)",
  "text", "2026-04-23", "Bund + Laender", "verified", "Bundesregierung; NRW ministry",
  "Drucksache 21/3563 questions 18-20; NRW Vorlage 18/5029",
  "https://dserver.bundestag.de/btd/21/035/2103563.pdf", "Drs 21/3563 p. 6; Vorlage 18/5029 last paragraph",
  "als Verschlusssache VS-Vertraulich eingestuft", RET, "high",
  "So 'actually paid' must come from company reports (F11, F16)."],
 ["F14", "SALCOS", "Direct grant (original)", "EUR 1 bn direct grant for DRI plant + EAF + 100 MW electrolyser",
  "1,000 (EC: '1 billion'); DR plant + EAF replacing one blast furnace; 100 MW electrolyser about 9,000 t H2 per year; about 1.9 Mt crude steel per year; start 2026 (EC); site in Salzgitter, Lower Saxony",
  "EUR m", "2022-10-04", "Bund + Land Niedersachsen", "verified", "European Commission press release",
  "State aid: Commission approves 1 billion German measure to support Salzgitter decarbonise its steel production by using hydrogen",
  EC + "ip_22_5968", "IP/22/5968, SA.104276", "a direct grant", RET, "high", ""],
 ["F15", "SALCOS", "Bund / Land split and Bescheid", "not stated",
  "about 700 Bund + about 300 Lower Saxony (70/30); Bescheid handed over 18 Apr 2023 (Habeck, Weil); first stage then planned end 2025",
  "EUR m", "2023-04-18", "Bund 70%, Niedersachsen 30%", "verified", "Projekttraeger Juelich (PtJ); company release",
  "PtJ news 18 Apr 2023; Salzgitter AG release 18 Apr 2023",
  "https://www.ptj.de/veroeffentlichungen/aktuelles/co2-armer_stahl_salcos-projekt_erhaelt_rund_1_milliarde_euro_foerderung",
  "PtJ page; Salzgitter release paragraphs 3-4",
  "Das BMWK uebernimmt 70 Prozent ..., die restlichen 30 Prozent traegt das Land Niedersachsen", RET, "high",
  "PtJ is the federal project agency for national IPCEI/KUEBLL hydrogen projects (notification support and payout handling)."],
 ["F16", "SALCOS", "Top-up of public funding", "EUR 1 bn",
  "+322 to about 1,322 (EC approval 6 Feb 2026 per h2-news; announced 23 Feb 2026 by Lower Saxony ministries via dpa); Bund 2/3 and Land 1/3 (of the additional amount)",
  "EUR m", "2026-02-23", "Bund and Niedersachsen", "workbook figure outdated",
  "Lower Saxony ministries (via dpa); company slides",
  "OLZ/dpa 23 Feb 2026; h2-news; Salzgitter annual press conference 23 Mar 2026 slides 5 and 28",
  "https://www.oldenburger-onlinezeitung.de/niedersachsen/bund-und-land-stocken-foerderung-fuer-salzgitter-stahlprojekt-auf-1322-milliarden-euro-auf-194831.html",
  "dpa text; JPK slide 5 'Aufstockung ... auf 1,322 Milliarden Euro'",
  "Aufstockung der staatlichen Foerderung fuer SALCOS auf 1,322 Milliarden Euro", RET, "high",
  "Original ministry page (mw.niedersachsen.de) showed a maintenance page on 2026-10-22; figure confirmed by the company's own slide deck."],
 ["F17", "SALCOS", "Granted versus paid out", "n/a",
  "committed about 1.3 bn; paid 1,076 between 2023 and 30 Jun 2026 (company); H1 2026 additional committed funds received: 290",
  "EUR m", "2026-06-30", "Bund + Niedersachsen", "verified", "Company interim report",
  "Salzgitter AG Zwischenbericht 1. Halbjahr 2026",
  "https://www.salzgitter-ag.com/fileadmin/finanzberichte/2026/h1/de/downloads/szag-h1-2026-de.pdf",
  "PDF p. 16 (Finanz- und Vermoegenslage)",
  "seit 2023 ... in Summe 1.076 Mio. EUR gezahlt", RET, "high",
  "Payout depends on investments made (pro rata)."],
 ["F18", "SALCOS", "Status and timing", "first stage 2027?",
  "commissioning planned H1 2027 (Mar 2026); green steel from new route offered from summer 2027 (Aug 2026 report); decision on further stages 2028/29; completion mid-2030s; earlier plans: end 2025 (Apr 2023), 2026 (EC 2022)",
  "year", "2026-08-10", "n/a", "verified: first stage slipped to 2027; later stages delayed", "Company reports",
  "Salzgitter JPK 2026 slide 5; H1 2026 report",
  "https://www.salzgitter-ag.com/fileadmin/finanzberichte/2026/h1/de/downloads/szag-h1-2026-de.pdf",
  "H1 2026 PDF p. 9", "Ab Sommer 2027 soll erstmals gruener Stahl ... angeboten werden", RET, "high",
  "Hydrogen: EWE contract (Jun 2026) about 10,000 t/yr from 2030 = about 6.5% of expected need (H1 2026 report); plant to use natural gas at the start (trade press)."],
 ["F19", "Klimaschutzvertraege (CCfD)", "Scheme size and design now", "EUR 5 bn scheme, 15-year contracts, 60%/90% thresholds",
  "EUR 5 bn; two-way CfD, 15 years; emission cuts at least 50% within four years and 85% by the end of the 15-year contract; replaces the March 2025 version (60%/90%)",
  "text", "2026-05-07", "Bund; PtJ administers", "partly outdated: thresholds changed",
  "European Commission press release", "IP/26/997 (SA.122980)", EC + "ip_26_997",
  "IP/26/997 paragraphs 'The German scheme'", "at least 50% within four years and 85% by the end of the contract period", RET, "high",
  "See ccfd_scheme_versions.csv for the Feb 2024, Mar 2025 and May 2026 decisions."],
 ["F20", "Klimaschutzvertraege (CCfD)", "Round 1 outcome", "n/a",
  "17 bids, 15 awarded; contracts signed Oct 2024; maximum funding up to 2,800; paid in arrears; about 17 Mt CO2e over 15 years", "EUR m",
  "2025-05-26", "Bund", "verified", "Bundesregierung (BMWE answer)",
  "Bundestag Drucksache 21/283", "https://dserver.bundestag.de/btd/21/002/2100283.pdf", "pp. 2, 3, 5 (q.1, 4, 5, 9)",
  "maximalen Foerdervolumen in Hoehe von bis zu 2,8 Mrd. Euro", RET, "high",
  "Nothing is paid before projects start ('nachschuessig'), so granted versus paid is zero-to-small."],
 ["F21", "Klimaschutzvertraege (CCfD)", "Round 2 status", "n/a",
  "bidding opened 5 May 2026; deadline for bids ended 9 Sep 2026; awards expected Nov/Dec 2026 (no results as of 22 Oct 2026); min aid above 15 m, max 2,500 per project, min 5 kt CO2 per year",
  "text", "2026-10-22", "Bund", "verified (awards pending)", "Federal funding database (BMWE) and chamber notice",
  "Foerderdatenbank entry; IHK Bonn notice 8 May 2026",
  "https://www.foerderdatenbank.de/FDB/Content/DE/Foerderprogramm/Bund/BMWi/co2-arme-produktionsverfahren.html",
  "Verfahrensablauf, Fristen, rechtliche Voraussetzungen; Richtlinie BAnz AT 08.05.2026 B2",
  "Die Frist ... endete mit Ablauf des 09.09.2026", RET, "high",
  "Award timing 'Nov/Dec' comes from the IHK notice (medium). Programme now branded 'CO2-Differenzvertraege'."],
 ["F22", "Klimaschutzvertraege (CCfD)", "Not combinable with IPCEI hydrogen aid", "n/a",
  "projects can use CCfD or IPCEI-hydrogen aid, not both; so tkH2Steel and SALCOS are not CCfD beneficiaries", "text",
  "2026-10-22", "n/a", "verified", "Bundesregierung; Foerderdatenbank",
  "Drs 20/12166 q.22 (p. 9); Foerderdatenbank CCfD entry",
  "https://dserver.bundestag.de/btd/20/121/2012166.pdf", "Drs 20/12166 p. 9",
  "Projekte koennen nur mit einer der beiden Foerdervarianten umgesetzt werden", RET, "high",
  "Matters for S9/A11: do not present CCfD as a source of the flagship aid."],
 ["F23", "DRI-EAF programme", "Commitments EUR 6.9 bn", "about EUR 6.9 bn public support",
  "Foerderzusagen of about 6,900 for SALCOS (1,000), tkH2Steel (2,000), Power4Steel (2,600), DRIBE2 (1,300) as at 2 Jul 2024", "EUR m",
  "2024-07-02", "Bund + Laender (IPCEI part: Laender 30%)", "verified as a 2024 commitment total; now outdated",
  "Bundesregierung (BMWK answer)", "Bundestag Drucksache 20/12166",
  "https://dserver.bundestag.de/btd/20/121/2012166.pdf", "p. 10 (q.23-25); components p. 9 (q.18-20)",
  "Foerderzusagen von rund 6,9 Mrd. Euro", RET, "high",
  "ArcelorMittal (DRIBE2, 1,300) stopped its German DRI plans on 19-20 Jun 2025; SALCOS +322 in 2026. Live total about 5,922 (checks_output.csv)."],
 ["F24", "DRI-EAF programme", "Total project cost EUR 12.5 bn", "nearly EUR 12.5 bn total cost",
  "NOT verified in a primary source. OSW (Sep 2025) states it without a source. Primary component totals found: ArcelorMittal about 2,500 (company), SHS Power4Steel about 3,500 (Saarland ministry), thyssenkrupp about 3,000 (company/BMWK, now reported higher), Salzgitter stage 1 about 2,000-2,700 (company, trade press) = about 11,000-11,700",
  "EUR m", "2025-09-17", "n/a", "UNRESOLVED", "Think-tank commentary; company; Land ministry",
  "OSW Commentary 'A fragile future'; ArcelorMittal Europe release 5 Feb 2024; Saarland ministry page",
  "https://www.osw.waw.pl/en/publikacje/osw-commentary/2025-09-17/a-fragile-future-decarbonisation-germanys-steel-sector",
  "OSW paragraph on four projects and footnote 8 (footnote gives no source for 12.5)",
  "against total costs amounting to nearly 12.5 billion", RET, "low",
  "A single search summary mentioned 4.6 bn for Power4Steel from a procurement notice; the notice returned 404 when opened, so it is not used."],
 ["F25", "DRI-EAF programme", "Capacity 11.5 Mt per year", "11.5 Mt per year low-emission steel, one-third of blast-furnace capacity",
  "Bundesregierung: 'ueber 11 Mt' per year and up to 17 Mt CO2 saved per year; EC capacities sum to 11.05 Mt (tk 2.3 hot metal + Salzgitter 1.9 + SHS 3.05 + ArcelorMittal 3.8); without ArcelorMittal 7.25 Mt; government planning: about one-third of German crude steel converted by 2030",
  "Mt per year", "2024-07-02", "n/a", "partly verified ('over 11 Mt', not 11.5)", "Bundesregierung; European Commission",
  "Drs 20/12166 pp. 3 and 5; IP/22/5968, IP/23/3928, IP/23/6647, IP/24/1009",
  "https://dserver.bundestag.de/btd/20/121/2012166.pdf", "Drs 20/12166 p. 3 (q.1), p. 5 (q.8)",
  "ueber 11 Millionen Tonnen pro Jahr", RET, "medium",
  "Mixes hot metal (tk) and crude steel (others)."],
 ["F26", "Power4Steel (SHS)", "Grant", "n/a", "2,600 direct grant; 3.05 Mt crude steel per year; Saarland says total investment about 3,500, start 2028/29", "EUR m",
  "2023-12-19", "Bund + Saarland (30%)", "verified", "European Commission; Saarland ministry; Bundesregierung",
  "IP/23/6647 (SA.105337); saarland.de H2 industry page; Drs 20/12166",
  EC + "ip_23_6647", "IP/23/6647; Saarland page paragraph on SHS", "Gesamtinvestitionskosten von rund 3,5 Mrd. Euro", RET, "high",
  "Financing package about 1.7 bn finalised Oct 2025 (trade press)."],
 ["F27", "DRIBE2 (ArcelorMittal)", "Grant and exit", "n/a",
  "1,300 approved 23 Feb 2024 (SA.104898); total project about 2,500; company stopped DRI/EAF plans 19 Jun 2025; state aid not used", "EUR m",
  "2025-06-20", "Bund (partly RRF) + Bremen about 250", "verified", "European Commission; company; dpa",
  "IP/24/1009; ArcelorMittal Europe release 5 Feb 2024; dpa-AFX 20 Jun 2025",
  EC + "ip_24_1009", "IP/24/1009", "the investments could not be continued (dpa)", RET, "high", ""],
 ["F28", "Industriestrompreis", "Decision and design", "n/a",
  "EC approved 16 Apr 2026 (SA.120495), budget EUR 3.8 bn, 1 Jan 2026 to 31 Dec 2028; relief up to 50% of 1-year-future reference with floor 5 ct/kWh, for 50% of consumption; example 2026 reference about 8.75 ct gives about 3.75 ct/kWh; 50% of aid to be invested in decarbonisation within 48 months; first applications early 2027 for 2026; BAFA; not combinable with Strompreiskompensation on the same kWh",
  "EUR m / ct per kWh", "2026-04-16", "Bund; BAFA pays", "verified",
  "BMWE press paper; European Commission press release",
  "BMWE Pressepapier zum Industriestrompreis 16 Apr 2026; IP/26/815",
  "https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Downloads/P-R/pressepapier-zum-industriestrompreis.pdf?__blob=publicationFile&v=6",
  "BMWE paper pp. 1-3; IP/26/815", "Die Laufzeit ... betraegt drei Abrechnungsjahre (2026 - 2028)", RET, "high",
  "The paper's list of main beneficiary branches does not name iron and steel; eligibility of steel NACE codes and the Richtlinie annex were not checked. The scheme is called 'Industriestrompreis', not 'Brueckenstrompreis'."],
 ["F29", "Hydrogen package", "BMWE 10 measures (19 Oct 2026)", "n/a",
  "new hydrogen window in the CCfD programme with at least EUR 1.5 bn (from the 2027 round); CCfD planned up to EUR 8.7 bn in total",
  "EUR m", "2026-10-19", "Bund", "partly verified (page blocked)", "BMWE press release (seen via search snippet) and trade press",
  "BMWE press release 19 Oct 2026; Cleanthinking 20 Oct 2026",
  "https://www.cleanthinking.de/wasserstoff-industrie-klimaschutzvertraege-reiche/",
  "n/a (BMWE page returned a Radware challenge)", "Wasserstoff-Fenster ... mindestens 1,5 Mrd. EUR", RET, "medium",
  "The BMWE page itself could not be opened; do not quote the 8.7 bn without re-checking."],
]
write("verified_facts.csv", H, F)

# ---------------------------------------------------------------- discrepancies
D = [
 ["D01", "BaseNotes-1 line 701", "Thyssenkrupp 'targets full hydrogen operation by 2029'",
  "2029 is a company target from Jul 2023 / Feb 2024 (first hydrogen 2028). The EC decision text says renewable-only operation as of 2037 and natural gas first. In Aug 2026 the funding rules were relaxed because hydrogen is not available; the plant will run longer on gas.",
  "F06, F07, F08", "high", "Replace with 'commissioning 2027 on natural gas; hydrogen ramp-up delayed; no firm full-hydrogen date'."],
 ["D02", "research brief lines 127 and 130 vs BaseNotes-1", "VW MoU (commissioning from 2027, gas first, supply 2028) vs '2029 full hydrogen'",
  "Not a date contradiction: 2027 = commissioning on gas, 2028 = first deliveries and first hydrogen (Feb 2024 plan), 2029 = end of hydrogen ramp-up (Feb 2024 plan). But 2029 is now stale (D01), and the MoU release itself says hydrogen is phased in gradually.",
  "F07, F09", "high", "Keep the MoU dates; drop 2029 or label it 'company target of Feb 2024, since delayed'."],
 ["D03", "BaseNotes-1 line 651; S9 footer", "SALCOS EUR 1 bn direct grant",
  "EUR 1 bn was the Oct 2022 approval and Apr 2023 Bescheid. Since Feb 2026 public funding is about EUR 1.322 bn (+322). About EUR 1,076 m had been paid by 30 Jun 2026.",
  "F14, F16, F17", "high", "Use 'about EUR 1.3 bn (EUR 1 bn at approval, topped up Feb 2026)'."],
 ["D04", "BaseNotes-1 line 659-662", "Klimaschutzvertraege: EUR 5 bn, 15 years, 60% / 90% thresholds",
  "EUR 5 bn and 15 years still hold, but 60% in three years / 90% belongs to the Feb 2024 and Mar 2025 versions. The scheme approved 7 May 2026 (SA.122980) requires at least 50% within four years and 85% at the end. Round 2 closed 9 Sep 2026; awards pending.",
  "F19, F21, ccfd_scheme_versions.csv", "high", "Update thresholds; say 'round 2 awards expected Nov/Dec 2026'."],
 ["D05", "BaseNotes-1 line 649-651", "Flagship aid framed as IPCEI hydrogen aid",
  "The Commission says both projects were selected in the 2021 IPCEI open call but assessed under the 2022 CEEAG (Art. 107(3)(c) TFEU), not under the IPCEI Communication. The German government still calls them 'IPCEI Wasserstoff' projects and pays 30% via the Laender.",
  "F01, F14, F23", "high", "Wording: 'selected through the IPCEI call, approved as State aid under CEEAG'."],
 ["D06", "BaseNotes-1 line 649", "tkH2Steel = EUR 550 m grant + up to EUR 1.45 bn conditional payment 'for the first ten years'",
  "Verified in the EC text. But group-level grant receipts reported by thyssenkrupp (about EUR 1.0 bn FY23/24 to 9M FY25/26) already exceed EUR 550 m; the Bundesregierung says IPCEI-type aid is paid out early pro rata to eligible investment costs. So the 550 / 1,450 split describes the legal form, not the cash timing.",
  "F01, F02, F11", "medium", "Do not show the 1.45 bn as 'paid over ten years'. Say 'committed EUR ~2 bn; about half received by mid-2026 (company data)'."],
 ["D07", "BaseNotes-3 / workbook line 807", "EUR 6.9 bn public support for DRI-EAF projects",
  "6.9 bn is a Foerderzusagen total (commitments) as at 2 Jul 2024, including ArcelorMittal EUR 1.3 bn which was not used after the Jun 2025 exit, and excluding SALCOS +322. Live commitments about EUR 5.9 bn (SALCOS 1,322 + tkH2Steel 2,000 + Power4Steel 2,600).",
  "F23, F27, F16", "high", "State as 'commitments, not payments'; give the 2024 figure with its date and the current 5.9 bn."],
 ["D08", "workbook line 807", "'nearly EUR 12.5 bn total project costs' and '11.5 Mt per year'",
  "Both rest on one think-tank commentary. Bundesregierung says 'over 11 Mt'. EC capacities add to 11.05 Mt. Primary component cost totals add to about EUR 11.0-11.7 bn including ArcelorMittal's withdrawn EUR 2.5 bn.",
  "F24, F25", "low", "Mark as unverified; if used, cite OSW (Sep 2025) as secondary and say 'about'."],
 ["D09", "BaseNotes-1 line 701", "'BMWK and NRW supporting the plant and hydrogen ramp-up'",
  "BMWK is now BMWE. The funding Bescheid was issued 27 Jul 2023 for 'construction and operation'; the hydrogen element is being renegotiated (D01).",
  "F03, F08", "medium", "Use BMWE; avoid implying hydrogen ramp-up funding is secure."],
 ["D10", "BaseNotes-1 line 659-665", "Steel projects 'eligible' for Klimaschutzvertraege",
  "True in principle (EC text), but IPCEI-hydrogen aid and CCfD cannot be combined, so the two flagship projects do not hold CCfDs. Round-1 winners were not checked for steel.",
  "F22", "high", "Do not attribute flagship funding to CCfD."],
]
write("discrepancies_vs_workbook.csv",
      ["id", "workbook_location", "workbook_statement", "finding", "fact_ids", "confidence", "suggested_fix"], D)

# ---------------------------------------------------------------- timeline
T = [
 ["2021", "IPCEI hydrogen open call in Germany; SALCOS and tkH2Steel selected", "EC IP/22/5968; IP/23/3928", "high"],
 ["2022-10-04", "EC approves EUR 1 bn aid for Salzgitter (SALCOS); start envisioned 2026", "IP/22/5968 (SA.104276)", "high"],
 ["2022-09-15", "Bund and Lower Saxony sign administrative agreement on joint SALCOS funding", "Salzgitter release 18 Apr 2023", "high"],
 ["2023-04-18", "SALCOS Foerderbescheid handed over (about EUR 1 bn; Bund 70% / Land 30%)", "PtJ; Salzgitter AG", "high"],
 ["2023-07-20", "EC approves up to EUR 550 m grant + up to EUR 1.45 bn conditional payment for tkH2Steel; renewable-only from 2037", "IP/23/3928 (SA.105244)", "high"],
 ["2023-07-26", "Federal commitment (about EUR 2 bn) confirmed at Duisburg event; NRW up to EUR 700 m", "thyssenkrupp Steel release", "high"],
 ["2023-07-27", "BMWE Bescheid for tkH2Steel (knapp EUR 2 bn)", "Drs 21/7837 q.58", "high"],
 ["2023-10-01", "CBAM reporting period starts (for context: all aid decisions above pre-date it)", "workbook U3", "high"],
 ["2023-12-19", "EC approves EUR 2.6 bn aid for SHS (Power4Steel)", "IP/23/6647", "high"],
 ["2024-02-16", "EC approves EUR 4 bn Klimaschutzvertraege scheme (partly RRF); thyssenkrupp launches hydrogen tender (first H2 2028, full 2029)", "IP/24/845; tk release", "high"],
 ["2024-02-23", "EC approves EUR 1.3 bn aid for ArcelorMittal (DRIBE2)", "IP/24/1009", "high"],
 ["2024-10-15", "Round-1 Klimaschutzvertraege signed: 15 contracts, up to EUR 2.8 bn", "Drs 21/283; search metadata", "high"],
 ["2024-10-22", "thyssenkrupp-VW MoU: DR plant commissioning 2027 (gas first), deliveries 2028", "tk release", "high"],
 ["2025-03-24", "EC approves redesigned EUR 5 bn Klimaschutzvertraege scheme (60%/90%)", "IP/25/846 (SA.116065)", "high"],
 ["2025-06-19", "ArcelorMittal stops German DRI/EAF plans; EUR 1.3 bn aid not used", "dpa-AFX 20 Jun 2025; OSW", "high"],
 ["2025-09", "Salzgitter postpones later SALCOS stages; investment decision on further stages now 2028/29 (date of the postponement from S&P Global and Eurometal headlines seen in search results only; the 2028/29 wording is in the company report)", "Salzgitter H1 2026 report PDF p. 9 (2028/29); headline date not verified", "medium"],
 ["2026-02-06", "EC approves SALCOS supplementary aid (EUR +322 m)", "h2-news (secondary)", "medium"],
 ["2026-02-23", "Lower Saxony announces SALCOS public funding EUR 1.322 bn", "dpa via OLZ", "high"],
 ["2026-04-16", "EC approves German Industriestrompreis (EUR 3.8 bn, 2026-2028); BMWE press paper", "IP/26/815; BMWE", "high"],
 ["2026-04-23", "NRW ministry reports EC is examining an adjustment of the tkH2Steel approval", "Vorlage 18/5029", "high"],
 ["2026-05-05", "Klimaschutzvertraege round 2 (Gebotsverfahren 2026) opens", "Foerderdatenbank", "high"],
 ["2026-05-07", "EC approves redesigned EUR 5 bn scheme (50%/85%); replaces Mar 2025 scheme", "IP/26/997 (SA.122980)", "high"],
 ["2026-06", "Salzgitter-EWE hydrogen contract: about 10,000 t/yr from 2030", "Salzgitter H1 2026 report", "high"],
 ["2026-08-13", "thyssenkrupp 9M results; CFO says EC approved amended funding rules (hydrogen requirement relaxed)", "Reuters via EUToday/Eurometal", "medium"],
 ["2026-09-09", "Round-2 bid deadline", "Foerderdatenbank", "high"],
 ["2026-09-24", "Trade press: hydrogen switch delayed, plant to run longer on gas", "Gasworld", "medium"],
 ["2026-10-19", "BMWE 10-point hydrogen package: hydrogen window of at least EUR 1.5 bn in CCfD from 2027", "BMWE (blocked) / Cleanthinking", "medium"],
 ["2026-11/12", "Round-2 awards expected", "IHK Bonn", "medium"],
 ["2027", "tkH2Steel DR plant commissioning starts (end 2027 per plant manager); SALCOS stage 1 green steel from summer 2027; CBAM certificate sales 1 Feb 2027", "tk site; Ingenieur.de; Salzgitter H1 2026", "medium"],
]
write("timeline_dated_events.csv", ["date", "event", "source", "confidence"], T)

# ---------------------------------------------------------------- commitments vs payments
C = [
 ["tkH2Steel", "Commitment (Bescheid)", "knapp 2,000", "EUR m", "2023-07-27", "BMWE; NRW 30% (or up to 700)", "Drs 21/7837 p. 39", "high"],
 ["tkH2Steel", "Group 'Proceeds from government grants' FY22/23", "154", "EUR m", "2023-09-30", "not tkH2Steel-specific", "tk AR 2023/24 PDF p. 183", "medium"],
 ["tkH2Steel", "Group 'Proceeds from government grants' FY23/24", "417", "EUR m", "2024-09-30", "mainly DR plant per company text", "tk AR 2023/24 PDF p. 183", "medium"],
 ["tkH2Steel", "Group 'Proceeds from government grants' FY24/25", "346", "EUR m", "2025-09-30", "mainly DR plant per company text", "tk AR 2024/25 PDF p. 232", "medium"],
 ["tkH2Steel", "9M FY24/25 grant payments", "205", "EUR m", "2025-06-30", "DR plant", "tk 9M 2025/26 PDF p. 41", "high"],
 ["tkH2Steel", "9M FY25/26 grant payments", "252", "EUR m", "2026-06-30", "DR plant", "tk 9M 2025/26 PDF p. 41 and Facts&Figures", "high"],
 ["tkH2Steel", "Purchase commitment for DR plant outstanding", "1,039 (1,091 at 30 Sep 2025)", "EUR m", "2026-06-30", "partly covered by Bund/NRW grants", "tk 9M 2025/26 PDF p. 41", "high"],
 ["tkH2Steel", "NRW share paid by Oct 2024", "'hoher zweistelliger Millionenbetrag'", "text", "2024-10-10", "Land NRW", "APr 18/703 PDF p. 10", "medium"],
 ["SALCOS", "Commitment at approval (Bescheid)", "about 1,000 (700 Bund + 300 Land)", "EUR m", "2023-04-18", "Bund 70% / Niedersachsen 30%", "PtJ; Salzgitter release", "high"],
 ["SALCOS", "Commitment after top-up", "about 1,322 (+322)", "EUR m", "2026-02-23", "Bund 2/3, Land 1/3 of the addition", "dpa; Salzgitter JPK 2026", "high"],
 ["SALCOS", "Paid out 2023 to 30 Jun 2026", "1,076", "EUR m", "2026-06-30", "paid as investments are made", "Salzgitter H1 2026 PDF p. 16", "high"],
 ["SALCOS", "Additional committed funds received in H1 2026", "290", "EUR m", "2026-06-30", "", "Salzgitter H1 2026 PDF p. 16", "high"],
 ["Klimaschutzvertraege R1", "Contracts signed", "up to 2,800 (15 contracts)", "EUR m", "2024-10", "Bund; paid in arrears", "Drs 21/283 p. 3", "high"],
 ["Klimaschutzvertraege R1", "Paid out", "not published; payments only start after project start", "text", "2025-05-26", "", "Drs 21/283 p. 3 and 5 (q.5, q.12)", "high"],
 ["Klimaschutzvertraege R2", "Budget", "up to 5,000", "EUR m", "2026-05-07", "Bund", "IP/26/997; IHK Bonn", "high"],
 ["Federal payout status per project", "Bund disclosure", "classified VS-Vertraulich", "text", "2026-01-08", "", "Drs 21/3563 p. 6", "high"],
]
write("commitments_vs_payments.csv",
      ["project", "measure", "value", "unit", "as_of", "funder_or_note", "source_and_page", "confidence"], C)

# ---------------------------------------------------------------- CCfD versions
V = [
 ["IP/24/845", "2024-02-16", "SA.104880", "4,000 (partly RRF)", "60% within 3 years; 90% within 15 years", "15 years", "Two-way CfD 'Climate Protection Contracts'", "Round 1 (2024)", EC + "ip_24_845"],
 ["IP/25/846", "2025-03-24", "SA.116065", "5,000", "60% within 3 years; 90% by end of supported project", "15 years", "Replaced in 2026 (not implemented in that form)", "planned for round 2", EC + "ip_25_846"],
 ["IP/26/997", "2026-05-07", "SA.122980", "5,000", "at least 50% within 4 years; 85% by end of 15-year contract", "15 years", "Current scheme; CCS/CCU, industrial steam allowed", "Round 2 (Gebotsverfahren 2026)", EC + "ip_26_997"],
]
write("ccfd_scheme_versions.csv",
      ["ec_press_release", "date", "sa_number", "budget_eur_m", "emission_reduction_requirement", "duration", "notes", "applies_to", "url"], V)

# ---------------------------------------------------------------- access log
A = [
 ["ec.europa.eu presscorner API (reference=IP/..)", "worked", "Used for IP/22/5968, 23/3928, 23/6647, 24/845, 24/1009, 25/846, 26/815, 26/997"],
 ["dserver.bundestag.de (Drucksachen)", "worked", "20/12166, 21/283, 21/3563, 21/7837"],
 ["landtag.nrw.de (Vorlage, Ausschussprotokoll)", "worked", "MMV18-5029, MMA18-703"],
 ["ptj.de", "worked", "SALCOS news 18 Apr 2023"],
 ["foerderdatenbank.de", "worked", "CCfD programme entry"],
 ["ucpcdn.thyssenkrupp.com, thyssenkrupp-steel.com, transformation.thyssenkrupp-steel.com", "worked", "Company reports and releases"],
 ["www.thyssenkrupp.com (HTML)", "connection reset from this machine", "Used ucpcdn PDFs instead"],
 ["salzgitter-ag.com", "worked", "JPK 2026 slides, H1 2026 report, 2023 release"],
 ["bundeswirtschaftsministerium.de / bmwk.de HTML pages", "BLOCKED: Radware 'Verifying your browser' challenge; not bypassed",
  "Press releases of 26 Jul 2023, 18 Apr 2023, 5 May 2026, 19 Oct 2026 could not be opened. A PDF under /Downloads/ (Industriestrompreis press paper) was served normally"],
 ["eur-lex.europa.eu (OJ C/2025/4871 for SA.105244)", "BLOCKED: HTTP 202 JavaScript challenge; not bypassed", "Case number SA.105244 taken from the EC press release instead"],
 ["competition-cases.ec.europa.eu", "JavaScript application, no text returned", "State aid register not read"],
 ["land.nrw, wirtschaft.nrw, klimaschutzvertraege.info, co2-differenzvertraege.info", "connection refused or reset from this machine", "Used Landtag documents and Foerderdatenbank instead"],
 ["mw.niedersachsen.de", "maintenance page returned", "SALCOS top-up taken from dpa text and company slides"],
 ["reuters.com", "not accessible to the search tool", "Aug 2026 funding amendment known only through EUToday, Eurometal, GMK, Gasworld"],
 ["KfW", "no KfW financing of the two flagships found in a search", "Company loans are export-credit-agency covered (SACE, OeKB) per search summary; not verified"],
]
write("access_log.csv", ["source", "result", "note"], A)

# ---------------------------------------------------------------- checks (arithmetic only)
checks = []


def chk(name, expr_value, comment):
    checks.append([name, expr_value, comment])


chk("tk EC split: 550 + 1450", 550 + 1450, "EUR m; equals 'about 2 bn'")
chk("NRW 30% of 2000", round(0.30 * 2000, 1), "EUR m; vs 'up to 700' (35%)")
chk("Bund share if NRW=700", 2000 - 700, "EUR m")
chk("Bund share if NRW=30%", 2000 - 600, "EUR m")
chk("Commitments 2024: 1000+2000+2600+1300", 1000 + 2000 + 2600 + 1300, "EUR m; equals 6.9 bn in Drs 20/12166")
chk("Live commitments: 1322+2000+2600", 1322 + 2000 + 2600, "EUR m; after ArcelorMittal exit and SALCOS top-up")
chk("EC capacity sum incl. ArcelorMittal (2.3+1.9+3.05+3.8)", round(2.3 + 1.9 + 3.05 + 3.8, 2), "Mt/yr; mixes hot metal and crude steel")
chk("EC capacity sum excl. ArcelorMittal", round(2.3 + 1.9 + 3.05, 2), "Mt/yr")
chk("Company cost totals low: SALCOS 2000 + tk 3000 + SHS 3500 + AM 2500", 2000 + 3000 + 3500 + 2500, "EUR m; vs 12,500 in workbook")
chk("Company cost totals high: SALCOS 2700 + tk 3000 + SHS 3500 + AM 2500", 2700 + 3000 + 3500 + 2500, "EUR m")
chk("Live cost totals low (no AM)", 2000 + 3000 + 3500, "EUR m")
chk("Live cost totals high (no AM)", 2700 + 3000 + 3500, "EUR m")
chk("Public share of live cost (5922 / 9200)", round(5922 / 9200, 3), "ratio, upper-cost case")
chk("Public share of live cost (5922 / 8500)", round(5922 / 8500, 3), "ratio, lower-cost case")
chk("SALCOS paid / committed 1.3bn", round(1076 / 1300, 3), "ratio")
chk("SALCOS paid / committed 1.322bn", round(1076 / 1322, 3), "ratio")
chk("SALCOS Bund share after top-up (700 + 2/3*322)", round(700 + 2 / 3 * 322, 1), "EUR m; assumes 2/3 applies to the addition only")
chk("SALCOS Land share after top-up (300 + 1/3*322)", round(300 + 1 / 3 * 322, 1), "EUR m; same assumption")
chk("tk grants FY23/24 + FY24/25 + 9M FY25/26", 417 + 346 + 252, "EUR m; group cash-flow line")
chk("tk grants incl. FY22/23", 154 + 417 + 346 + 252, "EUR m; FY22/23 pre-dates the Bescheid, likely other items")
chk("tk grants received / 2000 commitment", round((417 + 346 + 252) / 2000, 3), "ratio; indicative only")
chk("CCfD R1 awarded / R1 budget (2.8 / 4.0)", round(2.8 / 4.0, 3), "ratio")
chk("Industriestrompreis relief: 8.75 - 5.00", round(8.75 - 5.0, 2), "ct/kWh; matches 3.75 in BMWE paper")
write("checks_output.csv", ["check", "value", "comment"], checks)
