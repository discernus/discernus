# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Commands
```bash
# Install dependencies
python3 -m pip install --user --break-system-packages -r requirements.txt

# Install with development dependencies
python3 -m pip install --user --break-system-packages -e ".[dev]"

# Run tests
python3 -m pytest discernus/tests/
pytest discernus/tests/

# Code quality checks
black --line-length 120 discernus/
isort --profile black --line-length 120 discernus/
flake8 discernus/

# CLI commands - Current Interface
python3 -m discernus.cli run <experiment_path>       # Complete experiment (analysis + synthesis)
python3 -m discernus.cli continue <experiment_path>  # Resume from existing artifacts
python3 -m discernus.cli debug <experiment_path>     # Interactive debugging mode
python3 -m discernus.cli validate <experiment_path>  # Validate experiment structure
python3 -m discernus.cli list                        # List available experiments
python3 -m discernus.cli status                      # Infrastructure status
python3 -m discernus.cli start                       # Start infrastructure
python3 -m discernus.cli stop                        # Stop infrastructure

# Alternative: Use Makefile commands
make run EXPERIMENT=<path>      # Run complete experiment
make continue EXPERIMENT=<path> # Resume from artifacts
make debug EXPERIMENT=<path>    # Interactive debugging
make check                     # Verify environment
make test                      # Run test suite
```

### Quick Test Commands
```bash
# Run quick validation tests
python3 discernus/tests/quick_test.py

# Run comprehensive test suite
python3 discernus/tests/comprehensive_test_suite.py

# Run single test file
pytest discernus/tests/test_analysis_agent.py -v
```

### DiscernusLibrarian Commands
```bash
# Test DiscernusLibrarian research agent
python3 -m discernus.core.discernuslibrarian

# Results stored in discernus/librarian/
# - reports/ - Human-readable markdown reports
# - research_data/ - JSON data for programmatic access  
# - archives/ - Long-term storage by date/topic
```

## Architecture Overview

### THIN Philosophy
This codebase follows the "Thick LLM + Thin Software = Epistemic Trust" philosophy:
- **LLM Intelligence**: Analysis, reasoning, and content generation handled in prompts
- **Software Infrastructure**: Simple routing, storage, and execution
- **Natural Language Flow**: LLM-to-LLM communication without complex parsing
- **Centralized Prompts**: Prompts are part of agents that consume them, not hardcoded

### Core Components

**CLI Entry Point**: `discernus/cli.py` - Main command interface with validate/execute/resume commands

**Core Infrastructure** (`discernus/core/`):
- `spec_loader.py` - Loads V4 frameworks, V2 experiments, and corpus specifications
- `discernuslibrarian.py` - Citation-guided research agent using Vertex AI (located in `discernus/librarian/`)
- `project_chronolog.py` - Git-based provenance and session tracking
- `simple_llm_client.py` / `ultra_thin_llm_client.py` - LLM gateway abstractions

**Agent System** (`discernus/agents/`):
- `analysis_agent.py` - Primary text analysis using framework prompts
- `synthesis_agent.py` - Generates academic-quality reports
- `ensemble_configuration_agent.py` - Multi-model experiment orchestration
- Additional specialized agents for specific analytical tasks

**Orchestration** (`discernus/orchestration/`):
- `workflow_orchestrator.py` - Executes multi-step research workflows
- `ensemble_orchestrator.py` - Manages multi-model ensemble experiments

**Gateway** (`discernus/gateway/`):
- `llm_gateway.py` - Multi-provider LLM access via LiteLLM
- `model_registry.py` - Model configuration and cost management
- `models.yaml` - Model definitions and pricing

### Key Patterns

**Project Structure**: 
- Experiments live in `projects/` with framework, experiment, corpus, and results subdirectories
- Each project has a `PROJECT_CHRONOLOG.jsonl` for session tracking
- Results stored with full provenance in timestamped session directories

**Specification System**:
- V4 Framework specifications define analytical approaches in Markdown with YAML config