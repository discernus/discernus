# GitHub Issues Setup Guide

## ✅ **Status: Issue Templates Ready**

GitHub issue templates have been created and are available at:
`https://github.com/discernus/discernus/issues/new/choose`

## 🏷️ **Labels to Create**

Run these commands after `gh auth login`:

```bash
# Core issue types
gh label create "bug" --description "System defect or unexpected behavior" --color "d73a4a"
gh label create "enhancement" --description "Feature improvement or new capability" --color "a2eeef"
gh label create "research" --description "Methodological question or academic concern" --color "7057ff"

# Triage and priority
gh label create "needs-triage" --description "Requires initial assessment" --color "fbca04"
gh label create "release-blocker" --description "Must be fixed before 1.0 release" --color "b60205"
gh label create "high-priority" --description "Important for current milestone" --color "ff9500"

# Component areas  
gh label create "agents" --description "Agent system components" --color "0052cc"
gh label create "orchestration" --description "Workflow orchestration system" --color "5319e7"
gh label create "synthesis" --description "Report synthesis and generation" --color "1d76db"
gh label create "data-quality" --description "Data integrity and validation" --color "0e8a16"
gh label create "framework-support" --description "Framework compatibility" --color "c2e0c6"

# Academic/Research specific
gh label create "statistical-methodology" --description "Statistical analysis concerns" --color "ffc649"
gh label create "reproducibility" --description "Research reproducibility issues" --color "c5def5"
gh label create "peer-review" --description "Academic standards and quality" --color "f9d0c4"
```

## 🚨 **First Issues to Create**

### Issue #1: Resume Functionality Bug
```
Title: [BUG] Resume command restarts experiment instead of continuing from checkpoint
Labels: bug, release-blocker, orchestration
Priority: Critical

Description:
The `discernus_cli.py resume` command fails to continue from saved checkpoints and instead restarts experiments from scratch, causing duplicate work and wasted API costs.

Steps to Reproduce:
1. Start experiment: `python3 discernus_cli.py execute framework.md experiment.md corpus/ --dev-mode`
2. Stop during analysis phase (after ~20-30 LLM calls completed)
3. Resume: `python3 discernus_cli.py resume project/path`
4. System creates new session and re-analyzes same texts

Expected: Continue from checkpoint, skip completed analyses
Actual: New session, duplicate analyses, wasted costs

Impact: Could waste hundreds of dollars on large experiments
```

### Issue #2: SynthesisAgent Enhancement Validation
```
Title: [ENHANCEMENT] Validate enhanced SynthesisAgent generates academic-quality reports  
Labels: enhancement, synthesis, high-priority
Priority: High

Description:
Enhanced SynthesisAgent has been developed with comprehensive statistical analysis capabilities, but needs validation against the manually created exemplary report.

Benefits:
- Research quality: Generates peer-review quality academic reports
- Efficiency: Eliminates manual report creation 
- Cost: No additional API calls for synthesis enhancement

Implementation Notes:
- Enhanced prompt already created and tested with prompt harness
- Code integrated into production SynthesisAgent  
- Ready for end-to-end testing with existing experimental data
- Should match quality of manually created exemplary report
```

### Issue #3: DataIntegrityAnalyst Implementation
```
Title: [ENHANCEMENT] Implement DataIntegrityAnalyst quality gate
Labels: enhancement, data-quality, agents
Priority: High  

Description:
Add DataIntegrityAnalyst agent between CalculationAgent and SynthesisAgent to ensure data quality before statistical analysis.

Benefits:
- Research quality: Prevents contaminated data from reaching conclusions
- Efficiency: Early detection of data issues before analysis fails
- Academic standards: Explicit quality gates for research integrity

Implementation Notes:
- Design specification already created in PM documents
- Should validate completeness, consistency, and statistical outliers
- Framework-agnostic design following THIN principles
```

## 📋 **Next Steps**

1. **Authenticate GitHub CLI**: `gh auth login`  
2. **Create labels**: Run the label creation commands above
3. **File initial issues**: Create the three priority issues
4. **Test workflow**: Use GitHub Issues for tracking progress

## 🎯 **Usage Guidelines**

- **Bug reports**: Use for system defects, unexpected behavior
- **Enhancements**: Use for feature improvements, new capabilities  
- **Research questions**: Use for methodological concerns, academic standards
- **Release blockers**: Critical issues that must be fixed before 1.0
- **Academic focus**: Always consider research integrity and peer review standards 