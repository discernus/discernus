# EPIC: Statistical Preparation Offramp
*GitHub Issue Epic for Statistical Preparation Enhancement*

---

## Epic Overview

**Epic Title**: Statistical Preparation Offramp - Researcher-Ready Data Export  
**Epic Label**: `enhancement`, `statistical-methodology`, `peer-review`  
**Milestone**: Alpha Comprehensive (Academic Gold Standard)  
**Estimated Effort**: 5-7 issues, ~2-3 Cursor development days

### Strategic Context

Enable researchers to use Discernus for large-scale text processing while maintaining complete control over statistical analysis and interpretation. This creates a clean "trust boundary" where Discernus handles text analysis excellence and researchers handle statistical methodology.

**Market Position**: "Discernus handles large-scale text analysis; researchers handle statistical interpretation and conclusions."

**Target Users**: Academic researchers who need large-scale text processing but prefer their own statistical tools (R, Python, STATA, SPSS).

---

## Epic User Stories

### Primary User Story
> **As a conservative researcher**, I want to use Discernus for large-scale text processing and receive analysis-ready datasets, so that I can perform statistical analysis using my preferred tools while maintaining methodological control.

### Secondary User Stories
- **As a mixed-methodology team**, we want to divide responsibilities between text processing specialists and statistical analysts
- **As a cost-conscious researcher**, I want to optimize my LLM spending by using Discernus only for text processing
- **As a methodologically rigorous researcher**, I want complete transparency in text processing with the ability to perform my own statistical validation

---

## Technical Architecture

### New Orchestration Stage
```
Pre-Flight → Analysis → Statistical → Synthesis → Finalization
Validation     Stage    Preparation     Stage       Stage
                          ↓ OFFRAMP
                     Researcher-Ready
                        Dataset
```

### Core Components
1. **Statistical Preparation Agent**: Calculates framework-specified derived metrics
2. **CSV Export System**: Generates researcher-ready datasets with evidence
3. **Configuration Profiles**: Durable user preferences for workflow modes
4. **Resume Capability**: Can continue from statistical prep to full synthesis

### Integration Points
- **Content-Addressable Storage**: New artifact types with SHA-256 hashing
- **Provenance System**: Extended audit trail for statistical preparation stage
- **Git Persistence**: Appropriate commit messages and resume capability
- **CLI Configuration**: Profile system and durable preferences

---

## Implementation Issues

### Issue 1: Core Statistical Preparation Infrastructure
**Title**: Implement Statistical Preparation Stage and CSV Export System  
**Labels**: `enhancement`, `orchestration`, `high-priority`  
**Story Points**: 8

**Acceptance Criteria**:
- [ ] Add `--statistical-prep` CLI flag to ThinOrchestrator
- [ ] Implement derived metrics calculation using existing MathToolkit
- [ ] Create CSV export with raw scores, derived metrics, and evidence quotes
- [ ] Generate variable codebook with column definitions
- [ ] Store statistical preparation artifacts with content-addressable hashing
- [ ] Update manifest.json to track statistical preparation stage
- [ ] Maintain complete provenance chain for resume capability

**Technical Tasks**:
- [ ] Extend `ThinOrchestrator.run_experiment()` with `statistical_prep_only` parameter
- [ ] Create `_calculate_derived_metrics()` method using framework calculation specs
- [ ] Implement `_export_statistical_preparation_package()` for CSV generation
- [ ] Add `statistical_preparation` stage to EnhancedManifest
- [ ] Update ProvenanceOrganizer for statistical prep artifacts

### Issue 2: Enhanced CSV Export with Evidence Integration
**Title**: Implement Evidence-Integrated CSV Export for Statistical Analysis  
**Labels**: `enhancement`, `data-quality`, `statistical-methodology`  
**Story Points**: 5

**Acceptance Criteria**:
- [ ] Single CSV with raw scores, derived metrics, and truncated evidence (100 chars)
- [ ] Supplementary full evidence CSV for detailed validation
- [ ] Variable codebook CSV with column definitions and metadata
- [ ] Framework documentation markdown with application details
- [ ] Processing log JSON with complete audit trail
- [ ] Universal compatibility with R, Python, STATA, SPSS, Excel

**Technical Tasks**:
- [ ] Design flat CSV schema for multi-framework compatibility
- [ ] Implement evidence quote truncation with "..." indicator
- [ ] Create variable codebook generator with data types and ranges
- [ ] Generate framework documentation from experiment metadata
- [ ] Add processing log with LLM interactions and decisions

### Issue 3: Configuration Profiles and Durable Preferences
**Title**: Implement Research Workflow Configuration Profiles  
**Labels**: `enhancement`, `user-experience`, `peer-review`  
**Story Points**: 6

**Acceptance Criteria**:
- [ ] New configuration options: `default_execution_mode`, `synthesis.default_enabled`
- [ ] Pre-configured profiles: `conservative-researcher`, `complete-pipeline`, `minimal-processing`
- [ ] Interactive configuration wizard: `discernus config setup`
- [ ] Profile application command: `discernus config profile [name]`
- [ ] Environment variable support: `DISCERNUS_DEFAULT_EXECUTION_MODE`
- [ ] Workspace-specific configuration: `discernus config init --profile [name]`

**Technical Tasks**:
- [ ] Extend DiscernusConfig class with new execution mode options
- [ ] Create configuration profile templates (YAML files)
- [ ] Implement interactive setup wizard with workflow choice
- [ ] Add profile management CLI commands
- [ ] Update CLI run command to respect configuration defaults

### Issue 4: Resume Capability and Workflow Flexibility
**Title**: Implement Resume from Statistical Preparation to Full Synthesis  
**Labels**: `enhancement`, `orchestration`, `reproducibility`  
**Story Points**: 4

**Acceptance Criteria**:
- [ ] `discernus run --resume-from-stats` command functionality
- [ ] Automatic detection of existing statistical preparation artifacts
- [ ] Seamless continuation from statistical prep to synthesis stage
- [ ] Updated manifest.json with resume history and provenance
- [ ] Extended directory structure with synthesis artifacts
- [ ] Preserved statistical preparation results alongside synthesis results

**Technical Tasks**:
- [ ] Implement `--resume-from-stats` CLI option
- [ ] Add resume detection logic in ThinOrchestrator
- [ ] Extend existing directory structure without overwriting
- [ ] Update manifest with resume metadata and timeline
- [ ] Preserve complete audit trail across resume operations

### Issue 5: Enhanced User Experience and Messaging
**Title**: Implement User-Friendly Messaging for Statistical Preparation Mode  
**Labels**: `enhancement`, `user-experience`, `documentation`  
**Story Points**: 3

**Acceptance Criteria**:
- [ ] Clean, focused messaging for statistical preparation mode (no synthesis suggestions)
- [ ] Professional researcher-oriented output formatting
- [ ] Clear next-steps guidance for external statistical analysis
- [ ] Updated README templates for statistical preparation runs
- [ ] Tool-specific import scripts (R, Python, STATA) in statistical package
- [ ] Plain-text usage instructions in researcher package

**Technical Tasks**:
- [ ] Create statistical preparation specific messaging templates
- [ ] Update ProvenanceOrganizer README generation for researcher focus
- [ ] Generate tool-specific import scripts (R, Python, STATA)
- [ ] Create plain-text usage instructions and workflow guide
- [ ] Implement clean, non-nagging user interface

### Issue 6: Integration Testing and Validation
**Title**: Comprehensive Testing for Statistical Preparation Workflow  
**Labels**: `testing`, `statistical-methodology`, `reproducibility`  
**Story Points**: 4

**Acceptance Criteria**:
- [ ] Unit tests for statistical preparation stage and CSV export
- [ ] Integration tests for complete statistical preparation workflow
- [ ] Resume capability testing from statistical prep to synthesis
- [ ] Configuration profile testing and validation
- [ ] Cross-tool compatibility testing (R, Python, STATA import)
- [ ] Large-scale corpus testing (1000+ documents) with complex frameworks

**Technical Tasks**:
- [ ] Write unit tests for new ThinOrchestrator methods
- [ ] Create integration tests for statistical preparation pipeline
- [ ] Test resume functionality with various experiment configurations
- [ ] Validate CSV output compatibility across statistical software
- [ ] Performance testing with large corpora and complex frameworks

### Issue 7: Documentation and Academic Workflow Guides
**Title**: Create Documentation for Statistical Preparation Research Workflows  
**Labels**: `documentation`, `peer-review`, `user-experience`  
**Story Points**: 3

**Acceptance Criteria**:
- [ ] Conservative researcher workflow guide with setup instructions
- [ ] Configuration system documentation with profile examples
- [ ] Academic collaboration guide for mixed-methodology teams
- [ ] Tool-specific analysis examples (R, Python, STATA)
- [ ] Peer review and citation guidance for statistical preparation users
- [ ] Migration guide for existing users who want to switch modes

**Technical Tasks**:
- [ ] Write comprehensive conservative researcher guide
- [ ] Document configuration profiles and setup procedures
- [ ] Create academic workflow examples and best practices
- [ ] Develop tool-specific analysis templates and examples
- [ ] Update CLI documentation with new commands and options

---

## Success Criteria

### Technical Success
- [ ] Statistical preparation mode produces analysis-ready CSV datasets
- [ ] Complete provenance and audit trail maintained
- [ ] Resume capability works seamlessly
- [ ] Configuration profiles enable durable user preferences
- [ ] Cross-tool compatibility validated (R, Python, STATA, SPSS)

### User Experience Success
- [ ] Conservative researchers can set preferences once and forget
- [ ] No unwanted synthesis suggestions or "nagging" in statistical prep mode
- [ ] Clear, professional messaging focused on text processing excellence
- [ ] Easy collaboration between text processing specialists and statistical analysts

### Academic Impact Success
- [ ] Researchers can cite Discernus for text processing while maintaining statistical methodology control
- [ ] Complete transparency and auditability for peer review
- [ ] Reproducible research packages with full provenance
- [ ] Academic-grade documentation and workflow guidance

---

## Dependencies and Risks

### Technical Dependencies
- [ ] Existing MathToolkit framework calculation functionality
- [ ] Content-addressable storage and provenance system
- [ ] Current CLI configuration architecture
- [ ] EnhancedManifest and ProvenanceOrganizer systems

### Risks and Mitigations
- **Complexity Risk**: Multiple execution modes could confuse users
  - *Mitigation*: Configuration profiles and wizard make choice simple and durable
- **CSV Size Risk**: Large frameworks with many dimensions may create unwieldy files
  - *Mitigation*: Evidence truncation, supplementary files, performance testing
- **Tool Compatibility Risk**: Statistical software may have import issues
  - *Mitigation*: Extensive cross-tool testing and tool-specific import scripts

### Integration Risks
- **Breaking Changes**: New functionality could disrupt existing workflows
  - *Mitigation*: All changes are additive; existing complete pipeline unchanged
- **Provenance Complexity**: Extended artifact chain could break validation
  - *Mitigation*: Builds on existing content-addressable architecture

---

## Definition of Done

### Epic Completion Criteria
- [ ] All 7 implementation issues completed and tested
- [ ] Statistical preparation workflow fully functional end-to-end
- [ ] Configuration profiles working with durable preferences
- [ ] Resume capability tested and validated
- [ ] Cross-tool compatibility confirmed
- [ ] Documentation complete and accurate
- [ ] Integration tests passing
- [ ] Academic workflow guides published

### Quality Gates
- [ ] No regression in existing complete pipeline functionality
- [ ] Statistical preparation produces identical results to manual calculation
- [ ] CSV exports load successfully in R, Python, STATA, SPSS
- [ ] Provenance system maintains complete audit trail
- [ ] Performance acceptable for large corpora (1000+ documents)

---

## Timeline and Sequencing

### Phase 1: Core Infrastructure (Issues 1-2)
**Duration**: 1.5 Cursor days  
**Focus**: Basic statistical preparation and CSV export functionality

### Phase 2: User Experience (Issues 3, 5)
**Duration**: 1 Cursor day  
**Focus**: Configuration profiles and user-friendly interface

### Phase 3: Advanced Features (Issues 4, 6)
**Duration**: 0.5 Cursor days  
**Focus**: Resume capability and comprehensive testing

### Phase 4: Documentation (Issue 7)
**Duration**: 0.5 Cursor days  
**Focus**: Academic workflow guides and user documentation

**Total Estimated Effort**: 3.5 Cursor development days

---

## Related Documentation

- [Statistical Preparation Offramp Strategic Analysis](pm/active_projects/STATISTICAL_PREPARATION_OFFRAMP.md)
- [Provenance Integration Specification](pm/active_projects/STATISTICAL_PREPARATION_PROVENANCE_INTEGRATION.md)
- [Conservative Researcher Configuration Design](pm/active_projects/CONSERVATIVE_RESEARCHER_CONFIG_DESIGN.md)
- [Complete Orchestration Flow Documentation](docs/developer/workflows/COMPLETE_ORCHESTRATION_FLOW.md)

---

*Epic Version: 1.0*  
*Created: August 2025*  
*Status: Ready for Implementation*
