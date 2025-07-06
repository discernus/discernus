# Discernus Package

## Overview

The `discernus` package provides the core infrastructure for computational academic research with THIN architecture principles.

## Package Structure

### Production Code
- **`core/`**: Core services (knowledgenaut, corpus inspector, session management, conversation logging)
- **`gateway/`**: LLM API management (unified gateway, LiteLLM integration)
- **`orchestration/`**: Multi-agent conversation orchestration
- **`web/`**: Flask-based web interface

### Development & Testing
- **`dev_tools/`**: Development utilities (Vertex AI setup, test runner, timing analyzer, corpus demo)
- **`tests/`**: Test suite (infrastructure tests, end-to-end tests)

## Installation

From the project root:
```bash
pip install -r requirements.txt
```

## Usage

### Basic LLM Client
```python
from discernus.gateway.llm_gateway import LLMGateway

gateway = LLMGateway()
response = gateway.call_llm("gpt-4", "Your research question here")
```

### Research Agent
```python
from discernus.core.knowledgenaut import UltraThinKnowledgenaut

knowledgenaut = UltraThinKnowledgenaut()
research_results = knowledgenaut.research_question("Your research question")
```

### Expert Agent Prompts
```python
from discernus.core.llm_roles import get_expert_prompt

prompt = get_expert_prompt("political_psychology_expert")
```

## Development

### Running Tests
```bash
# Quick infrastructure test
python3 discernus/tests/simple_test.py

# Full MVP test
python3 discernus/tests/mvp_test.py

# End-to-end conversation test
python3 discernus/tests/end_to_end_test.py
```

### Development Tools
```bash
# Setup Vertex AI for cheaper LLM access
python3 discernus/dev_tools/setup_vertex_ai.py

# Run automated development tests
python3 discernus/dev_tools/dev_test_runner.py

# Analyze conversation timing
python3 discernus/dev_tools/analyze_conversation_timing.py <session_id>
```

### Architecture

This package follows THIN architecture principles:
- Minimal code that enables LLM conversations
- Leverage proven third-party infrastructure (LiteLLM, Git)
- No complex parsing or data structures
- Maximum transparency through conversation logging

See `pm/cara_architecture_specification.md` for detailed architectural documentation and development philosophy.
