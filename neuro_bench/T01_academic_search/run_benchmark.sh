#!/bin/bash
# Benchmark Test Case 1: Run Test and Grade
# Usage: ./run_benchmark.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=========================================="
echo "Benchmark Test Case 1: Academic Search"
echo "=========================================="
echo

# Run the test
echo "Running test_case.py..."
python "$SCRIPT_DIR/test_case.py"

echo
echo "Running grader.py..."
python "$SCRIPT_DIR/grader.py"

GRADER_EXIT=$?

echo
echo "=========================================="
if [ $GRADER_EXIT -eq 0 ]; then
    echo "✅ TEST PASSED"
else
    echo "❌ TEST FAILED"
fi
echo "=========================================="

exit $GRADER_EXIT
