# Report work plan (project: Inter Trade presentation and report)

Status as of 3 Nov 2026. Each step is committed and pushed when done.

1. Report text: audit points applied, first-person wording, full re-read (v13). Done.
2. Cover: KU logo placed by the requester in the working file. Done.
3. Verify two report facts against primary sources (done 3 Nov 2026: EWE deliveries from 2030 confirmed by Salzgitter press release; SALCOS first-stage support +EUR 322 million, total about EUR 1.32 billion, confirmed by Steelorbis 24 Feb 2026 citing the federal ministry):
   - EWE hydrogen deliveries to SALCOS, milestone year (report says 2030). In progress.
   - Salzgitter SALCOS first-stage support total (report says about EUR 322 million added, EUR 1.322 billion total). In progress.
4. Figures: all six drawn with GNUplot in Times New Roman (installed on Windows; no new install needed), each checked for alignment and overlaps. Done.
5. Appendix C: list the GNUplot scripts that produce the figures; keep sample data references generic.
6. Rebuild contents page numbers, verify text (no em dash, no "rather than"), save the final docx to Downloads.

7. Layout pass (3 Nov 2026): titles sit above each plot box, legends inside the margins, Figure 2.5 labels clear of lines and axes. Done.
8. Single report document: scripts/check_single_docx.py runs before every save and in .github/workflows/single-docx.yml. The only report file is report/inter-trade-report.docx; the Downloads folder keeps one final copy, "Inter Trade present (final).docx". Done.
