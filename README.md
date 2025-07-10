# test-pilot

An agent for orchestrating Playwright E2E tests to generate workloads and execution reports for downstream analysis.

## 1. Overview and Core Purpose

**test-pilot** is a specialized agent responsible for executing end-to-end (E2E) test suites using Playwright. Its primary role is to generate a realistic workload on a target application and report on the direct outcomes of those UI tests (e.g., pass/fail).

This agent intentionally follows the single responsibility principle. It is separate from trace-pilot (the Log Analysis Agent) to create a clean, modular system:

- **test-pilot**: Manages test execution and reports on UI-level success.
- **trace-pilot**: Analyzes the backend logs generated during the test run.

## 2. Technology Stack

- **Language**: Python
- **Orchestration/AI**: LangChain
- **Test Runner**: Playwright via `@playwright/mcp@latest`

## 3. Architecture and Workflow

The agent's architecture is designed as a linear workflow, making it efficient and straightforward to implement.

### Components

- **Input Handler**: Receives a structured list of Playwright test scripts to execute.
- **Orchestration Engine**: A core Python loop that records start/end timestamps and iterates through the test suite.
- **Playwright MCP Client**: A Python class that acts as a wrapper to manage the `@playwright/mcp@latest` subprocess, handling all communication via stdin and stdout.
- **Result Analyzer**: A LangChain LLMChain that takes the structured results from the test run and generates a concise, human-readable summary.
- **Handoff Formatter**: The final component that packages the agent's output into a structured JSON object for the downstream trace-pilot agent.

### Data Flow

1. The agent receives the **Test Suite** to be executed.
2. The **Orchestration Engine** records the overall `start_time_utc`.
3. It then loops through each test script in the suite.
4. For each script, the **Playwright MCP Client** sends the test command to the MCP process and parses the resulting JSON output (status, duration, errors).
5. After the loop completes, the engine records the overall `end_time_utc`.
6. The aggregated results are passed to the **Result Analyzer** chain, which generates a text summary.
7. The **Handoff Formatter** assembles the final JSON payload containing the summary, timestamps, and detailed results.

## 4. Implementation Plan

### Step 1: Build the Playwright MCP Client

Create a robust Python class to manage the `@playwright/mcp@latest` subprocess. This class should handle:

- Starting and stopping the process.
- Sending commands (test scripts) to the process's stdin.
- Reading and parsing JSON objects from the process's stdout.
- Error handling for process failures.

### Step 2: Implement the Core Orchestrator

Write the main Python script that defines the workflow. This script will:

- Initialize the MCP Client.
- Define the list of tests to run.
- Record the start time.
- Loop through the tests, calling the client to execute each one and collecting the results in a list of dictionaries.
- Record the end time.

### Step 3: Create the LangChain Analyzer

- Define a simple LLMChain using LangChain.
- Create a prompt template that accepts a list of structured test results.
- The prompt will instruct the LLM to generate a brief summary, including total tests run, number passed, and number failed.

### Step 4: Define and Format the Handoff

Implement the final function that takes all the collected data and formats it into the official handoff JSON object as defined in the contract below.

## 5. Handoff Contract

The output of **test-pilot** serves as the input for **trace-pilot**. The structure of this JSON object is critical.

```json
{
  "test_run_summary": {
    "status": "Completed",
    "total_tests": 2,
    "passed": 2,
    "failed": 0,
    "report_text": "Test run completed successfully. 2/2 tests passed."
  },
  "execution_metadata": {
    "overall_start_time_utc": "2025-07-09T23:28:14.123Z",
    "overall_end_time_utc": "2025-07-09T23:29:01.456Z"
  },
  "individual_test_results": [
    {
      "name": "test1.js",
      "status": "passed",
      "duration_ms": 1500
    },
    {
      "name": "test2.js",
      "status": "passed",
      "duration_ms": 2100
    }
  ]
}
```

## 6. Design Choices

### LangChain vs. LangGraph

**LangChain** was chosen for this agent because the workflow is a simple, predictable loop. The added complexity of LangGraph (stateful graphs, nodes, conditional edges) is not necessary here and would be over-engineering. LangChain provides the simple LLMChain needed for the final summarization step.

## 7. References

- **Playwright MCP**: [@playwright/mcp@latest](https://github.com/microsoft/playwright)
- **LangChain**: [LangChain Framework](https://github.com/langchain-ai/langchain)
- **LangChain MCP Adapters**: [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters/tree/main)
- **FastMCP**: [FastMCP Getting Started](https://gofastmcp.com/getting-started/welcome)
