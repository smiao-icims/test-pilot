import os
os.environ["LANGGRAPH_RECURSION_LIMIT"] = "100"

import argparse
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from modelforge.registry import ModelForgeRegistry, ProviderError, ModelNotFoundError, ConfigurationError

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test-suite", 
        type=str,
        required=True,
        help="Path to the test suite to run"
    )
    parser.add_argument(
        "--provider",
        type=str,
        required=True,
        help="LLM provider to use"
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Model name to use"
    )
    return parser.parse_args()

async def run_agent(llm, test_suite):
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp", "--browser", "chromium", "--isolated", "--viewport-size", "1920,1080", "--headless"],
    )
    # Add a note to the prompt to output DONE/REPORT at the end
    user_message = (
        test_suite.strip() +
        "\n\nIMPORTANT: " +
        "- If the login step fails for any reason, you must restart the entire test suite from the beginning and attempt the login again. Repeat this process up to 3 times if necessary. If login fails after 3 attempts, report the failure and stop the test.\n" +
        "- At the end of the test suite, output a clear, properly formatted markdown report. The report should be valid markdown, suitable for direct saving as a .md file, and should not be wrapped in JSON, Python objects, or any code block.\n" +
        "- Do not mix single and double quotes in the output.\n" +
        "- When you output the report, do not take any further actions or request more steps. This is the final output.\n" +
        "- Do not say 'Sorry, need more steps to process this request.' If you are finished, just output the markdown report.\n"
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(f"✅ Loaded {len(tools)} MCP tools:")
            for tool in tools:
                print(f"  • {tool.name}: {tool.description}")
            # Set recursion_limit to 100
            agent = create_react_agent(llm, tools)
            agent = agent.with_config(recursion_limit=100)  # Set your desired limit here
            print(f"\nUser Message: {user_message}\n--- Running agent... ---")
            # Step-by-step logging
            print("\n--- Agent Steps ---")
            steps = []
            async for step in agent.astream({"messages": user_message}):
                print(f"Step {len(steps)+1}: {step}")
                steps.append(step)
            print("\n--- Agent Final Response ---")
            print(steps[-1] if steps else "No response.")
            return steps[-1] if steps else None

def main():
    args = parse_args()
    try:
        with open(args.test_suite, "r") as f:
            test_suite = f.read()
        print(f"Loaded test suite: {test_suite}")
    except FileNotFoundError:
        print(f"Test suite file not found: {args.test_suite}")
        return
    print(f"Running test suite: {args.test_suite} (len={len(test_suite)} chars)")

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
    agent_response = asyncio.run(run_agent(llm, test_suite))
    # Extract markdown content from AIMessage if present
    markdown_content = None
    if agent_response and 'agent' in agent_response and 'messages' in agent_response['agent']:
        messages = agent_response['agent']['messages']
        if messages and hasattr(messages[0], 'content'):
            markdown_content = messages[0].content
    if markdown_content:
        with open("test_report.md", "w") as f:
            f.write(markdown_content)
        print("Test report saved to test_report.md (markdown only)")
    else:
        with open("test_report.md", "w") as f:
            f.write(str(agent_response))
        print("Test report saved to test_report.md (raw response)")

if __name__ == "__main__":
    main()