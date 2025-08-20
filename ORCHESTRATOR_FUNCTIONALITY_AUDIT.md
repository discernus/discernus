# Orchestrator Functionality Audit
## Critical Missing Features in Clean Orchestrator

### **CRITICAL ISSUE: Missing txtai RAG Integration**

**Legacy Orchestrator Has:**
- Line 21: `# txtai integration temporarily disabled for Phase 3 MVP`
- Line 8: `- txtai RAG integration for intelligent evidence retrieval`
- Lines 77-85: Evidence retrieval instructions for RAG queries
- Line 78: `You have access to {total_evidence_pieces} pieces of textual evidence`
- Lines 80-85: Semantic query instructions for evidence lookup

**Clean Orchestrator Missing:**
- ❌ No txtai RAG index creation
- ❌ No evidence semantic search capability  
- ❌ No evidence retrieval during synthesis
- ❌ Synthesis agent gets evidence hashes but can't query them semantically

**Impact:** Reports say "absence of textual evidence" despite having 542 evidence pieces

### **CRITICAL ISSUE: Missing Evidence Integration**

**Legacy Orchestrator Has:**
- Lines 754-761: Evidence artifact hash collection from registry
- Line 760: Transaction validation - errors if no evidence found
- Lines 107-113: Evidence context preparation for synthesis
- Lines 58-60: Evidence piece counting for RAG context

**Clean Orchestrator Missing:**
- ❌ Evidence artifact hash collection is wrong (using file stems vs registry)
- ❌ No transaction validation for evidence availability
- ❌ No evidence context preparation
- ❌ No evidence piece counting

### **CRITICAL ISSUE: Missing Corpus Manifest Access**

**Legacy Orchestrator Has:**
- Framework path, experiment path, research data provided to synthesis
- Complete experiment context including corpus metadata

**Clean Orchestrator Missing:**
- ❌ Synthesis agent doesn't get corpus manifest
- ❌ No document count or corpus metadata in synthesis
- ❌ Report shows "4 documents" but no corpus details

### **CRITICAL ISSUE: Missing Transaction Validation**

**Legacy Orchestrator Has:**
- Line 760-761: `if not evidence_hashes: raise V8OrchestrationError`
- Systematic error handling with specific exceptions
- Validation at each stage

**Clean Orchestrator Missing:**
- ❌ No validation that evidence artifacts exist
- ❌ No validation that txtai index is created
- ❌ No validation that synthesis has access to evidence
- ❌ Silent failures instead of explicit errors

### **CRITICAL ISSUE: Wrong Evidence Artifact Access**

**Legacy Orchestrator:**
```python
# Get evidence artifact hashes from the registry
evidence_hashes = []
for artifact_hash, artifact_info in self.artifact_storage.registry.items():
    metadata = artifact_info.get("metadata", {})
    if metadata.get("artifact_type", "").startswith("evidence_v6"):
        evidence_hashes.append(artifact_hash)
```

**Clean Orchestrator:**
```python
# Get evidence artifact hashes from the artifacts directory  
evidence_artifact_hashes = []
artifacts_dir = self.experiment_path / "shared_cache" / "artifacts"
if artifacts_dir.exists():
    evidence_files = list(artifacts_dir.glob("evidence_v6_*"))
    evidence_artifact_hashes = [f.stem for f in evidence_files]  # WRONG!
```

**Issue:** Using file stems instead of registry hashes, no metadata filtering

### **CRITICAL ISSUE: Missing Synthesis Prompt Assembly**

**Legacy Orchestrator Has:**
- Lines 98-105: Uses `SynthesisPromptAssembler` for legacy mode
- Lines 63-126: Complete prompt assembly with evidence instructions
- Lines 77-85: RAG evidence database instructions

**Clean Orchestrator Missing:**
- ❌ Only uses enhanced mode, no fallback to assembler
- ❌ No comprehensive prompt assembly
- ❌ No evidence retrieval instructions

## **Required Fixes**

### **1. Restore txtai RAG Integration**
- [ ] Create txtai index from evidence database
- [ ] Enable semantic evidence queries during synthesis
- [ ] Add RAG context to synthesis prompts

### **2. Fix Evidence Artifact Access**
- [ ] Use artifact registry instead of file system glob
- [ ] Proper metadata filtering for evidence artifacts
- [ ] Transaction validation for evidence availability

### **3. Add Corpus Manifest Access**
- [ ] Pass corpus manifest to synthesis agent
- [ ] Include document metadata in synthesis context
- [ ] Provide complete experiment context

### **4. Implement Transaction Validation**
- [ ] Error out if evidence artifacts missing
- [ ] Error out if txtai index creation fails
- [ ] Error out if synthesis can't access evidence
- [ ] Replace silent failures with explicit errors

### **5. Add Comprehensive Unit Tests**
- [ ] Test evidence artifact collection
- [ ] Test txtai index creation
- [ ] Test evidence retrieval during synthesis
- [ ] Test transaction validation failures

## **Engineering Process Failure**

**Root Cause:** Rewrote orchestrator without:
1. ❌ Documenting existing functionality first
2. ❌ Creating feature parity checklist  
3. ❌ Unit testing each component
4. ❌ Transaction-based validation
5. ❌ Systematic comparison with legacy

**Result:** Silent feature degradation discovered through manual inspection

**Required:** Systematic engineering approach with comprehensive testing before integration
