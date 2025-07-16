#!/bin/bash

echo "=== RUNNING HEADED MODE TEST (RELIABLE) ==="
echo "This approach consistently bypasses hCaptcha issues"
echo ""

# Run single-stage headed mode
poetry run python tests/exploratory/test_pilot_simple.py \
    --test-suite docs/icims-ats-demo-simple.md \
    --provider github_copilot \
    --model gpt-4.1 \
    --headed-mode

echo ""
echo "✅ Headed mode test completed"
echo "Test report saved to test_report.md"
