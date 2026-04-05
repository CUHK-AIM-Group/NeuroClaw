#!/bin/bash
# Benchmark Test Case 4: Run Grader
# Usage: ./run_benchmark.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Benchmark Test Case 4: Conn Tool"
echo "=========================================="
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
