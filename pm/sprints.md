# Discernus v10 Sprints

**Purpose**: Organized backlog with sprint planning, dependencies, and detailed item specifications.

**Usage**:

- "groom our sprints" → organize inbox items into proper sprint structure
- Items moved here from inbox.md during grooming sessions

---

## Current Status

**Latest Updates**:
- ✅ **Sprint 9 COMPLETED**: CLI UX improvements including dry run validation and model validation
- ✅ **Sprint 10 COMPLETED**: All critical logging integrity issues resolved, rate limiting fixed, and provider-consistent fallback strategy implemented
- ✅ **Golden Run Archive System**: Complete research transparency package with provenance consolidation, input materials consolidation, and comprehensive documentation
- ✅ **RAG Engine Analysis**: Confirmed txtai as primary RAG engine, Typesense for fact checker
- ✅ **Dependencies Updated**: Added txtai>=5.0.0 to requirements.txt

**Current Focus**: System is stable with comprehensive validation, logging integrity, robust fallback handling, and complete research transparency capabilities

---

## Current Sprint Planning

**Next Priority**: Organize inbox items into focused sprints for next development phase

---

## New Sprint Structure

### Sprint 11: Statistical Preparation & CSV Export (HIGH PRIORITY)

**Timeline**: 2-3 weeks
**Goal**: Implement core statistical preparation workflow and CSV export functionality for data analysis

#### [STATS-001] CSV Export Agent Restoration

- **Description**: Bring back the CSV export agent from `/Volumes/code/discernus/discernus/agents/csv_export_agent`
- **Purpose**: Restore CSV export functionality for data analysis workflows
- **Priority**: HIGH - Restoring existing functionality
- **Dependencies**: None
- **Effort**: 2-3 days

#### [STATS-002] Statistical Preparation Stage and CSV Export System

- **Description**: Implement the core infrastructure for statistical preparation mode, including the orchestration stage, derived metrics calculation, and CSV export system
- **Purpose**: Enable `discernus run --statistical-prep` command that produces analysis-ready CSV datasets with raw scores, derived metrics, and evidence quotes
- **Priority**: HIGH - Core workflow functionality
- **Acceptance Criteria**:
  - Add `--statistical-prep` CLI flag to orchestrator
  - Implement derived metrics calculation using existing MathToolkit
  - Create CSV export with raw scores, derived metrics, and evidence quotes
  - Generate variable codebook with column definitions
  - Store statistical preparation artifacts with content-addressable hashing
  - Update manifest.json to track statistical preparation stage
  - Maintain complete provenance chain for resume capability
- **Dependencies**: [STATS-001]
- **Effort**: 1-2 weeks

#### [STATS-003] Evidence-Integrated CSV Export for Statistical Analysis

- **Description**: Enhance the CSV export functionality to include evidence integration, allowing researchers to export statistical results with linked evidence for comprehensive analysis and reporting
- **Purpose**: Enable researchers to export statistical analysis results with integrated evidence, maintaining the connection between data and supporting evidence in external tools
- **Priority**: MEDIUM - Data export enhancement
- **Acceptance Criteria**:
  - CSV export includes evidence columns
  - Evidence properly linked to statistical results
  - Export format is compatible with external analysis tools
  - Evidence metadata preserved in export
  - Export performance optimized for large datasets
- **Dependencies**: [STATS-002]
- **Effort**: 1 week

#### [STATS-004] Resume from Statistical Preparation to Full Synthesis

- **Description**: Implement the ability to resume from statistical preparation to full synthesis, providing workflow flexibility for researchers who initially chose the offramp but later want complete analysis
- **Purpose**: Enable researchers to continue from statistical preparation results to full Discernus synthesis when needed, providing maximum flexibility in research workflow
- **Priority**: MEDIUM - Workflow flexibility
- **Acceptance Criteria**:
  - `discernus run --resume-from-stats` command functionality
  - Automatic detection of existing statistical preparation artifacts
  - Seamless continuation from statistical prep to synthesis stage
  - Updated manifest.json with resume history and provenance
  - Extended directory structure with synthesis artifacts
  - Preserved statistical preparation results alongside synthesis results
- **Dependencies**: [STATS-002]
- **Effort**: 1 week

#### [STATS-005] Skip Synthesis Offramp Option

- **Description**: Bring back the "skip synthesis" offramp option
- **Purpose**: Allow users to run analysis-only workflows without synthesis phase
- **Priority**: MEDIUM - Workflow flexibility improvement
- **Dependencies**: [STATS-002]
- **Effort**: 1-2 days

#### [STATS-006] User-Friendly Messaging for Statistical Preparation Mode

- **Description**: Implement user-friendly messaging for statistical preparation mode to improve user experience and clarity
- **Purpose**: Provide clear messaging about what statistical preparation mode does, when to use it, and what outputs to expect
- **Priority**: MEDIUM - User experience
- **Acceptance Criteria**:
  - Clear messaging about statistical preparation mode functionality
  - User guidance on when to use statistical preparation vs full synthesis
  - Clear explanation of expected outputs and deliverables
  - Improved user experience for statistical preparation workflow
- **Dependencies**: [STATS-002]
- **Effort**: 2-3 days

---

### Sprint 12: Provenance System Restoration (HIGH PRIORITY)

**Timeline**: 2-3 weeks
**Goal**: Restore and enhance provenance system components and ensure compliance with architectural standards

#### [PROV-001] Provenance Components Restoration

- **Description**: Restore provenance components:
  - `/Volumes/code/discernus/discernus/core/provenance_organizer.py`
  - `/Volumes/code/discernus/discernus/core/provenance_stamp.py`
  - `/Volumes/code/discernus/discernus/core/provenance_visualizer.py`
- **Purpose**: Restore full provenance system functionality
- **Priority**: HIGH - Core system functionality
- **Dependencies**: None
- **Effort**: 1-2 weeks

#### [PROV-002] Provenance System Compliance

- **Description**: Comply with provenance, provenance validation, and dual-track logging documents:
  - @PROVENANCE_SYSTEM.md
  - @DUAL_TRACK_LOGGING_ARCHITECTURE.md
  - @INTEGRATED_PROVENANCE_VALIDATION_SPEC.md
- **Purpose**: Ensure system meets documented architectural standards
- **Priority**: HIGH - Architecture compliance
- **Dependencies**: [PROV-001]
- **Effort**: 1 week

#### [PROV-003] Research Integrity & Provenance Architecture Enhancement

- **Description**: Enhance existing provenance architecture by fixing connection points, adding validation, and improving human comprehension
- **Purpose**: Fix critical provenance chain breaks and create human-comprehensible artifact organization for academic transparency
- **Priority**: HIGH - Research integrity
- **Acceptance Criteria**:
  - Zero empty CSV files, all statistical results properly exported
  - Human-comprehensible artifact organization with readable names
  - Complete provenance visualization tools and browser interface
  - External reviewers can validate findings in <2 minutes
  - Platform meets highest academic standards for transparency
- **Dependencies**: [PROV-001], [PROV-002]
- **Effort**: 1-2 weeks

#### [PROV-004] Audit and Fix Directory Creation Logic to Comply with Provenance Standard

- **Description**: Audit codebase to find and fix logic that creates incorrect directory structures, ensuring compliance with v3 provenance standard
- **Purpose**: Fix non-compliant directory structures and create migration script for legacy project data
- **Priority**: HIGH - Provenance compliance
- **Acceptance Criteria**:
  - All new experiments create correct `projects/{PROJECT}/sessions/{SESSION}` structure
  - Migration script successfully reorganizes all legacy project data
  - Root `/projects` directory clean of non-compliant project folders
  - Tests verify correct directory structure creation
- **Dependencies**: [PROV-001]
- **Effort**: 1 week

---

### Sprint 13: Code Quality & Architecture Cleanup (MEDIUM PRIORITY)

**Timeline**: 2-3 weeks
**Goal**: Clean up dead code, remove deprecated components, and update architecture documentation

#### [CLEANUP-001] Dead Code Inventory

- **Description**: Conduct comprehensive inventory for dead code
- **Purpose**: Identify and remove unused code to improve maintainability
- **Priority**: MEDIUM - Code quality improvement
- **Dependencies**: None
- **Effort**: 1 week

#### [CLEANUP-002] Remove Revision Agent and Fact Checker Agent

- **Description**: Remove the revision agent and fact checker agent
- **Purpose**: Clean up unused or deprecated agent components
- **Priority**: MEDIUM - Code cleanup
- **Dependencies**: [CLEANUP-001]
- **Effort**: 2-3 days

#### [CLEANUP-003] Clean Up Dead Code and Update Architecture Documentation

- **Description**: Clean up dead code and update architecture documentation to align with current 3-stage unified pipeline
- **Purpose**: Remove technical debt and align documentation with actual implementation
- **Priority**: HIGH - Technical debt and documentation
- **Acceptance Criteria**:
  - Remove Redis dependencies from requirements.txt and pyproject.toml
  - Remove MinIO references from Makefile and scripts
  - Clean up deprecated orchestrator patterns and unused agent directories
  - Update DISCERNUS_SYSTEM_ARCHITECTURE.md to reflect current 3-stage pipeline
  - Update CURSOR_AGENT_QUICK_START.md to reflect current architecture
  - All dead dependencies removed and deprecated code cleaned up
- **Dependencies**: [CLEANUP-001], [CLEANUP-002]
- **Effort**: 1-2 weeks

#### [CLEANUP-004] System Architecture Document Update

- **Description**: Update the system architecture document to reflect current state
- **Purpose**: Keep architecture documentation current and accurate
- **Priority**: MEDIUM - Documentation maintenance
- **Dependencies**: [CLEANUP-003]
- **Effort**: 3-5 days

---

### Sprint 14: Open Source Strategy & Licensing (HIGH PRIORITY)

**Timeline**: 3-4 weeks
**Goal**: Establish open source strategy, conduct license audit, and prepare for open source release

#### [OPENSOURCE-001] Open Source License Selection and Implementation

- **Description**: Select and implement appropriate open source license for Discernus
- **Purpose**: Balance open source adoption with business strategy while protecting intellectual property and enabling community contribution
- **Priority**: HIGH - Foundation for open source release
- **Acceptance Criteria**:
  - License research and evaluation completed across all options (MIT/Apache 2.0, GPL v3, AGPL v3, dual licensing)
  - Business strategy alignment assessment completed
  - Legal review and compliance verification completed
  - License implementation across entire codebase
  - Contributor license agreement (CLA) setup completed
  - License documentation and notices added throughout codebase
  - Business strategy aligned with selected license
  - Full codebase compliance with selected license confirmed
- **Dependencies**: None
- **Effort**: 2-3 weeks

#### [OPENSOURCE-002] Project Open Source License Dependencies and Business Strategy Alignment

- **Description**: Ensure all project dependencies are license-compatible with business strategy
- **Purpose**: Audit all third-party dependencies for license compatibility and identify potential conflicts with future commercial offerings
- **Priority**: HIGH - Business strategy foundation
- **Acceptance Criteria**:
  - Complete dependency license audit across all components
  - License compatibility matrix created for all dependencies
  - Conflict resolution strategy established for incompatible dependencies
  - Alternative dependency evaluation completed where conflicts exist
  - License compliance monitoring system established
  - Business impact assessment completed for all dependencies
  - All dependencies confirmed license-compatible with business strategy
  - Risk mitigation plan in place for any identified conflicts
- **Dependencies**: [OPENSOURCE-001]
- **Effort**: 1-2 weeks

#### [OPENSOURCE-003] GitHub Strategy - Clean Separation of Development vs Open Source Code

- **Description**: Establish strategy for cleanly separating internal development code from open source version
- **Purpose**: Protect internal IP while enabling community contribution and professional open source release
- **Priority**: HIGH - Open source strategy
- **Acceptance Criteria**:
  - Repository structure planned (main repo vs internal development repos)
  - Branch strategy established (main branch open source vs development branches)
  - Feature flags implemented for internal features disabled in open source builds
  - Configuration management for environment-specific feature enablement
  - Contribution guidelines and boundaries clearly established
  - Open source release pipeline created
  - Internal IP protected while open source version remains professional and complete
- **Dependencies**: [OPENSOURCE-001], [OPENSOURCE-002]
- **Effort**: 1-2 weeks

#### [OPENSOURCE-004] Open Source License Audit

- **Description**: Conduct open source license audit
- **Purpose**: Ensure compliance with all open source dependencies
- **Priority**: HIGH - Legal compliance
- **Dependencies**: [OPENSOURCE-001]
- **Effort**: 1 week

#### [OPENSOURCE-005] Open Source License Insertion

- **Description**: Insert appropriate open source licenses
- **Purpose**: Properly license the project for open source distribution
- **Priority**: HIGH - Legal compliance
- **Dependencies**: [OPENSOURCE-001], [OPENSOURCE-004]
- **Effort**: 3-5 days

#### [OPENSOURCE-006] Release Process

- **Description**: Establish release process
- **Purpose**: Define how to create and distribute releases
- **Priority**: MEDIUM - Process establishment
- **Dependencies**: [OPENSOURCE-001], [OPENSOURCE-002], [OPENSOURCE-003]
- **Effort**: 1 week

---

### Sprint 15: Academic Quality & Documentation (MEDIUM PRIORITY)

**Timeline**: 3-4 weeks
**Goal**: Implement academic quality standards and comprehensive documentation

#### [ACADEMIC-001] Academic Quality & Standards Implementation

- **Description**: Implement comprehensive academic standards, peer review preparation, quality assurance frameworks, and THIN compliance cleanup
- **Purpose**: Ensure Discernus outputs meet top-tier academic journal requirements and stakeholders have complete understanding of system capabilities
- **Priority**: HIGH - Academic excellence
- **Acceptance Criteria**:
  - Evidence standards match top academic journals with >3 sources per claim
  - Automated quality scoring >80% with evidence hallucination detection
  - Performance audit completed with scalability characterization
  - Complete agent architecture documentation with THIN compliance validation
  - Peer review ready quality standards implemented
- **Dependencies**: None
- **Effort**: 2-3 weeks

#### [ACADEMIC-002] Academic Output Standards Implementation

- **Description**: Implement academic-grade output formatting standards for evidence-infused reports with footnote systems and provenance transparency
- **Purpose**: Create publication-ready reports with complete audit trails and multi-audience integration
- **Priority**: HIGH - Academic standards
- **Acceptance Criteria**:
  - Numbered footnotes for all evidence citations with full provenance chains
  - "Evidence Provenance" section with complete audit trail
  - Multi-audience integration (scanner/collaborator/transparency sections)
  - Academic-quality formatting meeting peer-review publication standards
  - Verifiable claim-to-source mapping for reproducibility
- **Dependencies**: [ACADEMIC-001]
- **Effort**: 1-2 weeks

#### [ACADEMIC-003] Enhance Methodology Transparency with Framework Operationalization

- **Description**: Enhance methodology transparency by explaining how abstract framework concepts are operationalized into measurable indicators
- **Purpose**: Provide academic readers with clear understanding of what specific linguistic features or thematic markers are being measured
- **Priority**: MEDIUM - Academic transparency
- **Acceptance Criteria**:
  - Concise methodology section (1-2 paragraphs) in every final report
  - Framework operationalization explicitly explained for each dimension
  - Analysis process from raw text to scores clearly documented
  - Sufficient detail provided for independent replication
- **Dependencies**: [ACADEMIC-001]
- **Effort**: 1 week

#### [ACADEMIC-004] Implement Defensive Prompting to Constrain LLM Over-Generalization

- **Description**: Implement system of defensive prompting to make analysis more robust against LLM over-generalization and hallucination
- **Purpose**: Add constraints and negative instructions to prevent inappropriate scoring based on speaker identity or other biases
- **Priority**: MEDIUM - Quality assurance
- **Acceptance Criteria**:
  - New constraints object added to framework schema
  - Framework parser updated to append constraints to LLM prompts
  - Methodology section includes summary of defensive prompts used
  - Constraints prevent scoring based on speaker identity or other inappropriate factors
- **Dependencies**: [ACADEMIC-001]
- **Effort**: 1 week

#### [ACADEMIC-005] Create Unified Results Dashboard for Researcher-Centric Information Architecture

- **Description**: Design and implement unified, human-readable results dashboard to replace scattered CSVs and markdown reports
- **Purpose**: Provide single, clear dashboard that significantly improves user experience and researcher workflow
- **Priority**: MEDIUM - User experience
- **Acceptance Criteria**:
  - New dashboard agent created that ingests all final artifacts
  - Generates single, standalone HTML file in run's results directory
  - Presents key findings, summary statistics, and visualizations in clear, interactive format
  - Replaces current scattered CSV and markdown output approach
- **Dependencies**: [ACADEMIC-001]
- **Effort**: 1-2 weeks

#### [ACADEMIC-006] Fix Pydantic Serialization Warning in Audit Logging

- **Description**: Fix Pydantic serialization warnings when LiteLLM response objects are logged
- **Problem**: UserWarning appears during audit logging: "Expected 9 fields but got 5: Expected `Message` - serialized value may not be as expected"
- **Impact**: Log noise, no data corruption or functionality issues
- **Root Cause**: LiteLLM response objects don't perfectly align with Pydantic model expectations during JSON serialization
- **Priority**: LOW - Cosmetic issue, no production impact
- **Acceptance Criteria**:
  - Eliminate Pydantic serialization warnings in audit logs
  - Maintain data integrity and functionality
  - Preserve complete audit trail accuracy
- **Solution Options**:
  - Custom JSON serializer for LiteLLM objects in audit logger
  - Convert LiteLLM objects to plain dicts before logging
  - Suppress specific Pydantic warnings for LiteLLM objects
- **Dependencies**: None
- **Effort**: 2-3 days

#### [ACADEMIC-007] Documentation Pass

- **Description**: Conduct comprehensive documentation pass
- **Purpose**: Ensure all documentation is current, accurate, and complete
- **Priority**: MEDIUM - Documentation quality
- **Dependencies**: [ACADEMIC-001], [ACADEMIC-002]
- **Effort**: 1-2 weeks

#### [ACADEMIC-008] Research Spike - Corpus RAG Integration Strategy

- **Description**: Investigate integration strategy for corpus RAG (Retrieval-Augmented Generation) to enhance research capabilities
- **Purpose**: Enhance research capabilities with intelligent corpus discovery and validation through RAG integration
- **Priority**: MEDIUM - Research enhancement
- **Acceptance Criteria**:
  - Value proposition analysis completed for corpus RAG integration
  - Content isolation strategies designed and documented
  - Academic integrity preservation methods established
  - Scalability and performance considerations analyzed
  - Technical architecture design completed
  - Controlled testing plan developed
  - Production integration strategy defined (if validated)
- **Dependencies**: None
- **Effort**: 1-2 weeks

#### [ACADEMIC-009] EPIC - Academic Research-Aligned LLM Ensemble Strategy Implementation

- **Description**: Implement academic research-aligned LLM ensemble strategy
- **Purpose**: Enhance research quality through ensemble methodology and academic validation
- **Priority**: HIGH - Research methodology
- **Acceptance Criteria**:
  - Foundation implementation completed
  - Self-consistency ensemble implemented
  - Multi-model ensemble implemented
  - Parameter integration and optimization completed
  - Academic validation and documentation completed
  - Architecture integration completed
  - Parameter strategy alignment completed
  - Quality assurance framework implemented
- **Dependencies**: None
- **Effort**: 2-3 weeks

---

### Sprint 16: Alpha Release Preparation (CRITICAL PRIORITY)

**Description**: Critical items required for alpha release readiness
**Purpose**: Ensure system is ready for alpha release with comprehensive testing, documentation, and performance validation
**Priority**: CRITICAL - Alpha release blockers
**Timeline**: Immediate - must complete before alpha release
**Dependencies**: None - can begin immediately

#### [ALPHA-001] Complete Test Gauntlet Run

- **Description**: Run complete test gauntlet to validate Alpha Release readiness
- **Purpose**: Ensure all systems work correctly before release
- **Priority**: HIGH - Release validation
- **Acceptance Criteria**:
  - All tests passing across all categories
  - Framework tests completed (all v7.2 frameworks, migration validation, edge cases)
  - Evidence architecture tests completed (three-track validation, evidence retention metrics)
  - Performance tests completed (response times, token usage, resource utilization)
  - Integration tests completed (end-to-end workflows, CLI functionality, error handling)
  - Performance metrics meet targets
  - No regressions detected
  - Results documented
- **Dependencies**: None
- **Effort**: 1-2 weeks

#### [ALPHA-002] Comprehensive Performance & Scalability Audit

- **Description**: Conduct comprehensive system-wide performance audit to establish clear understanding of capabilities and limitations
- **Purpose**: Provide transparent documentation for users and stakeholders about system performance envelope
- **Priority**: HIGH - Release readiness
- **Acceptance Criteria**:
  - Complete performance envelope documented (what we can/cannot handle)
  - Scalability characteristics mapped from 10 to 2000+ documents
  - Resource requirements quantified for different scales
  - Known limitations honestly documented with workarounds
  - Performance SLAs established for different user scenarios
  - Competitive benchmarks validated (40-200x academic practice claims)
  - Release readiness assessment completed
- **Dependencies**: None
- **Effort**: 1-2 weeks

#### [ALPHA-003] Strategic Unit Testing Implementation

- **Description**: Design and implement focused unit testing strategy that tests what actually matters for a research platform
- **Purpose**: Focus on deterministic functions that can break silently and cause research failures
- **Priority**: HIGH - Quality assurance
- **Acceptance Criteria**:
  - Framework validation tests (schema parsing, required field checking, version compatibility)
  - Statistical calculation tests (ANOVA, correlations, effect sizes, significance calculations)
  - Data validation tests (score range validation, evidence quotation validation, JSON schema compliance)
  - All tests run in < 30 seconds with no flaky or non-deterministic tests
  - Test coverage ≥ 70% for critical modules
- **Dependencies**: None
- **Effort**: 1-2 weeks

#### [ALPHA-004] Automated Unit Testing Infrastructure

- **Description**: Establish comprehensive automated unit testing infrastructure to catch regressions and ensure code quality
- **Purpose**: Create automated test suite that catches regressions and ensures code quality as we approach alpha release
- **Priority**: HIGH - Quality assurance
- **Acceptance Criteria**:
  - All existing tests pass without import errors
  - Automated test suite runs in < 30 seconds
  - GitHub Actions workflow executes on every commit
  - Test coverage ≥ 80% for core modules
  - All critical functions have unit tests
  - Agent functionality thoroughly tested with mocks
  - No flaky or non-deterministic tests
- **Dependencies**: [ALPHA-003]
- **Effort**: 1-2 weeks

#### [ALPHA-005] Alpha Release Notes and Migration Guide

- **Description**: Create comprehensive release notes and migration guide for Alpha Release
- **Purpose**: Provide complete documentation for users upgrading to Alpha Release
- **Priority**: MEDIUM - Documentation
- **Acceptance Criteria**:
  - Release notes complete with feature summary, breaking changes, performance improvements
  - Migration guide tested with examples provided
  - Framework migration (v7.1 → v7.2) documented
  - Evidence architecture adoption guide included
  - CLI updates and configuration changes documented
  - Upgrade checklist with pre-upgrade tasks, upgrade steps, post-upgrade validation
- **Dependencies**: [ALPHA-001], [ALPHA-002]
- **Effort**: 1 week

#### [ALPHA-006] Alpha Release Documentation Package

- **Description**: Create comprehensive documentation package for Alpha Release
- **Purpose**: Provide complete documentation for all user types and use cases
- **Priority**: MEDIUM - Documentation
- **Acceptance Criteria**:
  - User documentation complete (Getting Started Guide, Framework Author's Guide, Experiment Design Guide, CLI Reference, Best Practices Guide)
  - Academic documentation complete (Methodology Overview, Validation Approach, Evidence Architecture, Research Reproducibility Guide)
  - Technical documentation complete (Architecture Overview, API Reference, Configuration Guide, Deployment Guide)
  - All documentation reviewed and updated
  - Examples tested and verified
  - Links checked and working
  - PDF versions generated
  - Academic citations verified
- **Dependencies**: [ALPHA-001], [ALPHA-002]
- **Effort**: 2-3 weeks

---

## Current Sprint Planning

**Next Priority**: Sprint 16 (Alpha Release Preparation) - CRITICAL PRIORITY
**Status**: Ready for execution
**Dependencies**: None - can begin immediately
