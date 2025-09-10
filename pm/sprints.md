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
- ✅ **Sprint 11 COMPLETED**: Statistical preparation workflow and CSV export functionality fully implemented
- ✅ **Golden Run Archive System**: Complete research transparency package with provenance consolidation, input materials consolidation, and comprehensive documentation
- ✅ **RAG Engine Analysis**: Confirmed txtai as primary RAG engine, Typesense for fact checker
- ✅ **Dependencies Updated**: Added txtai>=5.0.0 to requirements.txt

**Current Focus**: System is stable with comprehensive validation, logging integrity, robust fallback handling, complete research transparency capabilities, and full statistical preparation workflow

---

## Current Sprint Planning

**Next Priority**: Sprint 12 (Statistical Preparation Provenance Integration) - HIGH PRIORITY
**Status**: Ready for execution
**Dependencies**: None - can begin immediately

---

## New Sprint Structure


---

### Sprint 12: Statistical Preparation Provenance Integration (HIGH PRIORITY)

**Timeline**: 2-3 weeks
**Goal**: Integrate statistical preparation workflows with provenance system using hybrid approach (runtime efficiency + archive completeness) and implement human-friendly directory structure

#### [PROV-001] ProvenanceOrganizer Integration

- **Description**: Integrate ProvenanceOrganizer into current orchestrator alongside existing results creation
- **Purpose**: Enable provenance organization during runs while maintaining current results functionality
- **Priority**: HIGH - Core provenance functionality
- **Acceptance Criteria**:
  - ProvenanceOrganizer called after results directory creation
  - `artifacts/` directory created with academic-standard structure
  - Symlinks created to shared cache artifacts
  - Provenance metadata generated and stored
  - Both `results/` and `artifacts/` directories coexist
  - No disruption to existing results creation
- **Dependencies**: None
- **Effort**: 1 week

#### [PROV-002] Enhanced Manifest Structure for Statistical Preparation

- **Description**: Implement enhanced manifest structure to track statistical preparation stages and modes
- **Purpose**: Enable proper tracking of different run modes and their artifacts
- **Priority**: HIGH - Provenance compliance
- **Acceptance Criteria**:
  - Manifest includes statistical preparation stage metadata
  - Mode-specific tracking (analysis-only, statistical-prep, skip-synthesis, complete)
  - Resume capability metadata stored
  - Artifact dependency tracking enhanced
- **Dependencies**: [PROV-001]
- **Effort**: 3-5 days

#### [PROV-003] Archive Command Enhancement for Statistical Preparation

- **Description**: Enhance archive command to handle different run modes and include complete session logs and artifact content
- **Purpose**: Create mode-aware, self-contained archives for all run types with ALL necessary assets for replication and audit
- **Priority**: HIGH - Research integrity
- **Acceptance Criteria**:
  - Session logs copied to archive (`session_logs/` directory) with complete execution logs
  - Actual artifact content copied (not just symlinks) to `artifacts/` directory
  - Statistical package created for statistical prep runs
  - Mode-specific README generation
  - Complete self-contained archives (no external dependencies, no broken symlinks)
  - Archive command works for all run modes
  - Both `results/` and `artifacts/` directories included in archive
  - Experiment.md and framework files properly located in `inputs/` directory
  - All LLM interactions, agent logs, system logs, and error logs preserved
  - Complete provenance chain with actual artifact content for audit verification
- **Dependencies**: [PROV-002]
- **Effort**: 1 week

#### [PROV-004] Statistical Package Generation

- **Description**: Implement statistical package generation for statistical preparation runs
- **Purpose**: Create researcher-ready packages with all necessary files and documentation
- **Priority**: MEDIUM - User experience
- **Acceptance Criteria**:
  - `statistical_package/` directory created for statistical prep runs
  - Researcher-ready CSV files with proper naming
  - Variable codebook generation
  - Import scripts for R/Python/STATA
  - Plain text usage instructions
- **Dependencies**: [PROV-003]
- **Effort**: 3-5 days

#### [PROV-005] Directory Structure Reorganization

- **Description**: Implement human-friendly directory structure for all run types with complete asset preservation
- **Purpose**: Create logical organization that meets expectations of researchers, replication researchers, and auditors with ALL necessary assets
- **Priority**: HIGH - User experience and research integrity
- **Acceptance Criteria**:
  - Clear separation: data/, outputs/, inputs/, provenance/, artifacts/, session_logs/
  - README files explaining each directory and its contents
  - No file duplication between root and results
  - Consistent naming conventions
  - Audit-friendly provenance organization
  - Self-contained archives with clear structure
  - Complete session logs in session_logs/ directory
  - Actual artifact content (not symlinks) in artifacts/ directory
  - All LLM interactions, agent logs, system logs, and error logs preserved
  - Complete provenance chain with actual artifact content for audit verification
- **Dependencies**: [PROV-001]
- **Effort**: 1 week

#### [PROV-006] Session Logs and Artifact Content Copying Implementation

- **Description**: Implement actual copying of session logs and artifact content (not symlinks) in archive command
- **Purpose**: Ensure complete self-contained archives with all necessary assets for replication and audit
- **Priority**: HIGH - Research integrity
- **Acceptance Criteria**:
  - Session logs copied from `session/{SESSION_ID}/logs/` to `session_logs/logs/` in archive
  - All artifact content copied from shared cache to `artifacts/` directory (not symlinks)
  - Archive command creates completely self-contained archives
  - No broken symlinks or external dependencies in archives
  - Complete LLM interactions, agent logs, system logs, and error logs preserved
  - All artifacts accessible without shared cache dependency
- **Dependencies**: [PROV-003]
- **Effort**: 1 week

#### [PROV-007] Git Integration for Statistical Preparation

- **Description**: Implement mode-aware Git commit messages and branch strategies
- **Purpose**: Enable proper version control for different run types
- **Priority**: MEDIUM - Version control
- **Acceptance Criteria**:
  - Different commit messages for different run modes
  - Statistical prep runs clearly identified in Git history
  - Resume commits properly linked to original statistical prep runs
  - Git integration works with archive command
- **Dependencies**: [PROV-002, PROV-005, PROV-006]
- **Effort**: 2-3 days

#### [PROV-008] Alpha Hardening (Provenance & CLI) — COMPLETED

- **Description**: Hardening tasks required for a reliable alpha: logging cleanup, robust Git auto-commit, accurate run-mode detection, reorganizer idempotency/clarity, archive security checks, minimal test coverage, and CLI UX consistency.
- **Purpose**: Eliminate fragile paths and silent failures; ensure predictable behavior for alpha users.
- **Priority**: CRITICAL - Alpha readiness
- **Acceptance Criteria**:
  - Logging cleanup: replace remaining `print()` paths in orchestrator/helpers with structured logging; respect verbosity levels
  - Git auto-commit robustness: repo root detected by `.git` discovery or `git rev-parse --show-toplevel`; no path-depth assumptions
  - Run mode detection: `_detect_run_mode` reads enhanced manifest (`run_mode.mode_type`) reliably; no "unknown" for supported modes
  - Reorganizer idempotency: safe to run multiple times; skip already-moved files; either remove empty `results/` or add sentinel README explaining deprecation in favor of `data/`/`outputs/`/`inputs/`
  - Archive security: validate symlink targets before copying; only copy when resolved paths are under experiment `shared_cache` or repo root; warn and skip otherwise
  - Minimal tests: unit tests for `DirectoryStructureReorganizer`, archive helpers (`_copy_session_logs`, `_copy_artifact_content`, `_detect_run_mode`), `EnhancedManifest` (`set_run_mode`, `set_resume_capability`, `finalize_manifest`), and `StatisticalPackageGenerator` (files + exec bits). One integration test: run `--statistical-prep` then `archive` with all flags and assert no symlinks, complete logs, expected READMEs
  - CLI UX consistency: CLI help/defaults for archive flags match documentation; clear skip messages respect future quiet mode
- **Dependencies**: [PROV-002], [PROV-003], [PROV-004], [PROV-005], [PROV-006], [PROV-007]
- **Effort**: 1-1.5 weeks

---

### Sprint 13: Essential Code Quality & Architecture Cleanup (HIGH PRIORITY)

**Timeline**: 2-3 weeks
**Goal**: Clean up critical dead code, remove deprecated components, and update essential architecture documentation

#### [CLEANUP-001] Essential Dead Code Inventory

- **Description**: Conduct focused inventory for critical dead code that impacts alpha users
- **Purpose**: Identify and prioritize removal of unused code that creates confusion or maintenance burden
- **Priority**: HIGH - Code quality improvement
- **Acceptance Criteria**:
  - Identify dead imports and unused dependencies
  - Catalog deprecated agent patterns and unused directories
  - Prioritize cleanup based on alpha user impact
  - Document findings for systematic removal
- **Dependencies**: None
- **Effort**: 1 week

#### [CLEANUP-002] Remove Deprecated Fact Checker and Revision Agents

- **Description**: Remove disabled fact checker and revision agents that still generate confusing artifacts
- **Purpose**: Clean up agents that are disabled but still create artifacts, causing user confusion
- **Priority**: HIGH - Alpha user experience
- **Acceptance Criteria**:
  - Remove `fact_checker_agent/` and `revision_agent/` directories
  - Stop generating `fact_check_results.json` artifacts
  - Remove unused imports from orchestrator
  - Clean up or remove related test files
  - Update architecture documentation to remove references
  - Verify no fact-check artifacts appear in results directories
- **Dependencies**: [CLEANUP-001]
- **Effort**: 2-3 days

#### [CLEANUP-003] Critical Dead Dependencies and Architecture Updates

- **Description**: Remove critical dead dependencies and update essential architecture documentation
- **Purpose**: Remove technical debt that impacts alpha users and align documentation with actual implementation
- **Priority**: HIGH - Technical debt and documentation
- **Acceptance Criteria**:
  - Remove Redis dependencies from requirements.txt and pyproject.toml
  - Remove MinIO references from Makefile and scripts
  - Clean up deprecated orchestrator patterns and unused agent directories
  - Update DISCERNUS_SYSTEM_ARCHITECTURE.md to reflect current 3-stage pipeline
  - Update CURSOR_AGENT_QUICK_START.md to reflect current architecture
  - All critical dead dependencies removed and deprecated code cleaned up
- **Dependencies**: [CLEANUP-001], [CLEANUP-002]
- **Effort**: 1-2 weeks

#### [CLEANUP-004] Essential Architecture Document Updates

- **Description**: Update essential architecture documentation to reflect current state
- **Purpose**: Keep critical architecture documentation current and accurate for alpha users
- **Priority**: MEDIUM - Documentation maintenance
- **Acceptance Criteria**:
  - Update system architecture document with current agent list
  - Remove references to deprecated agents and patterns
  - Ensure documentation matches actual implementation
  - Verify all links and references are current
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

### Sprint 15: Essential Academic Quality & Documentation (HIGH PRIORITY)

**Timeline**: 2-3 weeks
**Goal**: Implement essential academic quality standards and documentation for alpha release

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

#### [ACADEMIC-007] Documentation Pass

- **Description**: Conduct comprehensive documentation pass
- **Purpose**: Ensure all documentation is current, accurate, and complete
- **Priority**: MEDIUM - Documentation quality
- **Dependencies**: [ACADEMIC-001], [ACADEMIC-002]
- **Effort**: 1-2 weeks

---

### Sprint 16: Alpha Release Preparation (CRITICAL PRIORITY)

**Description**: Essential items required for alpha release readiness
**Purpose**: Ensure system is ready for alpha release with essential testing, basic documentation, and core performance validation
**Priority**: CRITICAL - Alpha release blockers
**Timeline**: 2-3 weeks - must complete before alpha release
**Dependencies**: None - can begin immediately

#### [ALPHA-001] Essential Test Gauntlet Run

- **Description**: Run essential test suite to validate Alpha Release readiness
- **Purpose**: Ensure core systems work correctly before release
- **Priority**: HIGH - Release validation
- **Acceptance Criteria**:
  - Core functionality tests passing (CLI, analysis, synthesis)
  - Framework validation tests for v7.2 frameworks
  - Evidence architecture basic validation
  - Integration tests for end-to-end workflows
  - No critical regressions detected
  - Results documented
- **Dependencies**: None
- **Effort**: 1 week

#### [ALPHA-002] Core Performance & Scalability Validation

- **Description**: Validate core performance characteristics and document basic scalability limits
- **Purpose**: Provide essential performance information for alpha users
- **Priority**: HIGH - Release readiness
- **Acceptance Criteria**:
  - Basic performance envelope documented (10-100 documents)
  - Resource requirements quantified for small-medium scales
  - Known limitations documented with basic workarounds
  - Performance targets validated for alpha use cases
  - Release readiness assessment completed
- **Dependencies**: None
- **Effort**: 1 week

#### [ALPHA-003] Essential Unit Testing Implementation

- **Description**: Implement focused unit testing for critical functions that can break silently
- **Purpose**: Prevent silent failures that could break research
- **Priority**: HIGH - Quality assurance
- **Acceptance Criteria**:
  - Framework validation tests (schema parsing, required field checking)
  - Statistical calculation tests (basic ANOVA, correlations, effect sizes)
  - Data validation tests (score range validation, JSON schema compliance)
  - All tests run in < 30 seconds with no flaky tests
  - Test coverage ≥ 60% for critical modules
- **Dependencies**: None
- **Effort**: 1 week

#### [ALPHA-004] Basic Automated Testing Infrastructure

- **Description**: Establish basic automated testing infrastructure for regression prevention
- **Purpose**: Catch regressions and maintain code quality during alpha development
- **Priority**: HIGH - Quality assurance
- **Acceptance Criteria**:
  - All existing tests pass without import errors
  - Automated test suite runs in < 30 seconds
  - Basic GitHub Actions workflow for core tests
  - Test coverage ≥ 60% for core modules
  - Critical functions have unit tests
  - No flaky or non-deterministic tests
- **Dependencies**: [ALPHA-003]
- **Effort**: 1 week

#### [ALPHA-005] Essential Alpha Documentation

- **Description**: Create essential documentation for Alpha Release including installation and setup
- **Purpose**: Provide basic documentation for alpha users to get started
- **Priority**: HIGH - Essential for alpha users
- **Acceptance Criteria**:
  - Basic installation guide with Vertex AI Gemini setup
  - Essential release notes with key features and breaking changes
  - Basic CLI reference and configuration guide
  - Simple getting started guide with example experiment
  - All documentation reviewed and up-to-date
  - Outdated documentation removed from project
- **Dependencies**: [ALPHA-001], [ALPHA-002]
- **Effort**: 1 week

---

## Current Sprint Planning

**Next Priority**: Sprint 16 (Alpha Release Preparation) - CRITICAL PRIORITY
**Status**: Ready for execution
**Dependencies**: None - can begin immediately
