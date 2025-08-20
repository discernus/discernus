# CleanAnalysisOrchestrator Missing Features Audit

## CRITICAL MISSING COMPONENTS

### 1. EnhancedManifest (CRITICAL)
**Legacy:** Initializes `EnhancedManifest` for comprehensive provenance tracking
**Clean:** ❌ MISSING - No manifest initialization
**Impact:** Complete loss of experiment provenance and metadata tracking

### 2. RAG Evidence Integration (CRITICAL) 
**Legacy:** Uses `SynthesisPromptAssembler` with txtai RAG queries
**Clean:** ❌ BROKEN - Invented "enhanced mode" without approval, doesn't scale
**Impact:** Evidence integration fails on large corpora, architectural mismatch

### 3. Audit Logger Setup (MODERATE)
**Legacy:** `run_folder=run_folder` (session/run_id/)
**Clean:** `run_folder=session_dir / "logs"` (session/run_id/logs/)
**Impact:** Different logging structure, potential log location issues

### 4. Artifact Storage Path (MODERATE)
**Legacy:** `shared_cache_dir = experiment_path / "shared_cache"`
**Clean:** `shared_cache_dir = experiment_path / "shared_cache" / "artifacts"`
**Impact:** Different cache structure, potential artifact location issues

### 5. LLM Gateway Initialization (MODERATE)
**Legacy:** Initializes `LLMGateway(ModelRegistry())` in infrastructure setup
**Clean:** ❌ MISSING - No LLM gateway initialization
**Impact:** May affect model tracking and LLM interaction logging

### 6. Missing Infrastructure Components
**Legacy has but Clean missing:**
- `SecureCodeExecutor` initialization
- `CapabilityRegistry` setup  
- `DataAggregationPromptAssembler` integration
- Complete infrastructure initialization pattern

## LOGGING & PROVENANCE GAPS

### Missing Logging Calls
- ❌ No `log_experiment_complete` call (though legacy also missing this)
- ❌ Different audit logger folder structure
- ❌ No manifest-based provenance tracking

### Missing Provenance Features  
- ❌ No `EnhancedManifest` = No experiment metadata tracking
- ❌ No comprehensive artifact chain tracking
- ❌ No LLM interaction logging through proper gateway

## ARCHITECTURAL ISSUES

### 1. Evidence Integration Architecture
The "enhanced mode" direct embedding approach:
- ❌ Doesn't scale beyond small corpora
- ❌ Was never approved or discussed
- ❌ Replaces proven RAG architecture without justification
- ❌ Creates context window and quality degradation risks

### 2. Infrastructure Initialization
Clean orchestrator uses ad-hoc initialization vs. legacy's comprehensive `_initialize_infrastructure()` pattern.

## REQUIRED FIXES

### Immediate (Critical)
1. **Revert to RAG approach** - Remove "enhanced mode", use `SynthesisPromptAssembler`
2. **Add EnhancedManifest** - Critical for provenance tracking
3. **Fix audit logger paths** - Match legacy structure
4. **Fix artifact storage paths** - Match legacy structure

### Secondary (Important)  
1. **Add LLM Gateway initialization** - For proper model tracking
2. **Add missing infrastructure components** - SecureCodeExecutor, etc.
3. **Standardize initialization pattern** - Use `_initialize_infrastructure()` approach

## ROOT CAUSE
The clean orchestrator was created by copying patterns without understanding the full infrastructure requirements. Critical components were omitted, and architectural changes were made without approval.

## RECOMMENDATION
**Stop using CleanAnalysisOrchestrator until these critical gaps are fixed.** The missing `EnhancedManifest` alone represents a complete loss of academic provenance tracking.
