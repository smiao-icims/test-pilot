# Playwright Test Execution Agent Workflow

This document outlines how to effectively use the Playwright Agent to automate web application testing using structured natural language test suites.

## 1. Overview

The Playwright Agent leverages the Playwright Model Context Protocol (MCP) server to interpret your natural language test scripts (typically in Markdown format) and execute them in a browser. This allows for code-less test automation driven by descriptive steps.

## 2. Prerequisites (Before You Start)

Ensure the following are set up and verified:

*   **Playwright MCP Server**:
    *   Configured as per `playwright-mcp-demo/setup/mcp-config.md` or `playwright-mcp-demo/playwright-guide.md`.
    *   Running and accessible.
*   **Target Browser**:
    *   Installed via Playwright (e.g., `npx playwright install firefox`).
    *   The browser specified in your MCP configuration or test script is available.
*   **Test Suite File**:
    *   A Markdown file (e.g., `playwright-mcp-demo/examples/icims-ats-demo.md`) containing clear, step-by-step instructions for the test.
*   **Environment Variables / Credentials**:
    *   If your test requires credentials (e.g., for login), ensure they are correctly set up in a `.env` file that the agent/test script can access, or be prepared to provide them securely if prompted.

## 3. How to Instruct the Playwright Agent

To initiate a test run, provide a clear prompt to the agent. Include the following details:

*   **Reference to the Test Suite File**: Clearly specify the path to your Markdown test file.
*   **Execution Mode**:
    *   **Automatic Full Run**: Request the agent to run all phases/steps without pausing.
    *   **Phased Execution**: Specify which phases to run or skip (if your test suite is structured in phases).
*   **Reporting**: Ask for progress updates and a final status.

### Example Prompts:

**Scenario 1: Full Automatic Execution of a Named Test Suite**

```
Execute the complete iCIMS ATS test suite automatically using the '''playwright-mcp-demo/examples/icims-ats-demo.md''' workflow.
Run all phases (1, 2, 3, and 5) without pausing for confirmation. Skip Phase 4 as configured in the test document.
Provide brief progress updates for each phase and complete with logout verification.
```

**Scenario 2: General Test File Execution**

```
Please run the Playwright test suite located at `[path/to/your/test-suite.md]`.
Execute all steps automatically and report the final outcome.
I'''ve already configured the browser and credentials as per the test suite'''s prerequisites.
```

**Scenario 3: Resuming or Continuing a Test (If Agent Supports Context)**

```
Resume the ATS testing workflow from the current state.
Execute the remaining test scenarios (Phases 3 and 5) through completion automatically, using '''playwright-mcp-demo/examples/icims-ats-demo.md'''.
```

## 4. What to Expect from the Agent

The Playwright Agent should:

*   Acknowledge your request and the test file.
*   Parse the natural language steps from the Markdown file.
*   Perform browser interactions as described (navigate, type, click, etc.).
*   Utilize accessibility snapshots to understand page structure and locate elements.
*   Handle conditional steps if described in the test suite (e.g., 2FA).
*   Provide progress updates as requested (e.g., per phase or key step).
*   Report any errors encountered during execution.
*   Confirm successful completion or failure of the test suite.

## 5. Crafting Effective Test Suite Files (e.g., `your-test.md`)

Refer to `playwright-mcp-demo/playwright-guide.md` and existing examples like `icims-ats-demo.md` for best practices:

*   **Clear, Sequential Steps**: Number or bullet your steps.
*   **Descriptive Element Locators**: Instead of CSS/XPath, describe elements (e.g., "the button labeled '''Submit'''", "the input field for '''Email Address'''").
*   **Explicit Waits/Checks**: Instruct the agent to "wait for page to load" or "take a snapshot" to ensure the page is ready.
*   **Credential Handling**: Use placeholders like `${USERNAME}` and instruct the agent to source them from `.env` or a secure mechanism.
*   **Modular Phases (Optional but Recommended)**: Break down long tests into logical phases for better manageability and reporting.

## 6. Troubleshooting with the Agent

If the agent encounters issues or the test doesn'''t run as expected:

*   **Review Agent'''s Output**: Look for error messages or points of confusion.
*   **Check MCP Server Logs**: Errors might originate from the Playwright MCP server.
*   **Take a Snapshot**: Ask the agent to "take an accessibility snapshot" to understand what it'''s seeing if it'''s stuck.
*   **Simplify Instructions**: If a complex step fails, try breaking it down further in your test suite file.
*   **Verify Prerequisites**: Double-check that the MCP server, browser, and environment variables are correctly configured and active.
*   **Consult `playwright-mcp-demo/playwright-guide.md`**: This guide contains troubleshooting tips for the underlying Playwright MCP setup.

---
This workflow aims to streamline your interaction with the Playwright Agent for efficient automated testing.
