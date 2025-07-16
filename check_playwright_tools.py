#!/usr/bin/env python3

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def list_playwright_tools():
    """List all available tools in Playwright MCP"""
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp", "--browser", "chromium"],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List all available tools
            tools_result = await session.list_tools()
            
            print("=== AVAILABLE PLAYWRIGHT MCP TOOLS ===")
            for tool in tools_result.tools:
                print(f"• {tool.name}")
                if tool.description:
                    print(f"  Description: {tool.description}")
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    print(f"  Schema: {tool.inputSchema}")
                print()

if __name__ == "__main__":
    asyncio.run(list_playwright_tools())
