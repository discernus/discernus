#!/usr/bin/env python3
"""
Narrative Gravity Analysis - LLM Validation Workbench
Chainlit Interface for Systematic Validation Experiments

This interface serves as the primary research workbench for User Story 1.1:
Multi-Variable LLM Validation Experiments, supporting the comprehensive
15-step validation experimentation cycle.
"""

import chainlit as cl
import asyncio
import json
from datetime import datetime
import os
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from narrative_gravity.chatbot.narrative_gravity_bot import NarrativeGravityBot
    from narrative_gravity.framework_manager import FrameworkManager
    from narrative_gravity.utils.environment_setup import setup_environment, check_database_connection
    from narrative_gravity.models.database import SessionLocal
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Global bot instance
bot = None
framework_manager = None

@cl.on_chat_start
async def start():
    """Initialize the LLM Validation Workbench"""
    global bot, framework_manager
    
    try:
        # Initialize environment
        setup_environment()
        
        # Test database connection
        db_connected = check_database_connection()
        if not db_connected:
            await cl.Message(
                content="⚠️ Database connection failed. Some features may be limited. Please check `python check_database.py`"
            ).send()
        
        # Initialize bot and framework manager
        bot = NarrativeGravityBot()
        framework_manager = FrameworkManager()
        
        # Get available frameworks
        frameworks = framework_manager.list_frameworks()
        current_framework = framework_manager.get_active_framework()
        
        # Create welcome message for validation workbench
        framework_list = "\n".join([f"   • **{fw['name']}** (v{fw['version']}) - {fw['description'][:80]}..." 
                                   for fw in frameworks])
        
        welcome_message = f"""# 🧪 **LLM Validation Workbench**
## *Systematic Framework Validation & Evidence Generation*

Welcome to the **Narrative Gravity Analysis Validation Workbench** - your primary research interface for conducting systematic validation experiments as described in **User Story 1.1**.

### 🎯 **Current Configuration**
- **Active Framework**: **{current_framework or 'None selected'}**
- **Database**: {'✅ Connected' if db_connected else '❌ Disconnected'}
- **Available Frameworks**: {len(frameworks)}

### 📋 **Available Frameworks**
{framework_list}

### 🧪 **Validation Experiment Capabilities**

#### **Phase 1: Experiment Design**
- **Text Corpus Assembly**: Upload and analyze multiple texts with metadata
- **Framework Variants**: Test different weighting configurations
- **Prompt Template Testing**: Compare analysis prompt approaches  
- **LLM Configuration**: Multi-model validation studies

#### **Phase 2: Execution & Monitoring**
- **Batch Processing**: Systematically analyze text collections
- **Framework Fit Assessment**: Automatic quality gates and appropriateness detection
- **Real-time Progress**: Monitor multi-LLM validation runs
- **Cost Tracking**: Real-time API usage monitoring

#### **Phase 3: Deep Analysis**
- **Cross-LLM Consensus**: Target >0.90 correlation analysis
- **Evidence Extraction**: Supporting passage identification and quality assessment
- **Metadata Patterns**: Historical trends and speaker difference analysis
- **Statistical Validation**: Significance testing and confidence intervals

#### **Phase 4: Evidence Synthesis**
- **Academic Export**: R, Python, CSV formats for publication
- **Methodology Documentation**: Replication package generation
- **Confidence Assessment**: Academic-grade validation reporting

### 🚀 **Quick Start Validation Commands**

**Switch Framework**: `switch to fukuyama_identity framework`
**Analyze Text**: Paste or upload text for immediate analysis
**Start Experiment**: `create validation experiment with [framework] using [text corpus]`
**Compare Models**: `compare GPT-4 vs Claude analysis of [text]`
**Framework Fit**: `assess framework fit for [text or corpus]`
**Export Results**: `export academic format for [analysis or experiment]`

### 💡 **Research Workflow Examples**

**Example 1**: Framework Validation Study
```
1. "Switch to fukuyama_identity framework"
2. "Analyze Lincoln's Second Inaugural address"
3. "Compare with Trump 2015 campaign announcement"
4. "Generate cross-LLM consensus analysis"
5. "Export academic comparison dataset"
```

**Example 2**: Multi-Text Validation Experiment  
```
1. "Create validation experiment with presidential speeches corpus"
2. "Test framework fit across historical periods"
3. "Run batch analysis with GPT-4, Claude, and Mistral"
4. "Analyze temporal patterns in identity dynamics"
5. "Export replication package for academic review"
```

**Ready to begin systematic validation research!** 

Type your research question, paste text for analysis, or request specific validation experiments. The workbench will guide you through the comprehensive validation process designed to build academic confidence in the LLM-based approach.
"""
        
        await cl.Message(content=welcome_message).send()
        
        # Create action buttons for validation workbench functions
        actions = [
            cl.Action(name="validation_experiment", 
                     value="start_experiment", 
                     label="🧪 Start Validation Experiment"),
            cl.Action(name="framework_comparison", 
                     value="compare_frameworks", 
                     label="⚖️ Compare Frameworks"),
            cl.Action(name="batch_analysis", 
                     value="batch_process", 
                     label="📊 Batch Analysis"),
            cl.Action(name="academic_export", 
                     value="export_academic", 
                     label="📄 Academic Export"),
            cl.Action(name="framework_fit", 
                     value="assess_fit", 
                     label="🎯 Framework Fit Assessment"),
            cl.Action(name="evidence_extraction", 
                     value="extract_evidence", 
                     label="🔍 Evidence Extraction")
        ]
        
        await cl.Message(
            content="**Choose a validation research function:**",
            actions=actions
        ).send()
        
    except Exception as e:
        error_message = f"""
## ❌ **Validation Workbench Initialization Error**

**Error**: {str(e)}

**Troubleshooting Steps**:
1. Check database connection: `python check_database.py`
2. Verify environment setup: Check `.env` file exists
3. Test framework loading: `python -c "from src.narrative_gravity.framework_manager import FrameworkManager; print('OK')"`

**Need Help?** Check `LAUNCH_GUIDE.md` for setup instructions.
        """
        await cl.Message(content=error_message).send()

@cl.action_callback("validation_experiment")
async def start_validation_experiment(action):
    """Start a new validation experiment workflow"""
    await cl.Message(content="""# 🧪 **Validation Experiment Designer**

## **Step 1: Experiment Configuration**

Please specify your validation experiment parameters:

### **Text Corpus Selection**
- **Single Text**: Paste text directly for focused analysis
- **Multi-Text**: Describe corpus (e.g., "presidential inaugural addresses 1861-2021")
- **Comparative**: Specify texts to compare (e.g., "Lincoln vs Trump rhetoric")

### **Framework Configuration**
- **Target Framework**: Which framework to validate 
- **Variant Testing**: Test different weighting configurations?
- **Cross-Framework**: Compare multiple frameworks?

### **LLM Configuration**  
- **Model Selection**: Which LLMs to include (GPT-4, Claude, Mistral, Gemini)
- **Consensus Target**: Target correlation threshold (default: >0.90)
- **Runs per Model**: Number of runs for statistical validation (default: 3)

### **Quality Gates**
- **Framework Fit**: Minimum fit threshold (default: 0.7)
- **Evidence Quality**: Supporting passage requirements
- **Statistical Significance**: P-value threshold (default: 0.05)

**Example**: "Create experiment comparing Fukuyama Identity Framework analysis of Lincoln 1865 vs Trump 2015 speeches using GPT-4 and Claude with 3 runs each"

**What validation experiment would you like to design?**
""").send()

@cl.action_callback("framework_comparison")
async def compare_frameworks(action):
    """Start framework comparison analysis"""
    frameworks = framework_manager.list_frameworks() if framework_manager else []
    framework_list = "\n".join([f"   • **{fw['name']}**: {fw['description'][:100]}..." for fw in frameworks])
    
    await cl.Message(content=f"""# ⚖️ **Framework Comparison Analysis**

## **Available Frameworks for Comparison**
{framework_list}

## **Comparison Methodologies**

### **Single Text, Multiple Frameworks**
Analyze the same text across different frameworks to understand dimensional differences.

**Example**: "Compare civic_virtue vs fukuyama_identity analysis of Obama 2008 victory speech"

### **Framework Sensitivity Analysis**
Test how different frameworks respond to similar content types.

**Example**: "Compare framework responses to populist vs establishment rhetoric"

### **Cross-Framework Correlation Study**
Measure correlation between framework outputs across text corpus.

**Example**: "Correlate political_spectrum and fukuyama_identity scores across presidential speech corpus"

**What framework comparison would you like to conduct?**
""").send()

@cl.action_callback("batch_analysis")
async def batch_analysis(action):
    """Start batch processing workflow"""
    await cl.Message(content="""# 📊 **Batch Analysis Configuration**

## **Batch Processing Capabilities**

### **Text Corpus Processing**
- **Upload Multiple Files**: Process entire document collections
- **Systematic Analysis**: Apply consistent framework across corpus
- **Metadata Integration**: Include speaker, date, context information
- **Quality Control**: Automatic framework fit assessment

### **Multi-LLM Validation**
- **Parallel Processing**: Run multiple models simultaneously  
- **Consensus Analysis**: Measure cross-model agreement
- **Statistical Validation**: Generate confidence intervals
- **Evidence Extraction**: Collect supporting passages

### **Progress Monitoring**
- **Real-time Updates**: Track analysis completion
- **Cost Monitoring**: API usage and expense tracking
- **Quality Gates**: Automatic filtering of poor-fit results
- **Error Handling**: Graceful failure recovery

## **Batch Analysis Examples**

**Example 1**: Historical Trend Analysis
```
Corpus: Presidential speeches 1789-2025
Framework: fukuyama_identity
Models: GPT-4, Claude-3-Sonnet
Output: Temporal trend analysis of democratic identity rhetoric
```

**Example 2**: Cross-Cultural Validation
```
Corpus: Democratic speeches from US, UK, Canada, Australia
Framework: civic_virtue
Models: All available
Output: Cross-cultural democratic values comparison
```

**What batch analysis would you like to configure?**
""").send()

@cl.action_callback("academic_export")
async def academic_export(action):
    """Handle academic export requests"""
    await cl.Message(content="""# 📄 **Academic Export Tools**

## **Export Formats Available**

### **Statistical Software Formats**
- **R Package**: Complete datasets with analysis scripts
- **Python/Pandas**: Jupyter notebooks with replication code
- **SPSS/Stata**: Native format exports with variable labels
- **CSV/JSON**: Raw data for custom analysis

### **Publication-Ready Outputs**
- **Methodology Documentation**: Complete replication package
- **Statistical Reports**: Correlation matrices, significance tests
- **Evidence Tables**: Supporting passages organized by framework dimensions
- **Visualization Data**: Chart-ready datasets with formatting

### **Academic Validation**
- **Inter-rater Reliability**: Human vs LLM comparison metrics
- **Cross-model Consensus**: Statistical agreement analysis
- **Confidence Intervals**: Uncertainty quantification
- **Replication Instructions**: Step-by-step methodology

## **Export Examples**

**Example 1**: Paper Replication Package
```
Content: Complete fukuyama_identity validation study
Format: R package with raw data, analysis scripts, methodology
Includes: Cross-LLM correlations, evidence passages, temporal trends
```

**Example 2**: Supplementary Materials
```
Content: Framework comparison across political speech corpus  
Format: CSV + metadata + Jupyter notebook
Includes: Statistical significance tests, visualization code
```

**What would you like to export for academic publication?**
""").send()

@cl.action_callback("framework_fit")
async def assess_framework_fit(action):
    """Framework fit assessment tool"""
    await cl.Message(content="""# 🎯 **Framework Fit Assessment**

## **Quality Gate System**

### **Automatic Fit Detection**
The system automatically assesses whether texts are appropriate for analysis with specific frameworks:

- **High Fit (0.8-1.0)**: Framework highly appropriate
- **Medium Fit (0.6-0.8)**: Framework applicable with caution  
- **Low Fit (0.4-0.6)**: Framework marginally applicable
- **Poor Fit (0.0-0.4)**: Framework inappropriate - alternative suggested

### **Fit Assessment Criteria**
- **Content Relevance**: Does text contain framework-relevant themes?
- **Conceptual Alignment**: Are framework dimensions meaningful for this content?
- **Historical Context**: Is framework appropriate for time period/culture?
- **Text Type**: Does framework suit the genre (speech, policy, media, etc.)?

## **Example Assessments**

### **High Fit Example**
```
Text: Political campaign speech
Framework: fukuyama_identity  
Fit Score: 0.95
Reason: Rich identity rhetoric, recognition dynamics, thymos elements
```

### **Poor Fit Example**  
```
Text: Shakespeare's Sonnet 18
Framework: fukuyama_identity
Fit Score: 0.15
Reason: Romantic poetry lacks political identity content
Alternative: Consider literary_analysis framework
```

## **Quality Control Benefits**
- **Research Integrity**: Prevents meaningless analyses
- **Academic Credibility**: Ensures appropriate framework application
- **Resource Efficiency**: Avoids wasted LLM API calls
- **Confidence Building**: Validates analytical choices

**What text would you like to assess for framework fit?**
""").send()

@cl.action_callback("evidence_extraction")
async def extract_evidence(action):
    """Evidence extraction and quality assessment"""
    await cl.Message(content="""# 🔍 **Evidence Extraction & Quality Assessment**

## **Supporting Passage Analysis**

### **Automated Evidence Collection**
- **High-Score Passages**: Extracts text supporting framework dimensions with scores >0.7
- **Contextual Quotes**: Maintains sentence-level context around key phrases
- **Attribution**: Links evidence to specific framework wells and scoring rationale
- **Quality Scoring**: Assesses strength and relevance of supporting evidence

### **Cross-LLM Evidence Consensus**
- **Passage Agreement**: Measures how often multiple LLMs identify same evidence
- **Scoring Consistency**: Validates that evidence supports consistent scoring
- **Explanation Quality**: Evaluates coherence of LLM reasoning for passage selection
- **Quote Reliability**: Identifies most robust supporting evidence across models

## **Evidence Quality Metrics**

### **Relevance Scoring**
- **Direct Relevance**: Quote explicitly demonstrates framework dimension
- **Implicit Relevance**: Quote requires inference to support dimension
- **Contextual Relevance**: Quote meaningful only within broader context
- **Spurious Relevance**: Quote identified incorrectly

### **Coherence Assessment**
- **Logical Connection**: Clear link between quote and framework dimension
- **Explanatory Power**: Quote effectively illustrates concept
- **Semantic Precision**: Quote accurately represents claimed meaning
- **Academic Standards**: Quote suitable for scholarly citation

## **Example Evidence Extraction**

### **Text**: Lincoln's Second Inaugural
**Framework**: fukuyama_identity
**Dimension**: Integrative Recognition (Score: 0.9)

**Evidence**: "With malice toward none, with charity for all"
**Quality**: High (0.95) - Directly demonstrates integrative recognition
**LLM Consensus**: 3/3 models identified this passage
**Academic Suitability**: Excellent - clear, quotable, representative

**What text would you like to analyze for evidence extraction?**
""").send()

@cl.on_message
async def main(message: cl.Message):
    """Handle validation workbench interactions"""
    global bot
    
    if not bot:
        await cl.Message(content="❌ Bot not initialized. Please refresh the page.").send()
        return
    
    # Show typing indicator
    async with cl.Step(name="processing", type="tool") as step:
        step.input = message.content
        
        try:
            # Process message through validation-enhanced bot
            response = await process_validation_message(message.content)
            step.output = response
            
        except Exception as e:
            error_response = f"""
## ⚠️ **Processing Error**

**Error**: {str(e)}

**Validation Workbench Status**: Active
**Suggestion**: Try rephrasing your request or use one of the action buttons above.

**Common Commands**:
- "Switch to [framework_name] framework"
- "Analyze: [paste your text here]"
- "Create validation experiment with [specification]"
- "Compare [text1] vs [text2] using [framework]"
"""
            step.output = error_response
            await cl.Message(content=error_response).send()
            return
    
    await cl.Message(content=response).send()

async def process_validation_message(message_content: str) -> str:
    """Enhanced message processing for validation workbench functionality"""
    global bot, framework_manager
    
    # Handle validation experiment commands
    if "validation experiment" in message_content.lower() or "create experiment" in message_content.lower():
        return handle_experiment_creation(message_content)
    
    # Handle framework fit assessment
    if "framework fit" in message_content.lower() or "assess fit" in message_content.lower():
        return handle_fit_assessment(message_content)
    
    # Handle batch analysis requests
    if "batch analysis" in message_content.lower() or "batch process" in message_content.lower():
        return handle_batch_analysis(message_content)
    
    # Handle academic export requests
    if "export" in message_content.lower() and any(word in message_content.lower() for word in ["academic", "publication", "csv", "json", "r package"]):
        return handle_academic_export(message_content)
    
    # Handle cross-LLM comparison requests
    if "cross-llm" in message_content.lower() or "compare models" in message_content.lower():
        return handle_cross_llm_analysis(message_content)
    
    # Default to standard bot processing with validation context
    response = bot.process_message(message_content)
    
    # Enhance response with validation context if this was an analysis
    if "analysis complete" in response.lower() or "framework:" in response.lower():
        response += "\n\n---\n**🧪 Validation Options**: Use action buttons above for batch processing, cross-model validation, or academic export of this analysis."
    
    return response

def handle_experiment_creation(message: str) -> str:
    """Handle validation experiment creation requests"""
    return f"""# 🧪 **Validation Experiment Created**

**Experiment Configuration Detected**:
```
Request: {message[:200]}...
Status: Configuration Phase
Next Steps: Specify corpus, models, and validation parameters
```

## **Experiment Design Template**

### **Phase 1: Design Configuration**
- **Text Corpus**: [Specify texts or collection]
- **Framework**: [Target framework for validation]
- **Models**: [LLM selection for cross-validation]
- **Metrics**: [Correlation targets and quality gates]

### **Phase 2: Execution Plan**
- **Batch Size**: [Number of texts per processing batch]
- **Timeout Settings**: [Per-analysis time limits]
- **Quality Gates**: [Framework fit thresholds]
- **Cost Limits**: [API usage budgets]

### **Phase 3: Analysis Specification**
- **Statistical Tests**: [Correlation, significance testing]
- **Evidence Extraction**: [Supporting passage requirements]
- **Export Format**: [Academic publication requirements]

**To proceed**: Please specify your corpus, model selection, and validation targets. 

**Example**: "Use presidential inaugural addresses 1861-2021, test fukuyama_identity framework with GPT-4 and Claude, target >0.90 correlation, export R package for academic publication"
"""

def handle_fit_assessment(message: str) -> str:
    """Handle framework fit assessment requests"""
    return f"""# 🎯 **Framework Fit Assessment**

**Assessment Request**: {message[:100]}...

## **Fit Analysis Protocol**

### **Step 1: Content Analysis**
- **Genre Detection**: Speech, policy, media, academic, etc.
- **Theme Identification**: Political, cultural, economic content
- **Context Evaluation**: Historical period, audience, purpose

### **Step 2: Framework Alignment**
- **Dimensional Relevance**: Are framework concepts present?
- **Conceptual Appropriateness**: Do dimensions make sense for this content?
- **Analytical Value**: Will analysis produce meaningful insights?

### **Step 3: Quality Gate Application**
- **Fit Score Calculation**: 0.0-1.0 appropriateness rating
- **Threshold Evaluation**: Meets minimum standards?
- **Alternative Suggestions**: Better framework options if score low

## **Assessment Results Template**
```
Text: [Title/Description]
Framework: [Framework Name]
Fit Score: [0.0-1.0]
Confidence: [High/Medium/Low]
Recommendation: [Proceed/Caution/Alternative]
Reasoning: [Detailed explanation]
```

**To perform assessment**: Please provide the text you'd like evaluated for framework appropriateness.
"""

def handle_batch_analysis(message: str) -> str:
    """Handle batch analysis requests"""
    return f"""# 📊 **Batch Analysis Configuration**

**Batch Request**: {message[:100]}...

## **Batch Processing Workflow**

### **Phase 1: Corpus Preparation**
- **Text Collection**: Upload or specify text sources
- **Metadata Integration**: Speaker, date, context, audience
- **Quality Preprocessing**: Encoding, length, format validation
- **Corpus Statistics**: Size, distribution, characteristics

### **Phase 2: Analysis Configuration**
- **Framework Selection**: Primary and comparative frameworks
- **Model Configuration**: LLM selection and parameters
- **Batch Settings**: Parallel processing, error handling
- **Quality Gates**: Fit thresholds, timeout settings

### **Phase 3: Execution Monitoring**
- **Progress Tracking**: Real-time completion status
- **Quality Control**: Automatic fit assessment
- **Cost Monitoring**: API usage and budget tracking
- **Error Management**: Failed analysis handling

### **Phase 4: Results Compilation**
- **Statistical Analysis**: Cross-text patterns, trends
- **Consensus Measurement**: Inter-model agreement
- **Evidence Compilation**: Supporting passage collection
- **Export Preparation**: Academic format generation

## **Batch Analysis Examples**

**Example 1**: Temporal Trend Study
```
Corpus: Presidential speeches 1789-2025 (200+ texts)
Framework: fukuyama_identity
Models: GPT-4, Claude-3-Sonnet
Analysis: Democratic identity evolution over time
Output: R package with temporal trend analysis
```

**To configure batch analysis**: Specify your text corpus, framework, model selection, and desired outputs.
"""

def handle_academic_export(message: str) -> str:
    """Handle academic export requests"""
    return f"""# 📄 **Academic Export Generator**

**Export Request**: {message[:100]}...

## **Publication-Ready Export Options**

### **Data Formats**
- **CSV/TSV**: Raw analysis results with metadata
- **JSON**: Structured data with nested analysis details
- **R Package**: Complete dataset with analysis scripts
- **Python/Pandas**: Jupyter notebooks with replication code

### **Statistical Supplements**
- **Correlation Matrices**: Cross-model agreement analysis
- **Significance Testing**: P-values, confidence intervals
- **Reliability Metrics**: Inter-rater, test-retest consistency
- **Effect Size Calculations**: Practical significance measures

### **Evidence Documentation**
- **Supporting Passages**: Organized by framework dimension
- **Quote Attributions**: Source, context, relevance scores
- **Consensus Evidence**: Cross-model agreement on key passages
- **Quality Assessments**: Evidence strength and reliability

### **Methodology Package**
- **Replication Instructions**: Step-by-step analysis procedure
- **Parameter Documentation**: Framework settings, model configurations
- **Validation Protocols**: Quality gates, fit assessments
- **Computational Environment**: Software versions, dependencies

## **Export Template**
```
Analysis: [Description]
Timeframe: [Analysis period]
Frameworks: [Framework(s) used]
Models: [LLM models included]
Texts: [Number and type of texts analyzed]
Format: [Requested export format]
Purpose: [Academic paper, replication, etc.]
```

**To generate export**: Specify which analysis results you need in academic format and your intended use case.
"""

def handle_cross_llm_analysis(message: str) -> str:
    """Handle cross-LLM validation requests"""
    return f"""# 🤖 **Cross-LLM Validation Analysis**

**Validation Request**: {message[:100]}...

## **Multi-Model Consensus Protocol**

### **Model Selection**
- **GPT-4 Family**: GPT-4, GPT-4-Turbo, GPT-4o
- **Claude Family**: Claude-3-Opus, Claude-3-Sonnet, Claude-3-Haiku
- **Mistral Family**: Mistral-Large, Mistral-Medium
- **Gemini Family**: Gemini-Pro, Gemini-Ultra (when available)

### **Consensus Metrics**
- **Correlation Analysis**: Pearson correlations across model pairs
- **Agreement Thresholds**: Target >0.90 for high confidence
- **Outlier Detection**: Identify models with divergent scoring
- **Confidence Intervals**: Statistical uncertainty quantification

### **Validation Targets**
- **Score Consistency**: Similar numerical scores across models
- **Dimension Agreement**: Consistent identification of key themes
- **Evidence Consensus**: Agreement on supporting passages
- **Explanation Coherence**: Consistent analytical reasoning

## **Cross-LLM Results Template**
```
Text: [Analysis target]
Framework: [Framework used]
Models: [List of LLMs tested]
Correlation Matrix: [Model-pair correlations]
Consensus Score: [Overall agreement 0.0-1.0]
High-Agreement Dimensions: [List]
Divergent Results: [Areas of disagreement]
Evidence Consensus: [Agreed-upon supporting quotes]
Confidence Level: [High/Medium/Low]
Recommendation: [Proceed/Review/Revise]
```

**To run cross-LLM validation**: Specify your text, framework, and which models to include in the consensus analysis.
""" 