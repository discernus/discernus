<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# <q>User Story 1: Systematic Prompt Engineering Workflow

As a researcher conducting prompt optimization
"I want to systematically test prompt variations using my existing CLI tools and document the evolution of prompt effectiveness, so that I can maintain clear experimental provenance while rapidly iterating toward reliable thematic hierarchy detection."</q> I think we should expand this to framework development and weighting methodologies, which I think are distinct from the prompt template engineering. All of these need to be done manually with LLM chatbots, but tracked and versioned in the database, then used in the single run or batch run analysis in the CLI.

🧠 **Essential Expansion for Comprehensive Research Workflow:**

- Framework development as distinct from prompt template engineering
- Weighting methodology experimentation separate from both prompts and frameworks
- Manual development via LLM chatbots with systematic database tracking
- Version control for all three components with compatibility matrices
- Integration pipeline for CLI analysis using versioned components

You're absolutely right to expand this beyond just prompt engineering. Based on your comprehensive project documentation, there are three distinct but interdependent components that need systematic development and version tracking:

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

<div style="text-align: center">⁂</div>

[^1]: in-order-to-make-progress-on-w-yJLy9NxIQsaXVbsGvKPXHg.md

[^2]: README.md

[^3]: i-ve-updated-the-files-in-this-3SOhPLUeRHirmfQDLsNCOw.md

[^4]: COMPREHENSIVE_PROJECT_DOCUMENTATION.md

[^5]: CHANGELOG.md

[^6]: if-you-were-to-develop-a-compl-5KHQ_w5ARS6NumH6P0fHvA.md

[^7]: moral_rhetorical_posture_api_prompt.md

[^8]: 5_dipole_interactive_prompt_v2025.01.03.19.45.txt

[^9]: database_first_architecture_todos.md

[^10]: FRAMEWORK_ARCHITECTURE.md

[^11]: VALIDATION_FIRST_DEVELOPMENT_STRATEGY.md

[^12]: framework.json

[^13]: Moral-Gravity-Wells-A-Quantitative-Framework-for-Discerning-the-Moral-Forces-Driving-the-Formatio.md

[^14]: moral_rhetorical_posture_prompt.md

[^15]: civic_virtue_prompt.md

