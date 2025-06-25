# Experiment Results Merge System Design

**Document Version**: v1.0.0  
**Created**: 2025-06-25  
**Author**: Claude & Jeff  
**Status**: Design Phase  
**Priority**: High (needed for phased experiment approaches)

## 🎯 Purpose

The Experiment Results Merge System enables researchers to combine results from multiple separate experiments into unified datasets for comprehensive analysis. This addresses the common research pattern of running experiments in phases (e.g., testing with 2 LLMs first, then adding 2 more) while maintaining complete analytical capabilities.

## 🚨 Problem Statement

### Current Limitation
- Each experiment run creates a separate, isolated result set
- No way to combine results from related experiments (e.g., Phase 1: Claude+GPT-4o, Phase 2: Gemini+Mistral)
- Researchers cannot incrementally build comprehensive datasets
- Cross-experiment analysis requires manual data manipulation

### Use Cases
1. **Phased Budget Management**: Test with expensive models first, add cheaper models later
2. **Iterative Research**: Refine corpus/framework between experiment phases
3. **Collaborative Research**: Combine experiments run by different team members
4. **Cost Optimization**: Add models/analyses incrementally based on intermediate results
5. **Failure Recovery**: Re-run failed portions without losing successful analyses

## 💡 Proposed Solution

### Core Architecture

```
ExperimentMergeSystem
├── ExperimentResultsLoader     # Load results from multiple experiments
├── DataDeduplicator           # Handle duplicate analyses intelligently
├── MetadataReconciler         # Resolve conflicts in experiment metadata
├── QualityValidator           # Re-run QA validation on merged dataset
├── UnifiedReportGenerator     # Generate reports on combined data
└── ProvenanceTracker          # Maintain audit trail of merge operations
```

## 🔧 Technical Design

### 1. ExperimentResultsLoader

```python
class ExperimentResultsLoader:
    """Load and normalize results from multiple experiments"""
    
    def load_experiments(self, experiment_identifiers: List[str]) -> List[ExperimentDataset]:
        """
        Load multiple experiments by various identifier types:
        - Database experiment IDs
        - Result directory paths  
        - Experiment names with date ranges
        """
        experiments = []
        
        for identifier in experiment_identifiers:
            if identifier.isdigit():
                # Database experiment ID
                exp_data = self._load_from_database(int(identifier))
            elif Path(identifier).exists():
                # Result directory path
                exp_data = self._load_from_directory(identifier)
            else:
                # Experiment name search
                exp_data = self._load_by_name_search(identifier)
            
            if exp_data:
                experiments.append(exp_data)
        
        return experiments
    
    def _normalize_experiment_format(self, raw_data: Dict) -> ExperimentDataset:
        """Normalize different experiment result formats to common schema"""
        return ExperimentDataset(
            experiment_id=raw_data.get('experiment_id'),
            name=raw_data.get('name'),
            runs=self._normalize_runs(raw_data.get('results', [])),
            metadata=self._extract_metadata(raw_data),
            provenance=self._extract_provenance(raw_data)
        )

@dataclass
class ExperimentDataset:
    experiment_id: str
    name: str
    runs: List[AnalysisRun]
    metadata: ExperimentMetadata
    provenance: ProvenanceInfo
    
@dataclass 
class AnalysisRun:
    run_id: str
    text_id: str
    model: str
    framework: str
    raw_scores: Dict[str, float]
    qa_assessment: Dict[str, Any]
    success: bool
    api_cost: float
    timestamp: str
    # Merge-specific fields
    source_experiment_id: str
    deduplication_key: str  # For identifying duplicates
```

### 2. DataDeduplicator

```python
class DataDeduplicator:
    """Handle duplicate analyses intelligently during merge"""
    
    def deduplicate_runs(self, all_runs: List[AnalysisRun], 
                        strategy: str = "keep_latest") -> Tuple[List[AnalysisRun], List[DuplicationReport]]:
        """
        Deduplicate runs using configurable strategies
        
        Strategies:
        - keep_latest: Keep most recent analysis of same text+model+framework
        - keep_highest_quality: Keep analysis with highest QA confidence
        - keep_all: Keep all, mark as duplicates but preserve for analysis
        - merge_scores: Average scores from duplicate analyses
        """
        
        duplicates_found = []
        deduplicated_runs = []
        
        # Group by deduplication key (text_id + model + framework)
        grouped_runs = self._group_by_deduplication_key(all_runs)
        
        for dedup_key, runs in grouped_runs.items():
            if len(runs) == 1:
                deduplicated_runs.extend(runs)
            else:
                # Handle duplicates according to strategy
                kept_runs, duplicate_report = self._apply_deduplication_strategy(
                    runs, strategy
                )
                deduplicated_runs.extend(kept_runs)
                duplicates_found.append(duplicate_report)
        
        return deduplicated_runs, duplicates_found
    
    def _generate_deduplication_key(self, run: AnalysisRun) -> str:
        """Generate key for identifying duplicate analyses"""
        return f"{run.text_id}|{run.model}|{run.framework}"
```

### 3. MetadataReconciler

```python
class MetadataReconciler:
    """Reconcile conflicting metadata from multiple experiments"""
    
    def reconcile_metadata(self, experiments: List[ExperimentDataset]) -> MergedMetadata:
        """
        Reconcile metadata conflicts intelligently
        
        Resolution strategies:
        - Framework versions: Require exact match or explicit mapping
        - Prompt templates: Allow evolution, track changes
        - Cost limits: Use maximum across experiments
        - Quality thresholds: Use strictest thresholds
        """
        
        reconciled = MergedMetadata()
        conflicts = []
        
        # Check framework compatibility
        frameworks = {exp.metadata.framework_version for exp in experiments}
        if len(frameworks) > 1:
            conflicts.append(FrameworkVersionConflict(frameworks))
        
        # Merge cost information
        reconciled.total_cost = sum(exp.metadata.total_cost for exp in experiments)
        reconciled.cost_breakdown = self._merge_cost_breakdowns(experiments)
        
        # Combine model coverage
        reconciled.models_used = list(set(
            model for exp in experiments for model in exp.metadata.models_used
        ))
        
        # Track experiment sources
        reconciled.source_experiments = [
            {
                'experiment_id': exp.experiment_id,
                'name': exp.name,
                'run_count': len(exp.runs),
                'contribution': len(exp.runs) / sum(len(e.runs) for e in experiments)
            }
            for exp in experiments
        ]
        
        return reconciled, conflicts

@dataclass
class MergedMetadata:
    source_experiments: List[Dict]
    total_analyses: int
    successful_analyses: int
    total_cost: float
    cost_breakdown: Dict[str, float]
    models_used: List[str]
    frameworks_used: List[str]
    date_range: Tuple[str, str]
    merge_timestamp: str
    merge_strategy: str
    conflicts_resolved: List[str]
```

### 4. QualityValidator

```python
class MergedExperimentQualityValidator:
    """Re-run QA validation on merged dataset"""
    
    def validate_merged_experiment(self, merged_runs: List[AnalysisRun], 
                                  original_qa_system: Any) -> MergedQualityReport:
        """
        Run comprehensive QA validation on merged dataset
        
        Validations:
        - Cross-experiment consistency checks
        - Model performance comparison across source experiments
        - Framework application consistency
        - Statistical validity of merged dataset
        """
        
        report = MergedQualityReport()
        
        # Cross-model consistency analysis
        report.cross_model_consistency = self._analyze_cross_model_consistency(merged_runs)
        
        # Framework application consistency
        report.framework_consistency = self._validate_framework_consistency(merged_runs)
        
        # Statistical validity
        report.statistical_validity = self._assess_statistical_validity(merged_runs)
        
        # Re-run individual QA assessments if needed
        report.qa_reassessments = self._rerun_qa_assessments(
            merged_runs, original_qa_system
        )
        
        return report

@dataclass
class MergedQualityReport:
    overall_quality_score: float
    cross_model_consistency: Dict[str, float]
    framework_consistency: Dict[str, Any]
    statistical_validity: Dict[str, Any]
    qa_reassessments: List[Dict]
    warnings: List[str]
    recommendations: List[str]
```

### 5. UnifiedReportGenerator

```python
class UnifiedReportGenerator:
    """Generate comprehensive reports on merged experiment data"""
    
    def generate_merged_report(self, merged_data: MergedExperimentResult) -> Path:
        """
        Generate unified HTML report showing:
        - Combined analysis results
        - Cross-experiment comparisons
        - Model performance across experiments
        - Merge operation audit trail
        """
        
        report_sections = {
            'executive_summary': self._generate_executive_summary(merged_data),
            'source_experiments': self._summarize_source_experiments(merged_data),
            'combined_analysis': self._generate_combined_analysis(merged_data),
            'cross_experiment_comparison': self._compare_across_experiments(merged_data),
            'model_performance': self._analyze_model_performance(merged_data),
            'quality_assessment': self._assess_merged_quality(merged_data),
            'methodology': self._document_merge_methodology(merged_data),
            'provenance': self._generate_provenance_trail(merged_data)
        }
        
        return self._render_html_report(report_sections)
    
    def _generate_cross_experiment_visualizations(self, merged_data: MergedExperimentResult):
        """Generate visualizations comparing results across source experiments"""
        visualizations = []
        
        # Model performance comparison across experiments
        model_comparison = self._create_model_performance_chart(merged_data)
        visualizations.append(model_comparison)
        
        # Framework scoring consistency across experiments
        framework_consistency = self._create_framework_consistency_chart(merged_data)
        visualizations.append(framework_consistency)
        
        # Cost efficiency comparison
        cost_efficiency = self._create_cost_efficiency_chart(merged_data)
        visualizations.append(cost_efficiency)
        
        return visualizations
```

## 📋 Implementation Plan

### Phase 1: Core Merge Infrastructure (1-2 days)
- [ ] **ExperimentResultsLoader**: Load from database and file systems
- [ ] **DataDeduplicator**: Basic deduplication with configurable strategies
- [ ] **Basic MetadataReconciler**: Handle simple metadata conflicts
- [ ] **Simple CLI interface**: `merge_experiments.py exp1 exp2 --output merged/`

### Phase 2: Quality and Validation (1 day)
- [ ] **QualityValidator integration**: Re-run QA on merged data
- [ ] **Cross-experiment consistency checks**: Validate framework application
- [ ] **Statistical validity assessment**: Ensure merged data is analytically sound
- [ ] **Conflict resolution UI**: Handle metadata conflicts interactively

### Phase 3: Advanced Features (1-2 days)
- [ ] **UnifiedReportGenerator**: Comprehensive HTML reports
- [ ] **Cross-experiment visualizations**: Compare performance across experiments
- [ ] **Provenance tracking**: Complete audit trail of merge operations
- [ ] **Academic export formats**: Export merged data for publications

### Phase 4: Integration and Polish (1 day)
- [ ] **Orchestrator integration**: Merge directly from orchestrator
- [ ] **Research workspace integration**: Auto-discover related experiments
- [ ] **Documentation and examples**: User guides and common workflows
- [ ] **Testing with real experiments**: Validate with actual research data

## 🎯 User Workflows

### Basic Merge Workflow
```bash
# Merge two experiments by database ID
python3 scripts/applications/merge_experiments.py \
  --experiments 41 42 \
  --output research_workspaces/june_2025_research_dev_workspace/results/merged_mft_comprehensive \
  --strategy keep_latest

# Merge by result directory paths
python3 scripts/applications/merge_experiments.py \
  --experiments \
    "research_workspaces/.../results/MFT_Study_Phase1/" \
    "research_workspaces/.../results/MFT_Study_Phase2/" \
  --output merged_comprehensive_study
```

### Advanced Merge with Conflict Resolution
```bash
# Interactive merge with metadata conflict resolution
python3 scripts/applications/merge_experiments.py \
  --experiments 41 42 43 \
  --interactive \
  --resolve-conflicts \
  --validate-quality \
  --generate-report
```

### Orchestrator Integration
```yaml
# Future: Merge capability in experiment definitions
experiment_meta:
  name: "MFT_Comprehensive_Merged"
  merge_from:
    - experiment_id: 41
    - experiment_id: 42
  merge_strategy: "keep_highest_quality"
  validate_merged_quality: true
```

## 📊 Success Criteria

### Technical Success
- [ ] **Zero Data Loss**: All source experiment data preserved in merge
- [ ] **Accurate Deduplication**: Intelligent handling of duplicate analyses
- [ ] **Quality Preservation**: QA validation maintained on merged data
- [ ] **Complete Provenance**: Full audit trail of merge operations
- [ ] **Format Compatibility**: Works with all current experiment output formats

### User Experience Success  
- [ ] **Simple CLI**: Researchers can merge experiments with single command
- [ ] **Clear Conflict Resolution**: Metadata conflicts handled transparently
- [ ] **Comprehensive Reports**: Merged experiments generate publication-ready reports
- [ ] **Performance**: Merge operations complete in <2 minutes for typical experiments
- [ ] **Error Recovery**: Clear error messages and recovery suggestions

### Research Impact Success
- [ ] **Phased Research Support**: Enables iterative, budget-conscious research
- [ ] **Collaboration Enhancement**: Teams can easily combine related work
- [ ] **Publication Ready**: Merged results suitable for academic papers
- [ ] **Reproducibility**: Merge operations can be exactly reproduced
- [ ] **Academic Integration**: Works seamlessly with existing analysis pipelines

## 🔍 Risk Assessment

### Data Integrity Risks
- **Duplicate handling errors**: Incorrect deduplication could lose or double-count analyses
  - *Mitigation*: Extensive testing, conservative defaults, manual override options
- **Metadata conflicts**: Incompatible experiments could produce invalid merged data
  - *Mitigation*: Strict compatibility checking, clear conflict resolution workflows

### Performance Risks
- **Large dataset handling**: Merging many large experiments could be slow
  - *Mitigation*: Streaming processing, incremental merge capabilities
- **Memory usage**: Loading multiple experiments simultaneously could exhaust memory
  - *Mitigation*: Lazy loading, batch processing for large datasets

### User Experience Risks
- **Complexity overload**: Too many options could confuse researchers
  - *Mitigation*: Smart defaults, progressive disclosure of advanced features
- **Error interpretation**: Users might not understand merge conflicts or failures
  - *Mitigation*: Clear documentation, helpful error messages, examples

## 📈 Future Enhancements

### Advanced Merge Strategies
- **Weighted merging**: Weight experiments by quality scores or recency
- **Selective merging**: Merge only specific analyses or corpus subsets
- **Conditional merging**: Merge based on experiment outcome criteria

### Collaboration Features
- **Multi-workspace merging**: Combine experiments from different research workspaces
- **Remote experiment merging**: Merge experiments from different installations
- **Team merge workflows**: Collaborative merge with approval processes

### Research Integration
- **Automated experiment series**: Automatically merge related experiments
- **Publication integration**: Direct export to paper formats with merge documentation
- **Version control integration**: Git-based tracking of merge operations

## 🎯 Conclusion

The Experiment Results Merge System enables flexible, iterative research workflows while maintaining data integrity and analytical rigor. By supporting phased experiment approaches, the system allows researchers to optimize costs, manage budgets, and build comprehensive datasets incrementally.

This capability is essential for the Discernus research ecosystem, enabling both individual researchers and collaborative teams to conduct sophisticated multi-phase studies without sacrificing analytical capabilities or reproducibility.

**Implementation Priority**: High - Needed to support cost-effective multi-LLM research and collaborative workflows. 