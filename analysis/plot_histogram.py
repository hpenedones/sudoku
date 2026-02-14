#!/usr/bin/env python3
"""
Generate histogram of Sudoku backtrack counts.
Replaces gnuplot with matplotlib for simpler visualization.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import sys

# Constants for bar width calculations
ZERO_BAR_WIDTH = 0.5  # Fixed width for bars at x=0 (not visible on log scale)
BAR_SPACING_FACTOR = 0.8  # Use 80% of spacing between adjacent bars

def read_histogram_data(filename='histogram.txt'):
    """Read histogram data from file."""
    x_values = []
    y_values = []
    
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                frequency = int(parts[0])
                backtracks = float(parts[1])
                x_values.append(backtracks)
                y_values.append(frequency)
    
    return x_values, y_values

def plot_histogram(x_values, y_values, output_file='histogram.png'):
    """Create and save histogram plot."""
    plt.figure(figsize=(10, 6))
    
    # Calculate widths for logarithmic scale
    # For each bar, use 80% of the spacing to the next value (or use the value itself for the last bar)
    widths = []
    for i in range(len(x_values)):
        if x_values[i] == 0:
            # For zero, use a small fixed width
            widths.append(ZERO_BAR_WIDTH)
        elif i < len(x_values) - 1:
            # Use spacing factor times the distance to next point
            widths.append((x_values[i+1] - x_values[i]) * BAR_SPACING_FACTOR)
        else:
            # For last bar, use spacing factor times the value itself
            widths.append(x_values[i] * BAR_SPACING_FACTOR)
    
    # Create bar plot
    plt.bar(x_values, y_values, width=widths, align='edge', 
            edgecolor='black', linewidth=0.5, label='Sudoku 17-puzzles')
    
    # Set logarithmic scale for x-axis
    plt.xscale('log')
    
    # Labels and title
    plt.xlabel('#backtracks to solve (log-scale)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3, which='both')
    
    # Save figure
    plt.tight_layout()
    plt.savefig(output_file, dpi=100)
    print(f"Histogram saved to {output_file}")

def main():
    """Main function."""
    input_file = 'histogram.txt'
    output_file = 'histogram.png'
    
    # Allow command line arguments for input/output files
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    try:
        x_values, y_values = read_histogram_data(input_file)
        plot_histogram(x_values, y_values, output_file)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
