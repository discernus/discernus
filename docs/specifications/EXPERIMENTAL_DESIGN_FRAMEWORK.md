# Experimental Design Framework for Narrative Analysis
*Version: 2.1.0*  
*Last Updated: June 13, 2025*

## **🎯 Overview**

Narrative analysis experiments are systematic explorations of a **five-dimensional design space** where each dimension represents independent methodological choices. This framework enables rigorous hypothesis testing about the interaction effects between different analytical approaches, content types, and evaluation methods.

## **📐 The Five-Dimensional Experimental Design Space**

### **Dimension 1: TEXTS** 
*What content is being analyzed*

**Design Choices**:
- **Content Type**: Political speeches, literary works, social media, news articles, historical documents
- **Text Length**: Short-form (tweets, headlines) vs Long-form (speeches, articles)
- **Historical Period**: Contemporary vs Historical texts
- **Author Characteristics**: Known vs anonymous authors, demographic attributes
- **Genre Conventions**: Formal vs informal register, rhetorical vs descriptive style
- **Temporal Scope**: Single text vs text collections vs longitudinal corpora

**Experimental Implications**:
- **Content Validity**: Different frameworks may be more appropriate for different content types
- **Length Effects**: Short texts may show higher variance, long texts more stable patterns
- **Temporal Stability**: Historical texts may require period-appropriate interpretation
- **Author Effects**: Known authorship may bias framework application
- **Genre Sensitivity**: Formal political speech vs casual social media require different analytical approaches

**Hypothesis Examples**:
- *H1*: Civic virtue framework shows higher reliability on formal political texts than informal social media
- *H2*: Historical texts (>50 years old) require adjusted weighting schemes for contemporary frameworks
- *H3*: Author anonymity reduces systematic bias in LLM moral framework application

### **Dimension 2: FRAMEWORKS**
*What theoretical lens is applied to the analysis*

**Design Choices**:
- **Theoretical Foundation**: Virtue ethics, moral foundations, political spectrum, rhetorical analysis
- **Dimensional Structure**: Number of dimensions, dipole vs single-pole design
- **Complexity Level**: Simple binary classifications vs complex multi-dimensional spaces
- **Domain Specificity**: General-purpose vs domain-specific frameworks
- **Cultural Context**: Western vs non-Western philosophical foundations
- **Temporal Orientation**: Contemporary vs historical theoretical frameworks

**Experimental Implications**:
- **Framework Fit**: Some frameworks may be inappropriate for certain content types
- **Dimensional Sufficiency**: Complex texts may require more dimensional frameworks
- **Cultural Bias**: Western frameworks may not capture non-Western narrative patterns
- **Theoretical Validity**: Framework choice affects what patterns can be detected
- **Comparative Analysis**: Multiple frameworks enable triangulation and validation

**Hypothesis Examples**:
- *H4*: Moral foundations framework shows higher inter-rater reliability than political spectrum for moral argumentation texts
- *H5*: Domain-specific frameworks (civic virtue for political texts) outperform general frameworks for specialized content
- *H6*: Multi-dimensional frameworks capture more nuanced patterns than binary classifications

### **Dimension 3: PROMPT TEMPLATES**
*How evaluators are instructed to perform analysis*

**Design Choices**:
- **Analysis Approach**: Hierarchical ranking vs simultaneous scoring vs comparative assessment
- **Evidence Requirements**: No evidence vs textual citations vs comprehensive justification
- **Instruction Detail**: Minimal vs comprehensive vs step-by-step guidance
- **Output Format**: Structured JSON vs natural language vs hybrid approaches
- **Cognitive Load**: Simple scoring vs complex analytical reasoning
- **Model Compatibility**: Model-agnostic vs model-optimized instructions

**Experimental Implications**:
- **Reliability Effects**: More structured prompts may increase consistency but reduce nuance
- **Evidence Quality**: Evidence requirements improve justification but increase response length/cost
- **Cognitive Complexity**: Complex instructions may exceed some models' capabilities
- **Parsing Reliability**: Structured outputs enable automation but may constrain natural reasoning
- **Model Bias**: Different models may respond differently to identical instructions

**Hypothesis Examples**:
- *H7*: Hierarchical prompts produce more reliable results than simultaneous scoring across all frameworks
- *H8*: Evidence-required prompts improve human-LLM agreement at the cost of response consistency
- *H9*: Model-optimized prompts show higher reliability within-model but lower cross-model generalizability

### **Dimension 4: WEIGHTING SCHEMES**
*How scoring results are mathematically interpreted*

**Design Choices**:
- **Mathematical Approach**: Linear averaging vs nonlinear transformations vs hierarchical weighting
- **Dominance Handling**: Equal treatment vs amplification of dominant signals
- **Noise Reduction**: Standard calculation vs noise-suppressing algorithms
- **Interpretability**: Simple geometric positioning vs complex mathematical transformations
- **Edge Case Handling**: Standard vs specialized handling of ties, zeros, outliers
- **Normalization Method**: Raw scores vs normalized vs standardized approaches

**Experimental Implications**:
- **Pattern Detection**: Different schemes emphasize different aspects of the underlying data
- **Interpretability Trade-offs**: Complex schemes may reveal patterns but reduce understandability
- **Reliability Effects**: Some schemes may amplify or reduce measurement error
- **Comparative Validity**: Scheme choice affects conclusions about relative positioning
- **Mathematical Properties**: Different schemes have different statistical properties

**Hypothesis Examples**:
- *H10*: Winner-take-most weighting improves pattern clarity for texts with dominant themes
- *H11*: Hierarchical weighting based on LLM rankings shows higher validity than equal weighting
- *H12*: Linear schemes show higher reliability while nonlinear schemes show higher discriminative validity

### **Dimension 5: EVALUATORS**
*What agents perform the analysis*

**Design Choices**:
- **Evaluator Type**: Large Language Models vs Human expert reviewers vs Hybrid approaches
- **LLM Provider**: OpenAI vs Anthropic vs Mistral vs Google AI vs Open-source models
- **Model Capability**: Reasoning-optimized vs efficiency-optimized vs specialized models
- **Human Expertise**: Domain experts vs naive coders vs trained research assistants
- **Evaluation Protocol**: Independent assessment vs consensus building vs iterative refinement
- **Scale Considerations**: Single evaluator vs multiple evaluators vs crowd-sourcing

**Experimental Implications**:
- **Reliability Patterns**: Different evaluators show different consistency patterns
- **Validity Questions**: Human-LLM agreement varies by task type and complexity
- **Cost-Quality Trade-offs**: Human evaluation expensive but potentially higher quality
- **Bias Patterns**: Different models and humans show different systematic biases
- **Scalability**: Evaluation choice affects feasible study scope and timeline

**Hypothesis Examples**:
- *H13*: Claude models show higher evidence quality while GPT models show higher consistency
- *H14*: Human expert evaluation shows higher validity but lower reliability than LLM evaluation
- *H15*: Multi-model consensus approaches reduce systematic bias while maintaining efficiency

## **🔬 Experimental Design Methodologies**

### **Single-Factor Experiments**
**Purpose**: Isolate the effect of one dimensional choice while holding others constant

**Design Pattern**:
```
Texts: [Fixed set]
Frameworks: [Fixed framework]  
Prompts: [Variable: A, B, C]
Weighting: [Fixed scheme]
Evaluators: [Fixed model]
```

**Example**: Testing whether hierarchical vs traditional vs evidence-based prompts affect reliability for civic virtue analysis of presidential speeches using GPT-4.1-mini and linear weighting.

**Statistical Analysis**: ANOVA comparing means across prompt conditions
**Key Metrics**: Reliability (CV), validity (human agreement), efficiency (cost/time)

### **Two-Factor Experiments**
**Purpose**: Examine interaction effects between two dimensional choices

**Design Pattern**:
```
Texts: [Fixed set]
Frameworks: [Variable: Framework A, Framework B]
Prompts: [Variable: Prompt X, Prompt Y]  
Weighting: [Fixed scheme]
Evaluators: [Fixed model]
```

**Example**: Testing framework × prompt interactions to determine whether hierarchical prompts work better with some frameworks than others.

**Statistical Analysis**: 2×2 factorial ANOVA with interaction terms
**Key Metrics**: Main effects, interaction effects, effect sizes

### **Multi-Factor Experiments**
**Purpose**: Systematic exploration of complex interaction patterns

**Design Pattern**:
```
Texts: [Stratified sample across content types]
Frameworks: [2-3 frameworks]
Prompts: [2-3 prompt types]
Weighting: [2-3 schemes]  
Evaluators: [2-3 models]
```

**Example**: Full factorial design comparing civic virtue vs political spectrum frameworks with hierarchical vs traditional prompts using linear vs winner-take-most weighting across GPT vs Claude models.

**Statistical Analysis**: Multi-way ANOVA, mixed-effects models, component analysis
**Key Metrics**: Main effects, all interaction terms, optimal configurations

### **Component Matrix Experiments**
**Purpose**: Systematic optimization across all dimensional choices

**Design Pattern**: Complete enumeration of practically feasible combinations
**Sample Size**: Determined by statistical power requirements for planned comparisons
**Controls**: Randomization of execution order, balanced assignment, replication

**Output**: 
- **Optimal Configurations**: Best combinations for specific research goals
- **Component Rankings**: Relative importance of each dimensional choice
- **Interaction Maps**: Which combinations work well together
- **Efficiency Frontiers**: Cost-quality trade-offs across configurations

### **Validation Studies**
**Purpose**: Compare LLM approaches against human expert evaluation

**Design Pattern**:
```
Texts: [Representative sample with known characteristics]
Frameworks: [Established, validated framework]
Prompts: [Best-performing from prior experiments]
Weighting: [Validated scheme]
Evaluators: [LLMs vs Human experts]
```

**Gold Standard**: Expert human evaluation with high inter-rater reliability
**Validation Metrics**: Correlation, agreement rates, systematic bias detection
**Outcome**: Confidence bounds for LLM-based analysis validity

## **📊 Experimental Outcome Analysis**

### **Component Performance Metrics**

**Reliability Measures**:
- **Intra-evaluator consistency**: Multiple runs with same configuration
- **Inter-evaluator agreement**: Different evaluators, same configuration  
- **Test-retest stability**: Same analysis repeated over time
- **Internal consistency**: Coherence across framework dimensions

**Validity Measures**:
- **Content validity**: Framework appropriateness for text type
- **Construct validity**: Framework captures intended theoretical constructs
- **Criterion validity**: Agreement with external validation measures
- **Convergent validity**: Agreement across different analytical approaches

**Efficiency Measures**:
- **Cost efficiency**: Analysis quality per dollar spent
- **Time efficiency**: Analysis quality per unit time
- **Scalability**: Performance degradation with increased scope
- **Resource utilization**: Optimal use of computational/human resources

### **Interaction Effect Analysis**

**Synergistic Effects**: Combinations that perform better than individual components predict
**Antagonistic Effects**: Combinations that perform worse than expected
**Compensatory Effects**: Weaknesses in one dimension offset by strengths in another
**Multiplicative Effects**: Performance improvements that compound across dimensions

### **Optimization Outcomes**

**Configuration Recommendations**: Best combinations for specific research goals
**Trade-off Analysis**: Cost vs quality vs speed vs reliability optimization
**Robustness Assessment**: Performance stability across different contexts
**Generalizability**: Applicability of findings to new domains/applications

## **🎯 Research Question Framework**

### **Methodological Research Questions**

**Prompt Engineering**:
- Which instruction approaches produce most reliable results?
- How do evidence requirements affect analysis quality vs efficiency?
- What level of instruction detail optimizes performance?

**Framework Validation**:
- Which theoretical frameworks best capture specific content types?  
- How do framework complexity and analytical depth interact?
- What domain-specificity vs generalizability trade-offs exist?

**Weighting Methodology**:
- Which mathematical approaches best reveal meaningful patterns?
- How do noise reduction vs information preservation trade-offs affect outcomes?
- What weighting schemes optimize interpretability vs discriminative power?

**Evaluator Performance**:
- How do different LLMs compare on reliability, validity, and efficiency?
- What systematic biases exist across different models and providers?
- How does human expert evaluation compare to optimized LLM approaches?

**System Integration**:
- Which component combinations produce optimal results for specific research goals?
- How do interaction effects vary across content types and research contexts?
- What are the efficiency frontiers for cost, quality, and speed optimization?

### **Substantive Research Questions**

**Content Analysis**:
- How do political communication patterns vary across speakers, time periods, contexts?
- What moral and rhetorical strategies characterize different types of persuasive discourse?
- How do narrative frameworks reveal bias, manipulation, or persuasive intent?

**Comparative Analysis**:
- How do different authors, parties, or movements compare on specific analytical dimensions?
- What patterns distinguish effective vs ineffective persuasive communication?
- How do cultural, temporal, or contextual factors affect narrative analysis results?

**Longitudinal Analysis**:
- How do communication patterns change over time within speakers or movements?
- What events or contexts trigger systematic changes in rhetorical approach?
- How do narrative frameworks capture evolution in political or cultural discourse?

## **📚 Implementation Guidelines**

### **Experimental Planning Process**

1. **Research Question Definition**: Clearly specify what hypotheses are being tested
2. **Dimensional Analysis**: Identify which dimensions are experimental variables vs controls
3. **Power Analysis**: Determine required sample sizes for planned statistical tests
4. **Resource Planning**: Estimate costs, time requirements, and computational needs
5. **Protocol Design**: Specify randomization, controls, and data collection procedures

### **Quality Assurance Integration**

**Pre-experimental Validation**:
- Component compatibility verification
- Pilot testing with small samples
- Statistical power confirmation
- Resource requirement validation

**During-experiment Monitoring**:
- Real-time quality metrics tracking
- Anomaly detection and flagging
- Cost and time tracking against projections
- Interim analysis for early stopping or modification

**Post-experimental Validation**:
- Comprehensive quality assessment using 6-layer QA system
- Statistical assumption testing
- Effect size calculation and interpretation
- Replication readiness verification

### **Documentation Standards**

**Pre-registration**: Complete experimental design specification before data collection
**Provenance Tracking**: Complete audit trail for all analytical choices and configurations
**Replication Package**: All code, data, and instructions necessary for independent replication
**Transparency Reporting**: Full disclosure of all analytical choices, including those that didn't work

## **🔄 Iterative Experimental Development**

### **Component Development Cycle**

1. **Hypothesis Formation**: Specific predictions about component performance
2. **Pilot Testing**: Small-scale validation of component functionality
3. **Systematic Evaluation**: Controlled comparison against established alternatives
4. **Integration Testing**: Performance in combination with other components
5. **Optimization**: Parameter tuning and refinement based on empirical results

### **Framework Evolution**

**Version Control**: Systematic tracking of component changes and performance impact
**Backward Compatibility**: Ensuring new versions can reproduce previous results
**Migration Pathways**: Clear procedures for updating experimental configurations
**Deprecation Management**: Graceful handling of obsolete components and methods

---

**This framework enables systematic, rigorous experimental research that treats narrative analysis as a multidimensional methodological space rather than a collection of independent tools. It supports both component development and substantive research while maintaining standards for reproducibility and academic rigor.** 