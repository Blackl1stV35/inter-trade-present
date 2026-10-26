# Slide sketches

One PNG per deck page, 1920 x 1080 (a 16:9 slide at 144 dpi, so 1 pt = 2 px), drawn from `outline/final-outline-proposal.md`.
The sketches show the on-slide content and layout only; the "Say", "Limits" and speaker-note text of the outline stays in the outline.

- `src/<id>.html` — one fragment per page (S1 to S13, then backup A1 to A15)
- `png/<id>.png` — the rendered sketch; `png/_report/<id>.json` — per page checks (overflow, text outside the slide, smallest font)
- `contact-sheet-main.png`, `contact-sheet-backup.png` — thumbnails of all pages
- `style.css` — shared style; `../../scripts/build_sketches.py` — renderer (Edge through Playwright, TH Sarabun New from `tools/fonts`)
- `../../graphs/gephi/` — the company-case network drawn on S9 (Gephi project, nodes and edges, exports)

Rebuild: `. scripts\env.ps1; python -I -X utf8 scripts\build_sketches.py [ids] [--sheet]`

## Fragment format

```html
<!--META {"id":"S7","chapter":"CH2","min":1.5,"label":"Observed data","chips":["M","Q","P"],
"title":"Action title, two lines at most (about 80 characters)",
"foot":"One or two short lines: what the slide does not show.",
"tags":"Source tags, for example Comext DS-045409 · U24"} -->
<div class="row grow"> ...main area HTML... </div>
```

- `label` is exactly one of: Observed data, Policy rule, Model-based result, Theoretical-illustrative, Company announcement, Team judgement.
- `chapter` is CH1, CH2, CH3 or BK (backup page; `min` is then omitted).
- `chips` lights the variables the slide covers (X, M, NX, BOP, Q, P, GDP, Tax, C, I, G); leave `[]` when none.
- The frame (CH1 | CH2 | CH3 ribbon, label, title, footer, variable chips) is drawn by the renderer; the fragment fills the main area only (1800 x 696 px).

## Rules

- Body text 28 pt (56 px), the default size. Tile labels, table cells in dense tables and chart captions may drop to 20 pt (40 px, class `cap` or `lbl`); nothing in the main area below 19 pt; `tag` text is 16 pt.
- Cells and bullets of about eight words; at most one chart and one small table or tile group per slide (a two-panel figure counts as one chart).
- Numbers are copied from the outline exactly; never add a number that is not in the outline or in the repository's data files; condense by dropping detail, not by rounding.
- No title says "effect"; no causal verbs; policy dates are annotations.
- Charts are the existing PNGs (`graphs/out/*.png`, `sources/images/base-doc-fig-01.png`); a missing figure is a labelled placeholder box.

## Classes in `style.css`

`row`, `col` (flex; `grow` = flex 1, `w2`, `w3` = flex 2 and 3), `center`; `card` (+ `blue`, `green`, `amber`, `grey` top bar) with `h2`; `tile` with `num` and `lbl`; `blue-t`, `green-t`, `amber-t`, `grey-t` text colours;
`fig` (image box; `<img src="graphs/out/…png">`, paths are relative to the repository root); `cap` (caption, 40 px); `tag`; `ul.b` bullets; `opp` (green left bar) and `lim` (amber left bar) lines;
`chip` (+ `mou`, `contract`, `gap`, `ctx`, `obs`) status pills; `table.t` (+ `sm`); `banner` (amber banner, for ILLUSTRATIVE); `strip` (three columns BEFORE / DURING / AFTER, each with `<span class="k">`).
