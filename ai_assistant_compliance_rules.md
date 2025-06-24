# 🤖 AI Assistant Compliance Rules for Narrative Gravity Analysis Project

> This document defines **mandatory rules** for AI assistants contributing to the Narrative Gravity Analysis project. It also captures user preferences, development workflows, and prohibited behaviors. **Failure to follow these rules may result in invalid or counterproductive suggestions.**

---

## 🎯 USER PREFERENCES

- **Temperature:** Always behave as if temperature = 0  
  → Prioritize systematic, rule-following, deterministic responses over creative or exploratory variation.

- **Development Bias:** Production-first  
  → Assume the user prefers using and extending existing systems over rebuilding or inventing alternatives.

- **Communication Style:** Technical, concise, and directive  
  → Avoid verbosity, speculation, or opinion unless explicitly requested.

---

## 🖥️ RULE 0: LOCAL DEVELOPMENT ENVIRONMENT

**ALL development and testing uses local Python environment with PostgreSQL.**

### ✅ MANDATORY: Local Development Setup
```bash
# Set up local development environment
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your API keys and database settings

# Run local PostgreSQL (macOS with Homebrew)
brew install postgresql
brew services start postgresql
createdb discernus

# Test database connection
python3 check_database.py

# Run the orchestrator locally
python3 scripts/applications/comprehensive_experiment_orchestrator.py
```

### 🎯 Why This Rule Changed
Local development provides:
- **Faster iteration cycles** - No container rebuild delays
- **Easier debugging** - Direct access to code and processes  
- **Better file system performance** - No Docker file sync issues
- **Simplified setup** - Single environment instead of Docker + local hybrid

### 🔍 Environment Validation
Before any development work, verify your local setup:
```bash
# Check database connectivity
python3 -c "from src.utils.database import get_database_url; print('DB OK:', get_database_url())"

# Check API keys
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OpenAI:', 'OK' if os.getenv('OPENAI_API_KEY') else 'Missing')"
```

---

## 📋 PRODUCTION CLASSIFICATION

### ✅ Production Systems (Use These)
Code that is **stable, tested, and approved for research use**:
- `src/` - Core application code with established APIs
- `scripts/applications/` - Orchestration and production workflows
- `frameworks/` - Validated analysis frameworks
- Systems documented in `docs/EXISTING_SYSTEMS_INVENTORY.md`
- Code with comprehensive tests and documentation

**Characteristics of Production Code:**
- Has been used successfully in real experiments
- Has proper error handling and logging
- Follows project architectural standards
- Is maintained and actively supported

### 🧪 Development Systems (Build Here)
Code under active development or validation:
- `experimental/prototypes/` - New feature development
- `sandbox/` - Personal/exploratory work
- `research_workspaces/` - Research-specific experiments
- `scripts/utilities/` - Helper scripts and tools

### 🗑️ Deprecated Systems (Never Use)
Code that has been superseded or identified as problematic:
- `deprecated/` - Explicitly moved obsolete code
- Files marked with `# DEPRECATED` comments
- Systems listed as deprecated in inventory documentation
- Code that violates current architectural standards

### 🎯 When In Doubt
If unsure whether something is production-ready:
1. Check `docs/EXISTING_SYSTEMS_INVENTORY.md`
2. Look for usage in successful experiments
3. Check for proper documentation and tests
4. Ask: "Would I trust this for an academic publication?"

---

## 🚨 CRITICAL: BEFORE YOU SUGGEST ANYTHING

You **must always** run the production system check first:

\`\`\`bash
python3 scripts/applications/check_existing_systems.py "functionality description"
\`\`\`

If you suggest building something **without first checking** for existing systems, you are violating project standards.

---

## 🔴 RULE 0: USE THE PRODUCTION ORCHESTRATOR FOR EXPERIMENT WORK

For **any statistical analysis, hypothesis testing, data export, or report generation**, you must use:

\`\`\`bash
python3 scripts/applications/comprehensive_experiment_orchestrator.py experiment.json
\`\`\`

To resume interrupted experiments:

\`\`\`bash
python3 scripts/applications/comprehensive_experiment_orchestrator.py --resume
\`\`\`

**You must not suggest writing custom scripts** for:
- Experiment execution
- Statistical analysis
- Visualization
- Hypothesis validation
- Data export
- Report generation

These functions are already supported via the orchestrator and must be used for integrity, traceability, and cost control.

---

## ⚖️ MANDATORY DEVELOPMENT WORKFLOW

### ✅ Rule 1: Search Before Building

Always run the existing systems checker before proposing new work:

\`\`\`bash
python3 scripts/applications/check_existing_systems.py "functionality description"
\`\`\`

### ❌ Rule 2: Never Use Deprecated Systems

Do **not** suggest or reference:
- \`"AI Academic Advisor"\` (file-checker; deprecated)
- Any code in the \`deprecated/\` or \`archive/\` directories
- Files containing \`# DEPRECATED\` comments
- \`architectural_compliance_validator.py\` (moved to deprecated)

### ✅ Rule 3: Build in \`experimental/\` First

All new development **must** begin in \`experimental/prototypes/\`

Do **not** suggest creating or modifying files directly in \`src/\` or \`scripts/\`

### ✅ Rule 4: Enhance Before Rebuilding

If the needed functionality exists in production, **enhance it**

Do **not** duplicate or replace existing production systems unnecessarily

---

## 🔍 SEARCH STRATEGY

### ✅ Always Search These:
- \`src/\` – Core production code
- \`scripts/applications/\` – Production orchestration and validation scripts
- \`docs/specifications/\` – Technical and implementation specs

### ⚠️ Conditionally Search:
- \`experimental/\` – Only when explicitly asked or no production tool is suitable
- \`sandbox/\` – For early-stage or exploratory research only

### ❌ Never Search:
- \`deprecated/\`, \`archive/\`
- Files with \`# DEPRECATED\` annotations
- Any reference to "AI Academic Advisor"

---

## ✅ APPROVED PRODUCTION SYSTEMS

### Quality Assurance

- \`LLMQualityAssuranceSystem\` – 6-layer mathematical validator
- \`ComponentQualityValidator\` – Component-level QA validator

### Experiment Execution

- \`scripts/applications/comprehensive_experiment_orchestrator.py\` (the comprehensive production orchestrator)
- \`scripts/applications/comprehensive_experiment_orchestrator.py\` – Full orchestration with checkpoint/resume

### Academic Export

- \`QAEnhancedDataExporter\`
- \`src/academic/data_export.py\`
- \`scripts/cli/export_academic_data.py\`

---

## ✅ REQUIRED REFERENCES

AI assistants must use and reference these docs when reasoning about project structure:

1. \`docs/EXISTING_SYSTEMS_INVENTORY.md\` – Catalog of implemented systems  
2. \`docs/CODE_ORGANIZATION_STANDARDS.md\` – Where functionality belongs  
3. \`docs/platform-development/DEV_ENVIRONMENT.md\` – End-to-end guide for development workflows  
4. \`.ai_assistant_compliance_rules.md\` – This file  

---

## 🧠 EXAMPLE PROMPTS FOR SESSION STATE MANAGEMENT

Use these regularly to manage assistant context during extended development:

### Session Recap

\`\`\`
Summarize the current state of this session. Include the goal, key files involved, major decisions made, and what's been completed.
\`\`\`

### Assumptions Check

\`\`\`
What assumptions are you currently making about the task, the codebase, and our intended outcome? List them explicitly.
\`\`\`

### Assistant Handoff Bootstrap

\`\`\`
You're joining an in-progress development effort. Here's the most recent context:
- Recent commits
- Changed files
- High-level summary

What is in progress, what's likely done, and what still needs to happen?
\`\`\`

---

## 🛡️ SUCCESS CRITERIA

An assistant is **compliant** if it:
- ✅ Searches production systems first  
- ✅ Enhances existing tools rather than duplicating  
- ✅ Uses only approved QA and experiment tooling  
- ✅ Puts all new development into \`experimental/\` first  
- ✅ Never references deprecated or superseded systems  

---

## ❌ COMMON VIOLATIONS (DO NOT DO THESE)

| Violation | Why It's Wrong |
|----------|----------------|
| **Not setting up local environment** | **Must use proper local development setup (Rule 0)** |
| **Missing .env configuration** | **Must configure local environment variables** |
| Suggesting new QA system | Use \`LLMQualityAssuranceSystem\` instead |
| Using "AI Academic Advisor" | Deprecated and ineffective |
| Creating new files in \`src/\` | Must go through \`experimental/\` first |
| Suggesting statistical scripts | Use orchestrator pipeline instead |
| Using code from \`deprecated/\` | Violates architectural compliance rules |

---

## 🧭 REMEMBER

These rules exist because the project has **repeatedly wasted time and resources** rebuilding inferior versions of already sophisticated systems.

By following these standards, AI assistants help the team:
- Preserve architectural coherence  
- Reduce duplication and drift  
- Maintain data and experiment integrity  
- Improve productivity over time

---

### Rule 1: ALWAYS Search Production Systems First
Before suggesting ANY development work, you MUST run:
```bash
python3 scripts/applications/check_existing_systems.py "functionality description"
```

### Rule 2: NEVER Use Deprecated Systems
- ❌ NEVER mention "AI Academic Advisor" (it's just file existence checks)
- ❌ NEVER reference `deprecated/` directory code
- ❌ NEVER use `architectural_compliance_validator.py` (moved to deprecated)
- ❌ NEVER use JSON format for experiments (use YAML: experiment.yaml)

### Rule 3: ALWAYS Use Production Systems
- ✅ USE: `LLMQualityAssuranceSystem` (6-layer mathematical validation)
- ✅ USE: `ComponentQualityValidator` (component validation)
- ✅ USE: `QAEnhancedDataExporter` (academic export)
- ✅ USE: `scripts/applications/comprehensive_experiment_orchestrator.py experiment.yaml` (experiments)
- ✅ USE: YAML format for all frameworks and experiments (Framework Specification v3.1)

---
