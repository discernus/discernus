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

### Sprint 11: v2.1 Release Preparation

**Priority:** High  
**Estimated Effort:** 3 days  
**Status:** Planning  
**Target Start:** 2025-01-15

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
