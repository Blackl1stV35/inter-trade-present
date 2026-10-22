# Save step of the work loop: stage everything not ignored, commit with the given message, push the current branch.
#   powershell -ExecutionPolicy Bypass -File scripts\save.ps1 -Message "Add Fig. 2 redraw"
# Refuses to push unless the GitHub remote has the expected visibility (default PUBLIC, as set by the owner on 2026-10-22).
param([Parameter(Mandatory = $true)][string]$Message, [string]$Paths = '.', [switch]$NoPush, [string]$ExpectVisibility = 'PUBLIC')   # -Paths 'graphs,notes' (comma separated)
$ErrorActionPreference = 'Stop'
$repo = Split-Path $PSScriptRoot -Parent
Set-Location $repo

git add -A -- ($Paths -split ',')
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host 'Nothing new to commit; will still push any unpushed commits.'
} else {
    $file = Join-Path $env:TEMP ('commit-msg-' + [guid]::NewGuid().ToString('N') + '.txt')
    $text = "$Message`n`nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`n"
    [System.IO.File]::WriteAllText($file, $text, (New-Object System.Text.UTF8Encoding($false)))
    git commit -q -F $file
    Remove-Item $file
}
git log --oneline -1

if ($NoPush) { exit 0 }
$remote = git remote get-url origin 2>$null
if (-not $remote) { Write-Host 'No origin remote; not pushing.'; exit 0 }
$slug = ($remote -replace '^https://github.com/', '' -replace '\.git$', '')
$vis = gh repo view $slug --json visibility -q .visibility
if ($vis -ne $ExpectVisibility) { throw "Remote $slug is $vis but $ExpectVisibility was expected (visibility changed?); refusing to push. Re-run with -ExpectVisibility $vis only if that change was intended." }
$branch = git rev-parse --abbrev-ref HEAD
# git writes progress to stderr even on success; judge by exit code only
$ErrorActionPreference = 'Continue'
git push -u origin $branch 2>&1 | Out-Null
$code = $LASTEXITCODE
$ErrorActionPreference = 'Stop'
if ($code -ne 0) { throw "git push failed (exit $code)" }
Write-Host "Pushed $branch to $slug ($vis)."
