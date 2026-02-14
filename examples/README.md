# Sudoku Puzzle Examples

This directory contains example Sudoku puzzles for testing the solver.

## Files

- `example_grid.txt` - Example puzzle in grid format (9x9 grid with '_' for empty cells)
- `example_linear.txt` - Example puzzle in linear format (81 characters, '0' for empty cells)
- `hard_puzzle.txt` - A challenging puzzle that requires more backtracking

## Usage

Test with grid format:
```bash
./solver 2 < examples/example_grid.txt
```

Test with linear format:
```bash
./solver 1 < examples/example_linear.txt
```
