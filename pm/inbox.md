# Inbox - Raw Backlog Items

**Purpose**: Raw capture of backlog items without organization or sprint planning. Items here will be groomed into organized sprints later.

**Usage**:

- "inbox this" → append new items here with minimal formatting
- "groom our sprints" → move all items from here to sprints.md with proper organization

---

## Agent & Component Restoration

### CSV Export Agent Restoration
**Task**: Bring back the CSV export agent from `/Volumes/code/discernus/discernus/agents/csv_export_agent`
**Purpose**: Restore CSV export functionality for data analysis workflows
**Priority**: MEDIUM - Restoring existing functionality

### Skip Synthesis Offramp Option
**Task**: Bring back the "skip synthesis" offramp option
**Purpose**: Allow users to run analysis-only workflows without synthesis phase
**Priority**: MEDIUM - Workflow flexibility improvement

### Provenance Components Restoration
**Task**: Restore provenance components:
- `/Volumes/code/discernus/discernus/core/provenance_organizer.py`
- `/Volumes/code/discernus/discernus/core/provenance_stamp.py`
- `/Volumes/code/discernus/discernus/core/provenance_visualizer.py`
**Purpose**: Restore full provenance system functionality
**Priority**: HIGH - Core system functionality

## System Architecture & Compliance

### Provenance System Compliance
**Task**: Comply with provenance, provenance validation, and dual-track logging documents:
- @PROVENANCE_SYSTEM.md
- @DUAL_TRACK_LOGGING_ARCHITECTURE.md
- @INTEGRATED_PROVENANCE_VALIDATION_SPEC.md
**Purpose**: Ensure system meets documented architectural standards
**Priority**: HIGH - Architecture compliance

### System Architecture Document Update
**Task**: Update the system architecture document to reflect current state
**Purpose**: Keep architecture documentation current and accurate
**Priority**: MEDIUM - Documentation maintenance

## Agent Cleanup & Code Quality

### Remove Revision Agent and Fact Checker Agent
**Task**: Remove the revision agent and fact checker agent
**Purpose**: Clean up unused or deprecated agent components
**Priority**: MEDIUM - Code cleanup

### Dead Code Inventory
**Task**: Conduct comprehensive inventory for dead code
**Purpose**: Identify and remove unused code to improve maintainability
**Priority**: MEDIUM - Code quality improvement

## Open Source & Release Management

### Open Source License Audit
**Task**: Conduct open source license audit
**Purpose**: Ensure compliance with all open source dependencies
**Priority**: HIGH - Legal compliance

### Open Source License Insertion
**Task**: Insert appropriate open source licenses
**Purpose**: Properly license the project for open source distribution
**Priority**: HIGH - Legal compliance

### Release Process
**Task**: Establish release process
**Purpose**: Define how to create and distribute releases
**Priority**: MEDIUM - Process establishment

### Documentation Pass
**Task**: Conduct comprehensive documentation pass
**Purpose**: Ensure all documentation is current, accurate, and complete
**Priority**: MEDIUM - Documentation quality

## System Architecture & Compliance



## GitHub Issues - Alpha Quality & Hygiene



### Issue #365: Epic - Academic Quality & Standards Implementation
**Task**: Implement comprehensive academic standards, peer review preparation, quality assurance frameworks, and THIN compliance cleanup
**Purpose**: Ensure Discernus outputs meet top-tier academic journal requirements and stakeholders have complete understanding of system capabilities
**Priority**: HIGH - Academic excellence
**Acceptance Criteria**:
- Evidence standards match top academic journals with >3 sources per claim
- Automated quality scoring >80% with evidence hallucination detection
- Performance audit completed with scalability characterization
- Complete agent architecture documentation with THIN compliance validation
- Peer review ready quality standards implemented

### Issue #351: Academic Output Standards Implementation
**Task**: Implement academic-grade output formatting standards for evidence-infused reports with footnote systems and provenance transparency
**Purpose**: Create publication-ready reports with complete audit trails and multi-audience integration
**Priority**: HIGH - Academic standards
**Acceptance Criteria**:
- Numbered footnotes for all evidence citations with full provenance chains
- "Evidence Provenance" section with complete audit trail
- Multi-audience integration (scanner/collaborator/transparency sections)
- Academic-quality formatting meeting peer-review publication standards
- Verifiable claim-to-source mapping for reproducibility

### Issue #302: Enhance Methodology Transparency with Framework Operationalization
**Task**: Enhance methodology transparency by explaining how abstract framework concepts are operationalized into measurable indicators
**Purpose**: Provide academic readers with clear understanding of what specific linguistic features or thematic markers are being measured
**Priority**: MEDIUM - Academic transparency
**Acceptance Criteria**:
- Concise methodology section (1-2 paragraphs) in every final report
- Framework operationalization explicitly explained for each dimension
- Analysis process from raw text to scores clearly documented
- Sufficient detail provided for independent replication

### Issue #303: Pydantic Serialization Warning in Audit Logging
**Task**: Fix Pydantic serialization warnings when LiteLLM response objects are logged
**Problem**: UserWarning appears during audit logging: "Expected 9 fields but got 5: Expected `Message` - serialized value may not be as expected"
**Impact**: Log noise, no data corruption or functionality issues
**Root Cause**: LiteLLM response objects don't perfectly align with Pydantic model expectations during JSON serialization
**Priority**: LOW - Cosmetic issue, no production impact
**Acceptance Criteria**:
- Eliminate Pydantic serialization warnings in audit logs
- Maintain data integrity and functionality
- Preserve complete audit trail accuracy
**Solution Options**:
- Custom JSON serializer for LiteLLM objects in audit logger
- Convert LiteLLM objects to plain dicts before logging
- Suppress specific Pydantic warnings for LiteLLM objects
- Academic readers can understand methodology without expert knowledge

### Issue #301: Implement Defensive Prompting to Constrain LLM Over-Generalization
**Task**: Implement system of defensive prompting to make analysis more robust against LLM over-generalization and hallucination
**Purpose**: Add constraints and negative instructions to prevent inappropriate scoring based on speaker identity or other biases
**Priority**: MEDIUM - Quality assurance
**Acceptance Criteria**:
- New constraints object added to framework schema
- Framework parser updated to append constraints to LLM prompts
- Methodology section includes summary of defensive prompts used
- Constraints prevent scoring based on speaker identity or other inappropriate factors

### Issue #292: Epic - Research Integrity & Provenance Architecture Enhancement
**Task**: Enhance existing provenance architecture by fixing connection points, adding validation, and improving human comprehension
**Purpose**: Fix critical provenance chain breaks and create human-comprehensible artifact organization for academic transparency
**Priority**: HIGH - Research integrity
**Acceptance Criteria**:
- Zero empty CSV files, all statistical results properly exported
- Human-comprehensible artifact organization with readable names
- Complete provenance visualization tools and browser interface
- External reviewers can validate findings in <2 minutes
- Platform meets highest academic standards for transparency

### Issue #249: Create Unified Results Dashboard for Researcher-Centric Information Architecture
**Task**: Design and implement unified, human-readable results dashboard to replace scattered CSVs and markdown reports
**Purpose**: Provide single, clear dashboard that significantly improves user experience and researcher workflow
**Priority**: MEDIUM - User experience
**Acceptance Criteria**:
- New dashboard agent created that ingests all final artifacts
- Generates single, standalone HTML file in run's results directory
- Presents key findings, summary statistics, and visualizations in clear, interactive format
- Replaces current scattered CSV and markdown output approach

### Issue #30: Audit and Fix Directory Creation Logic to Comply with Provenance Standard
**Task**: Audit codebase to find and fix logic that creates incorrect directory structures, ensuring compliance with v3 provenance standard
**Purpose**: Fix non-compliant directory structures and create migration script for legacy project data
**Priority**: HIGH - Provenance compliance
**Acceptance Criteria**:
- All new experiments create correct `projects/{PROJECT}/sessions/{SESSION}` structure
- Migration script successfully reorganizes all legacy project data
- Root `/projects` directory clean of non-compliant project folders
- Tests verify correct directory structure creation

## GitHub Issues - Alpha Release Close Down

### Issue #406: Implement User-Friendly Messaging for Statistical Preparation Mode
**Task**: Implement user-friendly messaging for statistical preparation mode to improve user experience and clarity
**Purpose**: Provide clear messaging about what statistical preparation mode does, when to use it, and what outputs to expect
**Priority**: MEDIUM - User experience
**Acceptance Criteria**:
- Clear messaging about statistical preparation mode functionality
- User guidance on when to use statistical preparation vs full synthesis
- Clear explanation of expected outputs and deliverables
- Improved user experience for statistical preparation workflow

### Issue #400: Clean Up Dead Code and Update Architecture Documentation
**Task**: Clean up dead code and update architecture documentation to align with current 3-stage unified pipeline
**Purpose**: Remove technical debt and align documentation with actual implementation
**Priority**: HIGH - Technical debt and documentation
**Acceptance Criteria**:
- Remove Redis dependencies from requirements.txt and pyproject.toml
- Remove MinIO references from Makefile and scripts
- Clean up deprecated orchestrator patterns and unused agent directories
- Update DISCERNUS_SYSTEM_ARCHITECTURE.md to reflect current 3-stage pipeline
- Update CURSOR_AGENT_QUICK_START.md to reflect current architecture
- All dead dependencies removed and deprecated code cleaned up

### Issue #368: Comprehensive Performance & Scalability Audit for Release Readiness
**Task**: Conduct comprehensive system-wide performance audit to establish clear understanding of capabilities and limitations
**Purpose**: Provide transparent documentation for users and stakeholders about system performance envelope
**Priority**: HIGH - Release readiness
**Acceptance Criteria**:
- Complete performance envelope documented (what we can/cannot handle)
- Scalability characteristics mapped from 10 to 2000+ documents
- Resource requirements quantified for different scales
- Known limitations honestly documented with workarounds
- Performance SLAs established for different user scenarios
- Competitive benchmarks validated (40-200x academic practice claims)
- Release readiness assessment completed

### Issue #333: Epic - Strategic Unit Testing for Discernus Research Platform
**Task**: Design and implement focused unit testing strategy that tests what actually matters for a research platform
**Purpose**: Focus on deterministic functions that can break silently and cause research failures
**Priority**: HIGH - Quality assurance
**Acceptance Criteria**:
- Framework validation tests (schema parsing, required field checking, version compatibility)
- Statistical calculation tests (ANOVA, correlations, effect sizes, significance calculations)
- Data validation tests (score range validation, evidence quotation validation, JSON schema compliance)
- All tests run in < 30 seconds with no flaky or non-deterministic tests
- Test coverage ≥ 70% for critical modules

### Issue #332: Epic - Automated Unit Testing Infrastructure for Alpha Quality
**Task**: Establish comprehensive automated unit testing infrastructure to catch regressions and ensure code quality
**Purpose**: Create automated test suite that catches regressions and ensures code quality as we approach alpha release
**Priority**: HIGH - Quality assurance
**Acceptance Criteria**:
- All existing tests pass without import errors
- Automated test suite runs in < 30 seconds
- GitHub Actions workflow executes on every commit
- Test coverage ≥ 80% for core modules
- All critical functions have unit tests
- Agent functionality thoroughly tested with mocks
- No flaky or non-deterministic tests

### Issue #312: Release - Alpha Release Notes and Migration Guide
**Task**: Create comprehensive release notes and migration guide for Alpha Release
**Purpose**: Provide complete documentation for users upgrading to Alpha Release
**Priority**: MEDIUM - Documentation
**Acceptance Criteria**:
- Release notes complete with feature summary, breaking changes, performance improvements
- Migration guide tested with examples provided
- Framework migration (v7.1 → v7.2) documented
- Evidence architecture adoption guide included
- CLI updates and configuration changes documented
- Upgrade checklist with pre-upgrade tasks, upgrade steps, post-upgrade validation

### Issue #311: Performance - Alpha Release Performance Validation
**Task**: Conduct comprehensive performance validation for Alpha Release
**Purpose**: Validate system performance across all areas before release
**Priority**: MEDIUM - Performance validation
**Acceptance Criteria**:
- Performance metrics documented across all areas
- LLM optimization validated (token usage efficiency, response time, cost metrics)
- System performance validated (memory usage, disk I/O, CPU utilization)
- Scalability tests completed (large corpus handling, multi-framework processing)
- Optimization recommendations provided
- Resource usage guidelines established
- Cost projections documented

### Issue #310: Validation - Complete Test Gauntlet Run
**Task**: Run complete test gauntlet to validate Alpha Release readiness
**Purpose**: Ensure all systems work correctly before release
**Priority**: HIGH - Release validation
**Acceptance Criteria**:
- All tests passing across all categories
- Framework tests completed (all v7.2 frameworks, migration validation, edge cases)
- Evidence architecture tests completed (three-track validation, evidence retention metrics)
- Performance tests completed (response times, token usage, resource utilization)
- Integration tests completed (end-to-end workflows, CLI functionality, error handling)
- Performance metrics meet targets
- No regressions detected
- Results documented

### Issue #309: Documentation - Alpha Release Documentation Package
**Task**: Create comprehensive documentation package for Alpha Release
**Purpose**: Provide complete documentation for all user types and use cases
**Priority**: MEDIUM - Documentation
**Acceptance Criteria**:
- User documentation complete (Getting Started Guide, Framework Author's Guide, Experiment Design Guide, CLI Reference, Best Practices Guide)
- Academic documentation complete (Methodology Overview, Validation Approach, Evidence Architecture, Research Reproducibility Guide)
- Technical documentation complete (Architecture Overview, API Reference, Configuration Guide, Deployment Guide)
- All documentation reviewed and updated
- Examples tested and verified
- Links checked and working
- PDF versions generated
- Academic citations verified

## GitHub Issues - Strategic Planning & Architecture

### Issue #420: GitHub Strategy - Clean Separation of Development vs Open Source Code
**Task**: Establish strategy for cleanly separating internal development code from open source version
**Purpose**: Protect internal IP while enabling community contribution and professional open source release
**Priority**: HIGH - Open source strategy
**Acceptance Criteria**:
- Repository structure planned (main repo vs internal development repos)
- Branch strategy established (main branch open source vs development branches)
- Feature flags implemented for internal features disabled in open source builds
- Configuration management for environment-specific feature enablement
- Contribution guidelines and boundaries clearly established
- Open source release pipeline created
- Internal IP protected while open source version remains professional and complete

### Issue #419: Project Open Source License Dependencies and Business Strategy Alignment
**Task**: Ensure all project dependencies are license-compatible with business strategy
**Purpose**: Audit all third-party dependencies for license compatibility and identify potential conflicts with future commercial offerings
**Priority**: HIGH - Business strategy foundation
**Acceptance Criteria**:
- Complete dependency license audit across all components
- License compatibility matrix created for all dependencies
- Conflict resolution strategy established for incompatible dependencies
- Alternative dependency evaluation completed where conflicts exist
- License compliance monitoring system established
- Business impact assessment completed for all dependencies
- All dependencies confirmed license-compatible with business strategy
- Risk mitigation plan in place for any identified conflicts

### Issue #418: Epic - Open Source License Selection and Implementation
**Task**: Select and implement appropriate open source license for Discernus
**Purpose**: Balance open source adoption with business strategy while protecting intellectual property and enabling community contribution
**Priority**: HIGH - Foundation for open source release
**Acceptance Criteria**:
- License research and evaluation completed across all options (MIT/Apache 2.0, GPL v3, AGPL v3, dual licensing)
- Business strategy alignment assessment completed
- Legal review and compliance verification completed
- License implementation across entire codebase
- Contributor license agreement (CLA) setup completed
- License documentation and notices added throughout codebase
- Business strategy aligned with selected license
- Full codebase compliance with selected license confirmed

## GitHub Issues - Research & Development

### Issue #381: Research Spike - Corpus RAG Integration Strategy
**Task**: Investigate integration strategy for corpus RAG (Retrieval-Augmented Generation) to enhance research capabilities
**Purpose**: Enhance research capabilities with intelligent corpus discovery and validation through RAG integration
**Priority**: MEDIUM - Research enhancement
**Acceptance Criteria**:
- Value proposition analysis completed for corpus RAG integration
- Content isolation strategies designed and documented
- Academic integrity preservation methods established
- Scalability and performance considerations analyzed
- Technical architecture design completed
- Controlled testing plan developed
- Production integration strategy defined (if validated)

### Issue #344: APDES Early Populist Emergence Collection (2008-2012)
**Task**: Create comprehensive collection of early populist emergence speeches and documents from 2008-2012 period
**Purpose**: Document early populist emergence patterns including financial crisis responses, Tea Party emergence, and populist consolidation
**Priority**: MEDIUM - Research collection
**Acceptance Criteria**:
- Financial crisis populist responses collected and documented
- Tea Party electoral emergence speeches gathered
- Populist consolidation patterns identified and catalogued
- Dual populist origins documented (left and right)
- Foundational patterns established
- Multi-method collection strategy implemented
- Standard APDES metadata applied
- Early populist-specific metadata added

### Issue #343: APDES Baseline Senate and Gubernatorial Race Collection (2012-2014)
**Task**: Establish baseline collection of pre-populist institutional patterns through Senate and gubernatorial race speeches
**Purpose**: Provide comparative analysis opportunities and foundational establishment of pre-populist discourse patterns
**Priority**: MEDIUM - Research collection
**Acceptance Criteria**:
- 2012 election cycle pre-populist baseline established
- 2014 election cycle pre-populist baseline established
- Pre-populist institutional patterns documented
- Comparative analysis opportunities identified
- Speech selection criteria defined and applied
- Multi-method collection strategy implemented
- Standard APDES metadata applied
- Baseline-specific metadata added

### Issue #342: APDES Swing State Senate Race Collection
**Task**: Create comprehensive collection of swing state Senate race speeches across multiple election cycles
**Purpose**: Analyze populist discourse evolution and provide corpus diversity enhancement for analytical research
**Priority**: MEDIUM - Research collection
**Acceptance Criteria**:
- 2016 election cycle speeches collected
- 2018 election cycle speeches collected
- 2020 election cycle speeches collected
- 2022 election cycle speeches collected
- 2024 election cycle speeches collected
- Speech selection criteria defined and applied
- Multi-method collection strategy implemented
- Standard APDES metadata applied
- Senate race-specific metadata added
- Corpus diversity enhancement achieved

### Issue #341: APDES Corpus Metadata Refinement and Integration
**Task**: Refine and integrate APDES corpus metadata with standardized schema and quality assurance
**Purpose**: Ensure comprehensive corpus organization and validation for research analysis
**Priority**: MEDIUM - Research infrastructure
**Acceptance Criteria**:
- Standard APDES metadata schema implemented
- Era-specific metadata enhancement completed
- Quality assurance metadata added
- Corpus manifest updates completed
- Framework analysis preparation completed
- Metadata audit completed (4-6 hours)
- Metadata enhancement completed (6-8 hours)
- Quality assurance completed (4-6 hours)
- Integration and validation completed (3-4 hours)

### Issue #340: APDES Era 4 Collection - Populist Consolidation (2024)
**Task**: Collect and organize populist consolidation era documents from 2024
**Purpose**: Document populist consolidation patterns and discourse evolution in the current era
**Priority**: MEDIUM - Research collection
**Acceptance Criteria**:
- Collection targets of 55-68 documents achieved
- Multi-method collection strategy implemented
- Quality assurance protocols applied
- Comprehensive metadata requirements met
- Populist consolidation patterns documented
- Discourse evolution analysis prepared
- Standard APDES metadata applied
- Era-specific metadata added

### Issue #339: APDES Era 3 Collection - Institutional Crisis (2020-2021)
**Task**: Create collection of institutional crisis era documents from 2020-2021 period
**Purpose**: Analyze institutional crisis discourse and populist responses during crisis period
**Priority**: MEDIUM - Research collection
**Acceptance Criteria**:
- Collection targets of 45-57 documents achieved
- Multi-method collection strategy implemented
- Quality assurance protocols applied
- Comprehensive metadata requirements met
- Institutional crisis discourse documented
- Populist responses during crisis analyzed
- Standard APDES metadata applied
- Era-specific metadata added

### Issue #338: APDES Era 2.5 Collection - Populist Governance Transition (2017-2019)
**Task**: Organize populist governance transition era documents from 2017-2019
**Purpose**: Analyze populist governance transition patterns and discourse evolution
**Priority**: MEDIUM - Research collection
**Acceptance Criteria**:
- Collection targets of 24-30 documents achieved
- Multi-method collection strategy implemented
- Quality assurance protocols applied
- Comprehensive metadata requirements met
- Populist governance transition patterns documented
- Discourse evolution during transition analyzed
- Standard APDES metadata applied
- Era-specific metadata added

### Issue #337: APDES Academic Presentation and Outreach Materials
**Task**: Create academic presentation and outreach materials for APDES research
**Purpose**: Prepare comprehensive academic presentation materials and outreach strategy for APDES research
**Priority**: MEDIUM - Academic presentation
**Acceptance Criteria**:
- Faithful replication stage materials prepared
- Enhanced analysis stage materials prepared
- Advanced analytics stage materials prepared
- Primary targets identified and documented
- Outreach materials created
- Academic engagement strategy developed
- Research impact documentation completed
- Platform adoption strategy defined

### Issue #336: APDES Framework Execution and Validation
**Task**: Execute and validate APDES framework with comprehensive testing and validation
**Purpose**: Ensure APDES framework works correctly and produces valid research results
**Priority**: MEDIUM - Framework validation
**Acceptance Criteria**:
- Faithful replication stage completed
- Enhanced analysis stage completed
- Advanced analytics stage completed
- Benchmark comparison completed
- Statistical testing completed
- Framework reliability validated
- Technical validation completed
- Academic extensions prepared

### Issue #279: Research Spike - Populist Rhetorical Cascade Theory
**Task**: Investigate populist rhetorical cascade theory through research spike
**Purpose**: Understand rhetorical pattern evolution and cascade effects in populist discourse
**Priority**: MEDIUM - Research investigation
**Acceptance Criteria**:
- Populist rhetorical cascade theory investigated
- Rhetorical pattern evolution analyzed
- Cascade effects in populist discourse documented
- Research spike methodology completed
- Findings documented and analyzed
- Theoretical framework developed
- Research implications identified

### Issue #274: Epic - APDES American Populist Discourse Evolution Study (1992-2024 Longitudinal Analysis)
**Task**: Conduct comprehensive longitudinal analysis of American populist discourse evolution
**Purpose**: Provide comprehensive analysis of populist discourse evolution over three decades
**Priority**: HIGH - Major research study
**Acceptance Criteria**:
- Faithful replication stage completed
- Enhanced analysis stage completed
- Advanced analytics stage completed
- Framework specifications implemented
- Academic presentation strategy developed
- Immediate validation completed
- Academic extensions prepared
- Research innovation documented

### Issue #244: Quantitative Grammar Architecture - Statistical Output Interface Standardization
**Task**: Implement quantitative grammar architecture with statistical output interface standardization
**Purpose**: Standardize statistical output formats and improve data processing consistency
**Priority**: MEDIUM - Architecture enhancement
**Acceptance Criteria**:
- Core grammar infrastructure implemented
- Framework extensions completed
- Adaptive bridge developed
- Statistical output interface standardized
- Core components implemented
- Example structure documented
- Phase 1 core grammar infrastructure completed
- Phase 2 framework extensions completed
- Phase 3 adaptive bridge completed

### Issue #240: EPIC - Academic Research-Aligned LLM Ensemble Strategy Implementation
**Task**: Implement academic research-aligned LLM ensemble strategy
**Purpose**: Enhance research quality through ensemble methodology and academic validation
**Priority**: HIGH - Research methodology
**Acceptance Criteria**:
- Foundation implementation completed
- Self-consistency ensemble implemented
- Multi-model ensemble implemented
- Parameter integration and optimization completed
- Academic validation and documentation completed
- Architecture integration completed
- Parameter strategy alignment completed
- Quality assurance framework implemented

### Issue #233: Implement Reliability and Resilience Metrics Tracking
**Task**: Implement comprehensive reliability and resilience metrics tracking system
**Purpose**: Monitor system performance and ensure consistent operation across different use cases
**Priority**: MEDIUM - System monitoring
**Acceptance Criteria**:
- Reliability and resilience metrics tracking implemented
- System performance monitoring established
- Failure pattern identification system created
- Consistent operation validation completed
- Performance metrics documented
- Monitoring infrastructure deployed
- Alerting system implemented
- Performance optimization recommendations provided

### Issue #232: Maintain Read-Only Parsing for Existing CSV Experiment Results
**Task**: Maintain read-only parsing capabilities for existing CSV experiment results
**Purpose**: Ensure backward compatibility and support for legacy experiment data formats
**Priority**: MEDIUM - Backward compatibility
**Acceptance Criteria**:
- Read-only parsing for existing CSV experiment results maintained
- Backward compatibility ensured
- Legacy experiment data format support provided
- Current implementation preserved
- Technical implementation completed
- Data migration support provided
- Legacy format validation maintained
- Transition strategy documented

### Issue #230: Deploy Unified JSON Processing Pipeline
**Task**: Deploy unified JSON processing pipeline to standardize data processing
**Purpose**: Improve consistency and ensure reliable data handling throughout the analysis workflow
**Priority**: MEDIUM - Data processing
**Acceptance Criteria**:
- Unified JSON processing pipeline deployed
- Data processing standardized across system
- Consistency improved throughout workflow
- Reliable data handling ensured
- Technical implementation completed
- Validation results documented
- Performance improvements achieved
- Error handling enhanced

### Issue #226: Convert All Reference and Seed Frameworks to JSON Specification
**Task**: Convert all reference and seed frameworks to JSON specification format
**Purpose**: Standardize framework definitions and improve maintainability
**Priority**: MEDIUM - Framework standardization
**Acceptance Criteria**:
- All reference frameworks converted to JSON specification
- All seed frameworks converted to JSON specification
- Framework definitions standardized
- Maintainability improved
- Consistent framework processing ensured
- Technical implementation completed
- Remaining work documented
- Migration strategy completed

### Issue #214: Research Spike - Configuration Management Strategy - Externalize Hardcoded Settings
**Task**: Investigate configuration management strategy to externalize hardcoded settings
**Purpose**: Improve system flexibility and enable better configuration management
**Priority**: MEDIUM - System configuration
**Acceptance Criteria**:
- Configuration management strategy investigated
- Hardcoded settings externalized
- System flexibility improved
- Configuration management enhanced
- Configuration categories identified
- Configuration locations analyzed
- Current state audit completed
- Configuration architecture designed

### Issue #213: Research Spike - Comprehensive LLM Parameter Strategy Investigation
**Task**: Investigate comprehensive LLM parameter strategy to optimize model performance
**Purpose**: Understand parameter effects and develop best practices for LLM configuration
**Priority**: MEDIUM - LLM optimization
**Acceptance Criteria**:
- Comprehensive LLM parameter strategy investigated
- Model performance optimized
- Parameter effects understood
- Best practices for LLM configuration developed
- Core parameters investigated
- Model variations analyzed
- Parameter optimization strategies developed
- Performance improvements documented

### Issue #113: Academic Paper Development - Framework Weight Research Publication
**Task**: Develop academic paper on framework weight research for publication
**Purpose**: Document and publish framework weighting research findings
**Priority**: MEDIUM - Academic publication
**Acceptance Criteria**:
- Academic paper on framework weight research developed
- Methodology documented
- Results analyzed
- Academic presentation of framework weighting research completed
- Publication-ready paper prepared
- Peer review process initiated
- Research findings documented
- Academic impact assessed

### Issue #109: EPIC - Research Publication & Academic Documentation
**Task**: Create comprehensive research publication and academic documentation epic
**Purpose**: Develop comprehensive academic documentation and publication materials
**Priority**: MEDIUM - Academic documentation
**Acceptance Criteria**:
- Research publication epic completed
- Academic documentation comprehensive
- Paper development completed
- Methodology documentation completed
- Academic presentation materials prepared
- Research findings documented
- Publication strategy developed
- Academic impact assessed

### Issue #107: EPIC - DiscernusLibrarian → WorkflowOrchestrator Integration
**Task**: Integrate DiscernusLibrarian with WorkflowOrchestrator
**Purpose**: Streamline research workflow and improve system integration
**Priority**: MEDIUM - System integration
**Acceptance Criteria**:
- DiscernusLibrarian integrated with WorkflowOrchestrator
- Research workflow streamlined
- System integration improved
- Research capabilities enhanced
- Component coordination improved
- Integration testing completed
- Performance optimization achieved
- User experience enhanced

### Issue #91: Research A1 - Relational Dynamics Literature Review - Validate CFF Amity-Enmity 0.40 Weight
**Task**: Conduct relational dynamics literature review to validate CFF Amity-Enmity 0.40 weight
**Purpose**: Validate framework weighting through comprehensive literature analysis
**Priority**: MEDIUM - Research validation
**Acceptance Criteria**:
- Relational dynamics literature review completed
- CFF Amity-Enmity 0.40 weight validated
- Comprehensive literature analysis completed
- Empirical validation of framework weighting completed
- Research methodology documented
- Findings analyzed and documented
- Validation results published
- Framework weighting confirmed

### Issue #60: Research Platform Maturation Epic - Enhanced Provenance and Academic Features
**Task**: Enhance research platform with improved provenance capabilities and academic features
**Purpose**: Support rigorous research standards and academic publication requirements
**Priority**: MEDIUM - Platform enhancement
**Acceptance Criteria**:
- Research platform enhanced with improved provenance capabilities
- Academic features implemented
- Rigorous research standards supported
- Reproducibility requirements met
- Academic publication requirements supported
- Platform maturation completed
- Enhanced capabilities documented
- User experience improved

### Issue #29: Complete Attesor Study - Speaker Identity Bias Evaluation and Mitigation
**Task**: Complete comprehensive Attesor study on speaker identity bias evaluation and mitigation
**Purpose**: Understand and address potential biases in analysis results
**Priority**: MEDIUM - Bias research
**Acceptance Criteria**:
- Comprehensive Attesor study completed
- Speaker identity bias evaluated
- Bias mitigation strategies developed
- Potential biases in analysis results addressed
- Research validity improved
- Study methodology documented
- Findings analyzed and published
- Bias mitigation implemented

## GitHub Issues - Alpha Feature Complete

### Issue #402: Statistical Preparation Stage and CSV Export System
**Task**: Implement the core infrastructure for statistical preparation mode, including the orchestration stage, derived metrics calculation, and CSV export system
**Purpose**: Enable `discernus run --statistical-prep` command that produces analysis-ready CSV datasets with raw scores, derived metrics, and evidence quotes
**Priority**: HIGH - Core workflow functionality
**Acceptance Criteria**:
- Add `--statistical-prep` CLI flag to orchestrator
- Implement derived metrics calculation using existing MathToolkit
- Create CSV export with raw scores, derived metrics, and evidence quotes
- Generate variable codebook with column definitions
- Store statistical preparation artifacts with content-addressable hashing
- Update manifest.json to track statistical preparation stage
- Maintain complete provenance chain for resume capability

### Issue #403: Evidence-Integrated CSV Export for Statistical Analysis
**Task**: Enhance the CSV export functionality to include evidence integration, allowing researchers to export statistical results with linked evidence for comprehensive analysis and reporting
**Purpose**: Enable researchers to export statistical analysis results with integrated evidence, maintaining the connection between data and supporting evidence in external tools
**Priority**: MEDIUM - Data export enhancement
**Acceptance Criteria**:
- CSV export includes evidence columns
- Evidence properly linked to statistical results
- Export format is compatible with external analysis tools
- Evidence metadata preserved in export
- Export performance optimized for large datasets

### Issue #405: Resume from Statistical Preparation to Full Synthesis
**Task**: Implement the ability to resume from statistical preparation to full synthesis, providing workflow flexibility for researchers who initially chose the offramp but later want complete analysis
**Purpose**: Enable researchers to continue from statistical preparation results to full Discernus synthesis when needed, providing maximum flexibility in research workflow
**Priority**: MEDIUM - Workflow flexibility
**Acceptance Criteria**:
- `discernus run --resume-from-stats` command functionality
- Automatic detection of existing statistical preparation artifacts
- Seamless continuation from statistical prep to synthesis stage
- Updated manifest.json with resume history and provenance
- Extended directory structure with synthesis artifacts
- Preserved statistical preparation results alongside synthesis results

## Rate Limiting & Performance Issues

*Moved to Sprint 10: Critical Logging Integrity & Rate Limiting Resolution*

## Critical Logging Integrity Issues

*Moved to Sprint 10: Critical Logging Integrity & Rate Limiting Resolution*
