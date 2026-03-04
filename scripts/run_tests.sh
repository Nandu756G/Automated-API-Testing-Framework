#!/usr/bin/env bash
# =============================================================================
# run_tests.sh — Execute the full API test suite and generate HTML report
# =============================================================================
# Usage:
#   bash scripts/run_tests.sh            # run all tests (default)
#   bash scripts/run_tests.sh -k posts   # run only post tests
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
REPORT_DIR="reports"
REPORT_FILE="${REPORT_DIR}/report.html"
TESTS_DIR="tests"

# Ensure the reports directory exists
mkdir -p "${REPORT_DIR}"

echo "=========================================="
echo "  API Test Automation Framework"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# ---------------------------------------------------------------------------
# Run pytest
# ---------------------------------------------------------------------------
pytest "${TESTS_DIR}/" \
  --html="${REPORT_FILE}" \
  --self-contained-html \
  -v \
  --tb=short \
  "$@"

EXIT_CODE=$?

echo ""
echo "=========================================="
if [ "${EXIT_CODE}" -eq 0 ]; then
  echo "  ✅  All tests passed!"
else
  echo "  ❌  Some tests failed. Exit code: ${EXIT_CODE}"
fi
echo "  📄 HTML report: ${REPORT_FILE}"
echo "=========================================="

exit "${EXIT_CODE}"
