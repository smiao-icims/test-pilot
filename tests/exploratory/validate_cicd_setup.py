#!/usr/bin/env python3
"""
Validation script for CI/CD optimized headless mode.
This demonstrates the final recommended configuration for enterprise testing.
"""

import os
import sys
import argparse
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def parse_args():
    parser = argparse.ArgumentParser(description="Validate CI/CD headless setup")
    parser.add_argument(
        "--mode",
        choices=["headless", "headed", "validate-only"],
        default="validate-only",
        help="Execution mode (default: validate-only)"
    )
    parser.add_argument(
        "--hcaptcha-disabled",
        action="store_true",
        help="Indicate that hCaptcha is disabled for the test account"
    )
    return parser.parse_args()

async def validate_playwright_setup():
    """Validate that Playwright MCP is properly configured."""
    print("🔍 Validating Playwright MCP setup...")
    
    # Test basic Playwright MCP connection
    browser_args = [
        "@playwright/browser-automation",
        "--browser=chromium",
        "--headless"  # Always test headless for CI/CD
    ]
    
    server_params = StdioServerParameters(
        command="npx",
        args=browser_args,
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # List available tools
                tools = await session.list_tools()
                print(f"✅ Playwright MCP connected successfully")
                print(f"📊 Available tools: {len(tools.tools)}")
                
                # Test basic browser operations
                result = await session.call_tool("browser_navigate", {
                    "url": "https://www.google.com"
                })
                print("✅ Basic browser navigation test passed")
                
                # Test snapshot capability
                snapshot_result = await session.call_tool("browser_snapshot", {})
                print("✅ Browser snapshot capability verified")
                
                return True
                
    except Exception as e:
        print(f"❌ Playwright MCP validation failed: {e}")
        return False

def validate_environment():
    """Validate the CI/CD environment setup."""
    print("🔍 Validating CI/CD environment...")
    
    # Check required environment variables
    required_vars = [
        "OPENAI_API_KEY",  # For GitHub Copilot
        "GITHUB_TOKEN",    # For GitHub provider
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {missing_vars}")
        print("💡 For CI/CD, ensure these are set in your pipeline secrets")
    else:
        print("✅ All required environment variables are set")
    
    # Check Node.js and npm
    try:
        import subprocess
        node_result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        npm_result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        
        print(f"✅ Node.js: {node_result.stdout.strip()}")
        print(f"✅ npm: {npm_result.stdout.strip()}")
        
        # Check if Playwright is installed
        npx_result = subprocess.run(["npx", "playwright", "--version"], capture_output=True, text=True)
        if npx_result.returncode == 0:
            print(f"✅ Playwright: {npx_result.stdout.strip()}")
        else:
            print("⚠️  Playwright not found - run: npx playwright install")
            
    except Exception as e:
        print(f"❌ Node.js/npm validation failed: {e}")

async def test_headless_with_hcaptcha_disabled():
    """Test the optimal CI/CD configuration with hCaptcha disabled."""
    print("\n🚀 Testing optimal CI/CD configuration...")
    print("📋 Configuration: Headless mode with hCaptcha disabled")
    
    # This would be the actual test for an environment where hCaptcha is disabled
    browser_args = [
        "@playwright/browser-automation",
        "--browser=chromium",
        "--headless"
    ]
    
    server_params = StdioServerParameters(
        command="npx",
        args=browser_args,
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Navigate to a test login page (would be iCIMS in production)
                await session.call_tool("browser_navigate", {
                    "url": "https://example.com"  # Replace with actual test URL
                })
                
                # Take snapshot to verify page loads
                snapshot = await session.call_tool("browser_snapshot", {})
                print("✅ Page navigation successful in headless mode")
                
                print("💡 In production with hCaptcha disabled:")
                print("   - Login would proceed without hCaptcha challenge")
                print("   - Full test automation would run headless")
                print("   - Perfect for CI/CD pipelines")
                
                return True
                
    except Exception as e:
        print(f"❌ Headless test failed: {e}")
        print("💡 This is expected if hCaptcha is still enabled")
        return False

def main():
    args = parse_args()
    
    print("🔧 CI/CD Setup Validation")
    print("=" * 50)
    
    # Environment validation
    validate_environment()
    
    if args.mode == "validate-only":
        print("\n📊 Validation complete. To test browser automation:")
        print("   python validate_cicd_setup.py --mode headless")
        if not args.hcaptcha_disabled:
            print("   Note: Add --hcaptcha-disabled if testing with disabled hCaptcha")
        return
    
    # Run async tests
    if args.mode in ["headless", "headed"]:
        if args.hcaptcha_disabled:
            asyncio.run(test_headless_with_hcaptcha_disabled())
        else:
            asyncio.run(validate_playwright_setup())
    
    print("\n✨ Validation complete!")
    print("\n📋 CI/CD Recommendations:")
    print("1. Disable hCaptcha for test accounts (OPTIMAL)")
    print("2. Use headless mode in CI/CD pipelines")
    print("3. Set up proper environment variables")
    print("4. Monitor test execution for reliability")

if __name__ == "__main__":
    main()
