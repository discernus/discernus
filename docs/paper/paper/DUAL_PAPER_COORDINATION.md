# Dual Paper Development Coordination Guide

## Overview

This guide provides workflows for developing both the **Narrative Gravity Maps (NGM)** and **Three Gravitational Wells Model (TWM)** papers in parallel, leveraging their complementary relationship while maintaining independent development tracks.

## Paper Relationship Matrix

| Aspect | NGM Paper | TWM Paper | Shared Elements |
|--------|-----------|-----------|-----------------|
| **Primary Focus** | Universal Methodology | Political Theory Application | Mathematical Framework |
| **Target Audience** | Computational Social Science | Political Science/Theory | Interdisciplinary |
| **Core Contribution** | Technical Infrastructure | Theoretical Framework | Gravitational Wells Concept |
| **Evidence Requirements** | Cross-domain validation | Political discourse validation | Human validation studies |
| **Development Priority** | Experimental design completion | Empirical validation | Shared validation infrastructure |

## Parallel Development Workflows

### 1. Independent Development Track

**When to work independently:**
- NGM: Technical methodology refinements, experimental design improvements
- TWM: Theoretical argumentation, political case studies, historical analysis
- Both: Writing, section development, citation management

**Workflow:**
```bash
# Work on NGM paper
cd paper/drafts/narrative_gravity_maps/
# Edit narrative_gravity_maps_v1.3.1.md or create new version

# Work on TWM paper  
cd paper/drafts/three_wells_model/
# Edit three_wells_model_paper_draft_v1.md or create new version
```

### 2. Synergistic Development Track

**When to coordinate development:**
- Shared terminology and definitions
- Mathematical framework consistency
- Validation methodology alignment
- Cross-references and mutual citations

**Coordination Points:**
1. **Terminology Alignment**: Update `paper/ngmp_twm_glossary.md` when either paper develops new concepts
2. **Mathematical Consistency**: Ensure identical formulations across both papers
3. **Cross-Citations**: Each paper should reference the other appropriately
4. **Validation Coordination**: Share validation studies and human judgment data

### 3. Joint Validation Track

**Shared Validation Requirements:**
- Human validation studies serve both papers
- Technical validation of mathematical framework benefits both
- Cross-domain testing strengthens both methodological and theoretical claims

**Shared Development Areas:**
- `paper/evidence/validation_studies/` - Human validation data
- `paper/evidence/technical_validation/` - Cross-LLM consistency
- `paper/bibliography/` - Shared academic sources
- Framework implementations in `frameworks/` directory

## Version Coordination Strategy

### Independent Versioning
- Each paper maintains its own version numbers
- NGM: Currently v1.3.1, focuses on technical methodology
- TWM: Currently v1.0, focuses on theoretical development

### Coordination Points
- Major releases of either paper should trigger review of the other
- Shared glossary updates require coordination across both papers
- Mathematical framework changes affect both papers simultaneously

### Change Documentation
- Paper-specific changes: Document in respective README files
- Shared changes: Document in main `PAPER_CHANGELOG.md`
- Cross-paper impacts: Note in both papers' documentation

## Development Priorities Coordination

### Phase 1: Parallel Foundation Building (Current)
- **NGM**: Complete experimental design framework validation
- **TWM**: Implement empirical validation using NGM methodology
- **Shared**: Develop human validation study infrastructure

### Phase 2: Integrated Validation
- **NGM**: Human-LLM comparison studies across all frameworks
- **TWM**: Apply NGM methodology to political discourse corpus
- **Shared**: Cross-domain validation demonstrating universal applicability

### Phase 3: Publication Preparation
- **NGM**: Target computational social science venues
- **TWM**: Target political science/theory venues  
- **Shared**: Coordinate timing to maximize cross-citation benefits

## Practical Coordination Workflows

### Daily Development
1. **Check glossary**: Review shared terms before significant writing
2. **Mathematical consistency**: Verify formulations match across papers
3. **Cross-references**: Update citations as papers evolve

### Weekly Coordination
1. **Progress sync**: Review development in both papers
2. **Shared resource update**: Update bibliography, evidence, validation data
3. **Terminology alignment**: Resolve any definitional inconsistencies

### Major Version Coordination
1. **Cross-impact review**: How does this change affect the other paper?
2. **Terminology update**: Update shared glossary as needed
3. **Mathematical alignment**: Ensure consistent technical presentation
4. **Citation updates**: Update cross-references appropriately

## Quality Assurance for Dual Development

### Consistency Checks
- [ ] Mathematical formulations identical across papers
- [ ] Terminology definitions consistent with shared glossary
- [ ] Cross-references accurate and current
- [ ] Shared evidence properly referenced in both papers

### Development Standards
- [ ] Changes to shared elements documented in both papers
- [ ] Version increments consider impact on other paper
- [ ] Validation studies designed to serve both papers when possible
- [ ] Academic citations checked for relevance to both papers

## Submission Strategy Coordination

### Timing Considerations
- **Option 1**: Sequential submission (NGM first, then TWM with established methodology)
- **Option 2**: Parallel submission to different venues (maximize independence)
- **Option 3**: Joint submission as companion papers (emphasize relationship)

### Cross-Citation Strategy
- Each paper should cite the other as complementary work
- NGM cites TWM as example application
- TWM cites NGM as methodological foundation
- Coordinate submission timing to enable mutual citation

### Resource Sharing
- Shared validation studies reduce overall effort
- Joint replication package serves both papers
- Coordinated peer review can provide feedback on both

---

This coordination guide ensures that both papers can advance independently while leveraging their complementary relationship to strengthen the overall contribution to academic literature. 