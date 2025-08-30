# Van der Veen Presidential Campaign Replication Study

## 🎯 **Project Overview**

This dedicated project replicates the presidential campaign portion of Van der Veen et al. (2024) "Classifying populist language in American presidents" using the PDAF v10.0 framework instead of their original methodology.

## ✅ **Experiment Status: COMPLETED**

**Run ID**: 20250830T054450Z  
**Status**: Successfully completed  
**Results**: All primary hypotheses confirmed, PDAF v10.0 framework validated on 57 presidential speeches  
**Summary**: The experiment successfully replicated van der Veen et al. (2024) methodology using PDAF v10.0, confirming significant differences in populist rhetoric across candidates (ANOVA, p < .05). Trump (M = 0.84) and Sanders (M = 0.81) scored highest on populism, with Republicans higher on Nationalist Exclusion and Democrats higher on Economic Populist Appeals. Full results available in `runs/20250830T054450Z/results/final_report.md`.

## 📊 **Strategic Rationale**

### **Why This Approach?**
- **✅ Focused Scope**: Uses existing, validated data instead of massive corpus expansion
- **✅ Immediate Results**: Concrete PDAF validation within 3 days
- **✅ Methodological Clarity**: Direct comparison between frameworks
- **✅ Risk Reduction**: No data collection challenges or quality concerns
- **✅ Research Value**: Establishes PDAF credibility on established populism data

### **Three-Phase Strategy**
| **Phase 1 (Completed)** | **Phase 2 (In Progress)** | **Phase 3 (Planned)** |
|------------------------|---------------------------|----------------------|
| 57 speeches (2016) | 200+ speeches (2008-2024) | Multi-framework analysis |
| PDAF v10.0 only | PDAF v10.0 validation | CFF + MFT + Lakoff Framing |
| Framework validation | Corpus expansion | Cross-framework comparison |
| 3-day execution | 2-week timeline | 2-week timeline |

*For detailed project planning and current status, see `/pm/vanderveen_replication_extension/vdv_pm/`*

## 📁 **Project Structure**

```
projects/vanderveen_presidential_pdaf/
├── 📋 experiment.md              # Study design and methodology
├── 📄 corpus.md                  # Data source documentation
├── 🔧 pdaf_v10.md               # Framework specification (inherited)
├── 📊 corpus/                   # Converted speech files
│   ├── manifest.json           # Speech metadata and statistics
│   └── *.txt                   # Individual speech files (57 total)
├── 📈 runs/                    # PDAF analysis results
│   └── 20250830T054450Z/      # Completed experiment run
│       └── results/            # Analysis outputs and reports
├── 📜 scripts/                 # Processing and analysis scripts
│   └── convert_docx_to_text.py # DOCX to text conversion
└── 📚 docs/                    # Analysis reports and findings
```

## 🚀 **Execution Plan**

### **Phase 1: Initial Experiment (COMPLETED)**
1. **Data Processing**: Convert and validate 57 presidential speeches
2. **PDAF Analysis**: Execute PDAF v10.0 on full corpus
3. **Results Generation**: Statistical analysis and hypothesis testing
4. **Framework Validation**: Confirm PDAF performance on presidential discourse

### **Additional Runs (Planned)**
- **Refinement Runs**: Additional experiment executions with tweaked experiment parameters and corpus metadata to refine the analytical approach
- **Validation Runs**: Cross-validation of results and framework performance
- **Extension Runs**: Preparation for Phase 2 corpus expansion

## 📊 **Data Overview**

### **Source Material**
- **Study**: Van der Veen et al. (2024) "Classifying populist language in American presidents"
- **Corpus**: 57 speeches from 6 major 2016 presidential candidates
- **Format**: Plain text files with standardized metadata
- **Date Range**: June 16, 2015 - November 8, 2016

### **Key Candidates**
- **Trump** (n=22): Republican nominee, outsider candidate
- **Clinton** (n=21): Democratic nominee, establishment candidate
- **Sanders** (n=5): Democratic primary challenger, progressive populist
- **Cruz** (n=3): Republican primary challenger, conservative populist
- **Rubio** (n=4): Republican establishment candidate
- **Kasich** (n=2): Republican moderate, baseline reference

### **Processing Requirements**
- **Input**: Standardized text files with metadata
- **Output**: PDAF analysis results with statistical validation
- **Metadata**: Dates, titles, word counts, context, candidate type
- **Quality**: Validated transcription and consistent formatting

## 🔬 **PDAF Analysis Scope**

### **Framework Application**
- **9 Core Dimensions**: All PDAF v10.0 dimensions applicable
- **Salience Weighting**: Rhetorical prominence analysis
- **Strategic Tension**: Internal contradiction detection (PSCI calculation)
- **Context**: 2016 presidential campaign rhetoric

### **Key Insights Achieved**
- **Candidate Differentiation**: Clear populism patterns identified across candidates
- **Partisan Patterns**: Republicans higher on Nationalist Exclusion, Democrats on Economic Populist Appeals
- **Strategic Analysis**: Strategic tension analysis reveals rhetorical sophistication
- **Framework Validation**: PDAF successfully discriminates between candidate types

## 📈 **Success Metrics**

### **Technical Success** ✅ **ACHIEVED**
- ✅ All 57 speeches successfully processed and analyzed
- ✅ PDAF analysis completed without errors
- ✅ Results format suitable for research dissemination
- ✅ Processing time under 2 hours total

### **Research Success** ✅ **ACHIEVED**
- ✅ Clear populism patterns identified across campaign
- ✅ All primary hypotheses confirmed with statistical significance
- ✅ Strategic tension analysis reveals rhetorical dynamics
- ✅ Results provide basis for framework validation and Phase 2 expansion

## 🔗 **Integration Points**

### **Related Projects**
- **Main Trump Project**: `/projects/2d_trump_populism/` (PDAF framework source)
- **Project Management**: `/pm/vanderveen_replication_extension/vdv_pm/` (current planning)
- **Analysis Tools**: `/corpus/tools/` (processing utilities)

### **Dependencies**
- **Python Environment**: Compatible with PDAF v10.0
- **File Access**: Read access to source directory, write access to output
- **Framework**: PDAF v10.0 specification and analysis pipeline

## ⚠️ **Prerequisites**

### **System Requirements**
```bash
# PDAF v10.0 environment already configured
# Analysis pipeline functional and validated
```

### **Data Access**
- ✅ Source speeches available and processed
- ✅ Write access to output directories
- ✅ Sufficient disk space for analysis results

### **Framework Readiness**
- ✅ PDAF v10.0 specification available
- ✅ Analysis pipeline functional and tested
- ✅ Output validation procedures established

## 📋 **Quick Start Guide**

### **1. Review Completed Results**
```bash
cd projects/vanderveen_presidential_pdaf
cat runs/20250830T054450Z/results/final_report.md
```

### **2. Examine Statistical Results**
```bash
cat runs/20250830T054450Z/results/statistical_results.json
```

### **3. Access Analysis Artifacts**
```bash
ls runs/20250830T054450Z/results/  # View all outputs
ls runs/20250830T054450Z/results/corpus/  # Access source documents
```

### **4. Prepare for Additional Runs**
```bash
# Modify experiment.md for parameter tweaks
# Update corpus.md for metadata refinements
# Execute new experiment runs as needed
```

## 🎯 **Next Steps**

### **Immediate Actions**
1. **Review completed results** from Run 20250830T054450Z
2. **Plan refinement runs** with tweaked parameters and metadata
3. **Prepare for Phase 2** corpus expansion (200+ speeches)
4. **Execute additional validation runs** to refine analytical approach

### **Phase 2 Preparation**
1. **Corpus expansion planning** for 2008-2024 election cycles
2. **PDAF validation** on expanded corpus
3. **Longitudinal analysis** preparation across election cycles
4. **Phase 3 transition** planning for multi-framework analysis

---

**Project Status**: **PHASE 1 COMPLETED** ✅  
**Next Phase**: **CORPUS EXTENSION** 🎯  
**Estimated Duration**: Phase 2 (2 weeks), Phase 3 (2 weeks)  
**Success Probability**: High (Phase 1 validated, clear path forward)  
**Impact**: Framework validation + methodological insights + Phase 2/3 foundation
