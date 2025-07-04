# Discernus: Conversational Academic Research Architecture

Ultra-thin platform for LLM-native computational research through natural conversation with integrated code execution.

## Philosophy

**Strategically Thin Software**: Provide LLMs with execution capability and transparency, not predefined functions.

**Conversation-Native**: Analysis emerges from natural dialogue, not parsing or structured responses.

**Academic Rigor**: Complete git transparency and reproducible computational workflows.

## Quick Start

```bash
# Install minimal dependencies
pip install GitPython litellm python-dotenv

# Configure API keys
cp .env.example .env  # Add your LLM API keys

# Run demonstration
python3 discernus/demo/demo.py --quick
```

## Core Concept

Instead of building complex analysis functions, Discernus gives LLMs:
- **Code execution** (```python blocks in conversation)
- **Conversation logging** (git-native transparency)  
- **Multi-LLM coordination** (academic peer review)

LLMs naturally request statistical analysis, effect sizes, visualizations, etc. when needed.

## Architecture

```
discernus/
├── core/
│   ├── conversation_logger.py      # Git-native conversation logging
│   └── simple_code_executor.py     # Ultra-thin code execution (50 lines)
├── orchestration/
│   └── orchestrator.py            # Multi-LLM coordination
├── demo/
│   └── demo.py                     # Working demonstration
└── gateway/                        # LiteLLM integration
```

## Example Usage

```python
from discernus.orchestration.orchestrator import DiscernusOrchestrator

# Let LLMs analyze naturally
orchestrator = DiscernusOrchestrator()
results = await orchestrator.run_conversation(config)

# Code execution happens automatically in conversation:
# LLM: "I need to check reliability:"
# ```python
# import scipy.stats
# cronbach_alpha = calculate_reliability(data)
# ```
# System: *executes* → *enhances response with results*
```

## Academic Integration

- **Complete transparency**: Every conversation committed to git
- **Reproducible research**: All code execution logged and auditable
- **Peer review workflow**: Multi-LLM academic validation
- **Citation-ready**: Conversation logs as supplementary materials

## Dependencies

**Core** (6 packages):
- GitPython (conversation logging)
- litellm (LLM access)
- python-dotenv (configuration)
- numpy, pandas, scipy (when LLMs request analysis)

**Optional** (install as needed):
- statsmodels, scikit-learn, plotly, jupyter

## Getting Started

1. **Demo**: `python3 discernus/demo/demo.py --quick`
2. **Full conversation**: `python3 discernus/demo/demo.py`
3. **Custom research**: Import `DiscernusOrchestrator` and configure

Built for academic researchers who want computational capability without infrastructure complexity.
