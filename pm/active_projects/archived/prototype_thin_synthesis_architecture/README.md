# THIN Code-Generated Synthesis Architecture - Standalone Prototype

## Overview

This prototype implements the breakthrough THIN Code-Generated Synthesis Architecture designed to solve the fundamental scalability limitations of monolithic LLM synthesis approaches.

## Key Innovation

Instead of asking LLMs to perform complex statistical analysis directly (which leads to hallucination and token limits), we ask them to **generate Python code** that performs the analysis. This leverages:

- **LLM Intelligence**: For understanding frameworks and generating appropriate analytical approaches
- **Deterministic Software**: For reliable mathematical computation (pandas, numpy, scipy)
- **Post-Computation Evidence Curation**: Evidence selection based on *actual* statistical results

## Architecture

### 4-Agent Pipeline

1. **AnalyticalCodeGenerator**: LLM generates framework-appropriate Python analysis code
2. **CodeExecutor**: Executes the generated code in a sandboxed environment  
3. **EvidenceCurator**: LLM selects relevant evidence based on actual statistical results
4. **ResultsInterpreter**: LLM synthesizes statistical results + curated evidence into final narrative

### Separation of Concerns

- **Deterministic Tasks**: Code generation → execution → statistical results
- **Subjective Tasks**: Evidence curation → narrative interpretation
- **Critical Sequencing**: Evidence curation happens *after* statistical computation

## Directory Structure

```
agents/
├── analytical_code_generator/    # Issue #167
├── code_executor/               # Issue #168  
├── evidence_curator/            # Issue #169
└── results_interpreter/         # Issue #170
orchestration/                   # Issue #171
test_data/                      # Synthetic test datasets
```

## Usage

```python
from orchestration.pipeline import ThinSynthesisPipeline

pipeline = ThinSynthesisPipeline()
result = pipeline.run(
    framework_spec="path/to/framework.md",
    scores_csv="path/to/scores.csv", 
    evidence_csv="path/to/evidence.csv"
)
```

## Success Criteria

- [ ] Framework-agnostic code generation
- [ ] Reliable statistical computation
- [ ] Intelligent evidence curation  
- [ ] Scalable synthesis without token limits
- [ ] Superior quality vs. monolithic approach

## Related Issues

- Epic: #166
- Phase 1 Implementation: #167-171
- Phase 2 Integration: #174
- Quality Validation: #172-173 