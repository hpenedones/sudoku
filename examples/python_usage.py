#!/usr/bin/env python3
"""
Example usage of the Python sudoku solver.

This script demonstrates various ways to use the sudoku.solve() function
from Python code.
"""

import sys
import os

# Add parent directory to path for imports (if not installed)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sudoku


def example_linear_format():
    """Example using linear format (81-character string)."""
    print("=" * 60)
    print("Example 1: Linear Format (81-character string)")
    print("=" * 60)
    
    # This is the example puzzle from the repository
    puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    
    print(f"\nPuzzle:\n{puzzle}")
    
    # Solve using the function
    solution = sudoku.solve(puzzle)
    
    if solution:
        print(f"\nSolution:\n{solution}")
        
        # Display in a more readable format
        print("\nFormatted Solution:")
        for i in range(9):
            row = solution[i*9:(i+1)*9]
            # Add separators for 3x3 blocks
            formatted = f"{row[0:3]} {row[3:6]} {row[6:9]}"
            print(formatted)
            if i in (2, 5):
                print()
    else:
        print("No solution found!")


def example_grid_format_string():
    """Example using grid format (multi-line string)."""
    print("\n" + "=" * 60)
    print("Example 2: Grid Format (multi-line string)")
    print("=" * 60)
    
    # Same puzzle in grid format with underscores
    puzzle_grid = """53__7____
6__195___
_98____6_
8___6___3
4__8_3__1
7___2___6
_6____28_
___419__5
____8__79"""
    
    print(f"\nPuzzle:\n{puzzle_grid}")
    
    # Solve
    solution = sudoku.solve(puzzle_grid)
    
    if solution:
        print(f"\nSolution (linear format):\n{solution}")
        
        # Display as grid
        print("\nSolution (grid format):")
        for i in range(9):
            row = solution[i*9:(i+1)*9]
            formatted = f"{row[0:3]} | {row[3:6]} | {row[6:9]}"
            print(formatted)
            if i in (2, 5):
                print("-----+-------+------")
    else:
        print("No solution found!")


def example_grid_format_list():
    """Example using grid format (9x9 list of lists)."""
    print("\n" + "=" * 60)
    print("Example 3: Grid Format (9x9 list)")
    print("=" * 60)
    
    # Same puzzle as above, but in list format
    puzzle = [
        ['5', '3', '0', '0', '7', '0', '0', '0', '0'],
        ['6', '0', '0', '1', '9', '5', '0', '0', '0'],
        ['0', '9', '8', '0', '0', '0', '0', '6', '0'],
        ['8', '0', '0', '0', '6', '0', '0', '0', '3'],
        ['4', '0', '0', '8', '0', '3', '0', '0', '1'],
        ['7', '0', '0', '0', '2', '0', '0', '0', '6'],
        ['0', '6', '0', '0', '0', '0', '2', '8', '0'],
        ['0', '0', '0', '4', '1', '9', '0', '0', '5'],
        ['0', '0', '0', '0', '8', '0', '0', '7', '9']
    ]
    
    print("\nPuzzle:")
    for row in puzzle:
        formatted = f"{' '.join(row[0:3])} | {' '.join(row[3:6])} | {' '.join(row[6:9])}"
        print(formatted)
    
    # Solve
    solution = sudoku.solve(puzzle)
    
    if solution:
        print(f"\nSolution (linear format):\n{solution}")
        
        # Display as grid
        print("\nSolution (grid format):")
        for i in range(9):
            row = solution[i*9:(i+1)*9]
            formatted = f"{row[0:3]} | {row[3:6]} | {row[6:9]}"
            print(formatted)
            if i in (2, 5):
                print("-----+-------+------")
    else:
        print("No solution found!")


def example_with_underscores():
    """Example using underscores for empty cells."""
    print("\n" + "=" * 60)
    print("Example 4: Using Underscores for Empty Cells")
    print("=" * 60)
    
    # You can use underscores, dots, or zeros for empty cells
    puzzle = "53__7____6__195____98____6_8___6___34__8_3__17___2___6_6____28____419__5____8__79"
    
    print(f"\nPuzzle:\n{puzzle}")
    
    solution = sudoku.solve(puzzle)
    
    if solution:
        print(f"\nSolution:\n{solution}")
    else:
        print("No solution found!")


def example_hard_puzzle():
    """Example with a harder puzzle."""
    print("\n" + "=" * 60)
    print("Example 5: Harder Puzzle")
    print("=" * 60)
    
    # One of the hardest puzzles (from the repository analysis)
    puzzle = "200500080001020000000000000070008000003000020000070600600200001040000700000300000"
    
    print(f"\nPuzzle:\n{puzzle}")
    print("\nPuzzle (formatted):")
    for i in range(9):
        row = puzzle[i*9:(i+1)*9]
        formatted = f"{row[0:3]} {row[3:6]} {row[6:9]}"
        print(formatted)
        if i in (2, 5):
            print()
    
    print("\nSolving (this may take a moment for hard puzzles)...")
    solution = sudoku.solve(puzzle)
    
    if solution:
        print(f"\nSolution:\n{solution}")
        print("\nSolution (formatted):")
        for i in range(9):
            row = solution[i*9:(i+1)*9]
            formatted = f"{row[0:3]} {row[3:6]} {row[6:9]}"
            print(formatted)
            if i in (2, 5):
                print()
    else:
        print("No solution found!")


def example_error_handling():
    """Example showing error handling."""
    print("\n" + "=" * 60)
    print("Example 6: Error Handling")
    print("=" * 60)
    
    # Test with invalid length
    print("\nTest 1: Puzzle too short")
    try:
        sudoku.solve("12345")
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    # Test with invalid characters
    print("\nTest 2: Invalid characters")
    try:
        sudoku.solve("A" * 81)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    # Test with invalid puzzle (constraint violation)
    print("\nTest 3: Invalid puzzle (two 1's in first row)")
    try:
        invalid_puzzle = "110070000600195000098000060800060003400803001700020006060000280000419005000080079"
        result = sudoku.solve(invalid_puzzle)
        if result is None:
            print("No solution found (as expected for invalid puzzle)")
        else:
            print(f"Unexpectedly found a solution: {result}")
    except ValueError as e:
        print(f"Caught error: {e}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Python Sudoku Solver Examples")
    print("=" * 60)
    
    example_linear_format()
    example_grid_format_string()
    example_grid_format_list()
    example_with_underscores()
    example_hard_puzzle()
    example_error_handling()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
