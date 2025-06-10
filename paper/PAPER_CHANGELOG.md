# Paper Changelog: Narrative Gravity Maps

All notable changes to the academic paper "Narrative Gravity Maps: A Quantitative Framework for Discerning the Forces Driving Persuasive Narratives" are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - Future

## [v1.0.1] - 2025-06-10

### Added
Fixed all validation overclaims in paper content - changed 'empirical validation' to 'technical implementation' throughout, removed inappropriate claims about human moral perception validation, updated validation checker to be more nuanced about appropriate vs inappropriate claims

### Evidence Status
- Technical validation: ✅ Available
- Case studies: ✅ Available  
- Human validation: ❌ Required for publication


### Planned
- Human validation studies section (v1.1.0)
- Cross-cultural validation analysis (v1.1.0)
- Expert annotation comparison results (v1.1.0)
- Expanded literature review incorporating human-LLM alignment research (v1.1.0)

## [1.0.0] - 2025-01-06

### Added
- **MAJOR CORRECTION**: Honest validation status assessment replacing overclaims
- Critical limitations section (6.1) addressing human alignment gap
- Clear distinction between technical consistency and empirical validation
- Required validation studies specification
- Appropriate current applications and limitations
- Future research priorities focused on human validation
- Literature review integration acknowledging LLM limitations

### Changed
- **Abstract**: Removed "empirical validation" claims, added human validation caveat
- **Introduction**: Clarified methodology as computational tool requiring validation
- **Keywords**: Changed from "empirical validation" to "computational consistency"
- **Section 6.1**: Complete rewrite addressing validation limitations honestly
- **Conclusion**: Honest assessment of current capabilities and limitations
- **Tone**: From definitive claims to appropriate academic caution

### Removed
- Overclaims about "production-ready status" for human moral perception
- Assertions that cross-LLM consistency equals empirical validation
- Inappropriate confidence about capturing human moral judgment

### Fixed
- Validation methodology confusion (technical vs. empirical)
- Overclaims about framework's relationship to human perception
- Missing acknowledgment of LLM limitations from recent research

### Evidence Status
- ✅ Technical implementation validation documented
- ✅ Cross-LLM consistency data (r > 0.90) properly contextualized
- ✅ Case study analyses included with appropriate caveats
- ❌ Human validation studies - acknowledged as critical gap
- ❌ Expert annotation studies - identified as required next step

## [0.9.0] - 2025-01-05 (Historical Reconstruction)

### Added (Before Validation Correction)
- Complete mathematical framework documentation
- Civic Virtue Framework implementation details
- Case study analyses (Trump, Obama, Biden inaugural addresses)
- Cross-LLM reliability testing results
- Enhanced metrics formulation (COM, NPS, DPS)
- Differential weighting system theoretical justification

### Known Issues (Corrected in v1.0.0)
- Overclaimed "empirical validation" without human studies
- Conflated technical consistency with human alignment
- Insufficient acknowledgment of LLM limitations
- Missing critical literature review on human-LLM alignment

## Version Guidelines

### MAJOR Version (X.0.0)
**Increment when**: Fundamental changes to:
- Core methodology or mathematical framework
- Primary conclusions or claims
- Framework architecture or theoretical foundations
- Validation status (e.g., completing human validation studies)

### MINOR Version (X.Y.0) 
**Increment when**: Adding:
- New validation studies or evidence
- Additional case studies or analyses
- New sections or substantial content
- Co-author contributions
- Significant methodological refinements

### PATCH Version (X.Y.Z)
**Increment when**: Making:
- Corrections and clarifications
- Minor edits and improvements
- Bibliography updates
- Formatting changes
- Figure/table corrections

## Evidence Tracking

### v1.0.0 Evidence Base
```
evidence/
├── technical_validation/
│   ├── cross_llm_correlation_data.json     # r > 0.90 across models
│   ├── system_reliability_metrics.json    # 99.5% test success
│   └── multi_run_consistency_analysis.json # Statistical reliability
├── case_studies/
│   ├── trump_2017_inaugural_analysis.json
│   ├── biden_2021_inaugural_analysis.json
│   ├── obama_2009_inaugural_multirun.json
│   └── comparative_analysis_metrics.json
└── figures/
    ├── trump_vs_biden_comparison.png
    ├── obama_multirun_dashboard.png
    └── civic_virtue_framework_diagram.png
```

### Critical Evidence Gaps (Must Address for v1.1.0)
- **Human validation studies**: Expert annotation comparison data
- **Inter-rater reliability**: Human expert agreement on narrative scoring
- **Salience ranking validation**: Human vs. LLM theme prioritization
- **Cross-cultural validation**: Framework applicability across contexts

## Review Status

### Internal Reviews
- [x] Technical accuracy review (2025-01-06)
- [x] Validation claims audit (2025-01-06) 
- [x] Literature review integration (2025-01-06)
- [ ] Independent technical review (planned)
- [ ] Academic writing quality review (planned)

### External Reviews
- [ ] Expert peer review (planned for v1.1.0)
- [ ] Methodology review by computational linguistics expert (planned)
- [ ] Moral psychology expert feedback (planned)

## Development Notes

### Research Integrity
- **No overclaims**: Every assertion backed by appropriate evidence
- **Transparent limitations**: Clear acknowledgment of validation gaps  
- **Reproducible**: All analysis materials organized for independent verification
- **Methodologically sound**: Appropriate statistical and validation procedures

### Independent Researcher Strategy
- **Credibility through transparency**: Open methodology and honest limitations
- **Evidence-based progression**: No version advancement without supporting data
- **Collaboration-ready**: Materials organized for potential co-author involvement
- **Publication-focused**: Systematic preparation for peer review process

---

*This changelog maintains complete transparency about paper development, ensuring that validation claims align precisely with available evidence and that the research maintains academic integrity throughout the publication process.* 