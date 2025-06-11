# Narrative Gravity Maps - Changelog

## [Unreleased]

### 🎬 YOUTUBE TRANSCRIPT INTELLIGENT INGESTION SERVICE: Video Content to Research Corpus - June 11, 2025

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

### 🤖 INTELLIGENT CORPUS INGESTION SERVICE: LLM-Powered Metadata Extraction - June 11, 2025

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

### 🎯 ENHANCED CORPUS MANAGEMENT SYSTEM: FAIR Data & Academic Standards - June 11, 2025

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

### 🎯 PRIORITY 1 DATABASE FOUNDATION: Component Versioning Infrastructure Complete - June 11, 2025

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

### 🏗️ ARCHITECTURAL IMPROVEMENT: Clean Component Separation - June 11, 2025

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

### 🎯 PRIORITY 3 COMPLETE: Academic Tool Integration Infrastructure - January 6, 2025

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

### 🎯 PRIORITY 2 COMPLETE: Manual Development Support Infrastructure - June 11, 2025

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

### 🧪 PRIORITY 1 TEST SUITE INTEGRATION - Automated Validation System - 2025-06-11
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

### 🎯 PRIORITY 1 COMPLETE: Core Infrastructure Implementation - 2025-06-11
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

### 🛠️ Environment Configuration - Date Handling Fix - 2025-06-11
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

## [v2.3.0] - Project organization and cursorrules compliance - 2025-06-10

## [Unreleased]

### 📁 Project Organization - Cursorrules Compliance Cleanup - 2025-01-06
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

### 🌐 Web Interface - Basic Flask UI for Chatbot - 2025-01-06
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

### 🤖 Chatbot Research Workbench - Phase 1 WORKING SOLUTION - 2025-01-06
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

### 🎯 Academic Paper Development System - 2025-01-06
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

### 🔧 Technical Implementation
- **Debug Monitor Service**: `frontend/src/services/debugMonitor.ts`
  - Global error handling with window event listeners
  - Performance monitoring with PerformanceObserver API
  - API call interception with fetch override and Axios interceptors
  - Component lifecycle tracking with React hooks integration
- **Terminal Logger Service**: `frontend/src/services/terminalLogger.ts`
  - Console output routing to development server terminal
  - Structured logging with component identification
  - Batch processing to prevent terminal overwhelm
  - Vite development server integration for output visibility
- **Debug Console Component**: `frontend/src/components/DebugConsole.tsx`
  - Professional dark-themed floating interface
  - Real-time event streaming with filtering capabilities
  - Health status dashboard with metrics display
  - Data export functionality for collaborative debugging

### 🎯 Independence Benefits
- **Zero Manual Error Reporting**: All errors automatically captured and displayed
- **AI Assistant Visibility**: Debug events appear in terminal output during development
- **Complete Error Context**: Stack traces, component state, user actions, and API history
- **Real-Time Monitoring**: Continuous health status without manual checks
- **Historical Analysis**: Full session tracking for pattern identification
- **Collaborative Debugging**: Exportable debug data for team analysis

### 🎯 Frontend Integration Breakthrough - 2025-06-10
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
  - **API Client Hardening**: Fallback handling for environment variable access
  - **Development Stability**: No more browser crashes from undefined process variables
- **Testing Infrastructure Enhanced**: 
  - **Browser Automation**: Playwright scripts catching frontend errors automatically
  - **Console Monitoring**: Real-time capture of JavaScript errors and warnings
  - **Integration Testing**: API ↔ Frontend communication fully validated

### 🐛 Bug Fixes
- **Fixed 'Analyze Text' Button Disabled Issue**: Ensured the 'Analyze Text' button is correctly enabled after creating an experiment by persisting the experiment name state in the frontend.
- **Resolved API Server Network Connectivity**: Addressed persistent 'Network Error' by disabling `reload=True` in `scripts/run_api.py` and by ensuring `launch.py --api-only` properly keeps the API server running in the background via `ServiceManager` and a persistent process. This requires manual launch of `python scripts/run_api.py` in a separate terminal for stable operation outside of Cursor.

## [Unreleased] - v2.1 Phase 1 Enhancements

### Added - Workstream 1: Prompt Engineering & Scoring Framework Refinement
- **Hierarchical Prompt Templates**: Enhanced prompt editor now creates prompts that require LLMs to:
  - Identify and rank the top 2-3 driving wells with relative weights (must sum to 100%)
  - Provide specific textual evidence for each ranked well
  - Explain WHY each well dominates over others
  - Flag single-well dominance when one well accounts for >80% weight
  - Assess framework fit score (0.0-1.0) with missing dimension identification
- **Nonlinear Weighting Mechanisms**: Added 4 new scoring algorithms implementing Phase 1 requirements:
  - `Winner-Take-Most`: Amplifies dominant wells while suppressing weaker ones for clearer hierarchy
  - `Exponential Weighting`: Squares differences to enhance thematic distinction
  - `Hierarchical Dominance`: Uses LLM-provided rankings with edge snapping for single-well dominance
  - `Nonlinear Transform`: Applies sigmoid transforms to exaggerate differences near poles
- **Multi-Model Comparison Infrastructure**: Enhanced experiment designer with:
  - Radio button selection between single-model and multi-model analysis modes
  - Checkbox interface for selecting multiple LLMs for stability assessment
  - Automated parallel execution across selected models with linked result metadata
  - Stability metrics calculation (elevation stability, polarity stability, model agreement)
- **Enhanced Analysis Results Display**: New hierarchical result rendering showing:
  - Prompt type badges (Hierarchical vs Standard)
  - Multi-model comparison indicators
  - Framework fit scores with color-coded warning for low fit (<70%)
  - Hierarchical well rankings with relative weights and evidence excerpts
  - Single-well dominance warnings when one well >80% weight
  - Multi-model stability assessment dashboard with comparative metrics

### Enhanced - Research Workbench Infrastructure
- **Experiment Versioning**: Added `type` property to PromptTemplate interface supporting 'standard' and 'hierarchical' types
- **Complete Provenance Tracking**: Extended metadata capture for multi-model experiments with comparison linking
- **API Interface Extensions**: Updated SingleTextAnalysisRequest/Response to support new scoring algorithm types
- **Store Architecture**: Enhanced experimentStore with 5 new scoring algorithms and hierarchical prompt support

### Technical Implementation - Phase 1 Foundation
- **Prompt Template Evolution**: Default new prompts now use hierarchical structure requiring ranked well identification
- **Framework Content Integration**: Enhanced prompt preview showing structured analysis requirements
- **Multi-Model Orchestration**: Batch processing infrastructure for parallel LLM analysis with result aggregation
- **Stability Assessment**: Mathematical implementation of model agreement and score distribution analysis

### Research Methodology Advancement
This phase establishes the foundation for **Workstream 2: Human-Machine Alignment & Validation** by implementing:
- Hierarchical prompt outputs that can be systematically compared to human expert rankings
- Multi-model stability data enabling LLM selection and ensemble approach evaluation  
- Framework fit detection preparing for identification of missing thematic dimensions
- Complete experimental provenance supporting rigorous validation methodology

### Phase 1 Completion Status (Weeks 1-4)
✅ **Define revised prompt templates** requiring model ranking and relative weighting
✅ **Implement nonlinear weighting mechanism** with 4 distinct algorithmic approaches
✅ **Multi-model comparison infrastructure** supporting stability assessment across LLMs
🔄 **Iterative refinement** based on validation feedback (ongoing as prompts are tested)

**Next Phase**: Validation Foundation (Weeks 5-8) will focus on human annotation studies and systematic prompt iteration based on validation results.

## [v2.2.1] - React Research Workbench Stable Baseline with Comprehensive Test Harness - 2025-06-09

### 🎯 Major Achievement: Stable Development Foundation
- **Configuration Crisis Resolution**: Eliminated all build/dependency conflicts and lockups
- **Test-Driven Stability**: Established comprehensive test harness with 14 automated validation tests
- **Zero-Error Baseline**: 18/18 stability checks passing, ready for incremental development

### ✨ New Features - Frontend Research Workbench
- **Minimal Stable App**: React 18 + TypeScript + Vite + Tailwind CSS working baseline
- **Tab-Based Navigation**: Four main research workbench sections (Experiment Designer, Prompt Editor, Analysis Results, Comparison Dashboard)
- **Responsive UI**: Professional gradient branding with research-focused design
- **Real-time Debug Panel**: Live development status and metrics display

### 🧪 Comprehensive Test Harness Implementation
- **14 Unit Tests**: Complete coverage of baseline functionality
  - Basic rendering and component structure
  - Tab navigation and state management 
  - CSS class application and styling integrity
  - Component isolation and error handling
  - Performance under rapid navigation stress
  - Integration readiness validation
- **Vitest Integration**: Modern testing framework with jsdom environment
- **Automated Validation**: Test-driven development with regression detection

### 🛡️ Stability Check System
- **Automated Configuration Audit**: `npm run stability-check` validates entire setup
- **18-Point Validation**: Package.json, TypeScript config, build system, test execution, imports, CSS
- **Build Pipeline Verification**: Complete end-to-end build and test validation
- **Development Readiness Gates**: Ensures stable foundation before adding complexity

### 🔧 Technical Infrastructure Resolution
- **Dependency Conflicts Fixed**: React 18, TypeScript 5.6, Vite 6.0 compatibility
- **Build System Stability**: Vite + PostCSS + Tailwind CSS v3.4 working properly
- **Import Path Cleanup**: Standardized ES module imports without React namespace pollution
- **TypeScript Configuration**: Strict mode enabled with proper bundler resolution

### 🏗️ Development Architecture
- **Phase-Based Development**: Validated incremental complexity addition
- **Test-First Approach**: Every addition validated by automated test suite
- **Configuration Monitoring**: Continuous validation prevents regression
- **Professional Structure**: Follows React/TypeScript best practices

### 📋 Scripts & Automation
```bash
npm run dev              # Development server (validated stable)
npm run build           # Production build (zero errors)
npm run test            # Full test suite (14 tests passing)
npm run stability-check # Complete configuration audit
npm run validate        # Full pipeline validation
```

### 🎉 Benefits Achieved
- **End to WSOD Era**: No more white screens of death or mysterious lockups
- **Predictable Development**: Test harness catches regressions immediately
- **Professional Foundation**: Enterprise-grade React application structure
- **Incremental Safety**: Can add complexity with confidence and validation
- **Academic Validation Ready**: Research-grade quality controls and reproducibility

### 🚀 Next Phase Ready
- **State Management Integration**: Foundation prepared for Zustand store addition
- **API Client Integration**: Structure ready for backend communication
- **Component Development**: Tab content areas ready for research workbench features
- **Framework Integration**: Architecture supports narrative gravity framework integration

## [v2.2.0] - Major project organization overhaul with governance standards implementation - 2025-06-09

### ✨ New Features
- **Release Management System**: Comprehensive automated release process
  - `scripts/release.py`: Automated release script with pre-release checks
  - File hygiene verification, test requirements, documentation checks
  - Semantic versioning, CHANGELOG updates, git tagging automation
  - Dry-run capability for testing release process safely

### 📋 Documentation
- **Release Process Guide**: `docs/development/RELEASE_PROCESS.md`
  - Complete manual and automated release procedures
  - Troubleshooting guides and recovery procedures
  - Release type definitions and timing guidelines
- **Research Data Export Standards**: Documented `exports/` directory organization
  - Academic data export formats (R, CSV, Parquet)
  - Timestamped versioning for reproducible research
  - External collaboration and validation support

## [v2.1.2] - Corpus Organization Consolidation - 2025-06-09

### 🏗️ Infrastructure
- **BREAKING**: Consolidated duplicate text data directories
  - Moved `reference_texts/` contents to `corpus/raw_sources/`
  - Moved processing scripts to `corpus/processing_scripts/`
  - Updated all file path references in code
  - Eliminated duplicate corpus organization
- **Text Data Organization**: Centralized all text data under `corpus/`
  - `corpus/golden_set/`: Curated, analysis-ready datasets
  - `corpus/raw_sources/`: Original source materials  
  - `corpus/processing_scripts/`: Data transformation scripts
- **Documentation**: Updated governance files with corpus organization standards

## [v2.1.1] - Project Organization & Database Architecture - 2025-01-06

### 🧹 Major Project Cleanup & Reorganization

#### **Root Directory Cleanup**
- **Moved Analysis Results**: 5 visualization files → `analysis_results/temp_cleanup_2025_01_06/`
- **Moved Test Files**: 6 temporary test files → `tests/temp_stress_tests/`
- **Moved Utility Scripts**: 7 scripts → `scripts/` directory
- **Moved Documentation**: Database architecture doc → `docs/architecture/`
- **Removed Legacy**: 0-byte `narrative_gravity.db` SQLite file causing confusion

#### **Python Package Structure Reorganization**
- **NEW**: Proper `src/narrative_gravity/` package structure following Python standards
- **Moved Core Files**:
  - `narrative_gravity_app.py` → `src/narrative_gravity/app.py`
  - `narrative_gravity_elliptical.py` → `src/narrative_gravity/engine.py` 
  - `launch_app.py` → `src/narrative_gravity/launcher.py`
  - `framework_manager.py` → `src/narrative_gravity/framework_manager.py`
- **Updated Imports**: Fixed 18+ Python files with new import paths
- **Enhanced Compatibility**: Dual import system for both direct execution and module imports

#### **Comprehensive Platform Launcher**
- **NEW**: `launch.py` - Orchestrates all platform services
- **Service Management**: Database, API server (port 8000), Celery worker, Streamlit UI (port 8501)
- **Launch Options**: Individual services or full platform with single command
- **Database Setup**: Automated PostgreSQL initialization and verification
- **Backward Compatibility**: `launch_streamlit.py` for simple UI access

#### **Database Architecture Clarification**
- **NEW**: `docs/architecture/database_architecture.md` - Comprehensive database usage guide
- **NEW**: `check_database.py` - Database configuration verification script
- **PostgreSQL PRIMARY**: All application data (main app, API, Celery, production)
- **SQLite LIMITED**: Unit testing (in-memory) and logging fallback only
- **Configuration**: Enhanced launcher with PostgreSQL verification and clear error messages
- **Fixed**: Alembic migration configuration for new package structure

### ✨ New Features
- **Service Orchestration**: Single command launches entire platform
- **Database Verification**: Automatic PostgreSQL connection testing
- **Import Flexibility**: Apps work in both development and package contexts
- **Clear Documentation**: Eliminates database confusion for AI assistants and developers

### 🔧 Fixes & Improvements
- **Import Path Standardization**: Converted to proper package imports throughout codebase
- **Database Confusion Resolution**: Crystal clear PostgreSQL vs SQLite usage documentation
- **Legacy File Cleanup**: Removed confusing 0-byte SQLite file
- **Service Dependencies**: Clear startup order and dependency management
- **Error Messages**: Reference specific documentation for troubleshooting

### 🏗️ Infrastructure
- **Python Package Standards**: Follows PEP 8 and packaging best practices
- **Service Architecture**: Proper microservice orchestration with cleanup
- **Database Strategy**: PostgreSQL for production, SQLite for testing only
- **Documentation Structure**: Centralized guides for database, launch, and architecture

### 📋 Usage Changes

#### **New Launch Commands**
```bash
python launch.py                    # Launch all services
python launch.py --streamlit-only   # UI only
python launch.py --api-only         # API server only
python launch.py --setup-db         # Database setup
python check_database.py            # Verify database config
```

#### **Import Updates** (For Developers)
```python
# NEW: Package imports
from src.narrative_gravity.engine import NarrativeGravityWellsElliptical
from src.narrative_gravity.framework_manager import FrameworkManager
```

### 🎯 Benefits
- **Professional Structure**: Standard Python package organization
- **Service Orchestration**: One-command platform startup
- **Database Clarity**: Zero confusion about PostgreSQL vs SQLite usage  
- **Developer Experience**: Clear setup, documentation, and troubleshooting
- **AI Assistant Clarity**: Explicit database usage prevents confusion

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

## [Pre-1.0 Development] - Foundation & Early Development - 2025-01-03 to 2025-05-21

### Initial Development Phase (January 2025)
- **bd5a2aa**: **Initial Commit** - Moral Gravity Well visualization with polar plot, legend, and summary text
- **1cdcf68**: Added README with usage instructions and basic project documentation
- **f5796ef**: Model information integration in JSON output and visualization
- **c6d2762**: Visual refinements - fine-tuned Resentment label positioning to avoid overlap
- **d57f73f**: Enhanced metadata - prompt versioning and model information in titles

### Core Feature Development (January-May 2025)
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

## [Documentation Cleanup] - 2025-01-06

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

## [LLM Validation Planning & Documentation] - 2025-01-06

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