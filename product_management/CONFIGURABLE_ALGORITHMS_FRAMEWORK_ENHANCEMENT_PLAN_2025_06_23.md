# Configurable Algorithms & Framework Enhancement Plan
**Date:** June 23, 2025  
**Priority:** HIGH - Critical architectural enhancement  
**Estimated Duration:** 2-3 weeks  
**Dependencies:** Framework specification updates → Visualization migration  

## 🎯 **EXECUTIVE SUMMARY**

Implementation of configurable algorithms in Discernus coordinate engine to replace hardcoded parameters and properly document the LLM-prompting-amplification methodological interaction. This enhancement enables researchers to customize algorithmic parameters for different frameworks, research contexts, and methodological approaches while maintaining transparency and reproducibility.

## 🚨 **CRITICAL ISSUES IDENTIFIED**

### **Issue 1: Hardcoded Algorithm Parameters**
Current implementation has non-configurable parameters:
- Dominance amplification threshold: `0.7` (hardcoded)
- Dominance amplification multiplier: `1.1` (hardcoded)  
- Adaptive scaling range: `0.65-0.95` (hardcoded)
- Variance/mean sensitivity factors (hardcoded)

**Impact**: Researchers cannot adapt algorithms to different frameworks or research contexts.

### **Issue 2: Undocumented LLM-Mathematical Interaction**
The dominance amplification system represents a sophisticated **LLM-prompting-amplification pipeline**:

1. **LLM Prompting**: Instructions to identify hierarchical dominance patterns
2. **Mathematical Amplification**: Algorithmic enhancement of high scores (>0.7)
3. **Visualization Representation**: Display of combined assessment

**Impact**: Methodological sophistication is hidden; researchers unaware of the integrated approach.

### **Issue 3: Deprecated JSON Framework Support**
Coordinate engine still supports deprecated JSON framework loading despite YAML-only migration.

**Impact**: Technical debt and inconsistent framework architecture.

## 📋 **IMPLEMENTATION STRATEGY**

### **Sequencing Decision: Algorithms First → Visualization Migration**

**Rationale**: Algorithm changes affect visualization requirements, so mathematical foundation must be established first.

### **Phase 1: Configurable Algorithms Implementation (2-3 weeks)**
1. Framework specification enhancement
2. YAML schema design for algorithm configuration  
3. Coordinate engine refactoring
4. Methodological documentation
5. Researcher guidance documentation

### **Phase 2: Visualization Migration (1 week)**
6. Extract matplotlib from test code
7. Migrate to production Plotly system
8. Integrate with finalized configurable algorithms
9. Academic output enhancements

## 🔧 **DETAILED IMPLEMENTATION PLAN**

### **Week 1: Framework Specification & Documentation**

#### **Day 1-2: Methodological Documentation**
- **Deliverable**: Comprehensive documentation of LLM-prompting-amplification interaction
- **Location**: `docs_site/docs/specifications/configurable_algorithms_methodology.md`
- **Content**:
  - Theoretical foundation for dominance amplification
  - LLM prompting strategies for dominance identification
  - Mathematical enhancement rationale
  - Integration methodology
  - When researchers should adjust parameters

#### **Day 3-4: YAML Schema Design**
- **Deliverable**: Extended framework YAML schema with algorithm configuration
- **Location**: Framework specification updates
- **Schema Addition**:
```yaml
algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.7           # Configurable threshold
    multiplier: 1.1          # Configurable multiplier
    rationale: "Enhances LLM-identified dominant themes"
  
  adaptive_scaling:
    enabled: true
    base_scaling: 0.65       # Minimum scaling factor
    max_scaling: 0.95        # Maximum scaling factor
    variance_factor: 0.3     # Variance sensitivity
    mean_factor: 0.1         # Mean sensitivity
    methodology: "Optimizes boundary utilization"
    
  prompting_integration:
    dominance_instruction: "Identify hierarchical dominance patterns"
    amplification_purpose: "Mathematical enhancement of identified dominance"
```

#### **Day 5: Framework Specification Document Update**
- **Deliverable**: Updated framework specification document
- **Location**: `docs_site/docs/specifications/framework_specification_v3.md`
- **Content**: Complete specification including algorithm configuration section

### **Week 2: Coordinate Engine Implementation**

#### **Day 1-2: Algorithm Configuration Loading**
- **Files Modified**: 
  - `src/coordinate_engine.py`
  - New: `src/utils/algorithm_config_loader.py`
- **Features**:
  - Load algorithm config from YAML frameworks
  - Backward-compatible defaults for existing frameworks
  - Validation of algorithm parameter ranges
  - Error handling for malformed configurations

#### **Day 3-4: Configurable Algorithm Implementation**
- **Files Modified**: `src/coordinate_engine.py`
- **Features**:
  - Configurable `apply_dominance_amplification()`
  - Configurable `calculate_adaptive_scaling()`
  - Parameter validation and range checking
  - Algorithm enable/disable functionality
  - Logging of applied algorithm parameters

#### **Day 5: JSON Framework Deprecation**
- **Files Modified**: `src/coordinate_engine.py`
- **Changes**:
  - Remove `_load_framework_config()` method
  - Update constructor to require YAML frameworks
  - Add migration guidance for JSON users
  - Update error messages and documentation

### **Week 3: Integration & Documentation**

#### **Day 1-2: Cross-System Integration**
- **Files Modified**:
  - `src/prompts/moral_foundations_analysis.py` (or equivalent)
  - `src/utils/llm_quality_assurance.py`
  - `scripts/production/comprehensive_experiment_orchestrator.py`
- **Features**:
  - Update prompting templates to reference algorithm configuration
  - QA validation of algorithm parameters
  - Experiment execution with configurable algorithms
  - Algorithm parameter logging in run metadata

#### **Day 3-4: Researcher Documentation**
- **Deliverable**: Comprehensive researcher guidance
- **Location**: `docs_site/docs/user-guides/configuring_algorithms.md`
- **Content**:
  - When to adjust algorithm parameters
  - Framework-specific recommendations
  - Methodological implications of parameter changes
  - Academic reporting guidelines
  - Example configurations for common research scenarios

#### **Day 5: Testing & Validation**
- **Files Created**:
  - `tests/unit/test_configurable_algorithms.py`
  - `tests/integration/test_algorithm_framework_integration.py`
- **Features**:
  - Unit tests for all configurable parameters
  - Integration tests with different framework configurations
  - Validation of backward compatibility
  - Performance benchmarking

## 📊 **EXPECTED OUTCOMES**

### **Research Benefits**
1. **Framework Flexibility**: Algorithms can be tailored to different theoretical frameworks
2. **Methodological Studies**: Researchers can study algorithm sensitivity and impact
3. **Cross-Framework Research**: Consistent methodology across different analytical approaches
4. **Publication Transparency**: Algorithm parameters explicitly documented and reportable

### **Technical Benefits**
1. **Architectural Consistency**: YAML-only framework architecture
2. **Code Maintainability**: Removal of deprecated JSON support
3. **Configuration Management**: Centralized algorithm configuration
4. **Documentation Quality**: Clear methodological documentation

### **Academic Benefits**
1. **Methodological Rigor**: Explicit documentation of LLM-mathematical integration
2. **Reproducibility**: Algorithm parameters explicitly configurable and reportable
3. **Transparency**: Clear understanding of computational methodology
4. **Flexibility**: Adaptation to different research contexts and requirements

## 🔍 **VALIDATION CRITERIA**

### **Technical Validation**
- [ ] All algorithm parameters configurable via YAML
- [ ] Backward compatibility maintained for existing frameworks
- [ ] JSON framework support completely removed
- [ ] Algorithm parameter validation working
- [ ] Performance impact < 5% increase in processing time

### **Documentation Validation**
- [ ] Complete methodological documentation published
- [ ] Researcher guidance documentation complete
- [ ] Framework specification updated
- [ ] All parameter options documented with examples
- [ ] Academic reporting guidelines provided

### **Integration Validation**
- [ ] Experiment execution uses configurable algorithms
- [ ] QA system validates algorithm configurations
- [ ] Algorithm parameters logged in run metadata
- [ ] Prompting templates reference algorithm configuration
- [ ] Visualizations reflect configured algorithm parameters

## 🚦 **RISK ASSESSMENT**

### **High Risk**
- **Breaking Changes**: Algorithm parameter changes could affect existing experiment reproducibility
- **Mitigation**: Provide exact backward-compatible defaults and migration guidance

### **Medium Risk**
- **Complexity**: Algorithm configuration adds complexity to framework specification
- **Mitigation**: Provide clear documentation and sensible defaults

### **Low Risk**
- **Performance**: Additional configuration loading could impact performance
- **Mitigation**: Cache configurations and optimize loading

## 📝 **SUCCESS METRICS**

1. **Configurability**: 100% of algorithm parameters configurable
2. **Documentation**: Complete methodological documentation published
3. **Compatibility**: Zero breaking changes for existing experiments with defaults
4. **Testing**: >95% test coverage for new configuration functionality
5. **Performance**: <5% performance impact from configuration loading

## 🎯 **POST-IMPLEMENTATION: VISUALIZATION MIGRATION**

After configurable algorithms are complete, proceed with visualization migration:
1. Extract matplotlib code from `tests/system_health/test_system_health.py`
2. Migrate smart label positioning to production Plotly system
3. Integrate foundation radar charts with configurable algorithms
4. Enhance academic output pipeline with algorithm parameter documentation
5. Clean up test code to use production visualization APIs

## 📚 **DELIVERABLES SUMMARY**

### **Documentation**
- [ ] `docs_site/docs/specifications/configurable_algorithms_methodology.md`
- [ ] `docs_site/docs/specifications/framework_specification_v3.md` 
- [ ] `docs_site/docs/user-guides/configuring_algorithms.md`

### **Code**
- [ ] Enhanced `src/coordinate_engine.py` with configurable algorithms
- [ ] New `src/utils/algorithm_config_loader.py`
- [ ] Updated prompting and QA integration
- [ ] Comprehensive test suite

### **Process**
- [ ] Updated experiment execution with algorithm configuration
- [ ] Enhanced academic output with algorithm documentation
- [ ] Migration guidance for existing JSON frameworks

---

**Plan Author**: AI Assistant  
**Approval Required**: Product Owner  
**Implementation Start**: Upon approval  
**Target Completion**: July 14, 2025  
**Next Phase**: Visualization Migration Plan 