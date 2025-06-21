# Comprehensive Experiment Orchestrator Workflow

This document provides a detailed architectural diagram of the `comprehensive_experiment_orchestrator.py` script. It illustrates the major stages and decision points in the experiment lifecycle, from initial validation to final academic export.

## Orchestrator Flowchart

This diagram shows the sequence of operations, including pre-flight checks, component registration, analysis execution, quality assurance, and reporting.

```mermaid
graph TD
    subgraph "Phase 1: Initialization & Validation"
        A[Start] --> B{Load Experiment Definition YAML};
        B --> C{Parse Experiment Context};
        C --> D[Run Pre-Flight Validation];
        D --> E{Components Valid?};
        E -- No --> F[Attempt Auto-Registration of Missing Components];
        F --> G{Registration Successful?};
        G -- No --> H_FAIL[Fail with Error & Guidance];
        E -- Yes --> I{Show Execution Plan & Ask for Confirmation};
        G -- Yes --> I;
    end

    subgraph "Phase 2: Execution"
        I -- No --> J_CANCEL[Execution Cancelled by User];
        I -- Yes --> K[Execute Analysis Matrix];
        K --> L{Execution Complete?};
        L -- No --> M_FAIL[Fail with Checkpoint Data];
        L -- Yes --> N[Run LLM Quality Assurance];
    end

    subgraph "Phase 3: Reporting & Export"
        N --> O[Generate Statistical Analysis];
        O --> P[Generate Visualizations];
        P --> Q[Generate Comprehensive HTML Report];
        Q --> R[Create Academic Exports (R, Stata, etc.)];
        R --> S_SUCCESS[End: Experiment Complete];
    end

    %% Styling
    style A fill:#d4edda,stroke:#155724
    style S_SUCCESS fill:#d4edda,stroke:#155724
    style H_FAIL fill:#f8d7da,stroke:#721c24
    style M_FAIL fill:#f8d7da,stroke:#721c24
    style J_CANCEL fill:#fff3cd,stroke:#856404
```

## Workflow Stages Explained

1.  **Initialization & Validation**:
    *   **Load Experiment Definition**: The orchestrator starts by loading the user-provided YAML file that defines all aspects of the experiment.
    *   **Pre-Flight Validation**: It then checks for the existence and integrity of all required assets: frameworks, prompt templates, weighting schemes, and corpus files.
    *   **Auto-Registration**: If a component is found on the filesystem but not in the database, the orchestrator attempts to register it automatically. If this fails, or if a component is missing entirely, the process terminates with clear guidance.
    *   **Execution Plan**: A summary of the planned analysis is shown to the user before proceeding.

2.  **Execution**:
    *   **Analysis Matrix**: This is the core of the experiment, where each text in the corpus is analyzed using the specified models and frameworks.
    *   **Checkpointing**: If the execution fails mid-run (e.g., due to an API error), the state is saved in a checkpoint file, allowing the experiment to be resumed later.
    *   **Quality Assurance**: After successful execution, the `LLMQualityAssuranceSystem` runs a 6-layer validation on the results to ensure methodological rigor.

3.  **Reporting & Export**:
    *   **Analysis & Visualization**: Statistical tests are performed on the results, and visualizations are generated.
    *   **HTML Report**: A comprehensive, self-contained HTML report is created, summarizing the entire experiment.
    -   **Academic Exports**: Finally, the data is exported into publication-ready formats for use in tools like R, Stata, or SPSS, complete with metadata and analysis scripts. 