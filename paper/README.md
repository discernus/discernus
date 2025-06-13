# Narrative Gravity Maps: Academic Paper Development

This directory contains all materials related to the academic paper on Narrative Gravity Maps methodology.

## Directory Structure

```
paper/
├── README.md                    # This file - paper development guide
├── PAPER_CHANGELOG.md           # Version history and changes
├── drafts/                      # Version-controlled paper drafts
│   ├── narrative_gravity_maps_v1.0.0.md    # Current corrected draft
│   └── [future versions]
├── evidence/                    # Supporting evidence and data
│   ├── validation_studies/      # Human validation study results
│   ├── technical_validation/    # Cross-LLM consistency data
│   ├── case_studies/           # Analyzed speeches and results
│   └── figures/                # Charts, visualizations, tables
├── reviews/                     # Peer review and feedback
│   ├── internal_reviews/        # Self-review and iteration notes
│   ├── expert_feedback/         # External expert input
│   └── journal_reviews/         # Formal peer review (when received)
└── submission/                  # Journal submission materials
    ├── formatted_versions/      # Journal-specific formatted drafts
    ├── supplementary_materials/ # Additional files for submission
    └── replication_package/     # Complete reproducibility materials
```

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

**Current Version**: v1.0.0 (June 2025)
**Status**: PROGRESSIVE UPDATE
**Next Milestone**: Human validation studies required before publication submission

### Key Validation Tasks Remaining:
- [ ] Expert annotation studies comparing LLM outputs to human judgment
- [ ] Cross-cultural validation of framework assumptions
- [ ] Temporal consistency testing across different time periods
- [ ] Salience ranking validation studies

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