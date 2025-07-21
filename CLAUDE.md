# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Install with development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest discernus/tests/
pytest discernus/tests/

# Code quality checks
black --line-length 120 discernus/
isort --profile black --line-length 120 discernus/
flake8 discernus/

# CLI commands
python3 discernus_cli.py validate <framework_file> <experiment_file> <corpus_dir>
python3 discernus_cli.py execute <framework_file> <experiment_file> <corpus_dir>
python3 discernus_cli.py resume <project_path>
python3 discernus_cli.py list-frameworks
python3 discernus_cli.py test
```

### Quick Test Commands
```bash
# Run quick validation tests
python discernus/tests/quick_test.py

# Run comprehensive test suite
python discernus/tests/comprehensive_test_suite.py

# Run single test file
pytest discernus/tests/test_analysis_agent.py -v
```

## Architecture Overview

### THIN Philosophy
This codebase follows the "Thick LLM + Thin Software = Epistemic Trust" philosophy:
- **LLM Intelligence**: Analysis, reasoning, and content generation handled in prompts
- **Software Infrastructure**: Simple routing, storage, and execution
- **Natural Language Flow**: LLM-to-LLM communication without complex parsing
- **Centralized Prompts**: Prompts are part of agents that consume them, not hardcoded

### Core Components

**CLI Entry Point**: `discernus_cli.py` - Main command interface with validate/execute/resume commands

**Core Infrastructure** (`discernus/core/`):
- `spec_loader.py` - Loads V4 frameworks, V2 experiments, and corpus specifications
- `knowledgenaut.py` - Citation-guided research agent using Vertex AI
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
- V2 Experiment specifications define models, runs, and statistical plans
- V2 Corpus specifications define text collections with metadata

**Agent Communication**:
- Agents receive natural language prompts and return structured data (not code)
- State flows between agents as enriched dictionaries
- No complex JSON parsing - agents prompted to return clean, parseable responses

### Testing Strategy

**Test Categories**:
- `quick_test.py` - Fast validation of core functionality
- `comprehensive_test_suite.py` - Full system integration tests
- `workflow_integration_tests.py` - End-to-end workflow validation
- Mock LLM responses in `tests/fixtures/realistic_responses/`

**Test Execution**:
- Tests run independently without external LLM calls via mock responses
- Realistic test data generation for agent validation
- Agent isolation testing framework for individual component validation

### Development Guidelines

**THIN Compliance**:
- Keep software logic minimal - delegate intelligence to LLMs
- Avoid hardcoded prompts in orchestrator code
- Use natural language for agent-to-agent communication
- Prefer structured data return over code generation

**Cost Management**:
- Primary models use cost-effective Vertex AI Gemini 2.5 Flash ($0.13/$0.38 per 1M tokens)
- Premium models (Claude) reserved for critique and synthesis
- Transparent cost estimation in experiment planning

**Debugging**:
- Session logs capture full execution traces in `results/session_*/`
- Conversation logs in JSONL format for LLM interaction replay
- State snapshots saved after each workflow step for resumption