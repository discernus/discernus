# DISCERNUS DECLARATIVE MATHEMATICAL SPECIFICATION MODEL
---

## Migration Plan: From Code Generation to Tool-Calling

This plan outlines the systematic transition from the fragile `AnalyticalCodeGenerator` architecture to a robust, reliable `MathToolkit` and `AnalysisPlanner` architecture, as recommended by our internal research and specifications.

### **Phase 1: Build the Foundation (The "TO" Architecture)**

We will build the new components in parallel with the existing system to allow for controlled testing without breaking the current implementation.

**Task 1.1: Create the `MathToolkit`**
*   **Action:** Create a new file: `discernus/core/math_toolkit.py`.
*   **Purpose:** This module will be the single source of truth for all mathematical and statistical operations. It will contain our own well-documented and unit-tested Python functions.
*   **Initial Functions:**
    *   `calculate_descriptive_stats(dataframe: pd.DataFrame, columns: list) -> dict`: Computes mean, std, min, max, etc., for specified columns.
    *   `perform_independent_t_test(dataframe: pd.DataFrame, grouping_variable: str, dependent_variable: str) -> dict`: Performs a t-test and returns the statistic and p-value.
    *   `calculate_pearson_correlation(dataframe: pd.DataFrame, columns: list) -> dict`: Computes a correlation matrix.
*   **Testing:** Each function will have a corresponding unit test to guarantee its correctness independent of any LLM.

**Task 1.2: Create the `AnalysisPlanner` Agent**
*   **Action:** Create a new agent: `discernus/agents/thin_synthesis/analysis_planner/`.
*   **Purpose:** This agent replaces the `AnalyticalCodeGenerator`. Its sole responsibility is to generate a structured JSON "analysis plan" that specifies which tools from the `MathToolkit` to run.
*   **Key Components:**
    *   `agent.py`: Contains the agent logic.
    *   `prompt.yaml`: A new, carefully engineered prompt that instructs the LLM to analyze the experiment/framework and output a JSON plan. **This prompt will leverage the API's `response_format={"type": "json_object"}` feature to enforce a clean, no-envelope JSON output.**
*   **Testing:** An integration test will be created to ensure the agent, given a sample experiment, reliably produces a syntactically valid JSON plan with the expected structure.

### **Phase 2: Refactor the Synthesis Pipeline**

We will now modify the orchestrator to use the new components.

**Task 2.1: Implement the Tool Dispatcher**
*   **Action:** Modify `discernus/agents/thin_synthesis/orchestration/pipeline.py`.
*   **Purpose:** Rewire the pipeline to use the new `AnalysisPlanner` and `MathToolkit`.
*   **Changes:**
    1.  **Replace Stage 1 (`_stage_1_generate_code`):** The call to `AnalyticalCodeGenerator` will be replaced with a call to our new `AnalysisPlanner.generate_plan()`.
    2.  **Replace Stage 2 (`_stage_2_execute_code`):** The call to `SecureCodeExecutor` will be replaced with a new internal method, `_execute_analysis_plan()`.
    3.  **Create Tool Registry:** This new method will contain a simple dictionary (`TOOL_REGISTRY`) that maps the string names from the JSON plan (e.g., `"t_test_independent"`) to the actual Python functions in our `MathToolkit`.
    4.  **Implement Dispatch Logic:** The method will parse the JSON plan, loop through the requested tasks, look up the function in the registry, and execute it with the provided parameters. The results will be aggregated into the `statistical_results` object that downstream agents expect.
*   **Testing:** An end-to-end test running the `a_civic_character_assessment` experiment. The primary success criterion is the successful generation of the `statistical_results` object, which will be validated by inspecting the intermediate artifact.

### **Phase 3: Deprecate and Remove the "FROM" Architecture**

Once the new pipeline is validated, we will permanently remove the old, fragile components to reduce complexity and technical debt.

**Task 3.1: Deprecate `AnalyticalCodeGenerator`**
*   **Action:** Delete the entire directory `discernus/agents/thin_synthesis/analytical_code_generator/`.

**Task 3.2: Deprecate `SecureCodeExecutor`**
*   **Action:** Delete the file `discernus/core/secure_code_executor.py`.

**Task 3.3: Deprecate `LLMCodeSanitizer`**
*   **Action:** Delete the file `discernus/core/llm_code_sanitizer.py`.

**Task 3.4: Final Cleanup**
*   **Action:** Search the codebase for any remaining imports or references to the deleted files and remove them. This includes the `autopep8`, `black`, and `ruff` dependencies we added.
*   **Testing:** Run all system tests one final time to ensure that the removal of these components has not caused any regressions.

---
