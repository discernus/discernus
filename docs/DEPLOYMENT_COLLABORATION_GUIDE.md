# Discernus Deployment & Collaboration Guide

## **🎯 Overview**

This guide covers how to deploy, use, and collaborate with Discernus across different environments - from individual academic research to classified government projects. The system is designed to support everything from open academic collaboration to air-gapped defense contractor work.

---

## **🏠 LOCAL INSTALLATION & SETUP**

### **Standard Installation**
```bash
# Clone the GPL-licensed core
git clone https://github.com/discernus/discernus.git
cd discernus

# Standard Python setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Initialize local configuration
cp env.example .env
# Edit .env with API keys, local database settings, etc.
```

### **Git Persistence Setup**

**Option A: Public Research (Most Academics)**
```bash
git remote add origin https://github.com/your-username/my-research-project.git
git push -u origin main
```

**Option B: Private Research (Sensitive Work)**
```bash
git remote add origin https://github.com/your-org/classified-research.git
git push -u origin main
```

**Option C: Air-Gapped (Defense Contractors)**
```bash
git remote add origin file:///secure/git/repositories/project-x.git
git push -u origin main
```

**Key Principle**: The GPL core stays GPL, but **research data, extensions, and analyses** can be private repositories.

---

## **🔬 STANDARD USAGE WORKFLOW**

### **Daily Research Pattern**
```bash
# Start research session
python3 -m discernus.web.app  # Web interface
# OR
python3 -m discernus.cli      # Command line interface

# Research session automatically creates:
research_sessions/session_20250105_143022/
├── conversation_log.jsonl     # Full conversation
├── conversation_readable.md   # Human-readable version
├── calculations/             # All code executions
├── notebooks/               # Important calculations as .ipynb
└── metadata.json           # Session metadata
```

### **End-of-Session Git Workflow**
```bash
# Commit research session
git add research_sessions/session_20250105_143022/
git commit -m "Analysis of political rhetoric in 2024 campaign speeches

- Analyzed 247 speeches using civic virtue framework
- Found significant correlation between populist rhetoric and emotional appeals
- Generated 3 research notebooks with statistical validation
- Session duration: 2.5 hours, 15 agent interactions"

git push origin main
```

### **Extension Development**
```bash
# Develop new extension
vim extensions/my_domain_expert.yaml

# Test extension
python3 -c "
from discernus.core.capability_registry import CapabilityRegistry
registry = CapabilityRegistry()
issues = registry.validate_extension('extensions/my_domain_expert.yaml')
print('✅ Valid' if not issues else f'Issues: {issues}')
"

# Commit extension
git add extensions/my_domain_expert.yaml
git commit -m "Added cognitive linguistics expert agent

- Expert specializes in cognitive metaphor analysis
- Includes spaCy and transformers integration
- Tested with political speech corpus
- Ready for collaboration"

git push origin main
```

---

## **🐛 BUG FIXES & CORE CONTRIBUTIONS**

### **Standard Open Source Workflow**
```bash
# Fork the main repo on GitHub
git clone https://github.com/your-username/discernus.git
cd discernus

# Create feature branch
git checkout -b fix/secure-executor-memory-leak

# Make changes to core code
vim discernus/core/secure_code_executor.py
# Add comprehensive tests
vim tests/test_secure_executor_memory.py
# Update documentation
vim docs/SECURITY.md

# Test thoroughly
python3 -m pytest tests/
python3 discernus/dev_tools/dev_test_runner.py

# Commit with detailed message
git add -A
git commit -m "Fix memory leak in secure code executor

Problem:
- SecureCodeExecutor was not properly cleaning up subprocess memory
- Long research sessions would accumulate memory usage
- Could lead to system instability after 50+ calculations

Solution:
- Added explicit subprocess cleanup in __del__ method
- Implemented memory monitoring and warnings
- Added resource limit enforcement per calculation
- Improved error handling for resource exhaustion

Testing:
- Added memory stress tests with 100+ consecutive calculations
- Verified memory usage stays constant over extended sessions
- Tested on macOS and Linux environments
- All existing tests pass

Impact:
- Fixes reported issues in GitHub #123, #145
- Improves system stability for long research sessions
- No breaking changes to existing API"

# Submit PR
git push origin fix/secure-executor-memory-leak
# Create PR on GitHub with description, tests, screenshots
```

### **Enterprise/Government Considerations**
```bash
# Problem: Can't contribute back due to classification
# Solution: Maintain private fork with security patches

git remote add upstream https://github.com/discernus/discernus.git
git fetch upstream
git merge upstream/main  # Merge public updates
git push origin main     # Push to private enterprise repo

# Internal security patches stay private
# Non-sensitive improvements can be contributed back
```

---

## **🔧 EXTENSION DEVELOPMENT & SHARING**

### **Public Extensions (Academic Community)**

**Create Extension**
```yaml
# extensions/computational_linguistics.yaml
name: computational_linguistics
description: Advanced NLP tools for linguistic research
author: Dr. Smith, University of Helsinki
version: 1.2.0
license: MIT
repository: https://github.com/linguistics-dept/discernus-extensions

libraries:
  - spacy>=3.4.0
  - transformers>=4.20.0
  - nltk>=3.8
  - stanza>=1.4.0

agents:
  syntax_expert:
    description: Computational syntactic analysis specialist
    prompt: |
      You are a syntax_expert specializing in computational syntactic analysis.
      
      RESEARCH QUESTION: {research_question}
      SOURCE TEXTS: {source_texts}
      EXPERT REQUEST: {expert_request}
      
      Your capabilities:
      - Dependency parsing with spaCy
      - Constituency parsing with Stanza
      - Syntactic complexity metrics
      - Cross-linguistic syntactic analysis
      - Tree visualization and interpretation
      
      Provide rigorous syntactic analysis with computational validation.
      Write Python code in ```python blocks for analysis.
  
  morphology_expert:
    description: Computational morphological analysis specialist
    prompt: |
      You are a morphology_expert specializing in computational morphological analysis.
      
      Focus on:
      - Morphological parsing and segmentation
      - Inflectional and derivational morphology
      - Cross-linguistic morphological patterns
      - Morphophonological processes
      
      Use spaCy and NLTK for morphological analysis.

environments:
  name: linguistics_env
  description: Computational linguistics research environment
  imports:
    - import spacy
    - import nltk
    - import stanza
    - from transformers import pipeline
  setup_code: |
    # Load linguistic models
    nlp_en = spacy.load("en_core_web_lg")
    nlp_es = spacy.load("es_core_news_lg")
    
    # Initialize Stanza for constituency parsing
    stanza.download('en')
    constituency_parser = stanza.Pipeline('en', processors='tokenize,pos,constituency')
    
    # Load transformer models
    ner_pipeline = pipeline("ner", aggregation_strategy="simple")
    
    # Utility functions
    def syntactic_complexity(doc):
        return {
            "avg_depth": sum(len(list(token.ancestors)) for token in doc) / len(doc),
            "clauses": len([token for token in doc if token.dep_ in ['ccomp', 'xcomp', 'advcl']]),
            "sentence_length": len(doc)
        }
  mock_fallbacks:
    stanza: |
      class MockStanza:
          def Pipeline(self, lang, processors):
              return self
          def __call__(self, text):
              return {"sentences": [{"constituency": "Mock parse tree"}]}
      stanza = MockStanza()
```

**Sharing Options**

```bash
# Option 1: Direct sharing
scp extensions/computational_linguistics.yaml colleague@helsinki.fi:~/discernus/extensions/

# Option 2: Extension repository
git clone https://github.com/computational-linguistics/discernus-extensions.git
cp computational_linguistics.yaml discernus-extensions/
cd discernus-extensions
git add computational_linguistics.yaml
git commit -m "Added computational linguistics extension v1.2.0"
git push origin main
# Submit PR to extension repository

# Option 3: Extension marketplace (future)
discernus extension publish computational_linguistics.yaml
discernus extension install computational_linguistics
```

### **Private Extensions (Sensitive Research)**

**Classified Extension Example**
```yaml
# extensions/classified/signals_intelligence.yaml
name: signals_intelligence
description: SIGINT analysis capabilities
author: NSA Research Division
version: 2.1.0
classification: TOP SECRET//SI//TK
license: CLASSIFIED

libraries:
  - cryptography>=3.4.0
  - numpy>=1.21.0
  - scipy>=1.7.0
  - custom_sigint_tools  # Internal package

agents:
  sigint_expert:
    description: Signals intelligence analysis specialist
    classification: TOP SECRET//SI//TK
    prompt: |
      You are a sigint_expert with access to classified SIGINT analysis tools.
      
      RESEARCH QUESTION: {research_question}
      SOURCE TEXTS: {source_texts}
      EXPERT REQUEST: {expert_request}
      
      Your capabilities:
      - Signal pattern analysis
      - Cryptographic assessment
      - Communication network analysis
      - Threat assessment and attribution
      
      All analysis must maintain appropriate classification levels.
      Use secure computation methods for all calculations.

environments:
  name: sigint_env
  classification: TOP SECRET//SI//TK
  setup_code: |
    # Classified initialization code
    import custom_sigint_tools
    analyzer = custom_sigint_tools.SecureAnalyzer()
    
    def secure_analysis(data):
        # Classified analysis methods
        return analyzer.process(data)
```

**Private Sharing Process**
```bash
# Private extension repository
git clone https://secure-git.defense.gov/project-x/discernus-extensions.git
git add extensions/classified/signals_intelligence.yaml
git commit -m "Added SIGINT analysis capabilities v2.1.0

Classification: TOP SECRET//SI//TK
- Enhanced signal pattern recognition
- Improved cryptographic assessment
- Added network topology analysis
- Tested with Q4 2024 collection data"

git push origin main

# Colleague access (security-cleared personnel only)
git clone https://secure-git.defense.gov/project-x/discernus-extensions.git
# Extension automatically loaded locally
```

---

## **🛡️ SECURE COLLABORATION PATTERNS**

### **Pattern 1: Open Academic Research**
```bash
# Public repository, public extensions, public research
git clone https://github.com/university/rhetoric-research.git
cd rhetoric-research

# Directory structure:
rhetoric-research/
├── discernus/                 # Git submodule to main repo
├── extensions/
│   ├── political_rhetoric.yaml
│   ├── media_analysis.yaml
│   └── discourse_analysis.yaml
├── research_sessions/         # All public
├── data/                     # Public datasets
└── publications/             # Published papers

# Workflow:
# 1. Conduct research openly
# 2. Share extensions with community
# 3. Publish findings with full reproducibility
# 4. Cite using DOI system
```

### **Pattern 2: Private Commercial Research**
```bash
# Private repository, private extensions, private research
git clone https://secure-git.company.com/market-research.git
cd market-research

# Directory structure:
market-research/
├── discernus/                 # Git submodule to main repo
├── extensions/
│   ├── proprietary/
│   │   ├── brand_analysis.yaml
│   │   └── consumer_sentiment.yaml
│   └── public/               # Can be shared
├── research_sessions/
│   ├── confidential/         # Internal use only
│   └── publishable/          # Can be made public
├── data/
│   └── proprietary/          # Never shared
└── reports/
    └── client_deliverables/

# Workflow:
# 1. Conduct research privately
# 2. Share non-sensitive extensions
# 3. Publish non-confidential findings
# 4. Maintain competitive advantage
```

### **Pattern 3: Classified Government Work**
```bash
# Air-gapped, classified repository, classified extensions
git clone file:///secure/git/intelligence-analysis.git
cd intelligence-analysis

# Directory structure:
intelligence-analysis/
├── discernus/                 # Offline copy of main repo
├── extensions/
│   ├── classified/
│   │   ├── sigint_analysis.yaml
│   │   ├── imagery_analysis.yaml
│   │   └── threat_assessment.yaml
│   └── unclassified/         # Can be shared
├── research_sessions/
│   ├── top_secret/
│   ├── secret/
│   └── unclassified/
├── data/
│   └── classified/           # Never leaves secure environment
└── intelligence_products/
    └── classified_reports/

# Workflow:
# 1. Conduct analysis in secure environment
# 2. Share unclassified extensions through proper channels
# 3. Classified results stay in secure environment
# 4. Unclassified insights can benefit community
```

### **Pattern 4: International Collaboration**
```bash
# Multiple secure repositories, encrypted communication
# US side: https://secure-git.defense.gov/nato-project.git
# EU side: https://secure-git.europa.eu/nato-project.git

# Synchronization workflow:
# 1. Develop extensions locally
# 2. Share through secure diplomatic channels
# 3. Merge approved changes
# 4. Maintain classification boundaries
```

---

## **🔄 UPDATE & MAINTENANCE STRATEGY**

### **Core Updates**
```bash
# Monthly core updates
git remote add upstream https://github.com/discernus/discernus.git
git fetch upstream

# Check for breaking changes
git log --oneline upstream/main..HEAD
git diff upstream/main

# Merge updates
git merge upstream/main

# Test compatibility
python3 -m pytest tests/
python3 discernus/dev_tools/dev_test_runner.py

# Test with existing extensions
python3 -c "
from discernus.core.capability_registry import CapabilityRegistry
registry = CapabilityRegistry()
for ext_file in Path('extensions').glob('*.yaml'):
    issues = registry.validate_extension(ext_file)
    if issues:
        print(f'❌ {ext_file}: {issues}')
    else:
        print(f'✅ {ext_file}: Valid')
"

# Deploy to production
git push origin main
```

### **Extension Updates**
```bash
# Extension marketplace (future)
discernus extension update computational_linguistics
discernus extension update --all

# Manual updates
cd extensions/
git pull origin main

# Validate after updates
python3 -c "
from discernus.core.capability_registry import CapabilityRegistry
registry = CapabilityRegistry()
print(f'Extensions loaded: {len(registry.extended_agents)}')
"
```

### **Security Updates**
```bash
# Critical security patches
git fetch upstream
git cherry-pick upstream/security-patch-commit

# For classified environments
# 1. Receive security patches through secure channels
# 2. Apply in isolated test environment
# 3. Validate security compliance
# 4. Deploy to production after approval
```

---

## **📋 LICENSING & COMPLIANCE STRATEGY**

### **GPL Core + Ecosystem Model**
```
┌─────────────────────────────────────────────────────────────┐
│                      DISCERNUS ECOSYSTEM                    │
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   GPL CORE      │  │   EXTENSIONS    │  │   RESEARCH  │ │
│  │                 │  │                 │  │             │ │
│  │ • Runtime       │  │ • MIT/Apache    │  │ • Private   │ │
│  │ • Agents        │  │ • BSD/ISC       │  │ • Classified│ │
│  │ • Security      │  │ • Public Domain │  │ • Commercial│ │
│  │ • Infrastructure│  │ • Proprietary   │  │ • Academic  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│         │                       │                   │       │
│         ▼                       ▼                   ▼       │
│  MUST STAY GPL           CAN BE ANY LICENSE    ALWAYS PRIVATE│
└─────────────────────────────────────────────────────────────┘
```

### **Compliance Guidelines**

**GPL Core Requirements**
- Any changes to core Discernus code must be GPL
- If you distribute modified core, source must be available
- Extensions are NOT considered derivative works
- Research data is NOT affected by GPL

**Extension Licensing**
- Extensions can use any license (MIT, Apache, BSD, proprietary)
- Extensions are separate works, not GPL derivatives
- Can be kept private or shared openly
- No obligation to share proprietary extensions

**Research Data**
- Research data is always private by default
- No GPL obligations on research outputs
- Can be published or kept confidential
- Research notebooks can be shared under any license

### **Compliance Examples**

**✅ Compliant: Academic Research**
```bash
# GPL core + MIT extensions + public research
git clone https://github.com/discernus/discernus.git  # GPL
extensions/linguistics.yaml                           # MIT license
research_sessions/political_rhetoric/                 # Can be public
publications/paper.pdf                                # Any license
```

**✅ Compliant: Commercial Use**
```bash
# GPL core + proprietary extensions + private research
git clone https://github.com/discernus/discernus.git  # GPL
extensions/proprietary/brand_analysis.yaml           # Proprietary
research_sessions/market_research/                    # Private
reports/client_deliverable.pdf                       # Private
```

**✅ Compliant: Government Use**
```bash
# GPL core + classified extensions + classified research
git clone https://github.com/discernus/discernus.git  # GPL
extensions/classified/sigint.yaml                     # Classified
research_sessions/intelligence/                       # Classified
products/threat_assessment.pdf                        # Classified
```

**❌ Non-Compliant: Modified Core Distribution**
```bash
# Problem: Distributing modified GPL core without source
# Solution: Provide source code or contribute changes back
```

---

## **🚀 DEPLOYMENT SCENARIOS**

### **Scenario 1: Individual Academic**
```bash
# Simple local installation
git clone https://github.com/discernus/discernus.git
cd discernus
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m discernus.web.app
```

### **Scenario 2: University Department**
```bash
# Shared server deployment
sudo apt update
sudo apt install python3 python3-venv postgresql
git clone https://github.com/discernus/discernus.git /opt/discernus
cd /opt/discernus
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure for multi-user
vim .env
# Set DATABASE_URL=postgresql://user:pass@localhost/discernus
# Set DISCERNUS_SHARED_MODE=true
# Set DISCERNUS_USER_ISOLATION=true

# Start service
python3 -m discernus.web.app --host 0.0.0.0 --port 8080
```

### **Scenario 3: Government Agency**
```bash
# Air-gapped deployment
# 1. Download dependencies on internet-connected system
pip download -r requirements.txt -d ./packages/

# 2. Transfer to air-gapped system
scp -r packages/ airgapped-system:/tmp/

# 3. Install on air-gapped system
cd /secure/discernus
python3 -m venv venv
source venv/bin/activate
pip install --no-index --find-links /tmp/packages/ -r requirements.txt

# 4. Configure for offline mode
vim .env
# Set DISCERNUS_MODE=offline
# Set DISCERNUS_MODELS_PATH=/secure/models/
# Set DISCERNUS_AUDIT_LOG=/secure/logs/discernus_audit.log

# 5. Start with security logging
python3 -m discernus.web.app --audit-mode --classification-level=SECRET
```

### **Scenario 4: International Collaboration**
```bash
# Encrypted multi-site deployment
# Site A (US)
git clone https://secure-git.defense.gov/nato-project.git
cd nato-project
docker-compose up -d  # Includes VPN, encryption, audit logging

# Site B (EU)
git clone https://secure-git.europa.eu/nato-project.git
cd nato-project
docker-compose up -d  # Mirrors site A configuration

# Synchronization via secure channels
# Automated nightly sync of approved changes
```

---

## **🎯 STRATEGIC ADVANTAGES**

### **For Academics**
- ✅ **Free core** - No licensing fees for research
- ✅ **Extensible** - Add any tools needed for research
- ✅ **Reproducible** - Full git history and provenance
- ✅ **Collaborative** - Easy sharing with colleagues
- ✅ **Citable** - DOI system for research outputs
- ✅ **Open source** - Transparent methodology

### **For Government/Defense**
- ✅ **Security compliant** - Air-gapped deployment supported
- ✅ **No vendor lock-in** - GPL ensures continued access
- ✅ **Classified extensions** - Private tooling for sensitive work
- ✅ **International collaboration** - Secure multi-site protocols
- ✅ **Audit trails** - Complete logging for compliance
- ✅ **Classification handling** - Built-in security controls

### **For Enterprise**
- ✅ **Cost effective** - GPL core is free to use
- ✅ **Proprietary extensions** - Maintain competitive advantage
- ✅ **Compliance friendly** - Clear licensing boundaries
- ✅ **Professional support** - Commercial support available
- ✅ **Scalable** - From individual to enterprise deployment
- ✅ **Integration ready** - APIs for existing systems

---

## **📞 SUPPORT & RESOURCES**

### **Community Support**
- **GitHub Issues**: Bug reports and feature requests
- **Discussion Forums**: Community help and sharing
- **Extension Marketplace**: Shared extensions and tools
- **Documentation**: Comprehensive guides and tutorials

### **Professional Support**
- **Enterprise Support**: SLA-backed support for organizations
- **Training**: Workshops and certification programs
- **Consulting**: Custom extension development
- **Integration**: Help with existing system integration

### **Government Support**
- **Security Clearance**: Cleared personnel available
- **Compliance**: FISMA, FedRAMP, and other certifications
- **Custom Development**: Classified extension development
- **Deployment**: Secure deployment assistance

---

**This deployment and collaboration model enables Discernus to serve everyone from individual academics to major defense contractors while maintaining security, compliance, and collaboration capabilities appropriate to each use case.** 