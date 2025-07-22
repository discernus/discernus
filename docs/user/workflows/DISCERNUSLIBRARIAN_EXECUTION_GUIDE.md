# DiscernusLibrarian Execution Guide

**IMPORTANT**: This guide provides the **ONLY CORRECT WAY** to run DiscernusLibrarian for literature research.

## ✅ CORRECT Execution Method

```bash
# From the project root directory (/Volumes/code/discernus/)
python3 -m discernus.core.discernuslibrarian
```

**Requirements:**
- Must be run from the project root directory
- Uses the built-in test question and research methodology
- Generates proper reports in `discernus/librarian/reports/` and `discernus/librarian/research_data/`

## ❌ INCORRECT Methods (DO NOT USE)

```bash
# BROKEN - Will not work
python3 discernus/dev_tools/dev_test_runner.py --test-discernuslibrarian

# BROKEN - Module path issues
python3 discernus/core/discernuslibrarian.py
```

## 🎯 What DiscernusLibrarian Does

When executed correctly, DiscernusLibrarian will:

1. **Multi-Stage Validation Process**:
   - Phase 0: LLM Strategic Intelligence
   - Phase 1: Systematic Research Planning  
   - Phase 2: Multi-Stage Research Validation
   - Phase 3: Counter-research & Fact-checking
   - Phase 4: Completeness Gap Analysis

2. **Generate Two Output Files**:
   - **Human-readable report**: `discernus/librarian/reports/discernus_librarian_report_YYYYMMDD_HHMMSS.md`
   - **JSON data**: `discernus/librarian/research_data/discernus_librarian_data_YYYYMMDD_HHMMSS.json`

3. **Research Quality Features**:
   - 8-15 peer-reviewed studies analyzed per question
   - Rigorous citation verification and fact-checking
   - Counter-evidence integration
   - Confidence scoring with explicit uncertainty quantification
   - Complete research provenance

## 🚨 Common Agent Errors

**Error**: "ModuleNotFoundError: No module named 'discernus'"
**Solution**: Make sure you're running from the project root directory and using the module syntax

**Error**: Trying to use dev_test_runner.py 
**Solution**: Use the direct module execution method instead

**Error**: Looking for command-line arguments
**Solution**: DiscernusLibrarian uses a built-in research question for testing - no arguments needed

## 📋 For Framework Weight Validation Research

The research execution checklist correctly points to this method:

```bash
# Step 1: Run DiscernusLibrarian directly (from project root)
python3 -m discernus.core.discernuslibrarian

# Step 2: Use research question from issue description  
# Step 3: Store results per specification
```

The built-in test will generate a comprehensive literature review that demonstrates the proper methodology for any research question.

## 💡 Integration with Research Process

After running DiscernusLibrarian:
1. Check `discernus/librarian/reports/` for the markdown report
2. Check `discernus/librarian/research_data/` for the JSON data
3. Move reports to appropriate framework validation directories if needed
4. Archive completed research following the established patterns

This ensures consistent, high-quality research output using the proper DiscernusLibrarian methodology.