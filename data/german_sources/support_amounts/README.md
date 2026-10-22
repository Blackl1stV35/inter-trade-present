# German public-support amounts for steel decarbonisation: verification

Retrieved 2026-10-22. Scope: the support amounts quoted in workbook BaseNotes-1 (lines 645-702 and 807 of `sources/text/inter-trade-present-base.txt`) for tkH2Steel (Thyssenkrupp Steel, Duisburg), SALCOS (Salzgitter), the Klimaschutzvertraege (carbon contracts for difference, CCfD) and the DRI-EAF programme total, plus the latest project and policy status.

Status: partial. Most figures are verified in German government or European Commission primary documents. Two workbook figures (total project cost of about EUR 12.5 bn, 11.5 Mt per year) could not be verified. Federal payout figures per project are not public (classified), so "paid out" comes from company reports.

## Verdicts at a glance

| Workbook claim | Verdict | Where |
| --- | --- | --- |
| tkH2Steel: EUR 550 m direct grant + up to EUR 1.45 bn conditional payment for the first ten years (about EUR 2 bn) | Verified (EC IP/23/3928, 20 Jul 2023, SA.105244). BMWE confirms "knapp 2 Mrd" approved 27 Jul 2023, Bund + NRW | F01-F05 |
| Thyssenkrupp "full hydrogen operation by 2029" | Company target of Jul 2023 / Feb 2024, now stale. Plant starts on natural gas, funding rules relaxed Aug 2026. EC decision text says renewable-only from 2037 | F06-F09, D01-D02 |
| SALCOS: EUR 1 bn direct grant, DRI plant + EAF + 100 MW electrolyser | Verified for 2022/2023 (EC IP/22/5968, SA.104276). Outdated: topped up by EUR 322 m to about EUR 1.322 bn in Feb 2026 | F14-F18, D03 |
| Klimaschutzvertraege: EUR 5 bn, 15 years, 60% / 90% thresholds | EUR 5 bn and 15 years hold. 60% / 90% belongs to the Feb 2024 / Mar 2025 versions. Current scheme (EC 7 May 2026, SA.122980): at least 50% within 4 years, 85% at end | F19-F22, D04, `ccfd_scheme_versions.csv` |
| DRI-EAF: about EUR 6.9 bn public support against about EUR 12.5 bn cost for 11.5 Mt per year | 6.9 bn verified as commitments at 2 Jul 2024 (Bundesregierung, Drs 20/12166 p. 10) but includes ArcelorMittal EUR 1.3 bn that was dropped in Jun 2025. Live total about EUR 5.9 bn. 12.5 bn and 11.5 Mt not verified ("over 11 Mt" in the government answer) | F23-F27, D07-D08 |

## Granted versus paid

- SALCOS: committed about EUR 1.3 bn; EUR 1,076 m paid 2023 to 30 Jun 2026 (Salzgitter H1 2026 report, PDF p. 16). Funding is paid as investments are made.
- tkH2Steel: committed knapp EUR 2 bn. The Bund does not publish payouts. Thyssenkrupp reports "proceeds from government grants" of EUR 417 m (FY23/24), EUR 346 m (FY24/25) and EUR 252 m (9M FY25/26); the three sum to EUR 1,015 m. These are group-level cash-flow lines (the 9M figure is explicitly for the direct reduction plant), so treat the sum as indicative. NRW said in Oct 2024 that a "high two-digit million" sum had flowed.
- Because receipts already exceed the EUR 550 m "direct grant", the legal split (grant versus conditional payment) is not the cash timing. The Bundesregierung says IPCEI-type aid is paid out early, pro rata to eligible investment costs (Drs 20/12166 p. 9).
- Klimaschutzvertraege: paid in arrears after project start (Drs 21/283). Round 1: 15 contracts, up to EUR 2.8 bn. Round 2: bids closed 9 Sep 2026, awards expected Nov/Dec 2026.
- The two flagships do not hold CCfDs: IPCEI-hydrogen aid and CCfD cannot be combined.

## Who funds

- tkH2Steel: Bund (BMWK, now BMWE) and Land NRW. BMWE says NRW co-finances 30%; the company and NRW cite "up to EUR 700 m". Both are in `verified_facts.csv` (F04).
- SALCOS: about EUR 700 m Bund and EUR 300 m Lower Saxony at approval (70/30). The EUR 322 m top-up is split Bund two-thirds, Land one-third (derived Bund about EUR 915 m, Land about EUR 407 m; `checks_output.csv`).
- Project agency: Projekttraeger Juelich (PtJ) handles the national side of the IPCEI-hydrogen projects and the CCfD programme. BAFA administers the Industriestrompreis. No KfW financing of the two flagships was found.

## Latest status (to 2026-10-22)

- tkH2Steel: construction under way (DR tower, smelters nearly pre-assembled, Jun 2026). Commissioning "starts 2027" (company), end 2027 per plant manager. Gas first. Funding rules amended after the Commission agreed in Aug 2026 (reported via Reuters); Germany must still adjust the Bescheid. Source quality for the amendment is trade press: medium confidence.
- SALCOS: stage 1 slipped from end 2025 to 2027; green steel offered from summer 2027; decision on further stages 2028/29; completion mid-2030s.
- 2026 policy changes: SALCOS top-up (Feb), Industriestrompreis approved 16 Apr (EUR 3.8 bn, 2026-2028, floor 5 ct/kWh, 50% of consumption), CCfD scheme redesigned 7 May and round 2 run May-Sep, BMWE hydrogen package 19 Oct (hydrogen window of at least EUR 1.5 bn in CCfD from 2027; BMWE page blocked, so medium confidence).

## Queries and method

Searches (English and German) for: tkH2Steel and SALCOS State-aid decisions; Foerderbescheid dates and Bund/Land splits; Bundestag answers on Stahl-Foerderung and Klimaschutzvertraege; Auszahlung / Mittelabfluss; thyssenkrupp and Salzgitter 2026 reports; Industriestrompreis; second CCfD round. Primary documents were downloaded to a scratch directory outside this folder and read in full for the cited pages; only extracted facts, short quoted labels and page references are stored here.

Core primary documents (page refs are in `verified_facts.csv`): EC press releases IP/22/5968, IP/23/3928, IP/23/6647, IP/24/845, IP/24/1009, IP/25/846, IP/26/815, IP/26/997 (fetched through the EC press-corner API); Bundestag Drucksachen 20/12166, 21/283, 21/3563, 21/7837; NRW Landtag Vorlage 18/5029 and committee protocol APr 18/703; PtJ news of 18 Apr 2023; Foerderdatenbank CCfD entry; BMWE press paper on the Industriestrompreis (16 Apr 2026); thyssenkrupp annual reports 2023/24 and 2024/25 and interim report 9M 2025/26; Salzgitter annual press conference slides (23 Mar 2026) and H1 2026 report.

## Units and conversions

EUR million unless stated; "bn" = 1,000 EUR million. Mt = million tonnes per year. Dates ISO. German terms are transliterated (ae, oe, ue) in the CSVs to keep them ASCII-safe. "Foerderzusage / Bescheid" = commitment; "Auszahlung" = cash paid. Hot metal (thyssenkrupp, EC) and crude steel (others) are not the same measure; the 11.05 Mt sum in `checks_output.csv` mixes them.

## Checks

`build_tables.py` writes all CSVs and recomputes the arithmetic into `checks_output.csv` (run: `python -I -X utf8 build_tables.py <this folder>`). Key results: 550 + 1,450 = 2,000; 1,000 + 2,000 + 2,600 + 1,300 = 6,900 (matches the government's 6.9 bn); live commitments 1,322 + 2,000 + 2,600 = 5,922; EC capacities 11.05 Mt (7.25 Mt without ArcelorMittal); company cost totals 11.0-11.7 bn (not 12.5 bn).

## Caveats

- Blocked or unreadable sources are listed in `access_log.csv`. BMWE/BMWK HTML pages sit behind a Radware browser check and EUR-Lex returned a JavaScript challenge; neither was bypassed. The BMWE hydrogen package (19 Oct 2026) and the 6 Feb 2026 EC approval of the SALCOS top-up are therefore known only through secondary reports.
- The 2026 thyssenkrupp funding amendment is reported by Reuters through EUToday, Eurometal, GMK and Gasworld; the CFO is Dr. Axel Hamann (GMK misspells "Gammann"). No Commission or BMWE text was opened. The new fuel conditions are not known.
- Total project costs (12.5 bn) have no primary source. Component totals: ArcelorMittal about 2.5 bn (company), SHS about 3.5 bn (Saarland ministry), thyssenkrupp about 3 bn (company, reported rising), Salzgitter stage 1 about 2.0-2.7 bn.
- Industriestrompreis: the BMWE paper's beneficiary list does not name iron and steel; whether primary steel NACE codes qualify, and the Richtlinie text (Bundesanzeiger 6 May 2026), were not checked.
- Round-1 CCfD winners were not listed (project sheets site unreachable), so a steel winner cannot be ruled out.

## Files

`verified_facts.csv` (29 facts with source, page, confidence), `discrepancies_vs_workbook.csv`, `timeline_dated_events.csv`, `commitments_vs_payments.csv`, `ccfd_scheme_versions.csv`, `access_log.csv`, `checks_output.csv`, `build_tables.py`.
