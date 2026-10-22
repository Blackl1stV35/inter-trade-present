# Inter Trade presentation — EU ETS and CBAM, Germany steel case

Group assignment for the International Trade course (slide deck + report, 20 pts).
Working title: *How EU ETS and CBAM Can Strengthen Europe's Long-Term Green Manufacturing Economy: The Case of Germany*.

This repository is a local archive of everything produced so far (saved 2026-10-22) plus the slide-deck outline.
The GitHub repository `Blackl1stV35/inter-trade-present` is **public** by the owner's decision (2026-10-22). Member names, student IDs, the group's Google Doc link and an email address in a script header were redacted from the files and the git history on 2026-10-22 (history rewritten and force-pushed); handles such as Member A, Member B, Member C and Member D remain.

## Layout

| Path | What it is |
| --- | --- |
| `sources/line-chat/line-inter-trade-chat.txt` | LINE group export, 2026-10-02 to 2026-10-22 (discussion, decisions, final confirm actions) |
| `sources/docx/inter-trade-present-base.docx` | Base research workbook (all tabs: main, "update", graph simulations, 5-topic notes, appendices) |
| `sources/docx/inter-trade-present-1-slide-draft-by-member-b.docx` | Member B's slide-structure draft (2026-10-22) + extra data request (German steel exports) |
| `sources/docx/inter-trade-present-2-revised-research-brief.docx` | The "update" tab: revised brief, 1995–2025 data, company cases, claim checks, sources U1–U35 |
| `sources/docx/inter-trade-present-3-five-topic-data-notes.docx` | Thai summary of the five data topics (subsidies, alternative supply, costs, trade data, jobs/GDP) |
| `sources/text/*.txt` | Plain-text dumps of the four .docx files (tables inlined) — regenerate with `scripts/extract_docx.py` |
| `sources/images/` | The six embedded graph-simulation figures from the base workbook, in document order |
| `notes/project-brief.md` | Assignment rules, team roles, deadlines, decision log, open items |
| `outline/final-outline-proposal.pdf` (source: `final-outline-proposal.md`) | **Final proposal** for the 15-minute talk: decisions, corrections found, 13 slides with charts, backup A1–A15, German-source results, open items, source list |
| `outline/slide-outline-15min.md` | First version of the outline (superseded by the final proposal) |
| `outline/workflow-run/` | Raw JSON from the run that produced it: three drafts, three judge reports, the synthesis, and the fact-check / audit / red-team reports |
| `data/` | Live data pulls and status checks of 22 Oct 2026 (Comext, Eurostat, Destatis, WV Stahl, SMARD, DEHSt/UBA, EEX, policy and company status), each folder with a README, tables and raw pages; `agent_reports/` holds each agent's structured result |
| `graphs/gnuplot/`, `graphs/out/` | gnuplot scripts and the rendered charts (Fig. 2 redraw, slides 6–8, backup A8); fonts: TH Sarabun New |
| `graphs/gephi/` | Gephi import files (nodes/edges CSV) for the company-case network, with build steps |
| `scripts/` | Helpers: .docx text/image extraction, `setup_tools.ps1` (project-local gnuplot + Gephi), `env.ps1`, `save.ps1` (commit + push loop), `build_pdf.py` (Markdown to PDF via Edge), `build_workbook_csv.py` |
| `tools/` | Git-ignored. Project-local gnuplot 6.0.5 and Gephi 0.11.3 created by `scripts/setup_tools.ps1` |

## Regenerating the text dumps

```bash
python -I scripts/extract_docx.py sources/text sources/docx/*.docx
python -I scripts/extract_media.py sources/docx/inter-trade-present-base.docx sources/images base-doc-fig
```

## Graph tools (project-local only)

gnuplot (charts and theory diagrams) and Gephi (company-case network) live in `tools/` inside this folder — no admin rights, nothing added to the system PATH.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_tools.ps1   # download, verify SHA-256, install into tools\
. scripts\env.ps1                                                  # this shell only: puts tools\gnuplot\bin on PATH
tools\run-gephi.cmd                                                # starts Gephi with its settings kept in tools\gephi-userdir
```

Downloads are pinned and checked: gnuplot `gp605-win64-mingw.7z` (SourceForge, SHA-256 from the published checksum file) and Gephi `gephi-0.11.3-windows-x64.exe` (GitHub release, SHA-256 `bf3f488a…`). The Gephi installer also writes one per-user uninstall entry in `HKCU`; `tools\gephi\unins000.exe` removes it. About 450 MB on disk.

## Not in this repo

The three lecture PDFs shared in the chat on 2026-10-07 (Export Policy, Offshoring of goods and services, Reason for domestic protection) were not found on this machine, so they are not archived here.
