# Git-Based Asset Management and Provenance System

**Document Version**: v1.0.0  
**Created**: 2025-06-25  
**Author**: Claude & Jeff  
**Status**: Planning Phase  

## 🎯 Executive Summary

This document outlines a comprehensive solution for research asset management and experiment provenance in the Discernus system. The approach leverages Git as the underlying versioning infrastructure while providing research-friendly abstractions that minimize cognitive overhead for non-developer users.

**Core Innovation**: Automatic experiment provenance capture with complete reproducibility, using Git for versioning but hiding complexity behind simple research workflows.

## 🚨 Problem Statement

### Current Pain Points

1. **Asset Versioning Chaos**
   - Frameworks, prompt templates, and weighting schemes scattered across multiple directories
   - No clear versioning strategy leads to "framework drift" across projects
   - Researchers copy assets into project directories, creating maintenance hell
   - No way to track "which version of framework X gave us those great results"

2. **Cognitive Overhead**
   - Users must mentally map between experiments/, frameworks/, prompt_templates/, etc.
   - Manual version management requires developer-level discipline
   - Researchers want to focus on research questions, not dependency management

3. **Reproducibility Gaps**
   - Experiments reference assets by name, not specific versions
   - No automatic capture of runtime artifacts (merged prompts, raw LLM responses)
   - Manual reproduction requires detective work to reconstruct exact conditions

4. **Collaboration Friction**
   - "Use framework X with prompt Y" is ambiguous without version specificity
   - No clear handoff process for research projects
   - Asset changes can break existing experiments unexpectedly

## 💡 Proposed Solution

### Core Design Principles

1. **Git-Native Asset Management**: Use Git as the versioning backend for all research assets
2. **Research-Friendly Abstractions**: Hide Git complexity behind simple, intuitive workflows
3. **Automatic Provenance Capture**: System automatically records complete experiment state
4. **Perfect Reproducibility**: Anyone can reconstruct exact experiment conditions
5. **Familiar Tools**: Leverage existing GitHub knowledge instead of inventing new paradigms

### High-Level Architecture

```
research_workspaces/june_2025_research_dev_workspace/
├── .git/                               # Git tracks ALL assets automatically
├── projects/                           # 🎯 Research projects
│   ├── mft_customgpt_training/
│   │   ├── experiment.yaml
│   │   ├── results/                    # Results with full provenance
│   │   └── README.md
│   └── mft_political_analysis/
├── assets/                             # 📦 Git-tracked versioned assets
│   ├── frameworks/
│   │   └── moral_foundations_theory/
│   │       └── framework.yaml          # Git-tracked, auto-versioned
│   ├── prompt_templates/
│   │   └── moral_foundations_analysis/
│   │       └── template.yaml
│   └── weighting_schemes/
│       └── foundation_pairs/
│           └── scheme.yaml
├── corpus/                             # 📚 Corpus files (can also be versioned)
├── scripts/                            # 🛠️ Helper scripts for non-Git experts
│   ├── checkpoint.sh
│   ├── status.sh
│   └── history.sh
└── docs/                               # 📖 Documentation
```

## 🔧 Technical Implementation

### Phase 1: Core Infrastructure

#### Git Provenance Capture System

```python
class GitProvenanceCapture:
    """Capture complete experiment state for perfect reproducibility"""
    
    def capture_experiment_state(self, experiment_file_path: str) -> Dict[str, Any]:
        """Capture complete reproducible state before experiment execution"""
        return {
            "experiment_metadata": {
                "experiment_file": experiment_file_path,
                "run_timestamp": datetime.now().isoformat(),
                "orchestrator_version": "2.1.0"
            },
            "git_state": {
                "commit_hash": self._get_current_commit(),
                "branch": self._get_current_branch(),
                "uncommitted_changes": self._check_workspace_dirty(),
                "tags": self._get_relevant_tags()
            },
            "dependency_snapshots": self._snapshot_all_dependencies(experiment_file_path),
            "environment_info": self._capture_environment()
        }
    
    def _snapshot_all_dependencies(self, experiment_file_path: str) -> Dict[str, Any]:
        """Capture exact content of all assets used by experiment"""
        experiment = self._load_experiment(experiment_file_path)
        snapshots = {}
        
        # Snapshot frameworks
        for framework in experiment.get('components', {}).get('frameworks', []):
            asset_path = self._resolve_framework_path(framework)
            snapshots[f"framework_{framework['id']}"] = {
                "asset_path": asset_path,
                "git_commit": self._get_file_last_commit(asset_path),
                "content_hash": self._hash_file(asset_path),
                "full_content": self._read_file(asset_path)
            }
        
        # Snapshot prompt templates
        for prompt in experiment.get('components', {}).get('prompt_templates', []):
            asset_path = self._resolve_prompt_path(prompt)
            snapshots[f"prompt_{prompt['id']}"] = {
                "asset_path": asset_path,
                "git_commit": self._get_file_last_commit(asset_path),
                "content_hash": self._hash_file(asset_path),
                "full_content": self._read_file(asset_path)
            }
        
        # Snapshot weighting schemes
        for scheme in experiment.get('components', {}).get('weighting_schemes', []):
            asset_path = self._resolve_weighting_path(scheme)
            snapshots[f"weighting_{scheme['id']}"] = {
                "asset_path": asset_path,
                "git_commit": self._get_file_last_commit(asset_path),
                "content_hash": self._hash_file(asset_path),
                "full_content": self._read_file(asset_path)
            }
        
        return snapshots
```

#### Runtime Artifact Capture

```python
class RuntimeProvenanceCapture:
    """Capture runtime artifacts for complete reproducibility"""
    
    def capture_analysis_artifacts(self, analysis_request: Dict, llm_response: Dict) -> Dict[str, Any]:
        """Capture complete analysis pipeline artifacts"""
        return {
            "merged_prompt": {
                "description": "Exact prompt sent to LLM (merged from template + context)",
                "content": analysis_request.get('prompt', ''),
                "template_variables": analysis_request.get('template_variables', {}),
                "context_enrichment": analysis_request.get('context_enrichment', {})
            },
            "llm_interaction": {
                "model": analysis_request.get('model', ''),
                "request_timestamp": analysis_request.get('timestamp', ''),
                "raw_request": analysis_request,
                "raw_response": llm_response,
                "response_timestamp": llm_response.get('timestamp', ''),
                "tokens_used": llm_response.get('usage', {}),
                "api_cost": llm_response.get('cost', 0.0)
            },
            "processing_pipeline": {
                "response_parser": analysis_request.get('parser_version', ''),
                "processed_output": llm_response.get('processed', {}),
                "processing_errors": llm_response.get('processing_errors', []),
                "qa_validation": llm_response.get('qa_assessment', {})
            }
        }
```

### Phase 2: Smart Asset Resolution

#### Experiment Asset References

```yaml
# Simple experiment definition - system resolves to current versions
components:
  frameworks:
    - id: "moral_foundations_theory"          # Uses current git HEAD
    
  prompt_templates:
    - id: "moral_foundations_analysis"        # Uses current git HEAD
    
  weighting_schemes:
    - id: "foundation_pairs"                  # Uses current git HEAD

# Advanced experiment definition - explicit version control
components:
  frameworks:
    - id: "moral_foundations_theory"
      pin_to: "frameworks-mft-v2.1.0"        # Uses specific git tag
      
  prompt_templates:
    - id: "moral_foundations_analysis"
      pin_to: "commit:a1b2c3d4"              # Uses specific commit
      
  weighting_schemes:
    - id: "foundation_pairs"                  # Uses current (mixed approach)
```

#### Asset Resolution Engine

```python
class AssetResolver:
    """Resolve experiment asset references to specific file paths and versions"""
    
    def resolve_asset_reference(self, asset_spec: Dict[str, Any], asset_type: str) -> Dict[str, Any]:
        """Resolve asset reference to actual file path and version info"""
        asset_id = asset_spec['id']
        
        if 'pin_to' in asset_spec:
            # Explicit version pinning
            return self._resolve_pinned_asset(asset_id, asset_spec['pin_to'], asset_type)
        else:
            # Use current version (git HEAD)
            return self._resolve_current_asset(asset_id, asset_type)
    
    def _resolve_pinned_asset(self, asset_id: str, pin_reference: str, asset_type: str) -> Dict[str, Any]:
        """Resolve asset to specific git reference"""
        asset_path = f"assets/{asset_type}s/{asset_id}"
        
        if pin_reference.startswith('commit:'):
            commit_hash = pin_reference.replace('commit:', '')
            return self._get_asset_at_commit(asset_path, commit_hash)
        elif pin_reference.startswith('tag:') or '-' in pin_reference:
            # Tag reference (e.g., "frameworks-mft-v2.1.0")
            tag_name = pin_reference.replace('tag:', '')
            return self._get_asset_at_tag(asset_path, tag_name)
        else:
            raise ValueError(f"Invalid pin reference: {pin_reference}")
    
    def _resolve_current_asset(self, asset_id: str, asset_type: str) -> Dict[str, Any]:
        """Resolve asset to current git HEAD version"""
        asset_path = f"assets/{asset_type}s/{asset_id}"
        return {
            "asset_path": asset_path,
            "resolved_version": "current",
            "git_commit": self._get_file_last_commit(asset_path),
            "content": self._load_asset_content(asset_path)
        }
```

## 👤 User Workflows

### Research-Friendly Workflows (No Git Expertise Required)

#### Basic Research Workflow

```bash
# 1. Researcher makes changes to framework
cd research_workspaces/june_2025_research_dev_workspace/
nano assets/frameworks/moral_foundations_theory/framework.yaml

# 2. Test changes with small experiment
python3 scripts/applications/comprehensive_experiment_orchestrator.py \
  projects/mft_customgpt/experiment.yaml --dry-run

# 3. Save checkpoint when satisfied (simple helper script)
./scripts/checkpoint.sh "Improved authority foundation scoring"
# Internally runs: git add -A && git commit -m "Improved authority foundation scoring"

# 4. Run full experiment
python3 scripts/applications/comprehensive_experiment_orchestrator.py \
  projects/mft_customgpt/experiment.yaml
```

#### Project Status and History

```bash
# Check current status
./scripts/status.sh
# Output:
# Current branch: main
# Uncommitted changes: 2 files modified
# Last checkpoint: "Improved authority foundation scoring" (2 hours ago)
# Recent experiments: MFT_Multi_LLM_Study (1 hour ago)

# View recent checkpoints  
./scripts/history.sh
# Output:
# a1b2c3d4 (2 hours ago) Improved authority foundation scoring
# b2c3d4e5 (1 day ago) Added liberty foundation to MFT framework
# c3d4e5f6 (3 days ago) Fixed prompt template evidence extraction
```

#### Safe Experimentation

```bash
# Try risky framework changes safely
./scripts/create-experiment-branch.sh "try-new-authority-scoring"
# Internally: git checkout -b experiment/try-new-authority-scoring

# Make changes, test
nano assets/frameworks/moral_foundations_theory/framework.yaml
python3 scripts/applications/comprehensive_experiment_orchestrator.py projects/test/experiment.yaml

# If it works, merge back
./scripts/merge-experiment.sh
# Internally: git checkout main && git merge experiment/try-new-authority-scoring

# If it doesn't work, go back to safety
./scripts/abandon-experiment.sh
# Internally: git checkout main && git branch -D experiment/try-new-authority-scoring
```

### Advanced Workflows (For Power Users)

#### Explicit Version Management

```bash
# Tag stable versions for reuse
git tag frameworks-mft-v2.2.0 -m "Stable MFT framework with improved Authority scoring"
git tag prompts-mft-v1.3.0 -m "Enhanced evidence extraction prompts"

# Reference specific versions in experiments
# Edit experiment.yaml to pin to specific tags
```

#### Time Travel for Debugging

```bash
# "That experiment from last Tuesday worked perfectly - how do I get back to that setup?"
git log --oneline --since="last Tuesday" --until="Wednesday"
git checkout <commit-from-tuesday>

# Run experiment with historical setup
python3 scripts/applications/comprehensive_experiment_orchestrator.py projects/mft/experiment.yaml

# Return to current
git checkout main
```

### AI Assistant Integration

Since the user has access to Claude (me), I can provide context-aware git assistance:

**User**: "I want to try a risky change to the framework but be able to get back"  
**Claude**: "Let's create a safety branch first: `git checkout -b backup-current-framework`"

**User**: "How do I get back to the framework from last Tuesday's successful experiment?"  
**Claude**: "Looking at your experiment results... that used commit a1b2c3d4. Run: `git checkout a1b2c3d4`"

## 📋 Implementation Plan

### Phase 1: Core Infrastructure (Week 1-2)
- [ ] **Git Provenance Capture System**
  - Implement `GitProvenanceCapture` class
  - Integrate with existing orchestrator
  - Capture git state, dependency snapshots, runtime artifacts
- [ ] **Asset Resolution Engine**
  - Implement `AssetResolver` class  
  - Support simple references (current versions)
  - Support pinned references (tags, commits)
- [ ] **Enhanced Result Storage**
  - Modify orchestrator to save complete provenance with each experiment
  - Include reproduction instructions in results
  - Test end-to-end provenance capture

### Phase 2: User Experience Improvements (Week 3)
- [ ] **Helper Scripts for Non-Git Users**
  - `checkpoint.sh` - Simple commit wrapper
  - `status.sh` - Human-readable git status
  - `history.sh` - Recent checkpoints view
  - `create-experiment-branch.sh` - Safe experimentation
  - `merge-experiment.sh` - Merge successful experiments
- [ ] **Workspace Reorganization Tools**
  - Script to migrate existing workspaces to new structure
  - Validation tools to check workspace organization
  - Documentation generation tools

### Phase 3: Advanced Features (Week 4)
- [ ] **Automatic Tagging System**
  - Auto-tag successful experiments with meaningful names
  - Suggest tags based on experiment success criteria
  - Integration with QA system for automatic "stable" tagging
- [ ] **Cross-Project Asset Sharing**
  - Tools for sharing assets between research workspaces
  - Asset dependency analysis
  - Bulk asset updates across projects

### Phase 4: Documentation and Training (Week 5)
- [ ] **Comprehensive Documentation**
  - User guide for research workflows
  - Technical documentation for developers
  - Troubleshooting guide
  - Video tutorials for common workflows
- [ ] **Validation and Testing**
  - End-to-end testing with real research projects
  - User acceptance testing with non-technical researchers
  - Performance testing with large asset repositories

## 📊 Success Criteria

### Technical Success Criteria
- [ ] **Perfect Reproducibility**: Any experiment can be exactly reproduced from its provenance record
- [ ] **Zero Manual Version Management**: System handles all versioning automatically
- [ ] **Complete Artifact Capture**: Every LLM interaction and processing step is recorded
- [ ] **Fast Asset Resolution**: Asset loading adds <5 seconds to experiment startup
- [ ] **Workspace Migration**: Existing workspaces can be migrated without data loss

### User Experience Success Criteria
- [ ] **Low Cognitive Overhead**: Researchers need to learn <5 new commands
- [ ] **Familiar Workflows**: Builds on existing file editing and command line usage
- [ ] **Error Recovery**: Users can easily recover from mistakes without losing work
- [ ] **Collaboration Ready**: Projects can be easily shared and understood by new team members
- [ ] **Documentation Quality**: Non-technical users can follow documentation successfully

### Research Impact Success Criteria
- [ ] **Audit Compliance**: Complete audit trail for all research decisions and results
- [ ] **Publication Ready**: Automatic generation of replication packages for papers
- [ ] **Cross-Study Validation**: Easy comparison of asset versions across different studies
- [ ] **Time Savings**: Researchers spend <10% of time on asset management vs research

## 🔍 Risk Assessment

### Technical Risks
- **Git Performance**: Large binary files or extensive history could slow operations
  - *Mitigation*: Use Git LFS for large files, regular repository maintenance
- **Complexity Creep**: System becomes too complex for target users
  - *Mitigation*: Extensive user testing, progressive disclosure of advanced features
- **Integration Overhead**: Significant changes to existing orchestrator
  - *Mitigation*: Phased rollout, backward compatibility during transition

### User Adoption Risks
- **Learning Curve**: Users resist adopting Git-based workflows
  - *Mitigation*: Helper scripts hide Git complexity, AI assistant provides guidance
- **Workflow Disruption**: Changes to existing research practices
  - *Mitigation*: Migration tools, parallel operation during transition
- **Documentation Gaps**: Insufficient training materials
  - *Mitigation*: User-centered documentation, video tutorials, examples

### Operational Risks
- **Repository Size**: Research assets could create very large Git repositories
  - *Mitigation*: Repository organization best practices, periodic cleanup tools
- **Backup and Recovery**: Git-based system needs robust backup strategy
  - *Mitigation*: Regular backups, GitHub integration for off-site storage
- **Merge Conflicts**: Multiple researchers editing same assets
  - *Mitigation*: Asset organization to minimize conflicts, conflict resolution tools

## 📈 Future Enhancements

### Advanced Provenance Features
- **Experiment Genealogy**: Visual representation of how experiments relate to each other
- **Asset Impact Analysis**: See which experiments are affected by asset changes
- **Automated Replication**: One-click reproduction of any historical experiment
- **Cross-Workspace Asset Sharing**: Formal system for sharing assets between research groups

### Research Workflow Integration
- **Paper Integration**: Direct export to academic paper formats with embedded provenance
- **Collaboration Tools**: Better support for multi-researcher projects
- **Experiment Planning**: Tools to plan experiment series with asset evolution
- **Quality Assurance Integration**: Automatic asset validation and testing

### Advanced Git Integration
- **Semantic Versioning**: Automatic version numbering based on asset changes
- **Change Impact Analysis**: Predict which experiments might be affected by asset changes
- **Automated Testing**: Run test experiments when assets change
- **Release Management**: Formal release process for stable asset versions

## 📚 Documentation Plan

### User Documentation
1. **Quick Start Guide**: Get new users productive in 15 minutes
2. **Research Workflow Guide**: Common patterns and best practices
3. **Troubleshooting Guide**: Solutions to common problems
4. **Advanced Features**: Power user features and workflows

### Technical Documentation
1. **Architecture Overview**: System design and integration points
2. **API Documentation**: Developer interfaces and extension points
3. **Database Schema**: Provenance data structures
4. **Deployment Guide**: Setting up new research workspaces

### Training Materials
1. **Video Tutorials**: Visual walk-throughs of common workflows
2. **Example Projects**: Complete example research projects with full provenance
3. **Best Practices**: Lessons learned and recommended approaches
4. **FAQ**: Answers to frequently asked questions

## 🎯 Conclusion

This Git-based asset management and provenance system addresses the core challenges of research reproducibility and asset management while maintaining a research-friendly user experience. By leveraging Git as the underlying infrastructure but hiding complexity behind intuitive abstractions, we can provide the benefits of rigorous version control without requiring researchers to become Git experts.

The phased implementation approach allows for iterative development and user feedback, while the comprehensive success criteria ensure the system meets both technical and user experience requirements.

The system's design aligns with the broader Discernus goal of making rigorous computational social science accessible to researchers, providing the infrastructure needed for reproducible, auditable research while maintaining focus on research questions rather than technical implementation details. 