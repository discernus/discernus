# Epic: Automated Function Generation Agents

## Overview
Implement the core innovation of v8.0: specialized agents that automatically generate Python calculation functions from natural language framework descriptions.

## Scope
This epic covers the four automated function generation agents that form the heart of the v8.0 notebook architecture.

## Key Deliverables
- [ ] **AutomatedDerivedMetricsAgent**
  - Generate calculation functions from v8.0 natural language descriptions
  - Handle dependency resolution automatically
  - Support CFF, CAF, PDAF frameworks without modification
  - Mathematical validation and error handling

- [ ] **AutomatedStatisticalAnalysisAgent**
  - Generate appropriate statistical analysis functions based on data structure
  - Auto-select statistical tests (t-tests, ANOVA, correlations)
  - Adapt to actual sample sizes and data characteristics
  - Produce structured, machine-readable results

- [ ] **AutomatedEvidenceIntegrationAgent**
  - Generate functions linking statistical findings to qualitative evidence
  - Integrate with existing ComprehensiveKnowledgeCurator RAG system
  - Implement Principle #22 (Epistemic Trust) requirements
  - Support cross-domain reasoning capabilities

- [ ] **AutomatedVisualizationAgent**
  - Generate publication-ready visualization functions
  - Create academic-quality charts, graphs, and tables
  - Adapt visualizations to results structure automatically
  - Support customizable output formats

- [ ] **Function Validation System** (`discernus/core/function_validation.py`)
  - Syntax validation using AST parsing
  - Execution validation with sample data
  - Mathematical correctness verification
  - Integration testing between generated functions

## Success Criteria
- [ ] **95%+ Function Generation Success Rate**: Generated functions execute without syntax errors
- [ ] **99%+ Mathematical Accuracy**: Results match reference implementations
- [ ] **Framework Agnostic**: Same agents work with CFF, CAF, PDAF without modification
- [ ] **Natural Language Processing**: "Tension between hope and fear" → working Python function
- [ ] **Error Recovery**: Graceful handling of edge cases and missing data

## Architectural Compliance
- [ ] All agents have externalized YAML prompts
- [ ] Agents are experiment-agnostic and framework-agnostic
- [ ] Complete instrumentation for dual-track logging
- [ ] Integration with existing audit and security systems
- [ ] RAG integration leverages existing txtai infrastructure

## Dependencies
- Phase 1 (v8.0 Specification Infrastructure) must be complete
- Existing ComprehensiveKnowledgeCurator for RAG integration
- ThinOrchestrator notebook generation pipeline hooks

## Estimate
**8-10 development days** (~1200 lines new code, ~200 lines modifications)

## Definition of Done
- All four automated agents implemented and tested
- Function validation system operational
- Integration with existing RAG system complete
- Natural language → Python conversion working for CFF calculations
- Cross-model consistency validated (Flash vs Pro)
- Performance benchmarks meet requirements (<5 minutes total generation)
