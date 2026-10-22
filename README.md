# Inter Trade presentation — EU ETS and CBAM, Germany steel case

Group assignment for the International Trade course (slide deck + report, 20 pts).
Working title: *How EU ETS and CBAM Can Strengthen Europe's Long-Term Green Manufacturing Economy: The Case of Germany*.

This repository is a local archive of everything produced so far (saved 2026-10-22) plus the slide-deck outline.
It is **local only** — the LINE chat export contains student IDs and a private Google Doc link, so do not push it to a public remote.

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
| `outline/slide-outline-15min.md` | Proposed slide outline for a 15-minute talk |
| `graphs/gephi/` | Gephi import files (nodes/edges CSV) for the company-case network, with build steps |
| `scripts/` | Helpers: .docx text/image extraction, `setup_tools.ps1` (project-local gnuplot + Gephi), `env.ps1` |
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
