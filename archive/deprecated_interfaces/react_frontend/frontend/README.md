# Narrative Gravity Research Workbench

A React-based research workbench for Workstream 1: Prompt Engineering & Scoring Framework Refinement of the Narrative Gravity Wells project.

## Overview

This application implements a unified experiment design interface that treats prompt engineering and scoring methodology as integrated experimental hypotheses, enabling systematic iteration while maintaining research reproducibility.

## Key Features

### 🧪 Unified Experiment Design Interface
- Create experimental conditions that bundle prompt templates, framework configurations, and scoring algorithms as single testable hypotheses
- Generate unique experiment identifiers with complete metadata tracking
- Support for hypothesis-driven research with clear experimental lineage

### ✏️ Dual-Layer Prompt Editor
- Split-pane interface separating general-purpose prompt templates from framework-specific dipole definitions
- Live preview of combined prompts sent to LLMs
- Version control with semantic versioning and hash-based change tracking
- Template management with creation, editing, and deletion capabilities

### 📊 Analysis Results & Provenance
- Complete experimental provenance tracking (prompt hash, framework version, scoring algorithm, LLM model, timestamp)
- Interactive visualization of gravity wells scores with bar charts
- Pin results for comparative analysis
- Detailed metrics display (Narrative Elevation, Polarity, Coherence, Directional Purity)

### ⚖️ Systematic Comparative Analysis
- Side-by-side comparison of up to 4 experimental conditions
- Statistical analysis including hierarchy sharpness metrics and correlation analysis
- Coefficient of variation and dominance ratio calculations
- Saved comparison sets for reproducible analysis

## Technical Architecture

### State Management
- **Zustand** for complex experimental state management
- Persistent storage with automatic versioning
- Optimistic updates for rapid iteration

### Backend Integration
- FastAPI integration with existing `/api/corpora`, `/api/jobs`, `/api/results` endpoints
- Mock mode for development when API is unavailable
- Extensible API client with type safety

### Component Structure
```
src/
├── components/
│   ├── ExperimentDesigner.tsx    # Unified experiment creation
│   ├── PromptEditor.tsx          # Dual-layer prompt editing
│   ├── AnalysisResults.tsx       # Results with provenance
│   └── ComparisonDashboard.tsx   # Statistical comparison
├── store/
│   └── experimentStore.ts        # Zustand state management
├── services/
│   └── apiClient.ts              # Backend integration
└── App.tsx                       # Main application shell
```

### Data Models
- **Experiments**: Unified experimental conditions with hypothesis tracking
- **Prompt Templates**: Versioned prompt content with hash-based change detection
- **Framework Configs**: Modular framework definitions with dipole specifications
- **Scoring Algorithms**: Configurable scoring approaches (linear, winner-take-most, etc.)
- **Analysis Results**: Complete provenance with statistical metrics

## Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn
- FastAPI backend running on port 8000 (optional - mock mode available)

### Installation
```bash
cd frontend
npm install
```

### Development
```bash
npm start
```

The application will open at `http://localhost:3000` with hot reloading enabled.

### Environment Variables
Create a `.env` file in the frontend directory:
```
REACT_APP_API_BASE_URL=http://localhost:8000
```

## Usage Workflows

### 1. Experiment Creation Workflow
1. Navigate to **Experiment Designer** tab
2. Fill in experiment name and research hypothesis
3. Select prompt template, framework configuration, and scoring algorithm
4. Click "Create Experiment" to generate unique experimental condition
5. Use the analysis interface to test with narrative texts

### 2. Rapid Iteration Cycle
1. Go to **Prompt Editor** tab
2. Edit prompt content in left pane
3. Modify framework wells in right pane
4. Preview combined prompt
5. Return to Experiment Designer to test changes
6. Pin results for comparison

### 3. Comparative Analysis
1. Pin multiple analysis results from **Analysis Results** tab
2. Navigate to **Comparison Dashboard**
3. Select 2-4 results for comparison
4. Choose visualization mode (side-by-side, overlay, statistical)
5. Save comparison sets for future reference

## Research Features

### Experimental Rigor
- **Complete Provenance**: Every analysis includes prompt hash, framework version, scoring algorithm version, LLM model, and timestamp
- **Version Control**: Semantic versioning for all components with rollback capability
- **Reproducibility**: Export functionality for complete replication packages

### Statistical Analysis
- **Hierarchy Sharpness**: Coefficient of variation and dominance ratio calculations
- **Correlation Analysis**: Pearson correlation coefficients between experimental conditions
- **Significance Testing**: Statistical comparison tools for score distributions

### Validation Support
- **Framework Fit Detection**: Identify when narratives don't map well to current dipoles
- **Quality Metrics**: Automated validation of experimental completeness
- **Research Documentation**: Built-in hypothesis tracking and insight capture

## Integration with Backend

### Current Endpoints
- `GET /api/health` - Health check
- `GET /api/corpora` - List available corpora
- `POST /api/jobs` - Create analysis jobs
- `GET /api/jobs/{id}` - Get job status

### Planned Endpoints (Phase 2)
- `POST /api/analyze/single` - Single text analysis for research workbench
- `POST /api/analyze/batch` - Batch analysis for experimental comparison
- `GET /api/frameworks` - Available framework configurations
- `GET /api/models` - Available LLM models

## Development Principles

### Validation-First Development
- Built to support academic validation requirements
- Statistical rigor for human-machine alignment studies
- Transparent methodology documentation

### Research Laboratory Approach
- Treats each prompt + framework + scoring combination as testable hypothesis
- Maintains experimental lineage and prevents chaos of scattered files
- Enables systematic testing rather than ad-hoc iteration

### Epistemic Humility
- Clear documentation of limitations and assumptions
- Transparent about mock vs. real data
- Designed for "good enough" validation rather than perfect alignment

## Contributing

This workbench is part of the Narrative Gravity Wells project's validation-first development strategy. When contributing:

1. Maintain complete experimental provenance
2. Follow semantic versioning for all changes
3. Document assumptions and limitations
4. Test with both mock and real backend data
5. Ensure statistical analysis tools remain rigorous

## License

Part of the Narrative Gravity Wells project. See main project LICENSE for details.

## Validation Status

**Current Phase**: Phase 1 - Unified Experiment Design Interface
**Next Phase**: Phase 2 - Backend Integration and Real-time Analysis
**Target**: Publication-ready academic validation package

Built with validation-first development principles for systematic prompt engineering and scoring framework refinement.
