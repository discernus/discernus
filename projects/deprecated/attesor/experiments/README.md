# Attesor Study Experiment Iterations

This directory organizes experiment iterations for incremental testing and validation before the full Attesor study.

## Directory Structure

```
experiments/
├── active/                           # Current experiment for orchestrator
│   ├── pdaf_v1.1_sanitized_framework.md
│   ├── attesor_bias_isolation_experiment.md
│   ├── corpus/
│   ├── orchestrator_validation.md   # Results: infrastructure validation
│   ├── raw_analysis_scores.json     # Results: PDAF anchor scores
│   └── audit_trail.jsonl           # Results: essential provenance
├── 01_smoketest/                    # Minimal orchestrator validation
│   ├── framework, experiment, corpus (assets)
│   └── validation results (when run)
├── 02_single_llm_pilot/             # Single-model bias detection test  
│   ├── framework, experiment, corpus (assets)
│   └── bias analysis results (when run)
├── 03_full_study/                   # Full 864-analysis study (future)
│   ├── framework, experiment, corpus (assets)
│   └── academic publication materials (when run)
└── README.md                        # This file
```

## Experiment Progression Strategy

### Phase 1: Infrastructure Validation (01_smoketest)
- **Purpose**: Validate THIN orchestrator changes work correctly
- **Scope**: 2 speeches, 1 model, sanitized condition only
- **Duration**: 5-10 minutes
- **Cost**: ~$0.50
- **Key Test**: Orchestrator chooses RAW_AGGREGATION workflow

### Phase 2: Methodology Validation (02_single_llm_pilot)
- **Purpose**: Test complete bias isolation protocol
- **Scope**: 4 speeches, 1 model, all 3 conditions
- **Duration**: 30-45 minutes  
- **Cost**: ~$2-3
- **Key Test**: Bias detection and cross-linguistic mitigation

### Phase 3: Full Study (03_full_study)
- **Purpose**: Complete multi-LLM bias characterization
- **Scope**: 8 speeches, 6 models, all 3 conditions
- **Duration**: 2-4 hours
- **Cost**: ~$25-40
- **Key Test**: Universal bias across premium models

## Usage Pattern

### Running Experiments

**Active Experiment** (what orchestrator sees):
```bash
# Point orchestrator to active experiment - results generated in same directory
python3 -c "from discernus.agents.validation_agent import ValidationAgent; ValidationAgent().validate_and_execute_sync('experiments/active/pdaf_v1.1_sanitized_framework.md', 'experiments/active/attesor_bias_isolation_experiment.md', 'experiments/active/corpus')"
```

**Specific Iteration**:
```bash
# Run smoke test - results saved alongside assets
python3 -c "from discernus.agents.validation_agent import ValidationAgent; ValidationAgent().validate_and_execute_sync('experiments/01_smoketest/pdaf_v1.1_sanitized_framework.md', 'experiments/01_smoketest/smoketest_experiment.md', 'experiments/01_smoketest/corpus')"
```

### Complete Project Management

**Package Complete Experiment** (assets + results):
```bash
# Zip entire experiment with all assets and results
zip -r attesor_smoketest_$(date +%Y%m%d).zip experiments/01_smoketest/

# Git commit complete experiment atomically  
git add experiments/01_smoketest/
git commit -m "Complete smoketest: assets + results"
```

**Promote Tested Experiment**:
```bash
# Copy complete experiment (assets + any existing results) to active
cp -r experiments/02_single_llm_pilot/* experiments/active/
```

**Archive Completed Project**:
```bash
# Archive complete project with all assets and results
mv experiments/active experiments/archive/attesor_full_study_$(date +%Y%m%d_%H%M%S)
```

## Benefits of Unified Project Structure

### Complete Asset Packaging  
- **Single Archive**: Zip one directory to get framework + experiment + corpus + results
- **Atomic Git Commits**: All related files committed together for complete provenance
- **Asset Discovery**: ValidationAgent finds everything in one location
- **No Fragmentation**: Results stay with the assets that generated them

### For Development
- **Incremental Testing**: Test changes on small scale before full commitment
- **Cost Control**: Validate methodology cheaply before expensive full runs
- **Risk Mitigation**: Catch issues early in development cycle
- **Complete Packaging**: Each experiment is self-contained unit

### For Research
- **Methodology Validation**: Prove approach works before major resource investment
- **Hypothesis Testing**: Test specific aspects of bias isolation protocol
- **Academic Documentation**: Clear research progression for publication
- **Replication Packages**: Complete experiments ready for sharing/archiving

### For Collaboration
- **Clear Iterations**: Other researchers can understand development progression
- **Reproducible Stages**: Each experiment fully documented and reproducible
- **Selective Testing**: Contributors can run relevant experiment subsets
- **Complete Handoffs**: Share entire experiment directories with all assets and results

## File Naming Convention

**Descriptive Names** (ValidationAgent reads English):
- `pdaf_v1.1_sanitized_framework.md` (not `framework.md`)
- `attesor_bias_isolation_experiment.md` (not `experiment.md`)
- `smoketest_experiment.md` (not `experiment.md`)

**Benefits**:
- Clear purpose from filename
- No confusion about content
- Easy to track across iterations
- Natural discovery for agents

This structure enables confident progression from small tests to full study while maintaining complete documentation and reproducibility. 