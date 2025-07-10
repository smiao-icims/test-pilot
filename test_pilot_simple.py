import asyncio
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o")

# Configure server parameters for Playwright MCP
server_params = StdioServerParameters(
    command="npx",
    args=["@playwright/mcp", "--browser", "chromium"],
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(f"✅ Loaded {len(tools)} MCP tools:")
            for tool in tools:
                print(f"  • {tool.name}: {tool.description}")
            agent = create_react_agent(model, tools)
            user_message = "navigate to www.google.com, search for Model Context Protocol and return the first page content"
            print(f"\nUser Message: {user_message}\n--- Running agent... ---")
            agent_response = await agent.ainvoke({"messages": user_message})
            print("\n--- Agent Response ---")
            print(agent_response)
            return agent_response

if __name__ == "__main__":
    asyncio.run(run_agent())