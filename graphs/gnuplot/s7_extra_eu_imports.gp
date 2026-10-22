# Slide 7: direct extra-EU Chapter 72 imports 1999-2025 (Comext DS-045409, vintage 2026-10-16), two stacked panels.
# Data: data/comext_exports/ch72_extra_eu_balance_1999_2025.csv  (col 3 imports EUR m, col 6 imports kt)
# Run from the repo root:  gnuplot -c graphs/gnuplot/s7_extra_eu_imports.gp
load 'graphs/gnuplot/common.gp'
data = 'data/comext_exports/ch72_extra_eu_balance_1999_2025.csv'
set terminal pngcairo size 1700,1000 font fnt
set output 'graphs/out/s7_extra_eu_imports.png'
set datafile separator ','
set xrange [1999:2026.4]
set xtics 2 ; set mxtics 2

set multiplot
set label 40 'German direct imports from outside the EU, HS Chapter 72 (incl. scrap), 1999-2025' at screen 0.5,0.965 center font fntT textcolor rgb dark
set label 41 'Net mass (thousand tonnes)' at screen 0.018,0.71 center rotate by 90 textcolor rgb dark
set label 42 'Value (EUR million, nominal)' at screen 0.018,0.30 center rotate by 90 textcolor rgb dark
set label 43 'Comext DS-045409, reporter DE, partner EXT_EU27_2020 (fixed 2020 composition), imports; vintage 2026-10-16.' at screen 0.085,0.045 noenhanced textcolor rgb grey font fntS
set label 44 'Not the CBAM base. No 2026 point on this axis (Jan-Aug 2026 is compared with Jan-Aug 2025 on the slide).' at screen 0.085,0.015 noenhanced textcolor rgb grey font fntS

# markers: ETS 2005, crisis 2009, COVID 2020, energy shock 2022, CBAM reporting Oct 2023
set object 1 rect from 2008.5,graph 0 to 2009.5,graph 1 fc rgb band fs solid noborder behind
set object 2 rect from 2019.5,graph 0 to 2020.5,graph 1 fc rgb band fs solid noborder behind
set object 3 rect from 2021.5,graph 0 to 2022.5,graph 1 fc rgb band fs solid noborder behind
set arrow 1 from 2005,graph 0 to 2005,graph 1 nohead dt 2 lw 2 lc rgb amber
set arrow 2 from 2023.75,graph 0 to 2023.75,graph 1 nohead dt 2 lw 2 lc rgb amber

set lmargin at screen 0.085 ; set rmargin at screen 0.97
set tmargin at screen 0.89 ; set bmargin at screen 0.53
set format x ''
set yrange [0:7000] ; set ytics 1000
set label 1 'ETS launch 2005' at 2004.8,6700 right textcolor rgb amber
set label 2 'CBAM reporting Oct 2023' at 2023.55,6700 right textcolor rgb amber
set label 3 'crisis' at 2009,350 center textcolor rgb grey
set label 4 'COVID' at 2020,350 center textcolor rgb grey
set label 5 'energy shock' at 2022,1900 center textcolor rgb grey
set label 6 '6,291 kt (2007)' at 2007.4,6700 left textcolor rgb dark
set label 7 '1,464 kt (2025)' at 2025.4,850 right textcolor rgb dark
plot data skip 1 using 1:6 w l lw 4 lc rgb blue

unset label 1 ; unset label 2 ; unset label 3 ; unset label 4 ; unset label 5 ; unset label 6 ; unset label 7
set tmargin at screen 0.47 ; set bmargin at screen 0.15
set format x '%g'
set yrange [0:6500] ; set ytics 1000
set label 8 'EUR 5,660 m (2007)' at 2007.4,6200 left textcolor rgb dark
set label 9 'EUR 1,591 m (2025)' at 2025.4,800 right textcolor rgb dark
plot data skip 1 using 1:3 w l lw 4 lc rgb green
unset multiplot
