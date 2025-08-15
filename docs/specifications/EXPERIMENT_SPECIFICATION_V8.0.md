# Experiment Specification (v8.0)

**Version**: 8.0  
**Status**: Current Standard  
**Replaces**: v7.3

The `experiment.md` file is a Markdown file with YAML appendix that defines the complete scope of a v8.0 analysis run. It acts as the **single source of truth** for an experiment, telling the Discernus v8.0 system what framework to use, what corpus to analyze, and what research questions to investigate.

**Design Philosophy**: Human-first readability with LLM-friendly generation and machine-parseable structure.

---

## 1. File Structure & Location

The experiment file MUST be a Markdown file named `experiment.md` located at the root of a project directory, alongside all experiment input files.

```
my_research_project/
├── experiment.md                 # Experiment specification (standard name)
├── corpus.md                     # Corpus specification (standard name)  
├── cff_v8.md                     # Framework file (descriptive name)
└── corpus/                       # Document directory (text files only)
    ├── document1.txt
    ├── document2.txt
    └── document3.txt
```

**Key Principles:**
- All experiment inputs at project root (simple discovery)
- Standard names for core files (`experiment.md`, `corpus.md`)
- Descriptive names for framework files (referenced in experiment.md)
- Text files only in corpus directory (keep it simple)

---

## 2. File Format

The file follows the **human-first** format: natural language description followed by YAML configuration appendix.

```markdown
# Democratic Discourse Analysis

This experiment analyzes political speeches to understand how different rhetorical styles contribute to democratic flourishing. We examine institutional vs. populist approaches across temporal and partisan dimensions.

## Research Questions
- How do institutional and populist communication styles differ in their democratic impact?
- What rhetorical patterns emerge across temporal sequences?
- Do progressive and conservative populist variants show different cohesion patterns?

## Expected Outcomes
Statistical analysis of dimensional scores with longitudinal trends and speaker-type comparisons...

---

## Configuration

```yaml
name: "democratic_discourse_analysis"
framework: "cff_v8.md"
corpus: "corpus.md"
version: "8.0"
```
```

---

## 3. Field Specifications

### **name** (Required)
- **Type**: String
- **Format**: Snake_case identifier
- **Purpose**: Machine-readable experiment identifier
- **Example**: `"democratic_discourse_cohesion_study"`
- **Constraints**: Must be unique within project, no spaces or special characters

### **description** (Required)  
- **Type**: String
- **Purpose**: Human-readable explanation of research objectives
- **Example**: `"Comparative analysis of social cohesion patterns across institutional and populist democratic discourse styles"`
- **Constraints**: Should be 1-2 sentences, focus on what is being studied

### **framework** (Required)
- **Type**: String (File Path)
- **Purpose**: Path to the v8.0 framework specification
- **Example**: `"frameworks/reference/flagship/cff_v8.md"`
- **Constraints**: Must point to valid v8.0 framework file, path relative to project root

### **corpus** (Required)
- **Type**: String (File Path)  
- **Purpose**: Path to the v8.0 corpus specification
- **Example**: `"corpus/corpus_v8.md"`
- **Constraints**: Must point to valid v8.0 corpus file, path relative to experiment root

### **questions** (Required)
- **Type**: Array of Strings
- **Purpose**: Research questions the experiment aims to answer
- **Example**: 
  ```yaml
  questions:
    - "Will McCain's institutional discourse show higher cohesion than populist styles?"
    - "Do populist progressive and conservative variants differ in social cohesion patterns?"
  ```
- **Constraints**: Minimum 1 question, maximum 5 questions, each should be specific and answerable

---

## 4. Validation Rules

### File Validation
- ✅ File must be named `experiment_v8.md`
- ✅ File must contain valid YAML syntax
- ✅ File must be located in experiment root directory

### Schema Validation
- ✅ All required fields must be present: `name`, `description`, `framework`, `corpus`, `questions`
- ✅ `name` must be valid identifier (no spaces, special characters)
- ✅ `framework` path must exist and point to valid v8.0 framework
- ✅ `corpus` path must exist and point to valid v8.0 corpus
- ✅ `questions` must contain at least 1 research question

### Content Validation
- ✅ Framework file must comply with Framework Specification v8.0
- ✅ Corpus file must comply with Corpus Specification v8.0  
- ✅ Research questions should be specific and investigable
- ✅ Description should clearly state research objectives

---

## 5. Migration from v7.3

### Key Changes
- **File Name**: `experiment.md` → `experiment_v8.md`
- **Framework Path**: Now relative to project root (not experiment root)
- **Corpus Path**: Now points to `corpus_v8.md` (not `corpus.md`)
- **Added Field**: `questions` array for research questions
- **Removed Fields**: `model_overrides`, `analysis_config`, `synthesis_config`

### Migration Steps
1. **Rename file** from `experiment.md` to `experiment_v8.md`
2. **Update framework path** to be relative to project root
3. **Update corpus path** to point to `corpus_v8.md`
4. **Add questions array** with specific research questions
5. **Remove deprecated fields** (model_overrides, analysis_config, etc.)

### Compatibility
- **v8.0 experiments** are NOT compatible with v7.3 orchestration systems
- **v7.3 experiments** are NOT compatible with v8.0 notebook generation pipeline
- **No automatic migration** - experiments must be manually updated

---

## 6. Example v8.0 Experiment

```yaml
name: "democratic_discourse_cohesion_study"

description: "Comparative analysis of social cohesion patterns across institutional and populist democratic discourse styles"

framework: "frameworks/reference/flagship/cff_v8.md"

corpus: "corpus/corpus_v8.md"

questions:
  - "Will McCain's institutional discourse show higher cohesion than populist styles?"
  - "Do populist progressive and conservative variants differ in social cohesion patterns?"
  - "What derived metrics best distinguish institutional from populist discourse?"
```

---

## 7. Integration with v8.0 Pipeline

### Analysis Flow
1. **Specification Loading**: v8.0 loader reads raw experiment content
2. **Framework Resolution**: Resolves framework path and loads v8.0 framework
3. **Corpus Resolution**: Resolves corpus path and loads v8.0 corpus
4. **Question Integration**: Research questions guide analysis focus
5. **Function Generation**: Automated agents generate analysis functions
6. **Notebook Assembly**: Universal template creates executable notebook

### CLI Integration
```bash
# v8.0 experiments are automatically detected by experiment_v8.md filename
discernus run --statistical-prep

# Or explicitly specify v8.0 mode
discernus run --statistical-prep --experiment-file experiment_v8.md
```

### Validation Integration
```bash
# Validate v8.0 experiment structure
discernus validate --v8

# Validate all components (experiment, framework, corpus)
discernus validate --v8 --comprehensive
```

---

## 8. Best Practices

### Experiment Design
- **Clear Objectives**: Write specific, testable research questions
- **Focused Scope**: Limit to 3-5 related research questions
- **Appropriate Framework**: Choose framework that matches research goals
- **Quality Corpus**: Ensure corpus contains relevant documents

### File Organization
- **Consistent Naming**: Use descriptive, machine-readable identifiers
- **Logical Structure**: Organize corpus documents meaningfully
- **Version Control**: Track all changes to experiment specifications
- **Documentation**: Include README explaining experiment context

### Research Questions
- **Specific**: Avoid vague or overly broad questions
- **Answerable**: Ensure questions can be addressed with available data
- **Focused**: Each question should target specific aspects
- **Complementary**: Questions should build on each other logically

This v8.0 specification prioritizes simplicity and human readability while maintaining the rigor needed for systematic research.
