# Existing Systems Inventory

This document serves as a catalog of all production-ready systems in the Discernus project. Before starting any new development, consult this inventory to see if existing functionality can be enhanced or reused.

---

## Core Application Systems (`src/`)

These modules form the core of the Discernus application.

| Module | Description |
| :--- | :--- |
| `academic/` | Contains tools for academic integration, such as data export and replication package builders. |
| `analysis/` | Core analysis components, including reliability and results processing. |
| `api/` | The main application API, including the analysis service and data schemas. |
| `api_clients/` | Clients for interacting with external LLM APIs (OpenAI, Anthropic, etc.). |
| `coordinate_engine.py` | The mathematical engine for calculating narrative positions from analysis scores. |
| `corpus/` | Tools for managing and processing text corpora, including discovery and ingestion. |
| `framework_manager.py` | Manages the loading, validation, and application of analytical frameworks. |
| `models/` | Defines the database models and schemas for all persistent data. |
| `prompts/` | Manages the generation and versioning of prompt templates for LLMs. |
| `utils/` | A collection of shared, production-ready utility functions. |
| `visualization/` | The engine for generating all plots and visualizations for reports. |

---

## Production Scripts & Tools (`scripts/applications/`)

These are production-ready scripts that perform key operational or administrative tasks.

| Script | Description |
| :--- | :--- |
| `comprehensive_experiment_orchestrator.py` | **Primary entry point for research.** The main script for defining and running complex experiments. |
| `execute_experiment_definition.py` | A focused script for running a pre-defined experiment file. Used by the main orchestrator. |
| `check_existing_systems.py` | **Mandatory check before development.** A utility to search the codebase for existing functionality. |
| `validate_ai_assistant_compliance.py` | A tool to ensure that AI-driven development adheres to project rules. |
| `framework_sync.py` | Synchronizes framework definitions between the filesystem and the database. |
| `bloat_prevention_system.py` | A system to detect and report on code or asset bloat. |
| `enhanced_experiment_reports.py` | Generates detailed, multi-page HTML reports from experiment results. |
| `create_experiment_package.py` | Creates a self-contained, shareable package from an experiment's results. |
| `end_to_end_pipeline_test.py` | A script for running a full, end-to-end test of the entire analysis pipeline. |

## 🎯 Current Status (June 20, 2025):** Major architectural breakthrough validated. Framework integration working. Import path technical debt affects enhanced analysis components.

## 🔍 Quality Assurance Systems

### ✅ LLMQualityAssuranceSystem (`src/narrative_gravity/utils/llm_quality_assurance.py`)
**What it does**: 6-layer mathematical validation of LLM analysis results
- **Layer 1**: Input validation (text length, quality, framework compatibility)
- **Layer 2**: LLM response validation (JSON format, score ranges, completeness)  
- **Layer 3**: Statistical coherence (default value detection, variance analysis)
- **Layer 4**: Mathematical consistency (coordinate calculation verification)
- **Layer 5**: Cross-validation (second opinion triggers)
- **Layer 6**: Anomaly detection (outliers, symmetry, artifacts)
**Status**: ✅ PRODUCTION READY - DO NOT REPLACE
**Usage**: `validate_llm_analysis(text, framework, response, scores)`

### ✅ ComponentQualityValidator (`src/narrative_gravity/development/quality_assurance.py`)
**What it does**: Validates prompt templates, frameworks, weighting methodologies
- 15+ mathematical checks for weighting algorithms
- Academic standards validation
- Component compatibility testing
**Status**: ✅ PRODUCTION READY
**Usage**: `validator.validate_prompt_template(template)`

### ❌ ArchitecturalComplianceValidator (`scripts/architectural_compliance_validator.py`)
**What it does**: File existence checks and string matching
**Status**: ⚠️ INFERIOR REPLACEMENT - Consider deprecating
**Problem**: Dumbed-down version of real QA systems above

## 🧪 Experiment Execution Systems

### ✅ DeclarativeExperimentExecutor (`scripts/execute_experiment_definition.py`)
**What it does**: YAML-driven experiment execution with QA integration
**Status**: ✅ PRODUCTION READY
**Features**: Built-in QA validation, cost controls, replication

### ✅ EnhancedExperimentOrchestrator (`scripts/production/comprehensive_experiment_orchestrator.py`)
**What it does**: Multi-phase experiment orchestration with framework-aware architecture
**Status**: ✅ CORE INFRASTRUCTURE WORKING - IMPORT ISSUES AFFECT ENHANCED ANALYSIS
**Architectural Breakthrough**: Unified YAML framework architecture eliminates configuration mismatches
**Working Components**:
- Framework integration and transaction management
- LLM connections (OpenAI, Anthropic, Google AI)
- Asset management and intelligent output routing
- Database graceful degradation
**Blocked Components**: Enhanced analysis pipeline (import path technical debt)
**Usage**: `PYTHONPATH=src python3 scripts/production/comprehensive_experiment_orchestrator.py experiment.yaml`

## 📊 Data Export & Analysis

### ✅ QAEnhancedDataExporter (`src/narrative_gravity/academic/data_export.py`)
**What it does**: Academic data export with integrated QA validation
**Status**: ✅ PRODUCTION READY
**Features**: CSV, R, Stata, JSON export with confidence scores

### ✅ AcademicAnalysisPipeline (`src/narrative_gravity/cli/academic_analysis_pipeline.py`)
**What it does**: Complete academic workflow orchestration
**Status**: ✅ PRODUCTION READY

## 🏗️ Framework Management

### ✅ FrameworkManager (`src/narrative_gravity/framework_manager.py`)
**What it does**: Load and manage analytical frameworks
**Status**: ✅ PRODUCTION READY

### ✅ UnifiedFrameworkArchitecture (Multiple Components)
**What it does**: Major architectural breakthrough solving YAML/JSON configuration mismatches
**Status**: ✅ VALIDATED & WORKING (June 20, 2025)
**Components Modified**:
- `src/narrative_gravity/engine_circular.py` - Framework-aware circular engine
- `src/narrative_gravity/api/analysis_service.py` - Framework-aware analysis service
- `src/narrative_gravity/utils/llm_quality_assurance.py` - Framework-aware QA coordinate calculations
**Breakthrough**: Eliminated fundamental mismatch between YAML experiment definitions and JSON circular engine configuration
**Result**: All Discernus components now use unified YAML framework architecture

## ⚠️ TECHNICAL DEBT

### ⚠️ Import Path Issues (Widespread)
**Problem**: `No module named 'src'` and `No module named 'scripts'` errors affecting multiple systems
**Affected Systems**: Most CLI tools, enhanced analysis pipeline, orchestrator components
**Workaround**: Use `PYTHONPATH=src` for all operations
**Status**: Technical debt preventing full enhanced analysis pipeline completion
**Impact**: Core systems work, but enhanced analysis components blocked

### ⚠️ Enhanced Analysis Pipeline Components
**Affected Files**:
- `scripts/extract_experiment_results.py`
- `scripts/statistical_hypothesis_testing.py` 
- `scripts/interrater_reliability_analysis.py`
- `scripts/generate_comprehensive_visualizations.py`
**Status**: Import path issues prevent loading despite core functionality being designed
**Workaround**: Core orchestrator provides graceful degradation

## ⚠️ DEPRECATION CANDIDATES

### ❌ AI Academic Advisor "Methodology"
**Problem**: Rebranded file existence checks as "AI methodology"
**Better Alternative**: Use existing LLMQualityAssuranceSystem
**Action**: Remove or merge with real QA systems

---

## 🛡️ PREVENTION RULES

### Rule 1: Search First
```bash
# ALWAYS run before building anything:
python3 scripts/applications/check_existing_systems.py "functionality description"
# OR manually search:
grep -r "quality.assurance\|validation\|QA" src/ docs/ scripts/
```

### Rule 2: Check This Inventory
**Before building**: "Do we already have something that does this?"

### Rule 3: Use PYTHONPATH
```bash
# ALWAYS use PYTHONPATH for CLI operations:
PYTHONPATH=src python scripts/any_script.py
# OR set environment variable:
export PYTHONPATH=src
```

### Rule 4: Test with Production Orchestrator
```bash
# Validate new components with working orchestrator:
PYTHONPATH=src python3 scripts/production/comprehensive_experiment_orchestrator.py \
    research_workspaces/test_workspace/experiments/test.yaml --force-reregister
```

### Rule 5: Explicit Deprecation
**When replacing**: Document WHY the new version is better

### Rule 6: Keep What Works
**If existing system works**: Enhance it, don't replace it

## 📊 PRODUCTION VALIDATION STATUS (June 20, 2025)

### ✅ Validated Working Systems
- Framework-aware orchestrator infrastructure
- YAML unified architecture (eliminates config mismatches)
- LLM connections (OpenAI, Anthropic, Google AI)
- Asset management and transaction system
- Intelligent output routing for research workspaces

### ⚠️ Systems Blocked by Technical Debt
- Enhanced analysis pipeline (import path issues)
- Most CLI tools (require PYTHONPATH)
- Statistical analysis components (import path issues)

### 🎯 Current Production Recommendation
Use validated orchestrator workflow for framework architecture validation and graceful degradation when enhanced components have import issues. 