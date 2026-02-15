#!/usr/bin/env python3
"""
Unit tests for the sudoku module (stateless API).
"""

import unittest
import sys
import os

# Add parent directory to path for imports (if not installed)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sudoku


class TestSudokuSolve(unittest.TestCase):
    """Test cases for the sudoku.solve() function."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Standard test puzzle
        self.test_puzzle_linear = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        self.expected_solution = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
        
        # Same puzzle in grid format (list)
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
        
        # Same puzzle in grid format (multi-line string)
        self.test_puzzle_grid_str = """53__7____
6__195___
_98____6_
8___6___3
4__8_3__1
7___2___6
_6____28_
___419__5
____8__79"""
    
    def test_solve_linear_format(self):
        """Test solving with linear format input."""
        solution = sudoku.solve(self.test_puzzle_linear)
        self.assertEqual(solution, self.expected_solution)
    
    def test_solve_grid_format_list(self):
        """Test solving grid format (list) input."""
        solution = sudoku.solve(self.test_puzzle_grid)
        self.assertEqual(solution, self.expected_solution)
    
    def test_solve_grid_format_string(self):
        """Test solving grid format (multi-line string) input."""
        solution = sudoku.solve(self.test_puzzle_grid_str)
        self.assertEqual(solution, self.expected_solution)
    
    def test_solve_with_underscores(self):
        """Test solving with underscore placeholders."""
        puzzle = "53__7____6__195____98____6_8___6___34__8_3__17___2___6_6____28____419__5____8__79"
        solution = sudoku.solve(puzzle)
        self.assertEqual(solution, self.expected_solution)
    
    def test_solve_with_dots(self):
        """Test solving with dot placeholders."""
        puzzle = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"
        solution = sudoku.solve(puzzle)
        self.assertEqual(solution, self.expected_solution)
    
    def test_hard_puzzle(self):
        """Test solving a hard puzzle."""
        # One of the hardest puzzles from the repository
        hard_puzzle = "200500080001020000000000000070008000003000020000070600600200001040000700000300000"
        expected = "297543186481726395356189274572638419963451827814972653638297541149865732725314968"
        
        solution = sudoku.solve(hard_puzzle)
        self.assertEqual(solution, expected)
    
    def test_invalid_puzzle_with_duplicates(self):
        """Test that invalid puzzle (duplicates) raises error."""
        # Two 1's in first row - invalid
        invalid_puzzle = "110070000600195000098000060800060003400803001700020006060000280000419005000080079"
        
        with self.assertRaises(ValueError):
            sudoku.solve(invalid_puzzle)
    
    def test_invalid_length_short(self):
        """Test error handling for puzzle that's too short."""
        with self.assertRaises(ValueError) as context:
            sudoku.solve("12345")
        
        self.assertIn("81 characters", str(context.exception))
    
    def test_invalid_length_long(self):
        """Test error handling for puzzle that's too long."""
        with self.assertRaises(ValueError):
            sudoku.solve("0" * 100)
    
    def test_invalid_characters(self):
        """Test error handling for invalid characters."""
        with self.assertRaises(ValueError):
            sudoku.solve("A" * 81)
    
    def test_invalid_grid_rows(self):
        """Test error handling for grid with wrong number of rows."""
        invalid_grid = [['1', '2', '3']]
        
        with self.assertRaises(ValueError) as context:
            sudoku.solve(invalid_grid)
        
        self.assertIn("9 rows", str(context.exception))
    
    def test_invalid_grid_columns(self):
        """Test error handling for grid with wrong number of columns."""
        invalid_grid = [
            ['1', '2', '3'],  # Wrong size
        ] * 9
        
        with self.assertRaises(ValueError) as context:
            sudoku.solve(invalid_grid)
        
        self.assertIn("9 columns", str(context.exception))
    
    def test_empty_puzzle(self):
        """Test handling of empty puzzle."""
        # An empty grid should have many solutions
        empty_puzzle = "0" * 81
        solution = sudoku.solve(empty_puzzle)
        
        # Should get some solution (there are many valid solutions for empty grid)
        self.assertIsNotNone(solution)
        self.assertEqual(len(solution), 81)
        
        # Verify it's a valid solution (no zeros)
        self.assertNotIn('0', solution)
    
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
        
        solution = sudoku.solve(grid_with_underscores)
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
        
        solution = sudoku.solve(grid_with_dots)
        self.assertEqual(solution, self.expected_solution)
    
    def test_stateless_multiple_calls(self):
        """Test that multiple calls work (stateless behavior)."""
        # First puzzle
        solution1 = sudoku.solve(self.test_puzzle_linear)
        self.assertEqual(solution1, self.expected_solution)
        
        # Second puzzle (different)
        puzzle2 = "200500080001020000000000000070008000003000020000070600600200001040000700000300000"
        expected2 = "297543186481726395356189274572638419963451827814972653638297541149865732725314968"
        solution2 = sudoku.solve(puzzle2)
        self.assertEqual(solution2, expected2)
        
        # Solve first puzzle again - should still work
        solution1_again = sudoku.solve(self.test_puzzle_linear)
        self.assertEqual(solution1_again, self.expected_solution)


class TestImportAPI(unittest.TestCase):
    """Test that the import API works as expected."""
    
    def test_import_sudoku(self):
        """Test that we can import sudoku module."""
        import sudoku
        self.assertTrue(hasattr(sudoku, 'solve'))
    
    def test_solve_function_available(self):
        """Test that solve function is available at module level."""
        import sudoku
        self.assertTrue(callable(sudoku.solve))
    
    def test_version_available(self):
        """Test that version information is available."""
        import sudoku
        self.assertTrue(hasattr(sudoku, '__version__'))
        self.assertIsInstance(sudoku.__version__, str)


def run_tests():
    """Run all tests and return the result."""
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSudokuSolve))
    suite.addTests(loader.loadTestsFromTestCase(TestImportAPI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
