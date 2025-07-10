import argparse
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from modelforge.registry import ModelForgeRegistry, ProviderError, ModelNotFoundError, ConfigurationError

def parse_args():
    parser = argparse.ArgumentParser(description="Run LLM agent with Playwright MCP via ModelForge.")
    parser.add_argument(
        "--provider",
        type=str,
        default=None,
        help="LLM provider to use (default: current model in ModelForge config)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model name to use (default: current model in ModelForge config)"
    )
    return parser.parse_args()

async def run_agent(llm):
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp", "--browser", "chromium"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(f"✅ Loaded {len(tools)} MCP tools:")
            for tool in tools:
                print(f"  • {tool.name}: {tool.description}")
            agent = create_react_agent(llm, tools)
            user_message = "navigate to www.google.com, search for Model Context Protocol, note AI Overview section if it exists, close the browser and return the summary"
            print(f"\nUser Message: {user_message}\n--- Running agent... ---")
            agent_response = await agent.ainvoke({"messages": user_message})
            print("\n--- Agent Response ---")
            print(agent_response)
            return agent_response

def main():
    args = parse_args()
    registry = ModelForgeRegistry()
    try:
        llm = registry.get_llm(
            provider_name=args.provider,
            model_alias=args.model
        )
        print(f"loaded LLM: {llm}")
    except (ProviderError, ModelNotFoundError, ConfigurationError) as e:
        print(f"Failed to load LLM: {e}")
        return
    
    # run the agent logic
    asyncio.run(run_agent(llm))

if __name__ == "__main__":
    main()