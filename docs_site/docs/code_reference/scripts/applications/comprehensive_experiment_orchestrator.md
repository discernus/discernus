# Comprehensive Experiment Orchestrator

**Module:** `scripts.applications.comprehensive_experiment_orchestrator`
**File:** `/app/scripts/applications/comprehensive_experiment_orchestrator.py`
**Package:** `applications`

Comprehensive Experiment Orchestrator

Addresses critical gaps identified in IDITI validation study failure:
- Single unified tool for complete experiment lifecycle
- Auto-component registration and validation  
- Experiment context propagation
- Clear error handling and guidance

Phase 1: Core Orchestrator (Day 1 Implementation)

## Dependencies

- `architectural_compliance_validator`
- `argparse`
- `asyncio`
- `dataclasses`
- `datetime`
- `enum`
- `experiment_validation_utils`
- `hashlib`
- `json`
- `logging`
- `os`
- `pathlib`
- `pickle`
- `scripts.utilities.unified_framework_validator`
- `shutil`
- `sqlalchemy`
- `sqlalchemy.exc`
- `sqlalchemy.orm`
- `src.academic.analysis_templates`
- `src.academic.documentation`
- `src.analysis.reliability`
- `src.analysis.results`
- `src.analysis.statistical_logger`
- `src.analysis.statistics`
- `src.analysis.visualization`
- `src.api.analysis_service`
- `src.corpus.exporter`
- `src.corpus.intelligent_ingestion`
- `src.corpus.registry`
- `src.corpus.validator`
- `src.models.component_models`
- `src.models.models`
- `src.utils.database`
- `src.utils.experiment_logging`
- `src.utils.framework_transaction_manager`
- `src.utils.llm_quality_assurance`
- `src.utils.statistical_logger`
- `src.visualization.themes`
- `sys`
- `tempfile`
- `traceback`
- `typing`
- `webbrowser`
- `yaml`

## Table of Contents

### Classes
- [MissingComponentsError](#missingcomponentserror)
- [FrameworkTransactionIntegrityError](#frameworktransactionintegrityerror)
- [ComponentInfo](#componentinfo)
- [ExperimentContext](#experimentcontext)
- [ConsolidatedFrameworkLoader](#consolidatedframeworkloader)
- [FrameworkAutoRegistrar](#frameworkautoregistrar)
- [ComponentAutoRegistrar](#componentautoregistrar)
- [CorpusAutoRegistrar](#corpusautoregistrar)
- [ExperimentState](#experimentstate)
- [ExperimentOrchestrator](#experimentorchestrator)
- [UnifiedAssetManager](#unifiedassetmanager)

### Functions
- [determine_experiment_results_location](#determine-experiment-results-location)
- [main](#main)

## Classes

### MissingComponentsError
*Inherits from: Exception*

Raised when required experiment components are missing

#### Methods

##### `__init__`
```python
__init__(self, missing_components: List[str], guidance: Dict[Any])
```

---

### FrameworkTransactionIntegrityError
*Inherits from: Exception*

🔒 FRAMEWORK TRANSACTION INTEGRITY ERROR

Exception raised when framework validation uncertainty threatens experiment integrity.
This is a critical error that requires experiment termination and user intervention.

#### Methods

##### `__init__`
```python
__init__(self, framework_errors: List[str], guidance: Dict[Any], detailed_message: str)
```

---

### ComponentInfo

Information about an experiment component

---

### ExperimentContext

Experiment context for hypothesis-aware analysis

#### Methods

##### `to_prompt_context`
```python
to_prompt_context(self) -> str
```

Generate context string for LLM prompts

##### `to_metadata_dict`
```python
to_metadata_dict(self) -> Dict[Any]
```

Generate metadata dictionary for database storage

##### `generate_context_summary`
```python
generate_context_summary(self) -> str
```

Generate human-readable context summary

---

### ConsolidatedFrameworkLoader

Loader for consolidated framework format

#### Methods

##### `__init__`
```python
__init__(self, frameworks_dir: str)
```

##### `load_framework`
```python
load_framework(self, framework_name: str) -> Dict[Any]
```

Load framework using enhanced pattern matching - descriptive names first, fallback to legacy

##### `validate_framework_structure`
```python
validate_framework_structure(self, framework: Dict[Any]) -> List[str]
```

Validate framework has required sections

---

### FrameworkAutoRegistrar

Auto-registration for frameworks using existing database infrastructure

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `register_framework`
```python
register_framework(self, framework_id: str, version: str) -> bool
```

Register framework from filesystem to database

##### `_extract_wells_from_consolidated`
```python
_extract_wells_from_consolidated(self, consolidated_data: Dict[Any]) -> Dict[Any]
```

Extract wells configuration from consolidated framework data

---

### ComponentAutoRegistrar

Auto-registration for prompt templates and weighting schemes

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `register_prompt_template`
```python
register_prompt_template(self, template_id: str, version: str) -> bool
```

Register default prompt template

##### `register_weighting_scheme`
```python
register_weighting_scheme(self, scheme_id: str, version: str) -> bool
```

Register default weighting scheme

##### `_generate_default_template_content`
```python
_generate_default_template_content(self, template_id: str) -> str
```

Generate default template content based on template ID

##### `_generate_default_weighting_config`
```python
_generate_default_weighting_config(self, scheme_id: str) -> Dict[Any]
```

Generate default weighting configuration based on scheme ID

---

### CorpusAutoRegistrar

Auto-registration and validation for corpus files

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `validate_corpus_file`
```python
validate_corpus_file(self, file_path: str, expected_hash: str) -> Dict[Any]
```

Validate corpus file existence and hash

##### `validate_corpus_collection`
```python
validate_corpus_collection(self, directory: str, pattern: str) -> Dict[Any]
```

Validate a collection of corpus files

##### `register_corpus_file`
```python
register_corpus_file(self, file_path: str, corpus_id: str) -> bool
```

Register corpus file using intelligent ingestion

##### `register_corpus_collection`
```python
register_corpus_collection(self, directory: str, pattern: str) -> bool
```

Register corpus collection using intelligent ingestion

##### `check_corpus_in_database`
```python
check_corpus_in_database(self, corpus_id: str, file_path: str) -> bool
```

Check if corpus item exists in database using CorpusRegistry API

##### `_calculate_file_hash`
```python
_calculate_file_hash(self, file_path: Path) -> str
```

Calculate SHA-256 hash of file

##### `_get_or_create_hash_manifest`
```python
_get_or_create_hash_manifest(self, directory: Path, filename: str) -> Optional[Path]
```

Get existing hash manifest or create one

##### `_generate_collection_manifest`
```python
_generate_collection_manifest(self, directory: Path, pattern: str) -> Optional[str]
```

Generate hash manifest for collection of files

---

### ExperimentState
*Inherits from: Enum*

Experiment transaction states for checkpoint management

---

### ExperimentOrchestrator

🚨 AI ASSISTANT WARNING: This is the PRODUCTION experiment execution system!

❌ DO NOT suggest custom scripts for:
- Statistical analysis (use enhanced_analysis_pipeline)
- Data extraction (built into orchestrator)
- Hypothesis testing (integrated in pipeline)
- Report generation (automatic HTML/academic exports)
- Visualization (comprehensive viz system included)

✅ ALWAYS use this orchestrator for ALL experiment work!

The orchestrator includes:
- Complete statistical analysis pipeline
- Architectural compliance validation
- Academic export systems
- Visualization generation
- Hypothesis tracking
- Transaction-safe execution with resume capability

Main orchestrator for comprehensive experiment execution with checkpoint/resume support

#### Methods

##### `__init__`
```python
__init__(self)
```

Initialize orchestrator with all necessary components

##### `_create_experiment_id`
```python
_create_experiment_id(self, experiment_meta: Dict[Any]) -> str
```

Create unique experiment ID for checkpoint management

##### `_get_checkpoint_path`
```python
_get_checkpoint_path(self, experiment_id: str) -> Path
```

Get checkpoint file path for experiment

##### `save_checkpoint`
```python
save_checkpoint(self, state: [ExperimentState](scripts/applications/comprehensive_experiment_orchestrator.md#experimentstate), data: Dict[Any])
```

Save experiment checkpoint for transaction safety

##### `load_checkpoint`
```python
load_checkpoint(self, experiment_id: str) -> Optional[Dict[Any]]
```

Load experiment checkpoint if it exists

##### `find_resumable_experiments`
```python
find_resumable_experiments(self) -> List[Dict[Any]]
```

Find experiments that can be resumed

##### `validate_experiment_transaction`
```python
validate_experiment_transaction(self, experiment_id: str) -> bool
```

Validate that experiment transaction completed successfully

##### `load_experiment_definition`
```python
load_experiment_definition(self, experiment_file: Path) -> Dict[Any]
```

Load and validate experiment definition with full specification validation

##### `_create_experiment_context`
```python
_create_experiment_context(self, experiment: Dict[Any]) -> [ExperimentContext](scripts/applications/comprehensive_experiment_orchestrator.md#experimentcontext)
```

Create ExperimentContext from experiment definition

##### `_create_experiment_context_for_qa`
```python
_create_experiment_context_for_qa(self, experiment: Dict[Any])
```

Create experiment context for QA system validation (imports from enhanced QA system).

##### `create_context_enriched_prompt`
```python
create_context_enriched_prompt(self, base_prompt: str, analysis_run_info: Dict[Any]) -> str
```

Create context-enriched prompt for hypothesis-aware analysis

##### `prepare_analysis_metadata`
```python
prepare_analysis_metadata(self, analysis_run_info: Dict[Any]) -> Dict[Any]
```

Prepare metadata for analysis run including experiment context

##### `generate_context_aware_output`
```python
generate_context_aware_output(self, analysis_results: Dict[Any], analysis_run_info: Dict[Any]) -> Dict[Any]
```

Generate context-aware output with hypothesis validation

##### `create_validation_report`
```python
create_validation_report(self, all_results: List[Dict[Any]]) -> Dict[Any]
```

Create validation report tied to research questions

##### `validate_components`
```python
validate_components(self, experiment: Dict[Any]) -> List[[ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)]
```

Validate all experiment components and identify missing ones

##### `_validate_framework`
```python
_validate_framework(self, framework_spec: Dict[Any]) -> [ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)
```

Validate framework component using unified framework validator and asset management flow.

🎯 CONSOLIDATED VALIDATION:
- Uses unified framework validator for comprehensive validation
- Supports both dipole-based and independent wells architectures
- Validates YAML and JSON formats
- Includes academic standards and semantic consistency checks

##### `_validate_prompt_template`
```python
_validate_prompt_template(self, template_spec: Dict[Any]) -> [ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)
```

Validate prompt template component

##### `_validate_weighting_scheme`
```python
_validate_weighting_scheme(self, scheme_spec: Dict[Any]) -> [ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)
```

Validate weighting scheme component

##### `_validate_model`
```python
_validate_model(self, model_spec: Dict[Any]) -> [ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)
```

Validate model availability

##### `_validate_corpus`
```python
_validate_corpus(self, corpus_spec: Dict[Any]) -> [ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)
```

Validate corpus component with integrity checks.

##### `_check_framework_in_database`
```python
_check_framework_in_database(self, framework_id: str, version: str) -> bool
```

Check if framework exists in database

##### `_check_template_in_database`
```python
_check_template_in_database(self, template_id: str, version: str) -> bool
```

Check if prompt template exists in database

##### `_check_weighting_in_database`
```python
_check_weighting_in_database(self, scheme_id: str, version: str) -> bool
```

Check if weighting scheme exists in database

##### `auto_register_missing_components`
```python
auto_register_missing_components(self, missing_components: List[[ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)]) -> bool
```

Auto-register missing components with comprehensive logging

##### `_register_framework_from_storage`
```python
_register_framework_from_storage(self, component: [ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)) -> bool
```

Register framework from content-addressable storage to database

##### `generate_error_guidance`
```python
generate_error_guidance(self, missing_components: List[[ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)]) -> Dict[Any]
```

Generate helpful error messages and guidance

##### `pre_flight_validation`
```python
pre_flight_validation(self, experiment: Dict[Any]) -> Tuple[Any]
```

Enhanced pre-flight validation with component existence checks.

##### `_generate_framework_failure_message`
```python
_generate_framework_failure_message(self, guidance: Dict[Any], framework_errors: List[str]) -> str
```

Generate comprehensive error message for framework transaction failures

##### `show_execution_plan`
```python
show_execution_plan(self, experiment: Dict[Any], components: List[[ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)])
```

Show what would be executed (dry-run mode)

##### `execute_enhanced_analysis_pipeline`
```python
execute_enhanced_analysis_pipeline(self, execution_results: Dict[Any], experiment: Dict[Any]) -> Dict[Any]
```

Orchestrates the post-processing of results into a full academic package.

##### `_generate_comprehensive_html_report`
```python
_generate_comprehensive_html_report(self, structured_results, statistical_results, reliability_results, visualization_results, output_dir)
```

Generate comprehensive HTML report combining all analysis results.

##### `_generate_academic_exports`
```python
_generate_academic_exports(self, structured_results, output_dir, experiment)
```

Generate academic exports if enabled.

##### `_determine_experiment_output_location`
```python
_determine_experiment_output_location(self, experiment_name: str, timestamp: str) -> Path
```

Determine the appropriate output location for experiment results.

Follows the new organizational pattern:
- Research experiments: results go in research workspace
- System experiments: results go in system experiments directory

##### `_generate_pipeline_summary_report`
```python
_generate_pipeline_summary_report(self, enhanced_results, output_dir, experiment_dir)
```

Generate a human-readable summary report.

##### `execute_analysis_matrix`
```python
execute_analysis_matrix(self, experiment: Dict[Any], components: List[[ComponentInfo](scripts/applications/comprehensive_experiment_orchestrator.md#componentinfo)]) -> Dict[Any]
```

Execute the actual analysis matrix with real API calls

##### `_load_corpus_text`
```python
_load_corpus_text(self, file_path: str) -> Optional[str]
```

Load text content from corpus file or directory collection

##### `execute_experiment`
```python
execute_experiment(self, experiment_file: Path)
```

🚨 TRANSACTION-SAFE EXPERIMENT EXECUTION 🚨

This method treats experiments as atomic transactions that must complete fully.
Resume capability prevents losing expensive LLM analysis work.

❌ AI ASSISTANTS: DO NOT suggest bypassing this with custom scripts!
✅ This orchestrator handles ALL experiment needs including statistical analysis.

##### `_validate_experiment_for_database`
```python
_validate_experiment_for_database(self, experiment_meta: Dict[Any], experiment: Dict[Any]) -> Dict[Any]
```

🔒 COHERENCE VALIDATION: Validate experiment data for database insertion
Ensures all required Experiment model fields are present and valid.

---

### UnifiedAssetManager

Unified asset management with content-addressable storage

#### Methods

##### `__init__`
```python
__init__(self, storage_root: str)
```

##### `calculate_content_hash`
```python
calculate_content_hash(self, content: Any, asset_type: str) -> str
```

Calculate SHA-256 hash of asset content

##### `get_storage_path`
```python
get_storage_path(self, content_hash: str, asset_type: str) -> Path
```

Get storage path for content hash using prefix-based directory structure

##### `store_asset`
```python
store_asset(self, content: Any, asset_type: str, asset_id: str, version: str, source_path: Optional[str]) -> Dict[Any]
```

Store validated asset in content-addressable storage

##### `load_asset_by_hash`
```python
load_asset_by_hash(self, content_hash: str, asset_type: str) -> Optional[Dict[Any]]
```

Load asset by content hash

##### `verify_asset_integrity`
```python
verify_asset_integrity(self, content_hash: str, asset_type: str) -> bool
```

Verify asset integrity by recalculating hash

---

## Functions

### `determine_experiment_results_location`
```python
determine_experiment_results_location(experiment_file_path: str, experiment_name: str) -> Path
```

Utility function to determine appropriate results location for any experiment.

This function implements the organizational pattern:
- Research experiments (from research_workspaces): results go in research workspace
- System experiments: results go in system experiments directory

Args:
    experiment_file_path: Path to the original experiment file
    experiment_name: Name of the experiment for directory naming
    
Returns:
    Path where experiment results should be placed

---

### `main`
```python
main()
```

Main CLI entry point

---

*Generated on 2025-06-21 20:19:04*