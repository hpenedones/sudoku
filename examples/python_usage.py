#!/usr/bin/env python3
"""
Example usage of the Python sudoku solver wrapper.

This script demonstrates various ways to use the sudoku solver
from Python code.
"""

import sys
import os

# Add parent directory to path for imports (if not installed)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku_solver import SudokuSolver, solve_sudoku


def example_linear_format():
    """Example using linear format (81-character string)."""
    print("=" * 60)
    print("Example 1: Linear Format (81-character string)")
    print("=" * 60)
    
    # This is the example puzzle from the repository
    puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    
    print(f"\nPuzzle:\n{puzzle}")
    
    # Solve using the convenience function
    solution = solve_sudoku(puzzle)
    
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


def example_grid_format():
    """Example using grid format (9x9 list of lists)."""
    print("\n" + "=" * 60)
    print("Example 2: Grid Format (9x9 list)")
    print("=" * 60)
    
    # Same puzzle as above, but in grid format
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
    
    # Solve and return as grid
    solver = SudokuSolver()
    solution = solver.solve(puzzle, return_format='grid')
    
    if solution:
        print("\nSolution:")
        for i, row in enumerate(solution):
            formatted = f"{' '.join(row[0:3])} | {' '.join(row[3:6])} | {' '.join(row[6:9])}"
            print(formatted)
            if i in (2, 5):
                print("------+-------+------")
    else:
        print("No solution found!")


def example_with_underscores():
    """Example using underscores for empty cells."""
    print("\n" + "=" * 60)
    print("Example 3: Using Underscores for Empty Cells")
    print("=" * 60)
    
    # You can use underscores, dots, or zeros for empty cells
    puzzle = "53__7____6__195____98____6_8___6___34__8_3__17___2___6_6____28____419__5____8__79"
    
    print(f"\nPuzzle:\n{puzzle}")
    
    solution = solve_sudoku(puzzle)
    
    if solution:
        print(f"\nSolution:\n{solution}")
    else:
        print("No solution found!")


def example_hard_puzzle():
    """Example with a harder puzzle."""
    print("\n" + "=" * 60)
    print("Example 4: Harder Puzzle")
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
    solution = solve_sudoku(puzzle)
    
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


def example_no_solution():
    """Example with an unsolvable puzzle."""
    print("\n" + "=" * 60)
    print("Example 5: Unsolvable Puzzle")
    print("=" * 60)
    
    # This puzzle has two 1's in the first row - invalid!
    puzzle = "110070000600195000098000060800060003400803001700020006060000280000419005000080079"
    
    print(f"\nPuzzle (invalid - two 1's in first row):\n{puzzle}")
    
    try:
        solution = solve_sudoku(puzzle)
        
        if solution:
            print(f"\nSolution:\n{solution}")
        else:
            print("\nNo solution found! (as expected for an invalid puzzle)")
    except ValueError as e:
        print(f"\nError: {e}")


def example_error_handling():
    """Example showing error handling."""
    print("\n" + "=" * 60)
    print("Example 6: Error Handling")
    print("=" * 60)
    
    solver = SudokuSolver()
    
    # Test with invalid length
    print("\nTest 1: Puzzle too short")
    try:
        solver.solve("12345")
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    # Test with invalid characters
    print("\nTest 2: Invalid characters")
    try:
        solver.solve("A" * 81)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    # Test with wrong grid dimensions
    print("\nTest 3: Invalid grid dimensions")
    try:
        solver.solve([['1', '2', '3']])  # Wrong size
    except ValueError as e:
        print(f"Caught expected error: {e}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Python Sudoku Solver Examples")
    print("=" * 60)
    
    example_linear_format()
    example_grid_format()
    example_with_underscores()
    example_hard_puzzle()
    example_no_solution()
    example_error_handling()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
