# Re-run the deterministic data pulls (Eurostat Comext) and re-render the charts. Used for the 13-14 Nov 2026 refresh.
#   powershell -ExecutionPolicy Bypass -File scripts\refresh_data.ps1
# Writes a log to notes\refresh-log.txt and prints what changed in the key tables (git diff, uncommitted).
# It does NOT edit the outline text or commit; see notes\refresh-13-14-nov.md for the rest of the runbook.
$ErrorActionPreference = 'Continue'
$repo = Split-Path $PSScriptRoot -Parent
Set-Location $repo
. (Join-Path $PSScriptRoot 'env.ps1')
$log = Join-Path $repo 'notes\refresh-log.txt'
function Log($m) { $line = '{0}  {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m; Add-Content -LiteralPath $log -Value $line -Encoding UTF8; Write-Host $line }
function Step($name, $cmd) {
    Log "START $name"
    & cmd /c $cmd 2>&1 | ForEach-Object { Log ('    ' + $_) }
    Log ("END   $name (exit " + $LASTEXITCODE + ')')
}

Log '=== refresh started ==='
$py = 'python -I -X utf8'
Step 'trade_2026: monthly Comext pull'     "$py data\trade_2026\scripts\01_pull_comext.py data\trade_2026\raw"
Step 'trade_2026: YTD tables'              "$py data\trade_2026\scripts\02_compute_ytd.py data\trade_2026\raw data\trade_2026\tables"
Step 'trade_2026: annual vintage check'    "$py data\trade_2026\scripts\03_vintage_check.py data\trade_2026\raw data\trade_2026\tables sources\text\inter-trade-present-2-revised-research-brief.txt"
Step 'comext_exports: annual pull + tables' "$py data\comext_exports\pull_comext.py"

foreach ($g in 'fig2_import_cost_redraw', 's6_manufacturing', 's7_extra_eu_imports', 's8_steel_trade_balance', 'a8_cleaner_steel_outcome') {
    Log "chart $g"
    # only the Fig. 2 script takes a format argument; the others treat ARG1 as a data file
    if ($g -eq 'fig2_import_cost_redraw') { $o = gnuplot -c "graphs/gnuplot/$g.gp" png 2>&1 | Out-String } else { $o = gnuplot -c "graphs/gnuplot/$g.gp" 2>&1 | Out-String }
    if ($o.Trim()) { Log ('    gnuplot: ' + $o.Trim()) }
}

Log '--- changed data tables (git diff --stat) ---'
git diff --stat -- data/trade_2026/tables data/comext_exports graphs/out | ForEach-Object { Log ('    ' + $_) }
Log 'Key table to read first: data\trade_2026\tables\ytd_comparison.csv (Jan-Sep 2026 vs Jan-Sep 2025 once Eurostat adds September)'
Log '=== refresh finished ==='
