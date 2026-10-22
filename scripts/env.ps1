# Dot-source to use the project-local tools in this PowerShell session only:  . scripts\env.ps1
$root = Split-Path $PSScriptRoot -Parent
$bin = Join-Path $root 'tools\gnuplot\bin'
if (Test-Path $bin) { $env:PATH = "$bin;$env:PATH" }
$env:INTER_TRADE_ROOT = $root
