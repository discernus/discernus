# Existing Systems Inventory
*BEFORE BUILDING ANYTHING NEW, CHECK THIS LIST*

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

### ✅ EnhancedExperimentOrchestrator (`scripts/comprehensive_experiment_orchestrator.py`)
**What it does**: Multi-phase experiment orchestration
**Status**: ✅ PRODUCTION READY

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
grep -r "quality.assurance\|validation\|QA" src/ docs/ scripts/
```

### Rule 2: Check This Inventory
**Before building**: "Do we already have something that does this?"

### Rule 3: Explicit Deprecation
**When replacing**: Document WHY the new version is better

### Rule 4: Keep What Works
**If existing system works**: Enhance it, don't replace it 