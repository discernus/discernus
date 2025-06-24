# Framework Specification v3.1 Project Handoff Documentation

**Date:** 2025-06-23  
**Phase:** Transition from Phase 2 (Framework Migration) to Phase 3 (Validator & Tools)  
**Status:** Ready for Phase 3 Implementation  

## 🎯 Project Overview

The **Framework Specification v3.1** project revolutionizes the Discernus framework architecture with a **clean slate approach** that eliminates rigid framework types in favor of flexible, attribute-based architecture. All core frameworks have been successfully migrated to v3.1 compliance.

### Key Architectural Changes
- **Eliminated rigid framework_type field** → Attribute-based capabilities
- **Flexible positioning system** → Mixed degrees/clock positions supported
- **Enhanced validation** → `opposite_of` links for angle validation
- **Academic integration** → Self-documenting with integrated README content
- **Clean versioning** → All frameworks reset to v1.0 for fresh start

## ✅ COMPLETED WORK

### Phase 1: Specification Development (COMPLETE)
- **Framework Specification v3.1** finalized and documented
- **Innovation**: Clock face positioning (3 o'clock = 90°, 6 o'clock = 180°, etc.)
- **Revolutionary architecture**: Frameworks define capabilities through component presence
- **Location**: `docs_site/docs/specifications/Framework_Specification_v3.1.md`

### Phase 2: Framework Migration (COMPLETE)
All 7 frameworks successfully migrated to v3.1 compliance:

#### 1. **Moral Foundations Theory v1.0** ✅
- **Location**: `research_workspaces/june_2025_research_dev_workspace/frameworks/moral_foundations_theory/moral_foundations_theory_v1.0.yaml`
- **Architecture**: 6 axes (Care↔Harm, Fairness↔Cheating, Loyalty↔Betrayal, Authority↔Subversion, Sanctity↔Degradation, Liberty↔Oppression)
- **Citation**: "Discernus Framework: Moral Foundations Theory v1.0 (Haidt, 2025)"
- **Key Fix**: Resolved angle conflicts from old framework

#### 2. **Civic Virtue v1.0** ✅
- **Location**: `research_workspaces/june_2025_research_dev_workspace/frameworks/civic_virtue/civic_virtue_v1.0.yaml`
- **Architecture**: 10 anchors with clustering (5 virtues @ 90°, 5 vices @ 270°)
- **Citation**: "Discernus Framework: Civic Virtue v1.0 (Aristotle/Sandel, 2025)"
- **Key Achievement**: Restored complete 10-anchor structure from degraded 2-anchor version

#### 3. **IDITI v1.0** ✅
- **Location**: `research_workspaces/june_2025_research_dev_workspace/frameworks/iditi/iditi_v1.0.yaml`
- **Architecture**: Simple binary (Dignity ↔ Tribalism)
- **Citation**: "Discernus Framework: Individual Dignity Identity v Tribal Identity v1.0 (Fukuyama/Jung, 2025)"

#### 4. **Lakoff v1.0** ✅
- **Location**: `research_workspaces/june_2025_research_dev_workspace/frameworks/lakoff/lakoff_v1.0.yaml`
- **Architecture**: Arc clustering (Strict Father 315°-45° vs Nurturant Parent 135°-225°)
- **Citation**: "Discernus Framework: Lakoff Family Models v1.0 (Lakoff, 2025)"

#### 5. **Entman v1.0** ✅
- **Location**: `research_workspaces/june_2025_research_dev_workspace/frameworks/entman/entman_v1.0.yaml`
- **Architecture**: 4 independent anchors (90° spacing)
- **Citation**: "Discernus Framework: Entman Framing Functions v1.0 (Entman, 2025)"

#### 6. **Populism vs Pluralism v1.0** ✅
- **Location**: `research_workspaces/june_2025_research_dev_workspace/frameworks/populism_pluralism/populism_pluralism_v1.0.yaml`
- **Architecture**: Binary (Pluralism ↔ Populism)
- **Citation**: "Discernus Framework: Populism vs Pluralism v1.0 (Müller/Urbinati, 2025)"

#### 7. **Business Ethics v1.0** ✅
- **Location**: `research_workspaces/june_2025_research_dev_workspace/frameworks/business_ethics/business_ethics_v1.0.yaml`
- **Architecture**: 5 axes with domain clustering
- **Citation**: "Discernus Framework: Business Ethics v1.0 (Freeman/Solomon, 2025)"

### Additional Completed Work
- **Test Framework Updated** ✅: `tests/system_health/frameworks/moral_foundations_theory/moral_foundations_theory_framework.yaml` updated to match v3.1 structure
- **README Files Integrated**: All framework README content integrated into YAML descriptions
- **Clean Slate Versioning**: All frameworks reset to v1.0 for fresh start

## 📋 NEXT STEPS - Phase 3: Validator & Tools Development

### Priority 1: Framework Validator
**Objective**: Build comprehensive validator for Framework Specification v3.1 compliance

**Implementation Location**: `experimental/prototypes/framework_validator_v3_1.py`

**Key Requirements**:
- Validate `opposite_of` links (must be bidirectional)
- Angle validation (allow legitimate 180° opposites like MFT pairs)
- Version normalization (v1.01 → v1.1, remove leading zeros)
- Citation format validation ("Discernus Framework: Name vX.Y (Author, Year)")
- Clock position conversion (3 o'clock → 90°)
- Required fields verification
- Academic validation requirements

**Reference Implementation**: Study existing frameworks for validation patterns

### Priority 2: Framework Normalization Tools
**Objective**: Automate framework cleanup and standardization

**Features Needed**:
- Auto-normalize version numbers
- Standardize positioning formats
- Validate and repair `opposite_of` links
- Generate framework registry keys
- Academic citation format enforcement

### Priority 3: Integration Testing
**Objective**: Ensure all frameworks work with existing systems

**Test Coverage**:
- `LLMQualityAssuranceSystem` compatibility
- `ComponentQualityValidator` integration
- `QAEnhancedDataExporter` export functionality
- Visualization system compatibility
- `comprehensive_experiment_orchestrator.py` integration

### Priority 4: System Integration
**Objective**: Deploy v3.1 frameworks to production pipeline

**Integration Points**:
- Update framework loading logic
- Ensure backward compatibility where needed
- Update documentation and user guides
- Production deployment validation

## 🔧 TECHNICAL DETAILS

### Framework Architecture Patterns
Based on completed migrations, frameworks follow these patterns:

1. **Binary Frameworks**: Single axis with two opposites (IDITI, Populism vs Pluralism)
2. **Multi-Axis Frameworks**: Multiple opposing pairs (MFT with 6 axes, Business Ethics with 5 axes)
3. **Clustered Anchor Frameworks**: Independent anchors with clustering (Civic Virtue, Entman)
4. **Arc Clustering Frameworks**: Hypothesis-driven positioning (Lakoff)

### Critical Technical Decisions Made

1. **Clean Slate Versioning**: All frameworks reset to v1.0 (no migration path needed since no research published yet)
2. **Flexible Positioning**: Mixed degrees/clock positions supported within same framework
3. **Attribute-Based Architecture**: Capabilities defined by component presence, not rigid types
4. **Opposite_of Validation**: Critical for angle validation and framework integrity

### Clock Position Mappings
```
12 o'clock = 0°     3 o'clock = 90°     6 o'clock = 180°     9 o'clock = 270°
1 o'clock = 30°     4 o'clock = 120°    7 o'clock = 210°     10 o'clock = 300°
2 o'clock = 60°     5 o'clock = 150°    8 o'clock = 240°     11 o'clock = 330°
```

## 📚 KEY DOCUMENTATION LINKS

### Specifications
- **Framework Specification v3.1**: `docs_site/docs/specifications/Framework_Specification_v3.1.md`
- **AI Assistant Compliance Rules**: `ai_assistant_compliance_rules.md`

### Production Systems (ALWAYS USE THESE)
- **Quality Assurance**: `src/analysis/llm_quality_assurance_system.py`
- **Component Validation**: `src/utils/component_quality_validator.py`
- **Data Export**: `src/academic/qa_enhanced_data_exporter.py`
- **Experiment Orchestration**: `scripts/applications/comprehensive_experiment_orchestrator.py`

### Framework Locations
- **All Migrated Frameworks**: `research_workspaces/june_2025_research_dev_workspace/frameworks/`
- **Test Framework**: `tests/system_health/frameworks/moral_foundations_theory/`

### Project Management
- **Implementation Plan**: `product_management/ACTIONABLE - Framework_Specification_v3.1_Implementation_Plan.md`
- **Change Tracking**: `CHANGELOG.md` (use search_replace for updates)

## 🚨 CRITICAL COMPLIANCE RULES

### Rule 1: ALWAYS Search Production Systems First
Before building anything new, run:
```bash
python3 scripts/applications/check_existing_systems.py "functionality description"
```

### Rule 2: NEVER Use Deprecated Systems
- ❌ NEVER use `deprecated/` directory code
- ❌ NEVER mention "AI Academic Advisor" 
- ❌ NEVER use `architectural_compliance_validator.py`

### Rule 3: ALWAYS Use Production Systems
- ✅ USE: `LLMQualityAssuranceSystem` for validation
- ✅ USE: `ComponentQualityValidator` for component validation
- ✅ USE: `QAEnhancedDataExporter` for academic export

### Rule 4: Build in Experimental First
- ✅ New development starts in `experimental/prototypes/`
- ❌ NEVER create files directly in `src/` without experimental testing

## 🎯 SUCCESS CRITERIA FOR PHASE 3

### Validator Success Metrics
- [ ] All 7 frameworks pass validation without errors
- [ ] Angle conflicts properly detected and reported
- [ ] Version normalization working correctly
- [ ] Citation format validation functional
- [ ] Clock position conversion accurate

### Integration Success Metrics
- [ ] All frameworks load correctly in production systems
- [ ] Experiment orchestrator runs without framework errors
- [ ] Quality assurance system validates all frameworks
- [ ] Export system handles all framework types
- [ ] Visualization system renders all frameworks correctly

## 🔄 DEVELOPMENT WORKFLOW

1. **Plan First**: User prefers strategic discussion before implementation
2. **Local Development**: Use `python3 -m venv venv`, no Docker
3. **Experimental Prototyping**: Build in `experimental/prototypes/` first
4. **Production Integration**: Move to `src/` only after experimental validation
5. **System Validation**: Use existing quality assurance systems

## 💡 KEY INSIGHTS FOR NEW COLLABORATOR

### What Worked Well
- **Clean slate approach**: No legacy constraints since no research published
- **Mixed positioning**: Degrees + clock positions provide flexibility
- **Attribute-based architecture**: Much more flexible than rigid types
- **Integrated documentation**: Self-documenting frameworks reduce maintenance

### Potential Challenges
- **Angle validation complexity**: Need to allow legitimate 180° opposites
- **Version normalization edge cases**: Handle various input formats
- **Integration testing**: Many existing systems to validate against
- **Academic validation**: Citation format enforcement critical

### Success Strategies
- **Start with existing frameworks**: Use migrated frameworks as validation test cases
- **Incremental development**: Build validator piece by piece
- **Comprehensive testing**: Use system health tests throughout
- **Follow compliance rules**: Prevents rebuilding existing functionality

---

**Next Collaborator**: You're inheriting a well-structured project with clear specifications and successfully migrated frameworks. Focus on building the validator and normalization tools to complete the v3.1 implementation. The foundation is solid - now it's time to build the tooling that makes it production-ready.

**Contact**: All technical decisions and architectural choices are documented. Follow the compliance rules, use existing production systems, and build incrementally in experimental first. 