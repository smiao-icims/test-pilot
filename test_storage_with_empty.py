#!/usr/bin/env python3

import asyncio
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

async def create_empty_storage_state(storage_file):
    """Create an empty storage state file that Playwright can use"""
    
    # Create a minimal storage state structure
    empty_storage = {
        "cookies": [],
        "origins": []
    }
    
    with open(storage_file, 'w') as f:
        json.dump(empty_storage, f)
    
    print(f"✅ Created empty storage state file: {storage_file}")

async def test_storage_state_with_empty_file():
    """Test Playwright MCP with an empty storage state file"""
    
    print("=== TESTING WITH EMPTY STORAGE STATE FILE ===")
    
    storage_file = "empty_storage.json"
    
    # Clean up
    if os.path.exists(storage_file):
        os.remove(storage_file)
    
    # Create empty storage state
    await create_empty_storage_state(storage_file)
    
    print(f"1. Testing with empty storage state file: {storage_file}")
    
    # Test with storage-state parameter
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp", "--browser", "chromium", "--isolated", "--storage-state", storage_file],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            
            print(f"✅ Connected to Playwright MCP with existing storage file")
            
            # Try to navigate to a simple page
            navigate_tool = next((tool for tool in tools if tool.name == "browser_navigate"), None)
            if navigate_tool:
                print("2. Navigating to example.com...")
                try:
                    result = await navigate_tool.ainvoke({"url": "https://example.com"})
                    print(f"✅ Navigation successful")
                except Exception as e:
                    print(f"❌ Navigation failed: {e}")
            
            print("3. Closing browser session...")
    
    # Check if storage file was updated
    print(f"4. Checking if {storage_file} was updated...")
    if os.path.exists(storage_file):
        file_size = os.path.getsize(storage_file)
        print(f"✅ Storage file exists! Size: {file_size} bytes")
        
        # Check if content was updated
        with open(storage_file, 'r') as f:
            content = json.load(f)
            print(f"Cookies: {len(content.get('cookies', []))}")
            print(f"Origins: {len(content.get('origins', []))}")
        
        # Clean up
        os.remove(storage_file)
        print(f"✅ Test completed - storage state file was properly updated!")
        
    else:
        print(f"❌ Storage file disappeared")

if __name__ == "__main__":
    asyncio.run(test_storage_state_with_empty_file())
