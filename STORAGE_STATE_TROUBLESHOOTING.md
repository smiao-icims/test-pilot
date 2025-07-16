# Playwright Storage State Troubleshooting Guide

## The Problem

When trying to use Playwright's `storageState` feature for two-stage authentication (headed login → headless execution), the storage state file is created but remains empty with `{"cookies": [], "origins": []}`, even though the login process completes successfully.

## Root Causes (Based on Analysis)

### 1. Timing Issues
- **Problem**: Storage state is captured before authentication cookies are fully set
- **Solution**: Add explicit wait periods (5-10 seconds) after login verification
- **Implementation**: Use `browser_wait_for` or explicit sleep after seeing "Logged in as..." text

### 2. Website-Specific Behavior  
- **Problem**: iCIMS may behave differently when automated vs manual use
- **Indicators**: Cookies may be `httpOnly`, `secure`, or set via JavaScript after page load
- **Solution**: Use headed mode for better compatibility with complex authentication flows

### 3. MCP Tool Limitations
- **Problem**: Playwright MCP may not properly capture storage state during session
- **Solution**: Test with our validation script to confirm if MCP supports storage state properly

### 4. Path and Configuration Issues
- **Problem**: Incorrect file paths or MCP configuration preventing storage capture
- **Solution**: Use absolute paths and verify MCP server version

## Available Solutions

### ✅ Solution 1: Enhanced Two-Stage (Improved Timing)
```bash
./debug-enhanced-two-stage.sh
```
**Features:**
- Proper wait periods after login
- Detailed storage state validation
- Session cookie detection
- Comprehensive diagnostics

### ✅ Solution 2: Storage State Validation
```bash
python test_storage_validation.py
```
**Purpose:**
- Test if Playwright MCP storage state works at all
- Validate with simple websites vs iCIMS specifically
- Determine if the issue is tool-specific or site-specific

### ✅ Solution 3: Single-Stage Headed Mode (Proven Reliable)
```bash
./run-headed-mode.sh
```
**Advantages:**
- Bypasses all hCaptcha issues
- No storage state complexity
- Proven to work consistently
- Suitable for development and testing

### ⚠️ Solution 4: Original Two-Stage (Basic)
```bash
./debug-two-stage.sh
```
**Status:** Known to have timing issues but useful for comparison

## Troubleshooting Workflow

### Step 1: Validate Tool Functionality
```bash
python test_storage_validation.py
```
**Expected Results:**
- If basic test passes but iCIMS fails → Website-specific issue
- If both tests fail → MCP tool issue
- If both pass → Timing issue in our implementation

### Step 2: Test Enhanced Implementation
```bash
./debug-enhanced-two-stage.sh
```
**Look for:**
- Cookie count > 0
- Session-related cookies (auth, token, icims)
- Proper storage file size (> 100 bytes)

### Step 3: Use Reliable Fallback
```bash
./run-headed-mode.sh
```
**When to use:** When storage state approach fails consistently

## Key Implementation Details

### Enhanced Login Stage (test_pilot_simple.py)
```python
# Added timing controls
"2. After successful login verification, wait for 5-10 seconds to ensure all cookies and session data are set"
"3. Take a final accessibility snapshot to confirm the authenticated state" 
"4. Check for presence of authentication cookies or session tokens if possible"
"8. Report any authentication-related cookies or session indicators you can observe"
```

### Storage State Validation (test_storage_validation.py)
- Tests basic storage state with simple cookie-setting website
- Tests iCIMS-specific storage state behavior
- Provides detailed analysis of captured data
- Identifies whether issue is tool-based or site-based

### Enhanced Debug Script (debug-enhanced-two-stage.sh)
- Detailed file size and timestamp analysis
- Cookie and origin counting
- Session-related data detection
- Comprehensive troubleshooting recommendations

## Recommendations by Use Case

### For Development/Testing
**Use headed mode** - Most reliable, no complexity
```bash
./run-headed-mode.sh
```

### For CI/CD (Headless Required)
1. **First try enhanced two-stage**:
   ```bash
   ./debug-enhanced-two-stage.sh
   ```
2. **If that fails, investigate alternatives**:
   - Browser profile persistence instead of storage state
   - API-based authentication if available
   - Custom session management implementation

### For Understanding the Problem
**Run validation tests** to understand root cause:
```bash
python test_storage_validation.py
```

## Expected Outcomes

### If Storage State Works
- Cookie count > 0 in storage file
- File size > 100 bytes
- Session-related cookies present
- Two-stage mode should function properly

### If Storage State Fails
- Use single-stage headed mode as primary approach
- Consider alternative session persistence methods
- File GitHub issues with Playwright MCP if tool is fundamentally broken

## Files Created/Modified

1. `debug-enhanced-two-stage.sh` - Enhanced debugging with timing controls
2. `test_storage_validation.py` - Validates MCP storage state functionality  
3. `run-headed-mode.sh` - Reliable single-stage headed execution
4. `test_pilot_simple.py` - Enhanced with better timing and validation
5. `debug-two-stage.sh` - Updated with additional troubleshooting options

This comprehensive approach addresses all the common causes of Playwright storage state failures and provides both diagnostic tools and reliable fallback solutions.
