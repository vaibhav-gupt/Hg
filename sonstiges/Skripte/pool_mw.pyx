# Command script saved by PyXPlot 0.8.3
# Timestamp: Mon Jan 24 01:25:09 2011
# User: Arne Babenhauserheide

set ylabel "Wahrscheinlichkeit"
set xlabel "Mindestwurf"
set title "Wahrscheinlichkeiten in Additivsystemen"
set style data lines
set output "pool_mw.png"
set term png
plot "pool_mw.dat" using 2:3 select ($1==1) title "1w6", "pool_mw.dat" using 2:3 select ($1==2) title "2w6", "pool_mw.dat" using 2:3 select ($1==3) title "3w6", "pool_mw.dat" using 2:3 select ($1==4) title "4w6", "pool_mw.dat" using 2:3 select ($1==5) title "5w6"
set term x11
replot
