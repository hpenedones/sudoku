#!/bin/bash
# Simple benchmark for sudoku solver

echo "Sudoku Solver Performance Benchmark"
echo "===================================="
echo ""

if [ ! -f solver ]; then
    echo "Building solver..."
    make > /dev/null 2>&1
fi

# Test with different difficulty levels
echo "Testing with example puzzles:"
echo ""

echo "1. Easy puzzle (example_linear.txt):"
time ./solver 1 < examples/example_linear.txt > /dev/null
echo ""

echo "2. Hard puzzle (hard_puzzle.txt):"
time ./solver 1 < examples/hard_puzzle.txt > /dev/null
echo ""

# If analysis files exist, test with those
if [ -f analysis/top10.txt ]; then
    echo "3. Hardest puzzle from analysis:"
    time head -1 analysis/top10.txt | ./solver 1 > /dev/null
    echo ""
fi

echo "Benchmark complete!"
