# Shared look for all deck charts. Load from the repo root:  load 'graphs/gnuplot/common.gp'
# Text font: TH Sarabun New (needs scripts/env.ps1 to be dot-sourced first so gnuplot can see the font).
fnt   = 'TH Sarabun New,22'
fntT  = 'TH Sarabun New,28'
fntS  = 'TH Sarabun New,19'
blue  = '#2B5C98' ; green = '#167A67' ; dark = '#263444' ; grey = '#78828C' ; amber = '#B26A00' ; band = '#EEF0F2' ; red = '#A33B3B'
set border 3 lw 2 lc rgb grey
set tics nomirror textcolor rgb dark
unset key
set grid ytics lc rgb '#E3E6E9' lw 1
set style textbox 1 opaque noborder fc rgb 'white'
