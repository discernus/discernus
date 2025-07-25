# Reference Framework Validation Suite
## Issue #68: Framework Validation Test Suite for Release Confidence

**Status**: 🚧 **In Development** (Issue #68 Implementation)  
**Purpose**: Validate functionality of all 4 reference frameworks before 1.0 release  
**Framework Coverage**: ECF v1.0, CAF v4.1-4.2, CHF v1.0-1.1, CFF v4.2-4.3

---

## Project Overview

This project implements **Issue #68: Framework Validation: Reference Framework Test Suite** by creating comprehensive validation experiments for all reference frameworks using a proven corpus and systematic testing methodology.

### Success Criteria (from Issue #68)
- [x] Minimal test corpus created for each reference framework
- [ ] Experiment specifications written for each framework  
- [ ] Validation experiments successfully executed
- [ ] Expected outputs documented and success criteria defined
- [ ] Automated testing framework established

---

## Unified Validation Strategy

### Core Approach
**Reuse Proven Foundation**: Leverage the successful `projects/soar_2_cff_poc/` validation pattern for all 4 reference frameworks using the same high-quality 8-speech corpus.

**Framework-Agnostic Design**: Each framework validation uses identical corpus and experiment structure, differing only in framework specifications and expected outputs.

### Test Corpus (8 Speeches)
**Source**: Proven political discourse collection from CFF validation project
- **Conservative Dignity**: McCain 2008 Concession, Romney 2020 Impeachment  
- **Progressive Dignity**: Booker 2018 First Step Act, Lewis 1963 March Washington
- **Conservative Tribalism**: King 2017 House, Vance National Conservative Conference
- **Progressive Tribalism**: AOC 2025 Fighting Oligarchy, Sanders 2025 Fighting Oligarchy

**Coverage**: 62-year timespan (1963-2025), ideological diversity, rhetorical variety

---

## Framework Validation Projects

### ✅ CFF v4.3 - Cohesive Flourishing Framework
**Status**: **Complete** (existing project: `projects/soar_2_cff_poc/`)
- **Dimensions**: 5 axes + Cohesion Index
- **Expected Patterns**: Dignity > Tribalism on cohesion metrics
- **Validation**: Proven end-to-end execution

### 🔄 ECF v1.0 - Emotional Climate Framework  
**Status**: **In Development**
- **Dimensions**: 6 emotional dimensions (Fear, Hope, Enmity, Amity, Envy, Compersion)
- **Expected Patterns**: Clear emotional climate differentiation across speech types
- **Location**: `ecf_validation/`

### 🔄 CAF v4.1-4.2 - Character Assessment Framework
**Status**: **In Development** 
- **Dimensions**: 10 character dimensions with identity foundation
- **Expected Patterns**: Dignity speeches show higher virtue scores
- **Location**: `caf_validation/`

### 🔄 CHF v1.0-1.1 - Constitutional Health Framework  
**Status**: **In Development**
- **Dimensions**: 3 constitutional dimensions (Procedural, Institutional, Systemic)
- **Expected Patterns**: Dignity speeches support constitutional health
- **Location**: `chf_validation/`

---

## Project Structure

```
projects/reference_framework_validation/
├── README.md                           # This file
├── corpus/                             # Shared 8-speech corpus 
│   ├── manifest.yaml
│   ├── conservative_dignity_mccain_2008_concession.txt
│   ├── conservative_dignity_romney_2020_impeachment.txt
│   ├── progressive_dignity_booker_2018_first_step_act.txt
│   ├── progressive_dignity_lewis_1963_march_washington.txt
│   ├── conservative_tribalism_king_2017_house.txt
│   ├── conservative_tribalism_vance_nat_con.txt
│   ├── progressive_tribalism_aoc_2025_fighting_oligarchy.txt
│   └── progressive_tribalism_sanders_2025_fighting_oligarchy.txt
├── ecf_validation/                     # ECF validation experiment
│   ├── experiment.md                   # ECF validation methodology (→ frameworks/reference/core/ecf_v1.0_refined.md)
│   └── results/                        # Generated results
├── caf_validation/                     # CAF validation experiment
│   ├── experiment.md                   # CAF validation methodology (→ frameworks/reference/core/caf_v4.1_enhanced.md)
│   └── results/                        # Generated results
├── chf_validation/                     # CHF validation experiment
│   ├── experiment.md                   # CHF validation methodology (→ frameworks/reference/core/chf_v1.0_bagehot.md)
│   └── results/                        # Generated results
├── automated_testing/                  # Automated validation infrastructure
│   ├── run_all_validations.py         # Execute all framework validations
│   ├── validation_test_suite.py       # Automated success criteria checking
│   └── reference_framework_tests.py   # Unit tests for framework validation
└── validation_results/                 # Consolidated results and analysis
    ├── framework_comparison_analysis.md
    ├── success_criteria_verification.md
    └── release_confidence_report.md
```

**Key Architecture Decision**: Each validation experiment **references** the existing production frameworks in `frameworks/reference/` rather than duplicating them. This maintains single-source-of-truth and ensures we're testing the actual frameworks that will be used in production.

---

## Implementation Plan

### Phase 1: Project Setup (Current)
- [x] Create unified project structure
- [ ] Set up shared corpus (symlink to proven CFF corpus)
- [ ] Create framework validation templates

### Phase 2: Framework Validations 
- [ ] Create ECF validation experiment
- [ ] Create CAF validation experiment  
- [ ] Create CHF validation experiment

### Phase 3: Execution & Testing
- [ ] Execute all framework validations
- [ ] Collect results and verify success criteria
- [ ] Create automated testing infrastructure

### Phase 4: Documentation & Release Confidence
- [ ] Document expected outputs and success criteria
- [ ] Generate framework comparison analysis
- [ ] Complete release confidence report

---

## Usage

### Validate Individual Framework
```bash
# ECF validation
python3 discernus_cli.py execute projects/reference_framework_validation/ecf_validation

# CAF validation  
python3 discernus_cli.py execute projects/reference_framework_validation/caf_validation

# CHF validation
python3 discernus_cli.py execute projects/reference_framework_validation/chf_validation
```

### Run All Validations
```bash
# Automated execution of all validations
python3 projects/reference_framework_validation/automated_testing/run_all_validations.py

# Run validation test suite
python3 -m unittest projects.reference_framework_validation.automated_testing.reference_framework_tests
```

---

## Success Criteria

### Functional Validation
- [x] **Minimal Test Corpus**: 8-speech corpus proven in CFF validation
- [ ] **Experiment Specifications**: ECF, CAF, CHF experiments written and validated
- [ ] **Validation Execution**: All frameworks execute successfully end-to-end
- [ ] **Expected Outputs**: Gold standard results documented for each framework

### Technical Validation  
- [ ] **Framework Agnosticism**: All validations use identical corpus and methodology
- [ ] **Automated Testing**: Test suite validates success criteria automatically
- [ ] **Release Confidence**: Documentation confirms frameworks ready for 1.0 release

### Quality Assurance
- [ ] **Consistent Results**: Framework outputs align with theoretical expectations
- [ ] **Error Handling**: Robust validation handles edge cases gracefully  
- [ ] **Documentation**: Complete validation documentation for future maintenance

---

## Integration with Issue #68

This project directly implements **Issue #68: Framework Validation: Reference Framework Test Suite**:

- **Addresses Epic Goals**: Tests all 4 reference frameworks systematically
- **Leverages Existing Assets**: Builds on proven CFF validation foundation
- **Release-Focused**: Provides confidence for 1.0 release decision-making
- **Framework-Agnostic**: Validates universal functionality across framework types

**Expected Completion**: 2-3 days for full implementation and validation execution 