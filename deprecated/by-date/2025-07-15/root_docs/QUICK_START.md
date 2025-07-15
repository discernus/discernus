# SOAR Quick Start Guide

This guide provides the essential commands to run experiments using the SOAR framework. The system is designed to be invoked via a simple, self-validating entrypoint.

## Running Experiments

### Prerequisites
```bash
# Activate your virtual environment
source venv/bin/activate

# Install dependencies (if you haven't already)
pip install -r requirements.txt
```

### The Modern Way: Workflow-Driven Execution

All modern experiments in this project are driven by a `workflow` definition inside the `experiment.md` file. This ensures the research process is explicit, reproducible, and transparent.

The execution command is always the same:

```bash
python3 -c "
from discernus.agents.validation_agent import ValidationAgent
agent = ValidationAgent()
agent.validate_and_execute_sync(
    'path/to/your/framework.md',
    'path/to/your/experiment.md', 
    'path/to/your/corpus/'
)
"
```

### Example: Running the "Claude Alpha" Reliability Test

This example runs a multi-stage experiment that includes analysis, statistical interpretation, and a peer-review cycle, all defined in the `workflow` block of the experiment file.

```bash
python3 -c "
from discernus.agents.validation_agent import ValidationAgent
agent = ValidationAgent()
agent.validate_and_execute_sync(
    'projects/attesor/experiments/06_even_deeper_smoke_test/framework_pdaf_v1.1_sanitized.md',
    'projects/attesor/experiments/06_even_deeper_smoke_test/experiment.md', 
    'projects/attesor/experiments/06_even_deeper_smoke_test/corpus'
)
"
```

### How It Works
1.  **Validation:** The `ValidationAgent` first validates all assets and uses its intelligence to propose and confirm any necessary fixes to your `experiment.md`.
2.  **Orchestration:** It then passes the validated assets to the `WorkflowOrchestrator`.
3.  **Execution:** The `WorkflowOrchestrator` reads the `workflow` from your `experiment.md` and executes the specified sequence of agents, passing the output of one as the input to the next.

This architecture ensures a transparent, reproducible, and powerful research process driven by the explicit definitions in your experiment files. For more details on the architecture, see `docs/AGENT_DESIGN_PRINCIPLES.md`. 