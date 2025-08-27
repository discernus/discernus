# Strategic Planning & Architecture Milestone

**Milestone**: Strategic Planning & Architecture
**Status**: Active
**Issues**: Open issues related to long-term strategic planning and architectural decisions

---

## Open Issues

### Strategy for 'But It Works on My Machine' Problem
- **Issue**: #421
- **Labels**: epic
- **Assignees**: 
- **Created**: 2025-08-11
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: Strategy for 'But It Works on My Machine' Problem

**Full Description**:
## Strategy for 'But It Works on My Machine' Problem

**Objective**: Eliminate environment-specific issues that prevent reproducible research

**Strategic Context**:
- Research reproducibility is critical for academic credibility
- Environment differences can invalidate research results
- Need consistent, reproducible execution across all platforms

**Problem Analysis**:
- **Environment Differences**: OS, Python versions, dependency versions
- **System Dependencies**: GPU drivers, system libraries, hardware differences
- **Configuration Drift**: Environment variables, paths, settings
- **Dependency Conflicts**: Package version incompatibilities

**Solution Strategy**:
- [ ] **Containerization**: Docker containers for consistent environments
- [ ] **Dependency Pinning**: Exact version requirements for all packages
- [ ] **Environment Validation**: Automated environment health checks
- [ ] **Configuration Management**: Centralized, version-controlled configs
- [ ] **CI/CD Integration**: Automated testing across multiple environments

**Implementation Plan**:
- [ ] **Phase 1**: Dependency pinning and environment validation
- [ ] **Phase 2**: Docker containerization for core platform
- [ ] **Phase 3**: Multi-environment CI/CD pipeline
- [ ] **Phase 4**: User environment setup automation

**Success Criteria**:
- [ ] 100% reproducible execution across environments
- [ ] Automated environment validation
- [ ] Clear setup instructions for all platforms
- [ ] CI/CD testing across multiple environments

**Priority**: HIGH - Research credibility foundation
**Dependencies**: Testing infrastructure completion

---

### GitHub Strategy: Clean Separation of Development vs Open Source Code
- **Issue**: #420
- **Labels**: epic
- **Assignees**: 
- **Created**: 2025-08-11
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: GitHub Strategy: Clean Separation of Development vs Open Source Code

**Full Description**:
## GitHub Strategy: Clean Separation of Development vs Open Source Code

**Objective**: Establish strategy for cleanly separating internal development code from open source version

**Strategic Context**:
- Much of current codebase is internal development/experimental
- Need clean separation for professional open source release
- Protect internal IP while enabling community contribution

**Current Codebase Analysis**:
- **Internal/Experimental**: Research spikes, experimental frameworks, internal tools
- **Open Source Ready**: Core platform, stable frameworks, user-facing features
- **Business Critical**: Enterprise features, proprietary algorithms, business logic

**Separation Strategy**:
- [ ] **Repository Structure**: Main repo vs. internal development repos
- [ ] **Branch Strategy**: Main branch (open source) vs. development branches
- [ ] **Feature Flags**: Internal features disabled in open source builds
- [ ] **Configuration Management**: Environment-specific feature enablement
- [ ] **Documentation**: Clear boundaries between open/closed components

**Implementation Plan**:
- [ ] Audit current codebase for open source readiness
- [ ] Create internal development repository structure
- [ ] Implement feature flag system for internal features
- [ ] Establish contribution guidelines and boundaries
- [ ] Create open source release pipeline

**Success Criteria**:
- [ ] Clean separation established
- [ ] Internal IP protected
- [ ] Open source version professional and complete
- [ ] Contribution workflow clear and safe

**Priority**: HIGH - Open source release foundation
**Dependencies**: License selection, business strategy finalization

---

### Project Open Source License Dependencies and Business Strategy Alignment
- **Issue**: #419
- **Labels**: epic, legal, dependencies
- **Assignees**: 
- **Created**: 2025-08-11
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: Project Open Source License Dependencies and Business Strategy Alignment

**Full Description**:
## Project Open Source License Dependencies and Business Strategy Alignment

**Objective**: Ensure all project dependencies are license-compatible with our business strategy

**Strategic Context**:
- Audit all third-party dependencies for license compatibility
- Identify potential license conflicts with future commercial offerings
- Establish dependency management strategy

**Scope**:
- [ ] Complete dependency license audit
- [ ] License compatibility matrix creation
- [ ] Conflict resolution strategy
- [ ] Alternative dependency evaluation
- [ ] License compliance monitoring
- [ ] Business impact assessment

**Critical Dependencies to Audit**:
- **LLM APIs**: OpenAI, Anthropic, Google Vertex AI
- **Python Libraries**: pandas, numpy, scipy, etc.
- **Framework Dependencies**: Any specialized research tools
- **Infrastructure**: Cloud services, databases, etc.

**Business Strategy Considerations**:
- [ ] Future commercial licensing model
- [ ] Enterprise feature development
- [ ] White-label opportunities
- [ ] Revenue model constraints

**Success Criteria**:
- [ ] All dependencies license-compatible
- [ ] Business strategy alignment confirmed
- [ ] Risk mitigation plan in place
- [ ] Compliance monitoring established

**Priority**: HIGH - Business model foundation
**Dependencies**: License selection decision

---

### EPIC: Open Source License Selection and Implementation
- **Issue**: #418
- **Labels**: epic, legal
- **Assignees**: 
- **Created**: 2025-08-11
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: EPIC: Open Source License Selection and Implementation

**Full Description**:
## EPIC: Open Source License Selection and Implementation

**Objective**: Select and implement appropriate open source license for Discernus

**Strategic Context**:
- Balance open source adoption with business strategy
- Ensure license compatibility with future commercial offerings
- Protect intellectual property while enabling community contribution

**Scope**:
- [ ] License research and evaluation
- [ ] Business strategy alignment assessment
- [ ] Legal review and compliance
- [ ] License implementation across codebase
- [ ] Contributor license agreement (CLA) setup
- [ ] License documentation and notices

**License Considerations**:
- **MIT/Apache 2.0**: Permissive, business-friendly
- **GPL v3**: Copyleft, ensures derivatives stay open
- **AGPL v3**: Network copyleft, strongest protection
- **Dual licensing**: Open source + commercial options

**Business Strategy Alignment**:
- [ ] Future commercial product compatibility
- **Enterprise feature licensing strategy
- [ ] Community contribution protection
- [ ] Revenue model alignment

**Success Criteria**:
- [ ] License selected and approved
- [ ] Full codebase compliance
- [ ] Legal review completed
- [ ] Business strategy aligned

**Priority**: HIGH - Foundation for open source release
**Dependencies**: Legal review, business strategy finalization

---

### Epic: Researcher Workbench Workflow Enhancement
- **Issue**: #275
- **Labels**: enhancement, epic
- **Assignees**: 
- **Created**: 2025-08-02
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: Epic: Researcher Workbench Workflow Enhancement

**Full Description**:
# Epic: Researcher Workbench Workflow Enhancement

## Problem
Current workflow issues from gauntlet testing (Issue #267):
- Confusing file management with scattered control files
- No clear system for experiment iteration
- Manual file copying and path management required
- Corpus manifest buried in data folder vs control files at root

## Solution: Workbench Mental Model
Implement clean researcher workflow:
- workbench/ = iteration space
- root files = operational (what CLI runs)  
- archive/ = timestamped history
- discernus promote = workbench to operational

## Phase 1: v7.0 Workbench Foundation
- Implement basic workbench promotion workflow
- Add discernus promote command
- Update CLI validation
- Integration testing

## Phase 2: v7.1 Structure Enhancement
- Design v7.1 with root-level corpus manifest
- Update core infrastructure
- Create migration tooling
- Migrate existing experiments

## Success Criteria
- Clean mental model
- Zero file naming confusion
- Automatic versioning
- Safe iteration with rollback

---

### [EPIC] Agent Ecosystem Expansion
- **Issue**: #126
- **Labels**: enhancement, epic
- **Assignees**: 
- **Created**: 2025-07-22
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: [EPIC] Agent Ecosystem Expansion

**Full Description**:
# 🚀 Agent Ecosystem Expansion Epic

## 🎯 **OBJECTIVE**
Expand Discernus agent capabilities with specialized agents for comprehensive research workflow support, focusing on academic rigor, domain expertise, and corpus intelligence.

## 🔬 **CONTEXT**
Current agent ecosystem needs expansion to support:
- Academic validation and reproducibility standards
- Domain-specific analytical guidance  
- Intelligent corpus discovery and validation
- End-to-end research workflow automation

## 📋 **EPIC COMPONENTS**

### 🚀 **CORE AGENT DEVELOPMENT**
- [ ] **Issue #124**: ReplicationAgent - Comprehensive experiment asset validation
- [ ] **Issue #123**: DomainExpertAgent - Specialized analytical guidance
- [ ] **Issue #122**: CorpusRecommendationAgent - Intelligent corpus discovery
- [ ] **Issue #121**: CorpusValidationAgent - Automated corpus quality assessment

## 🎯 **DEVELOPMENT PRIORITIES**
1. **Priority 1**: ReplicationAgent (#124) - Critical for academic integrity
2. **Priority 2**: DomainExpertAgent (#123) - Cross-field research support
3. **Priority 3**: CorpusValidationAgent (#121) - Research foundation quality
4. **Priority 4**: CorpusRecommendationAgent (#122) - Discovery enhancement

## 📊 **SUCCESS METRICS**
- [ ] All 4 agent types integrated into WorkflowOrchestrator
- [ ] CLI commands implemented for each agent
- [ ] Academic workflow integration complete
- [ ] Agent registry updated with new capabilities
- [ ] THIN architecture principles maintained throughout

## 🔗 **DEPENDENCIES**
- **WorkflowOrchestrator**: Core integration point for all agents
- **Agent Registry**: Registration and capability discovery
- **CLI Framework**: Command-line interface expansion
- **Academic Publication Pipeline**: Integration with research workflows

## ⏱️ **TIMELINE**
- **Week 1-2**: ReplicationAgent development (highest priority)
- **Week 2-3**: DomainExpertAgent development  
- **Week 3-4**: CorpusValidationAgent development
- **Week 4-5**: CorpusRecommendationAgent development
- **Week 5-6**: Integration testing and refinement

## 🏗️ **TECHNICAL REQUIREMENTS**
- Follow THIN architecture principles
- Integrate with existing agent framework in 
- Support both CLI and WorkflowOrchestrator integration
- Generate structured reports (JSON + Markdown)
- Maintain academic publication standards
- Full provenance logging and audit trail

**Priority**: Enhancement - Foundation for advanced research workflow automation

---

### EPIC: Framework Enhancement - Rhetorical Tension Pattern Analysis
- **Issue**: #125
- **Labels**: 
- **Assignees**: 
- **Created**: 2025-07-22
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: EPIC: Framework Enhancement - Rhetorical Tension Pattern Analysis

**Full Description**:
# Framework Enhancement Epic: Rhetorical Tension Pattern Analysis

## Strategic Vision
Enhance all flagship frameworks (CFF, PDAF, etc.) with robust quantification of rhetorical tension patterns - where speakers simultaneously employ opposing dimensional appeals with significant intensity.

## Problem Statement
Current independent dimension scoring reveals rich data about complex rhetorical strategies, but we lack systematic quantification of **rhetorical tensions** - when speakers use opposing appeals (Hope/Fear, Amity/Enmity) with high intensity and similar salience.

These tension patterns appear significant but currently require manual interpretation. We need mathematical quantification to enable:
- Systematic comparison across speakers and contexts  
- Research into the strategic and psychological implications of rhetorical contradiction
- Identification of sophisticated messaging patterns vs genuine ambivalence

## Solution Architecture

### Core Enhancement: Tension Mathematics
Add tension quantification to existing frameworks using current data (no new collection required):

**Dimensional Tension Score**: For each opposing anchor pair
```
Tension Score = min(Anchor_A_score, Anchor_B_score) × |Salience_A - Salience_B|
```

**Strategic Contradiction Index (SCI)**: Overall rhetorical tension summary
```
SCI = Average of all dimensional tension scores across framework
```

**Salience Tension Patterns**: Identification of where emphasis conflicts occur most prominently

### Implementation Approach: Pure Mathematics
- **Zero Interpretation Commitment**: Framework provides measurements, not explanations
- **Research Infrastructure**: Creates foundation for future tension pattern studies  
- **Context Agnostic**: Works across all ideological positions and speaker types
- **THIN Architecture**: Math only, no intelligence assumptions

## Research Insights from Pilot Analysis

### **Validated Tension Pattern Types** (Based on 4-speech pilot analysis)

**1. Harmony Strategy** (SCI = 0.07)
- Low rhetorical tension across all dimensions
- Strategic coherence with minimal contradictions  
- Example: Democratic concession speech with consistent unity themes

**2. Strategic Coalition Building** (SCI = 0.15)  
- Moderate tension through deliberate balance management
- Threading needle between sharp critique and broad appeal
- Example: Criminal justice reform speech balancing system criticism with unity

**3. Revolutionary Coherence** (SCI = 0.25)
- High populist intensity with aligned salience patterns
- Coherent theory of change prevents strategic contradictions
- Example: Civil rights movement speech with focused revolutionary messaging

**4. Strategic Overreach** (SCI = 0.38)
- High tension from competing high-salience dimensions  
- Attempt to emphasize multiple populist appeals simultaneously
- Example: Immigration speech trying to be both populist and constitutionalist

### **Critical Discovery: Salience-Tension Interaction Effects**

**Salience Concentration vs Strategic Coherence**:
- **Narrow Focus** (1-2 high salience dimensions): Low tension, high coherence
- **Strategic Spread** (3-4 moderate salience): Manageable tension, broad appeal  
- **Shotgun Approach** (4+ high salience): High tension, strategic confusion

**The "Rhetorical Efficiency" Principle**: 
You can achieve high populist intensity OR broad populist appeal, but attempting both simultaneously creates measurable strategic contradictions.

**Predictive Framework**:
- **High Salience Concentration + Low SCI** = Coherent Revolutionary Strategy
- **Moderate Salience Distribution + Low SCI** = Sophisticated Coalition Building
- **High Salience Spread + High SCI** = Strategic Messaging Overload

## Epic Breakdown

### Phase 1: Core Mathematical Enhancement (2-3 weeks)
**Issue #1**: Implement Dimensional Tension Scoring
- Add tension calculations for all opposing anchor pairs
- Integrate with existing salience-weighted analysis  
- Generate tension scores in framework outputs

**Issue #2**: Develop Strategic Contradiction Index
- Create overall tension summary metric
- Design SCI calculation methodology
- Add to framework result schemas

**Issue #3**: Tension Pattern Classification System
- Identify common tension pattern types based on research insights
- Create descriptive taxonomy (not interpretive)
- Enable pattern recognition across analyses

### Phase 2: Framework Integration (2-3 weeks)
**Issue #4**: CFF Tension Enhancement  
- Integrate tension analysis into Cohesive Flourishing Framework
- Update v4.3 to v4.4 with tension capabilities
- Maintain backward compatibility with existing analyses

**Issue #5**: PDAF Tension Enhancement
- Integrate tension analysis into Populist Discourse Analysis Framework  
- Update v1.2 to v1.3 with tension capabilities
- Ensure cross-ideological tension measurement validity

**Issue #6**: Core Module Tension Integration
- Add tension analysis to ECF, CVF, IDF frameworks
- Ensure consistent tension methodology across Core Modules
- Update framework specifications and documentation

### Phase 3: Research Infrastructure (1-2 weeks)  
**Issue #7**: Advanced Analytics Integration
- Implement Salience Concentration Index (SCI-S) for message architecture analysis
- Add salience-tension interaction effect calculations
- Create rhetorical efficiency metrics

**Issue #8**: Documentation and Research Agenda
- Document tension calculation methodology with validated examples
- Present interpretive possibilities with empirical evidence
- Create research agenda for strategic communication studies

**Issue #9**: Validation and Testing
- Test tension calculations across diverse speech samples
- Verify mathematical consistency and stability
- Ensure tension metrics work across different languages/contexts

## Success Criteria

### Technical Requirements
- [ ] Tension calculations integrated into all flagship frameworks
- [ ] Strategic Contradiction Index available for all analyses
- [ ] Salience-tension interaction effects quantified
- [ ] Tension patterns identifiable and comparable across contexts
- [ ] Zero performance impact on existing analysis workflows

### Research Infrastructure Goals  
- [ ] Mathematical foundation ready for strategic communication research
- [ ] Validated tension pattern taxonomy with empirical examples
- [ ] Cross-framework tension comparison capabilities enabled
- [ ] Academic research questions clearly identified with supporting evidence

### User Experience Standards
- [ ] Tension data available in analysis reports with interpretive context
- [ ] Clear distinction between mathematical measurement and strategic interpretation  
- [ ] No additional complexity burden on basic framework usage
- [ ] Advanced users can access detailed tension analytics and interaction effects

## Research Applications (Evidence-Based)

### **Validated Interpretive Possibilities** (require additional research):

**Strategic Communication Architecture**:
- **Coherent Messaging** (Low SCI): Speaker has clear rhetorical theory and strategic focus
- **Coalition Building** (Moderate SCI): Deliberate tension management for broad appeal
- **Strategic Overreach** (High SCI): Competing rhetorical goals creating message confusion

**Salience-Tension Dynamics**:
- **Focused High-Salience Strategy**: Maximum coherence, narrow appeal
- **Distributed Moderate-Salience Strategy**: Balanced appeal with manageable contradictions  
- **Competing High-Salience Strategy**: Strategic confusion and audience fragmentation

### **Future Research Questions**:
- Do high-tension speakers perform differently electorally?
- Is tension correlated with audience engagement or confusion?
- Do tension patterns predict speaker authenticity ratings?
- Are certain salience distributions more effective for specific strategic goals?
- How do tension patterns vary across cultural and political contexts?

## Implementation Notes

### THIN Architecture Compliance
- **Mathematics + Evidence**: Framework provides measurements with validated examples, not speculative interpretations
- **Research Infrastructure**: Enables discoveries based on empirical patterns from pilot analysis
- **Context Neutrality**: Works across ideological and cultural boundaries with proven examples
- **Academic Standards**: Creates foundation for peer-reviewed strategic communication research

### Resource Requirements
- **Development**: 4-6 weeks total across all phases  
- **Testing**: Integration with existing framework validation suites plus tension-specific validation
- **Documentation**: Update to framework specifications and user guides with research insights
- **Zero New Data Collection**: Uses existing dimension scores and salience rankings

## Strategic Impact

This enhancement transforms frameworks from measuring **rhetorical presence** to measuring **rhetorical strategy architecture**, including quantified analysis of strategic communication coherence and contradiction patterns.

Creates research infrastructure for strategic communication studies with validated empirical foundation from pilot analysis demonstrating clear tension pattern types and salience-tension interaction effects.

**Priority**: Medium-High  
**Complexity**: Low (pure mathematics on existing data)
**Research Value**: Very High (enables new analytical capabilities with proven research foundation)
**Empirical Foundation**: Strong (validated through 4-speech pilot analysis across different strategic contexts)

---

### Add ReplicationAgent for Comprehensive Experiment Asset Validation
- **Issue**: #124
- **Labels**: epic
- **Assignees**: 
- **Created**: 2025-07-22
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: Add ReplicationAgent for Comprehensive Experiment Asset Validation

**Full Description**:
## Problem
Academic reproducibility requires comprehensive validation of all experiment assets from corpus files to frameworks to analysis prompts to results calculations to final reports. Currently, there's no systematic way to verify that all components are present, consistent, and match the reported findings.

## Solution
Create a ReplicationAgent that performs end-to-end validation of experiment assets to ensure complete reproducibility and academic integrity.

## Core Capabilities

### Asset Inventory & Validation
- **Corpus Verification**: Validate all corpus files exist, match metadata, and have correct hashes
- **Framework Compliance**: Verify framework specifications match V4 standards and are internally consistent
- **Experiment Specification**: Check V2 experiment specs are complete and executable
- **Agent Configuration**: Validate all referenced agents exist in registry with correct configurations

### Analytical Chain Validation
- **Prompt Consistency**: Verify analysis prompts match framework specifications exactly
- **Parameter Integrity**: Check all model parameters, temperature settings, and configurations
- **State Transitions**: Validate workflow state transitions follow specified paths
- **Data Flow**: Ensure data flows correctly between workflow steps without modification

### Results Verification
- **Output Completeness**: Verify all expected analysis outputs were generated
- **Calculation Accuracy**: Re-check statistical calculations and aggregations
- **Report Consistency**: Ensure final reports accurately reflect analysis results
- **Provenance Completeness**: Validate full audit trail exists from input to output

### Reproducibility Assessment
- **Environment Validation**: Check Python dependencies, model versions, API configurations
- **Deterministic Verification**: Identify non-deterministic elements that may affect replication
- **Resource Estimation**: Calculate computational requirements for replication
- **Documentation Completeness**: Ensure all steps are documented for independent replication

### Academic Standards Compliance
- **Methodological Rigor**: Check experiment design follows academic best practices
- **Statistical Validity**: Validate statistical approaches and significance testing
- **Bias Detection**: Identify potential sources of experimental bias or confounding
- **Ethical Compliance**: Verify research follows ethical guidelines for text analysis

## Technical Requirements
- Integrate with all existing core components (corpus_inspector, spec_loader, agents)
- Generate comprehensive validation reports (JSON + Markdown + Academic PDF)
- Support both CLI and WorkflowOrchestrator integration
- Follow THIN architecture principles

## Integration Points
- **CLI**: `python3 discernus_cli.py validate-replication <project_path>`
- **Agent Registry**: Available for workflow orchestration
- **Pre-Publication**: Integrated with academic publication preparation workflow
- **Audit Trail**: Full provenance logging for validation process

## Validation Report Structure
### Executive Summary
- Overall replication confidence score (0-100%)
- Critical issues requiring attention
- Recommended actions for improvement

### Asset Verification
- Corpus integrity status
- Framework compliance status  
- Experiment specification status
- Agent configuration status

### Analytical Verification
- Prompt consistency verification
- Parameter integrity status
- Calculation accuracy verification
- Output completeness status

### Reproducibility Assessment
- Environment compatibility
- Deterministic verification results
- Resource requirements estimation
- Documentation completeness score

## Success Criteria
- [ ] Detects 95% of common replication barriers automatically
- [ ] Provides actionable recommendations for reproducibility improvement
- [ ] Integrates seamlessly with existing experiment workflows
- [ ] Generates publication-ready validation reports
- [ ] Reduces peer review concerns about reproducibility by 80%

## Priority: High
Critical for academic credibility and compliance with reproducibility standards.

**Parent EPIC**: [#126 Agent Ecosystem Expansion](https://github.com/discernus/discernus/issues/126)
**Development Priority**: 1 (Critical for academic integrity)

---

### Add DomainExpertAgent for Specialized Analytical Guidance
- **Issue**: #123
- **Labels**: epic
- **Assignees**: 
- **Created**: 2025-07-22
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: Add DomainExpertAgent for Specialized Analytical Guidance

**Full Description**:
## Problem
Researchers working across different domains (political science, ethics, communication theory) lack domain-specific analytical guidance when selecting frameworks, interpreting results, or ensuring methodological rigor.

## Solution
Create a DomainExpertAgent that provides specialized analytical guidance and framework recommendations based on research domain and context.

## Core Capabilities

### Domain Expertise
- **Political Science**: Constitutional analysis, populism detection, democratic health assessment
- **Ethics**: Business ethics, moral reasoning, deontological vs consequentialist approaches
- **Communication Theory**: Framing analysis, narrative structure, persuasive techniques
- **Interdisciplinary Research**: Cross-domain framework integration and methodology

### Framework Guidance
- **Framework Selection**: Recommend optimal frameworks for specific research questions
- **Framework Compatibility**: Assess framework combinations for multi-dimensional analysis
- **Methodological Alignment**: Ensure framework choice matches research methodology
- **Historical Context**: Provide background on framework development and validation

### Analytical Intelligence
- **Result Interpretation**: Domain-specific guidance on interpreting framework outputs
- **Statistical Significance**: Help researchers understand what constitutes meaningful results in their domain
- **Methodological Validation**: Check that analytical approaches follow domain best practices
- **Academic Standards**: Ensure compliance with field-specific research standards

### Research Optimization
- **Question Refinement**: Help researchers refine research questions for maximum analytical power
- **Corpus Recommendations**: Suggest domain-appropriate text collections
- **Experimental Design**: Provide guidance on study design and controls
- **Publication Readiness**: Pre-check research for academic publication standards

## Technical Requirements
- Integrate with existing framework library in `frameworks/`
- Support all V4 Framework Specifications
- Generate domain-specific guidance reports (JSON + Markdown)
- Follow THIN architecture principles

## Integration Points
- **CLI**: `python3 discernus_cli.py expert-guidance --domain "political-science" --framework CFF --research-question "..."`
- **Agent Registry**: Available for workflow orchestration
- **Framework Selection**: Integrated with experiment design workflow

## Success Criteria
- [ ] Provides relevant domain expertise for common academic fields
- [ ] Improves framework selection accuracy by 80%
- [ ] Reduces methodological errors in cross-domain research
- [ ] Supports academic publication preparation

## Priority: Medium
Enhances academic rigor and supports researchers working outside their primary domain expertise.

**Parent EPIC**: [#126 Agent Ecosystem Expansion](https://github.com/discernus/discernus/issues/126)
**Development Priority**: 2 (Cross-field research support)

---

### Add CorpusRecommendationAgent for Intelligent Corpus Discovery
- **Issue**: #122
- **Labels**: epic
- **Assignees**: 
- **Created**: 2025-07-22
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: Add CorpusRecommendationAgent for Intelligent Corpus Discovery

**Full Description**:
## Problem
Researchers often spend significant time searching for appropriate text corpora for their studies. There's no systematic way to discover existing corpora that match research questions, analytical frameworks, or methodological needs.

## Solution
Create a CorpusRecommendationAgent that intelligently suggests relevant corpora based on research context and requirements.

## Core Capabilities

### Research Context Analysis
- **Framework Matching**: Suggest corpora proven effective with specific frameworks (CFF, PDAF, etc.)
- **Domain Alignment**: Match research questions to appropriate text domains
- **Methodological Fit**: Consider corpus size, diversity requirements, temporal scope
- **Replication Opportunities**: Identify corpora used in comparable studies

### Corpus Discovery
- **Local Repository Scanning**: Catalog available corpora in `data/` and `projects/`
- **Academic Database Integration**: Future hook for Discernus Corpus Cloud
- **Usage Analytics**: Track which corpora work well for different research types
- **Quality Scoring**: Rank recommendations by corpus validation scores

### Recommendation Engine
- **Similarity Matching**: Compare research goals to historical corpus usage
- **Gap Analysis**: Identify missing corpus types for comprehensive analysis
- **Alternative Suggestions**: Provide backup options when primary recommendations unavailable
- **Customization Options**: Filter by size, language, time period, domain

### Integration Intelligence
- **Framework Compatibility**: Warn about corpus-framework mismatches
- **Experiment Planning**: Suggest corpus combinations for comparative studies
- **Resource Estimation**: Provide analysis time/cost projections per corpus
- **Validation Precheck**: Flag potential corpus quality issues upfront

## Technical Requirements
- Integrate with CorpusValidationAgent for quality assessment
- Support V2 Corpus Specification metadata
- Generate structured recommendation reports (JSON + Markdown)
- Follow THIN architecture principles

## Integration Points
- **CLI**: `python3 discernus_cli.py recommend-corpus --research-question "..." --framework CFF`
- **Agent Registry**: Available for workflow orchestration
- **Corpus Cloud**: Future integration with shared corpus library

## Success Criteria
- [ ] Reduces corpus discovery time by 60%
- [ ] Provides relevant recommendations for common research domains
- [ ] Integrates with existing corpus validation pipeline
- [ ] Supports both local and future cloud corpus libraries

## Priority: Medium
Foundational capability for Discernus Corpus Cloud and improved researcher experience.

**Parent EPIC**: [#126 Agent Ecosystem Expansion](https://github.com/discernus/discernus/issues/126)  
**Development Priority**: 4 (Discovery enhancement)

---

### Add CorpusValidationAgent for Automated Corpus Quality Assessment
- **Issue**: #121
- **Labels**: epic
- **Assignees**: 
- **Created**: 2025-07-22
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: Add CorpusValidationAgent for Automated Corpus Quality Assessment

**Full Description**:
## Problem
Corpus preparation currently requires manual validation of text quality, metadata consistency, and potential biases. Researchers spend significant time on corpus hygiene before analysis can begin.

## Solution
Create a CorpusValidationAgent that automatically assesses corpus quality and provides actionable recommendations.

## Core Capabilities

### Quality Assessment
- **Text Quality**: Encoding issues, malformed content, empty files
- **Metadata Validation**: Required fields, consistent formatting, valid values
- **Statistical Overview**: File count, size distribution, text length patterns
- **Content Consistency**: Language detection, formatting standardization

### Bias Detection
- **Source Bias**: Over-representation of specific authors, publications, time periods
- **Content Bias**: Keyword frequency analysis, sentiment skews
- **Sampling Bias**: Geographic, demographic, or ideological imbalances
- **Temporal Bias**: Time period clustering, historical context gaps

### Validation Reports
- **Quality Score**: Overall corpus fitness for analysis
- **Issue Flagging**: Critical problems requiring attention
- **Recommendations**: Specific improvement suggestions
- **Compliance Check**: V2 Corpus Specification adherence

## Technical Requirements
- Integrate with existing `corpus_inspector.py` functionality
- Generate structured validation reports (JSON + Markdown)
- Support all corpus formats (txt, md, with manifest.yaml)
- Follow THIN architecture principles

## Integration Points
- **CLI**: `python3 discernus_cli.py validate-corpus <corpus_dir>`
- **Agent Registry**: Available for workflow orchestration
- **Provenance**: Log validation results with timestamps

## Success Criteria
- [ ] Detects common corpus quality issues automatically
- [ ] Provides actionable improvement recommendations  
- [ ] Generates academic-quality validation reports
- [ ] Reduces manual corpus preparation time by 70%

## Priority: Medium
Part of broader corpus intelligence capabilities supporting Discernus Corpus Cloud vision.

**Parent EPIC**: [#126 Agent Ecosystem Expansion](https://github.com/discernus/discernus/issues/126)
**Development Priority**: 3 (Research foundation quality)

---

### Epic: Extension Architecture & Academic Tools
- **Issue**: #16
- **Labels**: enhancement, epic
- **Assignees**: 
- **Created**: 2025-07-19
- **Updated**: 2025-08-11
- **Milestone**: Strategic Planning & Architecture
- **Description**: Epic: Extension Architecture & Academic Tools

**Full Description**:
## Overview
This epic tracks the development of the extension system and academic-focused tools, starting with the knowledgenaut literature review agent.

## Key Extension Opportunities
- Knowledgenaut agent as first reference extension
- Extension architecture governance model needs implementation
- Health check system for environment validation
- Academic workflow enhancements

## Child Issues
This epic will contain issues for:
- [ ] Knowledgenaut extension implementation
- [ ] Extension architecture documentation and tooling
- [ ] Health check system restoration
- [ ] Academic workflow optimization
- [ ] Extension marketplace planning

## Success Criteria
- [ ] First extension (knowledgenaut) successfully implemented
- [ ] Extension development process documented
- [ ] Health checks validate environment before analysis
- [ ] Clear governance model for extension approval

## Priority
Medium - important for long-term platform growth and academic adoption

---

