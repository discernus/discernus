# Discernus Development Sprints

This document tracks upcoming development sprints for the Discernus project. Each sprint represents a focused development effort with clear objectives and deliverables.

## Sprint Status Legend

- **Planning**: Sprint is being defined and requirements gathered
- **Ready**: Sprint is defined and ready to start
- **In Progress**: Sprint is currently active
- **Completed**: Sprint has been finished
- **Blocked**: Sprint is waiting on external dependencies

---

## Upcoming Sprints

### Sprint 9: CLI Parameter Override & Fast Re-analysis

**Priority:** Medium  
**Estimated Effort:** 3 days  
**Status:** Planning  
**Target Start:** 2025-01-10

#### Problem Statement

While we've implemented experiment-level parameterization for reliability filtering, researchers still need to re-run expensive analysis phases when testing different parameter values. We need CLI parameter override support and fast re-analysis capabilities to enable efficient sensitivity analysis without re-running LLM analysis.

#### Success Criteria

- [ ] **CLI Parameter Override**: Support `--salience-threshold`, `--confidence-threshold` overrides
- [ ] **Fast Re-analysis**: Enable statistical re-runs without re-analysis when only parameters change
- [ ] **Provenance Tracking**: Track parameter changes in run metadata
- [ ] **User Documentation**: Clear guidance on parameter selection and trade-offs

#### Technical Requirements

- [ ] **CLI Enhancement**: Add parameter override flags to `discernus run` command
- [ ] **Parameter Validation**: Validate override parameters against framework requirements
- [ ] **Fast Path Logic**: Skip analysis phase when only statistical parameters change
- [ ] **Metadata Updates**: Update run metadata with parameter overrides
- [ ] **Documentation**: Create parameter selection guide

---

### Sprint 10: Resume Functionality Testing & Hardening

**Priority:** Critical  
**Estimated Effort:** 2 days  
**Status:** Planning  
**Target Start:** 2025-01-08

#### Problem Statement

Resume functionality has been reported as "breaking a lot lately" with experiments restarting from document 1 instead of resuming from interruption points. While the phase state infrastructure appears solid, resume behavior is unreliable in practice, particularly when analysis phase is interrupted mid-document-processing. This is a release blocker - we cannot ship v2.1 without reliable resume capability.

#### Known Issues

1. **Analysis Phase Interruption**: When analysis phase gets interrupted mid-document, `phase_state.json` may not mark analysis as complete, blocking all resume attempts
2. **Silent Restart Behavior**: Resume attempts that fail validation silently fall back to fresh runs, wasting compute and confusing users
3. **Artifact Registry Corruption**: Interrupted runs may leave inconsistent artifact registries, causing resume failures
4. **CDDF Resume Failures**: Recent CDDF experiment debugging showed resume attempts restarting from document 1

#### Success Criteria

**Phase 1: Diagnostic Testing (Day 1)**

- [ ] **Nano Experiment Baseline**: Run nano experiment (2 documents) to completion, verify phase_state.json correctness
- [ ] **Controlled Interruption Test**: Interrupt nano mid-document 2, verify phase state reflects partial completion
- [ ] **Resume Test**: Attempt resume, verify it continues from correct document (not restart)
- [ ] **Artifact Registry Validation**: Verify artifact registry consistency across resume boundary
- [ ] **Error Message Testing**: Verify clear error messages when resume is not possible

**Phase 2: Root Cause Analysis (Day 1)**

- [ ] **Phase Marking Logic Review**: Identify when `mark_phase_complete()` is called during analysis
- [ ] **Interruption Scenarios**: Document what happens to phase state during LLM timeout, keyboard interrupt, crash
- [ ] **Registry Merge Logic**: Verify artifact registry merging handles edge cases (duplicate hashes, missing entries)
- [ ] **Resume Validation Logic**: Confirm `can_resume_from()` correctly handles partial phase completion

**Phase 3: Fixes & Hardening (Day 2)**

- [ ] **Implement Per-Document Checkpointing**: Mark progress after each document completion, not just phase completion
- [ ] **Add Resume Validation**: Explicit validation that resume will work before copying artifacts
- [ ] **Improve Error Messages**: Clear guidance when resume is not possible and why
- [ ] **Add Resume Logging**: Enhanced logging to track resume operations and artifact copying
- [ ] **Implement Safe Resume Mode**: Option to verify artifact integrity before resume

**Phase 4: Comprehensive Testing (Day 2)**

- [ ] **Test Resume After Each Phase**: Validate resume after validation, analysis (per document), statistical, evidence, synthesis
- [ ] **Test Failure Scenarios**: Keyboard interrupt, LLM timeout, network failure, disk full
- [ ] **Test Cross-Run Resume**: Verify --run-dir parameter works correctly
- [ ] **Test Auto-Discovery**: Verify `find_resumable_run()` selects correct run
- [ ] **Performance Testing**: Verify resume doesn't add significant overhead

#### Technical Requirements

**Code Changes:**

- `discernus/core/phase_state.py`: Add per-document checkpoint support
- `discernus/cli.py`: Enhanced resume validation and error messages  
- `discernus/core/atomic_document_analysis.py`: Add document-level completion tracking
- `discernus/core/local_artifact_storage.py`: Add artifact integrity validation

**Testing:**

- `discernus/tests/test_resume_functionality.py`: Comprehensive resume test suite
- Test fixtures for interrupted runs with known good state
- Integration tests covering all phase boundaries

#### Deliverables

- [ ] **Resume Test Suite**: Automated tests covering all resume scenarios
- [ ] **Resume Diagnostic Tool**: CLI command to validate if a run can be resumed
- [ ] **Resume Documentation**: User guide on resume functionality and troubleshooting
- [ ] **Release Readiness Report**: Pass/fail assessment with evidence

#### Definition of Done

- Nano experiment can be interrupted at any point and successfully resumed
- Resume failures produce clear, actionable error messages
- Automated test suite validates resume functionality
- Documentation explains resume behavior and limitations
- All team members confident in resume reliability

---

### Sprint 11: v2.1 Release Preparation

**Priority:** High  
**Estimated Effort:** 3 days  
**Status:** Blocked (waiting on Sprint 10)  
**Target Start:** 2025-01-10

#### Problem Statement

The system has undergone significant enhancements including framework fit score implementation, THIN architecture compliance, validation agent improvements, and reliability filtering system updates. These changes need to be properly documented, packaged, and prepared for a v2.1 release to ensure users have clear guidance on new features and capabilities.

#### Success Criteria

##### Phase 1: Documentation Updates (Day 1)

- [ ] **README.md Update**: Update main README with v2.1 features and improvements
- [ ] **CLI Reference Update**: Update `docs/user/CLI_REFERENCE.md` with new parameters and options
- [ ] **Framework Specification**: Ensure `docs/specifications/FRAMEWORK_SPECIFICATION.md` is complete
- [ ] **Experiment Specification**: Ensure `docs/specifications/EXPERIMENT_SPECIFICATION.md` is current
- [ ] **API Documentation**: Update any API or developer documentation

##### Phase 2: User Guides & Examples (Day 2)

- [ ] **User Guide Updates**: Update `docs/user/` guides with new features
- [ ] **Troubleshooting Guide**: Update `docs/user/CLI_TROUBLESHOOTING.md` with new issues/solutions
- [ ] **Example Updates**: Update example experiments to demonstrate new features
- [ ] **Migration Guide**: Create guide for users upgrading from v2.0 to v2.1
- [ ] **Best Practices**: Document best practices for framework fit scores and reliability filtering

##### Phase 3: Release Preparation (Day 3)

- [ ] **Release Notes**: Create comprehensive v2.1 release notes
- [ ] **Changelog**: Update CHANGELOG.md with all changes since v2.0
- [ ] **Version Bumping**: Update version numbers in all relevant files
- [ ] **Tag Preparation**: Prepare git tags and release artifacts
- [ ] **Testing**: Final validation of all documentation and examples

#### Technical Requirements

- [ ] **Documentation Files**: Update all `.md` files in `docs/` directory
- [ ] **Version Files**: Update version numbers in `pyproject.toml`, `__init__.py`, etc.
- [ ] **Example Experiments**: Ensure all example experiments work with v2.1
- [ ] **Release Artifacts**: Prepare release packages and installation instructions
- [ ] **Migration Scripts**: Create any necessary migration scripts for users

#### Key Features to Document

**Framework Fit Score System:**
- [ ] **Framework Specification Requirements**: Document mandatory framework fit score requirements
- [ ] **Statistical Agent Integration**: Document how framework fit scores are calculated
- [ ] **Synthesis Agent Integration**: Document how framework fit scores are interpreted
- [ ] **Framework Examples**: Show examples of framework fit score definitions

**THIN Architecture Compliance:**
- [ ] **JSON Parsing Removal**: Document removal of unnecessary JSON parsing
- [ ] **Performance Improvements**: Document performance benefits
- [ ] **Architecture Principles**: Explain THIN architecture compliance

**Validation Agent Enhancements:**
- [ ] **Corpus Validation**: Document new corpus file accessibility validation
- [ ] **Document Count Validation**: Document document count consistency checks
- [ ] **Error Handling**: Document improved error messages and guidance

**Reliability Filtering System:**
- [ ] **Parameter Configuration**: Document experiment-level parameterization
- [ ] **System Defaults**: Document zero thresholds as default behavior
- [ ] **Sensitivity Analysis**: Document how to perform parameter sensitivity analysis

**CDDF Experiment:**
- [ ] **Corpus Assembly**: Document multi-speaker document handling
- [ ] **Framework v10.2**: Document CDDF v10.2 improvements
- [ ] **Experiment Results**: Document successful 42-document experiment

#### Release Artifacts

- [ ] **Release Notes**: Comprehensive v2.1 release notes
- [ ] **Changelog**: Detailed changelog since v2.0
- [ ] **Migration Guide**: Step-by-step upgrade instructions
- [ ] **Feature Highlights**: Key new features and improvements
- [ ] **Breaking Changes**: Any breaking changes and migration steps
- [ ] **Performance Notes**: Performance improvements and optimizations

#### Success Metrics

- [ ] **Documentation Completeness**: All new features properly documented
- [ ] **User Readiness**: Clear guidance for users upgrading to v2.1
- [ ] **Example Validation**: All example experiments work with v2.1
- [ ] **Release Quality**: Professional, comprehensive release package
- [ ] **Migration Success**: Users can successfully upgrade from v2.0 to v2.1

---

### Sprint 12: Multi-Speaker Document Processing Enhancement

**Priority:** Medium  
**Estimated Effort:** 2 days  
**Status:** Planning  
**Target Start:** 2025-01-25

#### Problem Statement

The CDDF experiment revealed challenges with multi-speaker documents (debates, military addresses) where individual speaker contributions need to be analyzed separately. Currently, these are manually split, but we need automated processing capabilities for common multi-speaker document types.

#### Success Criteria

- [ ] **Debate Processing**: Automated extraction of individual speaker contributions from debate transcripts
- [ ] **Military Address Processing**: Automated splitting of combined military addresses
- [ ] **Speaker Attribution**: Maintain speaker identity in analysis artifacts
- [ ] **Corpus Integration**: Seamless integration with existing corpus assembly workflow

#### Technical Requirements

- [ ] **Document Parser**: Create parser for common multi-speaker document formats
- [ ] **Speaker Detection**: Identify speaker changes in transcripts
- [ ] **Content Extraction**: Extract individual speaker contributions
- [ ] **Metadata Preservation**: Maintain speaker identity and document context
- [ ] **CLI Integration**: Add multi-speaker processing to corpus assembly tools

---

## Sprint Template

Use this template when creating new sprints:

```markdown
### Sprint X: [Sprint Name]

**Priority:** [High/Medium/Low]  
**Estimated Effort:** [X days/weeks]  
**Status:** [Planning/Ready/In Progress/Completed/Blocked]  
**Target Start:** [Date]

#### Problem Statement
[Clear description of the problem being solved]

#### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

#### Technical Requirements
- [ ] [Technical requirement 1]
- [ ] [Technical requirement 2]
- [ ] [Technical requirement 3]

#### Implementation Plan
- [ ] [Phase 1: Description]
- [ ] [Phase 2: Description]
- [ ] [Phase 3: Description]

#### Test Scenarios
1. [Test scenario 1]
2. [Test scenario 2]
3. [Test scenario 3]

#### Dependencies
- [Dependency 1]
- [Dependency 2]

#### Notes
[Additional context, considerations, or implementation notes]
```

---

## Sprint Management Guidelines

### Adding New Sprints

1. Copy the sprint template above
2. Fill in all required fields
3. Add to the "Upcoming Sprints" section
4. Update priority and target start date

### Updating Sprint Status

- Mark sprints as "In Progress" when work begins
- Update progress by checking off completed items
- Mark as "Completed" when all success criteria are met
- Move completed sprints to a "Completed Sprints" section if desired

### Sprint Planning

- Keep sprints focused on 1-2 weeks of work
- Ensure clear, measurable success criteria
- Identify dependencies early
- Include comprehensive test scenarios
