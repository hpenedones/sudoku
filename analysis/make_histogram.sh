
cat nbacktracks.txt | sort -n | awk -F" " '{print exp(int(log($1))) }' | uniq -c > histogram.txt

echo "set xlabel '#backtracks to solve (log-scale)';"			                  > plot.gnu
echo "set ylabel 'Frequency';"					                                 >> plot.gnu
echo "set output 'histogram.ps'"  						                         >> plot.gnu
echo "set terminal postscript"						                             >> plot.gnu
echo "set logscale x;"								                             >> plot.gnu
# echo "set logscale y;"								                             >> plot.gnu
echo "plot 'histogram.txt' u 2:1 w boxes t 'Sudoku 17-puzzles' ;" 				 >> plot.gnu
	
gnuplot plot.gnu

