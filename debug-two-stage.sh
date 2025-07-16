#!/bin/bash

echo "=== DEBUGGING TWO-STAGE MODE ==="
echo "This script will help debug the two-stage login issue"
echo "Using Playwright MCP --storage-state feature for session persistence"
echo ""

# Clean up any existing storage file
rm -f browser_storage.json

echo "1. Running Stage 1 (Login in headed mode)..."
echo "   - Browser will open in headed mode"
echo "   - Login credentials will be automatically saved to browser_storage.json"
echo "   - Check if browser_storage.json is created after login"
echo ""

# Run the two-stage mode
poetry run python tests/exploratory/test_pilot_simple.py \
    --test-suite docs/icims-ats-demo-simple.md \
    --provider github_copilot \
    --model gpt-4.1 \
    --two-stage-mode \
    --storage-file browser_storage.json

echo ""
echo "=== POST-EXECUTION ANALYSIS ==="

# Check if storage file was created/updated
if [ -f "browser_storage.json" ]; then
    echo "✅ browser_storage.json exists"
    echo "File size: $(ls -lh browser_storage.json | awk '{print $5}')"
    
    # Check if it has meaningful content
    if grep -q '"cookies":\[' browser_storage.json && [ "$(grep -o '"cookies":\[[^]]*\]' browser_storage.json | grep -c ',')" -gt 0 ]; then
        echo "✅ Storage file contains cookies - login was successful!"
        echo "File content preview:"
        head -c 300 browser_storage.json
        echo "..."
        echo ""
        echo "✅ Two-stage mode should work! The authentication state was saved."
    else
        echo "⚠️  Storage file exists but appears to have no cookies"
        echo "This suggests login may not have completed successfully"
        echo "File content:"
        cat browser_storage.json
    fi
else
    echo "❌ browser_storage.json was NOT created"
    echo "This indicates a fundamental issue with the Playwright MCP --storage-state feature"
fi

echo ""
echo "=== ALTERNATIVE APPROACHES ==="
echo "If two-stage mode isn't working, try:"
echo ""
echo "1. Enhanced two-stage with better timing:"
echo "   ./debug-enhanced-two-stage.sh"
echo ""
echo "2. Storage state validation test:"
echo "   python test_storage_validation.py"
echo ""
echo "3. Single-stage headed mode (no captcha issues):"
echo "   poetry run python tests/exploratory/test_pilot_simple.py \\"
echo "     --test-suite docs/icims-ats-demo-simple.md \\"
echo "     --provider github_copilot \\"
echo "     --model gpt-4.1 \\"
echo "     --headed-mode"
echo ""
echo "4. Common storage state troubleshooting:"
echo "   - Check timing: Login may complete before storage is saved"
echo "   - Check path: Ensure storage file path is correct and writable"
echo "   - Check MCP version: Update to latest Playwright MCP"
echo "   - Check website behavior: Some sites behave differently when automated"
echo ""
echo "2. Single-stage headless mode (original, may hit captcha):"
echo "   poetry run python tests/exploratory/test_pilot_simple.py \\"
echo "     --test-suite docs/icims-ats-demo-simple.md \\"
echo "     --provider github_copilot \\"
echo "     --model gpt-4.1"
