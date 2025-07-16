#!/bin/bash

echo "=== ENHANCED TWO-STAGE DEBUG WITH TIMING CONTROLS ==="
echo "Implementing Playwright storageState best practices:"
echo "- Proper timing controls"
echo "- Storage state validation"
echo "- Diagnostic logging"
echo ""

# Clean up any existing storage file
rm -f browser_storage.json

echo "1. Running Stage 1 (Login with enhanced timing)..."
echo "   - Browser will open in headed mode"
echo "   - Login will include proper wait periods"
echo "   - Storage state will be validated after capture"
echo ""

# Run the enhanced two-stage mode
poetry run python tests/exploratory/test_pilot_simple.py \
    --test-suite docs/icims-ats-demo-simple.md \
    --provider github_copilot \
    --model gpt-4.1 \
    --two-stage-mode \
    --storage-file browser_storage.json

echo ""
echo "=== DETAILED POST-EXECUTION ANALYSIS ==="

# Check if storage file was created/updated
if [ -f "browser_storage.json" ]; then
    echo "✅ browser_storage.json exists"
    echo "File size: $(ls -lh browser_storage.json | awk '{print $5}')"
    echo "File timestamp: $(ls -l browser_storage.json | awk '{print $6, $7, $8}')"
    
    # More detailed content analysis
    echo ""
    echo "📋 Storage file content analysis:"
    
    # Check for cookies
    cookie_count=$(grep -o '"cookies":\[[^]]*\]' browser_storage.json | grep -o ',' | wc -l)
    echo "   Cookies found: $cookie_count"
    
    # Check for origins/localStorage
    if grep -q '"origins":\[' browser_storage.json; then
        origin_count=$(grep -o '"origins":\[[^]]*\]' browser_storage.json | grep -o '{' | wc -l)
        echo "   Origins/localStorage entries: $origin_count"
    else
        echo "   Origins/localStorage: not found"
    fi
    
    # Check for session-related cookies
    if grep -q -i 'session\|auth\|token\|icims' browser_storage.json; then
        echo "   ✅ Session-related data detected"
        echo "   Session cookie preview:"
        grep -i 'session\|auth\|token\|icims' browser_storage.json | head -2
    else
        echo "   ⚠️  No session-related cookies found"
    fi
    
    echo ""
    echo "📄 Full storage file content:"
    if [ "$(wc -c < browser_storage.json)" -lt 1000 ]; then
        cat browser_storage.json | jq . 2>/dev/null || cat browser_storage.json
    else
        echo "   File is large (>1KB), showing first 500 characters:"
        head -c 500 browser_storage.json
        echo ""
        echo "   ... (truncated, use 'cat browser_storage.json' to see full content)"
    fi
    
    echo ""
    # Determine if two-stage should work
    if [ "$cookie_count" -gt 0 ] || grep -q -i 'session\|auth\|token' browser_storage.json; then
        echo "✅ DIAGNOSIS: Two-stage mode should work!"
        echo "   Storage file contains authentication data."
        echo ""
        echo "🧪 To test Stage 2 (headless with saved state):"
        echo "   poetry run python tests/exploratory/test_pilot_simple.py \\"
        echo "     --test-suite docs/icims-ats-demo-simple.md \\"
        echo "     --provider github_copilot \\"
        echo "     --model gpt-4.1 \\"
        echo "     --storage-file browser_storage.json"
    else
        echo "⚠️  DIAGNOSIS: Storage state capture failed"
        echo "   The file exists but contains no authentication data."
        echo "   This indicates a timing or MCP integration issue."
    fi
    
else
    echo "❌ browser_storage.json was NOT created"
    echo "   This indicates a fundamental issue with the Playwright MCP --storage-state feature"
    echo "   or the MCP server configuration."
fi

echo ""
echo "=== TROUBLESHOOTING RECOMMENDATIONS ==="
echo ""
echo "If storage state is empty, try these solutions:"
echo ""
echo "1. 🕒 Timing Issue Solutions:"
echo "   - Increase wait time after login (currently 5-10 seconds)"
echo "   - Add explicit verification steps before saving state"
echo "   - Use browser_wait_for to ensure specific elements are loaded"
echo ""
echo "2. 🔧 MCP Configuration Solutions:"
echo "   - Update Playwright MCP to latest version"
echo "   - Check if --storage-state is properly supported"
echo "   - Verify browser profile persistence"
echo ""
echo "3. 🌐 Website-Specific Solutions:"
echo "   - Check if iCIMS behaves differently in automation"
echo "   - Verify authentication cookies are httpOnly/secure"
echo "   - Test with different browser types (chromium vs chrome)"
echo ""
echo "4. 📋 Alternative Approaches:"
echo "   - Use persistent browser profiles instead of storage state"
echo "   - Implement custom session management"
echo "   - Consider API-based authentication if available"
echo ""
echo "=== FALLBACK SOLUTIONS ==="
echo ""
echo "Single-stage headed mode (guaranteed to work):"
echo "   ./run-headed-mode.sh"
echo ""
echo "Single-stage headless mode (may hit captcha):"
echo "   poetry run python tests/exploratory/test_pilot_simple.py \\"
echo "     --test-suite docs/icims-ats-demo-simple.md \\"
echo "     --provider github_copilot \\"
echo "     --model gpt-4.1"
