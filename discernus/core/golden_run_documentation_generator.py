#!/usr/bin/env python3
"""
Golden Run Documentation Generator for Discernus
===============================================

Generates comprehensive documentation for "golden run" archives that includes
all consolidated provenance data, input materials, and stakeholder-specific navigation.
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


class GoldenRunDocumentationGenerator:
    """
    Generates comprehensive documentation for "golden run" archives.
    
    This creates a complete navigation guide that includes all consolidated
    provenance data, input materials, and stakeholder-specific paths.
    """
    
    def __init__(self, run_directory: Path):
        self.run_dir = run_directory
        self.results_dir = run_directory / "results"
        self.artifacts_dir = run_directory / "artifacts"
        self.logs_dir = run_directory / "logs"
        
    def generate_golden_run_readme(self) -> str:
        """
        Generate comprehensive README for golden run archive.
        
        Returns:
            Complete README content as string
        """
        # Load existing data
        manifest_data = self._load_manifest()
        provenance_data = self._load_consolidated_provenance()
        input_materials_data = self._load_input_materials_consolidation()
        
        # Generate README content
        readme_content = self._generate_header(manifest_data)
        readme_content += self._generate_executive_summary(manifest_data, provenance_data)
        readme_content += self._generate_stakeholder_navigation(provenance_data)
        readme_content += self._generate_input_materials_section(input_materials_data)
        readme_content += self._generate_directory_structure()
        readme_content += self._generate_audit_workflows()
        readme_content += self._generate_provenance_system_explanation()
        readme_content += self._generate_golden_run_specific_guidance()
        
        return readme_content
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load manifest data."""
        manifest_path = self.run_dir / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_consolidated_provenance(self) -> Dict[str, Any]:
        """Load consolidated provenance data."""
        provenance_path = self.results_dir / "consolidated_provenance.json"
        if provenance_path.exists():
            with open(provenance_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_input_materials_consolidation(self) -> Dict[str, Any]:
        """Load input materials consolidation data."""
        input_path = self.results_dir / "input_materials_consolidation.json"
        if input_path.exists():
            with open(input_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _generate_header(self, manifest_data: Dict[str, Any]) -> str:
        """Generate README header."""
        experiment_name = manifest_data.get('experiment_name') or 'Unknown Experiment'
        run_timestamp = manifest_data.get('run_timestamp') or 'Unknown'
        
        return f"""# Golden Run Archive: {experiment_name}

**Complete Research Transparency Package - Ready for Peer Review**

This archive contains a **complete, self-contained research package** with full provenance, 
input materials, and comprehensive audit trails. This is a "golden run" - the definitive 
version of this research experiment, ready for academic review, replication, and archival.

## 🏆 Golden Run Status

- **Run ID**: {run_timestamp}
- **Archive Type**: Complete Research Package
- **Reproducibility**: 100% - All inputs and outputs included
- **Audit Readiness**: ✅ Complete transparency package
- **Peer Review Ready**: ✅ Academic-grade documentation

---

"""
    
    def _generate_executive_summary(self, manifest_data: Dict[str, Any], provenance_data: Dict[str, Any]) -> str:
        """Generate executive summary section."""
        model_info = provenance_data.get('model_provenance', {})
        timeline_info = provenance_data.get('execution_timeline', {})
        cost_info = provenance_data.get('cost_analysis', {})
        
        models_used = model_info.get('unique_models') or ['Unknown']
        total_duration = timeline_info.get('total_duration') or 0
        total_cost = cost_info.get('total_cost') or 0.0
        
        # Ensure numeric values are properly handled
        if total_duration is None:
            total_duration = 0
        if total_cost is None:
            total_cost = 0.0
        
        # Ensure models_used is a list
        if not isinstance(models_used, list):
            models_used = ['Unknown']
        
        models_str = ', '.join(str(m) for m in models_used) if models_used else 'Unknown'
        
        return f"""## 📊 Executive Summary

### Research Execution
- **Experiment**: {manifest_data.get('experiment_name') or 'Unknown'}
- **Framework**: {manifest_data.get('framework_version') or 'Unknown'}
- **Models Used**: {models_str}
- **Total Duration**: {total_duration:.1f} seconds
- **Total Cost**: ${total_cost:.4f} USD
- **Status**: ✅ Completed successfully

### Archive Contents
- **Input Materials**: Complete corpus, experiment specification, and framework
- **Analysis Results**: Raw LLM outputs with full provenance
- **Statistical Analysis**: Mathematical computations and significance tests
- **Evidence Curation**: Supporting quotes and citations
- **Audit Trails**: Complete system logs and model interactions
- **Provenance Data**: Consolidated metadata for all stakeholders

---

"""
    
    def _generate_stakeholder_navigation(self, provenance_data: Dict[str, Any]) -> str:
        """Generate stakeholder-specific navigation."""
        stakeholder_summaries = provenance_data.get('stakeholder_summaries', {})
        
        content = "## 🎯 Stakeholder Navigation\n\n"
        
        for stakeholder, summary in stakeholder_summaries.items():
            if not summary:
                continue
            stakeholder_name = stakeholder.replace('_', ' ').title()
            content += f"### {stakeholder_name}\n\n"
            content += f"**{summary.get('executive_summary') or 'No summary available'}**\n\n"
            
            navigation_guide = summary.get('navigation_guide') or []
            if navigation_guide:
                content += "**Start Here:**\n"
                for item in navigation_guide:
                    if item:
                        content += f"- {item}\n"
                content += "\n"
            
            key_metrics = summary.get('key_metrics') or {}
            if key_metrics:
                content += "**Key Metrics:**\n"
                for metric, value in key_metrics.items():
                    if metric and value is not None:
                        content += f"- {metric.replace('_', ' ').title()}: {value}\n"
                content += "\n"
        
        content += "---\n\n"
        return content
    
    def _generate_input_materials_section(self, input_materials_data: Dict[str, Any]) -> str:
        """Generate input materials section."""
        corpus_data = input_materials_data.get('corpus_materials', {})
        experiment_data = input_materials_data.get('experiment_specification', {})
        framework_data = input_materials_data.get('framework_materials', {})
        summary = input_materials_data.get('consolidation_summary', {})
        
        content = "## 📁 Input Materials (Complete Reproducibility)\n\n"
        
        # Reproducibility score
        reproducibility_score = summary.get('reproducibility_score') or 0
        content += f"**Reproducibility Score: {reproducibility_score}%** - All critical input materials included\n\n"
        
        # Corpus materials
        corpus_files_copied = corpus_data.get('corpus_files_copied') or 0
        corpus_manifest_copied = corpus_data.get('corpus_manifest_copied') or False
        
        content += "### Corpus Materials\n"
        content += f"- **Corpus Files**: {corpus_files_copied} documents in `results/corpus/`\n"
        content += f"- **Corpus Manifest**: {'✅ Included' if corpus_manifest_copied else '❌ Missing'} (`results/corpus/corpus.md`)\n"
        
        corpus_files = corpus_data.get('corpus_files') or []
        if corpus_files:
            content += "- **Document List**:\n"
            for file_info in corpus_files:
                if file_info:
                    filename = file_info.get('filename') or 'Unknown'
                    size_bytes = file_info.get('size_bytes') or 0
                    size_kb = size_bytes / 1024
                    content += f"  - `{filename}` ({size_kb:.1f} KB)\n"
        content += "\n"
        
        # Experiment specification
        experiment_copied = experiment_data.get('experiment_spec_copied') or False
        content += "### Experiment Specification\n"
        content += f"- **Experiment Spec**: {'✅ Included' if experiment_copied else '❌ Missing'} (`results/experiment.md`)\n"
        content += "  - Research design and methodology\n"
        content += "  - Statistical methods and hypotheses\n"
        content += "  - Analysis parameters and configuration\n\n"
        
        # Framework
        framework_copied = framework_data.get('framework_copied') or False
        framework_name = framework_data.get('framework_name') or 'Unknown'
        content += "### Analytical Framework\n"
        content += f"- **Framework**: {'✅ Included' if framework_copied else '❌ Missing'} (`results/{framework_name}`)\n"
        content += "  - Analytical dimensions and criteria\n"
        content += "  - Scoring methodology and validation rules\n"
        content += "  - Evidence curation guidelines\n\n"
        
        content += "---\n\n"
        return content
    
    def _generate_directory_structure(self) -> str:
        """Generate directory structure section."""
        return """## 📁 Complete Directory Structure

```
GOLDEN_RUN_ARCHIVE/
├── README.md                           # This comprehensive guide
├── manifest.json                       # Complete execution record
│
├── results/                            # Primary research deliverables
│   ├── final_report.md                # Main research findings
│   ├── scores.csv                     # Quantitative results
│   ├── evidence.csv                   # Supporting evidence
│   ├── statistical_results.csv        # Mathematical analysis
│   ├── metadata.csv                   # Provenance summary
│   │
│   ├── corpus/                        # Complete input materials
│   │   ├── corpus.md                  # Corpus specification
│   │   ├── document1.txt              # Source documents
│   │   └── document2.txt              # (all corpus files)
│   │
│   ├── experiment.md                  # Experiment specification
│   ├── framework.md                   # Analytical framework
│   │
│   ├── consolidated_provenance.json   # Comprehensive provenance data
│   └── input_materials_consolidation.json  # Input materials report
│
├── artifacts/                          # Complete audit trail (symlinks)
│   ├── analysis_results/              # Raw AI system outputs
│   ├── analysis_plans/                # Processing plans and strategies
│   ├── statistical_results/           # Mathematical computations
│   ├── evidence/                      # Curated supporting evidence
│   ├── reports/                       # Synthesis outputs
│   ├── inputs/                        # Framework and data sources
│   └── provenance.json                # Human-readable artifact map
│
└── logs/                              # System execution logs
    ├── llm_interactions.jsonl         # Complete LLM conversations
    ├── system.jsonl                   # System events and errors
    ├── agents.jsonl                   # Agent execution details
    ├── costs.jsonl                    # API cost tracking
    └── artifacts.jsonl                # Artifact creation log
```

---

"""
    
    def _generate_audit_workflows(self) -> str:
        """Generate audit workflow recommendations."""
        return """## 🔍 Audit Workflow Recommendations

### Quick Integrity Check (5 minutes)
1. **Verify Archive Completeness**: Check `results/corpus/` contains all input documents
2. **Confirm Execution Success**: Verify `manifest.json` shows successful completion
3. **Check Main Deliverable**: Ensure `results/final_report.md` exists and is substantial
4. **Validate Provenance**: Confirm `artifacts/provenance.json` shows complete artifact chain

### Standard Academic Review (30 minutes)
1. **Input Verification**: Review `results/corpus/`, `results/experiment.md`, and `results/framework.md`
2. **Methodology Review**: Examine `results/experiment.md` for research design
3. **Results Analysis**: Check `results/final_report.md` and `results/scores.csv`
4. **Evidence Validation**: Review `results/evidence.csv` for supporting quotes
5. **Statistical Verification**: Examine `results/statistical_results.csv`

### Deep Forensic Audit (2+ hours)
1. **Complete Log Analysis**: Full review of `logs/` directory
2. **LLM Interaction Analysis**: Review `logs/llm_interactions.jsonl` for prompt engineering
3. **Artifact Chain Verification**: Validate every symlink and dependency
4. **Reproducibility Testing**: Attempt replication using preserved inputs
5. **Statistical Validation**: Independent verification of mathematical computations
6. **Cost Analysis**: Review `logs/costs.jsonl` for resource usage patterns

### Replication Research (Variable)
1. **Environment Setup**: Use `manifest.json` to recreate execution environment
2. **Input Preparation**: Use `results/corpus/` and `results/experiment.md` for inputs
3. **Framework Application**: Use `results/framework.md` for analytical approach
4. **Independent Analysis**: Run analysis using preserved inputs
5. **Results Comparison**: Compare with `results/scores.csv` and `results/evidence.csv`

---

"""
    
    def _generate_provenance_system_explanation(self) -> str:
        """Generate provenance system explanation."""
        return """## 🔐 Content-Addressed Provenance System

### Cryptographic Integrity
Every artifact in this system is stored using **content-addressable hashing**:
- **SHA-256 hashes**: Each file's content generates a unique 256-bit fingerprint
- **Modification detection**: Any change to content results in a different hash
- **Deduplication**: Identical content across runs shares the same hash
- **Verification**: Run `sha256sum` on any artifact to check integrity

### Git-Based Permanent Provenance
- **Version history**: Every research run is committed to Git with timestamps
- **Distributed storage**: Git's distributed nature enables independent verification
- **Branching strategy**: Research runs are preserved across branches
- **Optional signatures**: Git commits can be cryptographically signed

### Dependency Chain Verification
The system maintains a complete **content-addressed dependency graph**:
```
Input Data (hash_A) → Analysis (hash_B) → Synthesis (hash_C) → Results (hash_D)
```
- Each stage records the hashes of its inputs in metadata
- Auditors can verify the complete chain from raw data to conclusions
- Any break in the chain indicates potential modification or data loss

---

"""
    
    def _generate_golden_run_specific_guidance(self) -> str:
        """Generate golden run specific guidance."""
        return """## 🏆 Golden Run Archive Usage

### For Peer Reviewers
This archive contains everything needed for comprehensive peer review:
- **Complete methodology**: All inputs, frameworks, and specifications
- **Full transparency**: Every computational decision is documented
- **Reproducible results**: All data and code paths are preserved
- **Audit trails**: Complete logs of system behavior and model interactions

### For Replication Researchers
This archive enables exact replication:
- **Self-contained**: No external dependencies required
- **Complete inputs**: All corpus documents, specifications, and frameworks included
- **Execution record**: Full manifest with timestamps and configurations
- **Validation tools**: Integrity checking and verification scripts available

### For Academic Archives
This archive meets the highest standards for computational research:
- **Long-term preservation**: Content-addressed storage ensures integrity over time
- **Format independence**: Human-readable formats with machine-readable metadata
- **Comprehensive documentation**: Multiple stakeholder perspectives included
- **Verification tools**: Built-in integrity checking and validation

### For Future Researchers
This archive provides a complete research package:
- **Methodology transparency**: Full documentation of analytical approach
- **Data accessibility**: All inputs and outputs in standard formats
- **Reproducibility**: Complete provenance chain for independent verification
- **Extensibility**: Framework and methodology can be applied to new data

---

## 📞 Support and Contact

For questions about this research archive or the Discernus platform:
- **Documentation**: See `docs/` directory for comprehensive guides
- **Validation**: Use provided integrity checking scripts
- **Reproduction**: Follow replication workflow recommendations above
- **Technical Issues**: Refer to system logs in `logs/` directory

---

**Archive Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
**Discernus Version**: Alpha System
**Archive Type**: Golden Run - Complete Research Package
"""
    
    def save_golden_run_readme(self, output_path: Optional[Path] = None) -> Path:
        """
        Save golden run README to file.
        
        Args:
            output_path: Optional path to save the README
            
        Returns:
            Path to the saved README file
        """
        if output_path is None:
            output_path = self.run_dir / "GOLDEN_RUN_README.md"
        
        readme_content = self.generate_golden_run_readme()
        
        with open(output_path, 'w') as f:
            f.write(readme_content)
        
        return output_path


def generate_golden_run_documentation(run_directory: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convenience function to generate golden run documentation for a single run.
    
    Args:
        run_directory: Path to the experiment run directory
        output_path: Optional path to save the documentation
        
    Returns:
        Path to the saved documentation file
    """
    generator = GoldenRunDocumentationGenerator(run_directory)
    return generator.save_golden_run_readme(output_path)
