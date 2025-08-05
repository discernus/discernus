# Research Run: presidential_populism_emergence_study_enhanced

**Welcome to the complete audit trail for this computational research run.**

This directory contains a fully transparent, integrity-checked record of a computational research experiment. Every artifact is content-addressable, enabling detection of modifications, and preserved in Git for academic provenance.

## Executive Summary

- **Run ID**: 20250805T203602Z
- **Experiment**: presidential_populism_emergence_study_enhanced
- **Framework**: ../../frameworks/reference/flagship/pdaf_v7.3.md
- **Model**: vertex_ai/gemini-2.5-flash-lite
- **Total Cost**: $0.0000 USD
- **Duration**: 0.0 seconds
- **Status**: ✅ Completed successfully

## 🎯 Start Here: Key Deliverables

### Primary Research Output
- **`results/final_report.md`** - Complete research findings (218KB, 73 lines)
  - Executive summary of experimental results
  - Statistical findings with confidence intervals
  - Academic-grade methodology documentation

### Data for External Verification
- **`results/scores.csv`** - Raw quantitative measurements
- **`results/evidence.csv`** - Supporting textual evidence
- **`results/statistical_results.csv`** - Mathematical computations
- **`results/metadata.csv`** - Complete provenance metadata

## 🔍 For Auditors: Complete Transparency

### Audit Trail Navigation
1. **Start with**: `manifest.json` - Complete execution record with timestamps
2. **Verify inputs**: `artifacts/inputs/` - Framework and corpus used
3. **Check analysis**: `artifacts/analysis_results/` - Raw LLM outputs that drove conclusions
4. **Examine synthesis**: `artifacts/statistical_results/` - Mathematical computations
5. **Review evidence**: `artifacts/evidence/` - How conclusions were supported
6. **Cross-reference**: `artifacts/provenance.json` - Human-readable artifact map

### Key Audit Questions Answered
- **"What data was processed?"** → `artifacts/inputs/` + `artifacts/analysis_results/`
- **"How were conclusions reached?"** → `artifacts/statistical_results/` + `artifacts/analysis_plans/`
- **"What evidence supports findings?"** → `artifacts/evidence/` + `results/evidence.csv`
- **"Can I reproduce this experiment?"** → `manifest.json` + all symlinked artifacts
- **"What did the AI system actually output?"** → `logs/llm_interactions.jsonl`
- **"Were there any errors or failures?"** → `logs/system.jsonl` + `logs/agents.jsonl`

### Provenance Chain Verification
All artifacts are cryptographically hashed and linked. The complete dependency chain is preserved in `artifacts/provenance.json` with full traceability from inputs to final outputs.

## 📁 Directory Structure (Actual)

```
20250805T203602Z/
├── README.md                    # This guide (you are here)
├── manifest.json                # Complete execution record
│
├── results/                     # Final outputs for researchers
│   ├── final_report.md         # Main research deliverable
│   ├── scores.csv              # Quantitative results
│   ├── evidence.csv            # Supporting evidence
│   ├── statistical_results.csv # Mathematical analysis
│   └── metadata.csv            # Provenance summary
│
├── artifacts/                   # Complete audit trail (symlinks to shared cache)
│   ├── analysis_results/       # Raw AI system outputs
│   ├── analysis_plans/         # Processing plans and strategies
│   ├── statistical_results/    # Mathematical computations
│   ├── evidence/               # Curated supporting evidence
│   ├── reports/                # Synthesis outputs
│   ├── inputs/                 # Framework and data sources used
│   └── provenance.json         # Human-readable artifact map
│
├── logs/                        # System execution logs
│   ├── llm_interactions.jsonl  # Complete LLM conversations
│   ├── system.jsonl            # System events and errors
│   ├── agents.jsonl            # Agent execution details
│   ├── costs.jsonl             # API cost tracking
│   └── artifacts.jsonl         # Artifact creation log
│
└── data/                        # Legacy CSV location (deprecated)
```

## 🚦 Audit Workflow Recommendations

### Quick Integrity Check (5 minutes)
1. Verify `manifest.json` shows successful completion
2. Check `results/final_report.md` exists and is substantial
3. Confirm `artifacts/provenance.json` shows complete artifact chain
4. Spot-check one artifact symlink resolves correctly

### Standard Audit (30 minutes)
1. **Inputs Verification**: Review `artifacts/inputs/` for frameworks and data sources
2. **Analysis Verification**: Examine `artifacts/analysis_results/` for AI system outputs
3. **Computation Verification**: Check `artifacts/statistical_results/` for mathematical work
4. **Evidence Verification**: Review `artifacts/evidence/` for supporting evidence
5. **Cost Verification**: Check `logs/costs.jsonl` for reasonable resource usage

### Deep Forensic Audit (2+ hours)
1. **Complete Log Analysis**: Full review of `logs/` directory
2. **Artifact Chain Verification**: Validate every symlink and dependency
3. **LLM Interaction Analysis**: Review `logs/llm_interactions.jsonl` for prompt engineering
4. **Reproducibility Testing**: Attempt replication using preserved inputs
5. **Statistical Validation**: Independent verification of mathematical computations

## 🔐 Content-Addressed Provenance System

### Content-Addressable Storage
Every artifact in this system is stored using **content-addressable hashing**:
- **SHA-256 hashes**: Each file's content generates a unique 256-bit fingerprint
- **Modification detection**: Any change to content results in a different hash
- **Deduplication**: Identical content across runs shares the same hash, ensuring efficiency
- **Verification**: Run `sha256sum` on any artifact to check if content matches expected hash

### Hash-Based Artifact Identification
```bash
# Example: Verify an artifact matches its expected hash
sha256sum artifacts/analysis_results/analysis_response_185f5e58.json
# Should start with: 185f5e58... (first 8 characters of SHA-256)
```

### Git-Based Permanent Provenance
- **Version history**: Every research run is committed to Git with timestamps
- **Distributed storage**: Git's distributed nature enables independent verification
- **Branching strategy**: Research runs are preserved across branches for long-term access
- **Optional signatures**: Git commits can be cryptographically signed for additional verification

### Symlink Architecture for Efficiency
- **Shared cache**: Common artifacts (frameworks, models) stored once, linked many times
- **Performance**: No duplication of large files across multiple runs
- **Integrity**: Symlinks point to content-addressed files, maintaining hash verification
- **Transparency**: All links are relative and auditable

### Dependency Chain Verification
The system maintains a complete **content-addressed dependency graph**:
```
Input Data (hash_A) → Analysis (hash_B) → Synthesis (hash_C) → Results (hash_D)
```
- Each stage records the hashes of its inputs in metadata
- Auditors can verify the complete chain from raw data to conclusions
- Any break in the chain indicates potential modification or data loss

### Academic Integrity Features
This content-addressed system provides **strong evidence** of:
1. **Data consistency**: Content matches expected hashes when unmodified
2. **Provenance completeness**: All inputs to conclusions are preserved and linked
3. **Temporal ordering**: Git timestamps document sequence of operations
4. **Reproducibility**: Exact inputs preserved for independent replication

### Automated Integrity Validation
**Recommended**: Use the provided validation script for comprehensive verification:
```bash
# Quick integrity check (recommended for all audits)
python3 scripts/validate_run_integrity.py 20250805T203602Z

# Verbose output showing all validation steps
python3 scripts/validate_run_integrity.py 20250805T203602Z --verbose

# Include Git history validation
python3 scripts/validate_run_integrity.py 20250805T203602Z --check-git
```

### Manual Verification Commands
```bash
# Verify artifact integrity manually
sha256sum artifacts/statistical_results/*.json

# Check Git history for this run
git log --oneline --grep="20250805T203602Z"

# Validate symlink targets exist and match hashes
find artifacts/ -type l -exec ls -la {} \;

# Verify dependency chain in artifact metadata
grep -r "dependencies" artifacts/*/
```

## 🤝 Auditor Support

### Common Questions
- **"Is this data fabricated?"** → All artifacts are content-addressed and linked to source
- **"Can I trust the AI system outputs?"** → Raw AI responses preserved in `artifacts/analysis_results/`
- **"How do I verify the computations?"** → Mathematical work in `artifacts/statistical_results/` with source data
- **"What if I find issues?"** → Complete provenance chain enables precise issue identification

### Technical Support
- **Automated Validation**: Run `python3 scripts/validate_run_integrity.py [run_path]` for comprehensive checks
- **Symlink Issues**: All artifacts are symlinked to `../../shared_cache/artifacts/[hash]`
- **Hash Verification**: Use `sha256sum` on any artifact to check content consistency
- **Reproduction**: Use `manifest.json` to recreate exact experimental conditions

### Academic Standards Compliance
- ✅ **Complete Transparency**: Every computation and decision preserved
- ✅ **Reproducibility**: All inputs and parameters documented
- ✅ **Traceability**: Complete audit trail from raw data to conclusions
- ✅ **Integrity**: Content-addressed hashing enables modification detection
- ✅ **Accessibility**: Human-readable organization with clear navigation

## 📞 Contact Information

For questions about this research run or audit procedures:
- **System**: Discernus v2.0 (THIN Architecture)
- **Provenance Organizer**: v1.0
- **Run Generated**: 20250805T203602Z
- **Audit Trail**: Complete and verified

---

**This README serves as your entry point to a fully transparent, auditable research process. Every claim is backed by preserved evidence, every computation is documented, and every decision is traceable. Welcome to academic-grade computational research transparency.**
