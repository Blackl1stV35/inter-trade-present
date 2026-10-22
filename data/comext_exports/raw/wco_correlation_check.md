# WCO correlation-table check for the headings used (classification breaks)

Retrieved 2026-10-22 by fetching the WCO Table I PDFs (HS edition N versus edition N-1) and searching the extracted text
for codes in Chapter 72 (7201-7229), headings 7304 and 7306, and subheading 2601.12. The WCO states these tables are a
guide with no legal status. Results are my reading of the extracted text (pdftotext), not a legal determination.

| HS edition (Table I) | Source file | Entries found for the codes checked |
| --- | --- | --- |
| HS 2002 vs 1996 | https://www.wcoomd.org/-/media/wco/public/global/pdf/topics/nomenclature/instruments-and-tools/hs-nomenclature-older-edition/2002/correlations-1996-2002/hs_correlation2002_table1_eng.pdf | None in Chapter 72, 7304, 7306 or 2601 (the only Chapter 72/73 neighbour is a 7302.20 deletion). |
| HS 2007 vs 2002 | https://www.wcoomd.org/-/media/wco/public/global/pdf/topics/nomenclature/instruments-and-tools/hs-nomenclature-older-edition/2007/correlations-2002-2007/hs_correlation2007_table_i_e_rev5.pdf | Chapter 72: subheading deletions/merges inside headings 7225, 7226, 7229 only (7204, 7207, 7208 not listed). Heading 7304: subheadings 7304.10 and 7304.21 subdivided (stainless line pipe, casing/tubing/drill pipe). Heading 7306: subheadings 7306.10, 7306.20, 7306.60 subdivided (new 7306.11/.19/.21/.29/.61/.69). All inside the same four-digit heading. 2601 not listed. |
| HS 2012 vs 2007 | https://www.wcoomd.org/-/media/wco/public/global/pdf/topics/nomenclature/instruments-and-tools/hs-nomenclature-2012/correlations-2007-2012/i_trp1207rev3eng.pdf | None in Chapter 72, 7304, 7306 or 2601 (heading 7319 only in Chapter 73). |
| HS 2017 vs 2012 | https://www.wcoomd.org/-/media/wco/public/global/pdf/topics/nomenclature/instruments-and-tools/hs-nomenclature-2017/2016/table_i_trp1712_en_rev1.pdf | None in Chapter 72, 7304, 7306 or 2601 (7326.90 only in Chapter 73). |
| HS 2022 vs 2017 | https://www.wcoomd.org/-/media/wco/public/global/pdf/topics/nomenclature/instruments-and-tools/hs-nomenclature-2022/table-i_en.pdf | None in Chapter 72, 7304, 7306 or 2601 (7317, 7318 only in Chapter 73). |

Cross-check against the live Comext data (pull_subcodes.py): the HS6 sub-code sets observed under 7204, 7207 and 7208
are identical in every year 1999-2025; under 7304 and 7306 the HS6 codes split in 2007 exactly as the HS 2007 table
describes (730410 -> 730411/730419, 730421 -> 730422/730423/730424, 730610 -> 730611/730619, 730620 -> 730621/730629,
730660 -> 730661/730669). Comext also carries non-numeric codes (heading "XX" not elsewhere specified/confidential,
"I" components of complete industrial plants, "S6" confidential SITC): 7304XX is used for 1999-2005 only and holds
6-14 percent of the 7304 export value in those years; all such codes roll up into the four-digit heading totals.
