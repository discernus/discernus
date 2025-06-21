# Formal Specification System
## Discernus Framework Standardization

**Version:** 2.1.0  
**Date:** June 21, 2025  
**Status:** Production (Updated post-validation consolidation)

---

## 🎯 **Executive Summary**

This document establishes **production-ready specifications** for the Discernus analytical system, updated to reflect the **unified validation architecture** and current **YAML-first format**:

1. **Framework Specifications** - YAML-based frameworks supporting multiple architectures (dipole + independent wells)
2. **Experiment Definition Specifications** - Comprehensive experiment configuration format  
3. **Validation System Architecture** - Unified validation with deprecated system documentation
4. **Component Integration Specifications** - Prompt templates, weighting schemes, and orchestrator integration

## 📐 **1. Framework Specification Standard (YAML v2.1)**

### **1.1 Current Framework Schema**

**Primary Format**: YAML (`.yaml` files in framework directories)

```yaml
# =============================================================================
# FRAMEWORK METADATA  
# =============================================================================
name: framework_identifier
framework_name: framework_identifier  # Legacy compatibility
display_name: "Human Readable Name"
version: vYYYY.MM.DD
description: |
  Academic description of theoretical foundation and methodology.
  Multi-line descriptions supported.

framework_type: enum[dipoles_based, independent_wells]

# =============================================================================
# COORDINATE SYSTEM
# =============================================================================
coordinate_system:
  type: circle
  radius: 1.0
  description: "Coordinate system description"

positioning_strategy:
  type: enum[opposing_pairs, clustered_positioning, equidistant_wells]
  description: "Positioning methodology description"

# =============================================================================
# THEORETICAL FOUNDATION
# =============================================================================
theoretical_foundation:
  primary_sources:
    - "Academic citation 1"
    - "Academic citation 2"
  theoretical_approach: |
    Methodological description and theoretical grounding
  core_insight: |
    Key theoretical insight driving the framework

# =============================================================================
# FRAMEWORK ARCHITECTURE (Dipole-Based)
# =============================================================================
dipoles:  # For dipole-based frameworks
  - name: Dipole_Name
    description: "Theoretical foundation for this dipole"
    
    positive:
      name: Positive_Well
      description: "Positive pole description"
      language_cues:
        basic_terms:
          - term1
          - term2
        moral_imperatives:
          - "imperative pattern"
      angle: 0
      weight: 1.0
      type: well_type
      tier: primary
    
    negative:
      name: Negative_Well
      description: "Negative pole description"
      language_cues:
        - basic_term1
        - basic_term2
      angle: 180
      weight: -1.0
      type: well_type_violation
      tier: primary

# =============================================================================
# FRAMEWORK ARCHITECTURE (Independent Wells)
# =============================================================================
wells:  # For independent wells frameworks
  well_identifier:
    position:
      angle_degrees: 0
      coordinates: [1.0, 0.0]
    name: "Well Name"
    description: "Well theoretical description"
    rich_description: "Extended description"
    core_principles:
      - "Principle 1"
      - "Principle 2"
    language_cues:
      category_name:
        - "cue pattern 1"
        - "cue pattern 2"
    weight: 1.0
    type: independent
    tier: primary

# =============================================================================
# ANALYSIS CONFIGURATION
# =============================================================================
weighting_philosophy:
  description: "Weighting methodology description"
  approach: enum[equal_weighting, empirical_validation_based, theoretical_weighting]
  
metrics:
  metric_code:
    name: "Metric Display Name"
    description: "Metric calculation and interpretation"
    calculation: "Mathematical formula description"

# =============================================================================
# VALIDATION METADATA (Added post-consolidation)
# =============================================================================
validation_metadata:
  last_validated: "2025-06-21"
  validator_version: "unified_framework_validator_v2.0"
  validation_result: VALID
  architecture_detected: enum[dipole_based, independent_wells]
  wells_count: integer
  dipoles_count: integer

# =============================================================================
# INTEGRATION COMPATIBILITY
# =============================================================================
compatibility:
  prompt_templates: ["template_id_1", "template_id_2"]
  weighting_schemes: ["scheme_id_1", "scheme_id_2"]
  orchestrator_version: "v2.1.0"
```

### **1.2 Framework Architecture Types**

**Dipole-Based Frameworks** (e.g., Moral Foundations Theory):
- Structure: `dipoles[]` array with `positive`/`negative` objects
- Wells: Automatically derived from dipole endpoints
- Use Case: Bipolar theoretical constructs (moral foundations, political spectrums)
- Validation: Ensures opposing pairs have consistent structure

**Independent Wells Frameworks** (e.g., Three Wells Political):
- Structure: `wells{}` dictionary with `position` objects
- Wells: Independently positioned theoretical constructs
- Use Case: Multiple competing theories, non-bipolar frameworks
- Validation: Ensures well positioning and theoretical coherence

### **1.3 Framework Validation Architecture**

**Production Validator**: `scripts/utilities/unified_framework_validator.py`
- **Multi-architecture support**: Automatically detects dipole vs independent wells
- **Format support**: YAML (primary) + JSON (legacy migration)
- **Validation layers**: Format → Structure → Semantics → Academic → Integration
- **CLI interface**: `python scripts/utilities/unified_framework_validator.py --all`

**Deprecated Systems** (moved to `deprecated/by-system/`):
- `validate_framework_spec.py` - Legacy JSON-only validator
- Use unified validator for all new development

**Validation Command Examples**:
```bash
# Validate single framework
python scripts/utilities/unified_framework_validator.py frameworks/moral_foundations_theory/

# Validate all frameworks with verbose output
python scripts/utilities/unified_framework_validator.py --all --verbose

# Framework validation in orchestrator (automatic)
python scripts/applications/comprehensive_experiment_orchestrator.py experiment.yaml
```

---

## 📋 **2. Experiment Definition Specification (YAML v2.1)**

### **2.1 Experiment Definition Schema**

```yaml
# =============================================================================
# EXPERIMENT METADATA
# =============================================================================
experiment_meta:
  name: "Experiment Name"
  version: "v1.0.0"
  description: "Comprehensive experiment description"
  created: "2025-06-21T10:00:00"
  
  # Research Context
  hypotheses:
    - "Research hypothesis 1"
    - "Research hypothesis 2"
  research_context: "Academic research context and background"
  success_criteria:
    - "Success criterion 1"
    - "Success criterion 2"
  
  # Academic Metadata
  principal_investigator: "researcher@institution.edu"
  institution: "Research Institution"
  funding_source: "Funding agency"
  ethical_clearance: "IRB-2025-001"
  tags: ["tag1", "tag2"]

# =============================================================================
# COMPONENT SPECIFICATIONS
# =============================================================================
components:
  frameworks:
    - id: framework_id
      type: file_path
      file_path: "frameworks/framework_name/framework_name_framework.yaml"
      version: "v2025.06.19"
  
  prompt_templates:
    - id: template_id
      type: existing
      version: "v2.1"
  
  weighting_schemes:
    - id: scheme_id
      type: existing
      version: "v1.0"
  
  models:
    - id: model_id
      provider: "openai"
      version: "gpt-4.1-mini"
      parameters:
        temperature: 0.1
        max_tokens: 4000
  
  corpus:
    - id: corpus_id
      type: file_collection
      file_path: "corpus/directory_name"
      pattern: "*.txt"

# =============================================================================
# EXECUTION CONFIGURATION
# =============================================================================
execution:
  description: "Execution methodology description"
  
  matrix:
    - run_id: "run_identifier"
      # Additional run parameters
  
  cost_controls:
    max_total_cost: 5.00
    max_run_cost: 0.10
    confirm_before_execution: true
  
  quality_assurance:
    enable_qa_validation: true
    qa_confidence_threshold: 0.7
    require_second_opinion_below: 0.5
  
  academic_compliance:
    generate_reproducibility_package: true
    publication_ready_exports: true
    statistical_analysis: true
```

### **2.2 Experiment Validation Architecture**

**Production Validator**: `scripts/applications/experiment_validation_utils.py`
- **Orchestrator integration**: Used by `comprehensive_experiment_orchestrator.py`
- **Comprehensive validation**: Structure, components, execution parameters
- **Error guidance**: Clear fix suggestions with examples
- **Academic standards**: Publication readiness validation

**Deprecated System** (moved to `deprecated/by-system/`):
- `experiment_validator.py` - Redundant standalone validator
- Use orchestrator-integrated validation for all experiments

**Validation Integration**:
```python
# In comprehensive_experiment_orchestrator.py
from scripts.applications.experiment_validation_utils import ExperimentValidator

validator = ExperimentValidator()
result = validator.validate_experiment_file(experiment_file)
```

---

## 🔧 **3. Component Integration Specifications**

### **3.1 Prompt Template Integration**

**Current Implementation**: Database-stored templates with framework compatibility
- **Template storage**: Database with version control
- **Framework agnostic**: Templates work across multiple frameworks  
- **LLM optimization**: Model-specific adaptations
- **Output standardization**: Consistent JSON response format

**Template Registration**:
```python
# Via orchestrator auto-registration
component_registrar.register_prompt_template(template_id, version)
```

### **3.2 Weighting Scheme Integration**

**Current Implementation**: Algorithm-based weighting with mathematical validation
- **Scheme storage**: Database with parameter definitions
- **Mathematical validation**: Formula verification and edge case handling
- **Framework compatibility**: Multi-framework support
- **Performance requirements**: Computational efficiency standards

**Scheme Registration**:
```python
# Via orchestrator auto-registration  
component_registrar.register_weighting_scheme(scheme_id, version)
```

### **3.3 Orchestrator Integration Architecture**

**Production System**: `scripts/applications/comprehensive_experiment_orchestrator.py`
- **Unified validation**: Frameworks, experiments, components
- **Transaction safety**: Checkpoint/resume capability
- **Cost protection**: Budget controls and monitoring
- **Academic exports**: Publication-ready outputs

**Integration Flow**:
1. **Experiment validation** → experiment_validation_utils
2. **Framework validation** → unified_framework_validator  
3. **Component validation** → orchestrator internal systems
4. **Execution** → transaction-safe pipeline
5. **Output generation** → academic export systems

---

## 🗑️ **4. Deprecated System Documentation**

### **4.1 Moved to `deprecated/by-system/`**

**Framework Validation**:
- `validate_framework_spec.py` - Legacy JSON-only validator
- **Replacement**: `scripts/utilities/unified_framework_validator.py`
- **Migration**: No action needed - new validator auto-detects formats

**Experiment Validation**:
- `experiment_validator.py` - Standalone validator not integrated with orchestrator
- **Replacement**: `scripts/applications/experiment_validation_utils.py` (orchestrator-integrated)
- **Migration**: Use orchestrator for all experiment execution

### **4.2 Migration Guidance**

**For Framework Development**:
```bash
# OLD (deprecated)
python scripts/utilities/validate_framework_spec.py framework.json

# NEW (production)
python scripts/utilities/unified_framework_validator.py frameworks/framework_name/
```

**For Experiment Execution**:
```bash
# OLD (deprecated)  
python scripts/applications/experiment_validator.py experiment.yaml

# NEW (production)
python scripts/applications/comprehensive_experiment_orchestrator.py experiment.yaml
```

---

## 📊 **5. Quality Assurance Integration**

### **5.1 Validation Pipeline Architecture**

**Multi-Layer Validation** (automatically applied):
1. **Format Detection & Parsing** - YAML/JSON with error handling
2. **Structural Validation** - Architecture-aware schema validation  
3. **Semantic Consistency** - Cross-component compatibility
4. **Academic Standards** - Citation format, theoretical foundation
5. **Integration Compatibility** - Orchestrator and QA system integration

### **5.2 Automated Quality Checks**

**Framework Validation**:
```bash
# Single framework with detailed output
python scripts/utilities/unified_framework_validator.py frameworks/framework_name/ --verbose

# All frameworks with summary report
python scripts/utilities/unified_framework_validator.py --all --summary
```

**Experiment Validation**:
```bash
# Integrated with orchestrator (automatic)
python scripts/applications/comprehensive_experiment_orchestrator.py experiment.yaml

# Manual pre-flight validation
python -c "
from scripts.applications.experiment_validation_utils import ExperimentValidator
validator = ExperimentValidator()
result = validator.validate_experiment_file('experiment.yaml')
validator.print_report()
"
```

---

## 🎯 **6. Current System Status & Compliance**

### **6.1 MECEC Compliance Assessment**

**✅ Mutually Exclusive**:
- Framework validation: Unified validator only (deprecated systems moved)
- Experiment validation: Orchestrator-integrated only (standalone deprecated)
- Clear component boundaries: Frameworks, experiments, prompts, weighting schemes

**✅ Collectively Exhaustive**:
- Framework architectures: Dipole-based + independent wells covered
- Validation layers: Format, structure, semantics, academic, integration
- Component types: All experiment components specified

**✅ Current**:
- Updated: June 21, 2025 (post-validation consolidation)
- Reflects: Current YAML format, unified validator, orchestrator integration
- Validated: Production systems verified, deprecated systems documented

### **6.2 Implementation Status**

**✅ Production Ready**:
- Unified framework validator (1,054 lines) - comprehensive multi-architecture support
- Experiment validation utils (463 lines) - orchestrator-integrated validation
- Comprehensive orchestrator - transaction-safe execution with QA integration

**✅ Migration Complete**:
- Legacy validators moved to `deprecated/by-system/`
- Clear deprecation notices with replacement guidance
- No breaking changes - backward compatibility maintained during transition

---

## 📋 **7. Developer Quick Reference**

### **7.1 Framework Development**
```bash
# 1. Create framework directory
mkdir frameworks/my_framework/

# 2. Create framework YAML file  
# Use existing framework as template (MFT for dipoles, Three Wells for independent)

# 3. Validate framework
python scripts/utilities/unified_framework_validator.py frameworks/my_framework/

# 4. Test with orchestrator
python scripts/applications/comprehensive_experiment_orchestrator.py test_experiment.yaml
```

### **7.2 Experiment Development**
```bash
# 1. Create experiment YAML file
# Use experiment template from docs/specifications/

# 2. Execute with validation
python scripts/applications/comprehensive_experiment_orchestrator.py experiment.yaml

# 3. Monitor execution and results
# Orchestrator provides real-time progress and academic exports
```

### **7.3 Validation Commands**
```bash
# Framework validation
python scripts/utilities/unified_framework_validator.py --all --verbose

# Experiment execution (includes validation)
python scripts/applications/comprehensive_experiment_orchestrator.py experiment.yaml

# QA system integration (automatic in orchestrator)
# No separate commands needed - integrated into all experiment execution
```

This specification system establishes **Discernus** as a rigorous, standardized framework for computational narrative analysis while maintaining the flexibility needed for ongoing research and development. 