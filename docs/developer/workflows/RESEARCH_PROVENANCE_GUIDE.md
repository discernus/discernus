# Research Provenance Guide

**For Researchers Using Discernus**

## Quick Start: Automatic Research Preservation

**Every Discernus research run is automatically preserved with complete provenance.** You don't need to do anything special - just run your experiments and everything is saved for academic integrity.

### Default Behavior (Recommended)

```bash
# Run your experiment - everything preserved automatically
discernus run projects/my_study --analysis-only

# Output shows automatic preservation:
📝 Auto-committed to Git: Complete run 20250804T175152Z: my_study
✅ Experiment completed successfully!
   📋 Run ID: 20250804T175152Z
   📁 Results: projects/my_study/runs/20250804T175152Z
```

**What happens automatically:**
- ✅ Complete run directory created with all results
- ✅ Comprehensive README generated for auditors
- ✅ All artifacts preserved with cryptographic integrity
- ✅ Run committed to Git with timestamp
- ✅ Validation script available for integrity checking

### Manual Control (If Preferred)

```bash
# Disable auto-commit for manual Git control
discernus run projects/my_study --no-auto-commit

# Manually commit when ready
git add projects/my_study/runs/20250804T175152Z
git commit -m "Analysis for paper submission"
```

## Understanding Your Research Provenance

### What Gets Preserved

**Every research run creates a complete academic package:**

```
projects/my_study/runs/20250804T175152Z/
├── README.md                    # ← Start here for audit trail
├── results/                     # ← Your research outputs
│   ├── final_report.md         # Main findings
│   ├── scores.csv              # Quantitative data
│   ├── evidence.csv            # Supporting quotes
│   └── metadata.csv            # Complete provenance
├── artifacts/                   # ← Complete transparency
│   ├── analysis_results/       # What the AI actually said
│   ├── statistical_results/    # Mathematical computations
│   ├── evidence/               # How evidence was curated
│   └── inputs/                 # Framework and data used
└── logs/                        # ← System execution record
    ├── llm_interactions.jsonl  # Complete AI conversations
    ├── system.jsonl            # System events
    └── costs.jsonl             # API usage tracking
```

### Academic Value

**Citation-Ready Research:**
- **Permanent Identifier**: Git commit hash (e.g., `efba4a7b`)
- **Complete Methodology**: Auto-generated documentation
- **Reproducibility Package**: All inputs and parameters preserved
- **Audit Trail**: Every decision documented and traceable

**Example Citation:**
```
Analysis conducted using Civic Analysis Framework v7.1 applied to 2 political 
speeches. Computational analysis employed Gemini 2.5 Flash with validation 
correlation. Reproducibility materials: Git commit efba4a7b.
```

## Working with Provenance

### Validating Your Research

**Quick Integrity Check:**
```bash
# Verify everything is intact
python3 scripts/validate_run_integrity.py projects/my_study/runs/20250804T175152Z

# Output:
🎉 INTEGRITY VERIFICATION: PASSED
   This research run has consistent content-addressed integrity.
   All artifacts match expected hashes and are traceable.
```

**Detailed Validation:**
```bash
# See all validation steps
python3 scripts/validate_run_integrity.py projects/my_study/runs/20250804T175152Z --verbose

# Include Git history check
python3 scripts/validate_run_integrity.py projects/my_study/runs/20250804T175152Z --check-git
```

### Preparing for Peer Review

**Your research run includes everything reviewers need:**

1. **Start Point**: `README.md` - Complete audit guide
2. **Main Results**: `results/final_report.md` - Your findings
3. **Raw Data**: `results/*.csv` - All quantitative outputs
4. **Transparency**: `artifacts/` - What AI systems actually output
5. **Methodology**: `logs/llm_interactions.jsonl` - Complete AI conversations

**For External Reviewers:**
```bash
# Give reviewers this command for quick validation
python3 scripts/validate_run_integrity.py [your_run_path]

# They can also manually inspect
cat README.md                    # Audit guide
ls -la artifacts/               # Artifact structure
grep "cost_usd" logs/costs.jsonl # Resource usage
```

### Sharing Research

**Complete Reproducibility Package:**
```bash
# Your entire run directory is self-contained
tar -czf my_study_20250804T175152Z.tar.gz projects/my_study/runs/20250804T175152Z/

# Or share the Git repository with commit hash
git log --oneline | grep "20250804T175152Z"
efba4a7b Complete run 20250804T175152Z: my_study
```

**What collaborators get:**
- ✅ Exact framework and corpus used
- ✅ Complete AI interaction logs
- ✅ All mathematical computations
- ✅ Statistical validation data
- ✅ Comprehensive audit trail
- ✅ Validation tools for verification

## Academic Workflow Integration

### For Paper Writing

**Methodology Section Generation:**
```
Analysis conducted using [Framework Name] v[Version] applied to [N] documents. 
Computational analysis employed [AI Model] with cross-validation. 
Statistical reliability: [Metrics from statistical_results.csv].
Reproducibility materials: Git commit [hash] in [repository].
```

**Data Availability Statement:**
```
All analysis data, computational logs, and reproducibility materials are 
available in the research repository at [Git URL], commit [hash]. 
Validation tools are provided for independent verification.
```

### For Conference Presentations

**Transparency Slide:**
```
Research Transparency
• Complete computational audit trail preserved
• All AI interactions logged and available
• Statistical computations independently verifiable  
• Reproducibility package: [Git commit hash]
• Validation: python3 scripts/validate_run_integrity.py [path]
```

### For Thesis/Dissertation

**Appendix: Computational Methods**
- Include complete `final_report.md` 
- Reference specific Git commits for each analysis
- Provide validation commands for committee members
- Include methodology sections from auto-generated documentation

## Best Practices

### Organizing Multiple Studies

**Project Structure:**
```
projects/
├── dissertation_study_1/
│   └── runs/
│       ├── 20250801T143022Z/  # Pilot analysis
│       ├── 20250804T175152Z/  # Main analysis  
│       └── 20250807T091234Z/  # Robustness check
├── dissertation_study_2/
│   └── runs/
│       └── 20250810T164455Z/  # Cross-validation
└── conference_paper/
    └── runs/
        └── 20250815T102233Z/  # Final analysis
```

**Git History Navigation:**
```bash
# Find all runs for a project
git log --oneline --grep="dissertation_study_1"

# See what changed between runs
git diff efba4a7b..a1b2c3d4 projects/dissertation_study_1/

# Tag important analyses
git tag -a "thesis-chapter-3" efba4a7b -m "Main analysis for Chapter 3"
```

### Quality Assurance

**Before Submission:**
1. **Validate All Runs**: `python3 scripts/validate_run_integrity.py [path] --check-git`
2. **Review README Files**: Ensure audit trails are complete
3. **Check Git History**: Verify all important runs are committed
4. **Test Reproducibility**: Try following your own methodology documentation

**Red Flags to Check:**
- ❌ Empty CSV files in results/
- ❌ Missing artifacts/ directories
- ❌ Broken symlinks in artifacts/
- ❌ Git commits missing for important runs
- ❌ Validation script failures

### Collaboration

**Sharing with Collaborators:**
```bash
# Share specific run
git add projects/shared_study/runs/20250804T175152Z
git commit -m "Add main analysis for review"
git push origin main

# Collaborators can validate
git pull
python3 scripts/validate_run_integrity.py projects/shared_study/runs/20250804T175152Z
```

**Working with Advisors:**
- Share Git repository with complete history
- Use commit hashes to reference specific analyses
- Provide validation commands for independent checking
- Include README files for non-technical reviewers

## Troubleshooting

### Common Issues

**"Auto-commit failed" Warning:**
```bash
# Usually harmless - check if run was actually saved
ls projects/my_study/runs/
python3 scripts/validate_run_integrity.py [run_path]

# If needed, commit manually
git add projects/my_study/runs/[run_id]
git commit -m "Manual commit for run [run_id]"
```

**Missing Results Files:**
```bash
# Check if analysis completed successfully
cat projects/my_study/runs/[run_id]/logs/system.jsonl | grep "error"

# Validate run integrity
python3 scripts/validate_run_integrity.py [run_path] --verbose
```

**Broken Symlinks:**
```bash
# Check shared cache
ls projects/my_study/shared_cache/artifacts/

# Validate and get details
python3 scripts/validate_run_integrity.py [run_path] --verbose
```

### Getting Help

**Self-Diagnosis:**
1. Read the run's `README.md` file
2. Run validation script with `--verbose` flag
3. Check `logs/system.jsonl` for errors
4. Verify Git status: `git status`

**Reporting Issues:**
- Include validation script output
- Provide Git commit hash if available
- Share relevant log excerpts from `logs/` directory
- Specify what you were trying to accomplish

## Advanced Usage

### Custom Validation

**Create Your Own Checks:**
```python
# Custom validation script
import json
from pathlib import Path

def validate_my_requirements(run_path):
    manifest = json.loads((run_path / "manifest.json").read_text())
    
    # Check custom requirements
    assert manifest["costs"]["total_cost_usd"] < 5.00
    assert len(manifest["corpus_files"]) >= 10
    # ... your validation logic
```

### Integration with Other Tools

**R/Python Analysis:**
```python
# Load Discernus results into your analysis
import pandas as pd

scores = pd.read_csv("projects/my_study/runs/20250804T175152Z/results/scores.csv")
evidence = pd.read_csv("projects/my_study/runs/20250804T175152Z/results/evidence.csv")

# Your statistical analysis here
# Results are automatically linked to Discernus provenance
```

**LaTeX Integration:**
```latex
\section{Computational Methods}
Analysis conducted using Discernus v2.0 with Civic Analysis Framework v7.1 
applied to \texttt{corpus\_files} political speeches. 
Complete reproducibility package available at Git commit 
\texttt{efba4a7b} with validation via 
\texttt{python3 scripts/validate\_run\_integrity.py}.
```

## Conclusion

The Discernus provenance system **automatically handles research transparency** so you can focus on your research questions. Every run creates a complete academic package that meets the highest standards for:

- ✅ **Peer review** - Complete audit trails
- ✅ **Replication** - All inputs and parameters preserved  
- ✅ **Academic integrity** - Tamper-evident provenance
- ✅ **Collaboration** - Self-contained reproducibility packages

**Just run your experiments** - everything else is handled automatically. When you're ready for peer review, submission, or collaboration, your complete provenance package is ready to go.