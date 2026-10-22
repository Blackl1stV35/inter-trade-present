# Project-local install of gnuplot and Gephi into <repo>\tools. No admin rights, no system PATH change.
# Re-runnable: skips a tool that is already installed. Run from anywhere:
#   powershell -ExecutionPolicy Bypass -File scripts\setup_tools.ps1
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

$Root = Split-Path $PSScriptRoot -Parent
$Tools = Join-Path $Root 'tools'
$Downloads = Join-Path $Tools '_downloads'
$SevenZip = 'C:\Program Files\7-Zip\7z.exe'

# Pinned releases. SHA-256 values: gnuplot from the checksum file published beside the file on SourceForge;
# Gephi from the GitHub release asset digest (matches the winget manifest).
$Gnuplot = @{
    Version = '6.0.5'
    Url     = 'https://sourceforge.net/projects/gnuplot/files/gnuplot/6.0.5/gp605-win64-mingw.7z/download'
    Sha256  = 'ffb636ec377d20c0039d27636ab94a89f3b700926f704fb3df1064dae16b0c35'
    File    = 'gp605-win64-mingw.7z'
}
$Gephi = @{
    Version = '0.11.3'
    Url     = 'https://github.com/gephi/gephi/releases/download/v0.11.3/gephi-0.11.3-windows-x64.exe'
    Sha256  = 'bf3f488ab9cdab57e2b9f7ab4f2b449b452391f29a9df4d7c7edea198fb323cf'
    File    = 'gephi-0.11.3-windows-x64.exe'
}

function Get-Verified([hashtable]$Pkg, [string]$SubDir) {
    $dir = Join-Path $Downloads $SubDir
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    $dest = Join-Path $dir $Pkg.File
    Write-Host "Downloading $($Pkg.File) ..."
    Invoke-WebRequest -Uri $Pkg.Url -OutFile $dest -UseBasicParsing -Headers @{ 'User-Agent' = 'inter-trade-setup' }
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $dest).Hash.ToLower()
    if ($actual -ne $Pkg.Sha256) {
        Remove-Item -LiteralPath $dest -Force
        throw "SHA-256 mismatch for $($Pkg.File): expected $($Pkg.Sha256), got $actual"
    }
    Write-Host "  SHA-256 verified."
    return $dest
}

New-Item -ItemType Directory -Force -Path $Tools | Out-Null

# --- gnuplot (portable 7z) ---
$gnuplotDir = Join-Path $Tools 'gnuplot'
if (Test-Path (Join-Path $gnuplotDir 'bin\gnuplot.exe')) {
    Write-Host "gnuplot already installed at $gnuplotDir"
} else {
    if (-not (Test-Path $SevenZip)) { throw "7-Zip not found at $SevenZip" }
    $archive = Get-Verified $Gnuplot 'gnuplot'
    $extract = Join-Path $Downloads 'gnuplot\extracted'
    New-Item -ItemType Directory -Force -Path $extract | Out-Null
    & $SevenZip x -y "-o$extract" $archive | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "7-Zip extraction failed ($LASTEXITCODE)" }
    $inner = Get-ChildItem -LiteralPath $extract -Directory | Select-Object -First 1
    if (-not $inner) { throw 'Unexpected gnuplot archive layout' }
    if (Test-Path $gnuplotDir) { Remove-Item -Recurse -Force $gnuplotDir }
    Move-Item -LiteralPath $inner.FullName -Destination $gnuplotDir
    Write-Host "gnuplot installed at $gnuplotDir"
}

# --- Gephi (Inno Setup installer, directed into the project; per-user, no admin) ---
$gephiDir = Join-Path $Tools 'gephi'
if (Get-ChildItem -LiteralPath $gephiDir -Filter 'gephi*.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1) {
    Write-Host "Gephi already installed at $gephiDir"
} else {
    $installer = Get-Verified $Gephi 'gephi'
    $log = Join-Path $Downloads 'gephi\install.log'
    $p = Start-Process -FilePath $installer -Wait -PassThru -ArgumentList @(
        '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART', '/CURRENTUSER', '/NOICONS',
        "/DIR=`"$gephiDir`"", "/LOG=`"$log`""
    )
    if ($p.ExitCode -ne 0) { throw "Gephi installer exited with code $($p.ExitCode); see $log" }
    Write-Host "Gephi installed at $gephiDir"
}

# --- launchers and env (keep Gephi's settings inside the project too) ---
$gephiExe = Get-ChildItem -LiteralPath $gephiDir -Filter 'gephi*.exe' -Recurse | Where-Object { $_.Name -notmatch 'unins' } | Select-Object -First 1
if ($gephiExe) {
    $userdir = Join-Path $Tools 'gephi-userdir'
    New-Item -ItemType Directory -Force -Path $userdir | Out-Null
    $cmd = "@echo off`r`nstart `"`" `"$($gephiExe.FullName)`" --userdir `"$userdir`" %*`r`n"
    Set-Content -LiteralPath (Join-Path $Tools 'run-gephi.cmd') -Value $cmd -Encoding ASCII
}

# Remove downloaded installers/archives (they are re-fetched and re-verified on the next run)
if (Test-Path $Downloads) { Remove-Item -Recurse -Force $Downloads }
Write-Host 'Done. In a shell: . scripts\env.ps1   (adds tools\gnuplot\bin to PATH for that session)'
