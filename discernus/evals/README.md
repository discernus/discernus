# Discernus Evaluation System (Pillar 3: Systematic Evals)

This directory contains the systematic evaluation pipeline for Discernus agents, implementing **Pillar 3** of our architectural foundation.

## Overview

The evaluation system uses `promptfoo` to test agents against a "golden set" of documents, ensuring consistent quality and preventing regressions as the system evolves.

## Philosophy

> "You cannot improve what you cannot measure."

Every critical prompt and model combination must be subject to automated tests that verify both **structural validity** (is it valid JSON?) and **semantic quality** (does the reasoning make sense?).

## Directory Structure

```
discernus/evals/
├── README.md                    # This documentation
└── eval_analysis_agent/         # EnhancedAnalysisAgent evaluation
    ├── promptfooconfig.yaml     # Test configuration
    ├── prompt_template.yaml     # Simplified prompt for testing
    ├── run_eval.py             # Python test runner
    └── golden_set/             # Test documents
        ├── Biden_Inaugural_2021.txt
        ├── Bush_Inaugural_2001.txt
        └── Trump_Inaugural_2017.txt
```

## Usage

### Quick Test Run

```bash
# Run all tests with all models
cd discernus/evals/eval_analysis_agent
python run_eval.py

# Test specific model only
python run_eval.py --model gemini-pro
python run_eval.py --model gemini-flash
```

### Direct Promptfoo Usage

```bash
# Run promptfoo directly
cd discernus/evals/eval_analysis_agent
npx promptfoo eval

# View results in web UI
npx promptfoo view
```

## Test Coverage

### Current Tests (EnhancedAnalysisAgent)

The evaluation pipeline currently tests:

1. **Structural Output Validation**
   - JSON validity
   - Required top-level keys: `analysis_summary`, `document_analyses`, `mathematical_verification`, `self_assessment`

2. **Model Performance Comparison**
   - Gemini 2.5 Pro vs Gemini 2.5 Flash
   - Consistency across different input documents

3. **Golden Set Documents**
   - Biden Inaugural 2021 (Democratic perspective)
   - Bush Inaugural 2001 (Republican perspective)
   - Trump Inaugural 2017 (Populist perspective)

### Assertions Tested

Each test case validates:
- ✅ **JSON Structure**: Response must be valid JSON
- ✅ **Required Fields**: All expected top-level keys present
- ✅ **Content Quality**: LLM-as-judge semantic validation (future enhancement)

## Integration with Development Workflow

### Pre-Commit Testing

```bash
# Add to git pre-commit hook
cd discernus/evals/eval_analysis_agent
python run_eval.py || exit 1
```

### Continuous Integration

The evaluation pipeline is designed to run in CI/CD pipelines to catch regressions:

```yaml
# Example GitHub Actions step
- name: Run Agent Evaluations
  run: |
    cd discernus/evals/eval_analysis_agent
    python run_eval.py
```

## Extending the Evaluation System

### Adding New Test Cases

1. Add document to `golden_set/`
2. Update `promptfooconfig.yaml` with new test case
3. Run evaluation to establish baseline

### Adding New Agents

1. Create new directory: `eval_{agent_name}/`
2. Copy and adapt configuration files
3. Create agent-specific golden set
4. Implement agent-specific assertions

### Advanced Assertions

Promptfoo supports sophisticated testing patterns:

```yaml
# LLM-as-judge semantic validation
assert:
  - type: llm-rubric
    value: |
      The analysis should demonstrate:
      1. Clear understanding of the document's worldview
      2. Accurate numerical calculations
      3. Logical reasoning for character assessments
      
# Statistical validation
assert:
  - type: javascript
    value: |
      const data = JSON.parse(output);
      const scores = Object.values(data.document_analyses)[0].scores;
      return Object.values(scores).every(s => s.intensity >= 0 && s.intensity <= 1);
```

## Architecture Alignment

This evaluation system embodies **THIN principles**:

- **LLM Intelligence**: Uses LLM-as-judge for semantic validation
- **Minimal Software**: Simple Python wrapper around proven `promptfoo` infrastructure
- **Externalized Prompts**: Prompts stored in YAML files for version control
- **Industry Standards**: Leverages `promptfoo` rather than building custom evaluation

## Future Enhancements

### Planned Features (Post-MVP)

1. **LLM-as-Judge Semantic Validation**
   - Use more powerful model to evaluate reasoning quality
   - Automated detection of hallucinated statistics

2. **Performance Benchmarking**
   - Response time tracking
   - Cost-per-evaluation metrics
   - Model efficiency comparisons

3. **Regression Detection**
   - Historical baselines
   - Automated alerts for quality degradation
   - A/B testing for prompt improvements

4. **Multi-Agent Workflows**
   - End-to-end pipeline testing
   - Cross-agent consistency validation

---

**Status**: ✅ **Pillar 3 (Systematic Evals) - IMPLEMENTED**
- Basic evaluation pipeline operational
- Golden set established
- Automated test runner created
- Ready for production use 