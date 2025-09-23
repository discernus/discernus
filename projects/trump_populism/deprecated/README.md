# Deprecated Content Directory

## 📁 Directory Purpose
This directory contains files and scripts that have been **superseded by the new project structure** implemented after the adversarial review synthesis.

## 📋 Content Categories

### **extraction_scripts/**
**Status**: DEPRECATED - No longer needed
**Reason**: Outdated extraction scripts replaced by systematic corpus expansion framework
**Replacement**: `/corpus/expansion_targets/` with specific expansion plans
**Files**: 11 extraction scripts from previous attempts

### **redundant_manifests/**
**Status**: DEPRECATED - Superseded
**Reason**: Old corpus manifests replaced by comprehensive analysis-ready structure
**Replacement**: `/corpus/analysis_ready/manifest.json`
**Files**:
- `corpus_complete_manifest.json` - Superseded by analysis-ready manifest
- `corpus_manifest_yaml.txt` - Format changed to JSON for consistency

### **test_files/**
**Status**: DEPRECATED - Development artifacts
**Reason**: Test scripts from previous extraction attempts
**Replacement**: New extraction framework with integrated testing
**Files**: 5 test files from various extraction attempts

## 🚨 Important Notes

### **Do Not Use These Files**
- **Risk**: May contain outdated logic or broken dependencies
- **Impact**: Could interfere with current systematic expansion approach
- **Alternative**: Refer to `/docs/execution_guides/` for current methodology

### **Preservation Purpose**
- **Audit Trail**: Maintain historical record of development process
- **Reference**: May contain useful code snippets for future reference
- **Backup**: Preserved in case rollback is needed

## 📈 Migration Path

### **From Old Structure → New Structure**
```
OLD: archive/old_extraction_attempts/ → NEW: deprecated/extraction_scripts/
OLD: tests/ → NEW: deprecated/test_files/
OLD: Loose manifest files → NEW: deprecated/redundant_manifests/
```

### **Current Active Structure**
```
✅ ACTIVE: /corpus/analysis_ready/ (109 curated documents)
✅ ACTIVE: /corpus/expansion_targets/ (systematic expansion plans)
✅ ACTIVE: /docs/execution_guides/ (current methodology)
✅ ACTIVE: /runs/experiment_templates/ (execution configurations)
```

## 🔄 Deprecation Date
**Deprecated**: January 30, 2025
**Reason**: Adversarial review identified structural deficiencies requiring comprehensive restructure
**Replacement**: Systematic expansion framework with quality gates and methodological rigor

---

**For current project status, see**: `/docs/final_project_status.md`
**For expansion plans, see**: `/corpus/expansion_targets/`
