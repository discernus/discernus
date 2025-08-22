# Test-Driven Development (TDD) Protocol for Critical Regressions

## Overview

This document outlines the proven 6-phase TDD approach that successfully resolved the ARCH-002 critical regression in the Discernus orchestrator. This protocol should be followed whenever critical regressions are identified to ensure cost-effective, disciplined remediation.

## Background: ARCH-002 Success Story

**Issue**: `CleanAnalysisOrchestrator` was processing all documents in a single batch LLM call, violating THIN architecture principles and creating scalability limitations.

**Impact**: 
- Experiments failed during statistical analysis phase
- No individual document caching or provenance
- Limited to ~400 documents maximum
- Violated core THIN architecture principles

**Resolution**: Complete success using 6-phase TDD approach
- **Cost**: ~$13 total (vs $50+ for unstructured debugging)
- **Time**: 1 session with disciplined methodology
- **Outcome**: Full restoration of individual processing with comprehensive testing

## 6-Phase TDD Protocol

### Phase 1: Unit Test Development
**Goal**: Validate regression patterns and expected behavior
**Deliverables**: 
- Focused unit tests for regression patterns
- Tests for expected individual processing behavior
- Mock-based tests that don't require API calls

**Example from ARCH-002**:
```python
# test_orchestrator_regression_simple.py
def test_individual_document_processing(self):
    """Verify orchestrator processes documents individually, not in batch"""
    # Test implementation
```

**Success Criteria**: All regression pattern tests pass

### Phase 2: Path Bug Investigation
**Goal**: Identify and fix configuration/path issues
**Deliverables**:
- Minimal code changes for path/configuration fixes
- Documentation of what was broken and why

**Example from ARCH-002**:
```python
# Fixed artifacts_dir path in _convert_analysis_to_dataframe
artifacts_dir = self.experiment_path / "shared_cache" / "artifacts"  # Fixed
# Old: artifacts_dir = self.experiment_path / "shared_cache" / "artifacts" / "artifacts"
```

**Success Criteria**: Path-related errors resolved

### Phase 3: Core Implementation
**Goal**: Implement fixes using proven patterns
**Deliverables**:
- Core functionality restored using working code patterns
- Individual document processing logic implemented
- Proper artifact storage and retrieval

**Example from ARCH-002**:
```python
# Refactored _run_analysis_phase to process documents individually
for prepared_doc in prepared_documents:
    result_hash = analysis_agent.analyze_batch(
        corpus_documents=[prepared_doc]  # Single document, not batch
    )
    # Store individual result
    self.artifact_storage.put_artifact(result_hash, analysis_data)
```

**Success Criteria**: Core functionality tests pass

### Phase 4: Integration Testing
**Goal**: Verify end-to-end pipeline logic with mocks
**Deliverables**:
- Integration tests using mocked LLM calls
- End-to-end pipeline validation without API costs
- Mock-based testing of orchestrator logic

**Example from ARCH-002**:
```python
# test_statistical_analysis_integration.py
# test_synthesis_integration.py
# Mock-based tests that validate pipeline logic
```

**Success Criteria**: All integration tests pass with mocked dependencies

### Phase 5: Limited Live Testing
**Goal**: Validate fixes in live environment with minimal cost
**Deliverables**:
- 1-document experiment that validates the fix
- Confirmation that analysis → statistics → synthesis works
- Minimal API usage for validation

**Example from ARCH-002**:
```bash
# Created projects/test_individual_processing/
# Single document experiment to validate individual processing
python -m discernus run .
```

**Success Criteria**: Limited live test completes successfully

### Phase 6: Full Validation
**Goal**: Confirm complete resolution with original experiments
**Deliverables**:
- Original failed experiment reruns successfully
- All documents processed individually
- Complete end-to-end pipeline validation

**Example from ARCH-002**:
```bash
# Reran simple_test_pdaf (4 documents)
# Confirmed 4 individual analysis artifacts created
# Statistical analysis and synthesis completed successfully
```

**Success Criteria**: Original experiment reruns without errors

## Cost Containment Rules

### API Usage Restrictions
- **Phase 1-4**: NO API calls allowed
- **Phase 5**: Maximum 1-document experiment
- **Phase 6**: Original experiment only after Phase 5 success

### Testing Strategy
- **90% Unit/Integration**: Use mocks and static data
- **10% Live Validation**: Minimal experiments for final confirmation
- **Document All Costs**: Track and justify each API call

### Pattern Reuse
- **Import Working Code**: Don't rebuild from scratch
- **Use Proven Patterns**: Leverage existing working implementations
- **Minimize Changes**: Focus on specific regression, not architecture changes

## Success Criteria Checklist

### Technical Requirements
- [ ] Unit tests pass for all regression patterns
- [ ] Integration tests pass with mocked dependencies
- [ ] Limited live test completes successfully
- [ ] Original experiment reruns without errors
- [ ] Individual processing restored (not batch processing)
- [ ] All artifacts properly structured and accessible

### Process Requirements
- [ ] Issue logged in backlog with ARCH-XXX identifier
- [ ] Detailed remediation plan documented
- [ ] All phases completed in sequence
- [ ] Cost tracking and justification documented
- [ ] Lessons learned captured for future use

### Documentation Requirements
- [ ] Remediation plan in `docs/developer/`
- [ ] Progress updates in `pm/todo/discernus_v10_backlog.md`
- [ ] Test files preserved for future regression detection
- [ ] This protocol updated with new learnings

## Implementation Examples

### Creating Unit Tests
```python
# Focus on regression patterns, not full functionality
def test_batch_processing_regression(self):
    """Verify orchestrator doesn't process all documents in single batch"""
    # Test that documents are processed individually
    # Mock analysis agent to track call patterns
```

### Mocking Dependencies
```python
# Mock LLM calls to avoid API costs
@patch('discernus.agents.EnhancedAnalysisAgent.analyze_batch')
def test_analysis_phase_integration(self, mock_analyze):
    mock_analyze.return_value = "test_hash"
    # Test orchestrator logic without real LLM calls
```

### Limited Live Testing
```bash
# Create minimal test experiment
mkdir -p projects/test_regression_fix/corpus
echo "Test document content" > projects/test_regression_fix/corpus/test.txt
# Run with minimal corpus to validate fix
```

## Lessons Learned from ARCH-002

### What Worked Well
1. **Immediate Documentation**: Logging issue in backlog prevented scope creep
2. **Sequential Phases**: Each phase built confidence before moving to next
3. **Mock-Based Testing**: 90% of debugging done without API costs
4. **Proven Patterns**: Importing working code was faster than rebuilding
5. **Cost Discipline**: Limited live testing prevented expensive debugging cycles

### Common Pitfalls to Avoid
1. **Skipping Phases**: Don't jump to live testing without unit test validation
2. **Scope Creep**: Focus on specific regression, not general improvements
3. **API Overuse**: Use mocks for most debugging, live tests only for validation
4. **Pattern Ignorance**: Don't rebuild when working code exists elsewhere

### Future Improvements
1. **Automated Regression Detection**: Unit tests that catch similar issues
2. **Cost Monitoring**: Built-in API usage tracking and alerts
3. **Pattern Library**: Document proven solutions for common regressions
4. **Test Coverage**: Ensure critical paths have comprehensive test coverage

## Conclusion

The 6-phase TDD protocol successfully resolved the ARCH-002 critical regression with minimal cost and maximum confidence. This approach should be the standard for all critical regression remediation in the Discernus project.

**Key Success Factors**:
- Disciplined adherence to the 6-phase sequence
- Heavy use of unit tests and mocks (90% of debugging)
- Minimal live testing (10% for validation only)
- Documentation and pattern reuse
- Cost containment and justification

**Next Steps**: 
- Apply this protocol to future critical regressions
- Update protocol based on new learnings
- Ensure all Cursor agents are familiar with this approach
- Build automated regression detection to prevent similar issues
