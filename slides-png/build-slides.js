// Renders the 12 sketch slides and the 5 charts as PNG files using headless Chrome.
const fs = require('fs');
const path = require('path');
const cp = require('child_process');

const base = 'C:\\Users\\user\\AppData\\Roaming\\Claude\\scratch-workspaces\\c7acaf2f-ed5f-4f26-814b-0755985b8641\\704b7f5d-017e-4c68-a76d-e0c46600fd5a\\scratch-2026-11-03-2a8cd8\\slides-png';
const src = path.join(base, 'src');
const chartDir = path.join(base, 'charts');
fs.mkdirSync(src, { recursive: true });
fs.mkdirSync(chartDir, { recursive: true });
const chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

const CSS = `
html,body{margin:0;background:#fff}
.slide{position:relative;width:1280px;height:720px;overflow:hidden;box-sizing:border-box;padding:34px 56px;font-family:"Times New Roman",Times,serif;color:#000;background:#fff}
.num{position:absolute;right:56px;top:18px;font-size:16px;color:#444}
h1{font-size:36px;margin:0 0 6px 0;font-weight:bold;line-height:1.15}
.key{font-size:21px;font-style:italic;margin:0;color:#222;line-height:1.3}
.content{position:absolute;left:56px;right:56px;top:170px;bottom:70px}
ul,ol{font-size:21px;line-height:1.35;margin:0;padding-left:26px}
li{margin-bottom:8px}
table{border-collapse:collapse;width:100%;font-size:18px}
th,td{border:1px solid #000;padding:7px 9px;vertical-align:top;text-align:left}
th{background:#e6e6e6}
.chartbox{position:absolute;left:0;bottom:0;width:1168px;height:200px}
.boxes{display:flex;gap:22px;margin-top:10px}
.boxes div{flex:1;border:2px solid #000;padding:34px 16px;font-size:26px;text-align:center}
.boxes small{font-size:18px}
.bottom{margin-top:34px;border:1px dashed #000;padding:14px;font-size:22px;text-align:center}
.cols{display:flex;gap:22px;margin-top:22px}
.cols div{flex:1;border:2px solid #000;padding:20px;font-size:20px}
.answer{margin-top:24px;border:2px solid #000;padding:16px;font-size:21px}
.title h1{font-size:44px;text-align:center;margin-top:30px}
.title .key{text-align:center;font-size:24px;margin-top:10px}
.title .content{top:250px}
.title .question{border:2px solid #000;padding:24px;font-size:26px;text-align:center}
.foot{position:absolute;left:56px;right:56px;bottom:12px;font-size:13px;color:#333;border-top:1px solid #777;padding-top:5px;line-height:1.25}
`;

// Chart 1: Virginia jobs, construction against operations (JLARC 2024 via GMU brief).
const chartJobs = `<svg width="1168" height="200" viewBox="0 0 1168 200" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman, Times, serif">
<line x1="40" y1="180" x2="520" y2="180" stroke="#000" stroke-width="1.5"/>
<rect x="110" y="30" width="150" height="150" fill="#333"/>
<rect x="320" y="142" width="150" height="38" fill="#999"/>
<text x="185" y="22" font-size="17" text-anchor="middle">59,000</text>
<text x="395" y="134" font-size="17" text-anchor="middle">15,000</text>
<text x="185" y="198" font-size="16" text-anchor="middle">Construction (temporary)</text>
<text x="395" y="198" font-size="16" text-anchor="middle">Operations (ongoing)</text>
<text x="600" y="30" font-size="19" font-weight="bold">Virginia data-center jobs, annual average</text>
<text x="600" y="62" font-size="17">Total about 74,000 jobs a year; about 50 operating staff per facility</text>
<text x="600" y="90" font-size="17">Construction is temporary: a building takes about 12 to 18 months</text>
<text x="600" y="130" font-size="15" fill="#333">Source: JLARC 2024 split as reported in GMU STEP Brief 5.</text>
<text x="600" y="150" font-size="15" fill="#333">Total jobs and GDP confirmed in the UVA Cooper Center summary of JLARC.</text>
</svg>`;

// Chart 2: power. Left: EGAT requests against system peak. Right: Bangkok capacity by stage.
const chartPower = `<svg width="1168" height="200" viewBox="0 0 1168 200" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman, Times, serif">
<text x="0" y="18" font-size="18" font-weight="bold">EGAT, September 2026 (national)</text>
<text x="0" y="50" font-size="16">Requested by data-center operators: about 3.5 GW</text>
<rect x="0" y="58" width="42" height="26" fill="#333"/>
<text x="0" y="110" font-size="16">System peak: about 40 GW</text>
<rect x="0" y="118" width="480" height="26" fill="#999"/>
<text x="600" y="18" font-size="18" font-weight="bold">Bangkok data centers (JustPow, 3 Sep 2026)</text>
<rect x="600" y="30" width="246.6" height="34" fill="#333"/>
<rect x="846.6" y="30" width="184.9" height="34" fill="#777"/>
<rect x="1031.5" y="30" width="48.5" height="34" fill="#bbb" stroke="#000" stroke-width="1"/>
<text x="600" y="90" font-size="16">Operating: 127 MW (16 of 24 sites with data)</text>
<text x="600" y="112" font-size="16">Under construction: 95.2 MW (6 of 7 sites with data)</text>
<text x="600" y="134" font-size="16">Planned: about 25 MW (derived: total minus the two above)</text>
<text x="600" y="162" font-size="16" font-weight="bold">Total: at least 247.2 MW</text>
<text x="600" y="188" font-size="14" fill="#333">Water use: about 2.23 million cubic metres a year (estimate).</text>
</svg>`;

// Chart 3: timeline of the Thai EIA and permit steps (August and September 2026).
const chartTimeline = `<svg width="1168" height="200" viewBox="0 0 1168 200" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman, Times, serif">
<line x1="40" y1="100" x2="1128" y2="100" stroke="#000" stroke-width="2"/>
<line x1="883" y1="92" x2="883" y2="108" stroke="#000" stroke-width="2"/>
<text x="40" y="126" font-size="15">1 Aug</text>
<text x="883" y="126" font-size="15" text-anchor="middle">1 Sep</text>
<circle cx="203" cy="100" r="7" fill="#000"/>
<circle cx="938" cy="100" r="7" fill="#000"/>
<circle cx="965" cy="100" r="7" fill="#666"/>
<text x="203" y="38" font-size="17" font-weight="bold">7 Aug 2026</text>
<text x="203" y="60" font-size="16">ONEP reply: data centers are not a listed EIA category</text>
<text x="203" y="80" font-size="16">EIA applies to large or high-rise buildings in sensitive areas</text>
<text x="1120" y="38" font-size="17" font-weight="bold" text-anchor="end">4 to 5 Sep 2026</text>
<text x="1120" y="60" font-size="16" text-anchor="end">166 projects paused nationally</text>
<text x="1120" y="80" font-size="16" text-anchor="end">(49 under construction; 117 awaiting approval)</text>
<text x="930" y="150" font-size="17" font-weight="bold" text-anchor="end">3 Sep 2026</text>
<text x="930" y="172" font-size="16" text-anchor="end">Bangkok governor halts new data-center permits</text>
</svg>`;

// Chart 4: supplier pyramid (Thai auto, Tier 1 against Tiers 2 and 3).
const chartPyramid = `<svg width="1168" height="200" viewBox="0 0 1168 200" xmlns="http://www.w3.org/2000/svg" font-family="Times New Roman, Times, serif">
<polygon points="404,8 764,8 824,98 344,98" fill="#ddd" stroke="#000" stroke-width="1.5"/>
<polygon points="344,98 824,98 1000,192 168,192" fill="#aaa" stroke="#000" stroke-width="1.5"/>
<text x="584" y="40" font-size="17" font-weight="bold" text-anchor="middle">Tier 1: about 720 firms</text>
<text x="584" y="62" font-size="15" text-anchor="middle">about half foreign-owned; ~30% foreign-Thai JVs</text>
<text x="584" y="84" font-size="15" text-anchor="middle">the remainder Thai-owned</text>
<text x="584" y="150" font-size="17" font-weight="bold" text-anchor="middle">Tiers 2 and 3: mostly Thai SMEs</text>
<text x="584" y="174" font-size="15" text-anchor="middle">count to be verified before use</text>
</svg>`;

const slides = [
{ n: 1, cls: 'title',
  title: 'Data-Center FDI in Thailand: Who Gains, and Under What Conditions?',
  key: 'Economics of International Investment | 26 November 2026',
  body: `<div class="question">Does FDI in data centers raise Thailand's welfare, and under what conditions?</div>
<ul style="margin-top:28px"><li>Four questions: why communities oppose; Thailand's view; conditions for net gain; comparison with developed hosts</li><li>Frame: the course framework for the effects of FDI on a host country</li></ul>`,
  foot: 'Title slide, no chart. Course reference: L1, topic slide "Effects of FDI: Introduction".' },

{ n: 2, title: 'Framework: Effects of FDI on the Host Country',
  key: 'FDI reaches a host through three channels. Each effect depends on the type of FDI, the sector and the timeframe.',
  body: `<div class="boxes">
<div>Product market<br><small>trade, output, competition</small></div>
<div>Factor market<br><small>capital, labour, wages</small></div>
<div>Spillovers<br><small>technology, skills, linkages</small></div></div>
<div class="bottom">Effects depend on FDI type, sector and timeframe.</div>`,
  foot: 'Redrawn diagram, not the lecture graphic. Course reference: L1, "Transmission mechanism" and "Things to consider when looking at the FDI effects".' },

{ n: 3, title: 'Why Data Centers Are a Distinct Case',
  key: 'Data centers are capital-heavy services with few permanent jobs, so manufacturing-based evidence may not transfer.',
  body: `<ul>
<li>Virginia (JLARC 2024): about 74,000 jobs a year, of which about 59,000 are temporary construction and about 15,000 operations</li>
<li>About 50 operating staff per facility (same source)</li>
<li>Thailand: 521.2 billion baht from 28 data-center projects in the first half of 2025 (BOI release 92/2568)</li>
<li>Course note: manufacturing has strong linkages; services give little spillover support (Alfaro 2003)</li></ul>
<div class="chartbox">${chartJobs}</div>`,
  foot: 'Sources: BOI press release 92/2568 (read in full, 24 Jul 2025). Jobs split as reported in GMU STEP Brief 5 (Sept 2026), citing JLARC 2024; total 74,000 jobs and $9.1 billion GDP confirmed in the UVA Cooper Center summary of JLARC. Course: IF, Alfaro slide and notes.' },

{ n: 4, title: 'Why Communities Oppose (1): Shared Resources',
  key: 'Data centers compete with local users for power and water, so part of their cost falls on the host community.',
  body: `<ul>
<li>EGAT: operators requested about 3.5 GW against a system peak of about 40 GW; EGAT seeks financial safeguards for grid costs (Sept 2026)</li>
<li>Bangkok: at least 247.2 MW across operating, under-construction and planned sites; water about 2.23 million cubic metres a year (JustPow estimate)</li>
<li>Chonburi and Rayong: residents and farmers fear water shortage; at least 19 projects planned or under way (Mongabay, Mar 2026)</li></ul>
<div class="chartbox">${chartPower}</div>`,
  foot: 'Sources: The Nation 40071212 and 40070626 (read live, 3 Nov 2026); Mongabay, 11 Mar 2026 (read live). Planned MW is derived from the article total. Course: L2 crowding in and out; L3 typology table, infrastructure row.' },

{ n: 5, title: 'Why Communities Oppose (2): Jobs, Information and Trust',
  key: 'Permanent local jobs are fewer than the investment suggests, and the information gap fuels opposition.',
  body: `<ul>
<li>US evidence: a typical county gains about 100 to 200 jobs; large projects promise dozens to a few hundred permanent workers (Brookings, 2026)</li>
<li>Thailand: ONEP (7 Aug 2026) says data centers are not a listed EIA category; EIA applies to large or high-rise buildings, or ones in sensitive areas</li>
<li>Bangkok governor halted new data-center permits (3 Sep 2026)</li>
<li>166 projects paused nationally while standards are drafted (5 Sep 2026)</li></ul>
<div class="chartbox">${chartTimeline}</div>`,
  foot: 'Sources: Brookings brief (read live); The Standard, 2 Sep 2026, reporting the ONEP reply of 7 Aug 2026 (read live); The Nation 40070626 and 40070670 (read live). The Google claim of about 100 jobs in Chonburi was not found in the Mongabay article and is omitted. Course: L4 wages and employment; L2 government policy.' },

{ n: 6, title: "Thailand's View (1): Balance of Payments and Trade",
  key: 'The government sees data centers as a gain for investment and exports. The course shows the gain depends on local content.',
  body: `<ul>
<li>BOI: 521.2 billion baht from 28 data-center projects in the first half of 2025</li>
<li>Imported equipment raises imports in the short run</li>
<li>Foreign subsidiaries that import most inputs widen the current-account deficit; local content reduces that drag</li>
<li>An export platform can raise exports (course example: Toyota Thailand)</li></ul>
<div class="cols"><div><b>Positive:</b> investment inflows; tax revenue; export platform</div><div><b>Negative:</b> equipment and input imports; profit repatriation</div></div>`,
  foot: 'Sources: BOI release 92/2568 (read in full). Course: L1, balance of payment effect; FDI-export and FDI-import links; short and medium-term effects.' },

{ n: 7, title: "Thailand's View (2): Linkages and Spillovers",
  key: 'Spillovers reach local firms through linkages and absorptive capacity. The auto sector shows how this works.',
  body: `<ul>
<li>About 720 Tier 1 auto suppliers: roughly half foreign-owned; about 30% foreign-Thai joint ventures (GTAI)</li>
<li>Tiers 2 and 3 are mostly Thai SMEs (Alvarez and Marsal, Mar 2026)</li>
<li>Spillover channels: demonstration, labour turnover, backward and forward linkages</li>
<li>Data-center rules: two plans (Thai staff training; supply chain) before the tax exemption (Por. 3/2569, law-firm summary)</li></ul>
<div class="chartbox">${chartPyramid}</div>`,
  foot: 'Sources: GTAI (German-language search snippet); Alvarez and Marsal, Mar 2026 (search snippet); Por. 3/2569 summaries by Tilleke and Gibbins (Mar 2026) and CTA (Aug 2026). The lecture chart figures (47% foreign majority; over 1,100 Tier 2 and 3 firms) are not verified and are not shown. Course: L3 spillovers and linkages; L1 local content.' },

{ n: 8, title: 'Conditions for Net Gain',
  key: 'Net gains depend on absorptive capacity, competition, cost assignment and additionality.',
  body: `<table>
<tr><th>Condition</th><th>Course factor</th><th>Example</th></tr>
<tr><td>Absorptive capacity</td><td>Human capital; technology gap</td><td>Two plans before the tax exemption: Thai staff training and supply chain (Por. 3/2569, Feb 2026; law-firm summary)</td></tr>
<tr><td>Competition</td><td>Open markets to competing firms</td><td>Singapore: four operators at about 50 MW each (EDB, Aug 2026)</td></tr>
<tr><td>Cost assignment</td><td>Does the benefit justify the cost?</td><td>Virginia: $0.011 per kWh data-center electricity tax, 1 July 2026 to 30 June 2028 (HB 30, Item 3-5.24)</td></tr>
<tr><td>Additionality</td><td>Counterfactual</td><td>Georgia: 30% of data centers attributed to the exemption (DOAA summary)</td></tr>
<tr><td>Source concentration</td><td>Dependency on foreign investment</td><td>Thai FDI inflows 2024, preliminary: China 21%; Singapore 11.3%; EU 10.1% (course slide, BOT data)</td></tr>
</table>`,
  foot: 'Sources: EDB fact sheet, 21 Aug 2026 (read in full); Georgia DOAA summary, Jan 2026 (read in full); Virginia HB 30 budget text (budget.lis.virginia.gov, read via search); Por. 3/2569 law-firm summaries; Thai FDI shares from the course slide (BOT data). Course: IF factor list; L2 "Does the benefit justify the cost?"; L5 counterfactual.' },

{ n: 9, title: 'Thailand Compared with Developed Hosts',
  key: 'Ireland and Singapore set data-center rules with clear limits. Thailand is earlier in that process.',
  body: `<table>
<tr><th>Dimension</th><th>Ireland</th><th>Singapore</th><th>Thailand</th></tr>
<tr><td>Power and renewables</td><td>New data centers match import demand with generation sold to the wholesale market; at least 80% of annual demand from additional renewables, on a 6-year glide path</td><td>More than 50% green energy; liquid cooling; 100% energy-efficient IT equipment; Green Mark DC Platinum</td><td>About 3.5 GW requested; operators asked for financial safeguards on grid costs</td></tr>
<tr><td>Siting and approvals</td><td>Dublin constrained; connection process due by 31 March 2026 (CRU requirement); High Court granted leave for judicial review (28 Apr 2026)</td><td>Jurong Island; four operators at about 50 MW each</td><td>166 projects paused while national rules are drafted</td></tr>
<tr><td>Incentives</td><td>Corporate tax rate of 12.5% (course, IDA slide)</td><td>Not checked</td><td>8-year and 5-year CIT exemptions, capped at 100% of investment</td></tr>
</table>`,
  foot: 'Sources: CRU decision page, 12 Dec 2025 (read live); Irish Times and ClientEarth reports on leave, Apr 2026 (search snippets); EDB fact sheet, 21 Aug 2026 (read in full); The Nation, Sept 2026 (read live); Tilleke and Gibbins, Feb 2026 (secondary). Course: IF, income level; IF, Ireland case study.' },

{ n: 10, title: 'Synthesis: Effect by Criterion',
  key: 'Data-center FDI likely helps the current account and tax revenue. Local jobs and spillovers depend on conditions.',
  body: `<table>
<tr><th>Channel</th><th>Likely effect</th><th>Condition</th><th>Evidence status</th></tr>
<tr><td>Balance of payments</td><td>Positive in the short run; equipment imports offset it</td><td>Local content</td><td>Investment sourced; import share not measured</td></tr>
<tr><td>Tax and incentives</td><td>Revenue from profits; forgone revenue from exemptions</td><td>Cost test</td><td>Sourced (Georgia audit; Virginia budget text)</td></tr>
<tr><td>Jobs and wages</td><td>Few permanent jobs; higher pay for skilled staff</td><td>Skills</td><td>US evidence only; no Thai data</td></tr>
<tr><td>Spillovers</td><td>Weak unless linkages form</td><td>Absorptive capacity</td><td>Course evidence only</td></tr>
<tr><td>Local resources</td><td>Negative for power and water</td><td>Cost assignment</td><td>Sourced (EGAT; JustPow estimate)</td></tr>
</table>`,
  foot: 'Course: L4 summary table format (factor, effect and conditionality). Sources as on slides 3 to 9.' },

{ n: 11, title: 'Conclusion',
  key: 'Data-center FDI helps Thailand when its costs are priced and its linkages are required.',
  body: `<ol>
<li>Test incentives against cost per job and forgone revenue (Georgia audit as the model).</li>
<li>Make operators pay for the power and water they use (Virginia rate class and tax as models).</li>
<li>Tie incentives to local suppliers and training, and publish the results.</li></ol>
<div class="answer">Answer: data-center FDI is likely to help Thailand's current account and tax base. Its gains for workers and local firms depend on conditions that policy can set now.</div>`,
  foot: 'Course: closing slides in L1, L3 and L5; influencing factors.' },

{ n: 12, title: 'Sources and Q&A',
  key: 'Sources are listed by status. Questions to expect are at the end.',
  body: `<ul>
<li>Primary sources read: BOI releases 92/2568 and 15/2569 (full-year 2025); EDB and IMDA fact sheet (Aug 2026); Georgia DOAA summary (Jan 2026); CRU decision page (Dec 2025); The Nation (EGAT; JustPow; 166-project pause); Mongabay (Mar 2026); Brookings brief (2026)</li>
<li>Checked in Chrome, 3 Nov 2026: Virginia HB 30 budget text; ONEP reply (The Standard, 2 Sep 2026); UVA Cooper Center JLARC summary; PDP 2024 draft (EXRI summary); World Bank FY26 classification; Irish Times leave report (28 Apr 2026)</li>
<li>Secondary: GMU STEP Brief 5 (JLARC split); Tilleke and Gibbins and CTA (Por. 3/2569); GTAI and Alvarez and Marsal (auto suppliers); course slide citing BOT (Thai FDI inflows 2024)</li>
<li>Likely questions: Will data centers create jobs? Will power bills rise? Should Thailand refuse them?</li></ul>`,
  foot: 'Charts drafted from the sourced figures. Sketch proposal for the 26 November 2026 talk.' }
];

// Standalone charts: each is the same SVG with a caption, saved as its own PNG.
const charts = [
  { file: 'chart-03-virginia-jobs.png', svg: chartJobs, caption: 'Virginia data-center jobs, annual average (JLARC 2024 via GMU brief)' },
  { file: 'chart-04-power-egat-bangkok.png', svg: chartPower, caption: 'Power requests against system peak (EGAT) and Bangkok capacity by stage (JustPow)' },
  { file: 'chart-05-timeline-eia-permits.png', svg: chartTimeline, caption: 'Thai EIA and permit steps, August to September 2026' },
  { file: 'chart-07-supplier-pyramid.png', svg: chartPyramid, caption: 'Thai auto supplier tiers (GTAI; Alvarez and Marsal)' }
];

function page(s) {
  const foot = s.foot;
  return `<!doctype html><html><head><meta charset="utf-8"><title>Slide ${s.n}</title><style>${CSS}</style></head><body>` +
    `<div class="slide ${s.cls || ''}"><div class="num">${s.n} / 12</div><h1>${s.title}</h1><p class="key">${s.key}</p>` +
    `<div class="content">${s.body}</div><div class="foot">${foot}</div></div></body></html>`;
}

function chartPage(c) {
  return `<!doctype html><html><head><meta charset="utf-8"><title>${c.caption}</title><style>` +
    `html,body{margin:0;background:#fff}.wrap{width:1200px;padding:24px 16px;box-sizing:border-box;font-family:"Times New Roman",Times,serif;color:#000}` +
    `.cap{font-size:18px;font-weight:bold;margin:0 0 12px 0}.src{font-size:13px;color:#333;margin-top:10px}` +
    `</style></head><body><div class="wrap"><p class="cap">${c.caption}</p>${c.svg}<p class="src">Charts are drafts from the sourced figures in the fact sheet. Grayscale for print.</p></div></body></html>`;
}

function shoot(htmlPath, pngPath, w, h) {
  cp.execFileSync(chrome, [
    '--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars',
    '--force-device-scale-factor=1', '--window-size=' + w + ',' + h,
    '--screenshot=' + pngPath, 'file:///' + htmlPath.replace(/\\/g, '/')
  ], { stdio: 'ignore', timeout: 90000 });
}

for (const s of slides) {
  const num = String(s.n).padStart(2, '0');
  const html = path.join(src, `slide-${num}.html`);
  const png = path.join(base, `slide-${num}.png`);
  fs.writeFileSync(html, page(s), 'utf8');
  try {
    shoot(html, png, 1280, 720);
    console.log('ok ' + png);
  } catch (e) {
    console.log('FAILED slide ' + num + ': ' + e.message);
  }
}

for (const c of charts) {
  const html = path.join(src, 'chart-' + c.file.replace('.png', '.html'));
  const png = path.join(chartDir, c.file);
  fs.writeFileSync(html, chartPage(c), 'utf8');
  try {
    shoot(html, png, 1240, 330);
    console.log('ok ' + png);
  } catch (e) {
    console.log('FAILED chart ' + c.file + ': ' + e.message);
  }
}
