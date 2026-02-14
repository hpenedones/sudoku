#!/bin/bash
# Test script for sudoku solver

set -e

echo "Building solver..."
make clean > /dev/null
make > /dev/null

echo "Running tests..."
echo ""

# Test 1: Grid format
echo "Test 1: Grid format example"
RESULT=$(./solver 2 < examples/example_grid.txt)
EXPECTED_FIRST_LINE="534678912"
FIRST_LINE=$(echo "$RESULT" | head -1)
if [ "$FIRST_LINE" = "$EXPECTED_FIRST_LINE" ]; then
    echo "✓ Grid format test passed"
else
    echo "✗ Grid format test failed"
    echo "  Expected: $EXPECTED_FIRST_LINE"
    echo "  Got: $FIRST_LINE"
    exit 1
fi

# Test 2: Linear format
echo "Test 2: Linear format example"
RESULT=$(./solver 1 < examples/example_linear.txt)
FIRST_LINE=$(echo "$RESULT" | head -1)
if [ "$FIRST_LINE" = "$EXPECTED_FIRST_LINE" ]; then
    echo "✓ Linear format test passed"
else
    echo "✗ Linear format test failed"
    echo "  Expected: $EXPECTED_FIRST_LINE"
    echo "  Got: $FIRST_LINE"
    exit 1
fi

# Test 3: Hard puzzle (just verify it solves without error)
echo "Test 3: Hard puzzle"
RESULT=$(./solver 1 < examples/hard_puzzle.txt)
if [ -n "$RESULT" ]; then
    echo "✓ Hard puzzle test passed"
else
    echo "✗ Hard puzzle test failed"
    exit 1
fi

# Test 4: Error handling - no arguments
echo "Test 4: Error handling (no arguments)"
OUTPUT=$(./solver 2>&1 || true)
if echo "$OUTPUT" | grep -q "Usage:"; then
    echo "✓ Error handling test passed"
else
    echo "✗ Error handling test failed"
    exit 1
fi

echo ""
echo "All tests passed! ✓"
