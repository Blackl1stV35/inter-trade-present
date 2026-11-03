# Figure 2.1: negative production externality, private and social marginal cost (illustrative).
# Invented values, not German data. Demand P = 120 - Q; PMC = 20 + Q; SMC = PMC + 20.
# Market: demand = PMC gives Q = 50, P = 70. Social optimum: demand = SMC gives Q = 40, P = 80.
# Run:  gnuplot -c fig21_externality.gp <OUT_DIR>        (OUT_DIR defaults to figures-rebuilt)
if (ARGC >= 1) OUT_DIR = ARG1; else OUT_DIR = 'figures-rebuilt'

set terminal pngcairo size 2600,1700 enhanced font 'Times New Roman,70'
set output OUT_DIR.'/fig21_externality.png'
DARK = '#263444'; BLUE = '#2B5C98'; TEAL = '#167A67'; RED = '#E8B4B4'

set tmargin screen 0.95
set bmargin screen 0.12
set lmargin screen 0.14
set rmargin screen 0.97
set xrange [0:100]
set yrange [0:230]
set xtics 0,20,100
set ytics 0,20,140
set xlabel 'Quantity (illustrative units)'
set ylabel 'Price / marginal cost (index)' offset 1,0
set grid ytics lc rgb '#e6e6e6'
set key top left Left reverse box samplen 3 spacing 1.3 font 'Times New Roman,70'
set object 10 polygon from 40,60 to 40,80 to 50,90 to 50,70 to 40,60 fc rgb RED fillstyle solid 0.6 noborder
set arrow 1 from 40,0 to 40,80 nohead dt 3 lw 7 lc rgb TEAL
set arrow 2 from 0,80 to 40,80 nohead dt 3 lw 7 lc rgb TEAL
set arrow 3 from 50,0 to 50,70 nohead dt 3 lw 7 lc rgb BLUE
set arrow 4 from 0,70 to 50,70 nohead dt 3 lw 7 lc rgb BLUE
set arrow 5 from 78,100 to 78,120 heads size 1.6,20 lw 11 lc rgb TEAL
set label 2 'Social optimum: Q = 40' at 30,20 left textcolor rgb TEAL
set arrow 6 from 30,24 to 40,80 nohead lw 5 lc rgb TEAL
set label 3 'Market: Q = 50, P = 70' at 62,28 left textcolor rgb BLUE
set arrow 7 from 62,31 to 50,70 nohead lw 5 lc rgb BLUE
set label 4 'Marginal external cost = 20' at 55,150 left textcolor rgb TEAL

plot 120-x lc rgb DARK lw 11 title 'Demand: D', \
     20+x lc rgb BLUE lw 9 dt 2 title 'Private marginal cost: PMC', \
     40+x lc rgb TEAL lw 12 title 'Social marginal cost: SMC = PMC + 20', \
     '-' using 1:2 with points pt 7 ps 3.5 lc rgb TEAL notitle
40 80
50 70
e
