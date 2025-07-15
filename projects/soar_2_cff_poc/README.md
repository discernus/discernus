# SOAR CFF Sample Project
## Comparative Analysis of Political Rhetoric Across Dignity and Tribal Dimensions

This sample project demonstrates the complete SOAR (Simple Atomic Orchestration Research) workflow using the CFF v3.1 framework to analyze political discourse across ideological and rhetorical dimensions.

---

## Quick Start

### 1. Validate the Project
```bash
python3 discernus_cli.py validate ./examples/soar_cff_sample_project
```

### 2. Execute the Analysis
```bash
python3 discernus_cli.py execute ./examples/soar_cff_sample_project --dev-mode
```

### 3. View Results
Results will be saved in `./examples/soar_cff_sample_project/results/` with timestamped folders containing:
- `conversation_readable.md` - Human-readable analysis
- `conversation_log.jsonl` - Complete conversation log
- `metadata.json` - Execution metadata

---

## Project Structure

```
soar_cff_sample_project/
├── framework.md                    # CFF v3.1 framework specification
├── experiment.md                   # Research design and methodology
├── corpus/                         # Text files for analysis
│   ├── manifest.yaml              # Corpus metadata and configuration
│   ├── conservative_dignity_mccain_2008_concession.txt
│   ├── conservative_dignity_romney_2020_impeachment.txt
│   ├── progressive_dignity_booker_2018_first_step_act.txt
│   ├── progressive_dignity_lewis_1963_march_washington.txt
│   ├── conservative_tribalism_king_2017_house.txt
│   ├── conservative_tribalism_vance_nat_con.txt
│   ├── progressive_tribalism_aoc_2025_fighting_oligarchy.txt
│   └── progressive_tribalism_sanders_2025_fighting_oligarchy.txt
├── results/                        # Generated during execution
└── README.md                      # This file
```

---

## Research Design

### Research Question
How do political speeches from different ideological orientations (conservative dignity, progressive dignity, conservative tribalism, progressive tribalism) differ in their social cohesion patterns as measured by the CFF v3.1 framework?

### Corpus Overview
- **8 Political Speeches** across 4 ideological categories
- **Time Span**: 1963-2025 (62 years of American political discourse)
- **Balance**: 2 speeches per category for comparative analysis
- **Diversity**: Different speakers, contexts, and rhetorical situations

### Expected Findings
1. **Dignity speeches** should show higher CFF Cohesion Index scores than tribal speeches
2. **Conservative and progressive dignity** should show similar cohesion patterns
3. **Identity Axis** should be the strongest discriminator between dignity and tribal categories

---

## Framework Details

### CFF v3.1 Framework
- **Identity Axis**: Individual Dignity ↔ Tribal Dominance
- **Fear-Hope Axis**: Threat Perception ↔ Optimistic Possibility
- **Envy-Compersion Axis**: Elite Resentment ↔ Others' Success Celebration
- **Enmity-Amity Axis**: Interpersonal Hostility ↔ Social Goodwill
- **Goal Axis**: Fragmentative Power ↔ Cohesive Generosity

### CFF Cohesion Index
Composite score combining four core dimensions:
```
CFF_Cohesion_Index = 0.25(Hope-Fear) + 0.20(Compersion-Envy) + 0.30(Amity-Enmity) + 0.25(Cohesive_Goal-Fragmentative_Goal)
```

---

## Sample Texts

### Conservative Dignity
- **John McCain 2008 Concession Speech**: Gracious defeat acknowledgment emphasizing democratic norms
- **Mitt Romney 2020 Impeachment Vote**: Principled constitutional stance despite party pressure

### Progressive Dignity
- **Cory Booker 2018 First Step Act**: Bipartisan criminal justice reform advocacy
- **John Lewis 1963 March on Washington**: Civil rights appeal emphasizing universal human dignity

### Conservative Tribalism
- **Steve King 2017 House Speech**: Immigration policy debate with exclusionary rhetoric
- **J.D. Vance National Conservative Conference**: Cultural populism and group identity politics

### Progressive Tribalism
- **Alexandria Ocasio-Cortez 2025 Fighting Oligarchy Rally**: Economic populism with elite targeting
- **Bernie Sanders 2025 Fighting Oligarchy Rally**: Class-based political mobilization

---

## Validation Requirements

### Structural Validation
- ✅ framework.md exists and contains CFF v3.1 specification
- ✅ experiment.md exists and meets experiment rubric requirements
- ✅ corpus/ directory contains 8 text files
- ✅ manifest.yaml provides corpus metadata

### Content Validation
- ✅ Framework specification passes validation rubric (>85% completeness)
- ✅ Experiment design passes validation rubric (>90% completeness)
- ✅ Corpus contains adequate texts for comparative analysis
- ✅ Framework and experiment are aligned and compatible

---

## Usage Examples

### Basic Validation
```bash
# Validate project structure and content
python3 discernus_cli.py validate ./examples/soar_cff_sample_project

# Interactive validation with issue resolution
python3 discernus_cli.py validate ./examples/soar_cff_sample_project --interactive

# Verbose validation output
python3 discernus_cli.py validate ./examples/soar_cff_sample_project --verbose
```

### Analysis Execution
```bash
# Standard execution
python3 discernus_cli.py execute ./examples/soar_cff_sample_project

# Development mode with simulated researcher
python3 discernus_cli.py execute ./examples/soar_cff_sample_project --dev-mode

# Auto-validate before execution
python3 discernus_cli.py execute ./examples/soar_cff_sample_project --auto-validate
```

### System Information
```bash
# List available frameworks
python3 discernus_cli.py list-frameworks

# Show system information
python3 discernus_cli.py info

# Check THIN compliance
python3 discernus_cli.py info --check-thin
```

---

## Expected Results

### Quantitative Predictions
- **Dignity Speeches**: Mean CFF Cohesion Index > +0.2
- **Tribal Speeches**: Mean CFF Cohesion Index < -0.2
- **Effect Size**: Cohen's d > 0.8 (large effect) for dignity vs. tribal difference
- **Identity Axis**: Strongest discriminator with effect size > 1.0

### Qualitative Patterns
- **Dignity**: Inclusive language, optimistic framing, unity-building goals
- **Tribal**: Exclusionary language, threat framing, zero-sum competition
- **Cross-Ideological**: Similar patterns within dignity and tribal categories regardless of conservative/progressive orientation

---

## Customization Guide

### Using Your Own Corpus
1. Replace files in `corpus/` directory with your own `.txt` files
2. Update `corpus/manifest.yaml` with your text metadata
3. Modify `experiment.md` to reflect your research question
4. Keep `framework.md` unchanged (or substitute your own framework)

### Different Framework
1. Replace `framework.md` with your framework specification
2. Ensure framework follows Framework Specification v3.1 format
3. Update `experiment.md` to align with your framework
4. Modify `corpus/manifest.yaml` framework requirements if needed

### Alternative Research Design
1. Modify `experiment.md` with your research question and hypotheses
2. Update corpus selection and categorization in `manifest.yaml`
3. Adjust expected outcomes and statistical analysis plan
4. Ensure alignment between framework capabilities and research objectives

---

## Troubleshooting

### Validation Errors
- **Framework not found**: Check that `framework.md` exists and is readable
- **Experiment incomplete**: Ensure all required sections are present in `experiment.md`
- **Corpus empty**: Verify `.txt` files exist in `corpus/` directory
- **Alignment issues**: Check that framework and experiment are compatible

### Execution Errors
- **LLM connection**: Verify API keys and network connectivity
- **Memory issues**: Consider reducing corpus size or batch size
- **Timeout errors**: Increase timeout settings or reduce complexity

### Common Issues
- **File permissions**: Ensure read/write access to project directory
- **Dependencies**: Install required packages from `requirements.txt`
- **Path issues**: Use absolute paths if relative paths cause problems

---

## Learning Objectives

### For Researchers
1. **SOAR Workflow**: Understand complete project structure and execution
2. **Framework Application**: Learn how to apply CFF v3.1 to political discourse
3. **Comparative Analysis**: Master techniques for cross-categorical research
4. **Validation Standards**: Appreciate rigorous quality control in computational research

### For Developers
1. **THIN Principles**: See how software provides infrastructure while LLMs provide intelligence
2. **Framework Agnostic**: Understand how SOAR works with any analytical framework
3. **Validation System**: Learn comprehensive project validation techniques
4. **CLI Architecture**: Study command-line interface design for research tools

### For Students
1. **Computational Social Science**: Introduction to systematic text analysis
2. **Research Design**: Learn experimental methodology for political discourse
3. **Statistical Analysis**: Understand comparative analysis and hypothesis testing
4. **Academic Standards**: Appreciate replication and transparency requirements

---

## Academic Context

This sample project demonstrates several important methodological innovations:

1. **Framework-Agnostic Analysis**: Shows how the same infrastructure can support different analytical frameworks
2. **Graduated Validation**: Demonstrates progressive quality gates from structure to content
3. **Comparative Methodology**: Illustrates systematic cross-categorical analysis
4. **Computational Reproducibility**: Provides complete provenance and replication capabilities

The project serves as a template for rigorous computational social science research while maintaining the simplicity and accessibility that makes SOAR valuable for researchers at all levels.

---

## Citation

If you use this sample project in your research, please cite:

```
Discernus SOAR CFF Sample Project (2025). "Comparative Analysis of Political Rhetoric 
Across Dignity and Tribal Dimensions: A CFF v3.1 Validation Study." 
Discernus Research Architecture. Available at: https://github.com/discernus/soar
```

---

## Support

For questions or issues with this sample project:
1. Check the troubleshooting section above
2. Review the SOAR documentation in `/docs`
3. Examine the validation output for specific error messages
4. Consider starting with a smaller corpus for testing

Remember: The goal of SOAR is to make world-class computational research as simple as pointing to a folder. This sample project demonstrates that vision in action. 