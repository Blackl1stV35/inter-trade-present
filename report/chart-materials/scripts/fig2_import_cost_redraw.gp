# Redrawn Fig. 2 (slide 5): carbon-related import cost with PARTIAL pass-through and a possible domestic supply shift.
# Qualitative: curve parameters are drawing aids only and no numbers appear on the axes.
#   D: P = 100 - Q      S: P = 20 + Q      S': P = 30 + Q      P_M0 = 40      P_M1 = 50      full carbon cost c = 16 -> P_M0 + c = 56
#   Domestic output is drawn unchanged because the supply shift (10) equals the import price rise (10); the panel says output may rise, stay or fall.
#   Full pass-through (56) would leave imports positive (Q_S = 36, Q_D = 44).
# Run from the repo root:  gnuplot -c graphs/gnuplot/fig2_import_cost_redraw.gp png   (or: svg)
fmt = (ARGC >= 1) ? ARG1 : 'png'
if (fmt eq 'svg') { set terminal svg size 1840,940 font 'TH Sarabun New,22' ; set output 'graphs/out/fig2_import_cost_redraw.svg' }
else { set terminal pngcairo size 1840,940 font 'TH Sarabun New,22' ; set output 'graphs/out/fig2_import_cost_redraw.png' }

blue = '#2B5C98' ; green = '#167A67' ; dark = '#263444' ; grey = '#78828C' ; amber = '#B26A00'

set lmargin at screen 0.125 ; set rmargin at screen 0.60 ; set tmargin at screen 0.90 ; set bmargin at screen 0.19
set border 3 lw 2 lc rgb grey
set tics nomirror textcolor rgb dark
unset key ; unset grid
set xrange [0:100] ; set yrange [0:112]
set samples 400
set xtics ("Q_{S0} = Q_{S1}" 20, "Q_{D1}" 50, "Q_{D0}" 60)
set ytics ("P_{M0}" 40, "P_{M1}" 50, "P_{M0} + c" 56)
# title and axis names as screen-positioned labels (TH Sarabun New metrics push set title/xlabel/ylabel off the canvas)
set label 30 'Redrawn Fig. 2: carbon-related import cost, partial pass-through' at screen 0.125,0.955 font 'TH Sarabun New,27' textcolor rgb dark
set label 31 'Quantity of steel (qualitative)' at screen 0.36,0.075 center textcolor rgb dark
set label 32 'Price (qualitative)' at screen 0.012,0.55 center rotate by 90 textcolor rgb dark
set style textbox 1 opaque noborder fc rgb 'white'

# curves (clipped so end labels fit)
D(x)  = 100 - x
S0(x) = (x <= 85) ? 20 + x : 1/0
S1(x) = (x <= 75) ? 30 + x : 1/0

# vertical guides
set arrow 1 from 20,0 to 20,50 nohead dt 3 lw 2 lc rgb blue
set arrow 2 from 50,0 to 50,50 nohead dt 3 lw 2 lc rgb green
set arrow 3 from 60,0 to 60,40 nohead dt 3 lw 2 lc rgb blue
# imports before / after
set arrow 4 from 20,14 to 60,14 heads size 2.5,20 lw 3 lc rgb blue
set arrow 5 from 20,6 to 50,6 heads size 2.5,20 lw 3 lc rgb green
set label 1 'Imports before' at 40,18 center textcolor rgb blue
set label 2 'Imports after (drawn smaller)' at 53,6 left front boxed bs 1 textcolor rgb green
# price rise by less than the full carbon cost
set arrow 6 from 90,40 to 90,50 heads size 2.5,20 lw 3 lc rgb green
set label 3 'less than full cost' at 88.5,45 right textcolor rgb green
set label 4 'full pass-through (not assumed)' at 99,60 right boxed bs 1 textcolor rgb grey
# curve labels
set label 5 'D' at 5,104 textcolor rgb dark
set label 6 'S' at 86,106 left textcolor rgb blue
set label 7 "S'" at 75,108 center textcolor rgb green

# right-hand reading panel (screen coordinates)
set label 10 'What moves' at screen 0.63,0.84 font 'TH Sarabun New,27' textcolor rgb dark
set label 11 'Landed import price: P_{M0} to P_{M1}, up by' at screen 0.63,0.775 textcolor rgb green
set label 19 'less than the full carbon cost c' at screen 0.63,0.735 textcolor rgb green
set label 12 "Domestic supply may shift to S' if ETS, energy" at screen 0.63,0.675 textcolor rgb green
set label 20 'and capital costs rise (size not evidenced)' at screen 0.63,0.635 textcolor rgb green
set label 13 'Quantity demanded falls along D (Q_{D0} to Q_{D1})' at screen 0.63,0.575 textcolor rgb dark
set label 14 'Domestic output: may rise, stay or fall' at screen 0.63,0.515 textcolor rgb amber
set label 21 '(drawn unchanged)' at screen 0.63,0.475 textcolor rgb amber
set label 15 'Import gap: drawn smaller, not guaranteed' at screen 0.63,0.415 textcolor rgb amber
set label 16 'Short run, static, one point in time.' at screen 0.63,0.325 textcolor rgb grey
set label 17 'Steel-using manufacturers face the cost' at screen 0.63,0.285 textcolor rgb grey
set label 22 'rise downstream (not drawn).' at screen 0.63,0.245 textcolor rgb grey
set label 18 'ILLUSTRATIVE | qualitative curves; not observed German data' at screen 0.125,0.03 textcolor rgb grey

plot D(x) w l lw 4 lc rgb dark, \
     S0(x) w l lw 4 lc rgb blue, \
     S1(x) w l lw 4 dt 2 lc rgb green, \
     40 w l lw 3 lc rgb blue, \
     50 w l lw 3 lc rgb green, \
     (x >= 44 ? 56 : 1/0) w l lw 2 dt 3 lc rgb grey
