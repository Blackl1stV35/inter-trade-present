# Gephi Toolkit run (no Gephi window; the Java 2D preview target needs the Windows desktop session, so it is not -Djava.awt.headless): compile RenderNetwork.java and render the company-case network (PNG, SVG, .gephi project).
#   powershell -ExecutionPolicy Bypass -File graphs\gephi\render_network.ps1
# Needs tools\gephi-toolkit\gephi-toolkit-0.11.3-all.jar (Maven Central, SHA-1 8bfad8f34cf51a42035185ccca8521ab9d375e43),
# the Java 17 runtime that ships with the project-local Gephi, a Java 17+ compiler (javac in WSL Ubuntu) and tools\fonts (scripts\env.ps1).
# Layout: hand-placed ('manual', default; ForceAtlas 2 makes a hairball of three disconnected chains) or set GEPHI_LAYOUT='scaling,gravity,strong,nodeSize,fa2'.
# Output: graphs\out\s9_company_network.* (the three cases and the state aid, slide S9) and
#         graphs\out\a13_company_network_full.* (all eleven nodes, backup A13); the .gephi projects go to graphs\gephi\.
$ErrorActionPreference = 'Continue'
$repo = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
Set-Location $repo
$jar = Join-Path $repo 'tools\gephi-toolkit\gephi-toolkit-0.11.3-all.jar'
$classes = Join-Path $repo 'tools\gephi-toolkit\classes'
New-Item -ItemType Directory -Force $classes | Out-Null
$wsl = { param($p) (wsl -d Ubuntu-22.04 -- wslpath -a ($p -replace '\\', '/')).Trim() }
$src = & $wsl (Join-Path $repo 'graphs\gephi\RenderNetwork.java')
$jarW = & $wsl $jar
$clsW = & $wsl $classes
$null = wsl -d Ubuntu-22.04 -- javac -cp $jarW -d $clsW $src 2>&1
if (-not (Test-Path (Join-Path $classes 'RenderNetwork.class'))) { throw 'javac failed' }
$java = (Get-ChildItem (Join-Path $repo 'tools\gephi\jre-x64') -Recurse -Filter java.exe | Select-Object -First 1).FullName
$cp = "$jar;$classes"
function Render($prefix, $w, $h, $exclude, $label, $edgeLabel, $scaling, $gravity, $strong, $nodeSize, $mode) {
    & $java '--add-opens=java.base/java.net=ALL-UNNAMED' '--add-opens=java.base/java.nio=ALL-UNNAMED' '--add-opens=java.desktop/javax.swing=ALL-UNNAMED' '--add-exports=java.desktop/sun.awt=ALL-UNNAMED' -cp $cp RenderNetwork (Join-Path $repo 'graphs\gephi\nodes.csv') (Join-Path $repo 'graphs\gephi\edges.csv') $prefix $w $h $exclude (Join-Path $repo 'tools\fonts') 7 $label $edgeLabel
    if ($LASTEXITCODE -ne 0) { throw "Gephi run failed for $prefix" }
}
$out = Join-Path $repo 'graphs\out'
$layout = if ($env:GEPHI_LAYOUT) { $env:GEPHI_LAYOUT -split ',' } else { @('60', '6', 'true', '14', 'manual') }
Render (Join-Path $out 's9_company_network') 1760 1240 'ssab,volvo,outo' 32 26 $layout[0] $layout[1] $layout[2] $layout[3] $layout[4]
Render (Join-Path $out 'a13_company_network_full') 1760 1440 '-' 32 26 $layout[0] $layout[1] $layout[2] $layout[3] $layout[4]
foreach ($n in 's9_company_network', 'a13_company_network_full') {
    Move-Item -Force (Join-Path $out "$n.gephi") (Join-Path $repo "graphs\gephi\$n.gephi")
}
