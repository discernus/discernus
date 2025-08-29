# Inbox - Raw Backlog Items

**Purpose**: Raw capture of backlog items without organization or sprint planning. Items here will be groomed into organized sprints later.

**Usage**: 
- "inbox this" → append new items here with minimal formatting
- "groom our sprints" → move all items from here to sprints.md with proper organization

---

## [RAG-001] RAG Index Not Available Error
- Experiment fails with "RAG index not available - cannot proceed to evidence retrieval"
- Occurs after statistical analysis completes successfully
- Need to investigate why RAG index isn't being built or found

## [STATS-001] Statistical Agent Looking for corpus_manifest.csv
- Generated functions look for corpus_manifest.csv instead of corpus.md
- This is odd - need to check prompting or code generation

## [THIN-001] Statistical Functions Not Being Generated After THIN Refactor
- **Error**: `[Errno 2] No such file or directory: 'automatedstatisticalanalysisagent_functions.py'`
- **Context**: After eliminating corpus.md parsing antipatterns, statistical agent fails completely
- **Root Cause Analysis**:
  1. **Prompt confusion**: LLM may be confused by new THIN instructions vs old parsing expectations
  2. **Missing delimiter usage**: LLM not wrapping functions in `<<<DISCERNUS_FUNCTION_START>>>` delimiters
  3. **Incomplete mapping guidance**: LLM needs clearer examples of direct document-to-metadata mapping
  4. **Context overload**: Too much corpus manifest content may be overwhelming the prompt

## [THIN-002] THIN Architecture Progress Made
- ✅ Eliminated corpus.md file copying to workspace (orchestrator lines 918-920, 1211-1213)
- ✅ Updated prompt to pass corpus manifest as context instead of file to parse
- ✅ Removed instructions for LLM to generate YAML parsing code
- ✅ Added direct mapping instructions in prompt.yaml
- ✅ Cache cleared to force regeneration with new approach

## [THIN-003] Core Architecture Philosophy Validated
- The THIN insight is correct: LLMs should understand relationships directly, not generate parsing code
- Instead of: `manifest = yaml.safe_load(...); df = pd.merge(data, manifest_df, ...)`
- Want: `administration_map = {'doc1': 'Bush H.W.', 'doc2': 'Clinton'}; data['admin'] = data['doc_name'].map(administration_map)`
- Implementation needs refinement to guide LLM properly

## [DEBUG-001] Next Steps for Statistical Agent Debug
1. Check what LLM is actually producing vs expected delimiters
2. Provide concrete mapping example in prompt
3. Test with minimal corpus to isolate context issues
4. Ensure fallback statistical function generation works
5. Validate delimiter extraction logic still functions

## 2025-08-28 - Cost Summary Report Generation
- **Task:** Generate a final cost summary report markdown file based on log data and place it in the results folder alongside final_report.md
- **Status:** Ready for implementation
- **Details:** 
  - Create simple 10-line cost summary from costs.jsonl logs
  - Include basic metrics: total cost, tokens, documents, model, agent, operation
  - Keep it concise and factual without optimization insights
  - Place in results directory for experiment transparency
- **Files Created:** `cost_summary_report.md` template in current session

## 2025-08-28 - Informational Appendix Implementation  
- **Task:** Investigate appending informational appendix section to final reports including Final Summary, Methodology Summary, and About Discernus
- **Status:** Ready for implementation
- **Details:**
  - Create generic boilerplate sections for all experiments (not custom)
  - Final Summary: Generic description of computational discourse analysis approach
  - Methodology Summary: Generic boilerplate about Discernus methodology and validation
  - About Discernus: Generic description of what Discernus is and core capabilities
  - Keep each section to 2-3 sentences maximum
- **Files Created:** `informational_appendix.md` template in current session

## [ALPHA-015] Strategy for 'But It Works on My Machine' Problem - CRITICAL FOR ALPHA
- **Issue**: #421
- **Labels**: epic, alpha-critical
- **Milestone**: Strategic Planning & Architecture
- **Status**: Not implemented
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 13

**Description**: Eliminate environment-specific issues that prevent reproducible research by implementing containerization, dependency pinning, environment validation, and configuration management.

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

**Definition of Done**:
- [ ] Environment validation system implemented
- [ ] Dependency pinning completed
- [ ] Basic containerization working
- [ ] Setup instructions documented for all platforms

---

## [ALPHA-016] GitHub Strategy: Clean Separation of Development vs Open Source Code - CRITICAL FOR ALPHA
- **Issue**: #420
- **Labels**: epic, alpha-critical
- **Milestone**: Strategic Planning & Architecture
- **Status**: Not implemented
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 8

**Description**: Establish strategy for cleanly separating internal development code from open source version to enable professional open source release while protecting internal IP.

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

**Definition of Done**:
- [ ] Codebase audit completed
- [ ] Internal development structure established
- [ ] Feature flags implemented for internal features
- [ ] Open source version ready for release

---

## [ALPHA-017] Project Open Source License Dependencies and Business Strategy Alignment - CRITICAL FOR ALPHA
- **Issue**: #419
- **Labels**: epic, legal, dependencies, alpha-critical
- **Milestone**: Strategic Planning & Architecture
- **Status**: Not implemented
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 5

**Description**: Ensure all project dependencies are license-compatible with our business strategy by conducting complete dependency license audit and conflict resolution.

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

**Definition of Done**:
- [ ] Complete dependency license audit completed
- [ ] License compatibility matrix created
- [ ] All conflicts resolved or alternatives identified
- [ ] Business strategy alignment confirmed

---

## [ALPHA-018] Open Source License Selection and Implementation - CRITICAL FOR ALPHA
- **Issue**: #418
- **Labels**: epic, legal, alpha-critical
- **Milestone**: Strategic Planning & Architecture
- **Status**: Not implemented
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 5

**Description**: Select and implement appropriate open source license for Discernus to balance open source adoption with business strategy and enable community contribution.

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
- [ ] Enterprise feature licensing strategy
- [ ] Community contribution protection
- [ ] Revenue model alignment

**Success Criteria**:
- [ ] License selected and approved
- [ ] Full codebase compliance
- [ ] Legal review completed
- [ ] Business strategy aligned

**Definition of Done**:
- [ ] License selected and approved by stakeholders
- [ ] License implemented across full codebase
- [ ] Legal review completed
- [ ] License documentation and notices in place- [PROVENANCE-001] Add model information to final reports for provenance tracking - user shouldn't need to consult logs to know which models were used for analysis/synthesis

## [THIN-004] Audit All Agents for YAML Parsing Antipatterns - IMMEDIATE
- **Task**: Comprehensive audit of all agents to identify and eliminate YAML parsing code
- **Status**: Ready for implementation
- **Priority**: HIGH - YAML parsing violates THIN architecture principles
- **Context**: Recent testing on Sprint 2 (analysis variance reduction) revealed multiple YAML parsing issues that are THICK antipatterns
- **Rationale**: YAML parsing adds unnecessary complexity and violates the project's THIN architecture principle of direct LLM consumption
- **Scope**: 
  - Audit all agent files in `discernus/agents/` directory
  - Identify any YAML parsing code (yaml.safe_load, yaml.load, PyYAML imports)
  - Convert to direct YAML file delivery to LLM with no parsing
  - Ensure agents consume YAML content directly as text
- **Acceptance Criteria**:
  - [ ] All YAML parsing code identified and documented
  - [ ] All agents converted to consume YAML files directly as text
  - [ ] No yaml.safe_load, yaml.load, or PyYAML imports in agent code
  - [ ] LLMs receive YAML content directly without preprocessing
  - [ ] System maintains functionality while eliminating parsing complexity
- **Effort**: 2-3 hours
- **Dependencies**: None
- **Impact**: Eliminates THICK antipatterns, improves system reliability, maintains THIN architecture principles
[ARCH-001] Refactor all agents to use plain text prompts (.txt) instead of parsed YAML prompts (.yaml) to align with THIN principles and prevent template parsing errors.
