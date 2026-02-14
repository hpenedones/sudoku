
cat nbacktracks.txt | sort -n | awk -F" " '{print exp(int(log($1))) }' | uniq -c > histogram.txt

# Generate histogram using Python matplotlib instead of gnuplot
python3 plot_histogram.py histogram.txt histogram.png

