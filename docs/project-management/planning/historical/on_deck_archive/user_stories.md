🧠 **Essential CLI-Based User Stories:**

- Document and systematize existing batch processing capabilities for academic validation
- Identify workflow gaps in manual prompt iteration + automated analysis pipeline
- Create robust process documentation for hybrid manual/automated research workflows
- Minimal development investment focused on process clarity and data generation
- Support validation-first development strategy through systematic CLI tools

You're absolutely right to leverage your existing CLI infrastructure rather than building elaborate interfaces. Based on your comprehensive backend capabilities and the strategic pivot toward manual iteration + batch processing, here are user stories that build on what you have:

## **User Story 1 (Expanded): Integrated Research Component Development**

### **As a researcher conducting systematic framework and methodology development**

"I want to systematically develop and test variations across prompt templates, framework definitions, and weighting methodologies using manual LLM interaction, while maintaining rigorous version control and experimental provenance in my database, so that I can rapidly iterate toward reliable thematic hierarchy detection while ensuring all components work together effectively."

## **Three Distinct Development Workflows**

### **1. Prompt Template Engineering**

**Manual Development Process:**

- Use Claude/GPT-4 web interfaces for iterative prompt refinement
- Focus on instruction clarity, scoring consistency, and hierarchy detection
- Test hierarchical ranking approaches vs. independent well assessment
- Experiment with evidence extraction requirements and reasoning chains

**Database Integration:**

```sql
-- Extend existing schema for prompt versioning
CREATE TABLE prompt_templates (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    template_content TEXT NOT NULL,
    description TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    parent_version_id UUID REFERENCES prompt_templates(id),
    UNIQUE(name, version)
);
```


### **2. Framework Definition Development**

**Manual Development Process:**

- Conversational framework construction using your established methodology
- Iterative dipole refinement and conceptual clarity enhancement
- Cross-framework compatibility testing and validation
- Framework fit assessment and boundary condition exploration

**Database Integration:**

```sql
-- Your existing framework infrastructure extended
CREATE TABLE framework_versions (
    id UUID PRIMARY KEY,
    framework_name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    dipoles_json JSONB NOT NULL,
    framework_json JSONB NOT NULL,
    description TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    parent_version_id UUID REFERENCES framework_versions(id),
    UNIQUE(framework_name, version)
);
```


### **3. Weighting Methodology Development**

**Manual Development Process:**

- Mathematical approach experimentation (linear averaging, winner-take-most, exponential weighting)
- Dominance hierarchy calculation methods
- Narrative positioning algorithm variations
- Compression of extremes solutions

**Database Integration:**

```sql
-- New component for weighting methodology tracking
CREATE TABLE weighting_methodologies (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    algorithm_description TEXT NOT NULL,
    mathematical_formula TEXT,
    implementation_notes TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    parent_version_id UUID REFERENCES weighting_methodologies(id),
    UNIQUE(name, version)
);
```


## **Enhanced CLI Workflow Integration**

### **Component Selection and Analysis Execution**

```bash
# Enhanced CLI with three-component specification
python analyze_single.py \
  --text golden_set/trump_joint_session.txt \
  --prompt-template hierarchical_ranking:v2.1 \
  --framework civic_virtue:v1.4 \
  --weighting-method winner_take_most:v1.2 \
  --model gpt-4o \
  --output results.json

# Batch analysis with component matrix
python analyze_batch.py \
  --corpus golden_set.jsonl \
  --component-matrix experiment_config.yaml \
  --output batch_results/
```


### **Experimental Configuration Management**

```yaml
# experiment_config.yaml - Component combination matrix
experiment_name: "hierarchical_prompting_validation"
prompt_templates:
  - "hierarchical_ranking:v2.1"
  - "evidence_extraction:v1.3"
frameworks:
  - "civic_virtue:v1.4"
  - "political_spectrum:v2.0"
weighting_methods:
  - "winner_take_most:v1.2"
  - "exponential_decay:v1.0"
models:
  - "gpt-4o"
  - "claude-3.5-sonnet"
runs_per_combination: 3
```


## **Version Compatibility and Tracking**

### **Compatibility Matrix Management**

```sql
-- Track which components work well together
CREATE TABLE component_compatibility (
    id UUID PRIMARY KEY,
    prompt_template_id UUID REFERENCES prompt_templates(id),
    framework_id UUID REFERENCES framework_versions(id),
    weighting_method_id UUID REFERENCES weighting_methodologies(id),
    compatibility_score FLOAT,
    validation_status VARCHAR(20),
    notes TEXT,
    validated_at TIMESTAMP DEFAULT NOW()
);
```


### **Experimental Provenance Enhancement**

```sql
-- Extend your existing experiments table
ALTER TABLE experiments ADD COLUMN prompt_template_id UUID REFERENCES prompt_templates(id);
ALTER TABLE experiments ADD COLUMN framework_version_id UUID REFERENCES framework_versions(id);
ALTER TABLE experiments ADD COLUMN weighting_method_id UUID REFERENCES weighting_methodologies(id);
```


## **Manual Development Documentation Workflow**

### **Development Session Tracking**

```bash
# Start development session with component specification
python start_dev_session.py \
  --component prompt_template \
  --base-version hierarchical_ranking:v2.0 \
  --description "Testing evidence extraction requirements"

# Document development iteration
python log_iteration.py \
  --session-id abc123 \
  --iteration-notes "Added requirement for ranking top 3 wells with evidence quotes" \
  --test-results "Improved hierarchy detection on synthetic narratives"

# Create new version from session
python create_version.py \
  --session-id abc123 \
  --new-version v2.1 \
  --changelog "Enhanced hierarchical ranking with evidence extraction"
```


### **Cross-Component Testing Protocol**

```bash
# Test component combinations for compatibility
python test_compatibility.py \
  --prompt hierarchical_ranking:v2.1 \
  --framework civic_virtue:v1.4 \
  --weighting winner_take_most:v1.2 \
  --test-corpus synthetic_narratives.jsonl \
  --metrics cv,hierarchy_sharpness,dominance_detection

# Generate compatibility report
python generate_compatibility_report.py \
  --experiment-id exp_456 \
  --output compatibility_analysis.json
```


## **Integration with Existing Infrastructure**

### **Leveraging Current Capabilities**

- **FrameworkManager**: Extend to support database-stored frameworks with version selection
- **PromptTemplateManager**: Integrate with database versioning system
- **PostgreSQL Schema**: Build on existing experiments and runs tables
- **Multi-Run Dashboard**: Enhanced to show component version information


### **CLI Enhancement Strategy**

```python
# Enhanced analysis service integrating all three components
class IntegratedAnalysisService:
    def __init__(self):
        self.prompt_manager = DatabasePromptManager()
        self.framework_manager = DatabaseFrameworkManager()
        self.weighting_manager = WeightingMethodologyManager()
    
    def analyze_with_components(self, text, prompt_version, framework_version, 
                              weighting_version, model):
        # Load versioned components
        prompt = self.prompt_manager.get_version(prompt_version)
        framework = self.framework_manager.get_version(framework_version)
        weighting = self.weighting_manager.get_version(weighting_version)
        
        # Execute analysis with full provenance tracking
        return self.execute_analysis(text, prompt, framework, weighting, model)
```


## **Research Workflow Benefits**

### **Systematic Component Development**

- **Independent Iteration**: Modify prompts without affecting framework definitions
- **Compatibility Testing**: Systematic evaluation of component combinations
- **Provenance Tracking**: Complete experimental history for academic publication
- **Rollback Capabilities**: Return to previous versions when experiments fail


### **Academic Validation Support**

- **Component Attribution**: Clear attribution of performance improvements to specific components
- **Replication Packages**: Complete component specifications for research reproduction
- **Statistical Analysis**: Performance comparison across component combinations
- **Documentation Standards**: Academic-quality methodology documentation

This expanded approach transforms your CLI tools from simple analysis executors into a comprehensive research laboratory that maintains the separation of concerns between prompts, frameworks, and weighting methodologies while enabling systematic exploration of their interactions. The manual development approach with LLM chatbots preserves the conversational creativity essential for hypothesis formation while the database integration ensures rigorous experimental tracking for academic credibility.

## **User Story 2: Multi-Framework Batch Validation Studies**

### **As a researcher validating framework reliability**

"I want to execute comprehensive variance studies across multiple frameworks, LLMs, and run counts using systematic CLI commands, so that I can generate publication-ready statistical validation data without complex interface development."

**Current Capabilities to Leverage:**

- Your existing multi-run analysis infrastructure (765 analyses capability)
- PostgreSQL v2.1 schema with complete experimental tracking
- Statistical analysis capabilities with coefficient of variation

**Enhanced CLI Workflow:**

```bash
# Systematic validation study execution
python batch_study.py \
  --texts golden_set.jsonl \
  --frameworks civic_virtue,political_spectrum,moral_rhetorical_posture \
  --models gpt-4o,claude-3.5-sonnet,gemini-1.5-pro \
  --runs 5 \
  --output validation_study_2025_06.json

python analyze_variance.py \
  --input validation_study_2025_06.json \
  --output statistical_summary.json \
  --include-plots
```

**Gaps to Address:**

- **Batch Study Orchestrator**: CLI tool for complex experimental matrices
- **Statistical Analysis Pipeline**: Automated CV, ICC, and confidence interval calculation
- **Academic Report Generator**: Publication-ready statistical documentation


## **User Story 3: Framework Fit Detection and Corpus Quality**

### **As a researcher managing corpus quality**

"I want CLI tools that automatically identify texts with high variance patterns and flag potential framework fit issues, so that I can systematically improve corpus quality and detect when frameworks are poorly suited to specific narratives."

**Current Capabilities to Leverage:**

- Your existing variance analysis infrastructure
- Framework switching capabilities for cross-framework comparison

**Enhanced Detection Workflow:**

```bash
# Framework fit analysis
python detect_framework_fit.py \
  --corpus political_speeches.jsonl \
  --framework civic_virtue \
  --threshold 0.20 \
  --output fit_analysis.json

python categorize_corpus.py \
  --input fit_analysis.json \
  --output corpus_categories.json
  # Categories: Core Texts (low variance), Boundary Cases, Outliers
```

**Gaps to Address:**

- **Framework Fit Detection Tool**: Automated variance threshold analysis
- **Corpus Quality Manager**: Text categorization and quality metrics
- **Cross-Framework Compatibility Check**: Systematic framework comparison


## **User Story 4: Research Archive Exploration and Pattern Recognition**

### **As a researcher synthesizing months of experimental data**

"I want CLI tools that can query my experimental database and generate insights about prompt evolution, framework performance, and methodological patterns, so that I can discover research insights from accumulated data without building complex interfaces."

**Current Capabilities to Leverage:**

- PostgreSQL database with comprehensive experimental tracking
- Existing API endpoints for data access

**Archive Analysis Workflow:**

```bash
# Research pattern analysis
python query_experiments.py \
  --date-range "2025-03-01:2025-06-01" \
  --framework civic_virtue \
  --pattern "hierarchical_prompting" \
  --output experiment_summary.json

python analyze_patterns.py \
  --input experiment_summary.json \
  --metrics cv,icc,effect_size \
  --output research_insights.json
```

**Gaps to Address:**

- **Experimental Query Tool**: Natural language-like database queries
- **Pattern Recognition Engine**: Statistical trend analysis across experiments
- **Research Synthesis Generator**: Academic insight documentation


## **User Story 5: Automated Documentation and Replication Package Generation**

### **As a researcher preparing for academic publication**

"I want CLI tools that automatically generate comprehensive methodology documentation, replication packages, and statistical summaries from my experimental database, so that I can meet academic standards without manual documentation overhead."

**Current Capabilities to Leverage:**

- Complete experimental provenance in PostgreSQL
- Existing version control for frameworks and prompts

**Documentation Pipeline:**

```bash
# Academic documentation generation
python generate_replication_package.py \
  --study-id variance_validation_2025 \
  --include-data \
  --include-code \
  --output replication_package.zip

python generate_methodology_doc.py \
  --experiments validation_study_2025_06.json \
  --format academic_paper \
  --output methodology_section.md
```

**Gaps to Address:**

- **Replication Package Builder**: Automated academic documentation
- **Methodology Documentation Generator**: Systematic process description
- **Statistical Report Formatter**: Publication-ready statistical summaries


## **Implementation Priorities for Cursor**

### **Week 1: Core CLI Enhancement**

```python
# Essential tools to build/enhance:
1. Prompt version management CLI
2. Batch study orchestrator  
3. Basic statistical analysis pipeline
4. Documentation generation framework
```


### **Week 2: Advanced Analysis Tools**

```python
# Analysis and quality tools:
1. Framework fit detection system
2. Corpus quality management tools
3. Cross-experimental pattern recognition
4. Research insight generation
```


### **Week 3: Academic Publication Support**

```python
# Documentation and replication tools:
1. Automated replication package generation
2. Academic methodology documentation
3. Statistical report formatting
4. Complete workflow documentation
```


## **Process Documentation Templates**

### **Standard Research Workflow Documentation**

```markdown
## Prompt Engineering Cycle
1. Manual iteration (Claude/GPT-4 interfaces)
2. Version creation: `python manage_prompts.py create --version v2.1`
3. Testing: `python test_prompt.py --version v2.1 --sample golden_set`
4. Documentation: `python document_changes.py --version v2.1 --notes "Added hierarchical ranking"`

## Validation Study Protocol  
1. Study design: `python design_study.py --type variance --frameworks all`
2. Execution: `python run_study.py --config study_design.json`
3. Analysis: `python analyze_results.py --study study_2025_06`
4. Documentation: `python generate_report.py --study study_2025_06`
```


### **Quality Assurance Checklist**

```markdown
## Before Each Analysis Run
- [ ] Prompt version documented and tested
- [ ] Framework compatibility verified
- [ ] Cost estimation completed
- [ ] Output format validated

## After Each Study
- [ ] Statistical significance verified
- [ ] Replication metadata captured
- [ ] Quality metrics calculated  
- [ ] Academic documentation updated
```


## **Success Metrics for CLI Approach**

### **Efficiency Gains**

- Reduce prompt testing cycle from hours to minutes
- Automate 80% of statistical analysis workflow
- Generate publication-ready documentation automatically


### **Research Quality**

- Complete experimental provenance for every analysis
- Systematic variance detection and corpus quality management
- Reproducible research workflows with version control


### **Academic Validation Support**

- Statistical validation studies executable in 2-3 CLI commands
- Human validation data integration through standardized formats
- Publication package generation with complete methodology documentation

This CLI-based approach leverages your existing sophisticated infrastructure while addressing workflow gaps through minimal, targeted development. The focus remains on data generation and systematic analysis rather than interface development, perfectly aligning with your validation-first strategy and academic publication goals.

Your existing backend provides the robust foundation needed—these user stories simply systematize and document the workflows you need for rigorous academic research while maintaining the manual flexibility that accelerates prompt iteration and hypothesis formation.

<div style="text-align: center">⁂</div>

[^1]: in-order-to-make-progress-on-w-yJLy9NxIQsaXVbsGvKPXHg.md

[^2]: FRAMEWORK_ARCHITECTURE.md

[^3]: README.md

[^4]: i-ve-updated-the-files-in-this-3SOhPLUeRHirmfQDLsNCOw.md

[^5]: COMPREHENSIVE_PROJECT_DOCUMENTATION.md

[^6]: if-you-were-to-develop-a-compl-5KHQ_w5ARS6NumH6P0fHvA.md

[^7]: VALIDATION_IMPLEMENTATION_ROADMAP.md

[^8]: framework.json

[^9]: Narrative-Gravity-Model-Epic-1-Corpus-Job-Management-Backend.md

[^10]: database_first_architecture_todos.md

[^11]: Milestone-1-Epics-Narrative-Gravity-Model.md

[^12]: Project-Milestones-Narrative-Gravity-Model.md

[^13]: User-Personas-Narrative-Gravity-Model.md

