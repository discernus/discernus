# Epic: CLI & Orchestrator Integration + Validation

## Overview
Complete the v8.0 implementation with full ThinOrchestrator integration, comprehensive testing, and validation using the `simple_test` experiment.

## Scope
This epic covers the final integration work and comprehensive validation that proves the v8.0 system works end-to-end.

## Key Deliverables

### **ThinOrchestrator Integration**
- [ ] **Notebook Generation Pipeline**
  - `_run_notebook_generation()` method in ThinOrchestrator
  - Replace `ProductionThinSynthesisPipeline` for `--statistical-prep` mode
  - Coordinate automated function generation agents
  - Integrate with universal template system

- [ ] **CLI Integration**
  - `--statistical-prep` flag fully operational
  - Integration with existing experiment validation
  - Backward compatibility with traditional synthesis mode
  - Clear user experience and error messaging

### **Comprehensive Testing & Validation**
- [ ] **simple_test Migration**
  - Convert `simple_test/experiment.md` to v8.0 format
  - Convert CFF v7.3 → v8.0 framework specification
  - Convert corpus specification to v8.0 format
  - End-to-end execution validation

- [ ] **Multi-Framework Testing**
  - Test with CAF (Civic Character Assessment Framework) 
  - Test with PDAF (Political Discourse Analysis Framework)
  - Validate framework-agnostic function generation
  - Cross-framework consistency validation

- [ ] **Academic Quality Validation**
  - Statistical rigor appropriate for 4-document analysis
  - Evidence integration linking findings to source texts
  - Transparency and reproducibility validation
  - Peer-review readiness assessment

### **Performance & Reliability**
- [ ] **Performance Benchmarks**
  - Complete pipeline execution <5 minutes
  - Function generation success rate >95%
  - Mathematical accuracy >99% vs reference
  - Notebook execution reliability validation

- [ ] **Integration Testing**
  - Full artifact storage and provenance integration
  - Dual-track logging validation
  - Security boundary enforcement
  - Git auto-commit functionality

## Success Criteria

### **Technical Success**
- [ ] `discernus run --statistical-prep` works end-to-end with `simple_test`
- [ ] Generated notebooks execute without errors
- [ ] All artifacts properly stored and tracked
- [ ] Complete audit trail preserved

### **Academic Quality** 
- [ ] **Statistical Rigor**: Appropriate tests for comparative analysis
- [ ] **Evidence Integration**: Clear links between statistics and textual evidence  
- [ ] **Transparency**: All calculations visible and modifiable
- [ ] **Reproducibility**: Notebook + data produces identical results

### **System Integration**
- [ ] **Provenance**: Complete audit trail from v8.0 specs → results
- [ ] **Logging**: Both development and research tracks operational
- [ ] **Security**: Proper isolation and boundary enforcement
- [ ] **Performance**: Meets established benchmarks

## Architectural Compliance
- [ ] Complete integration with established provenance system
- [ ] Full dual-track logging implementation
- [ ] Agent ecosystem properly classified and organized
- [ ] RAG system leveraged for evidence integration (Principle #22)

## Dependencies
- Phase 1, 2, and 3 must be complete
- All automated function generation agents operational
- Universal template system validated

## Estimate
**6-9 development days** (~600 lines new code, ~800 lines modifications, extensive testing)

## Definition of Done
- `simple_test` executes successfully in v8.0 mode
- Multi-framework testing validates framework-agnostic design
- Academic quality meets peer-review standards
- Performance benchmarks achieved
- Complete documentation and handoff
- All architectural compliance requirements met

## Strategic Impact
This epic delivers the complete v8.0 vision: **researchers provide simple markdown specifications, system automatically generates working research notebooks.**
