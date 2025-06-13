# Project Backlog - Unscheduled Items
*Created: June 13, 2025 | Updated: June 13, 2025 Evening*

## **Purpose**
Items discovered or decided but not yet prioritized for current iteration. Gets reviewed during iteration planning.

## **📋 STATUS NOTE** (June 13, 2025 Evening)
**Current iteration (June 13-14) COMPLETED with outstanding success** - All major deliverables achieved:
- ✅ QA-enhanced academic pipeline fully operational
- ✅ Declarative experiment execution engine operational (100% success rate)
- ✅ Critical narrative position calculation issue resolved
- ✅ Complete academic output generation with quality assurance

**Next iteration planning** (June 17, 2025) should focus on leveraging these newly operational capabilities.

---

## 🎯 **Dynamic Scaling Enhancement** (High Priority)
*Reference: `docs/development/planning/strategic/dynamic_scaling.md`*

**Strategic Justification**: Current fixed 0.8 scaling factor "mutes differences" and "wastes visual space" - dynamic runtime scaling will maximize visual clarity and analytical precision while preserving mathematical relationships.

- [ ] **Platform Implementation: Dynamic Scaling Algorithm** - Implement runtime scaling factor calculation (min(1, 1/max_observed_distance)) in visualization engine (discovered: June 13, priority: HIGH)
  - Replace fixed 0.8 scaling with dynamic calculation based on actual narrative positions
  - Add scaling factor logging for transparency and reproducibility
  - Ensure compatibility with both circular and elliptical coordinate systems
  - Implement configurable margin (e.g., 0.99 factor) to prevent boundary artifacts
  
- [ ] **Paper Update: Dynamic Scaling Documentation** - Update academic paper v1.3.0 to reflect dynamic scaling methodology (discovered: June 13, priority: MEDIUM)
  - Replace references to fixed 0.8 scaling factor with dynamic scaling description
  - Add mathematical formulation for runtime scaling calculation
  - Document benefits: maximized visual space, preserved analytical clarity, adaptability
  - Update methodology section with implementation details and transparency requirements

- [ ] **Framework Updates: Database and Filesystem** - Update all 5 frameworks to support dynamic scaling parameters (discovered: June 13, priority: MEDIUM)
  - Add scaling configuration options to framework.json specifications
  - Update database framework records with dynamic scaling metadata
  - Ensure backward compatibility with existing fixed scaling configurations
  - Migrate civic_virtue, political_spectrum, fukuyama_identity, mft_persuasive_force, moral_rhetorical_posture

- [ ] **Quality Assurance Integration** - Integrate dynamic scaling validation into 6-layer QA system (discovered: June 13, priority: MEDIUM)
  - Add scaling factor validation (reasonable bounds, no extreme distortion)
  - Include scaling transparency in quality reports
  - Flag potential issues with over-scaling or under-utilization of visual space

## 🔧 **Infrastructure & Performance**

- [ ] **Performance Benchmarking** - Measure visualization generation speed improvements (discovered: June 13, priority: TBD)
- [ ] **Theme Expansion** - Additional academic themes (journal-specific, conference-specific) (discovered: June 13, priority: TBD)
- [ ] **Export Format Enhancement** - Additional academic formats (EPS, TIFF for specific journals) (discovered: June 13, priority: TBD)
- [ ] **Interactive Feature Enhancement** - Advanced hover info, annotation capabilities (discovered: June 13, priority: TBD)
- [ ] **Framework-Specific Styling** - Custom styling overrides for different framework types (discovered: June 13, priority: TBD)

## 📊 **Testing & Validation**

- [ ] **Unit Testing Framework** - CLI component tests, database integration tests (discovered: June 13, priority: TBD)
- [ ] **Integration Testing Suite** - Cross-component compatibility tests (discovered: June 13, priority: TBD)
- [ ] **Academic Standard Compliance Tests** - Ensure outputs meet publication requirements (discovered: June 13, priority: TBD)
- [ ] **Statistical Accuracy Validation** - Verify calculations against known benchmarks (discovered: June 13, priority: TBD)
- [ ] **Enhanced Replication Package Tests** - Include quality metadata validation (discovered: June 13, priority: TBD)

## 📈 **Academic & Research Enhancements**

- [ ] **R Script Generators** - Cursor-assisted R code for advanced visualization and statistical modeling (discovered: June 13, priority: TBD)
- [ ] **Stata Integration Scripts** - PyStata workflows for publication-grade statistical analysis (discovered: June 13, priority: TBD)
- [ ] **Enhanced Bibliography Management** - Automated citation and reference management (discovered: June 13, priority: TBD)
- [ ] **Cross-Tool Workflow Orchestrator** - Seamless integration between Jupyter, R, and Stata (discovered: June 13, priority: TBD)

## 🎯 **User Experience & Research Process**

- [ ] **Circle Math in Paper Audit** - Ensure mathematical accuracy and academic rigor in paper v1.2.0 (discovered: June 13, priority: TBD)
- [ ] **User Persona, Story, and Journey Audit** - Validate user experience design against actual research workflows (discovered: June 13, priority: TBD)
- [ ] **YouTube Ingestion Accuracy Comparison** - Test case: Trump Joint Session Speech analysis accuracy validation (discovered: June 13, priority: TBD)
- [ ] **Visualization Source of Truth vs Repository Architecture** - Establish clear architecture for visualization code and assets (discovered: June 13, priority: TBD)
- [ ] **Experiment Design Process** - Formalize systematic approach to framework development and validation (discovered: June 13, priority: TBD)

## 🏗️ **Architecture & Best Practices**

- [ ] **Framework Development Best Practices** - Systematize framework development methodology based on 5 operational frameworks (discovered: June 13, priority: TBD)
- [ ] **Architecture Refinement** - Improve architecture based on lessons learned from migrations (discovered: June 13, priority: TBD)
- [ ] **Component Quality Validators** - Automated checks for prompt clarity, framework coherence (discovered: June 13, priority: TBD)
- [ ] **Development Analytics Dashboard** - Progress tracking and pattern recognition across sessions (discovered: June 13, priority: TBD)

## 📋 **Documentation & Training**

- [ ] **Technical Documentation Updates** - API documentation, database schema docs (discovered: June 13, priority: TBD)
- [ ] **Process Documentation** - Research workflow guides, quality assurance manuals (discovered: June 13, priority: TBD)
- [ ] **Training Materials** - Best practices compendium, troubleshooting guides (discovered: June 13, priority: TBD)

---

## **Review Process**
- **Weekly Review**: During iteration planning, items move from BACKLOG → CURRENT_ITERATION
- **Priority Assignment**: Items get priority levels (HIGH/MEDIUM/LOW) when moved to current iteration
- **Archive**: Completed items move to CHANGELOG.md

**Next Review**: June 17, 2025 (next iteration planning)

## **🎯 Recent Additions** (June 13, 2025 Evening)
- **Dynamic Scaling Enhancement**: High-priority enhancement based on strategic analysis in `dynamic_scaling.md`
  - Platform implementation (HIGH priority)
  - Paper documentation updates (MEDIUM priority) 
  - Framework database/filesystem updates (MEDIUM priority)
  - QA system integration (MEDIUM priority)
- **Strategic Impact**: Will maximize visual clarity and analytical precision while preserving mathematical relationships 