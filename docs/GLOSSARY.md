# Discernus Glossary

## Core Architecture Concepts

### **THIN Architecture**
Software design philosophy where minimal code enables LLM conversations rather than managing them. Software provides orchestration infrastructure; LLMs provide intelligence and analysis.

### **Expert Agent**
Specialized LLM with domain expertise (e.g., `discernuslibrarian_agent`, `corpus_detective_agent`) that can be spawned by the moderator to provide specific analysis.

### **Agent Spawning Instruction Set**
The system prompt and configuration that defines an expert agent's capabilities, stored in `agent_roles.py`.

### **Moderator Agent/LLM**
The orchestrating LLM (`moderator_llm`) responsible for coordinating expert agents and managing the overall research workflow.

## Research Workflow Components

### **Corpus Detective**
An expert agent that inspects user-provided corpus at ingestion time to identify document types, quality issues, and metadata gaps. Backed by CorpusInspector infrastructure for robust file reading from messy real-world directories.

### **Research Session**
A complete analytical workflow from research question through final analysis, stored in `research_sessions/session_id/`.

### **Design LLM**
The LLM responsible for proposing research methodology based on the research question and corpus.

### **Conversation Orchestration**
The process of coordinating multiple expert LLMs to build progressive analysis toward answering a research question.

## Data and Content

### **Corpus**
Collection of texts provided by the user for analysis. Can be messy, real-world data requiring inspection and cleaning.

### **Source Texts**
The actual text content being analyzed, passed to expert agents as context.

### **Framework Interrogation**
Process of validating novel analytical frameworks against academic literature (performed by discernuslibrarian_agent).

### **Literature Discovery**
Automated search and validation of academic papers relevant to research questions (performed by discernuslibrarian_agent).

## Technical Infrastructure

### **LiteLLM Client**
Unified interface for accessing multiple LLM providers (OpenAI, Anthropic, Vertex AI) with rate limiting and cost optimization.

### **Conversation Logger**
System that records all LLM interactions with timestamps and metadata for complete transparency.

### **Corpus Chunking**
Process of dividing large corpora into manageable pieces for API rate limit management.

### **Session Manager**
Component responsible for creating, tracking, and managing research sessions.

## Agent Types and Roles

### **Production Agents**
Expert agents used in the main research pipeline:
- `corpus_detective_agent`: Corpus inspection and quality assessment
- `discernuslibrarian_agent`: Academic literature discovery and framework validation  
- `computational_rhetoric_expert`: Rhetorical analysis and persuasive discourse
- `data_science_expert`: Statistical analysis and quantitative methods

### **Development Tools**
Utilities for development and testing:
- `dev_test_runner.py`: Automated testing framework
- `setup_vertex_ai.py`: Vertex AI configuration utility
- `analyze_conversation_timing.py`: Performance analysis tool
- `natural_corpus_demo.py`: Complete workflow demonstration with transparency logging

### **Core Infrastructure Services**
Production infrastructure that expert agents depend on:
- `UltraThinDiscernusLibrarian` (in `discernuslibrarian.py`): Academic literature discovery APIs
- `CorpusInspector` (in `corpus_inspector.py`): File reading and corpus inspection infrastructure
- `SecureCodeExecutor` (in `secure_code_executor.py`): Sandboxed computation with data science libraries
- `NotebookManager` (in `notebook_manager.py`): Automatic research notebook generation

### **Computational Rhetoric & Traditional NLP**
**Academic Value Assessment**: Recent research (2024-2025) shows traditional NLP tools maintain academic value alongside LLMs:

**🎯 THIN Recommendation**: Provide computational_rhetoric_expert with **lightweight NLP toolkit** rather than heavy infrastructure:
- **Core tools**: TextStat (readability), VADER sentiment, basic syntactic parsers
- **Rationale**: LLMs excel at interpretation but struggle with fine-grained linguistic annotation
- **Academic Use Cases**: Linguistic feature extraction that LLMs miss (clause detection, syntactic complexity)
- **Research Evidence**: "Linguistic Blind Spots of Large Language Models" (2025) shows LLMs fail at precise syntactic tasks

**🚫 Skip**: Heavy NLP infrastructure (spaCy pipelines, custom parsers) unless specific research demands it

### **Simulated Researcher**
LLM profiles that simulate human researcher feedback during development mode testing.

## File Organization

### **Package Structure**
- `discernus/core/`: Core production services
- `discernus/gateway/`: LLM API management
- `discernus/orchestration/`: Multi-agent coordination
- `discernus/web/`: Web interface
- `discernus/tests/`: Test suite
- `discernus/dev_tools/`: Development utilities
- `discernus/demo/`: Usage examples

### **Research Artifacts**
- `research_sessions/`: All completed research sessions
- `pm/`: Product management and specification documents
- `data/`: Research corpora and datasets
- `docs/`: Documentation and guides

## Workflow Terminology

### **Moderator Spawning**
The process where the moderator_llm determines which expert agents to activate based on research needs.

### **Expert Request**
Specific analytical task requested from an expert agent: `"REQUEST TO [Expert_Name]: [Specific analytical request]"`

### **Progressive Analysis**
Building knowledge systematically by using outputs from one expert to inform requests to subsequent experts.

### **Research Question**
The central question driving the entire analytical workflow, provided by the user.

### **Approved Design**
Research methodology that has been proposed by the design LLM and approved by the user/simulated researcher.

## Quality and Validation

### **THIN Compliance**
Adherence to THIN architecture principles - minimal code, maximum LLM intelligence, no complex parsing.

### **Evidence-Based Confidence**
Systematic approach to assigning confidence levels to research claims based on available evidence quality and quantity.

### **Red Team Critique**
Adversarial quality control where specialized models challenge research findings to identify weaknesses.

### **Corpus Quality Assessment**
Systematic evaluation of corpus characteristics including source diversity, temporal coverage, and potential biases.

---

*This glossary helps maintain consistent terminology across the Discernus project and reduces confusion during development and usage.*

## Related Documentation

- **`../AGENT_QUICK_START.md`** - 5-minute orientation for new Cursor agents
- `DEV_MODE_GUIDE.md` - Development mode and testing workflows
- `EXTENSION_GUIDE.md` - How to extend Discernus without forking
- `DEPLOYMENT_COLLABORATION_GUIDE.md` - Complete deployment and collaboration scenarios
- `../README.md` - Project overview and THIN architecture guide
- Core architecture documentation in `../pm/` directory 