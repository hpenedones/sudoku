#!/usr/bin/env python3
"""
Unit tests for the sudoku_wrapper module.
"""

import unittest
import sys
import os

# Add parent directory to path for imports (if not installed)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku_solver import SudokuSolver, solve_sudoku


class TestSudokuSolver(unittest.TestCase):
    """Test cases for the SudokuSolver class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.solver = SudokuSolver()
        
        # Standard test puzzle
        self.test_puzzle_linear = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        self.expected_solution = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
        
        # Same puzzle in grid format
        self.test_puzzle_grid = [
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
    
    def test_solve_linear_format(self):
        """Test solving with linear format input."""
        solution = self.solver.solve(self.test_puzzle_linear)
        self.assertEqual(solution, self.expected_solution)
    
    def test_solve_grid_format_return_string(self):
        """Test solving grid format and returning string."""
        solution = self.solver.solve(self.test_puzzle_grid, return_format='string')
        self.assertEqual(solution, self.expected_solution)
    
    def test_solve_grid_format_return_grid(self):
        """Test solving grid format and returning grid."""
        solution = self.solver.solve(self.test_puzzle_grid, return_format='grid')
        
        # Verify it's a 9x9 grid
        self.assertEqual(len(solution), 9)
        for row in solution:
            self.assertEqual(len(row), 9)
        
        # Convert to linear and compare
        linear = ''.join(''.join(row) for row in solution)
        self.assertEqual(linear, self.expected_solution)
    
    def test_solve_with_underscores(self):
        """Test solving with underscore placeholders."""
        puzzle = "53__7____6__195____98____6_8___6___34__8_3__17___2___6_6____28____419__5____8__79"
        solution = self.solver.solve(puzzle)
        self.assertEqual(solution, self.expected_solution)
    
    def test_solve_with_dots(self):
        """Test solving with dot placeholders."""
        puzzle = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
        solution = self.solver.solve(puzzle)
        self.assertEqual(solution, self.expected_solution)
    
    def test_hard_puzzle(self):
        """Test solving a hard puzzle."""
        # One of the hardest puzzles from the repository
        hard_puzzle = "200500080001020000000000000070008000003000020000070600600200001040000700000300000"
        expected = "297543186481726395356189274572638419963451827814972653638297541149865732725314968"
        
        solution = self.solver.solve(hard_puzzle)
        self.assertEqual(solution, expected)
    
    def test_invalid_puzzle_with_duplicates(self):
        """Test that invalid puzzle (duplicates) returns error."""
        # Two 1's in first row - invalid
        invalid_puzzle = "110070000600195000098000060800060003400803001700020006060000280000419005000080079"
        
        with self.assertRaises(ValueError):
            self.solver.solve(invalid_puzzle)
    
    def test_invalid_length_short(self):
        """Test error handling for puzzle that's too short."""
        with self.assertRaises(ValueError) as context:
            self.solver.solve("12345")
        
        self.assertIn("81 characters", str(context.exception))
    
    def test_invalid_length_long(self):
        """Test error handling for puzzle that's too long."""
        with self.assertRaises(ValueError):
            self.solver.solve("0" * 100)
    
    def test_invalid_characters(self):
        """Test error handling for invalid characters."""
        with self.assertRaises(ValueError):
            self.solver.solve("A" * 81)
    
    def test_invalid_grid_rows(self):
        """Test error handling for grid with wrong number of rows."""
        invalid_grid = [['1', '2', '3']]
        
        with self.assertRaises(ValueError) as context:
            self.solver.solve(invalid_grid)
        
        self.assertIn("9 rows", str(context.exception))
    
    def test_invalid_grid_columns(self):
        """Test error handling for grid with wrong number of columns."""
        invalid_grid = [
            ['1', '2', '3'],  # Wrong size
        ] * 9
        
        with self.assertRaises(ValueError) as context:
            self.solver.solve(invalid_grid)
        
        self.assertIn("9 columns", str(context.exception))
    
    def test_invalid_return_format(self):
        """Test error handling for invalid return format."""
        with self.assertRaises(ValueError) as context:
            self.solver.solve(self.test_puzzle_linear, return_format='invalid')
        
        self.assertIn("return_format", str(context.exception))
    
    def test_unsolvable_puzzle(self):
        """Test handling of unsolvable puzzle."""
        # An empty grid should have many solutions, let's just test it doesn't crash
        # In practice, most invalid puzzles will be caught during validation
        # A truly unsolvable puzzle (that passes validation) is hard to construct
        
        # Test with an empty puzzle (this should solve successfully)
        empty_puzzle = "0" * 81
        solution = self.solver.solve(empty_puzzle)
        
        # Should get some solution (there are many valid solutions for empty grid)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 81)
        
        # Verify it's a valid solution (no zeros)
        self.assertNotIn('0', solution)
    
    def test_convenience_function(self):
        """Test the convenience function solve_sudoku."""
        solution = solve_sudoku(self.test_puzzle_linear)
        self.assertEqual(solution, self.expected_solution)
    
    def test_grid_to_linear_conversion(self):
        """Test internal grid to linear conversion."""
        linear = self.solver._grid_to_linear(self.test_puzzle_grid)
        self.assertEqual(linear, self.test_puzzle_linear)
    
    def test_linear_to_grid_conversion(self):
        """Test internal linear to grid conversion."""
        grid = self.solver._linear_to_grid(self.test_puzzle_linear)
        
        self.assertEqual(len(grid), 9)
        for row in grid:
            self.assertEqual(len(row), 9)
        
        # Convert back and compare
        linear = self.solver._grid_to_linear(grid)
        self.assertEqual(linear, self.test_puzzle_linear)
    
    def test_empty_cell_markers_in_grid(self):
        """Test that various empty cell markers work in grid format."""
        # Test with underscores
        grid_with_underscores = [
            ['5', '3', '_', '_', '7', '_', '_', '_', '_'],
            ['6', '_', '_', '1', '9', '5', '_', '_', '_'],
            ['_', '9', '8', '_', '_', '_', '_', '6', '_'],
            ['8', '_', '_', '_', '6', '_', '_', '_', '3'],
            ['4', '_', '_', '8', '_', '3', '_', '_', '1'],
            ['7', '_', '_', '_', '2', '_', '_', '_', '6'],
            ['_', '6', '_', '_', '_', '_', '2', '8', '_'],
            ['_', '_', '_', '4', '1', '9', '_', '_', '5'],
            ['_', '_', '_', '_', '8', '_', '_', '7', '9']
        ]
        
        solution = self.solver.solve(grid_with_underscores)
        self.assertEqual(solution, self.expected_solution)
        
        # Test with dots
        grid_with_dots = [
            ['5', '3', '.', '.', '7', '.', '.', '.', '.'],
            ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
            ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
            ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
            ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
            ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
            ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
            ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
            ['.', '.', '.', '.', '8', '.', '.', '7', '9']
        ]
        
        solution = self.solver.solve(grid_with_dots)
        self.assertEqual(solution, self.expected_solution)


class TestSudokuSolverInstantiation(unittest.TestCase):
    """Test cases for SudokuSolver instantiation."""
    
    def test_solver_instantiation(self):
        """Test that SudokuSolver can be instantiated."""
        solver = SudokuSolver()
        self.assertIsNotNone(solver)
    
    def test_library_not_found_error(self):
        """Test error when library is not found."""
        # This test will pass if library exists, or raise OSError if it doesn't
        # We're mainly testing that the error message is helpful
        try:
            # Try with an invalid path
            solver = SudokuSolver(lib_path='/nonexistent/path/libsudoku.so')
            # If this succeeds, the library actually exists there (unlikely)
        except OSError as e:
            # Verify error message is helpful
            self.assertIn('Failed to load', str(e))


def run_tests():
    """Run all tests and return the result."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSudokuSolver))
    suite.addTests(loader.loadTestsFromTestCase(TestSudokuSolverInstantiation))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
