# Statistical Preparation Offramp - Provenance Integration
*Technical Integration with Discernus Provenance and GitHub Persistence*

---

## Question 1: Provenance System Integration

### Current Provenance Architecture

**Content-Addressable Storage**: All artifacts stored with SHA-256 hashes in `shared_cache/artifacts/`
**Git-Based Persistence**: Automatic commits of complete runs to version control
**Symlink Organization**: Human-readable structure with symlinks to content-addressed artifacts
**Complete Audit Trail**: Full dependency chains and processing logs

### Statistical Preparation Integration

#### New Artifacts in Content-Addressable Storage

```
shared_cache/artifacts/
├── derived_metrics_a7b3c8d2.json          # Framework-calculated composite scores
├── statistical_prep_package_f9e4d1c7.tar  # Complete researcher package
├── variable_codebook_2c8f5a91.csv         # Column definitions
└── evidence_full_quotes_8b2e7f43.csv      # Complete evidence (not truncated)
```

#### Provenance Chain Extension

**Current Chain:**
```
experiment.md → analysis → synthesis → finalization → git_commit
```

**With Statistical Preparation:**
```
experiment.md → analysis → statistical_prep → [OFFRAMP] → researcher_analysis
                     ↓
              git_commit (statistical prep)
                     
OR continue to:
statistical_prep → synthesis → finalization → git_commit (complete)
```

#### Content-Addressable Hashing for Statistical Prep

**Derived Metrics Hash**: `derived_metrics_hash = SHA256(scores + framework_formulas + calculation_metadata)`
- Enables caching: identical scores + framework = identical derived metrics
- Resume capability: can continue from statistical prep to synthesis
- Dependency tracking: synthesis stage depends on derived_metrics_hash

**Statistical Package Hash**: `statistical_package_hash = SHA256(csv_content + codebook + documentation)`
- Immutable researcher packages: identical inputs produce identical packages
- Version control: researchers can regenerate exact same package
- Integrity verification: package tampering detection

### Enhanced Manifest Structure

#### Statistical Preparation Stage Entry
```json
{
  "execution_stages": [
    {
      "stage_name": "statistical_preparation",
      "agent_name": "StatisticalPreparationAgent",
      "start_time": "2025-08-11T15:30:45Z",
      "end_time": "2025-08-11T15:31:02Z",
      "status": "completed",
      "metadata": {
        "derived_metrics_hash": "a7b3c8d2...",
        "statistical_package_hash": "f9e4d1c7...",
        "csv_records": 1000,
        "framework_formulas_applied": 5,
        "evidence_quotes_included": 10000,
        "package_format": "csv_with_codebook",
        "offramp_used": true
      }
    }
  ]
}
```

#### Dependency Tracking
```json
{
  "artifact_dependencies": {
    "derived_metrics_a7b3c8d2.json": {
      "depends_on": ["scores_hash", "evidence_hash", "framework_hash"],
      "stage": "statistical_preparation",
      "calculation_method": "framework_formulas"
    },
    "statistical_prep_package_f9e4d1c7.tar": {
      "depends_on": ["derived_metrics_hash", "scores_hash", "evidence_hash"],
      "stage": "statistical_preparation", 
      "format": "researcher_ready_csv"
    }
  }
}
```

### Git Integration for Statistical Preparation

#### Commit Message Strategy
```bash
# Statistical preparation offramp
git commit -m "Statistical prep: experiment_name"

# Full pipeline (existing)
git commit -m "Complete run: experiment_name"
```

#### Branch Strategy Options

**Option A: Same Branch (Recommended)**
- Statistical prep commits to same branch as full runs
- Clear commit messages distinguish between types
- Maintains simple git history

**Option B: Separate Branches**
- `statistical-prep` branch for offramp runs
- `main` branch for complete runs
- More complex but clear separation

---

## Question 2: Directory Structure Comparison

### Current Complete Run Structure

```
projects/experiment/runs/20250811T015608Z/
├── README.md                    # Complete audit guide
├── manifest.json                # Full execution record
├── results/                     # Final researcher outputs
│   ├── final_report.md         # Complete synthesis report
│   ├── scores.csv              # Raw dimensional scores  
│   ├── evidence.csv            # Supporting evidence quotes
│   ├── statistical_results.csv # Mathematical analysis
│   └── metadata.csv            # Provenance summary
├── artifacts/                   # Complete audit trail (symlinks)
│   ├── analysis_results/       # Raw LLM outputs
│   ├── analysis_plans/         # Processing strategies
│   ├── statistical_results/    # Mathematical computations
│   ├── evidence/               # Curated evidence
│   ├── reports/                # Synthesis outputs
│   ├── inputs/                 # Framework and corpus
│   └── provenance.json         # Artifact dependency map
├── logs/                        # System execution logs
│   ├── llm_interactions.jsonl  # Complete LLM conversations
│   ├── system.jsonl            # System events
│   ├── agents.jsonl            # Agent execution details
│   ├── costs.jsonl             # API cost tracking
│   └── artifacts.jsonl         # Artifact creation log
└── technical/                   # Additional technical logs
    ├── logs/
    └── model_interactions/
```

### Statistical Preparation Offramp Structure

```
projects/experiment/runs/20250811T015608Z/
├── README.md                    # Statistical prep guide (different content)
├── manifest.json                # Partial execution record (stops at stat prep)
├── results/                     # Researcher-ready outputs
│   ├── discernus_data.csv      # PRIMARY: Raw scores + derived metrics + evidence
│   ├── variable_codebook.csv   # Column definitions and metadata
│   ├── full_evidence.csv       # Complete evidence quotes (supplementary)
│   ├── framework_documentation.md # How framework was applied
│   ├── processing_log.json     # Audit trail of text processing
│   └── analysis_summary.json   # Statistical prep completion status
├── statistical_package/         # NEW: Complete researcher package
│   ├── discernus_data.csv      # Main dataset (symlink to results/)
│   ├── variable_codebook.csv   # Metadata (symlink to results/)
│   ├── full_evidence.csv       # Supplementary (symlink to results/)
│   ├── README.txt              # Plain text usage instructions
│   └── import_scripts/         # Tool-specific helpers
│       ├── import_spss.sps
│       ├── import_stata.do
│       └── import_r.R
├── artifacts/                   # Partial audit trail (analysis + stat prep only)
│   ├── analysis_results/       # Raw LLM outputs
│   ├── analysis_plans/         # Processing strategies  
│   ├── derived_metrics/        # NEW: Framework calculations
│   ├── evidence/               # Curated evidence
│   ├── inputs/                 # Framework and corpus
│   └── provenance.json         # Partial artifact map
├── logs/                        # Partial execution logs (analysis + stat prep)
│   ├── llm_interactions.jsonl  # LLM conversations (analysis only)
│   ├── system.jsonl            # System events (partial)
│   ├── agents.jsonl            # Agent execution (analysis + stat prep)
│   ├── costs.jsonl             # API costs (analysis only)
│   └── artifacts.jsonl         # Artifact creation (partial)
└── technical/                   # Partial technical logs
    ├── logs/
    └── model_interactions/
```

### Key Differences in Directory Structure

#### README.md Content Differences

**Complete Run README:**
```markdown
# Research Run: experiment_name

## 🎯 Start Here: Key Deliverables
- **`results/final_report.md`** - Complete research findings
- Statistical findings with confidence intervals
- Academic-grade methodology documentation

## 🔍 For Auditors: Complete Transparency
- Complete synthesis and interpretation available
- Full statistical analysis performed by Discernus
```

**Statistical Preparation README:**
```markdown  
# Statistical Preparation: experiment_name

## 🎯 Start Here: Researcher-Ready Data
- **`results/discernus_data.csv`** - Raw scores + derived metrics + evidence
- **`statistical_package/`** - Complete package for R/Python/STATA analysis

## 🔍 For Researchers: Analysis-Ready Data
- Text processing completed by Discernus
- Statistical analysis and interpretation: YOUR RESPONSIBILITY
- Complete audit trail of text processing decisions available

## 🚀 Next Steps
1. Load `discernus_data.csv` into your preferred statistical tool
2. Review `variable_codebook.csv` for column definitions  
3. Perform your own statistical analysis and interpretation
4. Cite: "Text analysis performed using Discernus; statistical analysis by [your method]"
```

#### Manifest.json Differences

**Complete Run:**
```json
{
  "experiment_mode": "complete_pipeline",
  "stages_completed": ["validation", "analysis", "synthesis", "finalization"],
  "final_deliverable": "results/final_report.md",
  "research_complete": true
}
```

**Statistical Preparation:**
```json
{
  "experiment_mode": "statistical_preparation",
  "stages_completed": ["validation", "analysis", "statistical_preparation"],
  "offramp_used": true,
  "researcher_package": "statistical_package/",
  "next_steps": "researcher_statistical_analysis",
  "resume_capability": {
    "can_continue_to_synthesis": true,
    "derived_metrics_hash": "a7b3c8d2...",
    "statistical_package_hash": "f9e4d1c7..."
  }
}
```

#### Missing Components in Statistical Preparation

**Not Present (Because Not Generated):**
- `artifacts/statistical_results/` - No Discernus statistical analysis
- `artifacts/reports/` - No synthesis reports
- `results/final_report.md` - No interpretation provided
- Synthesis-related logs and interactions

**Present But Partial:**
- `logs/llm_interactions.jsonl` - Only analysis stage interactions
- `artifacts/provenance.json` - Only analysis + statistical prep chain
- `costs.jsonl` - Only analysis stage costs

### Resume Capability Structure

#### Resuming from Statistical Preparation to Full Pipeline

**Command**: `discernus run --resume-from-stats`

**Additional Directory Structure Created:**
```
projects/experiment/runs/20250811T015608Z/
├── [existing statistical prep structure]
├── artifacts/                   # EXTENDED with synthesis artifacts
│   ├── statistical_results/    # NEW: Mathematical computations
│   ├── reports/                # NEW: Synthesis outputs  
│   └── provenance.json         # UPDATED: Complete artifact map
├── results/                     # EXTENDED with synthesis results
│   ├── final_report.md         # NEW: Complete research report
│   ├── statistical_results.csv # NEW: Discernus statistical analysis
│   └── [existing stat prep files remain]
└── logs/                        # EXTENDED with synthesis logs
    ├── llm_interactions.jsonl  # APPENDED: Synthesis interactions
    └── [other logs extended]
```

#### Manifest Update for Resume

```json
{
  "experiment_mode": "statistical_preparation_then_complete",
  "stages_completed": ["validation", "analysis", "statistical_preparation", "synthesis", "finalization"],
  "resume_history": [
    {
      "initial_run": "statistical_preparation",
      "timestamp": "2025-08-11T15:30:45Z",
      "offramp_used": true
    },
    {
      "resumed_run": "synthesis_continuation", 
      "timestamp": "2025-08-11T16:45:30Z",
      "resumed_from": "derived_metrics_a7b3c8d2"
    }
  ]
}
```

### Git Integration Differences

#### Statistical Preparation Commit

```bash
# Commit message
"Statistical prep: experiment_name"

# Files committed
projects/experiment/runs/20250811T015608Z/
├── README.md (statistical prep version)
├── manifest.json (partial)
├── results/ (researcher package)
├── statistical_package/ (complete package)
├── artifacts/ (partial)
└── logs/ (partial)
```

#### Complete Run Commit

```bash
# Commit message  
"Complete run: experiment_name"

# Files committed
projects/experiment/runs/20250811T015608Z/
├── README.md (complete version)
├── manifest.json (full)
├── results/ (complete with final_report.md)
├── artifacts/ (complete)
└── logs/ (complete)
```

#### Resume Commit Strategy

**Option A: Update Existing Commit**
- Amend the statistical prep commit with synthesis results
- Single commit contains complete run
- Cleaner git history

**Option B: Separate Resume Commit**
- New commit: "Resume synthesis: experiment_name"
- Two commits show the offramp → resume pattern
- Better audit trail of researcher decision

---

## Technical Implementation Considerations

### ProvenanceOrganizer Updates

#### New Artifact Categories
```python
def organize_statistical_preparation_artifacts(self):
    """Organize artifacts for statistical preparation offramp."""
    
    # Standard analysis artifacts
    self._organize_standard_artifacts()
    
    # New statistical preparation artifacts
    self._organize_derived_metrics()
    self._organize_researcher_package()
    self._create_statistical_prep_readme()
```

#### Modified README Generation
```python
def _create_statistical_prep_readme(self):
    """Generate README for statistical preparation offramp."""
    
    readme_content = f"""
# Statistical Preparation: {self.experiment_name}

## 🎯 Researcher-Ready Data Package
- Text processing completed by Discernus
- Statistical analysis: YOUR RESPONSIBILITY
- Complete audit trail available for transparency
    """
```

### Manifest Updates

#### New Stage Tracking
```python
class EnhancedManifest:
    def add_statistical_preparation_stage(self, 
                                        derived_metrics_hash: str,
                                        package_hash: str,
                                        offramp_used: bool = True):
        """Add statistical preparation stage to manifest."""
        
        stage_metadata = {
            "derived_metrics_hash": derived_metrics_hash,
            "statistical_package_hash": package_hash, 
            "offramp_used": offramp_used,
            "researcher_package_path": "statistical_package/",
            "resume_capability": True
        }
```

### Git Integration Updates

#### Modified Auto-Commit Logic
```python
def _auto_commit_run(self, run_folder, run_metadata, audit):
    """Auto-commit with statistical preparation awareness."""
    
    if run_metadata.get("offramp_used"):
        commit_msg = f"Statistical prep: {experiment_name}"
    else:
        commit_msg = f"Complete run: {experiment_name}"
    
    # Standard git operations
    self._execute_git_commit(commit_msg, run_folder)
```

---

## Summary

### Provenance Integration
- **Full compatibility** with existing content-addressable storage
- **Extended artifact chain** includes derived metrics and researcher packages
- **Git persistence** maintains same auto-commit with appropriate messaging
- **Resume capability** preserves complete provenance chain

### Directory Structure  
- **Statistical prep**: Researcher-focused structure with analysis-ready data
- **Complete run**: Academic-focused structure with full interpretation
- **Resume capability**: Seamless extension from statistical prep to complete
- **Consistent audit trail**: Same transparency standards regardless of offramp usage

The statistical preparation offramp integrates cleanly with existing provenance and persistence systems while providing researchers the control they need over statistical analysis and interpretation.

---

*Document Version: 1.0*  
*Date: August 2025*  
*Integration Status: Technical Specification Complete*
