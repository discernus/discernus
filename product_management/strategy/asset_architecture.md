<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Enhanced Technical Workflow: Asset Management and Processing Pipeline

## **Input Asset Definitions and Sources**

### **Primary Input Assets**

**1. Narrative Texts**

- **Definition**: Political speeches, op-eds, articles, policy documents, campaign materials requiring moral architecture analysis
- **Sources**: Manual upload (JSONL format), corpus ingestion pipeline, reference text collections
- **Format**: JSON records with metadata (author, date, document type, source URL)
- **Storage**: PostgreSQL `documents` and `chunks` tables with full provenance tracking
- **Schema Compliance**: Universal core schema with framework-specific extensions

**2. Framework Definitions**

- **Definition**: Mathematical and conceptual specifications for analytical frameworks (Civic Virtue, Political Spectrum, etc.)
- **Sources**: Manual development sessions using structured LLM interaction, academic literature adaptation
- **Components**:
    - `dipoles.json`: Conceptual definitions and language cues for LLM prompts
    - `framework.json`: Mathematical implementation with well positioning and weights
- **Storage**: Database `framework_versions` table with complete version history
- **Versioning**: Semantic versioning with parent-child relationships and change documentation

**3. Prompt Templates**

- **Definition**: Structured instructions for LLM analysis including scoring methodology and output format requirements
- **Sources**: Systematic development through conversational refinement with performance testing
- **Types**: Framework-specific prompts, universal templates, experimental variations
- **Storage**: Database `prompt_templates` table with version control and compatibility tracking
- **Validation**: Schema compliance checking and LLM response format verification

**4. Weighting Methodologies**

- **Definition**: Mathematical algorithms for transforming raw well scores into narrative positioning
- **Sources**: Academic research on moral psychology, empirical testing against expected outcomes
- **Algorithms**: Linear averaging, winner-take-most, exponential decay, hierarchical weighting
- **Storage**: Database `weighting_methodologies` table with mathematical formulas and implementation notes
- **Testing**: Validation against synthetic narratives with known expected positions


### **Development Session Assets**

**5. Component Development Sessions**

- **Definition**: Structured records of manual development iterations with hypothesis tracking
- **Sources**: Researchers using standardized seed prompts for component optimization
- **Content**: Objectives, hypotheses, performance metrics, version evolution
- **Storage**: Database `development_sessions` table linking to resulting component versions
- **Documentation**: Complete audit trail for academic reproducibility


## **Output Asset Definitions and Storage**

### **Analysis Results**

**1. Structured Analysis Data**

- **Definition**: Complete LLM analysis results with scores, metadata, and provenance
- **Format**: JSON with standardized schema including model information and timestamps
- **Content**: Well scores (0.0-1.0), narrative positioning, statistical metrics, analysis metadata
- **Storage**: PostgreSQL `experiments` and `runs` tables with foreign key relationships
- **Accessibility**: REST API endpoints for programmatic access and academic tool export

**2. Visualization Assets**

- **Definition**: Publication-ready elliptical positioning charts with narrative placement and metrics
- **Format**: High-resolution PNG files with configurable styling and academic formatting
- **Content**: Ellipse boundary, well positions, narrative center, statistical overlays, summary metrics
- **Storage**: File system organized by experiment ID with database metadata references
- **Generation**: Automated through analysis pipeline with customizable parameters


### **Statistical Analysis Outputs**

**3. Academic Export Packages**

- **Definition**: Data formatted for standard academic statistical tools
- **Formats**:
    - CSV files for universal compatibility
    - Stata (.dta) files for publication-grade statistical analysis
    - R data frames (.feather) for advanced visualization and modeling
    - JSON for programmatic analysis and replication
- **Content**: Experimental data with complete variable codebooks and methodology documentation
- **Storage**: Structured export directories with automated generation timestamps
- **Integration**: Direct pipeline to Jupyter notebooks, R scripts, and Stata analysis workflows

**4. Replication Packages**

- **Definition**: Complete materials enabling independent research reproduction
- **Components**: Data files, analysis scripts, methodology documentation, component definitions
- **Standards**: Academic publication requirements with proper attribution and version control
- **Storage**: Versioned packages in file system with database tracking
- **Documentation**: Step-by-step replication instructions and software requirements


### **Research Documentation**

**5. Statistical Reports**

- **Definition**: Publication-ready statistical analysis with academic formatting
- **Content**: Reliability metrics, inter-LLM correlations, framework validation statistics
- **Formats**: Academic paper sections, executive summaries, technical appendices
- **Generation**: Automated through Cursor-generated Jupyter notebooks and R scripts
- **Storage**: Documentation directories with experiment linkage and version control


## **Enhanced Asset Flow Diagram**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ASSET CREATION & INGESTION PIPELINE                   │
└─────────────────────────────────────────────────────────────────────────────────┘

INPUT ASSET SOURCES
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Text Sources  │    │  Manual LLM     │    │  Academic       │    │  Research       │
│   • Speeches    │    │  Development    │    │  Literature     │    │  Iteration      │
│   • Documents   │    │  • Claude/GPT   │    │  • Frameworks   │    │  • Hypotheses   │
│   • Articles    │    │  • Structured   │    │  • Methods      │    │  • Testing      │
│   • Campaigns   │    │    Sessions     │    │  • Theory       │    │  • Refinement   │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         ▼                       ▼                       ▼                       ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           ASSET PROCESSING LAYER                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   Text          │  │   Component     │  │   Framework     │  │  Development │  │
│  │   Ingestion     │  │   Versioning    │  │   Definition    │  │  Session     │  │
│  │   • JSONL       │  │   • Semantic    │  │   • Dipoles     │  │  Management  │  │
│  │   • Validation  │  │   • Git-style   │  │   • Mathematics │  │  • Tracking  │  │
│  │   • Chunking    │  │   • Provenance  │  │   • Validation  │  │  • Metrics   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────┘
         │                       │                       │                       │
         ▼                       ▼                       ▼                       ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                            DATABASE STORAGE LAYER                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   Documents     │  │   Component     │  │   Framework     │  │  Development │  │
│  │   & Chunks      │  │   Versions      │  │   Definitions   │  │  Sessions    │  │
│  │   • Metadata    │  │   • Templates   │  │   • Wells       │  │  • Hypotheses│  │
│  │   • Provenance  │  │   • Weights     │  │   • Positioning │  │  • Results   │  │
│  │   • Schema      │  │   • History     │  │   • Metrics     │  │  • Evolution │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           ANALYSIS ORCHESTRATION LAYER                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   CLI Analysis  │  │   Component     │  │   Multi-LLM     │  │  Statistical │  │
│  │   Coordination  │  │   Assembly      │  │   Processing    │  │  Validation  │  │
│  │   • Batch Jobs  │  │   • Version     │  │   • GPT-4o      │  │  • CV/ICC    │  │
│  │   • Multi-Run   │  │     Selection   │  │   • Claude 3.5  │  │  • Consensus │  │
│  │   • Parameters  │  │   • Validation  │  │   • Gemini 1.5  │  │  • CI        │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                           OUTPUT GENERATION PIPELINE                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐  │
│  │   Analysis      │  │   Visualization │  │   Statistical   │  │  Research     │  │
│  │   Results       │  │   Generation    │  │   Analysis      │  │  Documentation│  │
│  │   • JSON Data   │  │   • PNG Charts  │  │   • Academic    │  │  • Methods    │  │
│  │   • Metadata    │  │   • Metrics     │  │     Exports     │  │  • Replication│  │
│  │   • Provenance  │  │   • Overlays    │  │   • Reports     │  │  • Packages   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └───────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────┘
         │                       │                       │                       │
         ▼                       ▼                       ▼                       ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           OUTPUT STORAGE & ACCESS                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   Database      │  │   File System   │  │   Academic      │  │  Publication │  │
│  │   • Experiments │  │   • Visualize   │  │   Tool Exports  │  │  Materials   │  │
│  │   • Runs        │  │   • Archives    │  │   • Jupyter     │  │  • Papers    │  │
│  │   • Statistics  │  │   • Organized   │  │   • R/Stata     │  │  • Reports   │  │
│  │   • API Access  │  │     by Exp ID   │  │   • CSV/JSON    │  │  • Packages  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────┘
         │                       │                       │                       │
         ▼                       ▼                       ▼                       ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                              END USER ACCESS                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  │
│  │   Researchers   │  │   Academic      │  │   Collaborators │  │  Publication │  │
│  │   • Query API   │  │   • Statistical │  │   • Replication │  │  • Peer      │  │
│  │   • Download    │  │     Analysis    │  │   • Extension   │  │    Review    │  │
│  │   • Extend      │  │   • Publication │  │   • Validation  │  │  • Citation  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────┘
```


## **Asset Lifecycle Management**

### **Version Control Strategy**

- **Semantic Versioning**: All components follow semantic versioning (v1.0.0) with automated increment suggestions
- **Dependency Tracking**: Component compatibility matrices prevent incompatible combinations
- **Change Documentation**: Every version includes human-readable change descriptions and performance impact metrics
- **Rollback Capability**: Complete version history enables rollback to any previous configuration


### **Quality Assurance Pipeline**

- **Automated Validation**: All input assets undergo schema validation and compatibility checking
- **Performance Testing**: Component combinations tested against synthetic narratives with known expected outcomes
- **Statistical Monitoring**: Continuous monitoring of analysis reliability and consistency metrics
- **Academic Standards**: All outputs verified against publication requirements and reproducibility standards


### **Storage Architecture**

- **Database-Centric**: Primary storage in PostgreSQL with complete relational integrity
- **File System Organization**: Hierarchical organization by experiment ID with database metadata links
- **Export Automation**: Automated generation of academic format exports with proper documentation
- **Backup Strategy**: Complete versioning enables reconstruction of any analysis state

This enhanced asset management system ensures complete traceability from input sources through analysis processing to publication-ready outputs, supporting the validation-first development strategy while maintaining academic rigor and reproducibility standards essential for peer review and research collaboration.

<div style="text-align: center">⁂</div>

[^1]: Narrative-Gravity-Model-Epic-1-Corpus-Job-Management-Backend.md

[^2]: Milestone-1-Epics-Narrative-Gravity-Model.md

[^3]: moral_gravity_elliptical.txt

[^4]: if-you-were-to-develop-a-compl-5KHQ_w5ARS6NumH6P0fHvA.md

[^5]: COMPREHENSIVE_PROJECT_DOCUMENTATION.md

[^6]: CHANGELOG.md

[^7]: i-ve-updated-the-files-in-this-3SOhPLUeRHirmfQDLsNCOw.md

[^8]: in-order-to-make-progress-on-w-yJLy9NxIQsaXVbsGvKPXHg.md

[^9]: database_first_architecture_todos.md

[^10]: Moral-Gravity-Wells-A-Quantitative-Framework-for-Discerning-the-Moral-Forces-Driving-the-Formatio.md

[^11]: README.md

[^12]: Project-Milestones-Narrative-Gravity-Model.md

[^13]: FRAMEWORK_ARCHITECTURE.md

[^14]: Security-Guidelines-for-Cursor.md

[^15]: Deliverables-for-Cursor-ER-Diagram-Alembic-Migrations-and-Versioned-JSON-Schemas.md

