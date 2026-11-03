# One command for the whole report loop: render figures, rebuild the document, inspect every visual, save.
#   powershell -ExecutionPolicy Bypass -File report/scripts/build_report.ps1 -Message "what changed"
param([Parameter(Mandatory = $true)][string]$Message)
$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $root
. scripts/env.ps1
$data = Join-Path $root 'data'
Copy-Item report/chart-materials/data/fig24_steel_2012_2025.csv $data -Force
try { powershell -ExecutionPolicy Bypass -File report/chart-materials/gnuplot/render_all.ps1 -Data $data -Out (Join-Path $root 'report/chart-materials/figures-gnuplot') } finally { Remove-Item (Join-Path $data 'fig24_steel_2012_2025.csv') -ErrorAction SilentlyContinue }
python -I -X utf8 report/scripts/stage_e_rebuilt_figures.py
python -I -X utf8 report/scripts/stage_d_appendix_code.py
python -I -X utf8 report/scripts/stage_h_heading_pairs.py
python -I -X utf8 report/scripts/stage_i_format.py
python -I -X utf8 report/scripts/stage_c_front.py
python -I -X utf8 report/scripts/verify_visuals.py
if ($LASTEXITCODE -ne 0) { throw 'visual inspection failed; nothing saved' }
powershell -ExecutionPolicy Bypass -File scripts/save.ps1 -Message $Message -Paths 'report'
Copy-Item report/inter-trade-report.docx "D:\Downloads\Inter Trade present (final).docx" -Force
