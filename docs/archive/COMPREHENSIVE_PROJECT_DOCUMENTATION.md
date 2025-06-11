# Narrative Gravity Maps - Comprehensive Project Documentation
*Version: 2025.06.06 - Complete Technical Reference for Requirements Definition & LLM Collaboration*

## 🎯 Purpose

This document contains complete project information for the **Narrative Gravity Maps** framework (current version) to enable detailed requirements definition and collaboration with other LLMs in product manager mode. It includes architecture overview, Epic 1-4 completion status, current capabilities, validation-first strategy, and technical specifications needed for systematic development planning.

**Current Status**: Epic 1-4 infrastructure complete (99.5% test success rate), MetricsCollector bug fixed, now focused on validation-first development for academic credibility.

## 📋 Table of Contents

1. [Current Status & Strategic Position](#current-status--strategic-position)
2. [Epic 1-4 Completion Summary](#epic-1-4-completion-summary)
3. [Validation-First Development Strategy](#validation-first-development-strategy)
4. [Architecture Summary](#architecture-summary)
5. [Core Source Code](#core-source-code)
6. [Configuration System](#configuration-system)
7. [Framework Definitions](#framework-definitions)
8. [Current Validation & Research Requirements](#current-validation--research-requirements)
9. [Testing Infrastructure](#testing-infrastructure)
10. [Documentation](#documentation)

---

## 1. Current Status & Strategic Position

### ✅ Infrastructure Complete (Epic 1-4)
- **Backend Infrastructure**: Celery + Redis + PostgreSQL + FastAPI ✅
- **Multi-LLM Integration**: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro ✅
- **Golden Set Corpus**: 17 curated texts with metadata ✅
- **Universal Multi-Run Dashboard**: Auto-detection and framework agnostic ✅
- **Framework Support**: Civic Virtue, Political Spectrum, Moral Foundations ✅

### 🎯 Current Strategic Priority: Validation-First Development
**CRITICAL**: Academic credibility must be established before advancing to Milestone 2.

**Phase 1 (Weeks 1-3)**: Core Reliability Validation
- Multi-run consistency studies (17 texts × 3 frameworks × 3 LLMs × 5 runs = 765 analyses)
- Inter-LLM correlation analysis and consensus thresholds
- Framework internal consistency validation

**Phase 2 (Weeks 4-5)**: Interpretive Intelligence
- Evidence extraction systems with supporting quotes
- Automated report generation for human understanding
- Comparative analysis capabilities

**Phase 3 (Weeks 6-8)**: Conversational Analysis Interface
- Domain-specific AI assistant for natural language queries
- Hybrid local/remote LLM architecture
- User-friendly interface for non-technical stakeholders

### Key Current Capabilities
- **Framework-Agnostic Design**: Modular architecture supports any persuasive narrative type
- **Mathematical Rigor**: Elliptical coordinate system with differential weighting
- **Visualization Engine**: Automated generation of publication-ready plots
- **Universal Dashboard**: Auto-detects framework and metadata from filenames
- **Interactive Interface**: Streamlit app with comprehensive workflow management

---

## 2. Epic 1-4 Completion Summary

### ✅ Epic 1: Corpus & Job Management Backend (COMPLETED)
**Infrastructure**: Full backend services implementation
- **Data Models**: Corpus, Document, Chunk, Job, Task with PostgreSQL + Alembic
- **JSONL Ingestion**: Schema validation and metadata extraction
- **Queue & Orchestration**: Celery + Redis with fault-tolerant processing
- **APIs**: Complete REST endpoints for corpus and job management
- **Resumability**: Exponential backoff retry logic for LLM API failures
- **Testing**: 99.5% test success rate (181/182 tests passing)
- **Bug Fixes**: MetricsCollector increment_metric method completed

### ✅ Epic 2: Hugging Face API Integration Backend (COMPLETED)
**Multi-LLM Integration**: Unified access to multiple LLMs
- **Unified API**: Single integration point through HuggingFace
- **Model Support**: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro
- **Cost Tracking**: Integrated billing and usage monitoring
- **Rate Limiting**: Transparent retry and backoff strategies

### ✅ Epic 3: Results Analysis Backend (COMPLETED)
**Statistical Analysis**: Comprehensive reliability metrics
- **Variance Analysis**: Multi-run consistency measurements
- **Confidence Intervals**: Statistical reliability quantification
- **Inter-Model Agreement**: Cross-LLM consensus validation
- **Export Capabilities**: CSV/JSON for academic replication

### ✅ Epic 4: Admin Interface & Monitoring (COMPLETED)
**User Interface**: Complete workflow management
- **Streamlit Dashboard**: Real-time job monitoring and cost tracking
- **Upload Interface**: JSONL corpus ingestion with validation
- **Results Viewer**: Visualization and export capabilities
- **Settings Management**: Framework selection and parameter configuration

### 🆕 Additional Achievements Beyond Epic 1-4:
- **Universal Multi-Run Dashboard**: Auto-detection system for any framework/speaker/year
- **Golden Set Corpus**: 17 carefully curated texts for validation studies
- **Framework-Agnostic Architecture**: Hot-swappable framework support
- **Enhanced Visualization**: Professional publication-ready charts
- **Comprehensive Documentation**: Full technical and user documentation

---

## 3. Validation-First Development Strategy

### 🧪 Critical Gap Identified: Academic Validation
**Problem**: Current system produces numerical data (JSON/PNG) but lacks:
- Interpretive narratives explaining what scores mean
- Evidence extraction with supporting quotes
- Comparative context and insights
- Academic-grade reliability studies

### 📊 Validation Requirements (3-Phase Plan)
**See**: 
- `VALIDATION_FIRST_DEVELOPMENT_STRATEGY.md` for complete 270-line specification
- `VALIDATION_IMPLEMENTATION_ROADMAP.md` for specific implementation tasks

**Phase 1**: Multi-run consistency, inter-LLM correlation, framework validation
**Phase 2**: Evidence extraction, automated reports, human-readable explanations  
**Phase 3**: Conversational AI interface for domain-specific queries

### 🎯 Success Criteria for Academic Credibility
- Multi-run reliability: CV < 0.15 for 80% of well dimensions
- Inter-LLM consensus: r > 0.7 between primary LLM pairs
- Framework validity: Internal consistency α > 0.8
- Publication-quality statistical documentation

---

## 4. Architecture Summary

### Core Components
```
narrative_gravity_analysis/
├── 🚀 Core Application & Analysis
│   ├── launch_app.py                 # Main application launcher
│   ├── narrative_gravity_app.py      # Core Streamlit web interface
│   ├── narrative_gravity_elliptical.py # Core analysis & visualization engine
│   ├── create_generic_multi_run_dashboard.py # Universal multi-run dashboard system
│   ├── framework_manager.py          # Framework switching & management system
│   └── generate_prompt.py            # Legacy LLM prompt generator
│
├── 📁 Backend Infrastructure (src/)
│   ├── api/                          # FastAPI endpoints for jobs, tasks, corpora
│   ├── api_clients/                  # Clients for interacting with LLM APIs
│   ├── cli/                          # Command-line interface tools
│   ├── models/                       # Database models (SQLAlchemy)
│   ├── prompts/                      # Prompt templates and management
│   ├── tasks/                        # Celery tasks for background processing
│   └── utils/                        # Utility functions (validation, chunking)
│
├── 📊 Data & Configuration
│   ├── frameworks/                   # Framework definitions (Civic Virtue, etc.)
│   ├── config/                       # Symlinks to active framework
│   ├── corpus/                       # Text corpora (golden set, etc.)
│   ├── model_output/                 # Analysis results (JSON/PNG)
│   └── reference_texts/              # Sample texts for analysis
│
├── 📚 Documentation & Instructions
│   ├── docs/                         # User guides, architecture, examples
│   ├── docs/development/planning/    # Core strategic & development documents
│   ├── README.md                     # Main project documentation
│   └── PROJECT_STRUCTURE.md          # Detailed project structure overview
│
└── 🗃️ Testing & Archive
    ├── tests/                        # Unit, integration, and validation tests
    └── archive/                      # Historical development versions & outputs
```

### Technology Stack
```bash
# Core Dependencies (see requirements.txt for full list)
fastapi                # High-performance API framework
celery                 # Distributed task queue
redis                  # In-memory data store / message broker
sqlalchemy             # SQL toolkit and Object Relational Mapper (ORM)
alembic                # Lightweight database migration tool
streamlit              # Web interface for interactive apps
pandas                 # Data manipulation and analysis
plotly                 # Interactive visualizations
matplotlib             # Static visualization engine
numpy                  # Mathematical computations
```

### Modular Framework Architecture
The system uses **symlink-based modular architecture**:
- Multiple frameworks stored in `frameworks/` directory
- Active framework linked via `config/` symlinks
- Hot-swappable without code changes
- Currently supports 3 specialized frameworks

---

## 5. Core Source Code

### 5.1 Core Analysis Engine (`narrative_gravity_elliptical.py`)

**Mathematical heart of the system** (1,136+ lines) - provides the core visualization and analysis capabilities.

**KEY METHODS FOR API INTEGRATION:**
- `create_visualization(data: Dict, output_path: str = None) -> str`: Main visualization creation
- `calculate_narrative_position(well_scores: Dict[str, float]) -> Tuple[float, float]`: Core mathematics  
- `calculate_elliptical_metrics(narrative_x, narrative_y, well_scores)`: Statistical measures
- `normalize_analysis_data(data: Dict) -> Dict`: Data format standardization

**CRITICAL CLASS STRUCTURE:**

```python
class NarrativeGravityWellsElliptical:
    """
    Narrative Gravity Wells analyzer and visualizer.
    Implements mathematical framework for positioning narratives
    within coordinate system based on narrative gravity wells.
    """
    
    def __init__(self, config_dir: str = "config"):
        """Initialize with framework configuration"""
        
    def create_visualization(self, data: Dict, output_path: str = None) -> str:
        """Generate complete visualization for single analysis"""
        
    def create_comparative_visualization(self, analyses: List[Dict], output_path: str = None) -> str:
        """Generate comparative visualization for multiple analyses"""
        
    def calculate_narrative_position(self, well_scores: Dict[str, float]) -> Tuple[float, float]:
        """Calculate narrative position using gravity wells methodology"""
        
    def calculate_elliptical_metrics(self, narrative_x: float, narrative_y: float, 
                                   well_scores: Dict[str, float]) -> Dict[str, float]:
        """Calculate comprehensive metrics for narrative position"""
```

**DATA FORMATS:**

```python
# LLM Analysis Input Format
{
    "text_title": "Analysis Title",
    "model_name": "claude-4.0-sonnet", 
    "model_version": "20240229",
    "analysis_timestamp": "2025-06-04T20:34:29",
    "framework": "civic_virtue",
    "wells": {
        "Dignity": 0.8,      # Scores must be 0.0-1.0
        "Truth": 0.6,
        "Hope": 0.4,
        // ... all 10 wells
    }
}

# Analysis Output Format
{
    "center_of_mass": {"x": 0.12, "y": 0.34},
    "narrative_polarity_score": 0.67,
    "directional_purity_score": 0.84,
    "dominant_wells": ["Dignity", "Hope"],
    "ellipse_position": {"semi_major": 1.0, "semi_minor": 0.7}
}
```

**API Integration Points:**
- Input: JSON score files from LLM analysis
- Output: Visualization PNG files, metrics dictionaries
- Configuration: Framework-agnostic via config system
- Error handling: Comprehensive validation and fallback

**DATA FORMATS:**

```python
# LLM Analysis Input Format
{
    "text_title": "Analysis Title",
    "model_name": "claude-4.0-sonnet", 
    "model_version": "20240229",
    "analysis_timestamp": "2025-06-04T20:34:29",
    "framework": "civic_virtue",
    "wells": {
        "Dignity": 0.8,      # Scores must be 0.0-1.0
        "Truth": 0.6,
        "Hope": 0.4,
        // ... all 10 wells
    }
}

# Analysis Output Format
{
    "center_of_mass": {"x": 0.12, "y": 0.34},
    "narrative_polarity_score": 0.67,
    "directional_purity_score": 0.84,
    "dominant_wells": ["Dignity", "Hope"],
    "ellipse_position": {"semi_major": 1.0, "semi_minor": 0.7}
}
```

### 5.2 Streamlit Interface (`narrative_gravity_app.py`)

Comprehensive web interface - 1,372 lines providing:

**Core Functionality:**
- Framework switching and management
- Interactive analysis workflow
- Comparative analysis tools
- Prompt generation and download
- Real-time visualization updates

**Key Components:**
```python
# Main tabs
- "🎯 Quick Analysis": Single-file workflow
- "📝 Create Analysis": Multi-step analysis creation
- "🔍 Compare Analysis": Comparative analysis tools
- "⚙️ Framework Manager": Framework switching interface
- "📋 Generate Prompts": LLM prompt generation
```

**API Integration Potential:**
- File upload handling ready for automation
- Analysis pipeline easily adaptable to batch processing
- Framework switching can be programmatically controlled
- Error handling and validation already implemented

### 3.3 Framework Manager (`framework_manager.py`)

Framework switching system - 257 lines enabling:

**Core Methods:**
```python
class FrameworkManager:
    def list_frameworks(self):        # Discover available frameworks
    def get_active_framework(self):   # Identify current framework
    def switch_framework(self, name): # Change active framework
    def validate_framework(self, name): # Structural validation
```

**Framework Discovery Logic:**
- Automatic scanning of `frameworks/` directory
- Validation of required files (dipoles.json, framework.json)
- Version tracking and metadata extraction
- Symlink management for active configuration

### 3.4 Prompt Generator (`generate_prompt.py`)

LLM prompt generation system - 351 lines providing:

**Critical Features:**
```python
class PromptGenerator:
    def generate_interactive_prompt(self): # Conversational workflow
    def generate_batch_prompt(self):       # Batch processing
    def generate_simple_prompt(self):      # Single analysis
```

**Recent Critical Fixes:**
- **LLM Score Compliance**: Explicit 0.0-1.0 scale enforcement
- **Model Identification**: Guidance for accurate attribution
- **Framework Agnostic**: Removed political analysis assumptions

**Prompt Structure:**
1. Model identification verification
2. Critical scoring requirements (0.0-1.0 scale)
3. Framework-specific dipole definitions
4. Conceptual assessment methodology
5. JSON output format specification

---

## 6. Configuration System

### 6.1 Active Configuration (`config/`)

The `config/` directory contains symlinks to the active framework's configuration files. This allows for hot-swapping analysis frameworks without changing any code.

```bash
config/
├── dipoles.json -> ../frameworks/civic_virtue/dipoles.json
└── framework.json -> ../frameworks/civic_virtue/framework.json
```

### 6.2 Dipoles Configuration (`dipoles.json`)

This file defines the conceptual structure of a framework, including the names, descriptions, and language cues for each "dipole" (the opposing concepts like Dignity vs. Tribalism). It's used primarily for generating the LLM prompts.

```json
{
  "framework_name": "civic_virtue",
  "display_name": "Civic Virtue Framework", 
  "version": "v2025.06.04",
  "description": "The Civic Virtue Framework is a specialized implementation of the Narrative Gravity Map methodology, designed to evaluate the moral architecture of persuasive political discourse...",
  "dipoles": [
    {
      "name": "Identity",
      "description": "Moral worth and group membership dynamics",
      "positive": {
        "name": "Dignity",
        "description": "Affirms individual moral worth and universal rights, regardless of group identity...",
        "language_cues": ["equal dignity", "inherent worth", "regardless of background", "individual character", "universal rights", "human agency"]
      },
      "negative": {
        "name": "Tribalism", 
        "description": "Prioritizes group dominance, loyalty, or identity over individual agency...",
        "language_cues": ["real Americans", "our people", "they don't belong", "us vs them", "group loyalty", "identity politics"]
      }
    },
    // ... [4 additional dipoles: Integrity, Fairness, Aspiration, Stability]
  ]
}
```

### 6.3 Framework Configuration (`framework.json`)

This file defines the mathematical implementation of the framework, including the position and weight of each gravity well, the ellipse parameters, and metric definitions. It is used by the analysis and visualization engine.

```json
{
  "framework_name": "civic_virtue",
  "display_name": "Civic Virtue Framework",
  "version": "v2025.06.04", 
  "description": "Civic Virtue Framework - A specialized Narrative Gravity Map implementation...",
  "ellipse": {
    "description": "Coordinate system parameters",
    "semi_major_axis": 1.0,
    "semi_minor_axis": 0.7,
    "orientation": "vertical"
  },
  "weighting_philosophy": {
    "description": "Three-tier weighting system based on moral psychology research",
    "primary_tier": {
      "weight": 1.0,
      "description": "Identity forces - most powerful moral motivators",
      "wells": ["Dignity", "Tribalism"]
    },
    "secondary_tier": {
      "weight": 0.8,
      "description": "Universalizable principles - fundamental but secondary to identity", 
      "wells": ["Truth", "Justice", "Manipulation", "Resentment"]
    },
    "tertiary_tier": {
      "weight": 0.6,
      "description": "Cognitive moderators - abstract reasoning processes",
      "wells": ["Hope", "Pragmatism", "Fantasy", "Fear"]
    }
  },
  "wells": {
    "Dignity": {"angle": 90, "weight": 1.0, "type": "integrative", "tier": "primary"},
    "Truth": {"angle": 45, "weight": 0.8, "type": "integrative", "tier": "secondary"},
    "Hope": {"angle": 20, "weight": 0.6, "type": "integrative", "tier": "tertiary"},
    "Justice": {"angle": 135, "weight": 0.8, "type": "integrative", "tier": "secondary"},
    "Pragmatism": {"angle": 160, "weight": 0.6, "type": "integrative", "tier": "tertiary"},
    "Tribalism": {"angle": 270, "weight": -1.0, "type": "disintegrative", "tier": "primary"},
    "Fear": {"angle": 200, "weight": -0.6, "type": "disintegrative", "tier": "tertiary"},
    "Resentment": {"angle": 225, "weight": -0.8, "type": "disintegrative", "tier": "secondary"},
    "Manipulation": {"angle": 315, "weight": -0.8, "type": "disintegrative", "tier": "secondary"},
    "Fantasy": {"angle": 340, "weight": -0.6, "type": "disintegrative", "tier": "tertiary"}
  },
  "scaling_factor": 0.8,
  "metrics": {
    "com": {"name": "Center of Mass", "description": "Weighted center position considering signed weights"},
    "nps": {"name": "Narrative Polarity Score", "description": "Distance from center normalized by ellipse dimensions"},
    "dps": {"name": "Directional Purity Score", "description": "Consistency of integrative vs disintegrative pull"}
  }
}
```

---

## 7. Framework Definitions

### 7.1 Available Frameworks

The system currently supports three specialized, hot-swappable frameworks stored in the `frameworks/` directory:

1.  **Civic Virtue Framework** (`frameworks/civic_virtue/`) - **Primary**
    *   Our most advanced and validated framework for political discourse.
    *   Features 5 dipoles and 10 wells with a three-tier differential weighting system based on moral psychology research.

2.  **Political Spectrum Framework** (`frameworks/political_spectrum/`)
    *   A more traditional model for positioning narratives on a left-right political spectrum.
    *   Useful for comparative analysis against the Civic Virtue model.

3.  **Moral Rhetorical Posture Framework** (`frameworks/moral_rhetorical_posture/`)
    *   Assesses communication style and rhetorical strategy rather than ideological content.

### 7.2 Civic Virtue Framework Details

**Integrative Gravity Wells** (Upper hemisphere, positive weights):
- **Dignity** (90°, +1.0): Individual moral worth, universal rights
- **Truth** (45°, +0.8): Intellectual honesty, evidence-based reasoning
- **Hope** (20°, +0.6): Grounded optimism with realistic paths
- **Justice** (135°, +0.8): Impartial, rule-based fairness
- **Pragmatism** (160°, +0.6): Evidence-based, adaptable solutions

**Disintegrative Gravity Wells** (Lower hemisphere, negative weights):
- **Tribalism** (270°, -1.0): Group dominance over individual agency
- **Manipulation** (315°, -0.8): Information distortion and exploitation
- **Fantasy** (340°, -0.6): Denial of trade-offs and complexity
- **Resentment** (225°, -0.8): Grievance-centered moral scorekeeping
- **Fear** (200°, -0.6): Threat-focused reaction and control

### 7.3 Framework Creation Guidelines

A new framework can be added by creating a new subdirectory in `frameworks/` with the following required files:

```
frameworks/[framework_name]/
├── dipoles.json      # Conceptual definitions for LLM prompts
├── framework.json    # Mathematical implementation for analysis
└── README.md         # Documentation explaining the framework's theory
```
The system will automatically discover and validate any new frameworks that follow this structure.

---

## 8. Current Validation & Research Requirements

### 8.1 ✅ API Integration Complete (Epic 1-4)

**Multi-LLM Integration Achieved:**
✅ **HuggingFace API Integration**: Unified access to GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro  
✅ **Batch Processing**: Automated multi-run analysis with statistical aggregation  
✅ **Cross-Model Validation**: Systematic comparison and consensus analysis  
✅ **Statistical Enhancement**: Confidence intervals, variance quantification, uncertainty measures  
✅ **Workflow Automation**: No more manual copy/paste - full API automation  

**Infrastructure Complete:**
- Celery + Redis task queue for scalable processing
- PostgreSQL database for persistent storage
- FastAPI REST endpoints for job management
- Streamlit dashboard for real-time monitoring

### 8.2 🎯 Current Priority: Academic Validation Studies

**Critical Need**: Academic credibility through rigorous validation studies

**Phase 1 Requirements (Weeks 1-3): Core Reliability Validation**
```python
# Multi-run consistency study requirements
validation_study_requirements = {
    "corpus": "17 golden set texts",
    "frameworks": ["civic_virtue", "political_spectrum", "moral_foundations"],
    "llms": ["gpt-4o", "claude-3.5-sonnet", "gemini-1.5-pro"],
    "runs_per_combination": 5,
    "total_analyses": 765,  # 17 × 3 × 3 × 5
    "metrics": [
        "coefficient_of_variation",
        "confidence_intervals", 
        "inter_llm_correlation",
        "framework_internal_consistency"
    ]
}
```

**Phase 2 Requirements (Weeks 4-5): Interpretive Intelligence**
```python
# Evidence extraction and explanation system
interpretive_requirements = {
    "quote_extraction": "identify_passages_supporting_scores",
    "explanation_generation": "human_readable_reasoning_chains",
    "comparative_analysis": "corpus_relative_positioning", 
    "report_templates": [
        "executive_summary",
        "technical_appendix",
        "evidence_based_insights"
    ]
}
```

**Phase 3 Requirements (Weeks 6-8): Conversational Interface**
```python
# Domain-specific AI assistant requirements
conversational_requirements = {
    "query_types": [
        "score_explanations",
        "comparative_analysis", 
        "variance_investigation",
        "evidence_retrieval"
    ],
    "architecture": "hybrid_local_remote_llm",
    "local_model": "llama_3_1_8b",  # For basic queries
    "remote_models": "gpt4_claude_gemini",  # For complex analysis
    "hallucination_control": "grounded_responses_only"
}
```

### 8.3 Academic Publication Requirements

**Statistical Rigor Standards:**
- Multi-run reliability: CV < 0.15 for 80% of well dimensions
- Inter-LLM consensus: r > 0.7 between primary LLM pairs  
- Framework validity: Internal consistency α > 0.8
- Replication package: Complete methodology documentation

**Evidence Standards:**
- Quote relevance: 90% of extracted quotes directly support scores
- Explanation accuracy: 85%+ human evaluator approval
- Comparative insights: Meaningful cross-text pattern identification
- Report quality: Non-technical stakeholders can act on insights

### 8.4 Technology Stack for Validation Studies

**Statistical Analysis Tools:**
```python
# Required statistical libraries and methods
statistical_stack = {
    "correlation_analysis": ["scipy.stats.pearsonr", "spearmanr", "kendalltau"],
    "reliability_measures": ["cronbach_alpha", "test_retest_reliability"],
    "confidence_intervals": ["bootstrap_methods", "parametric_ci"],
    "variance_analysis": ["anova", "coefficient_of_variation"],
    "consensus_metrics": ["intraclass_correlation", "fleiss_kappa"]
}
```

**Validation Pipeline Architecture:**
- **Automated Study Runner**: Orchestrates large-scale validation experiments
- **Statistical Analyzer**: Computes reliability and consensus metrics  
- **Report Generator**: Creates publication-ready analysis summaries
- **Quality Assurance**: Validates results against academic standards
```json
{
  "api_providers": {
    "huggingface": {
      "base_url": "https://api-inference.huggingface.co/models/",
      "models": ["meta-llama/Llama-2-70b-chat-hf", "mistralai/Mixtral-8x7B-Instruct-v0.1"],
      "rate_limit": {"requests_per_minute": 60},
      "timeout": 30
    },
    "openai": {
      "models": ["gpt-4", "gpt-3.5-turbo"],
      "rate_limit": {"requests_per_minute": 20}
    },
    "anthropic": {
      "models": ["claude-3-sonnet-20240229", "claude-3-haiku-20240307"], 
      "rate_limit": {"requests_per_minute": 15}
    }
  },
  "analysis_settings": {
    "default_runs_per_model": 5,
    "confidence_level": 0.95,
    "statistical_tests": ["t-test", "mann-whitney"],
    "outlier_detection": {"method": "iqr", "threshold": 1.5}
  }
}
```

---

## 9. Technical Specifications

### 9.1 Current System Specifications

**Core Mathematics:**
- Elliptical coordinate transformation with configurable aspect ratios
- Differential weighting system supporting three-tier hierarchies
- Statistical metrics: Center of Mass (COM), Narrative Polarity Score (NPS), Directional Purity Score (DPS)
- Signed weight calculation for directional consistency measurement

**Data Formats:**
```python
# LLM Analysis Input Format
{
    "text_title": "Analysis Title",
    "model_name": "claude-4.0-sonnet", 
    "model_version": "20240229",
    "analysis_timestamp": "2025-06-04T20:34:29",
    "framework": "civic_virtue",
    "wells": {
        "Dignity": 0.8,      # Scores must be 0.0-1.0
        "Truth": 0.6,
        "Hope": 0.4,
        // ... all 10 wells
    }
}

# Analysis Output Format
{
    "center_of_mass": {"x": 0.12, "y": 0.34},
    "narrative_polarity_score": 0.67,
    "directional_purity_score": 0.84,
    "dominant_wells": ["Dignity", "Hope"],
    "ellipse_position": {"semi_major": 1.0, "semi_minor": 0.7}
}
```

**Visualization Specifications:**
- Publication-ready matplotlib/seaborn output
- Configurable color schemes and styling
- Support for single and comparative analysis plots
- Automatic scaling and aspect ratio management
- PNG output with configurable DPI and dimensions

### 9.2 API Response Processing Requirements

**LLM Response Validation:**
```python
class ResponseValidator:
    def validate_scores(self, scores: Dict[str, float]) -> ValidationResult:
        """
        Validate LLM scores meet requirements:
        - All wells present in active framework
        - Scores in 0.0-1.0 range
        - No missing or null values
        - Proper numeric formatting
        """
        
    def validate_metadata(self, metadata: Dict) -> ValidationResult:
        """
        Validate analysis metadata:
        - Model identification accuracy
        - Timestamp formatting
        - Framework version consistency
        """
```

**Error Handling Requirements:**
- Graceful handling of API timeouts and rate limits
- Automatic retry with exponential backoff
- Invalid response detection and resubmission
- Partial result preservation for batch interruptions
- Comprehensive logging for debugging and auditing

### 9.3 Performance Specifications

**Target Performance Metrics:**
- Single analysis: < 30 seconds end-to-end
- Batch analysis (5 runs): < 3 minutes per model
- Cross-model validation (3 models, 5 runs each): < 10 minutes
- Statistical processing and visualization: < 30 seconds
- Memory usage: < 500MB for typical batch operations

**Scalability Requirements:**
- Support for 100+ text corpus batch processing
- Concurrent API requests within rate limits
- Result caching to avoid duplicate analyses
- Progressive result storage for large batches
- Resume capability for interrupted long-running analyses

---

## 10. Development Context

### 10.1 Recent Critical Issues Resolved

**LLM Scoring Compliance Crisis** (v2025.06.04.2):
- **Issue**: LLMs using 1-10 integer scales instead of required 0.0-1.0 decimal scale
- **Impact**: Visualization failures, mathematical errors, invalid analysis results
- **Resolution**: Enhanced prompt generator with explicit scale warnings and format requirements
- **Status**: ✅ Fixed in production

**Model Identification Accuracy** (v2025.06.04.2):
- **Issue**: AI platforms (Perplexity, Poe) identifying as platform rather than underlying model
- **Impact**: Academic accuracy concerns, attribution problems
- **Resolution**: Added model verification workflow to prompt generator
- **Status**: ✅ Guidance implemented

**Framework Scope Limitation** (v2025.06.04.1):
- **Issue**: Political analysis assumptions embedded in prompt generator
- **Impact**: Limited applicability to non-political persuasive narratives
- **Resolution**: Framework-agnostic design with configurable prompts
- **Status**: ✅ Generalized for any persuasive narrative type

### 10.2 Architecture Evolution

**Version 1.0 → 2.0 Migration:**
- Single framework → Multi-framework modular architecture
- Hardcoded configuration → JSON-driven framework definitions
- Basic CLI → Comprehensive Streamlit interface
- Manual workflows → Semi-automated pipeline with testing

**Version 2.0 → API Integration (Next Phase):**
- Manual LLM interaction → Automated API workflows
- Single-run analysis → Multi-run statistical validation
- Single-model analysis → Cross-model comparison
- Individual text processing → Batch corpus processing

### 10.3 Quality Assurance Status

**Code Quality:**
- ✅ Comprehensive test suite (31 tests passing)
- ✅ Clean modular architecture with separation of concerns
- ✅ Consistent error handling and validation
- ✅ Documentation coverage for all major components
- ✅ Version control with semantic versioning

**Production Readiness:**
- ✅ Published academic paper with theoretical foundation
- ✅ Paper replication instructions available
- ✅ Clean project structure with archived development files
- ✅ Stable CLI and web interfaces
- ✅ Framework validation and switching system

**Research Validation:**
- ✅ Mathematical framework validated through academic review
- ✅ Multiple specialized framework implementations
- ✅ Real-world testing with political discourse analysis
- ✅ Comparative analysis capabilities demonstrated
- ✅ Visualization engine producing publication-ready outputs

### 10.4 Strategic Roadmap Alignment

The API integration development represents the **critical next milestone** in the project roadmap:

**Current Position**: Production-ready manual analysis tool
**Target Position**: Automated research platform with statistical validation
**Key Success Metrics**: 
- Variance quantification across multiple runs
- Cross-model validation for reliability assessment
- Batch processing capability for corpus-scale analysis
- Statistical confidence intervals for academic rigor

**Immediate Priorities for API Integration:**
1. **Hugging Face API client implementation** (highest ROI)
2. **Multi-run statistical analysis framework**
3. **Enhanced visualization with uncertainty quantification**
4. **Cross-model validation infrastructure**
5. **Batch processing optimization and result caching**

---

## 📊 **Summary for Product Manager Mode**

**Current Position (June 2025)**:
- ✅ **Infrastructure Complete**: Epic 1-4 finished with 99.5% test success rate
- ✅ **API Foundation**: Ready for LLM automation with bug fixes completed
- ✅ **Framework System**: 3 hot-swappable frameworks with modular architecture
- 🎯 **Next Phase**: Validation-first development for academic credibility

**Immediate Priorities**:
1. **Phase 1 Validation**: Multi-run consistency studies (765 analyses across golden set)
2. **Statistical Rigor**: Inter-LLM correlation analysis and framework validation  
3. **Evidence Systems**: Quote extraction and human-readable explanations
4. **Academic Publication**: Validation studies ready for peer review

**Key Capabilities**:
- Mathematical framework with elliptical coordinate system
- Multi-LLM integration (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro)
- Framework-agnostic design supporting any persuasive narrative type
- Comprehensive testing infrastructure and error handling
- Publication-ready visualization engine

This comprehensive documentation provides complete technical context for systematic development planning that will transform the Narrative Gravity Maps framework from a manual research tool into a scalable, statistically rigorous analysis platform suitable for large-scale academic and research applications.

---

## 5. Key Code Components

This section highlights the most critical Python modules in the system that drive the analysis, visualization, and backend processing.

### 5.1 Analysis & Visualization
- **`narrative_gravity_elliptical.py`**: The mathematical heart of the system. This module calculates narrative positions based on framework scores and generates the core elliptical visualizations. It's the primary engine for turning raw scores into graphical insights.
- **`create_generic_multi_run_dashboard.py`**: A key component for our validation studies. This script consumes multi-run analysis results, computes statistics like variance and confidence intervals, and generates the comprehensive multi-part dashboards that include elliptical maps, bar charts, and LLM-generated summaries. It is framework-agnostic and uses filename parsing for metadata extraction.

### 5.2 Application & Interface
- **`narrative_gravity_app.py`**: The main Streamlit web application. It provides the user interface for uploading texts, managing frameworks, launching analyses, and viewing results. It orchestrates the user-facing workflow.
- **`framework_manager.py`**: A utility that handles the loading, validation, and switching of analysis frameworks (e.g., Civic Virtue, Political Spectrum). It allows the system to be modular and extensible.

### 5.3 Backend Processing (Illustrative from `src/`)
- **`src/tasks/processing.py`**: A core Celery task for running analysis jobs in the background. It takes a chunk of text and an analysis configuration, interacts with the LLM client, and stores the result. This enables our scalable, asynchronous architecture.
- **`src/api_clients/huggingface_client.py`** (Illustrative): A client responsible for wrapping the Hugging Face API. It handles authentication, request formatting, and retry logic, providing a stable interface for the task processor to use.
- **`src/models/job.py`** (Illustrative): The SQLAlchemy data model for a 'Job'. It defines the database schema for tracking the state and parameters of an analysis job, including which texts, frameworks, and models are used.

---

*End of Comprehensive Documentation*

**File Statistics:**
- **Total Lines**: 7,500+ across all components
- **Core Code**: 4,084 lines Python
- **Documentation**: 4,508 lines across 15+ files  
- **Test Suite**: 906 lines, 31 tests
- **Configuration**: 185 lines JSON across frameworks
- **Status**: Production-ready, API integration ready 

---

## 9. Testing Infrastructure

Our testing philosophy has evolved from basic smoke tests to a more robust, multi-layered approach that ensures the reliability of the core application, the backend infrastructure, and the analysis results themselves.

### 9.1 Test Suite Overview
The `tests/` directory contains a combination of unit tests, integration tests, and (forthcoming) validation study tests. The suite is designed to verify both code correctness and the scientific validity of the analysis.

-   **Unit Tests (`tests/unit/`)**: Focused on isolating and testing individual functions and classes. For example, testing the mathematical calculations in `narrative_gravity_elliptical.py` or a specific utility function in `src/utils/`.
-   **Integration Tests (`tests/integration/`)**: Designed to test the interaction between different parts of the system. For example, verifying that a `Celery` task correctly calls the `API Client` and stores data using the `Database Models`.
-   **Validation Tests (`tests/validation/`)**: *[In Development]* This is a new, critical category of tests designed to execute the validation studies outlined in Phase 1 of our strategy. These tests will run analyses on the golden set corpus and perform statistical checks on the results to measure reliability and consensus.

### 9.2 Backend Testing (`src/`)
The backend components in the `src/` directory are tested with a focus on their specific roles in the application stack:
-   **API Tests**: Verifying FastAPI endpoint logic, including request/response formats, authentication, and error handling.
-   **Task Tests**: Testing Celery task execution, ensuring they can be queued, run, and handle success/failure states correctly.
-   **Model Tests**: Confirming that the SQLAlchemy database models correctly map to the database schema and that relationships are correctly defined.
-   **Client Tests**: Mocking external APIs (like Hugging Face) to test the retry logic, error handling, and data parsing of our API clients.

### 9.3 Forthcoming: Validation Study Automation
The next major development in our testing infrastructure is the creation of an automated test harness for the **Golden Set Validation Framework**.

---

## 10. Documentation

Our documentation is organized into three distinct categories to serve different audiences: strategic stakeholders, developers, and end-users.

### 10.1 Strategic & Planning Documentation (`docs/development/planning/`)
This is the canonical source for understanding the project's direction, priorities, and high-level plans. It's essential reading for product management and strategic decision-making.
-   **`VALIDATION_FIRST_DEVELOPMENT_STRATEGY.md`**: The most important document right now. Outlines our current 3-phase plan for achieving academic credibility.
-   **`COMPREHENSIVE_PROJECT_DOCUMENTATION.md`**: This document. A detailed technical and strategic reference.
-   **`User Personas - Narrative Gravity Model.md`**: Describes the target users who drive our development priorities.
-   **Milestone & Epic Docs**: Documents that track the completion status and high-level goals of major work packages.

### 10.2 Technical & Developer Documentation (`docs/` and code)
This documentation is aimed at developers working on the system.
-   **`docs/architecture/`**: Contains diagrams (like the ERD) and detailed explanations of the system's architecture.
-   **`README.md`**: The primary entry point for a new developer, explaining how to set up, configure, and run the application.
-   **Code Docstrings**: We aim for comprehensive docstrings within the code itself to explain the purpose and function of key classes and methods.
-   **`PROJECT_STRUCTURE.md`**: A detailed map of the files and directories in the repository.

### 10.3 User & Academic Documentation (`docs/` and outputs)
This documentation is for end-users of the tool, including researchers and academic collaborators.
-   **`docs/user-guides/`**: Contains guides for using the application, understanding the frameworks, and interpreting the results.
-   **`docs/examples/`**: Showcases example analyses and dashboards.
-   **Replication Materials**: For any publication, we will produce a complete replication package with data, scripts, and instructions to ensure full academic transparency and reproducibility.
-   **Generated Reports**: The automated reports from the interpretive intelligence phase will themselves be a form of user documentation, explaining the results of a specific analysis.