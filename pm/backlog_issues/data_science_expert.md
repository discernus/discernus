# Backlog Item: Implement `data_science_expert`

**Description**

The `data_science_expert` is an agent that performs statistical analysis and other quantitative methods. It is designed to take structured data produced by other agents and execute Python code to generate statistical insights. This agent will use the `SecureCodeExecutor` to run its analyses in a sandboxed environment, ensuring safety and reproducibility.

**Rationale**

Many research questions require quantitative analysis to answer rigorously. The `data_science_expert` provides a safe and reliable way to perform these calculations within the Discernus ecosystem. By leveraging the `SecureCodeExecutor`, it can perform complex statistical tests without compromising the integrity of the system.

**Implementation Tasks**

*   [ ] Create a new agent class, `DataScienceExpert`, in `discernus/agents/data_science_expert.py`.
*   [ ] The agent should accept structured data and a description of the desired analysis as input.
*   [ ] The agent will generate Python code to perform the analysis.
*   [ ] The generated code will be executed using the `discernus.core.secure_code_executor.SecureCodeExecutor`.
*   [ ] The results of the analysis (e.g., statistical tests, charts, tables) should be returned in a structured dictionary.
*   [ ] Add the new agent to `discernus/core/agent_registry.yaml`.
*   [ ] Create a unit test for the `DataScienceExpert` in `discernus/tests/agents/`, likely involving mock data and simple, verifiable calculations. 