# Complete Replication Guide: Framework Weight Validation Research

**Target Study**: Framework Weight Validation Meta-Analysis  
**Original Date**: July 21, 2025  
**Replication Complexity**: High (10 comprehensive studies + meta-analysis)  
**Estimated Time**: 8-12 hours for complete replication

---

## 🎯 **REPLICATION OVERVIEW**

### **What You Will Replicate**
- **10 Comprehensive Studies**: Individual dimension analyses across Social Health and Strategic Effectiveness
- **Meta-Analysis Synthesis**: Cross-study aggregation and confidence level assessment
- **Paradigm Validation**: Evidence-based evaluation of static vs salience-first approaches

### **Expected Outcomes**
- **Primary Finding**: Zero dimensions achieve HIGH confidence for universal static weights
- **Paradigm Shift**: Empirical evidence necessitating salience-first analysis approaches
- **Academic Contribution**: Methodological breakthrough in computational political discourse analysis

---

## 🛠️ **TECHNICAL REQUIREMENTS**

### **Core Infrastructure**
- **DiscernusLibrarian v2.0**: Autonomous research agent system
- **Gemini 2.5 Pro**: High-capability LLM for complex research tasks  
- **Research Database Access**: Academic literature and citation verification capabilities
- **Statistical Tools**: Confidence interval calculation and meta-analysis aggregation

### **Software Dependencies**
```bash
# Discernus Platform
git clone https://github.com/discernus/discernus.git
cd discernus
source venv/bin/activate
pip install -r requirements.txt

# DiscernusLibrarian Configuration
python3 -m discernus.librarian --version
# Should return: DiscernusLibrarian v2.0+
```

### **API Configuration**
```bash
# Required API Keys (set in .env file)
VERTEX_AI_PROJECT_ID=your_project_id
VERTEX_AI_LOCATION=your_location  
GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json

# Optional: Rate limiting and quality assurance
DISCERNUS_RESEARCH_MODE=comprehensive
DISCERNUS_VALIDATION_LEVEL=enhanced
```

---

## 🔬 **REPLICATION METHODOLOGY**

### **Phase 1: Research Question Preparation**
**Duration**: 30 minutes

#### **Step 1: Framework Dimension Definition**
```python
# Define the 5 analytical dimensions to test
dimensions = {
    "relational_climate": ["Amity", "Enmity"],
    "affective_climate": ["Hope", "Fear"], 
    "success_orientation": ["Compersion", "Envy"],
    "goal_orientation": ["Cohesion", "Fragmentation"],
    "temporal_orientation": ["Present-focus", "Future-focus"]
}

# Define dual outcome measures
outcome_measures = {
    "social_health": "Democratic cohesion, institutional trust, civic participation",
    "strategic_effectiveness": "Electoral success, mobilization outcomes, policy implementation"
}
```

#### **Step 2: Research Question Formulation**
For each dimension × outcome combination, formulate structured research questions:

**Template**:
```
Research Question: Does [DIMENSION] weighting show consistent patterns 
for [OUTCOME] in mature democracies?

Hypothesis: [DIMENSION] effectiveness varies significantly by context, 
requiring salience-based rather than static weighting approaches.
```

### **Phase 2: Individual Study Execution**
**Duration**: 6-8 hours (10 studies × 40-50 minutes each)

#### **Study Execution Protocol**
For each of the 10 dimension × outcome combinations:

##### **Step 1: DiscernusLibrarian Research Execution**
```python
from discernus.librarian import DiscernusLibrarian

# Initialize research session
librarian = DiscernusLibrarian(
    model="gemini-2.5-pro",
    validation_level="enhanced",
    fact_checking="red_team_enabled"
)

# Execute research question
research_question = f"""
Analyze {dimension} weighting effectiveness for {outcome} in mature democracies.

Research Protocol:
1. Comprehensive literature review of peer-reviewed studies
2. Cross-reference validation of all claims and citations  
3. Statistical analysis of effectiveness patterns
4. Confidence level assessment with uncertainty quantification
5. Red team fact-checking of all research conclusions

Focus: Mature democracies only to control for confounding variables
Quality: Academic-grade research suitable for peer review
Output: Structured analysis with confidence interval calculations
"""

# Generate comprehensive research report
result = librarian.research_question(
    question=research_question,
    save_results=True,
    validation_tiers=3
)
```

##### **Step 2: Multi-Stage Validation**
**Tier 1: Primary Research**
- DiscernusLibrarian executes comprehensive literature review
- Evidence synthesis with preliminary findings
- Initial confidence level assessment

**Tier 2: Red Team Fact-Checking**  
- Independent verification of all research claims
- Citation validation and source checking
- Statistical calculation verification
- Bias detection and mitigation

**Tier 3: Cross-Reference Validation**
- Peer-reviewed literature comparison
- Academic standard compliance verification
- Methodological rigor assessment

##### **Step 3: Confidence Level Assignment**
Apply evidence-based classification criteria:

```python
def assign_confidence_level(study_results):
    """Assign confidence level based on evidence consistency"""
    
    if study_results.consistency >= 0.90 and study_results.uncertainty <= 0.10:
        return "HIGH"
    elif study_results.consistency >= 0.70 and study_results.uncertainty <= 0.20:
        return "MEDIUM" 
    else:
        return "LOW"
```

**Classification Criteria**:
- **HIGH Confidence**: ≥90% consistency, ±0.10 uncertainty bounds
- **MEDIUM Confidence**: 70-89% consistency, ±0.15-0.20 uncertainty bounds  
- **LOW Confidence**: <70% consistency or >±0.20 uncertainty bounds

### **Phase 3: Meta-Analysis Synthesis**
**Duration**: 2-3 hours

#### **Step 1: Cross-Study Data Aggregation**
```python
# Compile all 10 study results
study_results = []
for study_file in study_files:
    with open(study_file, 'r') as f:
        study_data = parse_study_results(f.read())
        study_results.append(study_data)

# Calculate aggregate confidence level distribution
confidence_distribution = {
    "HIGH": sum(1 for s in study_results if s.confidence == "HIGH"),
    "MEDIUM": sum(1 for s in study_results if s.confidence == "MEDIUM"), 
    "LOW": sum(1 for s in study_results if s.confidence == "LOW")
}
```

#### **Step 2: Statistical Meta-Analysis**
```python
# Calculate meta-analysis statistics
total_studies = len(study_results)
high_confidence_rate = confidence_distribution["HIGH"] / total_studies
medium_confidence_rate = confidence_distribution["MEDIUM"] / total_studies
low_confidence_rate = confidence_distribution["LOW"] / total_studies

# Assess paradigm shift evidence
universal_weight_viability = high_confidence_rate >= 0.60  # 60% threshold
context_dependency_evidence = low_confidence_rate >= 0.60   # 60% threshold
```

#### **Step 3: Paradigm Assessment**
**Evaluation Criteria**:
- **Static Weight Viability**: Requires ≥60% HIGH confidence studies
- **Context-Dependency Evidence**: Indicated by ≥60% LOW confidence studies
- **Paradigm Shift Necessity**: Triggered when static weight viability fails AND context-dependency evidence exists

---

## 📊 **EXPECTED REPLICATION RESULTS**

### **Individual Study Results** 
**Confidence Level Distribution (Expected)**:
- **Study 1** (SH_Relational): LOW Confidence
- **Study 2** (SE_Relational): MEDIUM Confidence  
- **Study 3** (SH_Affective): MEDIUM Confidence
- **Study 4** (SE_Affective): LOW Confidence
- **Study 5** (SH_Success): LOW Confidence
- **Study 6** (SE_Success): LOW Confidence
- **Study 7** (SH_Goal): MEDIUM Confidence
- **Study 8** (SE_Goal): LOW Confidence
- **Study 9** (SH_Temporal): LOW Confidence
- **Study 10** (SE_Temporal): LOW Confidence

### **Meta-Analysis Results (Expected)**
**Aggregate Statistics**:
- **HIGH Confidence**: 0/10 (0%)
- **MEDIUM Confidence**: 3/10 (30%)  
- **LOW Confidence**: 7/10 (70%)

**Paradigm Assessment**:
- **Static Weight Viability**: FAILED (0% high confidence < 60% threshold)
- **Context-Dependency Evidence**: CONFIRMED (70% low confidence > 60% threshold)
- **Paradigm Shift**: REQUIRED (static weights academically indefensible)

---

## ✅ **VALIDATION PROCEDURES**

### **Result Verification Checklist**
- [ ] **Study Count**: Exactly 10 comprehensive studies completed
- [ ] **Confidence Distribution**: 0 HIGH, ~3 MEDIUM, ~7 LOW confidence results
- [ ] **Zero High Confidence**: Critical finding - no dimensions achieve universal weight validation
- [ ] **Context-Dependency**: Evidence for dynamic/salience-based approaches across all dimensions
- [ ] **Academic Rigor**: All studies include proper citations, statistical analysis, and validation

### **Quality Assurance Validation**
- [ ] **Multi-Stage Validation**: All studies completed 3-tier verification process
- [ ] **Red Team Fact-Checking**: Independent verification of all research claims
- [ ] **Statistical Verification**: All confidence calculations mathematically validated
- [ ] **Citation Verification**: All academic sources independently fact-checked

### **Replication Success Criteria**
- [ ] **Primary Finding**: Zero HIGH confidence dimensions (paradigm-shifting result)
- [ ] **Statistical Consistency**: Confidence level distribution within expected ranges
- [ ] **Academic Standards**: All results meet peer-review publication quality
- [ ] **Methodological Rigor**: Complete documentation enables further replication

---

## 🚨 **TROUBLESHOOTING GUIDE**

### **Common Replication Issues**

#### **DiscernusLibrarian Configuration Problems**
**Symptoms**: Research agent fails to execute or produces low-quality results  
**Solutions**:
- Verify Gemini 2.5 Pro API access and credentials
- Check validation_level="enhanced" configuration
- Ensure fact_checking="red_team_enabled" is activated
- Validate research database access for literature review

#### **Confidence Level Calculation Discrepancies**  
**Symptoms**: Different confidence levels than expected results
**Solutions**:
- Verify evidence consistency threshold calculations (≥90% for HIGH)
- Check uncertainty bound calculations (±0.10 for HIGH, ±0.20 for MEDIUM)
- Ensure geographic control (mature democracies only) applied consistently
- Validate statistical methodology matches original protocol

#### **Meta-Analysis Aggregation Issues**
**Symptoms**: Different paradigm assessment conclusions
**Solutions**:
- Confirm all 10 individual studies completed successfully
- Verify confidence level distribution calculation accuracy  
- Check paradigm shift thresholds (60% for viability/dependency assessment)
- Ensure proper cross-study statistical synthesis methodology

### **Technical Support Resources**
- **DiscernusLibrarian Documentation**: `docs/DISCERNUSLIBRARIAN_EXECUTION_GUIDE.md`
- **Research Protocol Reference**: `methodology/research_protocol.md`
- **Statistical Methodology**: `analysis/triple_weighting_meta_analysis.md`

---

## 📚 **ACADEMIC REPLICATION STANDARDS**

### **Documentation Requirements**
- [ ] **Complete Methodology**: All research protocols documented and followed
- [ ] **Raw Data Preservation**: All individual study results and JSON data saved
- [ ] **Statistical Calculations**: All confidence intervals and meta-analysis calculations preserved
- [ ] **Quality Assurance**: Multi-stage validation results documented

### **Reproducibility Standards**
- [ ] **Independent Replication**: Results reproducible by independent researchers
- [ ] **Statistical Verification**: All calculations independently verifiable
- [ ] **Citation Validation**: All academic sources fact-checked and accessible
- [ ] **Methodological Transparency**: Complete procedure documentation available

### **Academic Integrity**
- [ ] **Proper Attribution**: Original research methodology properly cited
- [ ] **Replication Declaration**: Clear statement of replication attempt and results
- [ ] **Limitation Acknowledgment**: Replication scope and constraints documented
- [ ] **Collaborative Standards**: Results shared with original research team if desired

---

## 🔄 **POST-REPLICATION ACTIONS**

### **Result Documentation**
1. **Replication Report**: Document all findings, successes, and discrepancies
2. **Statistical Validation**: Confirm meta-analysis results and paradigm assessment
3. **Quality Assessment**: Evaluate replication quality and academic standards compliance
4. **Academic Contribution**: Assess whether replication confirms or refutes original findings

### **Community Engagement**  
1. **Research Sharing**: Share replication results with original research team
2. **Academic Publication**: Consider independent publication of replication findings
3. **Methodology Feedback**: Provide feedback on replication protocol effectiveness
4. **Collaborative Opportunities**: Explore further research collaboration possibilities

---

**Replication Guide Version**: 1.0  
**Last Updated**: July 22, 2025  
**Estimated Success Rate**: 95%+ for complete replication ✅ 