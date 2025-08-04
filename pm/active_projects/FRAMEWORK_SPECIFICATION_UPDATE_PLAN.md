# Framework Specification Update Plan
## Issue: Framework Specification Drift Causing Data Extraction Regression

**Status**: Analysis Complete - Ready for Implementation  
**Priority**: Critical (Blocking Alpha System validation)  
**Root Cause**: Framework specification v7.0 doesn't match working v7.1+ implementation

---

## **🚨 Problem Analysis**

### **Working Implementation (Large Batch Test)**
- **Framework**: PDAF v7.1 with enhanced gasket architecture
- **Data Format**: Flat keys (`populism_score`, `nationalism_score`, etc.)
- **Result**: ✅ Perfect data extraction, complete CSV generation
- **Evidence**: 341 artifacts organized, comprehensive statistical analysis

### **Broken Implementation (Simple Test)**
- **Framework**: CAF v7.0 with legacy gasket architecture
- **Data Format**: Nested structure (`dimensional_scores.Dignity.raw_score`)
- **Result**: ❌ Data extraction failure, missing CSV files
- **Evidence**: "Failed (0/5 tasks completed successfully)"

### **Specification Gap**
- **Current Spec**: Framework Specification v7.0 (legacy format)
- **Working Reality**: v7.1+ enhanced gasket architecture
- **Impact**: New experiments follow broken specification

---

## **📋 Implementation Strategy**

### **🔗 GitHub Issues Integration**
This plan aligns with existing GitHub issues:
- **Issue #285**: EPIC: Framework Specification v7.1 Upgrade and Migration
- **Issue #286**: Create Framework Specification v7.1 Document (THIS TASK)
- **Issue #288**: Migrate v7.0 Frameworks to v7.1 (includes CAF v7.0 → v7.1)

### **Phase 1: Complete Issue #286 - Framework Specification v7.1** ⏱️ 15 minutes
1. **Analyze Working PDAF v7.1**: Extract enhanced gasket architecture patterns
2. **Create Framework Specification v7.1**: Document enhanced gasket schema features
3. **Document Breaking Changes**: No backward compatibility with v5.0/v6.0/v7.0

### **Phase 2: Begin Issue #288 - CAF v7.0 → v7.1 Migration** ⏱️ 10 minutes  
1. **Create CAF v7.1**: Apply v7.1 gasket architecture to Character Assessment Framework
2. **Update Simple Test Experiment**: Point to new CAF v7.1 framework
3. **Maintain Analytical Integrity**: Preserve civic character methodology, upgrade only data extraction

### **Phase 3: Validation Testing** ⏱️ 10 minutes
1. **Rerun Simple Test**: Confirm data extraction works with v7.1 gasket
2. **Verify CSV Generation**: Ensure complete results export
3. **Close Issues**: Mark #286 complete, update progress on #285 and #288

---

## **🎯 Key Innovations to Standardize**

### **Enhanced Gasket Schema (from PDAF v7.1)**
```json
"enhanced_gasket_features": {
  "explicit_schema_mapping": true,
  "flat_key_extraction": true,
  "dimension_group_validation": true,
  "calculation_spec_integration": true
}
```

### **Improved Data Flow Architecture**
1. **Raw Analysis Log** → Natural human analysis (unchanged)
2. **Intelligent Extractor** → Enhanced schema mapping (IMPROVED)  
3. **Mathematical Processing** → Flat key validation (IMPROVED)
4. **CSV Export** → Complete artifact integration (FIXED)

---

## **📊 Expected Outcomes**

### **Immediate Fixes**
- ✅ Simple test data extraction regression resolved
- ✅ CSV generation restored for all experiments  
- ✅ Framework specification matches working implementation

### **Long-term Benefits**
- ✅ New experiments follow proven v7.1 architecture
- ✅ Consistent data extraction across all framework types
- ✅ Academic-grade provenance + reliable mathematical processing
- ✅ Framework authors have clear, working specification to follow

---

## **🚦 Implementation Readiness**

**Prerequisites Met**:
- ✅ Working v7.1 implementation identified and analyzed
- ✅ Root cause of regression confirmed
- ✅ Specification gap documented
- ✅ Clear migration path established

**Next Action**: Begin Phase 1 - Update Framework Specification v7.0 → v7.1