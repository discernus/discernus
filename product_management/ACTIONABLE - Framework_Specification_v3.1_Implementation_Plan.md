# ACTIONABLE - Framework Specification v3.1 Implementation Plan
**Date:** June 23, 2025  
**Priority:** HIGH - Critical Infrastructure Foundation  
**Estimated Duration:** 5 weeks  
**Strategic Goal:** Establish flexible, attribute-based framework architecture for academic research

## 🎯 **EXECUTIVE SUMMARY**

Implementation of Framework Specification v3.1 representing a fundamental shift from rigid framework types to flexible attribute-based architecture. This change enables researchers to innovate freely while maintaining system integrity through validation rather than constraints.

**Key Transformation:** `framework_type` constraints → **attribute presence = capability**

## 🚀 **STRATEGIC RATIONALE**

### **Why Now: Clean Break Opportunity**
- **No published research yet** - optimal time for breaking changes
- **Infrastructure phase** - can establish clean patterns from day 1
- **Avoid technical debt** - prevent carrying forward rigid constraints
- **Enable innovation** - researchers can create novel framework architectures

### **Core Architectural Shift**
```yaml
# OLD (v3.0): Rigid constraints
framework_type: axis_set  # Forces specific structure

# NEW (v3.1): Flexible composition  
axes: {...}              # If present: uses opposing anchor pairs
anchors: {...}           # If present: uses independent anchors
positioning_strategy: {...} # If present: uses complex clustering
```

## 📋 **IMPLEMENTATION PHASES**

### **Phase 1: Lock Down Specification (Week 1)**
**Goal:** Finalize Framework Specification v3.1 with all architectural decisions

#### **Day 1-2: Specification Finalization**
**Deliverable:** Complete Framework Specification v3.1
**Location:** `docs_site/docs/specifications/framework_specification_v3.1.md`

**Required Components:**
- [ ] **Attribute-based architecture** documented with validation logic
- [ ] **Flexible versioning** with auto-normalization specification
- [ ] **Mandatory citation format** requirements and examples
- [ ] **Angle validation** with `opposite_of` link support
- [ ] **Self-documentation** requirements and integration guidance
- [ ] **Clean slate migration** strategy and rationale

#### **Day 3-4: External Review Integration**
**Deliverable:** Specification updates based on external review feedback

**Key Additions:**
- [ ] **Auto-normalization behavior** for leading zeros in versions
- [ ] **Angle conflict resolution** with opposing pair allowances
- [ ] **Future-proofing elements** for extensibility
- [ ] **Migration safety measures** and validation requirements

#### **Day 5: Specification Lock-Down**
**Deliverable:** Approved final specification ready for implementation

**Completion Criteria:**
- [ ] All architectural decisions documented and approved
- [ ] Validation rules clearly specified with examples
- [ ] Migration strategy defined with safety measures
- [ ] Academic requirements documented with citation examples
- [ ] Framework examples provided for all architecture types

### **Phase 2: Framework Migration (Week 2)**
**Goal:** Update all existing frameworks to v3.1 compliance

#### **Framework Updates Required:**

**All Frameworks:**
- [ ] **Remove `framework_type` fields** - replaced by attribute presence
- [ ] **Add mandatory citation format** to description sections
- [ ] **Reset to v1.0 versions** with clean file naming convention
- [ ] **Integrate README content** into framework descriptions
- [ ] **Add `last_modified` timestamps** and registry keys

**Specific Framework Fixes:**
- [ ] **Moral Foundations Theory**: Add `opposite_of` links for Care/Harm, Fairness/Cheating axes
- [ ] **Business Ethics**: Convert `clustered_dipoles` to `positioning_strategy` structure
- [ ] **Civic Virtue**: Update axis structure and remove deprecated fields
- [ ] **All Frameworks**: Validate angle uniqueness rules

#### **File Naming Convention:**
```bash
# Standardized naming
moral_foundations_theory_v1.0.yaml
business_ethics_v1.0.yaml
civic_virtue_v1.0.yaml
populism_pluralism_v1.0.yaml
iditi_v1.0.yaml
```

#### **Migration Validation:**
- [ ] **Manual validation** of each framework against v3.1 specification
- [ ] **Angle conflict detection** - ensure no duplicate angles except legitimate opposites
- [ ] **Citation format validation** - verify all frameworks include proper attribution
- [ ] **Documentation completeness** - confirm self-documenting requirements met

### **Phase 3: Tooling Development (Weeks 3-4)**
**Goal:** Build validation and normalization infrastructure

#### **Week 3: Core Validator**
**Deliverable:** Framework Specification v3.1 Validator
**Location:** `src/utils/framework_validator_v3_1.py`

**Validator Components:**
```python
class FrameworkValidator:
    def validate_structure(self, framework):
        """Validate attribute-based architecture"""
        - At least one positioning method present
        - Required fields complete for each component
        - Cross-references valid
        
    def validate_angles(self, framework):
        """Validate angle assignments with opposite support"""
        - No duplicate angles except legitimate opposites
        - opposite_of links properly formed
        - All angles 0-359 degrees
        
    def validate_version(self, version):
        """Validate and normalize version format"""
        - Auto-normalize leading zeros: v1.01 → v1.1
        - Ensure proper dot notation format
        - Log normalization changes
        
    def validate_citations(self, framework):
        """Validate mandatory citation format"""
        - Citation format present in description
        - Follows required pattern
        - Includes framework name and version
```

#### **Week 4: System Integration Tools**
**Deliverable:** Migration and system integration utilities

**Migration Utilities:**
- [ ] **Framework upgrade script** - automated v3.0 → v3.1 conversion
- [ ] **Version normalization tool** - handles leading zero cleanup
- [ ] **Registry management** - composite key generation and mapping
- [ ] **Citation format injector** - adds mandatory citation strings

**System Updates:**
- [ ] **Framework loader** updated for attribute-based validation
- [ ] **Database schema** updated for composite keys
- [ ] **Run-time registration** system implementation

### **Phase 4: System Integration (Week 5)**
**Goal:** Deploy v3.1 architecture to production

#### **Database Migration:**
```sql
-- Clean slate migration
TRUNCATE framework_registry;
CREATE TABLE framework_registry_v3_1 (
    composite_key VARCHAR(255) PRIMARY KEY,  -- "name__version"
    name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    framework_yaml TEXT NOT NULL,
    first_successful_run TIMESTAMP,
    validation_status VARCHAR(50) DEFAULT 'production_validated',
    run_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### **System Testing:**
- [ ] **Framework loading** with new attribute-based system
- [ ] **Validation pipeline** testing with all framework types
- [ ] **Version normalization** testing with edge cases
- [ ] **Registry management** testing with composite keys
- [ ] **End-to-end workflow** validation

## 🔧 **KEY TECHNICAL DECISIONS**

### **1. Attribute-Based Architecture**
**Decision:** Remove `framework_type` field, use component presence for capability detection
**Rationale:** Real frameworks mix approaches; rigid types create artificial constraints
**Implementation:** Validator checks for at least one positioning method present

### **2. Version Auto-Normalization**
**Decision:** Automatically normalize leading zeros in version numbers
**Example:** `v1.01` → `v1.1` (with logging)
**Rationale:** Prevents citation ambiguity and database conflicts
**Implementation:** Normalize during framework upload with user notification

### **3. Angle Validation with Opposites**
**Decision:** Allow 180° opposites within same axis using `opposite_of` links
**Example:**
```yaml
integrative:
  angle: 0
  opposite_of: "Harm"
disintegrative:  
  angle: 180
  opposite_of: "Care"
```
**Rationale:** Legitimate opposing pairs shouldn't trigger conflict detection

### **4. Mandatory Citation Format**
**Decision:** Require standardized citation in all framework descriptions
**Format:** `"Discernus Framework: Framework Name v1.0 (Author, 2025)"`
**Rationale:** Ensures academic attribution and professional consistency

### **5. Clean Slate Migration**
**Decision:** Reset all frameworks to v1.0 with clean file naming
**Rationale:** No research published yet; optimal time for breaking changes
**Implementation:** Preserve functionality, reset versioning system

## ⚠️ **RISK MITIGATION**

### **High Risk: Breaking Changes**
**Risk:** All existing framework loaders will break
**Mitigation:** 
- Dual-load period during development
- Clear migration documentation
- Validator testing before deployment

### **Medium Risk: Framework Validation**
**Risk:** Complex frameworks may fail new validation rules
**Mitigation:**
- Manual validation of all existing frameworks
- `opposite_of` links for legitimate angle conflicts
- Comprehensive test suite

### **Low Risk: Version Normalization**
**Risk:** User confusion with auto-normalization
**Mitigation:**
- Clear logging of all changes
- User notification during upload
- Documentation with examples

## 📊 **SUCCESS METRICS**

### **Technical Metrics**
- [ ] **100% Framework Migration**: All existing frameworks v3.1 compliant
- [ ] **Zero Validation Failures**: All frameworks pass new validator
- [ ] **Clean Database**: Registry contains only production-validated frameworks
- [ ] **Consistent Versioning**: All versions properly normalized

### **Academic Metrics**
- [ ] **Mandatory Citations**: All frameworks include proper attribution
- [ ] **Self-Documentation**: All frameworks comprehensive and clear
- [ ] **Professional Consistency**: Standardized citation format across all work

### **System Metrics**
- [ ] **Attribute Flexibility**: Mixed framework architectures supported
- [ ] **Extensibility**: New framework types possible without breaking changes
- [ ] **Clean Architecture**: No technical debt from rigid constraints

## 🚀 **DELIVERABLES SUMMARY**

### **Documentation**
- [ ] **Framework Specification v3.1** - Complete architectural specification
- [ ] **Migration Guide** - Step-by-step upgrade instructions
- [ ] **Validation Documentation** - Validator usage and requirements

### **Code**
- [ ] **Framework Validator v3.1** - Comprehensive validation system
- [ ] **Migration Utilities** - Automated upgrade and normalization tools
- [ ] **Updated System Code** - Attribute-based loading and validation

### **Frameworks**
- [ ] **All Frameworks v1.0** - Clean, v3.1-compliant framework files
- [ ] **Registry Database** - Clean slate with proper composite keys
- [ ] **Validation Test Suite** - Comprehensive framework testing

## 🎯 **NEXT STEPS**

### **Immediate Actions (This Week)**
1. **Complete Framework Specification v3.1** with all design decisions
2. **Review and approve** final specification
3. **Begin framework migration planning**

### **Week 2 Priorities**
1. **Migrate all existing frameworks** to v3.1 compliance
2. **Validate framework alignment** with new specification
3. **Prepare for tooling development**

### **Success Gateway**
**Phase 1 Complete When:** Framework Specification v3.1 is approved and locked down
**Phase 2 Complete When:** All frameworks are v3.1 compliant and validated
**Phase 3 Complete When:** Validator and migration tools are production-ready
**Phase 4 Complete When:** System is running v3.1 architecture in production

---

**Plan Author:** AI Assistant  
**Approval Required:** Product Owner  
**Implementation Start:** Upon specification lock-down  
**Target Completion:** July 28, 2025  
**Strategic Impact:** Foundation for all future framework innovation 