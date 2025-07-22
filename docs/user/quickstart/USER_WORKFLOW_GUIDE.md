# User Workflow Guide
*Essential Workflows for Discernus*

This guide provides the essential workflows for the three main user types. Each workflow is optimized for speed and focuses on the most common patterns.

## Three Core Workflows

### Academic Research Workflow (Peer Review Ready)

**Goal**: Rigorous, reproducible analysis suitable for publication

#### Essential Steps
```bash
# 1. Setup project
mkdir research_project && cd research_project

# 2. Get framework (use existing or create)
cp /path/to/framework.md . || python3 -c "
from discernus.core.framework_loader import FrameworkLoader
loader = FrameworkLoader()
loader.create_framework_template('my_framework')
"

# 3. Validate framework
python3 -c "
from discernus.core.framework_loader import FrameworkLoader
loader = FrameworkLoader()
result = loader.validate_framework('framework.md')
print('✅ Valid' if result['status'] == 'success' else f'❌ Issues: {result[\"issues\"]}')
"

# 4. Add corpus files to corpus/ directory
mkdir corpus
# Add your .txt files here

# 5. Get cost estimate
python3 -c "
from discernus.agents.execution_planner_agent import ExecutionPlannerAgent
planner = ExecutionPlannerAgent()
import os
corpus_files = [f for f in os.listdir('corpus') if f.endswith('.txt')]
with open('framework.md', 'r') as f:
    framework_text = f.read()
plan = planner.create_execution_plan(
    corpus_files=corpus_files,
    model_names=['claude-3-5-sonnet-20241022'],
    framework_text=framework_text,
    analysis_instructions='Academic analysis'
)
print(f'Cost: ${plan[\"estimated_cost\"]:.2f}, Time: {plan[\"estimated_time_hours\"]:.1f}h')
"

# 6. Run analysis
python3 -c "
from discernus.agents.validation_agent import ValidationAgent
agent = ValidationAgent()
result = agent.validate_and_execute_sync('framework.md', 'experiment.md', 'corpus/')
print(f'Status: {result[\"status\"]}')
print(f'Results: {result[\"results_path\"]}' if result['status'] == 'success' else f'Error: {result[\"error\"]}')
"
```

**Expected Output**: Publication-ready analysis with complete methodology documentation

### Corporate Analysis Workflow (Business Insights)

**Goal**: Fast, actionable insights within budget constraints

#### Essential Steps
```bash
# 1. Setup business project
mkdir business_analysis && cd business_analysis

# 2. Use pre-built business framework
python3 -c "
from discernus.core.framework_library import FrameworkLibrary
library = FrameworkLibrary()
framework = library.get_framework('brand_sentiment_analysis')
with open('framework.md', 'w') as f:
    f.write(framework['content'])
print(f'Framework ready. Typical cost: ${framework[\"typical_cost\"]:.2f}')
"

# 3. Add business data to corpus/
mkdir corpus
# Add customer feedback, social media, reviews, etc.

# 4. Run express analysis (cost-optimized)
python3 -c "
from discernus.agents.express_analyzer import ExpressAnalyzer
config = {
    'analysis_mode': 'express',
    'budget_limit': 100.00,
    'models': {'primary': 'gemini-pro'}
}
analyzer = ExpressAnalyzer(config)
result = analyzer.analyze_business_corpus('framework.md', 'corpus/')
print(f'Status: {result[\"status\"]}')
print(f'Cost: ${result[\"cost\"]:.2f}, Time: {result[\"execution_time\"]} min')
"
```

**Expected Output**: Executive summary with actionable recommendations

### Organizational Decision-Making Workflow (Risk Assessment)

**Goal**: High-confidence analysis for strategic decisions

#### Essential Steps
```bash
# 1. Setup organizational project
mkdir org_decision && cd org_decision

# 2. Configure for high-confidence analysis
cat > config.yaml << 'EOF'
analysis_type: organizational_decision_support
confidence_threshold: 0.85
models:
  primary: claude-3-5-sonnet-20241022
  validation: gpt-4o
budget_allocation:
  maximum_spend: 500.00
EOF

# 3. Add policy documents, stakeholder feedback to corpus/
mkdir corpus
# Add organizational documents

# 4. Run comprehensive analysis
python3 -c "
from discernus.agents.organizational_analyzer import OrganizationalAnalyzer
import yaml
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)
analyzer = OrganizationalAnalyzer(config)
result = analyzer.analyze_policy_impact('corpus/')
print(f'Status: {result[\"status\"]}')
print(f'Confidence: {result[\"confidence_score\"]:.1f}%')
print(f'Risk Level: {result[\"risk_level\"]}')
"
```

**Expected Output**: Decision package with risk assessment and stakeholder implications

## Quick Commands Reference

### Cost Management
```bash
# Get quick cost estimate
discernus estimate --framework framework.md --corpus corpus/ --model claude-3-5-sonnet-20241022

# Set budget limit
discernus analyze --framework framework.md --corpus corpus/ --budget 50.00

# Use cost-effective model
discernus analyze --framework framework.md --corpus corpus/ --model gemini-pro
```

### Results Access
```bash
# View latest results
cat results/*/final_report.md

# Check reproducibility
discernus validate session results/latest/

# Replicate analysis
discernus replicate session_20250115_143022
```

### Common Issues
```bash
# Framework validation failed
discernus validate framework framework.md

# Corpus reading errors
python3 -c "
from discernus.core.corpus_inspector import CorpusInspector
inspector = CorpusInspector()
files, errors = inspector.inspect_directory_corpus('corpus')
print(f'Files: {len(files)}, Errors: {errors}')
"

# Cost overrun
# Check budget before running:
discernus estimate --framework framework.md --corpus corpus/
```

## Success Patterns

### Academic Research
- **Reproducibility Score**: >95% 
- **Publication Ready**: Complete methodology documentation
- **Cost Efficiency**: <$50 per analysis

### Corporate Analysis  
- **Speed**: Results within 2 hours
- **Actionability**: Clear business recommendations
- **Cost Control**: Within approved budget

### Organizational Decisions
- **Confidence**: >85% in recommendations
- **Risk Assessment**: Comprehensive evaluation
- **Stakeholder Clarity**: Clear communication

---

**THIN Principle**: Maximum practical value, minimum cognitive overhead. These workflows get you from question to answer efficiently while maintaining the three foundational commitments.

*For comprehensive optimization strategies, see the extended documentation in the reference materials.* 