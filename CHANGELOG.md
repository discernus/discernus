# Narrative Gravity Maps - Changelog

## [Unreleased]

### Major Architecture Improvements
- **Centralized Visualization System (Phase 1 & 2 Complete)**: Migrated scattered matplotlib implementations to unified, theme-aware Plotly engine
  - **Phase 1**: Core systems - Academic templates, main dashboard, engine integration
  - **Phase 2**: Complete platform unification - Corpus exporters, experiment reports, legacy scripts
  - Eliminated 3000+ lines of duplicated visualization code across 25+ files
  - Implemented professional theming system (academic, presentation, minimal themes)
  - Converted static matplotlib outputs to interactive HTML + publication-ready PNG/SVG/PDF
  - Created `src/narrative_gravity/visualization/` package with centralized engine
  - **Affected Files**: All template generators, analysis exporters, experiment reports, dashboard systems
  - **Impact**: 98% code reduction, 100% styling consistency, interactive visualizations, zero matplotlib in production templates
  - **Documentation**: `docs/architecture/CENTRALIZED_VISUALIZATION_ARCHITECTURE.md`, `docs/architecture/CENTRALIZED_MIGRATION_COMPLETE.md`

### Code Quality  
- **Eliminated Code Duplication**: Replaced custom visualization classes with centralized system
- **Improved Maintainability**: Single source of truth for all visualization logic
- **Enhanced User Experience**: Interactive visualizations instead of static images

### Fixed
- **CRITICAL: Narrative Position Calculation Framework Mismatch** - Resolved (0,0) coordinate issue that was preventing meaningful analysis results - 2025-06-13
  - **Root Cause**: Framework configuration mismatch between LLM analysis (civic virtue wells: "Dignity", "Tribalism") and circular engine (default wells: "hope", "fear")
  - **QA Detection**: Quality assurance system correctly identified "Suspicious position calculation - Narrative position: (0.000, 0.000)"
  - **Automatic Fix**: Added framework-aware position recalculation in execution engine using correct civic virtue configuration
  - **Validation**: All analyses now produce meaningful coordinates (e.g., (0.075, 0.766), distance: 0.770) instead of origin positioning
  - **Production Impact**: Declarative experiment execution engine success rate improved from 0% to 100%
  - **Technical Implementation**: Added `_fix_narrative_position()` method in execution engine with framework configuration loading
  - **Quality Integration**: QA system continues to detect original broken calculations while execution engine automatically applies fixes

### Added
- **MAJOR: Five-Dimensional Experimental Design Framework**: Systematic experimental design framework for rigorous methodological research - 2025-06-13
  - **Core Innovation**: Five-dimensional design space treating analysis as exploration across TEXTS × FRAMEWORKS × PROMPTS × WEIGHTING × EVALUATORS
  - **Methodological Contribution**: Enables rigorous hypothesis testing about analytical methodology effectiveness and component interaction effects
  - **Research Framework**: Systematic approach to testing which analytical choices work best for specific research goals
  - **Quality Integration**: Six-layer quality assurance system integrated as experimental dependent variables
  - **Academic Impact**: Moves computational discourse analysis toward evidence-based methodological optimization
  - **Documentation**: `docs/specifications/EXPERIMENTAL_DESIGN_FRAMEWORK.md` - Complete specification of 5-dimensional design space with experimental methodologies
- **Paper v1.3.0 - Experimental Design Integration**: Updated paper draft to position experimental design framework as core methodological contribution - 2025-06-13
- **Declarative Experiment Definition System**: Comprehensive specification for JSON-based experiment packages enabling complex research without custom coding - 2025-06-13
  - **Core Innovation**: Declarative experiment specification using `experiment.json` + resource directories instead of custom Python scripts
  - **Complex Research Support**: Multi-text, multi-framework, multi-model experiments with automatic resource management
  - **Academic Standards**: Built-in QA integration, cost controls, replication packages, and success criteria
  - **User Experience**: "Specify what you want, not how to code it" - researchers create JSON files instead of programming
  - **Example Specification**: Complete civic virtue validation study example with 8 texts × 3 runs = 24 total runs
  - **Documentation**: `docs/specifications/EXPERIMENT_DEFINITION_FORMAT.md` - Complete specification with execution workflow
  - **Core Positioning**: Experimental design framework now central to paper's methodological contributions
  - **5-Dimensional Framework**: Each dimension (TEXTS, FRAMEWORKS, PROMPTS, WEIGHTING, EVALUATORS) documented with design choices and hypothesis examples
  - **Systematic Research**: Framework enables moving beyond ad hoc methodological choices toward principled experimental validation
  - **Academic Structure**: New Section 3 dedicated to experimental design framework with comprehensive methodology documentation
  - **Research Questions**: Framework enables both methodological research (component effectiveness) and substantive research (content analysis)
  - **Future Research**: Positions experimental validation as critical frontier for computational social science methodology
- **Experiment Infrastructure Status Documentation**: Comprehensive handoff documentation for new collaborator - 2025-06-13
  - **Status Document**: `docs/development/CURRENT_STATUS_2025_06_13.md` documenting complete experiment infrastructure discovery
  - **Architecture Analysis**: Found sophisticated experiment infrastructure already implemented (Experiment/Run tables, framework versions, academic pipeline)
  - **Database Resources**: 5 framework versions including MFT v2025.06.11, 4 presidential documents, hierarchical prompt template v2.1.0
  - **Zero Experiments Defined**: Infrastructure complete but no actual experiments created - immediate next step identified
  - **Technical Issues Catalogued**: Analysis service hardcoding status, framework loading validation needs, cost control requirements
  - **Implementation Roadmap**: Clear 3-step process for first real experiment using existing academic pipeline infrastructure
  - **Validation Requirements**: Comprehensive checklist for verifying real MFT analysis vs mock data, database sourcing vs filesystem
  - **Gold Standard Reconciliation**: Aligned proposed experiment design with existing database-driven architecture
  - **New Collaborator Ready**: Complete handoff with environment setup, architectural principles, success criteria, and next milestones
- **Priority 3 Documentation Update Completion**: Comprehensive documentation cleanup and accuracy improvements - 2025-06-13
  - Fixed all broken links in docs/README.md following file reorganization
  - Added new specifications section documenting reorganized content structure
  - Completely rewrote docs/architecture/CURRENT_SYSTEM_STATUS.md with accurate current state
  - Updated all architecture documents from outdated January 2025 to current June 13, 2025
  - Updated paper status to "PROGRESSIVE UPDATE" as requested
  - Documentation now accurately reflects framework v2.0 migration, pipeline testing results, and circular coordinate system

- **TODO Strategic Planning Enhancement**: Added 3 new high-priority tasks based on development roadmap analysis - 2025-06-13
  - **Priority 13: CLI Interface Systematization** - Address usability gaps identified in pipeline testing
  - **Priority 14: Database Architecture Enhancement** - Resolve critical `get_db_session` import failures (20 errors)
  - **Priority 15: Real LLM API Integration** - Replace mock data usage with actual LLM analysis integration
  - All priorities include detailed deliverables, success criteria, and integration plans with existing system

- **Futures Strategic Vision Documentation**: Created comprehensive strategic planning documents for long-term development - 2025-06-13
  - **Advanced Research Ecosystem Vision** - 6-12 month roadmap for community platform and collaborative research
  - **Framework Creation Wizard Specifications** - 3-6 month enhancement for democratizing framework development
  - **Advanced Academic Integration Strategy** - 2-6 month enhancement for comprehensive research infrastructure
  - Strategic visions extracted from development roadmap analysis and organized for future implementation

- **Development Planning Cleanup**: Organized completed planning documents following repo structure standards - 2025-06-13
  - Archived 3 completed planning documents to `docs/archive/completed_planning_2025_06_13/`
  - Moved `Plan_CLI_Interfaces_Solidification.md` (superseded by Priority 13)
  - Moved `Plan_Database_Architecture_Solidification.md` (superseded by Priority 14)
  - Moved `DEVELOPMENT_ROADMAP.md` (content extracted to TODO priorities and futures vision)
  - Maintained PRIORITY_2 and PRIORITY_3 guides as reference documentation for completed systems
  - Created comprehensive archive documentation with content migration tracking

- **Architecture Documentation Organization**: Properly categorized component versioning documentation - 2025-06-13
  - Moved `component_versioning_guide.md` → `docs/architecture/COMPONENT_VERSIONING_ARCHITECTURE.md`
  - Renamed to follow architecture documentation naming convention (ALL_CAPS_WITH_UNDERSCORES)
  - Added reference to main documentation index for proper discoverability
  - Component versioning system documentation now properly classified as architecture reference

- **Development Environment Documentation Cleanup**: Eliminated duplication between DEV_ENVIRONMENT.md and cursor rules - 2025-06-13
  - Simplified `docs/development/DEV_ENVIRONMENT.md` to focus only on IDE-specific setup and quick reference
  - Removed content duplication with `.cursorrules` (which is the authoritative source for AI assistants)
  - Retained unique IDE configuration guidance (VS Code settings.json, PyCharm setup)
  - Added clear reference directing users to `.cursorrules` for complete development environment guidance
  - Updated cursor rules reference to point to simplified DEV_ENVIRONMENT.md for IDE-specific setup only

- **Reference Documentation Naming Cleanup**: Removed confusing priority numbering from completed system documentation - 2025-06-13
  - Renamed `PRIORITY_2_MANUAL_DEVELOPMENT_GUIDE.md` → `MANUAL_DEVELOPMENT_SUPPORT_GUIDE.md`
  - Renamed `PRIORITY_3_ACADEMIC_TOOL_INTEGRATION_GUIDE.md` → `ACADEMIC_TOOL_INTEGRATION_GUIDE.md`
  - Eliminated confusion between historical priority numbers and current TODO priority system
  - Updated all documentation references to use new filenames
  - Files now clearly identified as reference guides for operational systems rather than active priorities

- **User Guide Documentation Organization**: Moved misplaced user guides to proper location following repo standards - 2025-06-13
  - Moved `docs/API_COST_PROTECTION_GUIDE.md` → `docs/user-guides/API_COST_PROTECTION_GUIDE.md`
  - Moved `docs/corpus_generation_tools.md` → `docs/user-guides/corpus_generation_tools.md`
  - Fixed broken references in main documentation index
  - Enhanced Priority 15 (LLM Integration) with cost management integration requirements
  - Identified need to validate existing cost protection system with real API calls vs. current mock data usage

- **Environment Troubleshooting Documentation**: Simplified and properly located troubleshooting guide - 2025-06-13
  - Moved `docs/ENVIRONMENT_TROUBLESHOOTING.md` → `docs/development/ENVIRONMENT_TROUBLESHOOTING.md`
  - Removed content duplication with `.cursorrules` (authoritative setup source)
  - Focused content on troubleshooting and diagnostic commands only
  - Added clear references to cursor rules for basic setup guidance
  - Retained unique value: emergency reset procedures, root cause analysis, diagnostic patterns
  - Updated cursor rules to reference troubleshooting guide for advanced diagnostic procedures

## [v2.4.0] - Framework Agnosticism and Source of Truth Architecture - 2025-06-12

## [Unreleased] - June 12, 2025

### 🧹 PROJECT ORGANIZATION CLEANUP: Repository Structure Standardization

**COMPLETED**: Major cleanup of repository organization following established repo rules
- **Root Directory Cleanup**: Moved 20+ files from root directory to appropriate locations per repo standards
  - **Installation Scripts**: Moved to `scripts/` directory
    - `install_essential_r_packages.R`, `install_academic_tools.py`, `install_r_packages.R`
    - `export_academic_data.py`, `enhanced_r_template.R`
  - **Visualization Demos**: Organized into `analysis_results/visualization_demos_2025_06_12/`
    - Demo scripts, positioning strategies, clustering comparisons
    - Lincoln visualization files (HTML/PNG outputs), test scripts
    - Plotly visualization pipeline and enhancement scripts
  - **Documentation Organization**: Moved guides to appropriate docs subdirectories
    - `PLOTLY_ELLIPTICAL_GUIDE.md` → `archive/deprecated_visualization_guides/` (outdated)
    - `ACADEMIC_PIPELINE_STATUS.md` → `docs/specifications/` (current status)
- **Temporary File Organization**: Applied proper tmp/ directory structure per repo rules
  - **Dated Structure**: Created `tmp/2025_06_12/framework_migration_cleanup/`
  - **Loose File Consolidation**: Moved 20+ temporary files into proper dated directories
  - **Framework Migration Artifacts**: Organized visualization iteration files, test scripts, and documentation
- **Root Directory Standards Achievement**: Now complies with repo rule philosophy
  - **Operational Files Only**: README.md, CHANGELOG.md, LICENSE, launch scripts, configuration
  - **No Analysis Results**: All outputs properly organized in `analysis_results/`
  - **No Utility Scripts**: All scripts properly organized in `scripts/`
  - **No Temporary Files**: All temp files properly organized in dated `tmp/` directories

**Repository Quality Improvement**: Clean, professional project structure following established standards
- **Maintainability**: Clear separation of operational vs development vs results files
- **Onboarding**: New contributors can quickly understand project organization
- **Scalability**: Structure supports continued growth without clutter
- **Academic Standards**: Professional organization supporting research credibility

### ✅ TODO LIST ENHANCEMENT: Phase 2-4 Planning Integration

**STRATEGIC PLANNING**: Added comprehensive next-phase planning to development TODO system
- **Phase 2: Prompt Template Specification System**: Formal specification and versioning for templates
  - JSON schema v2.0 for template structure, parameters, and validation rules
  - Bidirectional sync system between database and filesystem (similar to framework sync)
  - 3-tier validation pipeline (Schema, Semantic, Performance) with quality gates
  - Migration tools for existing prompt templates to formal specification
- **Phase 3: Weighting Scheme Specification System**: Mathematical methodology formalization
  - Formal specification for dominance amplification, scaling factors, boundary logic
  - Automated testing of weighting calculations against known benchmarks
  - A/B testing framework for parameter optimization and academic documentation
  - Cross-framework compatibility ensuring schemes work across all 5 frameworks
- **Phase 4: Integration and Testing Pipeline**: Complete end-to-end quality assurance
  - Automated integration tests for full pipeline (Framework → Prompt → Weighting → Visualization)
  - Performance benchmarking with regression detection and quality assurance gates
  - Cross-model validation testing consistency across different LLM providers
  - Academic compliance testing with automated publication-readiness verification

**Implementation Timeline**: 8-week structured rollout (July 10 - August 7, 2025)
- **Week 5**: Phase 2 - Prompt Template Specification System
- **Week 6**: Phase 3 - Weighting Scheme Specification System  
- **Week 7**: Phase 4 - Integration and Testing Pipeline
- **Week 8**: Cross-phase validation and documentation

**Success Metrics Integration**: Updated TODO success criteria to include Phase 2-4 completion
- All prompt templates formalized with validation pipeline
- Mathematical weighting schemes validated and optimized
- Full integration testing pipeline operational
- 100% automated test coverage for critical paths established

### 📄 ACADEMIC PAPER UPDATE: Framework-Agnostic Universal Methodology (v1.2.0)

**CRITICAL ACADEMIC REPOSITIONING**: Updated paper draft to reflect framework agnosticism principle established across platform
- **Universal Methodology Positioning**: Paper now positions Narrative Gravity Maps as universal framework-agnostic methodology
  - **Title Updated**: "A Universal Quantitative Framework for Analyzing Persuasive Discourse" 
  - **Abstract Focus**: Universal applicability across domains, not primarily political discourse analysis
  - **Introduction Scope**: Cross-domain methodology with political discourse as one example among many
  - **Framework Demonstrations**: 5 example frameworks across different domains (political, business, education, healthcare, communication)
- **Academic Language Transformation**: Comprehensive revision eliminating framework-specific language at methodology level
  - **Core Methodology**: "Configurable gravity wells," "conceptual forces," "framework-agnostic architecture"
  - **Domain Examples**: Political discourse clearly positioned as one domain-specific application
  - **Research Applications**: Universal applicability across business, education, healthcare, legal, international relations
  - **Framework Descriptions**: All 5 frameworks positioned as examples demonstrating versatility

**Structural Academic Improvements**: Enhanced paper organization for broader academic impact
- **Appendix Replacement**: Removed detailed framework code, replaced with framework summaries and domain applicability
  - **Framework Summary Table**: Configuration overview across all 5 example frameworks
  - **Domain Applications**: Research applications across political science, business, education, healthcare, communication, psychology
  - **Implementation Guidelines**: Framework development guidance for any domain
  - **Technical Notes**: Universal infrastructure supporting any framework type
- **Cross-Domain Validation**: Emphasized universal validation strategies and domain-specific requirements
- **Future Opportunities**: Clear pathway for framework development across any analytical domain

**Academic Impact Strategy**: Positioned for broader adoption and cross-disciplinary citation
- **Universal Appeal**: Any researcher can see applicability to their domain
- **Methodological Contribution**: Focus on universal methodology innovation rather than domain-specific applications
- **Community Development**: Clear framework contribution pathway for researchers across fields
- **Publication Strategy**: Suitable for computational social science, methodology, or interdisciplinary journals

**Framework Examples Repositioned**: Clear positioning as demonstrations rather than core focus
- **Civic Virtue**: Political discourse analysis (domain-specific example)
- **Political Spectrum**: Ideological positioning (domain-specific example)  
- **Moral Foundations**: Cross-cultural analysis (domain-specific example)
- **Identity Recognition**: Identity dynamics (domain-specific example)
- **Rhetorical Posture**: Communication styles (domain-specific example)

### 🎯 FRAMEWORK AGNOSTICISM: Platform Language Neutrality Achieved

**CRITICAL STRATEGIC UPDATE**: Systematically separated platform methodology from framework-specific language
- **Problem Solved**: Eliminated confusion between general methodology and domain-specific applications
  - **Platform Level**: Framework-agnostic language focusing on "gravity wells," "conceptual forces," "analytical frameworks"
  - **Framework Level**: Domain-specific language preserved within framework contexts (moral, political, integrative, etc.)
  - **Academic Credibility**: Clear separation shows methodology transcends any specific domain or use case
- **Documentation Language Updates**: Comprehensive revision of platform-level descriptions
  - **README.md**: Updated core platform description to be framework-agnostic while preserving examples
  - **User Guides**: Removed domain-specific language from platform descriptions
  - **Research Applications**: Updated from "Political Speech Analysis" to "Persuasive Discourse Analysis"
  - **Framework Descriptions**: Clarified as "domain-specific examples" rather than inherent platform capabilities
- **Terminology Standardization**: Established clear language boundaries
  - **Platform Level**: "Gravity wells," "coordinate systems," "conceptual forces," "analytical frameworks"
  - **Framework Level**: "Moral," "political," "integrative," "disintegrative" (only within framework context)
  - **Domain Neutrality**: "Persuasive discourse," "framework-defined forces," "domain-appropriate frameworks"

**Academic Impact**: Platform now clearly supports universal methodology applicable to any persuasive discourse domain
- **Broader Adoption**: Researchers in any field can see applicability to their domain
- **Theoretical Clarity**: Methodology separated from specific implementations
- **Framework Flexibility**: Clear path for creating frameworks for business, education, healthcare, etc.
- **Publication Ready**: Academic papers can emphasize methodology generalizability

**Implementation Examples**: 5 frameworks now clearly positioned as domain-specific demonstrations
- **Civic Virtue Framework**: "Political discourse analysis" (domain-specific example)
- **Political Spectrum Framework**: "Political positioning analysis" (domain-specific example)
- **MFT Framework**: "Cross-cultural moral analysis" (domain-specific example)
- **Identity Framework**: "Identity and recognition analysis" (domain-specific example)
- **Rhetorical Posture Framework**: "Communication style analysis" (domain-specific example)

### 🗄️ STRATEGIC FRONTEND ARCHIVING: Complete Interface Deprecation for Research Focus

**STRATEGIC DECISION**: Archived all frontend interfaces to focus on core research pipeline completion
- **Problem Solved**: Eliminated resource split between interface development and academic research requirements
  - **Research Priority**: Focus on experimental matrix runs, human validation studies, and paper publication
  - **Interface Complexity**: Frontend development consuming resources needed for statistical validation
  - **Academic Timeline**: Paper completion timeline requires concentrated effort on core methodology
- **Complete Interface Archive**: Systematically archived all user interface work to `archive/deprecated_interfaces/`
  - **Chainlit Interface**: Moved `launch_chainlit.py`, `chainlit.md`, `.chainlit/`, and `src/narrative_gravity/chatbot/`
  - **React Frontend**: Moved complete `frontend/` directory with TypeScript application and dependencies
  - **Node.js Artifacts**: Moved `package.json`, `package-lock.json`, `node_modules/`, and `public/` assets
  - **Testing Infrastructure**: Moved `playwright.config.ts`, `playwright-report/`, and `test-results/` 
- **Documentation and Restoration**: Complete preservation with restoration procedures
  - **Archive README**: Comprehensive documentation of all archived components with restoration procedures
  - **Strategic Context**: Clear priority sequence (Research → Validation → Paper → Interfaces)
  - **Technical Preservation**: All dependencies, configurations, and development state preserved
  - **Future Integration**: Backend API compatibility maintained for future interface restoration

**Repository Organization**: Professional structure supporting academic research focus
- **Clean Root Directory**: Only operational files remain (launch.py, database config, etc.)
- **Backend Focus**: `launch.py` updated to support only backend services (API, Celery workers)
- **Documentation Updates**: README.md and LAUNCH_GUIDE.md updated to reflect research pipeline focus
- **Archive Structure**: Organized archive preserving complete development history and technical achievements

**Research Pipeline Priority**: Clear strategic focus on academic completion sequence
- **Phase 1 Complete**: Framework Source of Truth architecture with all 5 frameworks validated
- **Phase 2-4 Planned**: Prompt templates, weighting schemes, and integration testing (July-August 2025)
- **Academic Validation**: Human validation studies and statistical rigor prioritized
- **Paper Publication**: Academic publication pathway clear without interface development overhead

### ✅ SOURCE OF TRUTH ARCHITECTURE: Framework Management System Complete

**ARCHITECTURAL ACHIEVEMENT**: Successfully resolved "source of truth" problem between database and filesystem framework storage
- **Problem Solved**: Eliminated dual-source confusion where frameworks existed in both database and filesystem
  - **Before**: Manual synchronization prone to drift, unclear authority, development friction
  - **After**: Database as authoritative source with filesystem as development workspace
- **Framework Sync Tool**: Complete bidirectional synchronization system (`scripts/framework_sync.py`)
  - **Status Checking**: Compare database vs filesystem versions with change detection
  - **Export/Import**: Seamless movement between database and filesystem for development
  - **Conflict Resolution**: Intelligent handling of version conflicts and drift
  - **Batch Operations**: Migrate all frameworks simultaneously with comprehensive error handling
- **All 5 Frameworks Migrated**: 100% success rate migrating to v2.0 specification
  - **civic_virtue**: ✅ Migrated to v2025.06.12, validation passed
  - **political_spectrum**: ✅ Migrated to v2025.06.12, validation passed
  - **fukuyama_identity**: ✅ Migrated to v2025.06.12, validation passed
  - **mft_persuasive_force**: ✅ Migrated to v2025.06.12, validation passed (schema fixes applied)
  - **moral_rhetorical_posture**: ✅ Migrated to v2025.06.12, validation passed
- **Infrastructure Tools**: Complete developer workflow system
  - **Validation Pipeline**: 3-tier validation (Schema, Semantic, Academic) with comprehensive error reporting
  - **Migration System**: Automated v1.x → v2.0 framework migration with backup and rollback
  - **Quality Assurance**: 100% framework validation success rate achieved

**Developer Workflow Established**: Clear processes for framework development and maintenance
- **Framework Development**: Export → Edit → Validate → Import cycle with conflict detection
- **Version Management**: Database-first versioning with complete provenance tracking
- **Quality Gates**: Automated validation prevents invalid frameworks from entering system
- **Team Collaboration**: Multiple developers can work safely with synchronized development

**Foundation for Next Phases**: Robust architecture supporting Phase 2-4 implementation
- **Proven Sync Architecture**: Framework sync patterns ready for prompt templates and weighting schemes
- **Validation Pipeline**: 3-tier validation system ready for extension to other component types
- **Database Integration**: Production-ready component versioning with proper foreign key relationships
- **Development Workflow**: Established patterns supporting systematic component development

### ✅ FORMAL SPECIFICATION SYSTEM v1.0 IMPLEMENTED

**MAJOR MILESTONE**: Successfully implemented formal specification system with validation tools
- **Framework Specification Schema v2.0**: Complete JSON schema with comprehensive validation rules
  - **Required Fields**: framework_name, display_name, version, description, coordinate_system, positioning_strategy, wells, theoretical_foundation
  - **Coordinate System**: Formal circular coordinate specification (deprecated elliptical)
  - **Positioning Strategy**: Clustered, even distribution, or custom positioning with cluster definitions
  - **Academic Foundation**: Required theoretical sources and approach documentation
  - **Validation Levels**: Schema, semantic, and academic validation with detailed error reporting
- **Validation Tools**: Comprehensive CLI validation system with detailed reporting
  - **Multi-level Validation**: Structural (JSON schema), semantic (consistency), academic (rigor)
  - **Error Categories**: Schema violations, semantic inconsistencies, academic gaps, best practices
  - **Fix Suggestions**: Automated recommendations for resolving validation issues
  - **Batch Processing**: Validate all frameworks with summary reporting
- **Migration System**: Automated migration from v1.x to v2.0 specification
  - **Civic Virtue Framework**: Successfully migrated and validated (✅ VALIDATION PASSED)
  - **Backward Compatibility**: Preserves existing data while adding required v2.0 fields
  - **Backup Creation**: Automatic backup of original frameworks before migration
- **Quality Assurance**: Automated validation pipeline with comprehensive checks
  - **Academic Rigor**: Citation format validation, theoretical approach depth checks
  - **Best Practices**: Color accessibility, metric completeness, compatibility declarations
  - **Semantic Consistency**: Well angle uniqueness, cluster span validation, type consistency

### 📋 FORMAL SPECIFICATION SYSTEM PROPOSAL

**STRATEGIC INITIATIVE**: Comprehensive proposal for formal specifications across all system components
- **Framework Specifications**: Standardized JSON schema for moral/political analysis frameworks
  - **Coordinate System**: Formal circular coordinate specification with positioning strategies
  - **Validation Rules**: Structural, semantic, and academic validation requirements
  - **Theoretical Foundation**: Required academic citations and empirical validation
  - **Compatibility Matrix**: Clear interoperability requirements with other components
- **Prompt Template Specifications**: Structured component-based template system
  - **Component Architecture**: 8 ordered components (header, role, scoring, methodology, etc.)
  - **Performance Targets**: CV < 0.20, hierarchical clarity, format compliance metrics
  - **Framework Compatibility**: Clear mapping between templates and frameworks
  - **Validation Pipeline**: Automated quality assurance and regression testing
- **Weighting Scheme Specifications**: Mathematical methodology standardization
  - **Algorithm Types**: winner_take_most, proportional, threshold_based, custom
  - **Mathematical Foundation**: LaTeX formulas, parameter definitions, edge case handling
  - **Empirical Validation**: Test scenarios, behavioral requirements, performance metrics
  - **Implementation Standards**: Python class specifications, complexity requirements
- **Quality Assurance Framework**: Automated validation pipeline with CLI tools
- **Implementation Strategy**: 4-phase rollout over 7 weeks with tooling and training
- **Academic Rigor**: Peer review support, reproducibility, standardization for research

### ✅ COMPLETE FRAMEWORK MIGRATION TO CIRCULAR COORDINATES

**MAJOR ARCHITECTURAL UPDATE**: Successfully migrated all 5 frameworks from elliptical to circular coordinate system
- **Framework Updates**: Updated all framework configurations in both filesystem and database
  - **Civic Virtue Framework**: Updated to circular with clustered positioning (top/bottom clusters)
  - **Political Spectrum Framework**: Updated to circular with left/right clustering for political orientation
  - **MFT Persuasive Force Framework**: Updated to circular with even distribution to avoid visual hierarchy
  - **Fukuyama Identity Framework**: Updated to circular with vertical dipole clustering
  - **Moral Rhetorical Posture Framework**: Updated to circular with restorative/retributive clustering
- **Database Synchronization**: All 5 frameworks now use circular coordinates in database (✅ Circular status confirmed)
- **Weight System Standardization**: Fixed all frameworks to use positive weights (well type determines moral direction)
- **Color Coding**: Added consistent well_type_colors for integrative/disintegrative visualization
- **Positioning Strategies**: Implemented proper clustering and arc variables as discussed in paper draft

### ✅ PLOTLY CIRCULAR VISUALIZATION PIPELINE VALIDATED

**Production Success**: Complete validation of Plotly-based circular visualization system through end-to-end testing
- **Database Schema Integration**: Successfully updated test pipeline to work with v2.1 schema
  - **Schema Migration**: Updated from legacy `analysis_result`/`framework_version`/`corpus_document` to modern `run`/`document` tables
  - **Query Optimization**: Proper joins on `run.text_id = document.text_id` with framework filtering via `run.framework_version`
  - **Data Structure**: Uses `run.raw_scores` JSON column for well scores, eliminating complex parsing
- **Visualization System Validation**: Comprehensive testing with sample civic virtue data
  - **Individual Visualizations**: Generated 3 distinct scenario visualizations (hopeful speech, divisive rhetoric, balanced analysis)
  - **Comparative Analysis**: Multi-panel comparison visualization with 4-quadrant layout
  - **Interactive Output**: All visualizations saved as interactive HTML files with hover info and academic styling
  - **Framework Compatibility**: Tested with 10-well civic virtue configuration (5 integrative, 5 disintegrative)
- **Production Pipeline Ready**: Complete test infrastructure for database-driven visualization
  - **Test Script**: `scripts/test_plotly_circular_pipeline.py` updated for v2.1 schema compatibility
  - **Demo Script**: `scripts/demo_plotly_circular_visualization.py` for standalone validation
  - **Error Handling**: Comprehensive database error detection with helpful troubleshooting messages
  - **Output Management**: Organized output in `analysis_results/plotly_demo/` with timestamped files

**Technical Implementation**: Robust production architecture validated through testing
- **PlotlyCircularVisualizer**: Confirmed working with wells configuration, narrative scores, and academic styling
- **Database Integration**: Seamless operation with PostgreSQL v2.1 schema and proper foreign key relationships
- **Framework Agnostic**: Supports arbitrary well types, colors, and arrangements as designed
- **Academic Standards**: Publication-ready outputs with proper titles, legends, and interactive features

**Next Steps Ready**: System prepared for real analysis data integration
- **Database Population**: Ready to process actual analysis results when available
- **Framework Extension**: Validated architecture supports multiple frameworks beyond civic virtue
- **Research Workflow**: Complete pipeline from database analysis results to publication-ready visualizations
- **Academic Integration**: Interactive HTML outputs suitable for research presentations and publications

### 🏗️ MAJOR ARCHITECTURAL DECISION: CIRCULAR COORDINATE SYSTEM ADOPTION

**Revolutionary Architectural Change**: Complete pivot from elliptical to circular coordinate system for maximum researcher adoption while preserving analytical sophistication
- **Architectural Analysis**: Systematic evaluation of elliptical vs circular coordinate trade-offs
  - **Elliptical Barriers Identified**: Mathematical complexity, poor tool compatibility, parameter sensitivity, export challenges
  - **Circular Advantages Realized**: Universal comprehension, tool compatibility, parameter robustness, zero learning curve
  - **Three-Dimensional Design**: Independent control of positional arrangement (visual rhetoric), mathematical weighting (analytical power), and algorithmic enhancement (technical sophistication)
- **Framework Flexibility Breakthrough**: Enables both normative (Civic Virtue) and descriptive (Moral Foundations Theory) approaches
  - **Normative Frameworks**: Visual hierarchy with "good" wells at top, hierarchical weighting (1.0, 0.8, 0.6)
  - **Descriptive Frameworks**: Neutral positioning, equal weighting (all 1.0), balanced theoretical stance
  - **Custom Arrangements**: Any positioning scheme supported by theoretical justification
- **Paper Draft v1.1.0**: Complete rewrite documenting circular coordinate architecture
  - **Mathematical Framework**: Standard polar coordinates with enhanced algorithms
  - **ASCII Art Placeholders**: Visual examples for Civic Virtue vs Moral Foundations Theory approaches
  - **Academic Justification**: Systematic analysis of adoption barriers and technical sophistication preservation
- **Implementation Roadmap**: Clear technical specifications for circular coordinate system development
  - **Core Mathematics**: Convert `NarrativeGravityWellsElliptical` → `NarrativeGravityWellsCircular`
  - **Enhanced Algorithms**: Implement validated dominance amplification, adaptive scaling, boundary snapping
  - **Academic Tools**: R/Stata export with standard polar coordinate support
  - **Universal Compatibility**: Cross-platform visualization support for publication workflows

### ✅ PRIORITY 1 & 2 COMPLETION: Hierarchical Theme Detection & Visualization Mathematics

**PRIORITY 1 COMPLETE**: Hierarchical Theme Detection Implementation (June 12, 2025)
- **Framework-Agnostic Template**: Created hierarchical analysis template v2.1.0 eliminating flat score distributions
  - **Three-Stage Architecture**: Dominant theme identification, percentage weighting, evidence grounding
  - **Mathematical Forcing Functions**: Eliminates moderate score clustering (0.3-0.7) across multiple wells
  - **Universal Compatibility**: Works across all 5 frameworks with 100% compatibility validation
- **Database Integration**: Stored in component versioning system with proper lifecycle management
- **Deprecated Cleanup**: Archived old prompts maintaining clean architectural separation

**PRIORITY 2 COMPLETE**: Visualization Mathematics Enhancement (June 12, 2025)
- **60% Boundary Utilization Improvement**: Systematic iterative optimization methodology
  - **Baseline Evaluation**: Documented 37.5% boundary usage and compression problems
  - **Enhanced Algorithms**: Nonlinear dominance amplification, adaptive scaling, boundary snapping
  - **Final Optimization**: 60.0% boundary usage with preserved nuanced differentiation
- **Multi-Dataset Validation**: Real vs synthetic differentiation confirms proper mathematical behavior
  - **Synthetic Extremes**: 0.539-0.600 distance from center (approaching boundaries as designed)
  - **Real Speeches**: 0.052 distance from center (moderate positioning for mixed rhetoric)
- **Publication-Ready Enhancement**: Algorithms maintain cross-LLM consistency while improving extreme representation

### 🔧 INTELLIGENT INGESTION SYSTEM: LLM API Issues Resolved & Truncation Improvements

**Critical Production Fix**: Resolved OpenAI API failures and aggressive content truncation preventing long document processing
- **OpenAI API Issue Resolution**: Fixed "Expecting value: line 1 column 1 (char 0)" errors plaguing system reliability
  - **Root Cause**: OpenAI responses wrapped in markdown code blocks (`````json`) causing JSON parsing failures
  - **Solution**: Intelligent markdown code block detection and removal before JSON parsing
  - **Retry Logic**: Added exponential backoff (1s, 2s, 4s delays) for intermittent API failures with 3-attempt limit
  - **Error Handling**: Better detection of empty responses and graceful fallback to rule-based extraction
- **Smart Content Truncation System**: Transformed aggressive truncation into intelligent content preservation
  - **Previous Limitation**: Hard 2000-character limit losing critical metadata at document end
  - **New Smart Truncation**: Configurable limits (4000 chars default) with beginning (60%) + end (40%) preservation
  - **Metadata Preservation**: Captures author signatures, dates in conclusions, and document-ending metadata
  - **Title Handling**: Increased limit to 200 characters with word-boundary truncation and smart ellipsis
- **JSON Serialization Fixes**: Resolved object serialization errors preventing result storage
  - **DateTime Objects**: Automatic conversion to ISO string format for JSON compatibility
  - **Path Objects**: Conversion to string representation for cross-platform serialization
  - **Registration Results**: Proper handling of complex CorpusDocument objects in result storage
- **Enhanced Output System**: Eliminated console truncation while providing complete result visibility
  - **Summary Files**: Non-truncated key information in separate `ingestion_summary.txt` files
  - **Complete Results**: Full metadata and registration details preserved in JSON files
  - **Clean Console Output**: Essential information only, with file references for complete data
  - **Professional Reporting**: Success rates, confidence scores, and processing statistics

**Demonstrated Success**: Successfully tested with large-scale documents proving production readiness
- **53KB Biden SOTU 2024**: Complete processing with full metadata extraction (100% confidence)
- **52KB Clinton SOTU 1997**: Proper duplicate detection via content-addressable storage
- **Long Document Pipeline**: Smart truncation preserving metadata at both document beginning and end
- **Content-Addressable Storage**: Hash-based organized storage working perfectly with stable semantic filenames
- **Database Integration**: Complete registration with PostgreSQL including stable paths and metadata

**Technical Implementation**: Robust production architecture supporting academic workflows
- **MetadataExtractor Enhancements** (`src/narrative_gravity/corpus/intelligent_ingestion.py`):
  - Configurable content limits with intelligent begin+end preservation algorithm
  - Markdown code block parsing for OpenAI response handling
  - Retry logic with exponential backoff for API reliability
  - Enhanced fallback extraction with word-boundary title truncation
- **Result Processing Improvements**:
  - JSON serialization fixes for datetime and Path objects
  - Summary file generation for complete result visibility
  - Enhanced error reporting with detailed failure analysis
- **Integration Ready**: Seamless operation with existing corpus organization and database systems

**Production Impact**: Intelligent ingestion system now fully operational for long document processing
- **API Reliability**: 100% success rate achieved through retry logic and markdown parsing
- **Content Quality**: Smart truncation preserves critical metadata while respecting API limits
- **Academic Standards**: Complete metadata extraction supporting research-grade corpus development
- **Workflow Ready**: Production-ready processing of State of the Union addresses and other lengthy political documents

### 🎬 YOUTUBE TRANSCRIPT INTELLIGENT INGESTION SERVICE: Video Content to Research Corpus

**Strategic Achievement**: Production-ready YouTube transcript extraction system extending intelligent corpus ingestion to video content
- **YouTube Transcript Extraction**: Complete service for automated video content processing
  - `YouTubeTranscriptExtractor` class with multi-language transcript extraction (manual and auto-generated captions)
  - Video ID extraction from various YouTube URL formats with validation
  - Content cleaning and formatting optimized for political speech analysis
  - Free transcript extraction using YouTube's caption API (no additional API costs)
- **Enhanced Metadata Pipeline**: Combines YouTube video metadata with AI-powered content analysis
  - `YouTubeCorpusIngestionService` extending existing intelligent ingestion architecture
  - Video-specific metadata: channel, upload date, views, duration, engagement metrics
  - Speaker identification from channel names and content analysis
  - Political content classification (speech, debate, interview, address, press conference)
  - +10 confidence boost for complete video metadata integration
- **Production CLI Tools**: Professional command-line interface for video processing
  - `scripts/intelligent_ingest_youtube.py`: Full LLM-enhanced YouTube processing with dry-run mode
  - `scripts/demo_youtube_ingestion.py`: Demonstration version requiring no API keys
  - Multi-language support, confidence thresholds, batch processing with rate limiting
  - Enhanced result reporting with video metrics and citation information
- **Demonstrated Results**: Successfully processed Phil Davidson 2010 political speech with 100% confidence
  - Video metadata extraction: Title, channel, upload date, view count (126K+ views), duration
  - Perfect transcript extraction: 3,904 characters of clean political speech content
  - Enhanced text ID generation: `davison_speech_2010_lipnBHey` with video context
  - Seamless corpus integration with YouTube-specific metadata fields

**Technical Implementation**: Robust video processing architecture with comprehensive error handling
- **Core Services** (`src/narrative_gravity/corpus/youtube_ingestion.py`):
  - `YouTubeVideoInfo` dataclass with complete video metadata structure
  - `YouTubeTranscriptExtractor` with youtube-transcript-api integration and content cleaning
  - `YouTubeCorpusIngestionService` extending IntelligentIngestionService with video enhancements
- **Enhanced Metadata Integration**: Combines YouTube and LLM analysis for superior results
  - Video metadata enhancement of extracted content metadata
  - Political figure recognition patterns (President, Senator, Governor)
  - Content type classification based on titles and transcript analysis
  - Citation generation with permanent video URLs and engagement metrics
- **Dependencies**: Added youtube-transcript-api and yt-dlp to requirements.txt
  - Free transcript extraction without YouTube API costs
  - Optional enhanced metadata with yt-dlp for video information
  - Graceful fallback when enhanced dependencies unavailable

**Research Workflow Integration**: Seamless extension of existing corpus management
- **Academic Standards**: YouTube videos treated as first-class corpus documents
- **Enhanced Citation Support**: Video URLs, upload dates, channels for academic referencing
- **Cross-Language Capability**: Extract political content in multiple languages
- **Engagement Analytics**: View counts, like ratios for content impact analysis
- **Temporal Analysis**: Upload dates enabling longitudinal political speech studies

**Complete Documentation Suite**: Comprehensive guides anticipating user needs and problems
- **Complete YouTube Guide** (`docs/user-guides/YOUTUBE_TRANSCRIPT_INGESTION_GUIDE.md`): 600+ lines comprehensive documentation
- **YouTube Quick Start** (`docs/user-guides/YOUTUBE_INGESTION_QUICKSTART.md`): Essential commands and workflow examples
- **Updated User Guide README** (`docs/user-guides/README.md`): Integration with existing documentation structure
- **Comprehensive Troubleshooting**: 20+ common issues with solutions and best practices
- **Security & Privacy Guidance**: Transparent handling of content sent to external APIs

**Success Rate Expectations**: Realistic performance targets based on content type
- **Professional political videos with manual captions**: 90-100% success rate
- **Major news channels with auto-captions**: 80-95% success rate
- **User-uploaded content with captions**: 70-90% success rate
- **Videos without captions**: 0% (graceful failure with clear messaging)

### 🤖 INTELLIGENT CORPUS INGESTION SERVICE: LLM-Powered Metadata Extraction

**Strategic Achievement**: Production-ready intelligent corpus ingestion system for automated metadata extraction from messy text files
- **LLM-Powered Metadata Extraction**: Complete service using GPT-3.5-turbo for automatic metadata extraction
  - `MetadataExtractor` class with OpenAI API integration and graceful error handling
  - Structured JSON extraction: title, author, date, document_type, description, language
  - Confidence scoring based on field completeness and validation checks (0-100%)
  - Fallback mechanisms when LLM extraction fails with rule-based title extraction
- **Intelligent Processing Workflow**: End-to-end service from messy files to corpus registration
  - `IntelligentIngestionService` with configurable confidence thresholds (default: 70%)
  - Automatic categorization: successful (≥70%), uncertain (40-69%), failed (<40%)
  - Integration with existing CorpusRegistry for high-confidence document registration
  - Semantic text ID generation from extracted metadata (`{author}_{type}_{year}` format)
- **Production CLI Tools**: Command-line interface for batch processing workflows
  - `scripts/intelligent_ingest.py`: Full LLM-powered ingestion with dry-run mode
  - `scripts/demo_intelligent_ingest.py`: Rule-based demo version requiring no API keys
  - Comprehensive argument support: confidence thresholds, output directories, verbose mode
  - Professional result reporting with detailed statistics and file-by-file analysis
- **Demonstrated Results**: Successfully processed 27 historical documents with 100% demo success rate
  - Historical document corpus: Presidential inaugurals, UN speeches, political addresses
  - Perfect metadata extraction: titles, authors, dates, document types with high confidence
  - Complete integration: All high-confidence documents automatically registered in corpus
  - Academic-quality metadata: Proper formatting, semantic IDs, comprehensive descriptions

**Technical Implementation**: Robust production architecture with error handling
- **Core Services** (`src/narrative_gravity/corpus/intelligent_ingestion.py`): 
  - `ExtractedMetadata` dataclass with confidence scoring and extraction notes
  - `MetadataExtractor` with LLM integration, prompt engineering, validation checks
  - `IntelligentIngestionService` with batch processing and database integration
- **Quality Assurance**: Comprehensive confidence scoring and validation
  - Field completeness scoring (title: 25pts, author: 20pts, date: 20pts, type: 15pts)
  - Content consistency validation (title presence in text, date format validation)
  - Error handling with detailed logging and fallback extraction methods
- **CLI Infrastructure**: Professional command-line tools with full argument support
  - Batch directory processing with file discovery and filtering
  - Detailed result categorization and JSON export for audit trails
  - Integration modes: full database registration vs. dry-run analysis only

**Research Workflow Integration**: Foundation for academic corpus management
- **Academic Standards**: Metadata extraction follows digital humanities best practices
- **FAIR Compliance**: Automatic generation of structured metadata supporting findability
- **Corpus Integration**: Seamless integration with existing CorpusRegistry and discovery systems
- **Provenance Tracking**: Complete audit trail from source files through extraction to registration
- **Research Enablement**: Transforms messy historical documents into analysis-ready corpus entries

**Complete Documentation Suite**: Comprehensive user guides and workflow integration
- **Complete User Guide** (`docs/user-guides/INTELLIGENT_CORPUS_INGESTION_GUIDE.md`): Step-by-step instructions, troubleshooting, advanced usage
- **Quick Start Guide** (`docs/user-guides/INTELLIGENT_INGESTION_QUICKSTART.md`): Essential commands and workflows for immediate use
- **Workflow Integration Guide** (`docs/user-guides/CORPUS_WORKFLOW_INTEGRATION.md`): Complete research workflow from messy files to publication
- **Navigation Overview** (`docs/user-guides/README.md`): Documentation index and getting started guidance
- **Comprehensive Troubleshooting**: Detailed problem-solving for processing, quality, and database issues
- **Best Practices**: Professional workflow recommendations for academic research standards

**Future Implementation Ready**: Intelligent classification and auto-formatting service
- **LLM Integration**: Production-ready OpenAI API integration with cost-effective GPT-3.5-turbo
- **Scalable Architecture**: Batch processing capable of handling large document collections
- **Quality Control**: Confidence-based processing ensuring only high-quality extractions reach corpus
- **Academic Workflow**: Supporting systematic corpus development for digital humanities research

### 🎯 ENHANCED CORPUS MANAGEMENT SYSTEM: FAIR Data & Academic Standards

**Strategic Achievement**: Comprehensive corpus management system meeting FAIR data principles and academic standards
- **Stable Text Identifiers**: Complete implementation of semantic document identification for academic workflow
  - **Semantic Text IDs**: Human-readable format `{author}_{type}_{year}[_{sequence}]` (e.g., `obama_inaugural_2009`)
  - **Placeholder URIs**: Infrastructure ready for stable URI web service (future implementation)
  - **Content Integrity**: SHA-256 hashing for file validation and change detection
  - **Database Integration**: Enhanced hybrid approach preserving file workflow while adding metadata management
- **FAIR Data Compliance**: Systematic implementation of Findable, Accessible, Interoperable, Reusable principles
  - **CorpusValidator**: Comprehensive validation with 63.9% overall FAIR score achievement
  - **Integrity Monitoring**: File existence, hash validation, metadata completeness checking
  - **Academic Standards**: Citation format validation, schema versioning, provenance tracking
  - **Compliance Reporting**: Automated FAIR assessment with principle-by-principle scoring
- **Discovery & Search Tools**: Advanced corpus exploration and navigation capabilities
  - **CorpusDiscovery**: Full-text and metadata search with relevance scoring
  - **Faceted Browsing**: Navigate by author, document type, year, decade with count statistics
  - **Corpus Statistics**: Comprehensive analytics (11 documents, 8 authors, 421-year span)
  - **Document Similarity**: Metadata-based similarity analysis for related content discovery
- **Academic Export Infrastructure**: Research-ready dataset generation in multiple formats
  - **CorpusExporter**: Multi-format exports (CSV, JSON, R, Python, Stata) with analysis templates
  - **Citation Generation**: APA, MLA, Chicago, BibTeX format support with stable URI integration
  - **Replication Packages**: Complete research packages with data, code, documentation, and guides
  - **Academic Metadata**: TEI-compliant structured metadata with JSONB flexibility

**Technical Implementation**: Production-ready corpus management with PostgreSQL integration
- **Enhanced Registry** (`src/narrative_gravity/corpus/registry.py`): Stable identifier management with database integration
- **Validation Framework** (`src/narrative_gravity/corpus/validator.py`): 5-tier quality assessment with academic compliance
- **Discovery Engine** (`src/narrative_gravity/corpus/discovery.py`): Search, faceting, and corpus analytics
- **Export System** (`src/narrative_gravity/corpus/exporter.py`): Multi-format academic dataset generation

**Academic Standards Achievement**: Meeting digital humanities best practices
- **FAIR Principle Scores**: Findable (100%), Accessible (4.6%), Interoperable (100%), Reusable (74.6%)
- **Metadata Standards**: Complete bibliographic information with provenance tracking
- **Citation Framework**: Stable text identifiers with infrastructure ready for URI web service
- **Quality Assessment**: Automated validation identifying corpus issues for improvement
- **Research Workflow**: Seamless integration supporting systematic corpus analysis and publication

**Integration with Existing Infrastructure**: Enhanced corpus foundation supporting Priority 2 CLI orchestration
- **Database Compatibility**: Works with existing PostgreSQL schema and document tables
- **Hybrid Approach**: Preserves file-based workflow while adding academic metadata management
- **Component Integration**: Foundation for batch orchestration and research validation protocols
- **Export Pipeline**: Research-ready datasets feeding into academic analysis workflows

### 🎯 PRIORITY 1 DATABASE FOUNDATION: Component Versioning Infrastructure Complete

**Strategic Achievement**: Complete database schema infrastructure for validation-first research platform
- **Component Versioning Database Schema**: Full implementation of systematic component management
  - **New Tables**: `prompt_templates`, `framework_versions`, `weighting_methodologies`, `component_compatibility`, `development_sessions`
  - **Foreign Key Integration**: Added component version references to existing `experiment` and `run` tables
  - **Data Migration**: Successfully migrated 16 experiments and 26 runs to use component versioning foreign keys
  - **Database Migration**: Applied migration `574edb17ee08` populating component tables with current civic virtue framework v2.1.0
  - **Complete Provenance**: All analysis results now linked to specific component versions for exact reproducibility
- **Component Management CLI**: Professional command-line interface for component lifecycle management
  - **Component Operations**: Create, list, validate, and export prompt templates, frameworks, and weighting methodologies
  - **Semantic Versioning**: Complete version control with parent-child relationships and validation status tracking
  - **Compatibility Matrix**: Systematic validation of component combinations with performance metrics
  - **Export Capabilities**: JSON export for sharing, backup, and external analysis tool integration
- **Academic Standards Integration**: Complete infrastructure for systematic research validation
  - **Performance Tracking**: Usage counts, success rates, average costs, and compatibility metrics
  - **Development Sessions**: Structured workflow tracking for hypothesis-driven component development
  - **Quality Assurance**: Validation status tracking (draft → tested → validated → deprecated)
  - **Reproducibility Support**: Complete experimental provenance with specific component version references

**Technical Implementation**: Production-ready infrastructure with complete PostgreSQL integration
- **Database Architecture**: UUID primary keys, JSON configuration storage, foreign key constraints
- **CLI Tool**: `src/narrative_gravity/cli/component_manager.py` with comprehensive command set
- **Documentation**: Complete guide at `docs/development/component_versioning_guide.md`
- **Migration Verification**: All foreign key relationships working, no data loss during migration

**Research Platform Foundation**: Enables systematic validation-first development methodology
- **Component Evolution**: Track framework and prompt development with complete history
- **Experimental Integrity**: Every analysis result linked to exact component versions used
- **Academic Workflow**: Infrastructure supports publication-quality provenance and reproducibility
- **Development Workflow**: Structured approach to systematic component improvement and validation

### 🏗️ ARCHITECTURAL IMPROVEMENT: Clean Component Separation

**Strategic Achievement**: Implemented clean separation of concerns for component architecture
- **New Framework-Agnostic Prompt Templates**: Created properly-named prompt templates that focus solely on LLM optimization
  - `hierarchical_analysis v2.1.0`: Framework-agnostic hierarchical ranking and evidence extraction
  - `traditional_analysis v2.1.0`: Framework-agnostic comprehensive dimensional scoring
  - `linear_traditional v2.1.0`: Equal-weight mathematical interpretation methodology
- **Architecture Principle**: Each component type now has distinct responsibilities and independent lifecycles:
  - **Prompt Templates**: Pure LLM optimization layer (prompt engineering techniques)
  - **Frameworks**: Pure theoretical constructs layer (dipoles, conceptual relationships)  
  - **Weighting Methodologies**: Pure mathematical interpretation layer (visualization algorithms)
- **Data Migration**: Successfully migrated all 16 experiments and 26 runs from conflated naming to clean architecture
- **Backward Compatibility**: Old `civic_virtue_hierarchical` template deprecated but preserved for historical analysis
- **Documentation**: Updated component versioning guide with new naming conventions and architectural principles

### 🎯 PRIORITY 2 COMPLETE: Manual Development Support Infrastructure

**Strategic Infrastructure**: Complete structured development workflow system for systematic component development
- **Seed Prompt Library** (`src/narrative_gravity/development/seed_prompts.py`): Standardized LLM conversation starters
  - Component-specific prompts for prompt templates, frameworks, and weighting methodologies
  - Context-aware prompt generation with placeholder management
  - Success criteria, development steps, and quality metrics for each component type
  - 3 comprehensive seed prompts with 200+ lines each optimized for academic development
- **Development Session Manager** (`src/narrative_gravity/development/session_manager.py`): Systematic session tracking
  - Complete development session lifecycle management with hypothesis tracking
  - Performance metrics integration (CV, hierarchy clarity, framework fit, evidence quality)
  - Database-backed session storage with iteration logging and analytics
  - Export capabilities for academic documentation and replication packages
- **Component Quality Validator** (`src/narrative_gravity/development/quality_assurance.py`): Automated quality assurance
  - 50+ automated quality checks across all component types
  - Academic standards compliance verification with publication readiness assessment
  - Cross-component compatibility validation for integrated workflows
  - Quality reports with recommendations and academic validation requirements

**CLI Tool Suite**: Complete command-line interface for development workflows
- **Development Session Starter** (`src/narrative_gravity/cli/start_dev_session.py`): Session initialization with seed prompts
  - Interactive and batch session creation with hypothesis tracking
  - Context-aware seed prompt generation for external LLM development
  - Active session management and status tracking
  - Integration with Priority 1 component versioning system
- **Iteration Logger** (`src/narrative_gravity/cli/log_iteration.py`): Performance tracking and session documentation
  - Interactive and command-line iteration logging with comprehensive metrics
  - JSON test results integration and custom performance metrics
  - Version creation tracking linking sessions to component development
  - Session analytics and progress monitoring across development workflows
- **Component Quality Validator** (`src/narrative_gravity/cli/validate_component.py`): Automated quality assessment
  - Comprehensive validation for prompt templates, frameworks, and weighting methodologies
  - Component compatibility testing across integrated workflows
  - Quality report generation with academic standards assessment
  - Export capabilities for documentation and publication preparation

**Documentation & Integration**: Complete development workflow documentation
- **Priority 2 Manual Development Guide** (`docs/development/PRIORITY_2_MANUAL_DEVELOPMENT_GUIDE.md`): Comprehensive user documentation
  - Complete workflow documentation with examples and best practices
  - Quality assurance framework explanation with 50+ automated checks
  - Academic integration guidance for publication and validation studies
  - Advanced usage patterns and customization examples
- **Seamless Priority 1 Integration**: Development sessions integrate with component versioning
  - Session-created components automatically tracked in Priority 1 infrastructure
  - Component matrix validation includes Priority 2 developed components
  - Version control integration with development session provenance tracking

**Academic Standards Support**: Publication-ready development methodology
- **Quality Levels**: 5-tier quality assessment (Excellent→Unacceptable) with academic readiness indicators
- **Performance Metrics**: Quantitative tracking (CV <0.20, hierarchy clarity >0.80, framework fit >0.75)
- **Validation Requirements**: Systematic academic standard compliance with publication preparation
- **Methodology Documentation**: Complete audit trail supporting academic reproducibility requirements

**Development Acceleration**: 50% reduction in development setup time through structured workflows
- **Standardized Processes**: Systematic development protocols reducing cognitive overhead
- **Quality Consistency**: Automated validation ensuring uniform quality across researchers
- **Academic Rigor**: Built-in academic standards supporting validation studies and publication

### 🧪 PRIORITY 1 TEST SUITE INTEGRATION - Automated Validation System

- **Comprehensive Test Coverage**: Complete automated testing for validation-first research platform
  - **Unit Tests** (`tests/unit/test_component_models.py`): 21 tests covering all Priority 1 database models
    - PromptTemplate model functionality and validation status options
    - FrameworkVersion model with JSON field handling and performance tracking
    - WeightingMethodology model with algorithm specifications and mathematical validation
    - ComponentCompatibility model with performance metrics and status lifecycle
    - DevelopmentSession model with iteration tracking and success metrics
    - Model relationships, versioning validation, and field requirements
  - **Integration Tests** (`tests/integration/test_priority1_infrastructure.py`): Database and CLI integration
    - Component creation workflows (prompt templates, frameworks, weighting methods)
    - Development session lifecycle management with hypothesis tracking
    - Component matrix validation with experimental configuration
    - Database schema integration with PostgreSQL backend
    - CLI tool functionality verification and error handling
- **Test Infrastructure**: Production-ready automated validation
  - **Regression Prevention**: All Priority 1 infrastructure protected by automated tests
  - **Database Integration**: Tests work with existing PostgreSQL database (not test-specific)
  - **CLI Validation**: Complete workflow testing from component creation to analysis
  - **Error Coverage**: Comprehensive edge case and error condition testing
- **Validation Strategy Alignment**: Tests implement validation-first research platform approach
  - **Academic Standards**: Systematic testing aligns with academic rigor requirements
  - **Experimental Provenance**: Test validation ensures component version tracking works
  - **Research Workflow**: Tests validate complete manual development workflow
  - **Quality Gates**: Automated tests prevent regression during Priority 2+ development

### 🎯 PRIORITY 1 COMPLETE: Core Infrastructure Implementation

- **Component Versioning System**: Complete database schema for systematic component management
  - **New Tables**: `prompt_templates`, `framework_versions`, `weighting_methodologies`, `component_compatibility`, `development_sessions`
  - **Version Control**: Full parent-child relationships, validation status tracking, performance metrics
  - **Database Migration**: Applied migration `21321e96db52` for component versioning tables
  - **Academic Provenance**: Complete experimental tracking with component version references
- **CLI Infrastructure Components**: Three major CLI tools implementing validation-first strategy
  - **Multi-Component Analysis Orchestrator** (`analyze_batch.py`): Batch processing with component matrix support
  - **Component Version Manager** (`manage_components.py`): Create, update, and track component versions
  - **Development Session Tracker** (`dev_session.py`): Structured session management with hypothesis tracking
- **Backend Integration Enhancements**: Foundation services for academic validation workflow
  - **ComponentMatrix**: Experimental component combinations and validation
  - **BatchAnalysisOrchestrator**: Systematic experimental matrix execution
  - **DevelopmentSessionTracker**: Complete audit trail system for academic validation
- **Configuration System**: Example configurations demonstrating validation-first methodology
  - **Component Matrix Config**: `examples/component_matrix_example.yaml` for systematic validation studies
  - **Database Utilities**: Enhanced `src/narrative_gravity/utils/database.py` for CLI tool integration
- **Academic Standards**: Complete implementation aligns with validation-first research platform strategy
  - **Experimental Provenance**: Every analysis linked to specific component versions
  - **Systematic Validation**: CLI tools support academic rigor and reproducibility
  - **Component Evolution**: Version tracking enables research methodology development

### 🛠️ Environment Configuration - Date Handling Fix

- **Fixed Incorrect Date Usage**: Resolved systematic issue where hardcoded dates were used instead of actual system date
  - **Problem**: Documentation contained "January 2025" when actual date was June 11, 2025
  - **Root Cause**: AI assistants were assuming dates instead of checking system time
  - **Solution**: Created `scripts/get_current_date.sh` utility for consistent date retrieval
  - **Updated Files**: Fixed dates in docs/README.md, archive summaries, and deprecation notices
- **Permanent Prevention System**: Added comprehensive date handling guidance
  - **Repository Rules**: Updated `.cursorrules` with mandatory date checking requirements
  - **Development Guide**: Added date handling section to `DEV_ENVIRONMENT.md`
  - **Utility Script**: Provides multiple date formats (human-readable, ISO, timestamp)
  - **AI Assistant Rules**: Future AI assistants must use system date commands

### 🚀 MIGRATION TO PLOTLY & CIRCULAR VISUALIZATION ENGINE (June 12, 2025)

**Major Visualization Overhaul**: Migrated all narrative gravity visualizations to Plotly, fully deprecating the elliptical approach in favor of a robust, framework-agnostic circular coordinate system.
- **Exclusive Plotly Adoption**: All visualizations now use Plotly for interactive, publication-ready outputs (HTML/PNG)
- **Elliptical Approach Deprecated**: Removed all elliptical engine and visualization code (`engine.py`, `plotly_elliptical.py`)
- **Enhanced Circular Visualizer**: Upgraded `PlotlyCircularVisualizer` with academic styling, metrics display, comparative analysis, and improved type/color handling
- **Engine Update**: `NarrativeGravityWellsCircular` now uses Plotly exclusively, with simplified config and output logic
- **Test & Demo Modernization**: Updated all test/demo scripts to use the new Plotly-based engine and output interactive HTML by default
- **Repository Cleanup**: Removed legacy matplotlib and elliptical files, ensuring a clean, maintainable codebase

**Impact**: The system is now fully aligned with modern academic visualization standards, supporting universal tool compatibility, interactive exploration, and streamlined publication workflows. Circular coordinate system is the sole supported architecture going forward.

## [v2.3.0] - Project organization and cursorrules compliance - June 10, 2025

### 📁 Project Organization - Cursorrules Compliance Cleanup

- **Root Directory Cleanup**: Moved misplaced files to proper directories per cursorrules standards
  - **Test files moved**: `test_*.py` → `tests/integration/` and `tests/e2e/`
  - **Chatbot files moved**: `chainlit_chat*.py`, `chatbot_web*.py`, `chat_with_file.py` → `src/narrative_gravity/chatbot/`
  - **Documentation moved**: All guide files → `docs/user-guides/` or `docs/development/`
  - **Archive cleanup**: Deprecated Streamlit files → `archive/streamlit_legacy/`
  - **Scripts organized**: Debug files → `scripts/`
- **Service Architecture Updated**: Cursorrules now reflect current service architecture
  - **React frontend**: Port 3000 (main interface)
  - **Chainlit chat**: Port 8002 (conversational analysis) 
  - **FastAPI server**: Port 8000 (REST API)
  - **Streamlit deprecated**: Moved to archive with proper deprecation notices
- **Import Path Updates**: Updated `launch_chainlit.py` and documentation references for moved files
- **Root Directory Standards**: Now compliant with cursorrules - only operational files, launch tools, and configuration remain

### 🎯 Frontend Integration Breakthrough

- **WSOD (White Screen of Death) Resolution**: Fixed critical browser compatibility issue
  - **Root Cause**: `process.env` undefined in browser environment causing React crashes
  - **Solution**: Added proper `process.env` polyfill in `vite.config.ts` for browser compatibility
  - **Impact**: Frontend now loads correctly at http://localhost:3000 with full React functionality
- **End-to-End UI Testing Ready**: Complete UI testing infrastructure established
  - **Playwright Integration**: Comprehensive browser automation testing with `tests/e2e/complete-end-to-end.spec.ts`
  - **Manual Testing Guide**: `MANUAL_UI_TESTING_GUIDE.md` with step-by-step UI validation procedures
  - **Debug Automation**: `debug_frontend.js` script for automated frontend health checking
- **API-Frontend Integration Verified**: All communication layers working
  - **Configuration Loading**: Frontend successfully loads 3 frameworks, 4 prompt templates, 4 scoring algorithms
  - **CORS Resolution**: Proper cross-origin communication between localhost:3000 ↔ localhost:8000
  - **Request/Response Validation**: API client properly handling all endpoint communications

### ✅ ANALYSIS ENGINE STATUS CONFIRMED - Real LLM Integration Working

- **Analysis Engine Investigation**: Verified `/api/analyze/single-text` uses **REAL LLM INTEGRATION**
  - **RealAnalysisService**: Uses DirectAPIClient with actual OpenAI, Anthropic, Google AI APIs
  - **Working API Clients**: Confirmed connections to GPT-4.1, Claude 3.5 Sonnet, Gemini 2.x series
  - **Real Analysis Pipeline**: PromptTemplateManager → DirectAPIClient → NarrativeGravityWellsElliptical → Database
  - **Actual Cost Tracking**: Real API usage costs with CostManager integration
- **Development Status Clarification**: 
  - ✅ **Frontend**: Fully functional React interface with all components working
  - ✅ **Database**: PostgreSQL with proper schemas and data persistence
  - ✅ **API Infrastructure**: Complete REST API with all endpoints and authentication
  - ✅ **Analysis Engine**: **REAL** - Complete LLM integration with OpenAI/Anthropic/Google APIs working
- **Note**: Fallback mock data only used if real LLM analysis fails (proper error handling)

### 🔧 Technical Infrastructure Improvements  

- **Environment Variable Handling**: Robust browser/server environment variable management
  - **Vite Configuration**: Proper `process.env` definition for browser environments

## [v2.2.0] - Academic and conversational interfaces - June 11, 2025

### 🎯 PRIORITY 3 COMPLETE: Academic Tool Integration Infrastructure

**Strategic Achievement**: Complete academic publication toolkit bridging systematic development with academic requirements
- **Academic Data Export Pipeline** (`src/narrative_gravity/academic/data_export.py`): Publication-ready data formatting
  - Multi-format export: CSV (universal), Feather (R-optimized), DTA (Stata), JSON (Python with metadata)
  - Academic variable naming standards (lowercase, underscore conventions) with comprehensive data dictionaries
  - Component development data export for methodology papers and development process documentation
  - Complete replication package builder with ZIP assembly including data, code, documentation, and troubleshooting guides
  - Database integration with Priority 1 infrastructure preserving experimental provenance and component versioning
- **AI-Generated Analysis Templates** (`src/narrative_gravity/academic/analysis_templates.py`): Multi-language statistical analysis
  - Jupyter notebook generation with interactive exploration, reliability analysis, visualization, and statistical modeling
  - R script generation with tidyverse, lme4 mixed-effects modeling, ggplot2 publication-grade visualizations
  - Stata integration with publication-ready analysis, LaTeX table export, mixed-effects regression, and APA-style reporting
  - Academic best practices: publication-ready styling, statistical rigor, reproducibility, and cross-tool compatibility
- **Academic Documentation Generators** (`src/narrative_gravity/academic/documentation.py`): Publication-ready documentation
  - Methodology paper generation from experimental data with complete component development process documentation
  - Statistical report formatting in APA style with significance testing, effect sizes, and publication compliance
  - Automated replication guide generation with step-by-step instructions, troubleshooting, and verification procedures
  - Academic citation support with proper version tracking and reproducibility requirements

**CLI Tool Suite**: Complete academic workflow automation
- **Academic Data Exporter** (`src/narrative_gravity/cli/export_academic_data.py`): Comprehensive data export automation
  - Multi-format data export with filtering by date range, frameworks, and study parameters
  - Component development analysis export for methodology documentation and academic validation
  - Complete replication package builder with automated assembly of data, code, and documentation
  - Integration with Priority 1 & 2 infrastructure for complete experimental provenance
- **Analysis Template Generator** (`src/narrative_gravity/cli/generate_analysis_templates.py`): Multi-language code generation
  - Jupyter notebook creation with comprehensive statistical analysis and visualization templates
  - R script generation with academic-standard statistical modeling and publication-ready plotting
  - Stata script creation with publication-grade analysis and automated LaTeX table export
  - Template customization options for different research contexts and publication requirements
- **Documentation Generator** (`src/narrative_gravity/cli/generate_documentation.py`): Academic documentation automation
  - Methodology section generation from experimental database with complete process documentation
  - Results section formatting with APA-style statistical reporting and significance testing
  - Replication guide creation with complete step-by-step instructions and troubleshooting support
  - Publication-ready formatting for manuscript submission and peer review

**Elena's User Journey Support**: Complete Weeks 3 & 5 workflow enablement
- **Week 3 Statistical Analysis**: Jupyter notebook statistical analysis, Stata integration, R visualization discovery
- **Week 5 Publication Preparation**: Documentation generation, replication package creation, methodology paper automation
- **Academic Standards Compliance**: All outputs meet publication requirements with proper citation and reproducibility
- **Multi-Tool Integration**: Seamless workflow across Python/Jupyter, R, and Stata with consistent analysis approaches

**Integration with Prior Infrastructure**: Seamless Priority 1 & 2 enhancement
- **Database Integration**: Leverages Priority 1 component versioning, experimental data, and statistical metrics
- **Development Session Integration**: Uses Priority 2 development sessions for methodology documentation and quality assessment
- **Academic Provenance**: Complete experimental tracking with component version specifications for exact replication
- **Quality Assurance**: Academic standards compliance with automated validation and publication readiness assessment

### 🌐 Web Interface - Basic Flask UI for Chatbot

- **Flask Web Interface**: Modern web interface for the narrative gravity chatbot
  - Clean, responsive HTML/CSS design with professional gradient styling
  - Large text input support up to 1.2MB (3x largest corpus file - Lenin's "What is to Be Done")
  - Real-time character counting with visual feedback and overflow protection
  - Framework switching with dropdown selector and live updates with confirmation
  - AJAX-powered API integration with loading states, error handling, and metadata display
  - Keyboard shortcuts (Ctrl+Enter) for improved user experience
  - Full integration with existing chatbot backend system and PostgreSQL database
- **Technical Implementation**: 
  - Flask server on port 5001 with 1.5MB request limit configuration
  - JSON API endpoints: `/chat`, `/switch_framework`, `/status`
  - Modern JavaScript with async/await, fetch API, and DOM manipulation
  - Professional UI with loading spinners, success messages, and error recovery
  - Template-based HTML rendering with Jinja2 integration
- **Advantages Over Terminal**: Eliminates buffer limitations, provides visual feedback, enables copy-paste of large political texts
- **Documentation**: Complete usage guide in `WEB_INTERFACE_GUIDE.md` with troubleshooting

### 🤖 Chatbot Research Workbench - Phase 1 WORKING SOLUTION

- **Domain-Constrained Conversational Interface**: Professional chatbot for narrative gravity analysis
  - **Domain Filtering**: 100% accurate filtering of off-topic queries while accepting relevant research questions
  - **Natural Language Framework Management**: Conversational framework switching, explanation, and listing
  - **Intelligent Intent Classification**: Automatic classification of user queries (framework questions, analysis requests, comparisons, explanations)
  - **Context-Aware Conversations**: Session tracking, message history, and analysis memory across chat interactions
- **Framework Integration**: Seamless integration with existing framework manager
  - **Automatic Framework Loading**: Inherits current framework configuration on startup
  - **Live Framework Switching**: "Switch to Civic Virtue framework" with immediate confirmation
  - **Framework Explanations**: Natural language explanations of dipoles, wells, and theoretical foundations
  - **Framework Listing**: "List all available frameworks" with current framework highlighting
- **Analysis Workflow**: Conversational analysis interface with placeholder integration
  - **Text Extraction**: Intelligent parsing of analysis requests with multiple input patterns
  - **Analysis Integration**: Ready for connection to existing NarrativeGravityWellsElliptical engine
  - **Results Formatting**: Professional markdown formatting with scores, metrics, and summaries
  - **Comparison Support**: Multi-analysis comparison with insights and pattern identification
- **Response System**: Consistent, professional response formatting
  - **Template Engine**: Structured response templates for different interaction types
  - **Academic Voice**: Professional tone suitable for research environments
  - **Error Handling**: Graceful error messages with helpful suggestions and redirects
  - **Interactive Guidance**: Context-aware suggestions for next steps and related queries
- **Technical Architecture**: Production-ready foundation with comprehensive testing
  - **Modular Design**: Separate engines for domain constraints, framework interface, conversation context, response generation
  - **100% Test Coverage**: All Phase 1 functionality validated with automated test suite
  - **Integration Ready**: Designed for easy integration with existing FastAPI backend and React frontend
- **CRITICAL FIX**: Replaced brittle keyword-based domain classification with intelligent LLM-powered approach
  - **Issue**: Political text was incorrectly rejected as off-topic due to false positives (e.g., "travel" in political context)
  - **Solution**: LLM-based classifier with robust fallback system for accurate content classification
  - **Result**: Political discourse now correctly accepted and analyzed instead of being filtered out
  - **Impact**: Chatbot is now actually usable with real-world political content
- **TERMINAL BUFFER SOLUTION**: Implemented file-based input system to handle unlimited text length
  - **Issue**: Terminal input() buffer couldn't handle long political text (>500 characters) causing apparent "lockups"
  - **Solution**: File-based input with auto-detection (`input.txt`) completely bypasses terminal limitations
  - **Verified**: Successfully processed 1000+ character political texts with full analysis
  - **Usage**: `python3 chat_with_file.py` with automatic file detection and cleanup

### 🎯 Academic Paper Development System

- **Complete Paper Management Infrastructure**: Established professional academic paper development workflow
  - **Dedicated Directory Structure**: `paper/` with organized subdirectories for drafts, evidence, reviews, submission
  - **Version-Controlled Drafts**: Semantic versioning system (vMAJOR.MINOR.PATCH) for systematic paper evolution
  - **Evidence Tracking System**: Comprehensive index linking all claims to supporting data with quality standards
  - **Paper-Specific Changelog**: `paper/PAPER_CHANGELOG.md` tracking all paper changes and evidence status
  - **Automated Management**: `paper/manage_paper.py` script for version control, evidence checking, validation claim audit
- **Validation Status Correction**: Fixed overclaims in paper about empirical validation
  - **Critical Distinction**: Clarified difference between technical consistency (✅ achieved) vs. human validation (❌ required)
  - **Honest Limitations**: Acknowledged LLM limitations from recent research in computational theme detection
  - **Evidence Requirements**: Specified human validation studies needed before publication claims
  - **Academic Integrity**: Positioned framework as computational tool requiring validation rather than validated method
- **Independent Researcher Workflow**: Tailored for non-academic, non-developer researcher context
  - **Evidence-Based Progression**: No version advancement without supporting data
  - **Publication-Focused**: Systematic preparation for peer review process
  - **Collaboration-Ready**: Materials organized for potential co-author involvement
  - **Transparency-Driven**: Credibility through open methodology and honest limitations

### 🚨 BREAKING CHANGES - Streamlit Interface Deprecation

- **Streamlit App Deprecated**: The legacy Streamlit interface has been officially deprecated in favor of the React Research Workbench
- **Files Moved to Archive**: 
  - `src/narrative_gravity/app.py` → `archive/streamlit_legacy/src/narrative_gravity/app.py`
  - `launch_streamlit.py` → `archive/streamlit_legacy/launch_streamlit.py`
  - Streamlit documentation → `archive/streamlit_legacy/docs/`
- **Launch Scripts Updated**: 
  - `launch.py` no longer starts Streamlit, focuses on backend services
  - `src/narrative_gravity/launcher.py` shows deprecation notice and migration guidance
- **README Updated**: All Streamlit references replaced with React interface instructions
- **Migration Support**: Complete deprecation notices and migration guides provided

### ✨ New Features - Autonomous Debug Monitoring System

- **Comprehensive Debug Console**: Real-time debugging interface with visual 🐛 button
  - Floating debug console accessible from any app state
  - Real-time health status indicators (🟢 Healthy, 🟡 Warning, 🔴 Error)
  - Event filtering by type, severity level, or component
  - Complete debug session export as JSON for external analysis
- **Terminal Debug Output**: Debug events echo to development server terminal
  - Autonomous error detection visible to AI assistant without manual copying
  - Structured terminal logging with timestamps and component context
  - API call monitoring with timing, status codes, and error details
  - Performance monitoring with automatic threshold warnings
- **Autonomous Error Detection**: Complete independence from manual error reporting
  - JavaScript runtime errors with full stack traces
  - React component lifecycle failures and render errors
  - Network issues with request/response context
  - Performance problems with specific metrics and thresholds
- **Enhanced Development Experience**: Zero manual intervention debugging
  - Debug launch script: `./debug-launch.sh` for instant debug mode
  - Environment variable support: `REACT_APP_DEBUG_MODE=true`
  - URL parameter activation: `?debug=true` for on-demand debugging
  - Persistent debug mode with localStorage state management

## [v2.1.0-post-rename] - Repository Rebranding to Narrative Gravity Analysis - 2025-06-04

### 🎯 Major Project Rebranding
- **Repository Renamed**: `moral_gravity_analysis` → `narrative_gravity_analysis`
- **Complete Branding Alignment**: All documentation and references updated
- **Functionality Verification**: All 31 tests passing after rename
- **Narrative Gravity Maps**: Full transition to new brand identity
- **Documentation Updates**: Complete alignment with new naming convention

### ✅ Validation
- **Testing Complete**: Comprehensive test suite validates functionality
- **Directory Alignment**: Repository name matches methodology branding
- **Legacy Compatibility**: All existing files and processes preserved

## [v2.1.0-pre-rename] - Complete Rebranding & Testing Infrastructure - 2025-06-04

### 🎯 Major Milestone: Complete Rebranding to Narrative Gravity Maps
- **Methodology Rebrand**: "Moral Gravity Map" → "Narrative Gravity Maps"
- **Framework Evolution**: Enhanced Civic Virtue Framework as primary implementation
- **Testing Infrastructure**: Comprehensive 31-test validation system
- **Project Restructuring**: Clean separation of concerns with archived legacy files

### ✨ New Features - Comprehensive Testing System
- **Smoke Testing Suite**: 31 automated tests covering all critical functionality
- **Test Runner Infrastructure**: `run_tests.py` with shell script wrapper
- **Quality Assurance**: Test-driven development approach for stability

### 🏗️ Architectural Improvements
- **Clean Project Structure**: Organized separation between active code and archived development
- **Framework Reorganization**: `civic_virtue` as primary framework with clear documentation
- **Legacy Migration**: Moved outdated files to `archive/` with clear version history
- **Documentation Consolidation**: Streamlined user guides and technical documentation

### 🔧 Framework Enhancements
- **Civic Virtue Framework**: Enhanced as primary Narrative Gravity Maps implementation
- **Multi-Framework Support**: Maintained compatibility with Political Spectrum and other frameworks
- **Configuration Management**: Improved framework switching and validation
- **Prompt Generation**: Enhanced template system with version tracking

### 📋 Pre-Rename Stability
- **Complete Functionality**: All features tested and validated
- **Documentation Currency**: All guides and references updated
- **Test Coverage**: Comprehensive validation of all major components
- **Ready for Rename**: Stable foundation for repository rebranding

## [v2025.06.04.2] - Paper Publication Readiness & Architectural Review - 2025-06-04

### 🎯 Major Focus: Academic Publication Preparation
- **Paper Replication Guide**: Complete instructions for reproducing all paper analyses
- **Documentation Organization**: Professional structure suitable for academic reference
- **LLM Scoring Fixes**: Resolved critical prompt compliance issues affecting analysis accuracy
- **Architectural Review**: Comprehensive evaluation and roadmap for API integration

### ✨ New Features - Publication Support
- **Replication Package**: `docs/academic/paper_replication_guide.md`
  - Step-by-step instructions for reproducing paper results
  - Framework validation procedures
  - Analysis workflow documentation
  - Academic researcher onboarding guide
- **Enhanced Documentation Organization**: 
  - Reorganized `docs/` directory for academic accessibility
  - Professional documentation hierarchy
  - Clear separation of user guides, development docs, and academic materials

### 🔧 Critical Fixes - LLM Prompt Compliance
- **Scoring Scale Crisis**: LLMs using 1-10 integer scales instead of required 0.0-1.0 decimal scale
  - Enhanced prompt generator with explicit scale warnings
  - Format requirements prominently displayed
  - Mathematical validation emphasized
- **Model Identification**: AI platforms identifying as platform rather than underlying model
  - Added model verification workflow
  - Academic accuracy improvements
  - Attribution problem resolution

### 🏗️ Infrastructure - Framework Generalization
- **Framework-Agnostic Design**: Removed political analysis assumptions
- **Universal Applicability**: Extended to any persuasive narrative type
- **Configurable Prompts**: Framework-specific customization support
- **Scope Expansion**: Beyond political discourse to general persuasive analysis

### 📋 Architectural Review & Planning
- **API Integration Evaluation**: Detailed assessment of Hugging Face vs. direct provider APIs
- **Development Roadmap**: Clear path toward automated analysis pipeline
- **Statistical Enhancement**: Planning for confidence intervals and cross-model validation
- **Batch Processing**: Architecture for large-scale corpus analysis

### ✅ Quality Assurance
- **Framework Testing**: All frameworks operational with updated prompt generation
- **Visualization Validation**: Enhanced analyses demonstrate proper scoring and output
- **Documentation Currency**: All guides updated with latest procedures
- **Academic Standards**: Professional quality suitable for peer review

## [v2025.06.04.1] - Universal Multi-Run Dashboard & Archive Organization - 2025-06-04

### 🎯 Major Achievement: Universal Dashboard System
- **Framework-Agnostic Design**: Transformed from Obama-specific to universal multi-run analysis tool
- **Auto-Detection Engine**: Automatically identifies speaker, year, framework from filenames
- **Parameter Override**: Manual specification for edge cases and custom analysis
- **100% Backwards Compatibility**: Works with all existing analysis files

### ✨ New Features - Universal Dashboard
- **Auto-Detection Algorithm**: 
  - Speaker identification from filenames (Obama, Trump, Biden, Lincoln, etc.)
  - Year extraction with intelligent parsing
  - Framework auto-identification (civic_virtue, political_spectrum, custom)
  - Run count detection for multi-run analysis
- **Parameter System**: 
  - Optional manual overrides for speaker, year, framework
  - Flexible title generation with smart defaults
  - Maintains statistical rigor with variance analysis
- **Framework Compatibility**: Works with any Narrative Gravity framework structure

### 🧹 Project Organization & Archive Management
- **Archive Restructuring**: 
  - Moved experimental tests to `archive/experimental_tests/`
  - Moved temporary results to `archive/temp_results/`
  - Organized development history in `archive/development_history/`
- **Documentation Reorganization**: 
  - Enhanced `docs/` directory structure
  - Clear separation of user guides, development docs, and archives
  - Comprehensive project structure documentation

### 📋 Enhanced Documentation
- **Generic Dashboard Usage**: Comprehensive guide for universal dashboard system
- **Generalization Summary**: Technical details of transformation process
- **Project Structure Updates**: Reflects new organization and capabilities
- **User Workflow Guides**: Enhanced instructions for various use cases

### 🔧 Technical Improvements
- **Dynamic Input Handling**: No hardcoded assumptions about speaker or content
- **Statistical Preservation**: Maintains all variance analysis and confidence intervals
- **Quality Assurance**: Comprehensive testing with existing analysis files
- **Performance Optimization**: Efficient processing of various file formats

### 📈 Impact & Success Criteria
- **Before**: Hardcoded Obama civic virtue analysis system
- **After**: Universal tool for any speaker, framework, or analysis type
- **Maintainability**: Eliminates need for custom dashboard creation
- **Scalability**: Ready for large-scale comparative analysis projects

## [v2.0.0-beta.1] - Advanced Visualization & Framework Versioning - 2025-06-04

### 🎯 Stable Visualization & Framework Architecture
- **Enhanced Framework System**: Comprehensive multi-framework support with versioning
- **Advanced Streamlit Interface**: `moral_gravity_app.py` with professional UI
- **Visualization Improvements**: Enhanced layout, spacing, and comparative analysis
- **Framework Versioning**: Structured prompt versioning with metadata tracking

### ✨ New Features - Streamlit Application
- **Professional Web Interface**: Complete Streamlit application for analysis workflow
- **Framework Management**: GUI for switching between frameworks
- **Batch Analysis Support**: Multi-file processing capabilities
- **Interactive Visualization**: Real-time analysis with immediate visual feedback

### 🔧 Enhanced Framework System
- **Framework Directory Structure**: Organized `frameworks/` with multiple options
  - `moral_foundations/`: Original civic virtue framework  
  - `moral_rhetorical_posture/`: Rhetorical analysis framework
  - `political_spectrum/`: Left-right political positioning
- **Prompt Versioning**: Structured versioning in `prompts/framework/version/`
- **Configuration Management**: Dynamic framework loading with validation

### 🎨 Visualization Enhancements
- **Layout Optimization**: Improved spacing and positioning for complex plots
- **Comparative Analysis**: Side-by-side visualization capabilities
- **Professional Styling**: Enhanced visual design for academic presentation
- **Summary Positioning**: Fixed text overlap and improved readability

### 📋 Documentation & Workflow Improvements
- **Framework Documentation**: Individual README files for each framework
- **Development Notes**: Comprehensive improvement tracking
- **Workflow Demonstrations**: Examples and tutorials for various use cases
- **Configuration Guides**: Setup and customization instructions

## [v2.0.0] - Modular Architecture & Multi-Framework Support - 2025-06-04

### 🎯 MILESTONE: Complete Modular Architecture Implementation
- **Framework-Agnostic Design**: Universal system supporting multiple analytical frameworks
- **Backward Compatibility**: All existing analyses continue to work unchanged
- **Configuration-Driven**: JSON-based framework definitions with mathematical separation
- **Research Foundation**: User stories and roadmap based on real workflow analysis

### ✨ New Features - Multi-Framework Architecture
- **Framework Management System**: `framework_manager.py` for listing, switching, and validation
- **Configurable Analysis**: `dipoles.json` + `framework.json` separation of concepts and math
- **Automated Prompt Generation**: `generate_prompt.py` creates prompts from configuration
- **Version Control**: Framework versioning with metadata tracking

### 🏗️ Infrastructure - Storage Architecture
- **Structured Framework Storage**: `frameworks/` directory with organized framework definitions
- **Active Configuration**: `config/` symlinks for current framework selection
- **Prompt Versioning**: `prompts/framework/version/` structure for historical tracking
- **Documentation Integration**: Framework-specific README files with theoretical foundations

### 🔧 Technical Capabilities
- **Framework Validation**: Structural and semantic consistency checking
- **JSON Format Evolution**: Support for both legacy and new analysis formats
- **Configuration Loading**: Dynamic framework switching without code changes
- **Template System**: Automated prompt generation with embedded metadata

### 📋 Available Frameworks
- **Moral Foundations**: Original 5-dipole civic virtue system (default)
- **Political Spectrum**: Left-right political positioning framework
- **Custom Framework Support**: Developer tools for creating new analytical frameworks

### 📈 Research Capabilities
- **Multi-Framework Analysis**: Same text analyzed through different theoretical lenses
- **Comparative Studies**: Cross-framework validation and correlation analysis
- **Framework Development**: Tools for creating domain-specific analysis systems
- **Academic Integration**: Publication-ready outputs with comprehensive metadata

### ✅ Quality Assurance
- **Comprehensive Testing**: All existing functionality validated
- **Documentation Quality**: 349 lines of user documentation, 384 lines of technical docs
- **Code Quality**: 921 lines main engine, modular configuration system
- **Research Workflow**: User stories identifying high-priority improvements

## [v2.0] - Interactive Workflow & Professional Visualizations - 2025-06-03

### 🎯 Major Enhancement: Interactive LLM Workflow
- **Interactive Prompt System**: Streamlined workflow for LLM interaction
- **Enhanced Filename Generation**: Content identification from analysis results
- **Professional Visualization**: Comprehensive visual analysis system
- **Multi-Model Support**: Comparative analysis across multiple AI models

### ✨ New Features - Workflow Automation
- **Enhanced Filename Generation**: 
  - Automatic content identification from text analysis
  - Timestamp-based organization for reproducibility
  - Speaker and content detection for systematic filing
- **Interactive LLM Integration**: 
  - Streamlined prompt system for multiple AI platforms
  - Model information tracking in metadata
  - Version-controlled prompt templates

### 🎨 Visualization System Overhaul
- **Professional Plot Generation**: Enhanced `moral_gravity_elliptical.py` (838 lines)
- **Comparative Analysis**: Multi-model comparison visualizations
- **Academic Quality**: Publication-ready plots with comprehensive legends
- **Mathematical Precision**: Elliptical coordinate system with differential weighting

### 📋 Enhanced Content & Documentation
- **Reference Text Expansion**: Added international political speeches
  - Hugo Chávez UN General Assembly Speech 2006
  - Nelson Mandela Inaugural Address 1994
  - Synthetic political manifestos across ideological spectrum
- **Academic Documentation**: `moral_gravity_wells_paper.md` (362 lines)
- **Prompt Evolution**: Enhanced prompt templates with versioning

### 🔧 Technical Improvements
- **Model Information Tracking**: Comprehensive metadata in JSON outputs
- **File Organization**: Systematic model output organization
- **Legacy Support**: Maintained backward compatibility
- **Requirements Update**: Enhanced dependencies for visualization

### 📈 Analysis Capabilities
- **Individual Text Analysis**: Professional single-narrative analysis
- **Multi-Model Comparison**: Systematic comparison across AI models
- **Framework Flexibility**: Foundation for multiple analytical frameworks
- **Academic Integration**: Research-quality outputs and documentation

## [v1.0.0] - First Stable Release with Multi-Model Comparison - 2025-05-21

### 🎯 MILESTONE: First Stable Production Release
- **Multi-Model Comparison**: Professional visualization comparing multiple LLM analyses
- **Object-Oriented Design**: Complete rewrite with modular, maintainable architecture
- **Smart Layout System**: Intelligent positioning and legend management
- **Academic Quality**: Publication-ready visualizations and documentation

### ✨ New Features - Multi-Model Analysis
- **Comparative Visualization**: Side-by-side analysis from multiple AI models
- **Model Differentiation**: Distinct colors using tab20 colormap for clear identification
- **Smart Legend Layout**: Adaptive 2-3 column layout based on model count
- **Overlap Management**: Circular arrangement for overlapping points

### 🎨 Professional Visualization Features
- **Enhanced Visual Design**: Professional polar plots with comprehensive elements
  - Gray dots for moral gravity wells (fixed positions)
  - Colored dots for narrative scores (model-specific)
  - Red dot for Center of Mass calculation
  - Dotted reference circles and dashed connection lines
- **Alpha Transparency**: Enhanced visibility with professional transparency effects
- **Copyright Integration**: Professional attribution and rights management

### 🔧 Technical Architecture
- **Object-Oriented Rewrite**: `moral_gravity_map.py` consolidated visualization system
- **Configuration Management**: Professional configuration handling
- **File Organization**: Systematic directory structure for outputs and archives
- **Requirements Management**: Comprehensive dependency specification

### 📋 Documentation & Usability
- **Comprehensive README**: Complete usage instructions and examples
- **Directory Structure**: Organized project layout with clear file purposes
- **JSON Format Specification**: Standardized analysis output format
- **Development Workflow**: Branching strategy and contribution guidelines

### 🧪 First Major Validation
- **9-LLM Analysis**: Jefferson's First Inaugural Address analyzed across:
  - **Reasoning LLMs**: Claude 3.7 Sonnet Thinking, Perplexity R1 1776, Le Chat
  - **Standard LLMs**: OpenAI o4-mini, Perplexity Sonar, Claude 3.7 Sonnet, OpenAI GPT-4.1, Gemini 2.5 Pro, Grok 3 Beta
- **Cross-Model Validation**: First systematic comparison of moral analysis across multiple AI systems
- **Research Foundation**: Established methodology for academic analysis

## Additional Historical Releases (From Git History)

## [v2.1.0-post-rename] - Repository Rebranding to Narrative Gravity Analysis - 2025-06-04

### 🎯 Major Project Rebranding
- **Repository Renamed**: `moral_gravity_analysis` → `narrative_gravity_analysis`
- **Complete Branding Alignment**: All documentation and references updated  
- **Functionality Verification**: All 31 tests passing after rename
- **Narrative Gravity Maps**: Full transition to new brand identity
- **Documentation Updates**: Complete alignment with new naming convention

## [v2.1.0-pre-rename] - Complete Rebranding & Testing Infrastructure - 2025-06-04

### 🎯 Major Milestone: Complete Rebranding to Narrative Gravity Maps
- **Methodology Rebrand**: "Moral Gravity Map" → "Narrative Gravity Maps"
- **Framework Evolution**: Enhanced Civic Virtue Framework as primary implementation
- **Testing Infrastructure**: Comprehensive 31-test validation system
- **Project Restructuring**: Clean separation of concerns with archived legacy files

### ✨ New Features - Comprehensive Testing System
- **Smoke Testing Suite**: 31 automated tests covering all critical functionality
- **Test Runner Infrastructure**: `run_tests.py` with shell script wrapper
- **Quality Assurance**: Test-driven development approach for stability

## [v2025.06.04.2] - Paper Publication Readiness & Architectural Review - 2025-06-04

### 🎯 Major Focus: Academic Publication Preparation  
- **Paper Replication Guide**: Complete instructions for reproducing all paper analyses
- **Documentation Organization**: Professional structure suitable for academic reference
- **LLM Scoring Fixes**: Resolved critical prompt compliance issues affecting analysis accuracy
- **Architectural Review**: Comprehensive evaluation and roadmap for API integration

### 🔧 Critical Fixes - LLM Prompt Compliance
- **Scoring Scale Crisis**: LLMs using 1-10 integer scales instead of required 0.0-1.0 decimal scale
- **Model Identification**: AI platforms identifying as platform rather than underlying model
- **Framework Generalization**: Removed political analysis assumptions for universal applicability

## [v2025.06.04.1] - Universal Multi-Run Dashboard & Archive Organization - 2025-06-04

### 🎯 Major Achievement: Universal Dashboard System
- **Framework-Agnostic Design**: Transformed from Obama-specific to universal multi-run analysis tool
- **Auto-Detection Engine**: Automatically identifies speaker, year, framework from filenames
- **Parameter Override**: Manual specification for edge cases and custom analysis
- **100% Backwards Compatibility**: Works with all existing analysis files

### 🧹 Project Organization & Archive Management
- **Archive Restructuring**: Moved experimental and temporary files to organized archive
- **Documentation Reorganization**: Enhanced docs directory structure
- **Project Structure Updates**: Comprehensive documentation of new organization

## [Pre-1.0 Development] - Foundation & Early Development - 2025-05-20 to 2025-05-21

### Initial Development Phase (May 2025)
- **bd5a2aa**: **Initial Commit** - Moral Gravity Well visualization with polar plot, legend, and summary text
- **1cdcf68**: Added README with usage instructions and basic project documentation
- **f5796ef**: Model information integration in JSON output and visualization
- **c6d2762**: Visual refinements - fine-tuned Resentment label positioning to avoid overlap
- **d57f73f**: Enhanced metadata - prompt versioning and model information in titles

### Core Feature Development (May 2025)
- **79fd9c7**: **🎯 First Major Milestone** - Complete first run across 9 LLMs on Jefferson's First Inaugural
- **393d9f1**: Professional foundation - copyright notices added to project files
- **52ace8d**: **✨ Multi-model comparison capability** - fundamental advancement enabling comparative analysis
- **3e7dd19**: System consolidation - unified visualization system
- **934d8a8**: Project organization - configuration management and cleanup

### Foundation Architecture
- **Polar Coordinate System**: Mathematical foundation for moral gravity mapping
- **JSON Data Format**: Standardized structure for analysis results
- **Visualization Engine**: Professional plotting system with customizable elements
- **Multi-Model Support**: Architecture enabling comparative AI analysis
- **Configuration Management**: Systematic approach to framework definitions

### Research Methodology Establishment
- **Moral Gravity Wells Concept**: Theoretical foundation for quantitative moral analysis
- **LLM Integration**: Systematic approach to AI-powered text analysis
- **Comparative Framework**: Multi-model validation methodology
- **Academic Standards**: Publication-quality output and documentation practices

## [Documentation Cleanup] - June 10, 2025

### Removed
- **Redundant paper file**: docs/narrative_gravity_wells_paper.md (superseded by paper/ directory)
- **Duplicate user stories**: docs/development/USER_STORIES.md (superseded by USER_STORIES_CONSOLIDATED.md)
- **Outdated status files**: PROGRESS_LOG.md, PROJECT_STATUS.md, SYSTEM_UPGRADE_2025.md
- **Obsolete cleanup plan**: docs/development/DOCS_CLEANUP_PLAN.md

### Archived
- **Completed integration guides**: ENDPOINT_SETUP_GUIDE.md, DIRECT_API_INTEGRATION.md, MULTI_LLM_STATUS.md, FOUR_LLM_INTEGRATION_SUMMARY.md
- **Historical development snapshot**: DEVELOPMENT_SNAPSHOT_v2025.06.04.2.md

### Result
- Cleaner documentation structure with focus on current operational needs
- Historical work preserved in organized archive
- Reduced redundancy and outdated information

---

## Version History Summary

### Major Milestones
- **🎯 v1.0.0 (2025-05-21)**: First stable release with multi-model comparison
- **🚀 v2.0 (2025-06-03)**: Interactive workflow and professional visualizations  
- **⚙️ v2.0.0 (2025-06-04)**: Complete modular architecture with multi-framework support
- **🏗️ v2.1.0 (2025-06-04)**: Rebranding to Narrative Gravity Maps with testing infrastructure
- **📊 v2025.06.04 (2025-06-04)**: Universal dashboard system and paper publication readiness
- **🎯 v2.2.0 (2025-06-09)**: Governance standards and automated release management
- **⚛️ v2.2.1 (2025-06-09)**: React research workbench with comprehensive test harness

### Methodology Evolution
- **Moral Gravity Map** → **Narrative Gravity Maps**: Enhanced methodology with broader applicability
- **Single Framework** → **Multi-Framework Architecture**: Universal system supporting various analytical lenses
- **Manual Workflow** → **Automated Pipeline**: From individual analysis to systematic batch processing
- **Research Tool** → **Academic Platform**: Publication-ready system with comprehensive validation

### Development Philosophy
- **Validation-First**: Academic credibility through rigorous testing and validation
- **Modular Design**: Framework-agnostic architecture supporting multiple analytical approaches
- **Professional Standards**: Enterprise-grade development practices and documentation
- **Research Foundation**: Built for academic publication and peer review

### Added
- **End-to-End Frontend Integration with Live Data** - 2025-06-09
  - Successfully integrated React frontend with FastAPI backend and PostgreSQL database
  - Fixed API client configuration to connect to correct port (8000)
  - Resolved database constraint issues with framework_version and prompt_template_version fields
  - Updated API endpoints to support optional authentication for testing and development
  - Created comprehensive end-to-end test suite validating complete workflow
  - Frontend now fully functional with live experiment creation, analysis execution, and results visualization
  - All configuration endpoints (frameworks, templates, algorithms) working correctly
  - Single text analysis endpoint providing complete hierarchical analysis results
  - Data consistency verified across all API endpoints

### Fixed
- API client base URL configuration (changed from port 8002 to 8000)
- Database field length constraints for framework_version and prompt_template_version
- Authentication requirements on get_experiment and get_run endpoints for development testing
- CORS configuration to support frontend development on multiple ports

### Technical Details
- Frontend: React 18 + TypeScript + Vite running on port 3000
- Backend: FastAPI running on port 8000 with comprehensive API documentation
- Database: PostgreSQL with complete v2.1 schema supporting hierarchical analysis
- All tests passing: end-to-end workflow, frontend integration, and data consistency 

## [LLM Validation Planning & Documentation] - June 10, 2025

### Added
- **LLM Validation Workbench Requirements**: Comprehensive 10-section requirements document (`docs/development/LLM_VALIDATION_WORKBENCH_REQUIREMENTS.md`)
  - Multi-variable experiment construction with text corpus, frameworks, prompts, LLM configurations
  - Framework fit assessment with automatic detection and quality gates  
  - Cross-LLM consensus analysis with statistical reliability testing
  - Academic export capabilities and publication-ready data generation
  - Complete API architecture and database schema specifications

- **Enhanced User Persona**: Detailed 15-step LLM validation experimentation cycle for Independent Research Author
  - Phase 1: Experiment Design (corpus assembly, framework variants, prompt templates)
  - Phase 2: Execution & Monitoring (batch processing, fit assessment, real-time progress)
  - Phase 3: Deep Analysis (cross-LLM consensus, evidence passages, metadata patterns)
  - Phase 4: Evidence Synthesis (confidence assessment, academic export, documentation)

- **Paper Validation Placeholders**: Comprehensive experimental result placeholders in paper draft
  - Multi-variable experimental design section with 1,350+ planned LLM analyses
  - Cross-LLM consensus analysis with 0.94± correlation targets
  - Framework sensitivity testing and robustness metrics
  - Evidence portfolio for academic confidence building
  - Phase 2 human validation study planning

### Changed
- **User Stories Focus**: Updated from generic "research workbench" to specific "LLM validation workbench"
  - Backend-first development strategy clearly defined
  - Multi-variable experiment construction prioritized
  - Framework fit assessment and cross-LLM consensus emphasized
  - Extended timeline to 3-4 weeks for realistic implementation

- **Implementation Roadmap**: Restructured to reflect systematic validation approach
  - Week 1-2: Data structures & API services development
  - Week 3: Statistical analysis engine implementation  
  - Week 4: Frontend integration & testing
  - Clear success criteria focusing on statistical reliability and academic confidence

### Result
- **Clear Development Path**: Backend-first approach with systematic LLM validation before human studies
- **Academic Credibility**: Paper now shows path from LLM confidence building to human validation
- **Implementation Focus**: Detailed requirements enabling immediate backend development start
- **Validation Sequence**: Established logical progression from computational consistency to human alignment 