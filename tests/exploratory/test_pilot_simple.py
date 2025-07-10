import argparse
import asyncio
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(provider: str, model: str):
    if provider == "openai":
        print(f"Using OpenAI model: {model}")
        return ChatOpenAI(model=model)
    elif provider == "gemini":
        print(f"Using Google Gemini model: {model}")
        return ChatGoogleGenerativeAI(model=model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def parse_args():
    parser = argparse.ArgumentParser(description="Run LLM agent with Playwright MCP via LangChain MCP bridge.")
    parser.add_argument(
        "--provider",
        type=str,
        default="openai",
        choices=["openai", "gemini"],
        help="LLM provider to use (default: openai)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.1",
        help="Model name to use (default: gpt-4.1 for OpenAI, gemini-2.5-flash for Gemini)"
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

if __name__ == "__main__":
    args = parse_args()
    # Set default model for Gemini if not specified
    if args.provider == "gemini" and args.model == "gpt-4o":
        args.model = "gemini-2.5-flash"
    llm = get_llm(args.provider, args.model)
    asyncio.run(run_agent(llm))