# 04: Futures & Roadmap for the Discernus Platform

This document outlines the planned evolution of the Discernus platform, guided by our question-driven development methodology. Each phase builds upon the last, incrementally adding value and technical sophistication while ensuring we do not lose the valuable, detailed thinking from the original reboot specifications.

## Guiding Principles
- **Evolve, Don't "Big Bang":** We will not attempt to build the entire system at once. Features will be added as they are required to answer the next researcher question.
- **Introduce Complexity Only When Necessary:** Powerful technologies like `PostgreSQL` and `Celery` are part of the long-term vision, but they will only be implemented when the scale of the user's question demands them.
- **Preserve the Core IP:** The unique geometric visualization and the academic rigor of the frameworks remain the project's core assets. All architectural choices are in service of making this IP more accessible and powerful.

## Cross-Phase Architectural Decisions

### Workflow Engine Integration Strategy
**Decision Timeline**: The platform will transition from native async/await orchestration to battle-tested workflow engines based on complexity triggers, not arbitrary timelines.

**Current State (Phase 1)**: 
- Native FastAPI async/await handles simple experiments (20 min, 64-96 analyses)
- Sequential processing prevents TPM limit violations
- Database persistence provides basic checkpointing

**Integration Triggers** (likely Phase 3-4):
- **Duration**: Experiments exceeding 1-2 hours consistently
- **Complexity**: Multi-step experiments requiring sophisticated retry logic
- **Concurrency**: Multiple simultaneous experiments with resource conflicts
- **Scheduling**: Time-based or event-driven experiment execution needs

**Candidate Technologies**:
- **Prefect**: Research-friendly, Python-native, excellent observability
- **Airflow**: Battle-tested for complex DAGs, extensive ecosystem
- **Temporal**: Modern approach with strong consistency guarantees

**Integration Strategy**: Build clean async/await foundation that can wrap existing experiment logic in workflow engine tasks without major refactoring. The current `execute_experiment()` functions become workflow tasks.

### Conversational Interface Strategy
**Vision**: "English as Code" - Natural language experiment design and execution that democratizes access to sophisticated research capabilities.

**Current State**: 
- Researchers manually construct YAML experiment definitions
- API endpoints require technical knowledge of parameters
- Complex statistical concepts require domain expertise to interpret

**Evolution Path**:
- **Phase 2-3**: Natural language experiment queries ("Compare OpenAI and Anthropic on political speeches")
- **Phase 3-4**: Conversational analysis ("What if we excluded the extreme texts?", "Show me the correlation breakdown")
- **Phase 4**: Full research assistant with memory, context, and iterative refinement

**Technical Foundation**:
- Experiment YAML as intermediate representation (researchers can still access)
- LLM-powered query translation to structured experiment definitions
- Conversational state management for iterative research workflows
- Natural language result interpretation and recommendations

**Risk Mitigation**: Maintain transparency - researchers can always inspect/modify the underlying experiment configuration generated from their natural language requests.

## Phase 2: Comparative, Temporal, and Longitudinal Analysis

- **Driving Question:** *"I have the signature for Text A. Now, how does it compare to Text B, and how do signatures for a single author evolve over time?"*
- **User Value:** Moves from single-point analysis to comparative and time-series insight, which is fundamental to narrative and political research.
- **Architectural Evolution (from `des_temporal_comparative_extension.md`):**
    - **State Management:** The application will need to "remember" previous analyses to enable comparison.
    - **Initial Persistence:** Introduce a simple persistence layer (e.g., `SQLite`) to store results, acting as a prototype for the full PostgreSQL database.
    - **API Enhancement:**
        - Create a new `/compare` endpoint that takes two sets of analysis parameters.
        - Add a `/trajectory` endpoint for longitudinal analysis of a single author.
    - **Visualization:**
        - Leverage the visualizer's side-by-side and overlay comparison modes.
        - Develop a new time-series plot to show an author's signature `centroid` drift over time.
    - **DES Evolution:** The internal Experiment Definition will be expanded to support new optional keys:
        - `comparative`: Defines pairings of texts or corpora.
        - `temporal`: Defines time windows and smoothing algorithms.
        - `longitudinal`: Defines the author/speaker metadata field to track.

## Phase 3: Group-Level Analysis & Systematic Sweeps

- **Driving Question:** *"How does the average signature of one group (e.g., Republicans) compare to another (e.g., Democrats)? And how robust is my analysis to changes in the prompt?"*
- **User Value:** Enables true quantitative social science and robustness testing.
- **Architectural Evolution (from `des_next_axes_v1.md`):**
    - **Full Database Implementation:** Migrate from SQLite to **PostgreSQL**. The schema will be finalized to store all runs, signatures, centroids, and experiment metadata, becoming the single source of truth.
    - **Asynchronous Task Queue:** Implement **Celery** and **Redis** to process large batches of texts and parameter sweeps without blocking the user interface.
    - **Corpus Management:** Introduce `corpus.strata` to define metadata-based cohorts (e.g., by party, gender, etc.) for stratified analysis.
    - **DES Evolution:**
        - Add an `analysis_mode: stratified` flag.
        - Introduce an `experiment_matrix.parameter_grid` to systematically vary inputs like LLM temperature, prompt wording, or few-shot examples.

## Phase 4: Full Academic & Conversational Platform

- **Driving Question:** *"Let's design a complex experiment with human raters, local models, and RAG. Then, run it, analyze the results with a custom script, and get a publication-ready replication package. I want to orchestrate this via chat."*
- **User Value:** The platform becomes a full-fledged research assistant.
- **Architectural Evolution (from `des_evaluator_extensions_v0.1.md`, `des_additional_dimensions_v1.md`, and `des_analysis_visual_guidance_v0.1.md`):**
    - **Unified `evaluators` Layer:** Abstract the "who" of the analysis. The `evaluators` list in the DES will support `cloud_llm`, `local_llm`, `human_crowd` (e.g., MTurk), and `human_offline` (pre-existing data).
    - **Advanced Research Dimensions:** The DES will support optional blocks for:
        - `context_enrichment`: For Retrieval-Augmented Generation (RAG).
        - `multimodal`: To incorporate images or other media.
        - `perturbation_tests`: To systematically test robustness.
    - **Advanced Analysis & Visualization:**
        - **Analysis Recipes (AR):** A simple YAML-based DSL for common analysis operations (`filter`, `groupby`, `stats`).
        - **Visualization Recipes (VR):** A Vega-Lite/Plotly JSON format for defining custom plots.
        - **Auto-Generated Notebooks:** Every run will still produce a baseline, auto-generated Jupyter notebook for maximum flexibility.
    - **Conversational UI:** Build a true chat interface on top of the powerful, mature backend API, fulfilling the "English-as-Code" vision.

This phased approach allows us to deliver value at every step while building steadily towards the ambitious and powerful vision laid out in the original reboot documents. 