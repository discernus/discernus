# Epic: v8.0 Specification Infrastructure

## Overview
Implement the foundational v8.0 specification parsers and infrastructure that enable natural language framework definitions and simple experiment configurations.

## Scope
This epic covers the core parsing and loading infrastructure needed to handle v8.0's simplified specifications.

## Key Deliverables
- [ ] **V8 Framework Parser** (`discernus/core/v8_specifications.py`)
  - Parse natural language calculation descriptions from v8.0 frameworks
  - Extract dimensions and research purpose semantically
  - Convert plain English formulas to structured requirements

- [ ] **V8 Experiment Loader** 
  - Load 4-field v8.0 experiment specifications (name, description, framework, corpus)
  - Handle optional research questions
  - Maintain backward compatibility detection

- [ ] **V8 Corpus Handler**
  - Load corpus with flexible metadata naming
  - Handle semantic understanding (`author`, `speaker`, `person` as synonyms)
  - Support missing metadata tolerance

- [ ] **CLI Integration**
  - Add `--statistical-prep` flag to production CLI
  - Integrate v8.0 validation in experiment structure checking
  - Maintain existing functionality for v7.3 experiments

- [ ] **Security Boundary Updates**
  - Add v8.0 specification validation
  - Ensure experiment path validation works with new formats
  - Maintain isolation requirements

## Success Criteria
- [ ] CLI `discernus run --statistical-prep` flag operational
- [ ] v8.0 specifications can be parsed without errors
- [ ] Backward compatibility maintained for existing v7.3 experiments
- [ ] Security and audit logging integration complete

## Architectural Compliance
- [ ] All new components follow THIN architecture (≤150 lines)
- [ ] Complete integration with dual-track logging system
- [ ] Full provenance tracking for all new artifacts
- [ ] Agent classification fits existing 6-layer model

## Dependencies
- Core ThinOrchestrator must be enhanced with notebook generation mode
- Existing security and audit systems must be extended

## Estimate
**5-7 development days** (~800 lines new code, ~400 lines modifications)

## Definition of Done
- All deliverables complete and tested
- `simple_test` experiment can be loaded and validated in v8.0 format
- Integration tests pass
- Documentation updated
- Code review completed
