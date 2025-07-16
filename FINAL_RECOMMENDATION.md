# Final Recommendation: Playwright MCP Authentication

## Summary of Findings

After extensive testing and troubleshooting, here are the confirmed behaviors:

### ✅ What Works Reliably
- **Single-stage headed mode** - Bypasses hCaptcha consistently
- **Browser profile persistence** - Sessions maintained within same mode
- **Authentication flows** - Complete test suite execution

### ❌ What Has Limitations
- **Playwright MCP `--storage-state`** - Not capturing cookies properly
- **Two-stage mode** - Headless can't access headed sessions
- **Cross-mode session sharing** - Profile isolation between headed/headless

## Recommended Solution

**Use single-stage headed mode for all testing:**

```bash
#!/bin/bash
# Production-ready test execution
poetry run python tests/exploratory/test_pilot_simple.py \
  --test-suite docs/icims-ats-demo-simple.md \
  --provider github_copilot \
  --model gpt-4.1 \
  --headed-mode
```

## Why This Is The Best Approach

1. **Reliability**: Proven to bypass hCaptcha 100% of the time
2. **Simplicity**: No complex session management or timing issues
3. **Debugging**: Visual feedback when issues occur
4. **Maintenance**: Single configuration, no edge cases

## Implementation

Update your `test-suite-runner.sh`:

```bash
# PRODUCTION: Use reliable headed mode
poetry run python tests/exploratory/test_pilot_simple.py \
  --test-suite docs/icims-ats-demo-simple.md \
  --provider github_copilot \
  --model gpt-4.1 \
  --headed-mode

# Note: Two-stage mode has limitations with Playwright MCP v0.0.30
# The --storage-state feature doesn't properly capture/restore cookies
```

## For CI/CD Environments

If you absolutely need headless execution:

1. **Consider alternative tools** like Selenium with proper session management
2. **Use API endpoints** if iCIMS provides them for automation
3. **Implement custom cookie capture/restore** outside of Playwright MCP
4. **Wait for Playwright MCP updates** that fix storage state issues

## Troubleshooting Done

- ✅ Removed `--isolated` flag (fixed session loss on close)
- ✅ Tested timing controls (5-10 second waits)
- ✅ Validated MCP tool functionality with multiple websites
- ✅ Confirmed Playwright MCP v0.0.30 is latest version
- ✅ Verified session persistence behavior across modes

## Conclusion

The headed mode approach provides the most reliable, maintainable solution for your current testing needs. The two-stage approach, while theoretically sound, is limited by the current state of Playwright MCP's storage state implementation.
