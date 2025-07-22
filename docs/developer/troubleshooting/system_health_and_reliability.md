# System Health and Reliability Architecture

This document provides a comprehensive overview of the multi-layered system designed to ensure the reliability, transparency, and cost-effectiveness of all Large Language Model (LLM) operations within the Discernus platform. This architecture is a direct implementation of the "Smart Colleague" and "Transparent, Tidy, and Traceable" design principles.

## The Core Problem: Managing API Fragility

Relying on third-party LLM APIs introduces significant fragility into the system. These APIs can fail for numerous reasons, including network issues, provider outages, misconfigured credentials, and, most subtly, unexpected reactions to API parameters. The architecture is designed to proactively and reactively manage this fragility.

## The Three-Pronged Solution

The system employs a three-pronged strategy to ensure model health and reliability:

1.  **A Centralized Knowledge Base (`models.yaml`)**: All provider- and model-specific knowledge is externalized into a single, human-readable configuration file, establishing a single source of truth.
2.  **A Smart, Rule-Based Parameter Manager**: A dedicated software component reads the configuration and systematically "cleans" all API requests to ensure they are safe and compliant.
3.  **A Dual-Mode Health-Checking System**: The platform uses both proactive, scheduled monitoring and on-demand, just-in-time checks to validate model availability.

---

### 1. `models.yaml`: The Single Source of Truth

The `discernus/gateway/models.yaml` file is the heart of the reliability system. It is a "Thick" knowledge base that contains all the hard-won, provider-specific intelligence required for stable operation.

**Key Features:**

*   **Provider Defaults**: A `provider_defaults` section at the top of the file defines baseline rules for each provider, including:
    *   `forbidden_params`: A list of API parameters (e.g., `max_tokens`) that are known to cause issues and must be stripped from requests.
    *   `required_params`: A dictionary of parameters (e.g., the `safety_settings` for Vertex AI) that must be included in every call to ensure correct behavior.
    *   `timeout`: A default timeout value for the provider.
*   **Model-Specific Overrides**: Each individual model definition can override the provider defaults, allowing for fine-grained control (e.g., setting a longer timeout for a slow, local `ollama` model).
*   **Utility Tier System**: A `utility_tier` for each model allows for intelligent, automated model selection and fallback. Lower numbers indicate higher priority.
*   **Task Suitability**: A `task_suitability` list for each model allows the system to choose the most appropriate tool for a given job (e.g., `synthesis`, `coordination`).

---

### 2. `ProviderParameterManager`: The Rule-Based Engine

The `discernus/gateway/provider_parameter_manager.py` class is the "Thin" software engine that enforces the rules defined in `models.yaml`.

**Key Features:**

*   **Configuration-Driven**: It loads all of its logic from `models.yaml` at initialization. It has no hardcoded rules.
*   **Parameter Cleaning**: Its core method, `get_clean_parameters`, takes a model name and a dictionary of parameters and systematically applies the rules from the configuration file, returning a "safe" set of parameters for the API call.
*   **Centralized Enforcement**: The `LLMGateway` is hardwired to pass all API call parameters through this manager before execution, ensuring that every single call made by the system is compliant.

---

### 3. The Dual-Mode Health-Checking System

The platform uses two complementary methods to monitor model health.

**A. Proactive, Scheduled Monitoring**

*   **Component**: `scripts/test_model_availability.py`
*   **Purpose**: This script is designed to be run on a schedule (e.g., a weekly cron job) to provide a regular, proactive report on the status of all key models. This allows operators to identify and fix issues with API keys or provider outages *before* they impact users.

**B. On-Demand, Just-in-Time Validation**

*   **Component**: `discernus/agents/project_coherence_analyst.py`
*   **Purpose**: This agent performs an on-demand health check at the beginning of every `execute` command.
*   **Workflow**: It parses the `experiment.md` to identify the specific models required for the run and then performs a health check only on those models. If a required model is unavailable, it immediately stops the execution and provides a clear, actionable error message to the user, preventing wasted time and resources.

This multi-layered system, built on the principle of externalizing complex knowledge into a "Thick" configuration file and using "Thin" software to enforce it, provides a robust, transparent, and easily maintainable solution to the complex problem of managing third-party LLM APIs. 