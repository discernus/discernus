# 🚀 Quick Start: Framework Specification v3.1 - Phase 3

**Date:** 2025-06-23  
**Your Mission:** Build validator and normalization tools for v3.1 frameworks  
**Status:** 7 frameworks successfully migrated ✅ → Ready for tooling  

## 🎯 What You're Building

### Priority 1: Framework Validator
**Location:** `experimental/prototypes/framework_validator_v3_1.py`  
**Purpose:** Validate all Framework Specification v3.1 compliance requirements  

**Key Features Needed:**
- `opposite_of` link validation (must be bidirectional)
- Angle conflict detection (allow legitimate 180° opposites like MFT)
- Version normalization (v1.01 → v1.1)
- Citation format checking ("Discernus Framework: Name vX.Y (Author, Year)")
- Clock position conversion (3 o'clock → 90°)

## 📁 Test Data Available

**All 7 frameworks ready for testing:**
```
research_workspaces/june_2025_research_dev_workspace/frameworks/
├── moral_foundations_theory/moral_foundations_theory_v1.0.yaml ✅
├── civic_virtue/civic_virtue_v1.0.yaml ✅  
├── iditi/iditi_v1.0.yaml ✅
├── lakoff/lakoff_v1.0.yaml ✅
├── entman/entman_v1.0.yaml ✅
├── populism_pluralism/populism_pluralism_v1.0.yaml ✅
└── business_ethics/business_ethics_v1.0.yaml ✅
```

## 🚨 Critical Rules - ALWAYS FOLLOW

### Rule 1: Search First
```bash
python3 scripts/applications/check_existing_systems.py "framework validator"
```

### Rule 2: Use Production Systems
- ✅ `LLMQualityAssuranceSystem` for quality validation
- ✅ `ComponentQualityValidator` for component validation  
- ✅ `QAEnhancedDataExporter` for academic export
- ❌ NEVER use `deprecated/` systems

### Rule 3: Build in Experimental
- ✅ Start in `experimental/prototypes/`
- ❌ NEVER create in `src/` directly

## 🔗 Essential Documents

**Full Context:** `research_workspaces/june_2025_research_dev_workspace/HANDOFF_DOCUMENTATION.md`  
**Framework Spec:** `docs_site/docs/specifications/Framework_Specification_v3.1.md`  
**Compliance Rules:** `ai_assistant_compliance_rules.md`  

## ⚠️Clock Position Mappings
```
12 o'clock = 0°     3 o'clock = 90°     6 o'clock = 180°     9 o'clock = 270°
1 o'clock = 30°     4 o'clock = 120°    7 o'clock = 210°     10 o'clock = 300°
2 o'clock = 60°     5 o'clock = 150°    8 o'clock = 240°     11 o'clock = 330°
```

## 🏁 Success Criteria

**Phase 3 Complete When:**
- [ ] All 7 frameworks pass validation without errors
- [ ] Version normalization working (v1.01 → v1.1)  
- [ ] Citation format validation functional
- [ ] Integration with existing systems tested
- [ ] Production deployment ready

## 💡 Development Setup

**Local Development:**
```bash
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

**Start Here:**
1. Read full handoff documentation
2. Study existing frameworks for patterns
3. Build validator incrementally in experimental/
4. Test against all 7 frameworks
5. Integrate with production systems

---

**Remember:** You're inheriting a well-structured project. The hard architectural work is done. Focus on building the tooling that makes v3.1 production-ready! 🎯 