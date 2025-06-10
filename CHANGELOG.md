# Narrative Gravity Maps - Changelog

## [Unreleased]

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
  - CLI command validation and error handling
  - Streamlit application startup and core functionality
  - Framework switching and configuration validation
  - File processing and visualization generation
  - Cross-platform compatibility checks
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