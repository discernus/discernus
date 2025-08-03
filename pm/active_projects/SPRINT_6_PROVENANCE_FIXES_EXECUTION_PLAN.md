# Sprint 6: Provenance Fixes Execution Plan
*Ready for immediate execution when user returns from beach*

## Critical Path Issues - Alpha Foundation

### **Issue #293: Fix Orchestrator Field Name Mismatch** *(15 minutes)*
**Problem**: `ThinOrchestrator` looks for `statistical_results_artifact_hash` but `ProductionThinSynthesisPipeline` returns `statistical_results_hash`

**Location**: `discernus/core/thin_orchestrator.py` lines 869-876
**Root Cause**: Field name mismatch between orchestrator expectations and pipeline output

**Fix Required**:
```python
# CURRENT (broken):
if "statistical_results_artifact_hash" in synthesis_result:
    statistical_results_hash = synthesis_result["statistical_results_artifact_hash"]
if "curated_evidence_artifact_hash" in synthesis_result:
    curated_evidence_hash = synthesis_result["curated_evidence_artifact_hash"]

# FIX TO:
if "statistical_results_hash" in synthesis_result:
    statistical_results_hash = synthesis_result["statistical_results_hash"]
if "curated_evidence_hash" in synthesis_result:
    curated_evidence_hash = synthesis_result["curated_evidence_hash"]
```

**Validation**: Run large batch test - `statistical_results.csv` should be populated

---

### **Issue #294: Fix CSV Export Agent Silent Failure** *(30 minutes)*
**Problem**: `CSVExportAgent._generate_statistical_results_csv()` creates empty file instead of raising error when no data provided

**Location**: `discernus/agents/csv_export_agent/agent.py` lines 602-626
**Root Cause**: Buggy failsafe condition `elif statistical_results:` matches empty dict

**Fix Required**:
```python
# CURRENT (broken):
elif statistical_results:  # This matches empty dict {}
    self.logger.info("No statistical results found - generating placeholder data")
    results = {}

# FIX TO:
elif statistical_results and any(statistical_results.values()):  # Check for actual content
    results = statistical_results
else:
    raise ValueError(f"No statistical results data provided to CSV export. "
                    f"Received: {statistical_results}")
```

**Additional Enhancement**: Add data validation before CSV generation
```python
def _validate_statistical_results(self, results: Dict[str, Any]) -> None:
    """Validate statistical results have required structure and content."""
    if not results:
        raise ValueError("Statistical results cannot be empty")
    
    # Add specific validation for expected statistical data structure
    required_fields = ['test_name', 'statistic_value', 'p_value']
    # Implementation details...
```

**Validation**: Empty statistical results should raise clear error, not create empty CSV

---

### **Issue #295: Add Synthesis Artifact Metadata** *(2 hours)*
**Problem**: Synthesis artifacts lack proper metadata for provenance tracking

**Location**: `discernus/agents/thin_synthesis/orchestration/pipeline.py`
**Enhancement Required**: Add comprehensive metadata to all synthesis artifacts

**Implementation**:
```python
def _store_artifact_with_metadata(self, content: str, artifact_type: str, 
                                stage: str, dependencies: List[str] = None) -> str:
    """Store artifact with comprehensive provenance metadata."""
    metadata = {
        "artifact_type": artifact_type,
        "stage": stage,
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": dependencies or [],
        "content_hash": hashlib.sha256(content.encode()).hexdigest(),
        "size_bytes": len(content.encode()),
        "pipeline_version": "v2.0",
        "agent_versions": {
            "analysis_planner": "v1.0",
            "results_interpreter": "v1.0", 
            "evidence_curator": "v1.0"
        }
    }
    
    # Store both content and metadata
    content_hash = self.artifact_storage.store_artifact(content, metadata)
    return content_hash
```

**Artifacts to Enhance**:
- `statistical_results` - add analysis provenance
- `curated_evidence` - add curation provenance  
- `synthesis_report` - add synthesis provenance
- `final_report` - add compilation provenance

**Validation**: All artifacts should have complete metadata in artifact registry

---

### **Issue #296: Add Artifact Hash Validation** *(1 hour)*
**Problem**: No validation that artifact hashes exist and are accessible

**Location**: `discernus/core/thin_orchestrator.py` 
**Enhancement Required**: Validate all artifact hashes before CSV export

**Implementation**:
```python
def _validate_artifact_hashes(self, *hashes: str) -> Dict[str, bool]:
    """Validate that all provided artifact hashes exist and are accessible."""
    validation_results = {}
    
    for hash_value in hashes:
        if not hash_value:
            validation_results[hash_value] = False
            continue
            
        try:
            # Check if artifact exists in storage
            artifact_exists = self.artifact_storage.artifact_exists(hash_value)
            validation_results[hash_value] = artifact_exists
            
            if not artifact_exists:
                self.logger.error(f"Artifact hash {hash_value} not found in storage")
                
        except Exception as e:
            self.logger.error(f"Error validating artifact hash {hash_value}: {e}")
            validation_results[hash_value] = False
    
    return validation_results

def _export_final_synthesis_csv_files(self, scores_hash, evidence_hash, 
                                    statistical_results_hash, curated_evidence_hash,
                                    framework_content, experiment_config, 
                                    corpus_manifest, synthesis_result, 
                                    results_dir, audit):
    """Export CSV files with artifact hash validation."""
    
    # Validate all hashes before proceeding
    hash_validation = self._validate_artifact_hashes(
        scores_hash, evidence_hash, statistical_results_hash, curated_evidence_hash
    )
    
    # Log validation results
    for hash_value, is_valid in hash_validation.items():
        if not is_valid and hash_value:  # Only log errors for non-empty hashes
            audit.log_error(f"Invalid artifact hash: {hash_value}")
    
    # Continue with existing CSV export logic...
```

**Validation**: Invalid or missing artifact hashes should be caught and logged before CSV export

## Execution Sequence

### **Step 1: Field Name Mismatch (15 min)**
1. Open `discernus/core/thin_orchestrator.py`
2. Navigate to lines 869-876
3. Change `statistical_results_artifact_hash` → `statistical_results_hash`
4. Change `curated_evidence_artifact_hash` → `curated_evidence_hash`
5. Test with simple experiment run

### **Step 2: CSV Export Silent Failure (30 min)**
1. Open `discernus/agents/csv_export_agent/agent.py`
2. Navigate to `_generate_statistical_results_csv()` method
3. Fix the buggy failsafe condition
4. Add proper error handling for empty data
5. Test with empty statistical results input

### **Step 3: Synthesis Artifact Metadata (2 hours)**
1. Open `discernus/agents/thin_synthesis/orchestration/pipeline.py`
2. Implement `_store_artifact_with_metadata()` method
3. Update all artifact storage calls to include metadata
4. Test artifact registry contains proper metadata
5. Validate metadata structure and completeness

### **Step 4: Artifact Hash Validation (1 hour)**
1. Open `discernus/core/thin_orchestrator.py`
2. Implement `_validate_artifact_hashes()` method
3. Add validation call to `_export_final_synthesis_csv_files()`
4. Test with missing/invalid artifact hashes
5. Validate error logging and handling

### **Step 5: Integration Testing (30 min)**
1. Run complete large batch test experiment
2. Verify `statistical_results.csv` is properly populated
3. Check artifact registry for complete metadata
4. Validate provenance chain is instantly traversable
5. Confirm no silent failures in CSV export pipeline

## Success Criteria

### **Immediate Validation**
- [ ] `statistical_results.csv` contains actual statistical data (not empty)
- [ ] Field name mismatch resolved - orchestrator finds synthesis artifacts
- [ ] CSV export agent raises clear errors instead of silent failures
- [ ] All synthesis artifacts have comprehensive metadata

### **Provenance Chain Validation**
- [ ] Can trace from final report back to raw artifacts instantly
- [ ] Artifact registry contains complete provenance metadata
- [ ] Hash validation catches missing or corrupted artifacts
- [ ] Error logging provides clear diagnostic information

### **Academic Integrity Validation**
- [ ] Statistical results in final report match CSV export
- [ ] Evidence quotes traceable to original corpus documents
- [ ] Analysis process fully documented and auditable
- [ ] No hallucinated or fabricated data in any output

## Risk Mitigation

### **Code Safety**
- **Backup Strategy**: Git commit before each change
- **Incremental Testing**: Test each fix individually before combining
- **Rollback Plan**: Clear revert path if any fix causes regression

### **Academic Integrity**
- **Validation Testing**: Use known-good experiment data for testing
- **Cross-Reference Checks**: Verify fixes don't alter research results
- **Audit Trail**: Complete logging of all changes and validations

---

**Ready for Execution**: All fixes identified, implementation planned, validation criteria established. Estimated total time: ~4 hours for complete Sprint 6 resolution.