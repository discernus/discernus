# Epic: Universal Notebook Template System

## Overview
Implement the universal notebook template engine that creates framework-agnostic research notebooks from auto-generated functions.

## Scope
This epic covers the template system that ties together all generated functions into executable, academic-quality research notebooks.

## Key Deliverables
- [ ] **Universal Notebook Template Engine** (`discernus/core/universal_notebook_template.py`)
  - Single template works for ANY v8.0 framework specification
  - Automatically imports and calls generated functions
  - Framework-agnostic data handling and orchestration
  - Never requires modification for different frameworks

- [ ] **Notebook Executor & Validation** (`discernus/core/notebook_executor.py`)
  - Pre-validate notebooks before delivery
  - Execute notebooks in sandboxed environment
  - Capture execution results and errors
  - Provide detailed execution reports

- [ ] **Template Enhancement for v8.0**
  - Enhanced template processing for v8.0 experiment specifications
  - Flexible corpus metadata handling
  - Automatic statistical analysis discovery
  - Research questions integration

- [ ] **Data Externalization Architecture**
  - Solve LLM truncation problems through external data files
  - `analysis_data.json` + `generated_functions.py` pattern
  - Efficient data loading without context window limits
  - Academic transparency through external data files

## Key Innovation
**The Universal Template Breakthrough**: One template + automatically generated functions = works for any framework without customization.

```python
# BEFORE: MathToolkit approach (problematic)
result = eval(formula, safe_dict)  # Runtime parsing - breaks frequently

# AFTER: Universal Template approach (reliable) 
result = functions_module.calculate_identity_tension(tribal_score, dignity_score, ...)  # Direct call
```

## Success Criteria
- [ ] **Framework Agnostic**: Same template works for CFF, CAF, PDAF, any v8.0 framework
- [ ] **Notebook Execution**: Generated notebooks run without errors
- [ ] **Academic Quality**: Notebooks meet peer-review standards
- [ ] **Data Externalization**: Handles large datasets without LLM truncation
- [ ] **Validation Pipeline**: Comprehensive pre-execution testing

## Architectural Compliance
- [ ] Template system integrates with existing artifact storage
- [ ] Complete provenance tracking for generated notebooks
- [ ] Dual-track logging for template generation and execution
- [ ] Security boundary enforcement for notebook execution
- [ ] Integration with existing audit systems

## Dependencies
- Phase 2 (Automated Function Generation) must be complete
- Generated functions must be available as inputs
- ThinOrchestrator integration for template orchestration

## Estimate
**4-6 development days** (~600 lines new code, ~300 lines modifications)

## Definition of Done
- Universal template engine operational
- Notebook validation system complete
- Template works with CFF, CAF, PDAF frameworks
- Data externalization architecture proven
- Integration testing passes for multiple framework types
- Performance meets requirements (notebook generation <2 minutes)
