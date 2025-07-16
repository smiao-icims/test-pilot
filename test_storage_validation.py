#!/usr/bin/env python3
"""
Test script to validate Playwright MCP storage state functionality
This will help determine if the issue is with our implementation or the MCP tool itself
"""

import asyncio
import json
import os
from mcp import ClientSession, StdioServerParameters, stdio_client

async def test_storage_state_basic():
    """Test basic storage state functionality with a simple website"""
    storage_file = "test_storage_basic.json"
    
    # Clean up any existing file
    if os.path.exists(storage_file):
        os.remove(storage_file)
    
    print("=== Testing Basic Storage State Functionality ===")
    print(f"Using storage file: {storage_file}")
    
    # Create empty storage state file
    with open(storage_file, 'w') as f:
        json.dump({"cookies": [], "origins": []}, f)
    
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp", "--browser", "chromium", "--isolated", "--storage-state", storage_file],
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # List available tools
                result = await session.list_tools()
                tools = [tool.name for tool in result.tools]
                print(f"✅ Connected to Playwright MCP, tools: {tools[:5]}...")
                
                # Navigate to a simple website that sets cookies
                print("\n1. Navigating to httpbin.org (sets cookies)...")
                nav_result = await session.call_tool(
                    "browser_navigate",
                    {"url": "https://httpbin.org/cookies/set/test_cookie/test_value"}
                )
                print(f"Navigation result: {nav_result.content[:100]}...")
                
                # Wait a moment for cookies to be set
                print("\n2. Waiting for cookies to be set...")
                await asyncio.sleep(3)
                
                # Take a snapshot to see current state
                print("\n3. Taking snapshot...")
                snapshot_result = await session.call_tool("browser_snapshot", {})
                print(f"Snapshot captured: {len(snapshot_result.content)} chars")
                
                # Check if we can see cookies
                print("\n4. Checking for cookies in page...")
                cookie_result = await session.call_tool(
                    "browser_navigate", 
                    {"url": "https://httpbin.org/cookies"}
                )
                print(f"Cookie check result: {cookie_result.content[:200]}...")
                
                print(f"\n5. Storage state should be saved to {storage_file} automatically")
                
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False
    
    # Check the storage file after the session ends
    print(f"\n=== Post-Session Storage Analysis ===")
    
    if os.path.exists(storage_file):
        file_size = os.path.getsize(storage_file)
        print(f"✅ Storage file exists: {storage_file} ({file_size} bytes)")
        
        with open(storage_file, 'r') as f:
            try:
                storage_data = json.load(f)
                cookie_count = len(storage_data.get('cookies', []))
                origin_count = len(storage_data.get('origins', []))
                
                print(f"   Cookies: {cookie_count}")
                print(f"   Origins: {origin_count}")
                
                if cookie_count > 0:
                    print(f"   ✅ SUCCESS: Storage state captured cookies!")
                    print(f"   First cookie: {storage_data['cookies'][0] if storage_data['cookies'] else 'None'}")
                    return True
                else:
                    print(f"   ⚠️  Storage file exists but no cookies captured")
                    print(f"   Content: {storage_data}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON in storage file: {e}")
                with open(storage_file, 'r') as f:
                    content = f.read()
                    print(f"   Raw content: {content}")
                return False
    else:
        print(f"❌ Storage file was not created: {storage_file}")
        return False

async def test_storage_state_icims():
    """Test storage state with iCIMS specifically"""
    storage_file = "test_storage_icims.json"
    
    # Clean up any existing file
    if os.path.exists(storage_file):
        os.remove(storage_file)
    
    print("\n\n=== Testing Storage State with iCIMS ===")
    print(f"Using storage file: {storage_file}")
    
    # Create empty storage state file
    with open(storage_file, 'w') as f:
        json.dump({"cookies": [], "origins": []}, f)
    
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp", "--browser", "chromium", "--isolated", "--storage-state", storage_file],
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                print("1. Navigating to iCIMS login page...")
                nav_result = await session.call_tool(
                    "browser_navigate",
                    {"url": "https://configrariet.icims.com"}
                )
                print(f"Navigation successful: {nav_result.content[:100]}...")
                
                # Wait for page to load and check for cookies
                print("\n2. Waiting for page to load...")
                await asyncio.sleep(5)
                
                # Take snapshot to see current state
                print("\n3. Taking snapshot of login page...")
                snapshot_result = await session.call_tool("browser_snapshot", {})
                print(f"Snapshot captured: {len(snapshot_result.content)} chars")
                
                print(f"\n4. Storage state should be saved to {storage_file} automatically")
                
    except Exception as e:
        print(f"❌ Error during iCIMS test: {e}")
        return False
    
    # Check the storage file
    print(f"\n=== Post-Session iCIMS Storage Analysis ===")
    
    if os.path.exists(storage_file):
        file_size = os.path.getsize(storage_file)
        print(f"✅ Storage file exists: {storage_file} ({file_size} bytes)")
        
        with open(storage_file, 'r') as f:
            try:
                storage_data = json.load(f)
                cookie_count = len(storage_data.get('cookies', []))
                origin_count = len(storage_data.get('origins', []))
                
                print(f"   Cookies: {cookie_count}")
                print(f"   Origins: {origin_count}")
                
                if cookie_count > 0:
                    print(f"   ✅ SUCCESS: iCIMS storage state captured cookies!")
                    # Look for iCIMS-specific cookies
                    icims_cookies = [c for c in storage_data['cookies'] if 'icims' in c.get('name', '').lower() or 'icims' in c.get('domain', '').lower()]
                    print(f"   iCIMS-specific cookies: {len(icims_cookies)}")
                    return True
                else:
                    print(f"   ⚠️  No cookies captured from iCIMS")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON in storage file: {e}")
                return False
    else:
        print(f"❌ Storage file was not created: {storage_file}")
        return False

async def main():
    """Run both tests and provide recommendations"""
    print("Playwright MCP Storage State Validation")
    print("=" * 50)
    
    basic_test = await test_storage_state_basic()
    icims_test = await test_storage_state_icims()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    print(f"Basic storage test: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"iCIMS storage test: {'✅ PASS' if icims_test else '❌ FAIL'}")
    
    if basic_test and icims_test:
        print("\n🎉 CONCLUSION: Playwright MCP storage state is working correctly!")
        print("   The issue may be with timing in our authentication flow.")
        print("   Recommendation: Use the enhanced debug script with longer wait times.")
    elif basic_test and not icims_test:
        print("\n🤔 CONCLUSION: Storage state works generally but not with iCIMS")
        print("   This suggests iCIMS-specific behavior (cookies may be httpOnly, secure, etc.)")
        print("   Recommendation: Try different approaches or use headed mode.")
    elif not basic_test:
        print("\n❌ CONCLUSION: Playwright MCP storage state is not working")
        print("   This indicates a fundamental issue with the MCP tool or configuration.")
        print("   Recommendation: Use single-stage headed mode as primary approach.")
    
    print(f"\nCheck the generated test files:")
    print(f"  - test_storage_basic.json")
    print(f"  - test_storage_icims.json")

if __name__ == "__main__":
    asyncio.run(main())
