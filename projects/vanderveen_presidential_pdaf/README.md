# Van der Veen Presidential Campaign Replication Study

## 🎯 **Project Overview**

This dedicated project replicates the presidential campaign portion of Van der Veen et al. (2024) "Classifying populist language in American presidents" using the PDAF v10.0 framework instead of their original methodology.

## 📊 **Strategic Rationale**

### **Why This Approach?**
- **✅ Focused Scope**: Uses existing, validated data instead of massive corpus expansion
- **✅ Immediate Results**: Concrete PDAF validation within 3 days
- **✅ Methodological Clarity**: Direct comparison between frameworks
- **✅ Risk Reduction**: No data collection challenges or quality concerns
- **✅ Research Value**: Establishes PDAF credibility on established populism data

### **Phase 1 vs. Phase 2 Strategy**
| **Phase 1 (Current)** | **Phase 2 (Future)** |
|----------------------|---------------------|
| 23 existing speeches | 180+ expanded corpus |
| Established data quality | New data collection |
| Framework validation | Longitudinal analysis |
| 3-day execution | 6-8 week timeline |
| Low risk, high certainty | Higher risk, broader scope |

## 📁 **Project Structure**

```
projects/vanderveen_presidential_pdaf/
├── 📋 experiment.md              # Study design and methodology
├── 📄 corpus.md                  # Data source documentation
├── 🔧 pdaf_v10.md               # Framework specification (inherited)
├── 📊 corpus/                   # Converted speech files
│   ├── manifest.json           # Speech metadata and statistics
│   └── *.txt                   # Individual speech files (23 total)
├── 📈 runs/                    # PDAF analysis results
├── 📜 scripts/                 # Processing and analysis scripts
│   └── convert_docx_to_text.py # DOCX to text conversion
└── 📚 docs/                    # Analysis reports and findings
```

## 🚀 **Execution Plan**

### **Day 1: Data Processing**
1. **Convert DOCX files** to plain text using `scripts/convert_docx_to_text.py`
2. **Create manifest.json** with speech metadata
3. **Validate conversion quality** and text formatting
4. **Prepare PDAF analysis input** files

### **Day 2: PDAF Analysis**
1. **Execute PDAF v10.0** on all 23 speeches
2. **Generate dimension scores** and salience ratings
3. **Calculate strategic tension** metrics
4. **Create per-speech analysis** reports

### **Day 3: Results & Insights**
1. **Aggregate campaign trajectory** analysis
2. **Compare with original study** methodology
3. **Document methodological insights** and PDAF advantages
4. **Generate research findings** report

## 📊 **Data Overview**

### **Source Material**
- **Study**: Van der Veen et al. (2024) "Classifying populist language in American presidents"
- **Speaker**: Donald Trump
- **Context**: 2016 Republican presidential nomination campaign
- **Format**: 23 Microsoft Word documents (.docx)
- **Date Range**: June 16, 2015 - November 8, 2016

### **Key Speeches**
- **Campaign Announcement** (June 16, 2015)
- **RNC Acceptance Speech** (July 21, 2016)
- **Election Night Speech** (November 8, 2016)
- **Primary victory speeches** (multiple dates)
- **Policy addresses** and rally speeches

### **Processing Requirements**
- **Input**: DOCX files with speech transcripts
- **Output**: Plain text files for PDAF analysis
- **Metadata**: Dates, titles, word counts, context
- **Quality**: Clean conversion without formatting artifacts

## 🔬 **PDAF Analysis Scope**

### **Framework Application**
- **9 Core Dimensions**: All PDAF v10.0 dimensions applicable
- **Salience Weighting**: Rhetorical prominence analysis
- **Strategic Tension**: Internal contradiction detection
- **Context**: 2016 presidential campaign rhetoric

### **Expected Insights**
- **Campaign Evolution**: Populism changes across primary/general phases
- **Rhetorical Patterns**: Most effective populist appeals
- **Strategic Dynamics**: Tension between different populist dimensions
- **Methodological Comparison**: PDAF vs. traditional coding approaches

## 📈 **Success Metrics**

### **Technical Success**
- ✅ All 23 speeches successfully converted and processed
- ✅ PDAF analysis completes without errors
- ✅ Results format suitable for research dissemination
- ✅ Processing time under 2 hours total

### **Research Success**
- ✅ Clear populism patterns identified across campaign
- ✅ Meaningful evolution tracked over 17 months
- ✅ Strategic tension analysis reveals rhetorical dynamics
- ✅ Results provide basis for framework validation

## 🔗 **Integration Points**

### **Related Projects**
- **Main Trump Project**: `/projects/2d_trump_populism/` (PDAF framework source)
- **Source Data**: `/pm/paper_replication_experiment_vanderveen/` (original speeches)
- **Analysis Tools**: `/corpus/tools/` (processing utilities)

### **Dependencies**
- **Python Environment**: Compatible with PDAF v10.0 and python-docx
- **File Access**: Read access to source directory, write access to output
- **External Libraries**: python-docx for DOCX processing

## ⚠️ **Prerequisites**

### **System Requirements**
```bash
pip install python-docx  # For DOCX processing
# PDAF v10.0 environment already configured
```

### **Data Access**
- ✅ Source speeches available at specified path
- ✅ Write access to output directories
- ✅ Sufficient disk space for converted files

### **Framework Readiness**
- ✅ PDAF v10.0 specification available
- ✅ Analysis pipeline functional
- ✅ Output validation procedures ready

## 📋 **Quick Start Guide**

### **1. Convert Speech Data**
```bash
cd projects/vanderveen_presidential_pdaf
python scripts/convert_docx_to_text.py
```

### **2. Verify Conversion**
```bash
ls corpus/*.txt | wc -l  # Should show 23
cat corpus/manifest.json # Review speech metadata
```

### **3. Execute PDAF Analysis**
```bash
# Use existing PDAF analysis pipeline
# Results will be stored in runs/ directory
```

### **4. Review Results**
```bash
# Check runs/ directory for analysis outputs
# Review docs/ for aggregated findings
```

## 🎯 **Next Steps**

### **Immediate Actions**
1. **Run conversion script** to process DOCX files
2. **Review manifest.json** for speech metadata accuracy
3. **Execute PDAF analysis** on converted corpus
4. **Analyze results** for populism patterns and evolution

### **Post-Analysis**
1. **Compare methodologies** (PDAF vs. original study)
2. **Document insights** and framework advantages
3. **Plan Phase 2 expansion** based on validated approach
4. **Publish findings** as methodological contribution

---

**Project Status**: **READY FOR EXECUTION** 🚀
**Estimated Duration**: 3 days
**Success Probability**: High (focused scope, established data, validated framework)
**Impact**: Framework validation + methodological insights + Phase 2 foundation
