# CARA: Conversational Academic Research Architecture

## Overview

CARA (Conversational Academic Research Architecture) is a revolutionary approach to computational academic research that eliminates traditional parsing brittleness through pure LLM dialogue while maintaining rigorous academic standards.

## Core Principles

### 1. Conversation-Native Processing
- All analysis occurs through natural language dialogue between LLMs
- No structured parsing or data extraction from LLM responses
- Analysis emerges from conversation flow, not imposed data structures
- Natural uncertainty expression through conversational disagreement

### 2. Strategically Thin Software
- Minimal custom code focused on enabling conversation, not managing it
- Leverage mature infrastructure (Redis, Celery, Git, Python) for heavy lifting
- Software orchestrates rather than interprets or analyzes
- Maximum functionality with minimum complexity

### 3. Complete Transparency
- Every analytical decision logged in natural language
- Full conversation histories preserved for audit and replication
- All generated code and execution results logged
- Academic reviewers can read actual reasoning chains

### 4. Simple Code Execution
- Lightweight subprocess-based code execution  
- Simple security through static analysis and resource limits
- Academic appropriateness standards and code review workflow
- Complete audit trail of all computational operations

## Architecture Components

### Core Components

```
cara/
├── core/
│   ├── conversation_logger.py    # Ultra-thin conversation logging
│   └── simple_code_executor.py   # Lightweight subprocess code execution
├── orchestration/
│   └── cara_orchestrator.py      # Ultra-thin orchestration engine
└── demo/
    └── cara_demo.py              # Demonstration script
```

### Key Features

- **ConversationLogger**: Records all LLM interactions verbatim to Git
- **SimpleCodeExecutor**: Lightweight security for code execution
- **CARAOrchestrator**: Ultra-thin coordination of multi-LLM conversations
- **Code Review**: LLM-based code review for academic appropriateness
- **Resource Management**: Simple subprocess isolation with resource limits

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Git** (for conversation logging)
3. **LLM API Access** (Claude, GPT-4, etc.)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd discernus
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your LLM API keys
```

## Usage

### Quick Test

Run a quick test to verify the system works:

```bash
python3 cara/demo/cara_demo.py --quick
```

### Full Demo

Run the full demonstration:

```bash
python3 cara/demo/cara_demo.py
```

### Custom Analysis

Create your own analysis script:

```python
import asyncio
from cara.orchestration.cara_orchestrator import CARAOrchestrator, ConversationConfig

async def analyze_speech():
    # Initialize orchestrator
    orchestrator = CARAOrchestrator()
    
    # Configure conversation
    config = ConversationConfig(
        research_question="Is this speech populist or pluralist?",
        participants=["populist_expert", "pluralist_expert"],
        speech_text="Your speech text here...",
        models={
            "populist_expert": "claude-3-5-sonnet",
            "pluralist_expert": "claude-3-5-sonnet"
        },
        max_turns=5,
        enable_code_execution=True
    )
    
    # Run conversation
    conversation_id = await orchestrator.start_conversation(config)
    results = await orchestrator.run_conversation(conversation_id)
    
    return results

# Run analysis
results = asyncio.run(analyze_speech())
```

## Security Features

### Multi-Layer Security

1. **Static Analysis**: Pattern matching for dangerous operations
2. **Import Validation**: Only approved libraries allowed
3. **Resource Limits**: Time constraints and workspace isolation
4. **Subprocess Isolation**: Isolated execution environment
5. **Code Review**: LLM-based academic appropriateness review

### Allowed Libraries

- Statistical analysis: `pandas`, `numpy`, `scipy`, `statistics`
- Visualization: `matplotlib`, `seaborn`, `plotly`
- Text processing: `nltk`, `textblob`, `re`
- Machine learning: `sklearn`
- Standard libraries: `json`, `math`, `collections`, `datetime`

### Prohibited Operations

- Network requests (`requests`, `urllib`, `socket`)
- System commands (`os.system`, `subprocess`)
- File system access outside workspace
- Cryptocurrency mining operations
- Infinite loops or resource abuse

## File Structure

After running CARA, your project will have:

```
project_root/
├── conversations/              # All conversation logs
│   ├── conversation_20240101_120000_abc123.jsonl
│   └── conversation_20240101_130000_def456.jsonl
├── code_workspace/            # Code execution workspaces
│   ├── conversation_20240101_120000_abc123/
│   │   ├── code_hash123.py
│   │   └── execution_logs.json
│   └── conversation_20240101_130000_def456/
└── .git/                      # Git repository with all conversations
```

## Integration with Existing System

CARA leverages existing Discernus infrastructure:

- **LiteLLM Client**: Unified API across LLM providers
- **Git Integration**: Version control and transparency
- **Docker Support**: Containerized execution environment

## Development

### Running Tests

```bash
# Quick component test
python3 cara/demo/cara_demo.py --quick

# Full integration test
python3 cara/demo/cara_demo.py
```

### Adding New Participants

To add a new expert participant:

1. Update `_build_participant_prompt()` in `cara_orchestrator.py`
2. Add participant-specific prompts and expertise
3. Configure the participant in your `ConversationConfig`

### Security Customization

To modify security settings:

1. Edit `allowed_libraries` in `simple_code_executor.py`
2. Update `dangerous_patterns` for additional security checks
3. Modify resource limits in `_execute_in_subprocess()`

## Roadmap

### Phase 1: Core Implementation ✅
- [x] Conversation-native logging
- [x] Simple code execution
- [x] Multi-LLM orchestration
- [x] Basic demonstration

### Phase 2: Enhanced Features (Planned)
- [ ] Redis/Celery integration for distributed processing
- [ ] Advanced code review with specialized models
- [ ] Enterprise governance and compliance features
- [ ] Performance optimization and scaling

### Phase 3: Academic Validation (Planned)
- [ ] Replication of van der Veen et al. (2024) study
- [ ] Academic peer review and validation
- [ ] Publication of methodology and results
- [ ] Community adoption and feedback

## Contributing

CARA follows the "strategically thin software" philosophy:

1. **Minimal Code**: Only add code that enables conversation
2. **Leverage Infrastructure**: Use mature tools (Git, Redis)
3. **Conversation-Native**: No parsing of LLM responses
4. **Complete Transparency**: All operations logged to Git

## License

This project is part of the Discernus academic research platform.

## Support

For questions or issues:

1. Check the conversation logs in `conversations/`
2. Review code execution logs in `code_workspace/`
3. Examine Git history for full transparency
4. Create issues in the project repository

## Academic Citation

When using CARA in academic work, please cite:

```
CARA: Conversational Academic Research Architecture
A parser-free approach to computational academic research
with simple code execution and complete transparency
``` 