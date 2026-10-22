# Slide 6: German manufacturing 1995-2025, two stacked panels (separate y axes, never combined).
# Data: data/workbook/de_manufacturing_1995_2025.csv (update tab 4.1; Eurostat nama_10_a64, sts_inpr_a). Run from repo root:
#   gnuplot -c graphs/gnuplot/s6_manufacturing.gp
data = ARGC >= 1 ? ARG1 : 'data/workbook/de_manufacturing_1995_2025.csv'
set terminal pngcairo size 1700,1000 font 'Arial,16'
set output 'graphs/out/s6_manufacturing.png'
blue = '#2B5C98' ; green = '#167A67' ; dark = '#263444' ; grey = '#78828C' ; band = '#EEF0F2' ; amber = '#B26A00'
set datafile separator ','
set border 3 lw 2 lc rgb grey
set tics nomirror textcolor rgb dark
unset key
set xrange [1995:2026.2]
set xtics 5 ; set mxtics 5
set grid ytics lc rgb '#E3E6E9' lw 1

set multiplot title 'German manufacturing (NACE C), annual, 1995-2025' font 'Arial,22' textcolor rgb dark

# helper markers shared by both panels
set object 1 rect from 2008.5,graph 0 to 2009.5,graph 1 fc rgb band fs solid noborder behind
set object 2 rect from 2019.5,graph 0 to 2020.5,graph 1 fc rgb band fs solid noborder behind
set arrow 1 from 2005,graph 0 to 2005,graph 1 nohead dt 2 lw 2 lc rgb amber
set arrow 2 from 2023.75,graph 0 to 2023.75,graph 1 nohead dt 2 lw 2 lc rgb amber

# panel A
set lmargin at screen 0.08 ; set rmargin at screen 0.97
set tmargin at screen 0.89 ; set bmargin at screen 0.53
set format x ''
set yrange [60:120]
set ylabel 'Real GVA, volume index (2020 = 100)' textcolor rgb dark
set label 1 'ETS launch 2005' at 2005.2,116 left textcolor rgb amber
set label 2 'CBAM reporting Oct 2023' at 2023.5,116 right textcolor rgb amber
set label 3 '2009' at 2009,64 center textcolor rgb grey
set label 4 '2020' at 2020,64 center textcolor rgb grey
plot data skip 1 using 1:2 w l lw 4 lc rgb blue

# panel B
unset label 1 ; unset label 2 ; unset label 3 ; unset label 4
set tmargin at screen 0.47 ; set bmargin at screen 0.13
set format x '%g'
set yrange [60:120]
set ylabel 'Production index (2021 = 100)' textcolor rgb dark
set xlabel 'Year (2023-25 GVA observations carry a provisional flag at the 2026-10-11 retrieval; see data/eurostat_macro)' noenhanced textcolor rgb grey font 'Arial,14'
plot data skip 1 using 1:3 w l lw 4 lc rgb green
unset multiplot
