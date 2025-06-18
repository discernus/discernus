# Discernus Software Platform Restructuring Plan (Option 4)
**Discernus: Technical Implementation for Established Frameworks**

*Date: December 2024*  
*Status: Comprehensive Technical Plan*  
*Strategic Approach: Option 4 - Platform Infrastructure for Established Academic Frameworks*

---

## Executive Summary

This document outlines the comprehensive technical restructuring required to transform the current Discernus platform from a research prototype supporting novel theoretical frameworks into production-ready methodological infrastructure for established academic frameworks. The restructuring focuses on implementing three validated frameworks (Moral Foundations Theory, Political Framing Theory, Cultural Theory) with systematic validation infrastructure and expert consultation capabilities.

**Core Technical Transformation**: From prototype research tool to production methodological infrastructure  
**Primary Goal**: Build credible platform for systematic framework comparison and validation  
**Success Criteria**: Platform adoption by computational social science community, validation against established measures, expert endorsement

---

## Current Platform Assessment

### Current System Status Analysis
Based on comprehensive platform review from June 2025:

**✅ Strong Foundation Components**:
- **Framework Architecture**: Production-ready with database as source of truth
- **Mathematical Foundation**: Circular coordinate system operational
- **Database Infrastructure**: PostgreSQL with complete schema and framework_data JSON storage
- **Development Tools**: Comprehensive CLI and validation tools working
- **Framework Management**: Symlink-based switching system with 4-5 frameworks available

**🚨 Critical Gaps Identified** (102 distinct issues):
- **LLM Integration**: Manual workflow rather than automated API calls
- **Import/Dependency Issues**: 20 errors including get_db_session import failures
- **Visualization Pipeline**: HTML output format issues, rendering problems
- **Service Integration**: Backend services not fully connected to pipeline
- **Configuration Management**: Missing framework config files

**Current Pipeline Success Rate**: 0% (0/10 tests passed)  
**Manual Interventions Required**: 30 across different system components

### Platform Architecture Strengths
1. **Transaction Integrity Architecture**: Fail-fast, fail-clean philosophy implemented
2. **Framework Agnostic Design**: Universal core with framework extensions
3. **Quality Assurance**: Six-layer validation focusing on procedural reliability
4. **Experimental Design Framework**: Five-dimensional space (TEXTS × FRAMEWORKS × PROMPTS × WEIGHTING × EVALUATORS)
5. **Professional Documentation**: World-class documentation architecture with MECE principles

### Platform Architecture Weaknesses
1. **Novel Framework Dependence**: Current frameworks are unvalidated theoretical constructs
2. **Manual Validation Workflow**: No systematic comparison with established measures
3. **Limited Expert Integration**: No formal expert consultation infrastructure
4. **Academic Validation Gap**: No convergent/discriminant validity testing
5. **Community Adoption Barriers**: Complex theoretical requirements limit adoption

---

## Technical Restructuring Requirements

### 1. Framework Implementation Infrastructure

#### 1.1 Established Framework Integration
**Objective**: Replace current novel frameworks with rigorous implementations of established academic frameworks

**Current Framework Removal**:
- Remove/archive existing frameworks: `civic_virtue`, `fukuyama_identity`, `three_wells_political`
- Maintain framework architecture and switching infrastructure
- Preserve framework management and validation systems

**New Framework Implementation**:

##### Moral Foundations Theory (MFT) Framework
**Technical Requirements**:
- Import validated MFT lexicons from established research (Haidt et al.)
- Implement five-foundation scoring system (Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation)
- Build prompt templates based on validated MFT instruments
- Create validation protocols comparing Discernus outputs to Moral Foundations Questionnaire (MFQ)
- Integrate expert consultation hooks for Jonathan Haidt and collaborators

**Implementation Details**:
```yaml
# frameworks/moral_foundations_theory/framework.json
{
  "framework_id": "moral_foundations_theory",
  "version": "1.0.0",
  "theoretical_grounding": "Haidt et al. (2009-2024)",
  "expert_consultants": ["Jonathan Haidt", "Jesse Graham", "Ravi Iyer"],
  "foundations": {
    "care_harm": {
      "positive_lexicon": ["care", "compassion", "protect", "nurture"],
      "negative_lexicon": ["harm", "hurt", "suffering", "cruelty"],
      "validation_instrument": "MFQ-30 Care subscale"
    }
  },
  "validation_protocols": {
    "construct_validity": "MFQ correlation study",
    "convergent_validity": "Behavioral measure correlation",
    "expert_review": "Haidt lab approval process"
  }
}
```

##### Political Framing Theory Framework
**Technical Requirements**:
- Implement Entman's frame definition operationalization
- Build Lakoff conceptual metaphor detection algorithms
- Create frame competition analysis capabilities
- Develop validation against established framing studies
- Integrate expert consultation with political communication scholars

**Implementation Details**:
```yaml
# frameworks/political_framing_theory/framework.json
{
  "framework_id": "political_framing_theory",
  "version": "1.0.0",
  "theoretical_grounding": "Entman (1993), Lakoff (2002)",
  "expert_consultants": ["Robert Entman", "Shanto Iyengar"],
  "frame_types": {
    "problem_definition": {
      "indicators": ["crisis", "challenge", "opportunity"],
      "detection_algorithms": "keyword_contextual_analysis"
    },
    "causal_interpretation": {
      "indicators": ["because", "due to", "caused by"],
      "detection_algorithms": "causal_chain_analysis"
    },
    # ... other frame elements
  },
  "validation_protocols": {
    "replication_studies": ["Classic framing experiments"],
    "expert_coding_comparison": "Inter-rater reliability assessment"
  }
}
```

##### Cultural Theory Framework
**Technical Requirements**:
- Implement Douglas & Wildavsky grid-group theory
- Build four ways of life classification (Hierarchist, Individualist, Egalitarian, Fatalist)
- Create cultural bias indicators and worldview protocols
- Develop validation against cultural cognition scales
- Integrate expert consultation with cultural theory researchers

**Implementation Details**:
```yaml
# frameworks/cultural_theory/framework.json
{
  "framework_id": "cultural_theory",
  "version": "1.0.0",
  "theoretical_grounding": "Douglas & Wildavsky (1982), Kahan et al. (2012)",
  "expert_consultants": ["Dan Kahan", "Cultural Cognition Project"],
  "worldviews": {
    "hierarchist": {
      "indicators": ["authority", "tradition", "order", "respect"],
      "risk_perception": "technology_optimistic"
    },
    "egalitarian": {
      "indicators": ["equality", "social justice", "collective action"],
      "risk_perception": "environmental_concern"
    },
    # ... other worldviews
  },
  "validation_protocols": {
    "cultural_cognition_scales": "CCS correlation study",
    "risk_perception_validation": "Behavioral consistency check"
  }
}
```

#### 1.2 Framework Architecture Enhancements
**Required Modifications**:

1. **Expert Consultation Integration**
   - Add expert_consultants field to framework configuration
   - Build expert review workflow integration
   - Create expert approval tracking system
   - Implement collaborative development protocols

2. **Validation Infrastructure**
   - Add validation_protocols configuration section
   - Implement systematic validation study management
   - Build convergent/discriminant validity testing
   - Create expert validation approval workflows

3. **Academic Integration**
   - Add theoretical_grounding documentation requirements
   - Implement citation tracking and bibliography management
   - Build replication study support infrastructure
   - Create academic publication integration hooks

### 2. LLM Integration Infrastructure Overhaul

#### 2.1 Automated API Integration
**Objective**: Replace manual LLM workflow with automated, scalable API-based analysis

**Current Manual Workflow Issues**:
- Human-in-the-loop requirement limits throughput
- Inconsistent prompt compliance across LLMs
- No systematic variance tracking
- Limited scalability for large corpora analysis

**Required API Integration**:

1. **Multi-Provider API Wrapper**
```python
# src/api_clients/unified_llm_client.py
class UnifiedLLMClient:
    def __init__(self):
        self.providers = {
            'openai': OpenAIClient(),
            'anthropic': AnthropicClient(), 
            'google': GoogleClient()
        }
    
    def analyze_text(self, text, framework_id, model, validation_runs=3):
        """Execute multi-run analysis with variance tracking"""
        results = []
        for run in range(validation_runs):
            result = self._single_analysis(text, framework_id, model)
            results.append(result)
        
        return self._aggregate_with_confidence(results)
```

2. **Batch Processing Engine**
```python
# src/processing/batch_analyzer.py
class BatchAnalyzer:
    def __init__(self, llm_client, framework_manager):
        self.llm_client = llm_client
        self.framework_manager = framework_manager
        self.queue_manager = QueueManager()
    
    def process_corpus(self, corpus_id, framework_id, model_list):
        """Process large corpus with systematic analysis"""
        # Queue management and batch processing
        pass
    
    def track_progress(self, batch_id):
        """Real-time progress tracking with resumption"""
        # Progress monitoring implementation
        pass
```

3. **Quality Control and Variance Tracking**
```python
# src/quality/variance_tracker.py
class VarianceTracker:
    def analyze_consistency(self, multi_run_results):
        """Analyze LLM response consistency across runs"""
        # Statistical variance analysis
        pass
    
    def detect_anomalies(self, results, thresholds):
        """Identify suspicious or inconsistent responses"""
        # Anomaly detection implementation
        pass
    
    def generate_confidence_metrics(self, results):
        """Generate statistical confidence measures"""
        # Confidence interval calculation
        pass
```

#### 2.2 Systematic Validation Infrastructure
**Objective**: Build comprehensive validation system for framework implementations

**Validation Study Management**:

1. **Construct Validation System**
```python
# src/validation/construct_validator.py
class ConstructValidator:
    def __init__(self, framework_id):
        self.framework_id = framework_id
        self.established_measures = self._load_established_measures()
    
    def run_construct_validation(self, text_corpus, participant_responses):
        """Compare Discernus outputs with established measures"""
        # Correlation analysis with validated instruments
        pass
    
    def convergent_validity_test(self, related_constructs):
        """Test convergent validity with theoretically related measures"""
        # Convergent validity implementation
        pass
    
    def discriminant_validity_test(self, unrelated_constructs):
        """Test discriminant validity with theoretically unrelated measures"""
        # Discriminant validity implementation
        pass
```

2. **Expert Validation System**
```python
# src/validation/expert_validator.py
class ExpertValidator:
    def __init__(self, framework_id):
        self.framework_id = framework_id
        self.expert_panel = self._load_expert_panel()
    
    def submit_for_expert_review(self, implementation_details):
        """Submit framework implementation for expert evaluation"""
        # Expert consultation workflow
        pass
    
    def track_expert_feedback(self, review_id):
        """Track and integrate expert feedback"""
        # Feedback integration system
        pass
    
    def approval_workflow(self, expert_reviews):
        """Manage expert approval process"""
        # Approval tracking implementation
        pass
```

#### 2.3 Human-Computer Comparison Infrastructure
**Objective**: Systematic comparison between human expert analysis and computational analysis

**Comparative Analysis System**:

1. **Human Expert Integration**
```python
# src/validation/human_computer_comparator.py
class HumanComputerComparator:
    def setup_comparison_study(self, text_sample, expert_panel, framework_id):
        """Setup systematic human vs computer comparison"""
        # Study design and management
        pass
    
    def collect_human_analyses(self, study_id):
        """Collect and validate human expert analyses"""
        # Human analysis collection system
        pass
    
    def run_comparative_analysis(self, human_results, computer_results):
        """Statistical comparison of human vs computer analyses"""
        # Comparative statistical analysis
        pass
    
    def identify_boundary_conditions(self, comparison_results):
        """Identify contexts where human analysis is superior"""
        # Boundary condition analysis
        pass
```

### 3. Database and Storage Architecture Updates

#### 3.1 Validation Data Storage
**Required Schema Extensions**:

```sql
-- Expert consultation tracking
CREATE TABLE expert_consultations (
    id UUID PRIMARY KEY,
    framework_id VARCHAR NOT NULL,
    expert_id VARCHAR NOT NULL,
    consultation_type VARCHAR NOT NULL, -- 'implementation_review', 'validation_approval'
    status VARCHAR NOT NULL, -- 'pending', 'in_progress', 'completed', 'approved'
    feedback JSONB,
    approval_decision VARCHAR, -- 'approved', 'rejected', 'revision_required'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Validation study management
CREATE TABLE validation_studies (
    id UUID PRIMARY KEY,
    framework_id VARCHAR NOT NULL,
    study_type VARCHAR NOT NULL, -- 'construct', 'convergent', 'discriminant', 'expert'
    study_design JSONB NOT NULL,
    status VARCHAR NOT NULL, -- 'planned', 'active', 'completed', 'published'
    participant_count INTEGER,
    results JSONB,
    statistical_summary JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Multi-run analysis results
CREATE TABLE multi_run_analyses (
    id UUID PRIMARY KEY,
    text_content_hash VARCHAR NOT NULL,
    framework_id VARCHAR NOT NULL,
    model_id VARCHAR NOT NULL,
    run_count INTEGER NOT NULL,
    individual_results JSONB NOT NULL, -- Array of individual run results
    aggregated_results JSONB NOT NULL, -- Mean scores with confidence intervals
    variance_metrics JSONB NOT NULL, -- Statistical variance analysis
    quality_flags JSONB, -- Anomaly detection flags
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Human-computer comparison studies
CREATE TABLE human_computer_comparisons (
    id UUID PRIMARY KEY,
    study_id UUID REFERENCES validation_studies(id),
    text_id UUID NOT NULL,
    human_results JSONB NOT NULL,
    computer_results JSONB NOT NULL,
    agreement_metrics JSONB NOT NULL,
    expert_consensus JSONB,
    boundary_conditions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.2 Framework Metadata Enhancement
**Enhanced Framework Configuration Storage**:

```sql
-- Enhanced framework metadata
ALTER TABLE frameworks ADD COLUMN expert_consultants JSONB;
ALTER TABLE frameworks ADD COLUMN validation_protocols JSONB;
ALTER TABLE frameworks ADD COLUMN theoretical_grounding JSONB;
ALTER TABLE frameworks ADD COLUMN implementation_status VARCHAR DEFAULT 'development';
ALTER TABLE frameworks ADD COLUMN expert_approval_status VARCHAR DEFAULT 'pending';
ALTER TABLE frameworks ADD COLUMN validation_summary JSONB;
```

### 4. Visualization and Reporting Infrastructure

#### 4.1 Enhanced Visualization System
**Required Visualization Enhancements**:

1. **Validation Dashboard**
```python
# src/visualization/validation_dashboard.py
class ValidationDashboard:
    def generate_construct_validity_report(self, validation_study_id):
        """Generate comprehensive construct validity visualization"""
        # Correlation matrices, scatterplots, statistical summaries
        pass
    
    def expert_consensus_visualization(self, expert_comparison_id):
        """Visualize expert agreement and disagreement patterns"""
        # Inter-rater reliability charts, consensus mapping
        pass
    
    def human_computer_comparison_charts(self, comparison_study_id):
        """Visualize human vs computer analysis comparison"""
        # Agreement visualizations, boundary condition maps
        pass
```

2. **Multi-Run Analysis Visualization**
```python
# src/visualization/multi_run_visualizer.py
class MultiRunVisualizer:
    def confidence_interval_charts(self, multi_run_results):
        """Visualize confidence intervals for multi-run analysis"""
        # Error bars, confidence bands, variance indicators
        pass
    
    def variance_analysis_dashboard(self, variance_metrics):
        """Dashboard for LLM response variance analysis"""
        # Variance trends, consistency metrics, quality indicators
        pass
```

#### 4.2 Academic Publication Integration
**Publication-Ready Output Generation**:

1. **Academic Report Generator**
```python
# src/reporting/academic_reporter.py
class AcademicReporter:
    def generate_validation_report(self, framework_id):
        """Generate comprehensive validation report for publication"""
        # Statistical tables, methodology description, results summary
        pass
    
    def create_replication_package(self, study_id):
        """Create complete replication package for academic sharing"""
        # Data, code, documentation, metadata
        pass
    
    def expert_endorsement_summary(self, framework_id):
        """Generate expert consultation and endorsement summary"""
        # Expert credentials, consultation process, approval decisions
        pass
```

### 5. Platform Integration and Testing Infrastructure

#### 5.1 Integration Testing Framework
**Comprehensive Testing for New Infrastructure**:

1. **Framework Implementation Testing**
```python
# tests/integration/test_framework_implementations.py
class TestFrameworkImplementations:
    def test_mft_implementation_validity(self):
        """Test MFT implementation against known validation data"""
        pass
    
    def test_framing_theory_replication(self):
        """Test Political Framing Theory implementation through study replication"""
        pass
    
    def test_cultural_theory_consistency(self):
        """Test Cultural Theory implementation consistency"""
        pass
```

2. **Validation Infrastructure Testing**
```python
# tests/integration/test_validation_infrastructure.py
class TestValidationInfrastructure:
    def test_construct_validation_pipeline(self):
        """Test complete construct validation workflow"""
        pass
    
    def test_expert_consultation_workflow(self):
        """Test expert consultation integration"""
        pass
    
    def test_human_computer_comparison(self):
        """Test human-computer comparison infrastructure"""
        pass
```

#### 5.2 Performance and Scalability Testing
**Platform Performance Validation**:

1. **Load Testing for API Integration**
```python
# tests/performance/test_api_performance.py
class TestAPIPerformance:
    def test_batch_processing_scalability(self):
        """Test batch processing with large corpora"""
        pass
    
    def test_multi_provider_reliability(self):
        """Test reliability across multiple LLM providers"""
        pass
    
    def test_concurrent_validation_studies(self):
        """Test concurrent validation study execution"""
        pass
```

---

## Implementation Timeline and Phases

### Phase 1: Foundation Infrastructure (Months 1-3)
**Objective**: Establish core infrastructure for established framework support

**Month 1: Database and Architecture**
- Implement enhanced database schema for validation data
- Update framework configuration architecture
- Build expert consultation infrastructure
- Create validation study management system

**Month 2: LLM Integration Overhaul** 
- Implement unified LLM API client
- Build batch processing engine
- Create variance tracking and quality control systems
- Implement multi-run analysis with confidence intervals

**Month 3: Framework Implementation Foundation**
- Remove/archive existing novel frameworks
- Build framework implementation infrastructure
- Create validation protocol integration
- Implement expert consultation workflow

### Phase 2: Established Framework Implementation (Months 4-6)
**Objective**: Implement and validate three established academic frameworks

**Month 4: Moral Foundations Theory Implementation**
- Import validated MFT lexicons and instruments
- Implement five-foundation scoring system
- Build MFT-specific prompt templates
- Create validation protocols against MFQ
- Initiate expert consultation with Haidt lab

**Month 5: Political Framing Theory Implementation**
- Implement Entman frame definition operationalization
- Build Lakoff conceptual metaphor detection
- Create frame competition analysis capabilities
- Implement validation against established framing studies
- Initiate expert consultation with political communication scholars

**Month 6: Cultural Theory Implementation**
- Implement Douglas & Wildavsky grid-group theory
- Build four ways of life classification system
- Create cultural bias indicators and worldview protocols
- Implement validation against cultural cognition scales
- Initiate expert consultation with cultural theory researchers

### Phase 3: Validation Infrastructure (Months 7-9)
**Objective**: Build and execute comprehensive validation studies

**Month 7: Construct Validation System**
- Implement construct validation infrastructure
- Build convergent and discriminant validity testing
- Create systematic validation study management
- Execute initial validation studies for all three frameworks

**Month 8: Human-Computer Comparison Infrastructure**
- Implement human expert integration system
- Build comparative analysis infrastructure
- Create boundary condition identification system
- Execute human-computer comparison studies

**Month 9: Expert Validation and Approval**
- Complete expert consultation process for all frameworks
- Integrate expert feedback and approval decisions
- Finalize framework implementations based on expert guidance
- Document expert endorsement process

### Phase 4: Platform Optimization and Publication (Months 10-12)
**Objective**: Optimize platform and prepare for publication and community adoption

**Month 10: Platform Optimization**
- Performance optimization based on validation study experience
- User experience improvements for research workflow
- Documentation enhancement for community adoption
- Integration testing and quality assurance

**Month 11: Publication Preparation**
- Generate comprehensive validation reports
- Create academic publication materials
- Build replication packages for community sharing
- Prepare platform for public release

**Month 12: Community Release and Adoption**
- Public platform release with documentation
- Academic publication submission
- Community engagement and adoption facilitation
- Ongoing support infrastructure establishment

---

## Critical Dependencies and Risk Mitigation

### Expert Consultation Dependencies
**Risk**: Expert availability and engagement limitations
**Mitigation**: Early engagement, flexible timelines, multiple expert options

### LLM API Integration Risks
**Risk**: API reliability, cost, and rate limiting issues
**Mitigation**: Multi-provider redundancy, cost monitoring, graceful degradation

### Validation Study Complexity
**Risk**: Validation studies require significant resources
**Mitigation**: Phased approach, automated infrastructure, strategic partnerships

### Platform Migration Challenges
**Risk**: Disruption to existing platform functionality during restructuring
**Mitigation**:
- Parallel development approach maintaining current functionality
- Comprehensive testing infrastructure and rollback procedures
- Staged migration with user communication and training
- Maintaining backward compatibility where possible

---

## Success Metrics and Evaluation Criteria

### Technical Performance Metrics
1. **Platform Reliability**: 99%+ uptime for API integration
2. **Validation Success**: Successful validation against established measures for all three frameworks
3. **Expert Approval**: Formal approval from framework originators
4. **Performance Scalability**: Support for large-scale corpus analysis (10,000+ documents)
5. **Community Adoption**: Platform usage by external researchers

### Academic Impact Metrics
1. **Publication Success**: Acceptance in top-tier computational social science journal
2. **Expert Endorsement**: Formal endorsement from framework originators
3. **Replication Studies**: Successful replication of established findings using Discernus
4. **Community Engagement**: External researcher adoption and collaboration
5. **Methodological Contribution**: Recognition as methodological advancement

### Platform Quality Metrics
1. **Validation Coverage**: 100% validation against established measures
2. **Expert Integration**: Successful consultation workflow with all framework experts
3. **Documentation Quality**: Comprehensive documentation enabling community adoption
4. **User Experience**: Streamlined workflow for academic researchers
5. **Open Science**: Complete replication packages and open-source availability

---

## Resource Requirements and Budget Considerations

### Development Resources
1. **Backend Development**: 6-8 months full-time for infrastructure development
2. **Framework Implementation**: 3-4 months per framework (parallel development possible)
3. **Validation Infrastructure**: 4-6 months for comprehensive validation system
4. **Expert Consultation**: Ongoing engagement throughout development process
5. **Testing and QA**: 2-3 months for comprehensive testing and validation

### Infrastructure and Tools
1. **Database Infrastructure**: Enhanced PostgreSQL configuration with validation data storage
2. **LLM API Costs**: Budget for systematic validation studies and testing
3. **Compute Resources**: Scalable infrastructure for batch processing and analysis
4. **Expert Consultation**: Budget for expert time and collaboration
5. **Publication Costs**: Open access publication fees and conference presentation

### Human Resources
1. **Technical Lead**: Full-time development coordination and architecture
2. **Framework Specialists**: Part-time specialists for each framework implementation
3. **Validation Coordinator**: Full-time validation study design and execution
4. **Expert Relations**: Part-time coordination of expert consultation process
5. **Documentation Specialist**: Technical writing and documentation development

---

## Conclusion

This comprehensive restructuring plan transforms the current Discernus platform from a research prototype into production-ready methodological infrastructure for computational social science. The plan addresses all critical gaps identified in the current system while building the validation infrastructure necessary for academic credibility and community adoption.

The restructuring eliminates dependence on novel theoretical frameworks in favor of rigorous implementation of established academic approaches, creating a solid foundation for methodological contribution rather than theoretical discovery. Success depends on systematic execution of the implementation phases, meaningful expert consultation, and comprehensive validation against established measures.

The resulting platform will provide genuine value to the computational social science community while establishing credibility for future theoretical innovation within a validated methodological framework. This approach maximizes the probability of successful publication and long-term platform adoption while creating sustainable infrastructure for academic research collaboration. 