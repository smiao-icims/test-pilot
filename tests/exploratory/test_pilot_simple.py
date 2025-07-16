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
    parser.add_argument(
        "--two-stage-mode",
        action="store_true",
        help="Use headed mode for login, then headless for the rest"
    )
    parser.add_argument(
        "--storage-file",
        type=str,
        default="browser_storage.json",
        help="File to save/load browser storage state"
    )
    parser.add_argument(
        "--headed-mode",
        action="store_true",
        help="Run entire test in headed mode (no headless)"
    )
    return parser.parse_args()

async def create_empty_storage_state(storage_file):
    """Create an empty storage state file that Playwright can use"""
    import json
    
    # Create a minimal storage state structure
    empty_storage = {
        "cookies": [],
        "origins": []
    }
    
    with open(storage_file, 'w') as f:
        json.dump(empty_storage, f)
    
    print(f"✅ Created empty storage state file: {storage_file}")

async def run_login_stage(llm, test_suite, storage_file):
    """Run login in headed mode and save browser storage"""
    import os
    
    # Create empty storage state file if it doesn't exist
    if not os.path.exists(storage_file):
        await create_empty_storage_state(storage_file)
    
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp", "--browser", "chromium", "--viewport-size", "1920,1080", "--storage-state", storage_file],
    )
    
    # Extract just the login portion of the test suite
    login_message = (
        "STAGE 1 - LOGIN ONLY: Perform only the login steps from the following test suite. "
        "After successful login, implement proper timing to ensure session state is captured.\n\n" +
        test_suite.strip() +
        f"\n\nCRITICAL INSTRUCTIONS FOR PROPER SESSION CAPTURE:\n" +
        f"1. Perform the login steps until you successfully authenticate and reach the main dashboard/homepage\n" +
        f"2. After successful login verification, wait for 5-10 seconds to ensure all cookies and session data are set\n" +
        f"3. Take a final accessibility snapshot to confirm the authenticated state\n" +
        f"4. Check for presence of authentication cookies or session tokens if possible\n" +
        f"5. Verify the dashboard URL contains '/platform' or similar authenticated path\n" +
        f"6. Only after this verification and wait period, state 'Login completed, session ready for persistence'\n" +
        f"7. Do NOT proceed with job search or other test phases - storage will be saved to '{storage_file}'\n" +
        f"8. Report any authentication-related cookies or session indicators you can observe"
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(f"✅ STAGE 1 - Loaded {len(tools)} MCP tools for login")
            
            agent = create_react_agent(llm, tools)
            agent = agent.with_config(recursion_limit=50)
            
            print(f"\n--- STAGE 1: Running login in headed mode ---")
            steps = []
            async for step in agent.astream({"messages": login_message}):
                print(f"Login Step {len(steps)+1}: {step}")
                steps.append(step)
            
            print(f"\n--- STAGE 1 Complete: Login finished ---")
            return steps[-1] if steps else None

async def run_main_stage(llm, test_suite, storage_file):
    """Run main test in headless mode using saved browser storage"""
    import os
    
    # Check if storage file exists
    if not os.path.exists(storage_file):
        print(f"ERROR: Storage file '{storage_file}' not found. Stage 1 may have failed.")
        return None
    
    print(f"✅ Found storage file: {storage_file}")
    
    server_params = StdioServerParameters(
        command="npx",
        args=["@playwright/mcp", "--browser", "chromium", "--viewport-size", "1920,1080", "--headless", "--storage-state", storage_file],
    )
    
    main_message = (
        f"STAGE 2 - MAIN TEST: The browser will automatically load the authenticated session from '{storage_file}'. "
        "Skip the login steps since authentication is already loaded.\n\n" +
        test_suite.strip() +
        "\n\nCRITICAL INSTRUCTIONS:\n" +
        f"1. The browser session is already authenticated (loaded from '{storage_file}')\n" +
        f"2. Navigate directly to the main application URL to start the test\n" +
        f"3. Skip any login steps since you should already be authenticated\n" +
        f"4. If you see a login page, report this as an authentication failure\n" +
        f"5. Proceed with the test suite (excluding login steps)\n" +
        f"6. At the end, output a clear markdown report\n"
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            print(f"✅ STAGE 2 - Loaded {len(tools)} MCP tools for main test")
            
            agent = create_react_agent(llm, tools)
            agent = agent.with_config(recursion_limit=100)
            
            print(f"\n--- STAGE 2: Running main test in headless mode ---")
            steps = []
            async for step in agent.astream({"messages": main_message}):
                print(f"Main Step {len(steps)+1}: {step}")
                steps.append(step)
            
            print(f"\n--- STAGE 2 Complete: Main test finished ---")
            return steps[-1] if steps else None

async def run_agent(llm, test_suite, two_stage_mode=False, storage_file="browser_storage.json", headed_mode=False):
    """Run agent in either single-stage or two-stage mode"""
    if two_stage_mode:
        print("=== TWO-STAGE MODE ENABLED ===")
        print("Stage 1: Login in headed mode")
        login_response = await run_login_stage(llm, test_suite, storage_file)
        
        if login_response:
            print(f"\n✅ Stage 1 completed. Checking if storage was updated in {storage_file}")
            import os
            import json
            if os.path.exists(storage_file):
                # Check if storage file has meaningful content (cookies/origins)
                try:
                    with open(storage_file, 'r') as f:
                        storage_data = json.load(f)
                    
                    cookies_count = len(storage_data.get('cookies', []))
                    origins_count = len(storage_data.get('origins', []))
                    
                    if cookies_count > 0 or origins_count > 0:
                        print(f"✅ Storage file has {cookies_count} cookies and {origins_count} origins")
                        print("Stage 2: Main test in headless mode")
                        main_response = await run_main_stage(llm, test_suite, storage_file)
                        return main_response
                    else:
                        print(f"❌ Storage file exists but appears empty (no cookies/origins saved)")
                        print("This suggests login may not have completed successfully")
                        return None
                except Exception as e:
                    print(f"❌ Error reading storage file: {e}")
                    return None
            else:
                print(f"❌ ERROR: Storage file '{storage_file}' was not created in Stage 1")
                return None
        else:
            print("❌ ERROR: Stage 1 (login) failed")
            return None
    else:
        # CI/CD optimized single-stage mode (hCaptcha disabled for test account)
        browser_args = ["@playwright/mcp", "--browser", "chromium", "--viewport-size", "1920,1080"]
        if not headed_mode:
            browser_args.append("--headless")
        # Note: --isolated removed to allow session persistence if needed
        
        server_params = StdioServerParameters(
            command="npx",
            args=browser_args,
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
    agent_response = asyncio.run(run_agent(llm, test_suite, args.two_stage_mode, args.storage_file, args.headed_mode))
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