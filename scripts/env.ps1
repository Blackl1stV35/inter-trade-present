# Dot-source to use the project-local tools in this PowerShell session only:  . scripts\env.ps1
# Puts tools\gnuplot\bin on PATH and lets gnuplot's fontconfig find TH Sarabun New. gnuplot cannot see per-user
# Windows fonts, so the two font files are copied from the per-user fonts folder into tools\fonts (git-ignored).
$root = Split-Path $PSScriptRoot -Parent
$bin = Join-Path $root 'tools\gnuplot\bin'
if (Test-Path $bin) { $env:PATH = "$bin;$env:PATH" }
$env:INTER_TRADE_ROOT = $root

$toolsDir = Join-Path $root 'tools'
if (Test-Path $toolsDir) {
    $fontDir = Join-Path $toolsDir 'fonts'
    New-Item -ItemType Directory -Force -Path $fontDir | Out-Null
    $userFonts = Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts'
    foreach ($f in 'thsarabunnew-webfont.ttf', 'thsarabunnew_bold-webfont.ttf') {
        $src = Join-Path $userFonts $f
        $dst = Join-Path $fontDir $f
        # Copy-Item fails with "could not be encrypted" for these per-user files; copy the bytes instead.
        if ((Test-Path $src) -and -not (Test-Path $dst)) { [System.IO.File]::WriteAllBytes($dst, [System.IO.File]::ReadAllBytes($src)) }
    }
    $cache = Join-Path $toolsDir 'fontconfig-cache'
    New-Item -ItemType Directory -Force -Path $cache | Out-Null
    $conf = Join-Path $toolsDir 'fonts.conf'
    $xml = @"
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <dir>$env:WINDIR\Fonts</dir>
  <dir>$fontDir</dir>
  <cachedir>$cache</cachedir>
</fontconfig>
"@
    [System.IO.File]::WriteAllText($conf, $xml, (New-Object System.Text.UTF8Encoding($false)))
    $env:FONTCONFIG_FILE = $conf
    $env:PANGOCAIRO_BACKEND = 'fc'
}
