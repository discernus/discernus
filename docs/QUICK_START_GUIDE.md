# Discernus Quick Start Guide
*Get Started with Computational Text Analysis*

This guide provides essential commands to run experiments using the Discernus platform. The system is designed to be framework-agnostic, domain-neutral, and accessible to researchers across disciplines.

## Three Foundational Commitments

Before starting, understand that every Discernus analysis provides:

- **Mathematical Reliability**: Hybrid intelligence where LLMs design analysis, secure code executes calculations, and LLMs interpret results
- **Cost Transparency**: Upfront cost estimation and budget controls for predictable institutional pricing
- **Complete Reproducibility**: Zero mystery - every analytical step documented for independent replication

## Prerequisites

```bash
# Activate your virtual environment
source venv/bin/activate

# Install dependencies (if you haven't already)
pip install -r requirements.txt
```

## How Discernus Works

**Three-Component Architecture**:
1. **Framework**: Your analytical approach (political analysis, literary criticism, brand sentiment, etc.)
2. **Experiment**: Your research design and methodology
3. **Corpus**: Your collection of texts to analyze

**The Universal Command**:
```bash
# THIN Experiment Lifecycle - Intelligent validation and execution
python3 discernus_cli.py execute ./my_project/experiment.md
```

## Multi-Domain Use Cases

### Academic Research: Political Discourse Analysis

**Use Case**: Analyze political speeches for democratic engagement patterns
**Framework**: Political discourse analysis framework
**Corpus**: Campaign speeches, policy statements, debate transcripts

```bash
# Execute with THIN Experiment Lifecycle validation gauntlet
python3 discernus_cli.py execute ./projects/political_discourse/experiment.md
```

**What Happens**:
- **Validation Gauntlet**: TrueValidationAgent, ProjectCoherenceAnalyst, StatisticalAnalysisConfigurationAgent, EnsembleConfigurationAgent, WorkflowCompletenessValidator
- **Enhancement**: Automatic detection of missing SynthesisAgent and workflow completion
- **Cost Estimation**: Provides upfront pricing based on corpus size and model selection  
- **Analysis**: Ensemble of LLMs applies framework to each text
- **Statistical Analysis**: Secure code execution calculates descriptive statistics
- **Interpretation**: LLMs provide natural language analysis of results
- **Reproducibility**: Complete chronolog enables independent replication

### Corporate Communications: Brand Sentiment Analysis

**Use Case**: Analyze customer communications for brand perception
**Framework**: Brand sentiment and perception framework
**Corpus**: Customer reviews, social media posts, support tickets

```bash
# Execute with THIN Experiment Lifecycle validation gauntlet  
python3 discernus_cli.py execute ./projects/brand_sentiment/experiment.md
```

**Business Value**:
- **Systematic Analysis**: Consistent methodology across all customer touchpoints
- **Cost Control**: Predictable pricing for regular sentiment monitoring
- **Actionable Insights**: Natural language interpretation suitable for executives
- **Audit Trail**: Complete documentation for regulatory compliance

### Literary Analysis: Narrative Structure Study

**Use Case**: Analyze narrative techniques across different authors
**Framework**: Narrative structure and literary device framework
**Corpus**: Novels, short stories, poetry collections

```bash
# Execute with THIN Experiment Lifecycle validation gauntlet
python3 discernus_cli.py execute ./projects/narrative_analysis/experiment.md
```

**Academic Benefits**:
- **Rigorous Methodology**: Systematic approach to subjective literary analysis
- **Scalable Analysis**: Process large corpora impossible with manual analysis
- **Reproducible Results**: Other scholars can replicate findings exactly
- **Cross-Author Comparison**: Consistent framework enables valid comparisons

### Religious Studies: Theological Text Analysis

**Use Case**: Analyze sermons for theological themes and pastoral approaches
**Framework**: Theological discourse and pastoral care framework
**Corpus**: Sermons, homilies, pastoral letters

```bash
# Execute with THIN Experiment Lifecycle validation gauntlet
python3 discernus_cli.py execute ./projects/theological_discourse/experiment.md
```

**Institutional Applications**:
- **Pastoral Development**: Systematic feedback on communication effectiveness
- **Theological Consistency**: Ensure messaging aligns with institutional values
- **Interfaith Dialogue**: Comparative analysis across religious traditions
- **Academic Research**: Scholarly study of contemporary religious discourse

### Think Tank Research: Policy Document Analysis

**Use Case**: Analyze policy documents for implementation feasibility
**Framework**: Policy analysis and implementation framework
**Corpus**: Legislative proposals, regulatory documents, policy briefs

```bash
# Execute with THIN Experiment Lifecycle validation gauntlet
python3 discernus_cli.py execute ./projects/policy_analysis/experiment.md
```

**Policy Applications**:
- **Evidence-Based Analysis**: Systematic evaluation of policy language
- **Implementation Guidance**: Identify potential obstacles and opportunities
- **Stakeholder Communication**: Clear, documented rationale for recommendations
- **Institutional Memory**: Consistent methodology across different policy areas

### Journalism: Source Credibility Analysis

**Use Case**: Analyze news sources for bias and reliability indicators
**Framework**: Journalistic credibility and bias detection framework
**Corpus**: News articles, press releases, editorial content

```bash
python3 -c "
from discernus.agents.validation_agent import ValidationAgent
agent = ValidationAgent()
agent.validate_and_execute_sync(
    'frameworks/source_credibility.md',
    'experiments/media_bias_study.md', 
    'corpus/news_sources/'
)
"
```

**Journalism Benefits**:
- **Systematic Verification**: Consistent approach to source evaluation
- **Transparency**: Complete methodology for readers and editors
- **Scalable Analysis**: Process large volumes of sources efficiently
- **Editorial Support**: Data-driven insights for newsroom decisions

## Understanding the Workflow

### 1. Validation Phase
The `ValidationAgent` performs comprehensive validation:
- **Framework Completeness**: Ensures analytical framework meets quality standards
- **Experiment Design**: Validates research methodology and statistical approach
- **Corpus Quality**: Checks data format, encoding, and accessibility
- **Cost Estimation**: Provides upfront pricing for the entire analysis

### 2. Orchestration Phase
The `WorkflowOrchestrator` manages the analysis:
- **Model Selection**: Chooses optimal LLMs based on task requirements and budget
- **Ensemble Analysis**: Multiple LLMs apply framework to each text
- **Adversarial Review**: Models challenge and validate each other's analysis
- **Statistical Processing**: Secure code execution for mathematical operations

### 3. Synthesis Phase
The system produces comprehensive results:
- **Quantitative Results**: Statistical analysis with confidence intervals
- **Qualitative Insights**: Natural language interpretation of patterns
- **Evidence Documentation**: Complete citations and reasoning
- **Reproducibility Package**: Everything needed for independent replication

## Cost and Budget Management

### Upfront Cost Estimation
```bash
# Get cost estimate before running analysis
python3 -c "
from discernus.agents.validation_agent import ValidationAgent
agent = ValidationAgent()
estimate = agent.estimate_cost_only(
    'path/to/framework.md',
    'path/to/experiment.md',
    'path/to/corpus/'
)
print(f'Estimated cost: ${estimate[\"total_cost\"]:.2f}')
print(f'Estimated time: {estimate[\"duration_minutes\"]} minutes')
"
```

### Budget Controls
- **Maximum Spend Limits**: Set budget caps to prevent overruns
- **Model Selection**: Choose cost-effective models for different tasks
- **Batch Processing**: Optimize corpus processing for cost efficiency
- **Usage Tracking**: Monitor spending throughout analysis

## Quality Assurance

### Framework Validation
The system validates your analytical framework against:
- **Completeness**: All required components present
- **Coherence**: Internal consistency and logical flow
- **Applicability**: Can be successfully applied to your corpus
- **Reproducibility**: Clear enough for independent replication

### Experiment Design Validation
Your experiment design is checked for:
- **Methodological Rigor**: Appropriate statistical approach
- **Sampling Strategy**: Representative corpus selection
- **Bias Mitigation**: Systematic error detection and correction
- **Ethical Compliance**: Appropriate handling of sensitive content

## Results and Outputs

### Standard Deliverables
Every Discernus analysis produces:
- **Analysis Report**: Human-readable findings with evidence
- **Statistical Summary**: Quantitative results with confidence measures
- **Methodology Documentation**: Complete analytical process description
- **Reproducibility Package**: All files needed for replication
- **Cost Report**: Detailed breakdown of analysis expenses

### Academic Integration
- **Citation-Ready Results**: Properly formatted for academic publication
- **Peer Review Package**: Complete methodology for reviewer evaluation
- **Replication Instructions**: Step-by-step guide for independent verification
- **Data Availability**: Transparent access to analytical inputs and outputs

## Troubleshooting

### Common Issues

**Framework Validation Fails**:
- Check framework completeness against validation rubric
- Ensure all required sections are present
- Verify internal consistency and clear scoring criteria

**Corpus Processing Errors**:
- Verify file formats and text encoding
- Check directory structure and file permissions
- Ensure corpus size matches experiment design

**Cost Estimation Too High**:
- Consider more cost-effective model selections
- Optimize corpus size for budget constraints
- Adjust experiment design for efficiency

**Analysis Quality Concerns**:
- Review framework specificity and clarity
- Check corpus representativeness
- Verify model selection appropriateness

### Getting Help
- **Architecture Reference**: `docs/THIN_ARCHITECTURE_REFERENCE.md`
- **Framework Integration**: `docs/FRAMEWORK_INTEGRATION_GUIDE.md`
- **Infrastructure Guide**: `docs/CORE_INFRASTRUCTURE_GUIDE.md`
- **Strategic Vision**: `docs/DISCERNUS_STRATEGIC_VISION.md`

## Next Steps

1. **Prepare Your Framework**: Use the Framework Integration Guide to create your analytical framework
2. **Design Your Experiment**: Define your research questions and methodology
3. **Assemble Your Corpus**: Gather and organize your texts for analysis
4. **Run Cost Estimation**: Get upfront pricing before committing to analysis
5. **Execute Analysis**: Run your experiment with full transparency and reproducibility

**Success Indicator**: If using Discernus feels like "working with a really smart colleague," you're experiencing the platform as designed - amplifying human intelligence through computational assistance.

---

*This guide demonstrates Discernus's commitment to domain-neutral, cost-transparent, and completely reproducible computational text analysis. The platform serves researchers, analysts, and organizations across disciplines with the rigor and reliability required for academic and institutional adoption.* 