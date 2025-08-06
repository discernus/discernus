# Score Validation Pipeline Guide

**THIN Implementation for Academic Score Validation**

## Overview

The **Score Validation Pipeline** provides <5 minute academic validation for any numerical score from computational social science research. It uses **THIN architecture** - delegating validation intelligence to LLM rather than building complex hardcoded logic.

### Key Features

- ✅ **<5 minute validation** - Rapid academic assessment
- ✅ **Framework-agnostic** - Works with any research framework
- ✅ **Model consistency** - Validates against same model used in analysis
- ✅ **Score grounding** - Links numerical claims to textual evidence
- ✅ **Academic standards** - Ensures peer review readiness

## Quick Start

### Basic Validation

```bash
# Validate any score from an experiment
discernus validate-score projects/experiment_name "document.txt" "score_name" --score-value 0.75

# Example: Validate dignity score from McCain concession speech
discernus validate-score projects/simple_test "john_mccain_2008_concession.txt" "dignity_score" --score-value 0.65
```

### Advanced Options

```bash
# Specify confidence level
discernus validate-score projects/simple_test "doc.txt" "score" --score-value 0.75 --confidence 0.9

# Use specific model for validation
discernus validate-score projects/simple_test "doc.txt" "score" --score-value 0.75 --model vertex_ai/gemini-2.5-pro

# Save validation report to file
discernus validate-score projects/simple_test "doc.txt" "score" --score-value 0.75 --output validation_report.md
```

## Validation Report Structure

### Score Grounding
- **Evidence Found**: Whether textual evidence supports the score
- **Primary Evidence**: Key supporting text from the document
- **Grounding Strength**: Quality of evidence linkage (strong/medium/weak)

### Evidence Quality
- **Relevance**: How well evidence matches the score concept
- **Specificity**: Precision of the supporting text
- **Quality Score**: Overall evidence quality (0.0-1.0)

### Academic Validation
- **Methodology Sound**: Whether research methods are appropriate
- **Transparency Adequate**: If methodology is sufficiently documented
- **Peer Review Ready**: Whether validation meets academic standards
- **Validation Confidence**: Overall validation confidence (0.0-1.0)

### Recommendations
- **Specific improvements** for research quality
- **Methodology suggestions** for academic rigor
- **Evidence enhancement** recommendations

## Model Consistency

### Auto-Detection
The pipeline automatically detects the model used in the original analysis:

```bash
🔍 Validating score: dignity_score = 0.65 from john_mccain_2008_concession.txt
📄 Framework: cff_v7.3
🤖 Model: vertex_ai/gemini-2.5-flash-lite (auto-detected)
⏱️  Target: <5 minutes
```

### Consistency Validation
- **Model Match**: Ensures validation uses same model as analysis
- **Framework Version**: Validates framework version compatibility
- **Academic Integrity**: Prevents model mismatch validation

### Override Options
```bash
# Use different model for validation (with warning)
discernus validate-score projects/simple_test "doc.txt" "score" --score-value 0.75 --model vertex_ai/gemini-2.5-pro

# Force validation despite model mismatch
discernus validate-score projects/simple_test "doc.txt" "score" --score-value 0.75 --force
```

## Academic Use Cases

### Peer Review
```bash
# Reviewer validates computational claims
discernus validate-score projects/populism_study "trump_speech.txt" "populism_score" --score-value 0.85
```

### Research Development
```bash
# Framework developer tests scoring methodology
discernus validate-score projects/framework_test "sample_doc.txt" "test_score" --score-value 0.6
```

### Quality Assurance
```bash
# Automated validation in research pipeline
python3 -c "
from discernus.orchestration.score_validation_orchestrator import ScoreValidationOrchestrator
orchestrator = ScoreValidationOrchestrator()
result = orchestrator.validate_score(request)
print(f'Validation confidence: {result.academic_validation.get(\"validation_confidence\", 0.0)}')
"
```

## THIN Architecture

### Design Principles
- **LLM Intelligence**: Delegates validation to LLM rather than hardcoded logic
- **Framework Agnostic**: Works with any research framework
- **Durable Infrastructure**: Simple, maintainable code
- **Cost Effective**: Uses appropriate models for validation tasks

### Implementation
```python
# THIN orchestrator delegates to LLM
orchestrator = ScoreValidationOrchestrator(model="vertex_ai/gemini-2.5-flash-lite")
result = orchestrator.validate_score(request)

# Externalized YAML prompts for customization
# See: discernus/orchestration/score_validation_prompt.yaml
```

### Integration Points
- **CLI Interface**: Standalone academic tool
- **Programmatic API**: Integrated into research pipelines
- **Quality Gates**: Automated validation checkpoints
- **Audit Logging**: Provenance tracking for validation

## Performance Targets

### Speed
- **Target**: <5 minutes for complete validation
- **Typical**: 3-4 seconds for standard validation
- **Complex**: <30 seconds for multi-document validation

### Quality
- **Score Grounding**: 95%+ evidence linkage success
- **Academic Standards**: 90%+ peer review readiness
- **Model Consistency**: 100% model match validation

### Cost
- **Flash Lite**: $0.001-0.005 per validation
- **Pro Model**: $0.01-0.05 per validation (for complex cases)
- **Batch Validation**: 10x cost reduction for multiple scores

## Troubleshooting

### Common Issues

**Model Mismatch Error**
```bash
❌ Validation failed: Model mismatch: Analysis used 'vertex_ai/gemini-2.5-flash', validation using 'vertex_ai/gemini-2.5-pro'
```
**Solution**: Use `--model vertex_ai/gemini-2.5-flash` or let auto-detection work

**Analysis Artifact Not Found**
```bash
❌ Analysis artifact not found for document: document.txt
```
**Solution**: Ensure experiment has been run and artifacts exist in `runs/` directory

**Framework Version Mismatch**
```bash
❌ Validation failed: Framework version mismatch: Analysis used 'v7.1', validation using v7.3
```
**Solution**: Use compatible framework version or update analysis to v7.3

### Debug Mode
```bash
# Enable debug output
export DISCERNUS_DEBUG=1
discernus validate-score projects/simple_test "doc.txt" "score" --score-value 0.75
```

## Best Practices

### For Researchers
1. **Run validation early** in research development
2. **Use consistent models** for analysis and validation
3. **Document framework versions** for reproducibility
4. **Review recommendations** for methodology improvements

### For Reviewers
1. **Validate key scores** before accepting research
2. **Check evidence grounding** for all numerical claims
3. **Assess methodology transparency** for peer review
4. **Use validation reports** in review documentation

### For Developers
1. **Integrate validation** into research pipelines
2. **Customize prompts** for specific frameworks
3. **Monitor performance** and cost metrics
4. **Maintain THIN principles** in extensions

## Examples

### Political Discourse Analysis
```bash
# Validate populism score
discernus validate-score projects/populism_study "trump_speech.txt" "populism_score" --score-value 0.85

# Validate dignity score  
discernus validate-score projects/dignity_study "concession_speech.txt" "dignity_score" --score-value 0.65
```

### Computational Social Science
```bash
# Validate sentiment score
discernus validate-score projects/sentiment_analysis "social_media.txt" "sentiment_score" --score-value 0.72

# Validate coherence score
discernus validate-score projects/coherence_study "policy_document.txt" "coherence_score" --score-value 0.58
```

### Academic Validation
```bash
# Batch validation for peer review
for score in dignity_score tribalism_score truth_score; do
  discernus validate-score projects/study "document.txt" "$score" --score-value 0.75 --output "validation_${score}.md"
done
```

## Technical Details

### File Structure
```
discernus/
├── orchestration/
│   ├── score_validation_orchestrator.py    # THIN orchestrator
│   └── score_validation_prompt.yaml        # Externalized prompts
├── interfaces/
│   └── academic_validation_interface.py    # CLI interface
└── cli.py                                 # Main CLI integration
```

### Dependencies
- **LLMGateway**: Model communication
- **ModelRegistry**: Model management
- **AuditLogger**: Provenance tracking
- **Click**: CLI framework

### Configuration
```yaml
# Global configuration (.discernus.yaml)
validation:
  default_model: vertex_ai/gemini-2.5-flash-lite
  timeout_seconds: 300
  max_retries: 3
  cost_threshold_usd: 0.10
```

## Future Enhancements

### Planned Features
- **Batch validation** for multiple scores
- **Comparative validation** across frameworks
- **Statistical validation** for score distributions
- **Visual validation** reports with charts

### Integration Roadmap
- **Synthesis pipeline** integration
- **Quality gates** in analysis workflows
- **Academic reporting** automation
- **Peer review** tool integration

---

**THIN Architecture**: Delegates intelligence to LLM, provides durable infrastructure, maintains framework agnosticism. 