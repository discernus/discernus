# Priority 2: Manual Development Support Guide

**Version:** 2.4.0  
**Status:** Complete  
**Created:** June 11, 2025

## Overview

Priority 2 provides structured development workflows, session management, and quality assurance tools for systematic component development. This infrastructure accelerates manual development while ensuring academic rigor and consistency.

## 🎯 Key Features

### **Structured Development Documentation**
- **Seed Prompt Library**: Standardized prompts for LLM-assisted development
- **Development Process Protocols**: Step-by-step systematic workflows
- **Quality Criteria Checklists**: Component-specific validation requirements
- **Success Metrics Framework**: Performance tracking and improvement measurement

### **Development Session Management**
- **Session Tracking**: Complete audit trail of development iterations
- **Hypothesis Testing**: Systematic validation of improvement approaches
- **Performance Monitoring**: Quantitative metrics across development sessions
- **Version Integration**: Seamless connection to Priority 1 component versioning

### **Quality Assurance Framework**
- **Automated Validation**: 50+ quality checks across component types
- **Academic Standards**: Publication-ready quality assessment
- **Compatibility Testing**: Cross-component integration validation
- **Report Generation**: Comprehensive quality reports with recommendations

## 🚀 Quick Start

### 1. Start a Development Session

```bash
# Start prompt template development
python src/narrative_gravity/cli/start_dev_session.py \
  --component-type prompt_template \
  --name hierarchical_v3 \
  --hypothesis "Improve evidence extraction and ranking clarity"

# Start framework development  
python src/narrative_gravity/cli/start_dev_session.py \
  --component-type framework \
  --name environmental_justice \
  --hypothesis "Test framework coverage for environmental narratives"

# Get seed prompt only (for external LLM sessions)
python src/narrative_gravity/cli/start_dev_session.py \
  --component-type prompt_template \
  --get-seed-prompt-only \
  --framework-name civic_virtue \
  --current-challenge "Inconsistent scoring across runs"
```

### 2. Log Development Iterations

```bash
# Log iteration with performance metrics
python src/narrative_gravity/cli/log_iteration.py \
  --session-id abc123-def456 \
  --hypothesis "Test evidence extraction improvements" \
  --changes "Added explicit quote requirements and examples" \
  --cv 0.18 \
  --hierarchy-score 0.85 \
  --notes "Significant improvement in thematic distinction"

# Interactive logging mode
python src/narrative_gravity/cli/log_iteration.py \
  --session-id abc123-def456 \
  --interactive

# Log with external test results
python src/narrative_gravity/cli/log_iteration.py \
  --session-id abc123-def456 \
  --hypothesis "Test parameter optimization" \
  --changes "Modified amplification factor to 1.3" \
  --results test_results.json
```

### 3. Validate Component Quality

```bash
# Validate prompt template
python src/narrative_gravity/cli/validate_component.py \
  --component-type prompt_template \
  --file prompt_hierarchical_v3.txt \
  --template-type hierarchical

# Validate framework with theoretical foundation
python src/narrative_gravity/cli/validate_component.py \
  --component-type framework \
  --file civic_virtue_framework.json \
  --framework-name "Civic Virtue Framework" \
  --theoretical-foundation theoretical_background.txt

# Validate component compatibility
python src/narrative_gravity/cli/validate_component.py \
  --component-type compatibility \
  --prompt-file prompt.txt \
  --framework-file framework.json \
  --weighting-file weighting.json
```

## 📋 Detailed Workflows

### **Prompt Template Development**

#### Development Session Workflow
1. **Start Session** with specific hypothesis
2. **Get Seed Prompt** customized for prompt template development
3. **Iterate** using LLM-assisted refinement
4. **Log Each Iteration** with performance metrics
5. **Validate Quality** using automated checks
6. **Complete Session** with lessons learned

#### Example Development Session
```bash
# 1. Start session
SESSION_ID=$(python src/narrative_gravity/cli/start_dev_session.py \
  --component-type prompt_template \
  --name hierarchical_v3 \
  --hypothesis "Improve ranking clarity and evidence extraction" \
  | grep "Session ID:" | cut -d: -f2 | xargs)

# 2. Development iterations (repeat as needed)
python src/narrative_gravity/cli/log_iteration.py \
  --session-id $SESSION_ID \
  --hypothesis "Test explicit ranking instructions" \
  --changes "Added step-by-step ranking requirements" \
  --cv 0.22 \
  --hierarchy-score 0.78

python src/narrative_gravity/cli/log_iteration.py \
  --session-id $SESSION_ID \
  --hypothesis "Test evidence integration" \
  --changes "Required specific quotes for each ranking" \
  --cv 0.18 \
  --hierarchy-score 0.85 \
  --evidence-quality 0.91

# 3. Quality validation
python src/narrative_gravity/cli/validate_component.py \
  --component-type prompt_template \
  --file prompt_hierarchical_v3.txt \
  --export-report quality_report.json

# 4. Create component version (using Priority 1 tools)
python src/narrative_gravity/cli/manage_components.py create prompt-template \
  --name hierarchical_civic_virtue \
  --version v3.0 \
  --file prompt_hierarchical_v3.txt \
  --parent-version v2.1
```

### **Framework Development**

#### Systematic Framework Design
1. **Theoretical Grounding**: Establish conceptual foundation
2. **Dipole Architecture**: Design complementary tension pairs  
3. **Operational Definitions**: Create precise, measurable descriptions
4. **Application Testing**: Validate across narrative types
5. **Quality Assessment**: Comprehensive validation checks

#### Framework Quality Criteria
- **Conceptual Distinctness**: Non-overlapping dipole dimensions
- **Operational Clarity**: Precise definitions enabling consistent application
- **Theoretical Grounding**: Connection to established scholarship
- **Domain Coverage**: Comprehensive capture of analytical space
- **Cross-Narrative Validity**: Applicability across different text types

### **Weighting Methodology Development**

#### Mathematical Rigor Requirements
1. **Algorithm Specification**: Clear mathematical formulation
2. **Parameter Validation**: Reasonable ranges and constraints
3. **Edge Case Analysis**: Behavior in extreme scenarios
4. **Performance Testing**: Quantitative improvement validation
5. **Integration Compatibility**: Seamless pipeline integration

#### Quality Validation Checks
- **Mathematical Soundness**: Proper mathematical operations
- **Hierarchy Enhancement**: Amplification of dominant themes
- **Statistical Properties**: Variance and distribution characteristics
- **Computational Efficiency**: Performance and scalability
- **Result Interpretability**: Clear meaning and thresholds

## 🧪 Quality Assurance System

### **Automated Quality Checks**

#### Prompt Template Validation (15+ checks)
- Format compliance (hierarchical requirements, JSON output)
- Instruction clarity (ambiguous language detection)
- Completeness (required elements, output specification)
- Academic standards (reasoning requirements, evidence extraction)
- Performance prediction (consistency enablers, edge case handling)

#### Framework Validation (12+ checks)  
- Structural requirements (dipoles, wells, theoretical foundation)
- Content quality (conceptual distinctness, operational clarity)
- Academic standards (theoretical grounding, framework coherence)
- Application readiness (measurability, cross-narrative applicability)

#### Weighting Methodology Validation (15+ checks)
- Mathematical specification (algorithm type, formula, parameters)
- Mathematical validity (soundness, edge cases, normalization)
- Performance characteristics (hierarchy enhancement, statistical properties)
- Integration compatibility (pipeline compatibility, interpretability)

#### Component Compatibility Validation (8+ checks)
- Cross-component alignment (prompt-framework, framework-weighting)
- Integration quality (workflow coherence, performance synergy)

### **Quality Levels**
- **🟢 Excellent** (0.9+): Publication-ready, academic validation ready
- **🟡 Good** (0.8+): High quality, minor improvements beneficial
- **🟠 Acceptable** (0.7+): Functional, moderate improvements needed
- **🔴 Needs Improvement** (0.5+): Significant issues, substantial work required
- **💀 Unacceptable** (<0.5): Fundamental problems, complete redesign needed

## 📊 Development Analytics

### **Session Analytics**
```python
from src.narrative_gravity.development.session_manager import DevelopmentSessionManager

manager = DevelopmentSessionManager()

# Get analytics across all sessions
analytics = manager.get_session_analytics()
print(f"Total sessions: {analytics['total_sessions']}")
print(f"Success rate: {analytics['completed_sessions']/analytics['total_sessions']:.2%}")

# Component-specific analytics
prompt_analytics = manager.get_session_analytics("prompt_template")
framework_analytics = manager.get_session_analytics("framework")
```

### **Performance Tracking**
- **Coefficient of Variation**: Consistency across runs (target: <0.20)
- **Hierarchy Clarity Score**: Thematic distinction quality (target: >0.80)
- **Framework Fit Average**: Framework applicability (target: >0.75)
- **Evidence Quality Score**: Textual grounding strength (target: >0.85)

## 🔧 Integration with Priority 1

### **Seamless Component Creation**
Priority 2 development sessions integrate directly with Priority 1 component versioning:

```bash
# Development session creates refined component
python src/narrative_gravity/cli/log_iteration.py \
  --session-id $SESSION_ID \
  --version-created hierarchical_civic_virtue:v3.0

# Component automatically tracked in Priority 1 infrastructure
python src/narrative_gravity/cli/manage_components.py list prompt-templates
```

### **Component Matrix Integration**
Developed components automatically available for systematic validation:

```bash
# Components appear in matrix validation
python src/narrative_gravity/cli/analyze_batch.py validate-matrix \
  --config priority2_components_matrix.yaml
```

## 📚 Advanced Usage

### **Custom Seed Prompts**
```python
from src.narrative_gravity.development.seed_prompts import SeedPromptLibrary, ComponentType

library = SeedPromptLibrary()

# Get customized seed prompt
context = {
    'framework_name': 'Civic Virtue',
    'current_challenge': 'Inconsistent scoring distributions',
    'development_hypothesis': 'Evidence extraction improvements'
}

prompt = library.get_prompt(ComponentType.PROMPT_TEMPLATE, context)
```

### **Custom Quality Validators**
```python
from src.narrative_gravity.development.quality_assurance import ComponentQualityValidator

validator = ComponentQualityValidator()

# Validate with custom parameters
report = validator.validate_prompt_template(
    template_content=template_text,
    template_type="hierarchical",
    framework_context={'wells': ['dignity', 'justice', 'tribalism']}
)
```

### **Session Data Export**
```python
# Export complete session data for external analysis
export_path = manager.export_session_data(
    session_id="abc123-def456",
    export_path="exports/session_analysis.json"
)
```

## 🎓 Academic Integration

### **Publication Readiness**
Priority 2 tools support academic publication requirements:

- **Methodology Documentation**: Complete development process audit trail
- **Quality Validation**: Academic standard compliance verification
- **Reproducibility**: Systematic development workflow documentation
- **Performance Evidence**: Quantitative improvement validation

### **Validation Study Preparation**
```bash
# Generate academic-quality component with full documentation
python src/narrative_gravity/cli/start_dev_session.py \
  --component-type prompt_template \
  --name academic_validation_v1 \
  --hypothesis "Prepare prompt for human expert validation study"

# Complete quality validation
python src/narrative_gravity/cli/validate_component.py \
  --component-type prompt_template \
  --file academic_prompt.txt \
  --export-report academic_quality_report.json
```

## 🚀 Next Steps

Priority 2 provides the foundation for:
- **Priority 3**: Academic Tool Integration (R scripts, Jupyter notebooks)
- **Priority 4**: Human Validation Study Infrastructure
- **Priority 5**: Publication Support Tools

The systematic development workflows and quality assurance framework ensure that components developed through Priority 2 meet the rigorous standards required for academic validation and publication.

---

**For technical details:** See `src/narrative_gravity/development/` module documentation  
**For CLI reference:** Run any CLI tool with `--help`  
**For integration:** See Priority 1 infrastructure documentation 