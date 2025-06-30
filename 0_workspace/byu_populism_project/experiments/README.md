# BYU Populism Project - Experiments

This folder contains experiments designed for **BYU charter customer validation** using the Brazilian 2018 presidential campaign corpus.

## 🎯 **Objective**
Validate the Discernus platform against **BYU Team Populism** research standards through systematic replication and extension of the Tamaki & Fuks (2019) competitive populism analysis.

## 📊 **Available Experiments**

### `byu_bolsonaro_validation.yaml`
**Four-condition methodological validation** using 12 Bolsonaro speeches from July-October 2018:

- **Target**: r > 0.80 correlation with BYU manual coding
- **Framework**: Democratic Tension Axis Model (Populism↔Pluralism + Patriotism↔Nationalism)  
- **Corpus**: 12 professional transcripts from actual campaign speeches
- **Methodology**: Sequential vs parallel prompting comparison
- **Output**: Auto-generated Jupyter notebook via Stage 5→6 integration

## 🔬 **Four-Condition Design**

1. **Manual Speaker Isolation** (Ground Truth)
2. **Full Context Analysis** (Baseline)  
3. **Controlled AI Pipeline** (Target Methodology)
4. **Conversational Analysis** (Comparative Validation)

## 📁 **Corpus Location**
Transcripts: `../populism in brazil 2018/speeches-zip/rev-transcripts/`

## 🚀 **Execution**
Run experiments through the main Discernus system:
```bash
cd ../../../  # Return to project root
python3 discernus/experiments/run_experiment.py --config 0_workspace/byu_populism_project/experiments/byu_bolsonaro_validation.yaml
```

## 📈 **Expected Deliverables**
- Statistical validation report
- Cross-LLM reliability analysis  
- Temporal progression visualization
- Publication-ready Jupyter notebook
- Academic methodology documentation

## 🎓 **Strategic Context**
This validation supports **BYU as a charter customer** by demonstrating:
- Computational methodology exceeding human reliability
- Novel insights impossible with manual coding
- Academic-grade experimental validation
- Scalable research acceleration potential

## 📋 **Success Criteria**
- **Gate 1**: Basic replication (r > 0.70)
- **Gate 2**: Methodological advancement (novel insights + cross-validation)
- **Partnership Decision**: Proceed to 6-month pilot if both gates achieved

---

**Cross-References:**
- `BYU_METHODOLOGICAL_VALIDATION_PROTOCOL.md`
- `BYU_EXPERIMENT_REQUIREMENTS_SCRATCHPAD.md`
- `experiment_design_considerations.md` 