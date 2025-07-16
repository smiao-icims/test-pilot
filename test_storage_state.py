#!/usr/bin/env python3

import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

async def test_storage_state_feature():
    """Test if Playwright MCP --storage-state feature works"""
    
    print("=== TESTING PLAYWRIGHT MCP STORAGE STATE FEATURE ===")
    
    storage_file = "test_storage.json"
    
    # Clean up
    if os.path.exists(storage_file):
        os.remove(storage_file)
    
    print(f"1. Testing storage state creation with file: {storage_file}")
    
    # Test with storage-state parameter
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp", "--browser", "chromium", "--isolated", "--storage-state", storage_file],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            
            print(f"✅ Connected to Playwright MCP with --storage-state {storage_file}")
            print(f"Available tools: {[tool.name for tool in tools]}")
            
            # Try to navigate to a simple page
            navigate_tool = next((tool for tool in tools if tool.name == "browser_navigate"), None)
            if navigate_tool:
                print("2. Navigating to a test page...")
                try:
                    result = await navigate_tool.ainvoke({"url": "https://example.com"})
                    print(f"Navigation result: {result[:200]}...")
                except Exception as e:
                    print(f"Navigation failed: {e}")
            
            print("3. Closing browser session...")
    
    # Check if storage file was created
    print(f"4. Checking if {storage_file} was created...")
    if os.path.exists(storage_file):
        file_size = os.path.getsize(storage_file)
        print(f"✅ Storage file created! Size: {file_size} bytes")
        
        # Show content preview
        with open(storage_file, 'r') as f:
            content = f.read(300)
            print(f"Content preview: {content}...")
        
        # Clean up
        os.remove(storage_file)
        print(f"✅ Test completed successfully - storage state feature works!")
        
    else:
        print(f"❌ Storage file was not created")
        print("The --storage-state feature may not be working as expected")

if __name__ == "__main__":
    asyncio.run(test_storage_state_feature())
