# Discernus Provenance System Architecture

**Version**: 2.0  
**Status**: Production Ready  
**Last Updated**: August 2025

## Overview

The Discernus Provenance System provides **comprehensive research transparency** through a multi-layered architecture that ensures every computational decision can be traced, verified, and reproduced. This system meets the highest academic standards for computational social science research.

## Architecture Principles

### 1. **Content-Addressed Integrity**
- Every artifact stored with SHA-256 hash for tamper detection
- Modification of any content results in different hash
- Deduplication through content addressing
- Cryptographic verification of data consistency

### 2. **Automatic Git Persistence**
- All successful research runs automatically committed to Git
- Complete audit trail with timestamps and commit hashes
- Distributed backup through Git remotes
- Optional opt-out via `--no-auto-commit` flag

### 3. **Human-Readable Organization**
- Symlink architecture for academic-friendly file structure
- Clear directory organization with descriptive names
- Comprehensive README files for each research run
- Automated validation scripts for integrity checking

### 4. **Complete Dependency Tracking**
- Full provenance chain from inputs to conclusions
- Artifact metadata includes all dependencies
- Recursive dependency resolution for cached results
- Tamper-evident dependency verification

## System Components

### Content-Addressable Storage

```
shared_cache/artifacts/
├── analysis_response_185f5e58.json    # Raw AI analysis output
├── statistical_results_ecbe79b4.json  # Mathematical computations  
├── curated_evidence_35008a8b.json     # Supporting evidence
└── final_report_c54d6e63.md          # Synthesis results
```

**Features**:
- **SHA-256 hashing**: 8-character prefix for human readability
- **Deduplication**: Identical content shared across runs
- **Integrity verification**: `sha256sum` validation available
- **Metadata storage**: Complete provenance information

### Git-Based Permanent Provenance

**Automatic Commits**:
```bash
# Default behavior - auto-commit enabled
discernus run projects/experiment --analysis-only
📝 Auto-committed to Git: Complete run 20250804T223703Z: experiment

# Opt-out for manual control  
discernus run projects/experiment --no-auto-commit
```

**Git Integration Features**:
- **Force override**: Preserves research despite .gitignore patterns
- **Short commit messages**: Under 50 characters per terminal compatibility
- **Timeout protection**: 30-second limit prevents hanging
- **Non-blocking**: Git failures don't break research runs
- **Comprehensive logging**: All Git operations logged for audit

### Human-Readable Run Organization

```
projects/experiment/runs/20250804T175152Z/
├── README.md                    # Complete audit guide
├── manifest.json                # Execution record
├── results/                     # Final outputs
│   ├── final_report.md         # Main deliverable
│   ├── scores.csv              # Quantitative results
│   ├── evidence.csv            # Supporting evidence
│   └── metadata.csv            # Provenance summary
├── artifacts/                   # Complete audit trail (symlinks)
│   ├── analysis_results/       # AI system outputs
│   ├── statistical_results/    # Mathematical work
│   ├── evidence/               # Supporting evidence
│   ├── inputs/                 # Framework and data
│   └── provenance.json         # Artifact dependency map
└── logs/                        # System execution logs
    ├── llm_interactions.jsonl  # Complete AI conversations
    ├── system.jsonl            # System events
    ├── agents.jsonl            # Agent execution
    └── costs.jsonl             # API cost tracking
```

### Automated Validation System

**Integrity Validation Script**: `scripts/validate_run_integrity.py`

```bash
# Quick integrity check
python3 scripts/validate_run_integrity.py projects/experiment/runs/20250804T175152Z

# Verbose validation with all checks
python3 scripts/validate_run_integrity.py projects/experiment/runs/20250804T175152Z --verbose

# Include Git history validation
python3 scripts/validate_run_integrity.py projects/experiment/runs/20250804T175152Z --check-git
```

**Validation Coverage**:
- **Manifest Structure**: Execution metadata completeness
- **Results Files**: Expected outputs exist and are substantial
- **Symlink Integrity**: All artifact links resolve correctly
- **Hash Integrity**: Content matches expected SHA-256 hashes
- **Provenance Chain**: Complete dependency relationships
- **Git History**: Run exists in repository history

## Academic Standards Compliance

### Computational Reproducibility

**Complete Transparency**:
- Every computation and decision preserved
- Raw AI system outputs available for inspection
- Mathematical work documented with source data
- Complete methodology documentation auto-generated

**Reproducibility Package**:
- Exact inputs preserved (framework, corpus, parameters)
- Environment specifications documented
- Complete audit trail from raw data to conclusions
- Validation tools for independent verification

**Integrity Guarantees**:
- Content-addressed hashing enables modification detection
- Git timestamps document sequence of operations
- Cryptographic dependency chains prevent tampering
- Distributed Git storage enables independent verification

### Peer Review Support

**Auditor-Friendly Design**:
- Clear navigation with README guides
- Common audit questions answered upfront
- Recommended audit workflows (5 min, 30 min, 2+ hours)
- Automated validation scripts for quick verification

**Academic Integration**:
- Citation-ready metadata with Git commit hashes
- Methodology sections auto-generated for papers
- Complete reproducibility packages for replication studies
- Academic presentation tools for research transparency

## Usage Patterns

### For Researchers

**Default Workflow** (Automatic Provenance):
```bash
# Run experiment - everything preserved automatically
discernus run projects/my_study --analysis-only

# Results automatically organized and committed to Git
# README generated with complete audit trail
# Validation script available for integrity checking
```

**Manual Control Workflow**:
```bash
# Disable auto-commit for manual Git control
discernus run projects/my_study --no-auto-commit

# Manually commit when ready
git add projects/my_study/runs/20250804T175152Z
git commit -m "Complete analysis for paper submission"
```

### For Auditors and Reviewers

**Quick Integrity Check** (5 minutes):
```bash
# Automated validation
python3 scripts/validate_run_integrity.py [run_path]

# Manual spot checks
ls -la artifacts/                    # Check symlink structure
cat README.md                       # Review audit guide
grep "cost_usd" logs/costs.jsonl    # Verify resource usage
```

**Standard Audit** (30 minutes):
1. Review `manifest.json` for execution record
2. Examine `artifacts/inputs/` for framework and data
3. Check `artifacts/analysis_results/` for AI outputs
4. Verify `artifacts/statistical_results/` for computations
5. Cross-reference `results/` with artifact chain

**Deep Forensic Audit** (2+ hours):
1. Complete log analysis in `logs/` directory
2. Validate every symlink and dependency
3. Review `logs/llm_interactions.jsonl` for prompt analysis
4. Attempt independent replication using preserved inputs
5. Statistical validation of mathematical computations

## Security Model

### Threat Model

**Designed to Defend Against**:
- Accidental data corruption or loss
- Unintended modification of research results
- Academic integrity challenges during peer review
- Reproducibility failures in replication studies

**NOT Designed to Defend Against**:
- Sophisticated adversarial attacks on the system
- Motivated researchers attempting to fabricate results
- Nation-state level computational security threats

### Security Features

**Content Integrity**:
- SHA-256 hashing for modification detection
- Cryptographic dependency chains
- Tamper-evident artifact storage
- Git-based version control and timestamps

**Academic Integrity**:
- Complete audit trails for all decisions
- Raw data preservation with exact inputs
- Methodology documentation auto-generation
- Independent verification tools provided

## Implementation Details

### Auto-Commit Architecture

**CLI Integration**:
```python
@click.option('--no-auto-commit', is_flag=True, 
              help='Disable automatic Git commit after successful run completion')
def run(experiment_path, ..., no_auto_commit=False):
    result = orchestrator.run_experiment(
        auto_commit=(not no_auto_commit),
        ...
    )
```

**Orchestrator Integration**:
```python
def run_experiment(self, auto_commit: bool = True, ...):
    # ... run experiment ...
    
    # Auto-commit successful run to Git (if enabled)
    if auto_commit:
        commit_metadata = {
            "run_id": run_timestamp,
            "experiment_name": self.experiment_path.name
        }
        commit_success = self._auto_commit_run(run_folder, commit_metadata, audit)
```

**Git Operations**:
```python
def _auto_commit_run(self, run_folder, run_metadata, audit):
    # Add with force to override .gitignore for research preservation
    subprocess.run(["git", "add", "--force", str(run_folder.relative_to(repo_root))])
    
    # Short commit message (under 50 chars per terminal compatibility)
    commit_msg = f"Complete run {run_id}: {experiment_name}"
    subprocess.run(["git", "commit", "-m", commit_msg])
```

### Validation Script Architecture

**Multi-Layer Validation**:
```python
class IntegrityValidator:
    def run_full_validation(self, check_git=False):
        validations = [
            ("Manifest Structure", self.validate_manifest),
            ("Results Files", self.validate_results_files), 
            ("Symlink Integrity", self.validate_symlinks),
            ("Hash Integrity", self.validate_artifact_hashes),
            ("Provenance Chain", self.validate_provenance_chain),
        ]
        
        if check_git:
            validations.append(("Git History", self.validate_git_history))
```

**Hash Verification**:
```python
def validate_artifact_hashes(self):
    for artifact_file in artifacts_dir.rglob("*"):
        expected_hash = self.extract_hash_from_filename(artifact_file.name)
        actual_hash = self.compute_file_hash(artifact_file.resolve())
        
        # Check if 8-char prefix matches full SHA-256
        if not actual_hash.startswith(expected_hash):
            hash_mismatches.append((artifact_file, expected_hash, actual_hash[:8]))
```

## Future Enhancements

### Phase 1: Enhanced Academic Integration
- Citation-ready metadata generation with DOI preparation
- Methodology section auto-generation for academic papers
- Enhanced CLI for analysis portfolio management
- Local analysis registry with search capabilities

### Phase 2: Distributed Provenance
- Persistent URL generation for published analyses
- Cross-institutional verification networks
- Community discovery and similarity detection
- Full DROI (Discernus Research Object Identifier) implementation

### Phase 3: Advanced Validation
- Statistical validation automation
- Cross-platform reproducibility testing
- Blockchain-based immutable provenance (if needed)
- Advanced security features for high-stakes research

## Troubleshooting

### Common Issues

**Auto-Commit Failures**:
```bash
# Check Git configuration
git config --list | grep user

# Verify repository status
git status

# Manual validation
python3 scripts/validate_run_integrity.py [run_path] --check-git
```

**Symlink Issues**:
```bash
# Check symlink targets
find artifacts/ -type l -exec ls -la {} \;

# Verify shared cache integrity
ls -la projects/experiment/shared_cache/artifacts/
```

**Hash Mismatches**:
```bash
# Verify artifact integrity
sha256sum artifacts/analysis_results/*.json

# Check for file corruption
python3 scripts/validate_run_integrity.py [run_path] --verbose
```

### Recovery Procedures

**Lost Git History**:
1. Check if run directory exists: `ls projects/experiment/runs/`
2. Add manually: `git add projects/experiment/runs/[run_id]`
3. Commit: `git commit -m "Recover run [run_id]"`
4. Validate: `python3 scripts/validate_run_integrity.py [run_path] --check-git`

**Broken Symlinks**:
1. Check shared cache: `ls projects/experiment/shared_cache/artifacts/`
2. Verify hash matches: `sha256sum [artifact_file]`
3. Re-run provenance organization if needed
4. Contact support if artifacts are missing

## Conclusion

The Discernus Provenance System provides **world-class research transparency** through a carefully designed architecture that balances:
- **Academic rigor** with **usability**
- **Complete transparency** with **performance**
- **Automatic preservation** with **researcher control**
- **Security** with **practical threat modeling**

This system enables computational social science research that meets the highest standards for peer review, replication, and academic integrity while remaining accessible to researchers at all technical levels.

For questions or support, consult the validation tools, README files, or contact the development team through GitHub issues.