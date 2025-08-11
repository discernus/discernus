# Statistical Preparation Offramp
*Strategic Enhancement to Discernus Orchestration*

---

## Executive Summary

**Proposal**: Add a "Statistical Preparation" stage between Analysis and Synthesis that produces researcher-ready datasets for external statistical analysis, creating a clean offramp for users who trust Discernus for text processing but prefer their own analytical tools.

**Market Position**: "Discernus handles large-scale text analysis; researchers handle statistical interpretation and conclusions."

**Implementation**: New CLI flag `--statistical-prep` that stops after producing analysis-ready CSV datasets with complete provenance.

---

## Strategic Rationale

### The Trust Boundary Problem

Current Discernus offers an all-or-nothing proposition: either accept our complete analysis pipeline (including statistical analysis and interpretation) or don't use the system at all. This creates a trust barrier for researchers who:

- **Trust us for text processing**: "I don't want to manually score 1000 documents"
- **Don't trust us for statistics**: "I'll choose my own statistical methods"
- **Don't trust us for interpretation**: "I'll draw my own research conclusions"

### Target User Profile

**Primary**: Academic researchers conducting text analysis studies who:
- Have expertise in statistical analysis using R, Python, STATA, or SPSS
- Need large-scale text processing capabilities beyond manual coding
- Require methodological control over statistical analysis and interpretation
- Must satisfy peer review standards for statistical rigor
- Want to collaborate with colleagues using different analytical approaches

**Secondary**: Research teams where roles are divided:
- **Data preparation specialist**: Uses Discernus for text processing
- **Statistical analyst**: Uses domain-specific tools for analysis
- **Domain expert**: Provides theoretical interpretation

### Competitive Advantage

This positions Discernus as:
- **Best-in-class text processor**: Excellence in LLM-powered dimensional scoring
- **Researcher-friendly**: Respects academic expertise and methodological preferences  
- **Collaboration enabler**: Multiple researchers can analyze same processed dataset
- **Quality focused**: Concentrate resources on text analysis excellence, not statistical consulting

---

## Current Architecture Gap

### Existing Orchestration Stages
```
Pre-Flight → Analysis → Synthesis → Finalization
Validation     Stage     Stage       Stage
```

### Proposed Enhancement
```
Pre-Flight → Analysis → Statistical → Synthesis → Finalization
Validation     Stage    Preparation     Stage       Stage
                          ↓ OFFRAMP
                     Researcher-Ready
                        Dataset
```

### The Missing Link

Currently, researchers must choose between:
1. **Analysis only** (`--analysis-only`): Raw LLM outputs, no derived metrics
2. **Complete pipeline**: Full synthesis with interpretation they may not want

**Gap**: No option for "analysis + framework calculations + researcher handoff"

---

## What We Provide vs. What Researchers Control

### Discernus Handles (Text Processing Excellence)

#### Large-Scale Framework Application
- Apply analytical frameworks consistently across entire corpus
- Generate dimensional scores for each document using LLM analysis
- Extract supporting evidence quotes with confidence/salience ratings
- Calculate framework-specified derived metrics and composite scores

#### Quality Assurance
- Complete audit trail of all processing decisions
- Content-addressable caching for reproducibility
- Methodological transparency and provenance tracking
- Academic-grade documentation of framework application

#### Data Preparation
- Clean, structured datasets ready for statistical analysis
- Standardized variable naming and formatting
- Universal file formats compatible with all statistical tools
- Complete metadata and variable documentation

### Researchers Control (Statistical & Interpretive Expertise)

#### Statistical Methodology
- Choice of statistical tests and analytical approaches
- Significance thresholds and multiple comparison corrections
- Model selection and validation strategies
- Missing data handling and outlier treatment

#### Research Interpretation
- Theoretical implications of statistical findings
- Contextual meaning within their research domain
- Causal claims and limitations of the analysis
- Integration with broader literature and theory

#### Academic Narrative
- Research questions and hypothesis formation
- Discussion of results and their significance
- Methodological limitations and future directions
- Conclusions and policy/theoretical recommendations

---

## Statistical Preparation Package Design

### Core Philosophy
**"Provide everything researchers need for their analysis, nothing they don't want to redo"**

### Package Structure
```
discernus_analysis_package/
├── discernus_data.csv              # Primary dataset
├── variable_codebook.csv           # Column definitions and descriptions
├── full_evidence.csv               # Complete evidence quotes (supplementary)
├── framework_documentation.md      # How framework was applied
├── processing_log.json            # Complete audit trail
├── README.txt                     # Plain text usage instructions
└── import_scripts/                # Optional tool-specific helpers
    ├── import_spss.sps
    ├── import_stata.do
    └── import_r.R
```

### Primary Dataset Format (discernus_data.csv)

#### Core Structure
```csv
document_id,speaker,dignity_score,dignity_evidence,dignity_confidence,truth_score,truth_evidence,truth_confidence,character_tension_composite,moral_character_index
doc_001,Senator Smith,0.85,"protecting vulnerable families",0.87,0.72,"demands accountability",0.83,0.23,0.785
doc_002,Rep Johnson,0.34,"personal responsibility",0.76,0.41,"merit-based outcomes",0.82,0.15,0.375
```

#### Column Categories

**Identifiers**
- `document_id`: Unique document identifier
- `speaker`: Document author/speaker
- `date`, `source`, etc.: Contextual metadata

**Raw Dimensional Scores** (Framework-dependent)
- Individual LLM-generated scores for each framework dimension
- Range: 0.0-1.0 or framework-specified scale
- One column per dimension (e.g., `dignity_score`, `truth_score`)

**Evidence Quotes** (Truncated for main dataset)
- Supporting textual evidence for each dimensional score
- Truncated to 100 characters for CSV compatibility
- One column per dimension (e.g., `dignity_evidence`, `truth_evidence`)

**Confidence Metrics**
- LLM confidence in each dimensional score
- Range: 0.0-1.0
- One column per dimension (e.g., `dignity_confidence`, `truth_confidence`)

**Derived Metrics** (Framework-calculated)
- Composite scores calculated using framework-specified formulas
- Examples: `character_tension_composite`, `moral_character_index`
- Cannot be easily reproduced without framework specification

#### Evidence Handling Strategy

**Main CSV**: Evidence quotes limited to 100 characters + "..." if truncated
**Rationale**: 
- Maintains CSV compatibility across all statistical tools
- Provides immediate context for scoring decisions
- Avoids Excel cell character limits (32,767 characters)

**Supplementary Evidence File**: Complete evidence quotes with full context
**Format**:
```csv
document_id,dimension,score,full_evidence_quote,confidence,salience,character_position
doc_001,dignity_score,0.85,"Senator Smith's call for 'protecting our most vulnerable families from economic hardship' demonstrates clear care-based moral reasoning",0.87,0.92,1247
```

### Variable Codebook Format

```csv
variable_name,description,data_type,range,calculation_method,framework_source
document_id,Unique document identifier,string,N/A,assigned,system
dignity_score,Civic Character Framework dignity dimension,numeric,0.0-1.0,LLM analysis,CHF v7.3 dignity definition
character_tension_composite,Overall character tension measure,numeric,0.0-1.0,framework formula,"|virtue_avg - vice_avg|"
```

### Framework Documentation

**Markdown format** including:
- Complete framework specification used
- LLM prompts and analysis instructions  
- Scoring rubrics and interpretation guidelines
- Version information and academic citations
- Processing parameters and model configurations

---

## Technical Implementation Requirements

### CLI Enhancement
```bash
# New statistical preparation mode
discernus run --statistical-prep

# Resume from statistical preparation to full synthesis
discernus run --resume-from-stats

# Existing modes remain unchanged
discernus run --analysis-only
discernus run  # Complete pipeline
```

### ThinOrchestrator Modifications

#### New Stage Integration
```python
def run_experiment(self, 
                  statistical_prep_only: bool = False,
                  resume_from_stats: bool = False,
                  **kwargs):
    
    # ... existing analysis logic ...
    
    if statistical_prep_only:
        # Calculate derived metrics using framework formulas
        derived_metrics_hash = self._calculate_derived_metrics(scores_hash)
        
        # Export statistical preparation package
        self._export_statistical_preparation_package(
            scores_hash, evidence_hash, derived_metrics_hash, 
            framework_content, experiment_config, results_dir
        )
        
        return self._finalize_statistical_preparation()
    
    # ... continue to synthesis if not statistical prep only ...
```

#### New Export Functions
- `_calculate_derived_metrics()`: Use existing MathToolkit functionality
- `_export_statistical_preparation_package()`: Generate CSV package
- `_create_variable_codebook()`: Generate metadata documentation
- `_finalize_statistical_preparation()`: Complete stage with appropriate messaging

### Content-Addressable Storage Integration

**Derived Metrics Caching**: 
- `derived_metrics_hash`: SHA256 of calculated composite scores
- Enables resume capability from statistical preparation stage
- Maintains complete provenance chain

**Package Versioning**:
- Statistical preparation packages are cached and versioned
- Researchers can regenerate identical packages for replication
- Changes to framework or processing trigger new package generation

---

## Academic Workflow Integration

### Typical Usage Pattern

#### Researcher Workflow
1. **Setup**: Create experiment with framework and corpus
2. **Processing**: `discernus run --statistical-prep`
3. **Analysis**: Load CSV into R/Python/STATA for statistical analysis
4. **Interpretation**: Apply domain expertise to statistical findings
5. **Publication**: Cite Discernus for text processing, own analysis for conclusions

#### Collaboration Workflow
1. **Data preparation specialist**: Runs statistical preparation
2. **Statistical analyst**: Performs analysis using preferred tools
3. **Domain expert**: Interprets results within theoretical framework
4. **Writing team**: Integrates findings into publication

### Methodological Transparency

#### In Methods Section
> "Text analysis was performed using Discernus v2.0 with the Civic Character Framework v7.3. 
> Discernus generated dimensional scores and framework-specified composite measures. 
> All statistical analysis and interpretation was performed independently using [R/STATA/Python] 
> following standard practices in [research domain]."

#### In Results Section
> "High dignity scores were evident in Senator Smith's statement including 'protecting vulnerable 
> families' (dignity score: 0.85, confidence: 0.87). Statistical analysis revealed..."

---

## Success Metrics

### Usage Adoption
- Number of experiments using `--statistical-prep` flag
- Ratio of statistical preparation vs. full pipeline usage
- User retention rates for statistical preparation users

### Academic Impact
- Publications citing Discernus for text processing only
- Diversity of statistical methods applied to Discernus-processed data
- Cross-institutional collaborations using shared Discernus datasets

### Quality Indicators
- Peer review acceptance rates for statistical preparation users
- Methodological rigor scores in published research
- Replication success rates using cached packages

---

## Risk Assessment

### Technical Risks

**CSV Size Limitations**: Large frameworks with many dimensions may create unwieldy files
- **Mitigation**: Evidence truncation, supplementary files, multiple CSV option

**Tool Compatibility**: Statistical software may have variable limits or import issues
- **Mitigation**: Extensive testing across R, Python, STATA, SPSS
- **Mitigation**: Tool-specific import scripts and documentation

### Market Risks

**Cannibalization**: Users may prefer statistical preparation over full pipeline
- **Assessment**: Low risk - different user segments with different needs
- **Opportunity**: Expands addressable market to methodology-conscious researchers

**Support Complexity**: Multiple output formats and tools increase support burden
- **Mitigation**: Comprehensive documentation and standardized formats
- **Mitigation**: Community-driven support through academic user base

---

## Next Steps

### Phase 1: Core Implementation
1. Implement `--statistical-prep` CLI flag
2. Develop CSV export functionality with evidence handling
3. Create variable codebook generation
4. Build basic documentation templates

### Phase 2: Tool Integration
1. Test compatibility across major statistical software
2. Develop tool-specific import scripts
3. Create comprehensive usage documentation
4. Implement resume-from-stats functionality

### Phase 3: Academic Validation
1. Pilot with academic collaborators
2. Gather feedback on format and usability
3. Refine based on real-world usage patterns
4. Document best practices and workflow guidance

---

*Document Version: 1.0*  
*Date: August 2025*  
*Status: Strategic Proposal*
