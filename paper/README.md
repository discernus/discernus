# Academic Papers: Dual Development

This directory contains all materials related to two complementary academic papers being developed in parallel within the Narrative Gravity Analysis project.

## Directory Structure

```
paper/
├── README.md                           # This file - dual paper development guide
├── PAPER_CHANGELOG.md                  # Shared version history and changes
├── ngmp_twm_glossary.md               # Shared terminology for both papers
├── manage_paper.py                     # Paper management utilities
├── drafts/                            # Version-controlled paper drafts
│   ├── narrative_gravity_maps/        # NGM Paper: Universal Methodology
│   │   ├── README.md                  # NGM-specific development guide
│   │   ├── narrative_gravity_maps_v1.3.1.md  # Latest NGM version
│   │   └── [version history]         # Previous NGM versions
│   └── three_wells_model/             # TWM Paper: Political Discourse Theory
│       ├── README.md                  # TWM-specific development guide
│       ├── three_wells_model_paper_draft_v1.md  # Latest TWM version
│       └── [future versions]         # TWM version history
├── bibliography/                       # Shared bibliography for both papers
├── evidence/                          # Supporting evidence and data
│   ├── validation_studies/            # Human validation study results
│   ├── technical_validation/          # Cross-LLM consistency data
│   ├── case_studies/                  # Analyzed speeches and results
│   └── figures/                       # Charts, visualizations, tables
├── reviews/                           # Peer review and feedback
│   ├── internal_reviews/              # Self-review and iteration notes
│   ├── expert_feedback/               # External expert input
│   └── journal_reviews/               # Formal peer review (when received)
└── submission/                        # Journal submission materials
    ├── formatted_versions/            # Journal-specific formatted drafts
    ├── supplementary_materials/       # Additional files for submission
    └── replication_package/           # Complete reproducibility materials
```

## Two Complementary Papers

### 1. Narrative Gravity Maps (NGM) Paper
**Focus**: Universal quantitative methodology for analyzing persuasive discourse across any analytical domain
**Current Version**: v1.3.1 - Framework-Agnostic Universal Methodology with Systematic Experimental Design
**Key Contribution**: Technical methodology with systematic experimental design framework

### 2. Three Gravitational Wells Model (TWM) Paper  
**Focus**: Specific theoretical framework for understanding contemporary political discourse
**Current Version**: v1.0 - Three Gravitational Wells of Contemporary Political Discourse: An Integrative Analysis
**Key Contribution**: Political theory applying gravitational wells concept to contemporary discourse

### Relationship and Synergy
- **NGM Paper**: Provides the universal methodology and technical infrastructure
- **TWM Paper**: Demonstrates a specific theoretical application with political significance
- **Parallel Development**: Both papers can advance simultaneously, each strengthening the other
- **Shared Foundation**: Same underlying mathematical framework and computational implementation
- **Different Audiences**: NGM targets methodological/computational communities; TWM targets political science/theory communities

## Paper Development Workflow

### Version Control System
- **Semantic Versioning**: `vMAJOR.MINOR.PATCH`
  - `MAJOR`: Fundamental changes to methodology, framework, or conclusions
  - `MINOR`: New sections, significant content additions, validation studies
  - `PATCH`: Corrections, clarifications, minor edits

### Development Process

#### 1. Draft Development
```bash
# Create new version when making significant changes
cp paper/drafts/narrative_gravity_maps_v1.0.0.md paper/drafts/narrative_gravity_maps_v1.1.0.md
```

#### 2. Evidence Collection
- All supporting data goes in `evidence/` with clear provenance
- Link evidence files to specific paper sections
- Maintain evidence changelog for reproducibility

#### 3. Review Integration
- Internal reviews and iterations tracked in `reviews/internal_reviews/`
- External feedback organized by reviewer/source
- Changes documented in PAPER_CHANGELOG.md

#### 4. Submission Preparation
- Journal-specific formatting in `submission/formatted_versions/`
- Complete replication package assembled in `submission/replication_package/`

## Current Status

### Narrative Gravity Maps Paper
**Current Version**: v1.3.1 (December 2024)
**Status**: EXPERIMENTAL DESIGN FRAMEWORK COMPLETE
**Next Milestone**: Complete systematic experimental validation across all five frameworks

**Key Development Tasks**:
- [ ] Complete systematic experimental validation across all five frameworks
- [ ] Conduct human-LLM comparison studies for each framework implementation  
- [ ] Generate publication-ready experimental results visualizations
- [ ] Develop comprehensive experimental replication packages

### Three Wells Model Paper
**Current Version**: v1.0 (December 2024)
**Status**: THEORETICAL FRAMEWORK COMPLETE
**Next Milestone**: Empirical validation using NGM methodology

**Key Development Tasks**:
- [ ] Implement pilot empirical strategy using Narrative Gravity Map methodology
- [ ] Complete development of Historical Ideological Triangle framework (Appendix A)
- [ ] Develop more detailed case studies and evidence
- [ ] Strengthen discussion of democratic implications and practical applications

### Shared Validation Requirements:
- [ ] Expert annotation studies comparing LLM outputs to human judgment
- [ ] Cross-cultural validation of framework assumptions  
- [ ] Temporal consistency testing across different time periods
- [ ] Human validation studies (critical gap for both papers)

## Evidence Requirements

### For Publication Credibility:
1. **Human Validation Data**: Inter-rater reliability studies, expert annotation results
2. **Statistical Evidence**: Confidence intervals, significance tests, effect sizes
3. **Replication Materials**: Complete code, data, and instructions for reproduction
4. **Methodological Documentation**: Detailed validation protocols and procedures

### Current Evidence Status:
- ✅ Technical implementation validation (99.5% test success)
- ✅ Cross-LLM consistency data (r > 0.90)
- ✅ Case study analyses (Trump, Obama, Biden inaugural addresses)
- ❌ Human validation studies (critical gap)
- ❌ Expert annotation comparison (required for publication)
- ❌ Cross-cultural validation (needed for generalizability claims)

## Quality Standards

### Before Any Version Increment:
- [ ] All claims supported by evidence in `evidence/` directory
- [ ] No validation overclaims (human vs. technical validation clearly distinguished)
- [ ] Methodology limitations clearly acknowledged
- [ ] Future research directions specified

### Before Submission:
- [ ] Peer review by at least 2 independent experts
- [ ] Complete replication package tested by external party
- [ ] All figures and tables properly referenced and captioned
- [ ] Bibliography complete and properly formatted
- [ ] Journal-specific formatting requirements met

## Development Notes

### Independent Researcher Considerations:
- **No institutional affiliation**: Emphasize methodological rigor and transparency
- **Limited resources**: Focus validation studies on highest-impact questions
- **AI-assisted development**: Document AI assistance appropriately in acknowledgments
- **Credibility building**: Ensure every claim is backed by solid evidence

### Collaboration Strategy:
- Invite academic co-authors after validation studies demonstrate value
- Share replication packages to enable independent verification
- Build credibility through transparency rather than authority

---

*This paper development system ensures rigorous tracking of evidence, proper version control, and systematic preparation for academic publication while maintaining the transparency and reproducibility essential for independent research credibility.* 