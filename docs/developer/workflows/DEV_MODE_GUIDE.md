# Discernus Development Mode Guide

## ✅ **System Status**
- **Knowledgenaut**: Fixed using THIN architecture (now works as expert agent)
- **Development Mode**: Fully operational with automated human researcher simulation
- **Self-Documenting**: THIN architecture guides built-in to prevent future issues

## 🧪 **Quick Testing**

### Run Default Test
```bash
python3 discernus/dev_test_runner.py
```

### Custom Research Question
```bash
python3 discernus/dev_test_runner.py --question "How does rhetoric work in political speeches?" --corpus "data/my_texts/"
```

### Test DiscernusLibrarian Specifically
```bash
python3 -m discernus.core.discernuslibrarian
```

### Different Researcher Profiles
```bash
python3 discernus/dev_test_runner.py --profile "political_discourse_expert"
python3 discernus/dev_test_runner.py --list-profiles
```

## 🎯 **What Development Mode Does**

1. **Automated Design Process**: AI design agent creates research methodology
2. **Simulated Human Feedback**: AI simulates experienced researcher reviewing the design
3. **Iterative Improvement**: System refines design based on feedback (up to 3 iterations)
4. **Automated Approval**: AI researcher decides whether to approve or request revisions
5. **Full Execution**: Runs the complete multi-expert analysis workflow
6. **Results Capture**: Saves everything to timestamped session folders

## 📋 **Available Researcher Profiles**

- `computational_social_scientist`: Quantitative text analysis expert
- `political_discourse_expert`: Political communication and rhetoric expert  
- `digital_humanities_scholar`: Computational linguistics background
- `data_scientist`: NLP and text mining specialist
- `rhetorical_analyst`: Classical and modern rhetorical analysis

## 📁 **Results Location**

Results are saved in: `research_sessions/session_YYYYMMDD_HHMMSS/`

Each session contains:
- `metadata.json`: Session configuration and status
- `conversation_*.jsonl`: Complete conversation log
- `conversation_readable.md`: Human-readable formatted results (when completed)

## 🔧 **Programmatic Usage**

```python
from discernus.orchestration.orchestrator import ThinOrchestrator

# Quick analysis
results = await ThinOrchestrator.quick_analysis(
    research_question="How does rhetoric work?",
    corpus_path="data/my_texts/",
    researcher_profile="political_discourse_expert"
)

# Full control
config = ResearchConfig(
    research_question="My research question",
    source_texts="My source texts",
    enable_code_execution=True,
    dev_mode=True,
    simulated_researcher_profile="computational_social_scientist"
)

orchestrator = ThinOrchestrator()
results = await orchestrator.run_automated_session(config)
```

## 🛠️ **THIN Architecture Features**

- **Expert Prompts**: Stored in `discernus/core/agent_roles.py`
- **Validation**: Run `python3 -c "from discernus.core.thin_validation import check_thin_compliance; check_thin_compliance()"`
- **Self-Documentation**: Built-in guidance prevents THICK anti-patterns
- **Pattern Examples**: `ThinHelper.show_expert_pattern()` for templates

## 📊 **Cost Optimization**

- **Gemini Models**: 10-40x cheaper than Claude for development
- **Vertex AI**: Automatically used when configured
- **Fallback**: Claude/OpenAI when Vertex AI unavailable
- **Mock Responses**: Graceful degradation when APIs unavailable

## 🔄 **Development Workflow**

1. **Write Question**: Define your research question
2. **Point to Corpus**: Provide path to texts to analyze
3. **Run Dev Mode**: Let system simulate full research workflow
4. **Review Results**: Check generated analysis in session folder
5. **Iterate**: Refine question/corpus based on results

This system eliminates the need for manual intervention during development and testing, making it easy to iterate on research questions and validate the DiscernusLibrarian functionality. 