# Unified Project Structure: Assets + Results Together

## The Better Approach: Complete Project Packaging

Instead of separating results from assets, each experiment directory contains **everything** needed for complete packaging, archiving, and sharing.

## Structure

### Smoketest Project (Infrastructure Validation)
```
experiments/01_smoketest/
├── pdaf_v1.1_sanitized_framework.md       # Asset: framework
├── smoketest_experiment.md                # Asset: experiment definition  
├── corpus/                                # Asset: test corpus (2 speeches)
├── orchestrator_validation.md             # Result: workflow verification
├── raw_analysis_scores.json               # Result: PDAF anchor scores
├── validation_report.md                   # Result: go/no-go decision
└── system_logs.jsonl                      # Result: debugging info
```

### Pilot Project (Methodology Validation) 
```
experiments/02_single_llm_pilot/
├── pdaf_v1.1_sanitized_framework.md       # Asset: framework
├── single_llm_pilot_experiment.md         # Asset: experiment definition
├── corpus/                                # Asset: corpus (4 speeches × 3 conditions)
├── bias_detection_report.md               # Result: human-readable findings
├── raw_pdaf_scores.json                   # Result: complete anchor scores
├── statistical_analysis.md                # Result: effect sizes & correlations
├── methodology_validation.md              # Result: academic assessment
├── pilot_summary.json                     # Result: machine-readable summary
└── audit_trail.jsonl                      # Result: essential provenance
```

### Full Study Project (Academic Publication)
```
experiments/03_full_study/
├── pdaf_v1.1_sanitized_framework.md       # Asset: framework
├── attesor_bias_isolation_experiment.md   # Asset: experiment definition
├── corpus/                                # Asset: complete corpus (8 speeches × 3 conditions)
├── academic_findings_report.md            # Result: publication summary
├── comprehensive_bias_analysis.md         # Result: cross-model analysis
├── cross_linguistic_validation.md         # Result: Esperanto effectiveness
├── raw_data/                              # Result: complete dataset
│   ├── pdaf_scores_by_model.json
│   ├── pdaf_scores_by_speech.json
│   └── model_metadata.json
├── statistical_outputs/                   # Result: formal analysis
│   ├── bias_effect_sizes.csv
│   ├── correlation_matrices.csv
│   └── significance_tests.csv
├── publication_materials/                 # Result: ready-to-submit
│   ├── paper_1_crisis_documentation.md
│   ├── paper_2_solution_validation.md
│   └── replication_package/
└── complete_audit_trail.jsonl             # Result: research integrity
```

## Benefits of Unified Structure

### Complete Packaging
- **Single Archive**: `zip -r experiment.zip experiments/01_smoketest/` gets everything
- **Atomic Commits**: `git add experiments/01_smoketest/` commits all related files
- **No Fragmentation**: Results never separated from the assets that generated them
- **Self-Contained**: Each directory is complete experimental package

### Academic Benefits  
- **Replication Ready**: Send entire directory for independent validation
- **Archive Friendly**: Complete experimental record in one location
- **Publication Support**: All materials and results together for peer review
- **Audit Trail**: Complete provenance maintained with experimental assets

### Development Benefits
- **Clean Handoffs**: Copy entire experiment directory between researchers
- **Version Control**: All experiment components tracked together
- **Discovery**: ValidationAgent finds everything in project root
- **Promotion**: `cp -r pilot/* active/` moves complete experiment

## Usage Patterns

### Running Experiments
```bash
# Run experiment - results saved in same directory
python3 -c "from discernus.agents.validation_agent import ValidationAgent; 
ValidationAgent().validate_and_execute_sync(
    'experiments/01_smoketest/pdaf_v1.1_sanitized_framework.md',
    'experiments/01_smoketest/smoketest_experiment.md', 
    'experiments/01_smoketest/corpus'
)"

# Results appear alongside assets:
# experiments/01_smoketest/orchestrator_validation.md
# experiments/01_smoketest/raw_analysis_scores.json
```

### Complete Project Management
```bash
# Archive complete experiment
zip -r attesor_smoketest_$(date +%Y%m%d).zip experiments/01_smoketest/

# Git commit everything atomically
git add experiments/01_smoketest/
git commit -m "Complete smoketest experiment: assets + results"

# Share with collaborators
scp -r experiments/01_smoketest/ colleague@university:/research/
```

### Experiment Promotion
```bash
# Promote tested experiment to active (assets + any existing results)
cp -r experiments/02_single_llm_pilot/* experiments/active/

# Archive completed experiment  
mv experiments/active experiments/archive/attesor_full_study_$(date +%Y%m%d)
```

## Implementation Changes

### Orchestrator Modifications
**Current**: Save results to separate `/results` directory
**New**: Save results directly to project directory

```python
# Instead of: self.results_path / "session_results" 
# Save to: self.project_path / "bias_detection_report.md"

def _save_results_to_project(self, results_data):
    """Save results directly to project directory alongside assets"""
    
    # Save human-readable bias analysis
    bias_report_path = self.project_path / "bias_detection_report.md"
    bias_report_path.write_text(self._generate_bias_report(results_data))
    
    # Save raw scores for statistical analysis  
    scores_path = self.project_path / "raw_pdaf_scores.json"
    scores_path.write_text(json.dumps(results_data['anchor_scores'], indent=2))
    
    # Save minimal audit trail
    audit_path = self.project_path / "audit_trail.jsonl"
    self._append_audit_entry(audit_path, results_data)
```

### ValidationAgent Integration
ValidationAgent can discover both assets AND results in same directory:

```python
def discover_complete_experiment(self, project_path):
    """Discover both experimental assets and any existing results"""
    
    assets = {
        'framework': self._find_framework_file(project_path),
        'experiment': self._find_experiment_file(project_path), 
        'corpus': self._find_corpus_directory(project_path)
    }
    
    results = {
        'bias_reports': self._find_bias_reports(project_path),
        'raw_scores': self._find_score_files(project_path),
        'audit_trails': self._find_audit_files(project_path)
    }
    
    return {'assets': assets, 'results': results}
```

This unified structure makes each experiment a complete, self-contained research package that can be easily archived, shared, and reproduced. 