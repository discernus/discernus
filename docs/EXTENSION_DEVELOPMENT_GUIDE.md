# Extension Development Guide
*Build Extensions for the Discernus Ecosystem*

This guide shows you how to create extensions that seamlessly integrate with Discernus's domain-neutral platform. Whether you're building academic tools, corporate analysis modules, or specialized frameworks, this guide provides the patterns and principles for sustainable extension development.

## Three Foundational Commitments for Extensions

Your extension must support Discernus's three foundational commitments:

- **Mathematical Reliability**: Extensions must enable the hybrid intelligence pattern where LLMs design analysis, secure code executes calculations, and LLMs interpret results
- **Cost Transparency**: Extensions must provide clear guidance for cost estimation and efficient resource usage
- **Complete Reproducibility**: Extensions must enable zero mystery with complete audit trails and deterministic behavior

## Drupal-Style Extension Architecture

### Core vs. Extension Boundaries

**Core Platform (Maintained by Discernus)**:
- Agent registry system
- Model registry and LLM gateway
- Secure code execution infrastructure
- Project chronolog and provenance
- Framework loading and validation

**Extension Modules (Community-Maintained)**:
- Domain-specific frameworks
- Specialized analysis agents
- Custom libraries and tools
- Visualization and reporting modules
- External API integrations

### Module Lifecycle

1. **Development**: Create and test your extension
2. **Validation**: Automated compatibility checking
3. **Publication**: Share with community
4. **Maintenance**: Updates and bug fixes
5. **Deprecation**: Sunset planning and migration

## Extension Types and Patterns

### Type 1: Library Extensions
**Purpose**: Add new computational libraries and tools
**Pattern**: Configuration-driven library whitelisting

```yaml
name: advanced_nlp_toolkit
description: Extended NLP libraries for computational linguistics
version: 1.2.0
author: Computational Linguistics Lab
license: MIT

# Mathematical Reliability: Ensure libraries support secure code execution
libraries:
  - name: spacy
    version: ">=3.4.0"
    description: Industrial-strength NLP
    security_level: high
    
  - name: transformers
    version: ">=4.20.0"
    description: Transformer models for deep NLP
    security_level: medium
    
  - name: nltk.parse
    version: ">=3.8.0"
    description: Parsing algorithms and grammars
    security_level: high

# Cost Transparency: Resource usage guidance
resource_requirements:
  memory_mb: 512
  computation_level: medium
  estimated_cost_per_use: 0.05

# Complete Reproducibility: Environment specification
environments:
  name: advanced_nlp_env
  description: Comprehensive NLP environment with consistent initialization
  
  imports:
    - import spacy
    - from transformers import pipeline
    - from nltk.parse import stanford
  
  setup_code: |
    # Reproducible model loading
    nlp = spacy.load("en_core_web_sm")
    
    # Consistent transformer initialization
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        device=-1  # CPU for consistency
    )
    
    # Custom analysis functions
    def analyze_syntax_complexity(text):
        doc = nlp(text)
        return {
            'sentence_count': len(list(doc.sents)),
            'avg_sentence_length': sum(len(sent.text.split()) for sent in doc.sents) / len(list(doc.sents)),
            'dependency_depth': max(len(list(token.ancestors)) for token in doc)
        }
  
  mock_fallbacks:
    spacy: |
      class MockSpacy:
          def load(self, model):
              return self
          def __call__(self, text):
              return type('Doc', (), {'sents': [text], 'text': text})()
      spacy = MockSpacy()
```

### Type 2: Agent Extensions
**Purpose**: Add specialized expert agents for specific domains
**Pattern**: Prompt-based agent definition with domain expertise

```yaml
name: financial_analysis_agents
description: Specialized agents for financial text analysis
version: 1.0.0
author: Financial Analytics Team
license: Commercial

# Domain-specific expert agents
agents:
  financial_risk_analyst:
    description: Expert in financial risk assessment from textual data
    domain: finance
    expertise_level: advanced
    
    # Complete Reproducibility: Standardized prompt structure
    prompt: |
      You are a financial_risk_analyst with expertise in risk assessment through textual analysis.
      
      RESEARCH QUESTION: {research_question}
      SOURCE TEXTS: {source_texts}
      EXPERT REQUEST: {expert_request}
      
      Your Expertise:
      - Credit risk assessment from financial documents
      - Market risk indicators in earnings calls
      - Operational risk detection in regulatory filings
      - Liquidity risk analysis in financial statements
      
      Mathematical Reliability Instructions:
      When performing quantitative analysis, write Python code in ```python blocks.
      Use secure calculation patterns:
      1. Load and validate data
      2. Apply financial risk models
      3. Calculate risk metrics with confidence intervals
      4. Return structured results for interpretation
      
      Cost Transparency:
      This analysis typically requires 800-1200 tokens per document.
      Recommend batch processing for large financial corpus analysis.
      
      Provide systematic risk analysis with quantitative metrics and qualitative insights.
  
  market_sentiment_analyst:
    description: Expert in market sentiment analysis from financial communications
    domain: finance
    expertise_level: intermediate
    
    prompt: |
      You are a market_sentiment_analyst specializing in financial market sentiment.
      
      RESEARCH QUESTION: {research_question}
      SOURCE TEXTS: {source_texts}
      EXPERT REQUEST: {expert_request}
      
      Your Expertise:
      - Market sentiment from earnings calls and investor communications
      - Sentiment impact on stock price movements
      - Regulatory sentiment analysis
      - Stakeholder sentiment assessment
      
      Use financial sentiment lexicons and market-specific indicators.
      Provide both quantitative sentiment scores and qualitative interpretation.

# Cost Transparency: Resource usage for financial analysis
resource_requirements:
  memory_mb: 256
  computation_level: medium
  estimated_cost_per_use: 0.03
  batch_processing_recommended: true

# Mathematical Reliability: Financial calculation environment
environments:
  name: financial_analysis_env
  description: Secure environment for financial calculations
  
  imports:
    - import pandas as pd
    - import numpy as np
    - from datetime import datetime
    - import statistics
  
  setup_code: |
    # Financial analysis functions
    def calculate_risk_metrics(returns):
        return {
            'volatility': np.std(returns),
            'var_95': np.percentile(returns, 5),
            'sharpe_ratio': np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        }
    
    def sentiment_score_to_market_impact(sentiment_score, volatility):
        # Quantitative model for sentiment-market relationship
        impact_coefficient = 0.3
        return sentiment_score * impact_coefficient * volatility
```

### Type 3: Framework Extensions
**Purpose**: Add complete analytical frameworks for specific domains
**Pattern**: Framework specification with validation and examples

```yaml
name: corporate_communication_frameworks
description: Analytical frameworks for corporate communication analysis
version: 2.0.0
author: Corporate Communication Research Group
license: Apache-2.0

# Complete frameworks with validation
frameworks:
  brand_crisis_communication:
    name: Brand Crisis Communication Analysis Framework
    version: 1.0
    description: Analyze corporate crisis communication effectiveness
    
    # Framework specification file
    specification_file: frameworks/brand_crisis_communication.md
    
    # Validation examples for reproducibility
    validation_examples:
      - input: "We sincerely apologize for the inconvenience and are working to resolve this issue immediately."
        expected_scores:
          accountability: 0.8
          transparency: 0.6
          empathy: 0.7
        rationale: "High accountability (apologize), moderate transparency (working to resolve), good empathy (sincerely)"
    
    # Cost estimation parameters
    cost_factors:
      tokens_per_document: 1200
      complexity_multiplier: 1.3
      recommended_batch_size: 10
    
    # Domain-specific libraries
    required_libraries:
      - pandas
      - textblob
      - vaderSentiment
  
  stakeholder_engagement:
    name: Stakeholder Engagement Assessment Framework
    version: 1.1
    description: Evaluate stakeholder engagement quality in corporate communications
    
    specification_file: frameworks/stakeholder_engagement.md
    
    validation_examples:
      - input: "We value your feedback and have incorporated your suggestions into our new policy."
        expected_scores:
          responsiveness: 0.9
          inclusivity: 0.7
          transparency: 0.8
        rationale: "High responsiveness (value feedback), good inclusivity (your suggestions), high transparency (incorporated)"

# Extension metadata for discoverability
metadata:
  keywords: [corporate, communication, crisis, stakeholder, brand]
  domains: [business, public_relations, corporate_communications]
  use_cases: [crisis_management, stakeholder_analysis, brand_monitoring]
  academic_fields: [communication_studies, business_administration, public_relations]
```

### Type 4: Integration Extensions
**Purpose**: Connect external services and APIs
**Pattern**: Service wrapper with authentication and rate limiting

```yaml
name: social_media_integrations
description: Social media platform integrations for text analysis
version: 1.0.0
author: Social Media Analytics Team
license: MIT

# External service integrations
integrations:
  twitter_api:
    name: Twitter API Integration
    description: Fetch and analyze Twitter data
    authentication: oauth2
    rate_limits:
      requests_per_minute: 100
      requests_per_hour: 1500
    
    # Cost transparency for API usage
    cost_structure:
      base_cost_per_request: 0.001
      premium_endpoints: 0.005
      bulk_processing_discount: 0.8
    
    # Reproducibility: Consistent data fetching
    configuration:
      default_tweet_count: 100
      include_retweets: false
      language_filter: en
      result_format: json
    
    # Integration agent
    agent_prompt: |
      You are a twitter_integration_agent specialized in Twitter data analysis.
      
      Your capabilities:
      - Fetch tweets by keyword, hashtag, or user
      - Analyze tweet sentiment and engagement
      - Track trending topics and viral content
      - Temporal analysis of social media conversations
      
      Mathematical Reliability:
      Use secure code execution for:
      - API rate limiting calculations
      - Statistical analysis of tweet metrics
      - Sentiment aggregation with confidence intervals
      
      Always provide cost estimates for API usage before execution.
  
  reddit_api:
    name: Reddit API Integration
    description: Fetch and analyze Reddit discussions
    authentication: oauth2
    rate_limits:
      requests_per_minute: 60
      requests_per_hour: 600
    
    agent_prompt: |
      You are a reddit_integration_agent specialized in Reddit discussion analysis.
      
      Your capabilities:
      - Fetch posts and comments from subreddits
      - Analyze community sentiment and engagement
      - Track discussion topics and themes
      - Identify influential users and viral content
      
      Focus on community-driven discourse patterns and discussion dynamics.

# Security and compliance
security:
  data_retention_policy: "30 days"
  privacy_compliance: [GDPR, CCPA]
  authentication_required: true
  rate_limiting_enforced: true
```

## API Contracts and Interfaces

### Extension API Contract
Every extension must implement standardized interfaces:

```python
# Extension interface specification
class ExtensionInterface:
    """Standard interface for all Discernus extensions"""
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return extension metadata"""
        return {
            'name': str,
            'version': str,
            'description': str,
            'author': str,
            'license': str,
            'compatibility': str,
            'resource_requirements': Dict[str, Any],
            'foundational_commitments': List[str]
        }
    
    def validate_compatibility(self, core_version: str) -> bool:
        """Check compatibility with core platform version"""
        pass
    
    def get_cost_estimate(self, usage_params: Dict[str, Any]) -> Dict[str, float]:
        """Provide cost transparency for extension usage"""
        pass
    
    def get_reproducibility_info(self) -> Dict[str, Any]:
        """Return reproducibility and audit trail information"""
        pass
    
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize extension with configuration"""
        pass
    
    def cleanup(self) -> bool:
        """Clean up resources on extension shutdown"""
        pass
```

### Agent Contract
All extension agents must follow the standard agent contract:

```python
class ExtensionAgent:
    """Standard interface for extension agents"""
    
    def get_prompt_template(self) -> str:
        """Return agent prompt template"""
        pass
    
    def get_required_libraries(self) -> List[str]:
        """Return list of required libraries"""
        pass
    
    def get_cost_parameters(self) -> Dict[str, Any]:
        """Return cost estimation parameters"""
        return {
            'tokens_per_use': int,
            'complexity_multiplier': float,
            'batch_processing_factor': float
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate agent input data"""
        pass
    
    def get_output_schema(self) -> Dict[str, Any]:
        """Return expected output schema for reproducibility"""
        pass
```

## Development Workflow

### 1. Extension Bootstrap
```bash
# Create extension template
python3 -c "
from discernus.core.capability_registry import create_extension
extension_file = create_extension('my_extension', 'Description of my extension')
print(f'Created: {extension_file}')
"
```

### 2. Development Environment Setup
```bash
# Development environment
python3 -m venv extension_dev
source extension_dev/bin/activate
pip install -r requirements.txt
pip install -r my_extension_requirements.txt

# Run extension validation
python3 -c "
from discernus.core.capability_registry import CapabilityRegistry
registry = CapabilityRegistry()
issues = registry.validate_extension('extensions/my_extension.yaml')
if issues:
    print('Issues to fix:')
    for issue in issues:
        print(f'- {issue}')
else:
    print('✅ Extension is valid')
"
```

### 3. Testing and Validation
```yaml
# Add to your extension.yaml
testing:
  unit_tests:
    - test_file: tests/test_my_extension.py
      description: Unit tests for extension functionality
  
  integration_tests:
    - test_file: tests/test_integration.py
      description: Integration tests with core platform
  
  validation_tests:
    - test_file: tests/test_validation.py
      description: Validation against three foundational commitments
  
  performance_tests:
    - test_file: tests/test_performance.py
      description: Performance and cost validation tests
```

### 4. Documentation Requirements
```markdown
# Extension documentation structure
my_extension/
├── README.md              # Overview and quick start
├── USAGE.md               # Detailed usage examples
├── API.md                 # API documentation
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md           # Version history
├── LICENSE                # License file
└── examples/              # Example usage scripts
    ├── basic_usage.py
    ├── advanced_features.py
    └── integration_examples.py
```

## Quality Standards

### Code Quality
- **PEP 8 compliance** for Python code
- **Type hints** for all public functions
- **Docstrings** for all modules, classes, and functions
- **Unit tests** with >80% coverage
- **Integration tests** with core platform

### Documentation Quality
- **Clear installation instructions**
- **Working examples** for all features
- **API documentation** with examples
- **Version history** with breaking changes
- **Contribution guidelines**

### Performance Standards
- **Memory usage** < 1GB for typical operations
- **Processing time** < 5 seconds for single document
- **Cost efficiency** optimized for institutional budgets
- **Scalability** tested with large corpora

### Security Standards
- **Library whitelisting** for secure execution
- **Input validation** for all user inputs
- **Authentication** for external API access
- **Rate limiting** to prevent abuse
- **Data privacy** compliance

## Foundational Commitments Integration

### Mathematical Reliability Checklist
- [ ] **Hybrid Intelligence Pattern**: LLM designs → secure code executes → LLM interprets
- [ ] **Calculation Transparency**: All mathematical operations logged and auditable
- [ ] **Error Handling**: Robust error handling for computational failures
- [ ] **Validation**: Mathematical results validated against known benchmarks

### Cost Transparency Checklist
- [ ] **Upfront Estimation**: Cost estimation before execution
- [ ] **Resource Tracking**: Memory, compute, and API usage monitoring
- [ ] **Batch Optimization**: Efficient processing for large corpora
- [ ] **Budget Controls**: Spending limits and overrun prevention

### Complete Reproducibility Checklist
- [ ] **Version Control**: All extension versions tracked
- [ ] **Environment Specification**: Complete environment setup documented
- [ ] **Deterministic Behavior**: Consistent results across runs
- [ ] **Audit Trail**: Complete logging of all operations

## Publication and Distribution

### Extension Registry
Submit your extension to the Discernus Extension Registry:

```bash
# Publish extension
python3 -c "
from discernus.extensions.registry import publish_extension
result = publish_extension('extensions/my_extension.yaml')
print(f'Publication result: {result}')
"
```

### Metadata Requirements
```yaml
# Required metadata for publication
publication:
  name: my_extension
  version: 1.0.0
  description: Brief description of extension functionality
  long_description: |
    Detailed description of extension capabilities,
    use cases, and benefits.
  
  author: Extension Developer
  author_email: developer@institution.edu
  maintainer: Extension Maintainer
  maintainer_email: maintainer@institution.edu
  
  license: MIT
  homepage: https://github.com/user/my_extension
  repository: https://github.com/user/my_extension
  documentation: https://my-extension.readthedocs.io
  
  keywords: [domain, analysis, nlp, academic]
  categories: [text_analysis, academic_tools, domain_specific]
  
  # Platform compatibility
  discernus_version: ">=1.0.0"
  python_version: ">=3.8"
  
  # Resource requirements
  memory_mb: 512
  disk_mb: 100
  cpu_cores: 1
  
  # Security classification
  security_review: completed
  data_privacy: compliant
  external_dependencies: listed
```

### Community Guidelines
- **Clear documentation** with examples
- **Responsive maintenance** with timely updates
- **Community support** through issues and discussions
- **Backward compatibility** when possible
- **Migration guides** for breaking changes

## Advanced Extension Patterns

### Multi-Domain Extensions
```yaml
name: cross_domain_analysis
description: Cross-domain analytical capabilities

# Multiple domain support
domains:
  academic:
    frameworks: [literary_analysis, discourse_analysis]
    agents: [literature_expert, discourse_analyst]
  
  corporate:
    frameworks: [brand_analysis, stakeholder_communication]
    agents: [brand_analyst, stakeholder_expert]
  
  journalism:
    frameworks: [source_credibility, fact_checking]
    agents: [credibility_analyst, fact_checker]

# Shared infrastructure
shared_environments:
  cross_domain_env:
    setup_code: |
      # Common utilities for all domains
      def domain_adaptive_analysis(text, domain):
          # Adaptive analysis based on domain
          pass
```

### Temporal Extensions
```yaml
name: temporal_analysis_suite
description: Time-series and temporal analysis capabilities

# Temporal analysis patterns
temporal_capabilities:
  trend_analysis:
    description: Analyze trends over time
    time_granularity: [daily, weekly, monthly, yearly]
    
  change_detection:
    description: Detect significant changes in temporal data
    algorithms: [changepoint, anomaly_detection, trend_breaks]
  
  longitudinal_analysis:
    description: Long-term pattern analysis
    minimum_timespan: 30_days
    maximum_timespan: 10_years

# Temporal-aware agents
agents:
  temporal_analyst:
    prompt: |
      You are a temporal_analyst specialized in time-series text analysis.
      
      Your capabilities:
      - Trend detection in text corpora over time
      - Change point analysis for topic evolution
      - Longitudinal pattern recognition
      - Temporal correlation analysis
      
      Use temporal analysis libraries and statistical methods.
```

### Collaborative Extensions
```yaml
name: collaborative_research_tools
description: Tools for collaborative research workflows

# Multi-user collaboration support
collaboration:
  version_control:
    description: Track changes in collaborative analysis
    features: [diff_tracking, merge_conflict_resolution, annotation_history]
  
  access_control:
    description: Manage access to shared resources
    levels: [read_only, contributor, maintainer, admin]
  
  workflow_management:
    description: Coordinate collaborative research workflows
    features: [task_assignment, review_cycles, approval_workflows]

# Collaborative agents
agents:
  collaboration_coordinator:
    prompt: |
      You are a collaboration_coordinator managing multi-user research workflows.
      
      Your capabilities:
      - Coordinate analysis tasks across team members
      - Manage version control for collaborative research
      - Track progress and resolve conflicts
      - Facilitate peer review processes
      
      Focus on efficient collaboration and quality assurance.
```

## Extension Lifecycle Management

### Version Management
```yaml
# Semantic versioning for extensions
version_policy:
  major: Breaking changes to API or behavior
  minor: New features, backward compatible
  patch: Bug fixes, no feature changes
  
  # Version compatibility matrix
  compatibility:
    "1.0.x": ["discernus>=1.0.0,<2.0.0"]
    "1.1.x": ["discernus>=1.1.0,<2.0.0"]
    "2.0.x": ["discernus>=2.0.0,<3.0.0"]
```

### Migration Support
```yaml
# Migration assistance for version updates
migration:
  from_version: "1.0.0"
  to_version: "2.0.0"
  
  breaking_changes:
    - change: "Agent prompt format updated"
      impact: "Existing agents may need prompt updates"
      migration_guide: "docs/migration_v1_to_v2.md"
    
    - change: "New required parameter for cost estimation"
      impact: "Extensions must implement get_cost_estimate()"
      migration_guide: "docs/api_changes.md"
  
  automated_migration:
    script: "scripts/migrate_v1_to_v2.py"
    validation: "scripts/validate_migration.py"
```

### Deprecation Policy
```yaml
# Deprecation and sunset planning
deprecation:
  policy: "12 months advance notice"
  
  phases:
    - phase: "deprecation_notice"
      duration: "6 months"
      actions: ["warnings", "documentation_updates"]
    
    - phase: "legacy_support"
      duration: "6 months"
      actions: ["limited_support", "migration_assistance"]
    
    - phase: "sunset"
      duration: "immediate"
      actions: ["removal", "archive"]
```

## Community Integration

### Extension Marketplace
- **Discover extensions** by domain, functionality, or author
- **Rate and review** extensions based on quality and usefulness
- **Track compatibility** with core platform versions
- **Monitor security** and maintenance status

### Contribution Workflow
1. **Fork and develop** your extension
2. **Test thoroughly** against platform requirements
3. **Submit for review** through standard process
4. **Address feedback** from community reviewers
5. **Publish** to extension registry
6. **Maintain** with updates and support

### Quality Assurance
- **Automated testing** for all extensions
- **Security scanning** for vulnerabilities
- **Performance benchmarking** for efficiency
- **Compatibility checking** with platform versions

**Success Indicator**: Your extension should enable researchers to say "This tool seamlessly extends Discernus for my specific needs" - amplifying platform capabilities while maintaining the three foundational commitments.

---

*This guide enables creation of extensions that maintain Discernus's three foundational commitments while providing powerful domain-specific capabilities. The result is a thriving ecosystem of specialized tools that serve researchers, analysts, and organizations across disciplines.* 