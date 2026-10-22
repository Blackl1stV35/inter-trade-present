# Save step of the work loop: stage everything not ignored, commit with the given message, push the current branch.
#   powershell -ExecutionPolicy Bypass -File scripts\save.ps1 -Message "Add Fig. 2 redraw"
# Refuses to push unless the GitHub remote is private.
param([Parameter(Mandatory = $true)][string]$Message, [switch]$NoPush)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
Set-Location $repo

git add -A
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Write-Host 'Nothing to commit.'; exit 0 }

$file = Join-Path $env:TEMP ('commit-msg-' + [guid]::NewGuid().ToString('N') + '.txt')
$text = "$Message`n`nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`n"
[System.IO.File]::WriteAllText($file, $text, (New-Object System.Text.UTF8Encoding($false)))
git commit -q -F $file
Remove-Item $file
git log --oneline -1

if ($NoPush) { exit 0 }
$remote = git remote get-url origin 2>$null
if (-not $remote) { Write-Host 'No origin remote; not pushing.'; exit 0 }
$slug = ($remote -replace '^https://github.com/', '' -replace '\.git$', '')
$vis = gh repo view $slug --json visibility -q .visibility
if ($vis -ne 'PRIVATE') { throw "Remote $slug is $vis, not PRIVATE; refusing to push." }
$branch = git rev-parse --abbrev-ref HEAD
git push -u origin $branch 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'git push failed' }
Write-Host "Pushed $branch to $slug ($vis)."
