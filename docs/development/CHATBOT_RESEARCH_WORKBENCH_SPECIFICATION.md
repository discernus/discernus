# Narrative Gravity Analysis Chatbot Research Workbench
## Technical Specification v1.0

### 🎯 Vision Statement

Transform the narrative gravity analysis workflow from complex web forms to natural conversational research, enabling researchers to explore political discourse through intuitive dialogue while maintaining academic rigor and methodological precision.

---

## 1. Core Requirements

### 1.1 Domain-Constrained Intelligence
**Requirement**: Chatbot must stay within narrative analysis domain
- **Domain Keywords**: framework, analysis, dipole, narrative, gravity, political, discourse, civic, identity, recognition, thymos, creedal, ethnic, democratic, megalothymic
- **Constraint Mechanism**: Keyword matching + exclusion filters + redirect responses
- **Success Criteria**: >95% accuracy filtering off-topic queries
- **Fallback Response**: Standardized redirect to domain-appropriate suggestions

### 1.2 Natural Research Workflow
**Requirement**: Support researcher's natural thought process
- **Conversational Analysis**: "Analyze this Trump speech transcript"
- **Comparative Queries**: "Now compare this to the Biden speech we analyzed earlier"
- **Methodological Questions**: "What does a high Megalothymic Thymos score mean?"
- **Framework Exploration**: "Show me how this would score under the Civic Virtue framework"

### 1.3 Academic Rigor
**Requirement**: Maintain scientific methodology and reproducibility
- **Transparent Scoring**: Show framework calculations and justifications
- **Provenance Tracking**: Complete audit trail of analysis decisions
- **Export Capabilities**: Academic formats, statistical scripts, replication packages
- **Methodology Documentation**: Explain theoretical foundations and limitations

---

## 2. Architecture Overview

### 2.1 System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Chatbot Interface                        │
├─────────────────────────────────────────────────────────────┤
│ • Natural Language Processing                               │
│ • Domain Constraint Engine                                  │
│ • Context Management                                        │
│ • Response Generation                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Integration Layer                         │
├─────────────────────────────────────────────────────────────┤
│ • Input Parser (Text/URL/File)                             │
│ • Framework Manager Interface                               │
│ • Analysis Engine Connector                                 │
│ • Visualization Generator                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Existing Infrastructure                      │
├─────────────────────────────────────────────────────────────┤
│ • Framework Manager                                         │
│ • Analysis Engine                                           │
│ • Visualization Tools                                       │
│ • Database & API                                           │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack
- **Frontend**: React + TypeScript for web interface
- **Backend**: FastAPI integration with existing Python infrastructure
- **LLM Integration**: OpenAI/Anthropic APIs for conversational interface
- **Database**: PostgreSQL (existing)
- **Visualization**: D3.js/Chart.js embedded in chat responses

---

## 3. Phase 1: Core Chatbot Foundation

### 3.1 Duration: 2-3 weeks

### 3.2 Deliverables

#### 3.2.1 Domain-Constrained Chat Engine
```python
class NarrativeGravityBot:
    def __init__(self):
        self.current_framework = "fukuyama_identity"  # Default
        self.conversation_context = {}
        self.domain_validator = DomainConstraintEngine()
        
    def handle_query(self, query: str) -> ChatResponse:
        # Domain validation
        # Intent classification  
        # Response generation
        # Context updating
```

**Features**:
- **Intent Classification**: Framework questions, analysis requests, methodology queries
- **Context Management**: Track current framework, previous analyses, user preferences
- **Domain Enforcement**: >95% accuracy filtering with graceful redirects
- **Response Templates**: Structured responses for common query types

#### 3.2.2 Framework Integration
```python
class FrameworkInterface:
    def get_available_frameworks(self) -> List[Framework]
    def switch_framework(self, framework_name: str) -> bool
    def explain_framework(self, framework_name: str) -> str
    def get_dipole_details(self, dipole_name: str) -> DipoleInfo
```

**Integration Points**:
- **Framework Manager**: Direct integration with existing `src/narrative_gravity/framework_manager.py`
- **Configuration**: Read from existing `frameworks/` directory structure
- **Validation**: Use existing framework validation logic

#### 3.2.3 Basic Analysis Interface
```python
class AnalysisInterface:
    def analyze_text(self, text: str, framework: str) -> AnalysisResult
    def explain_scores(self, result: AnalysisResult) -> str
    def generate_summary(self, result: AnalysisResult) -> str
```

**Analysis Features**:
- **Text Input**: Direct paste, basic validation
- **Single Framework**: Use current active framework
- **Score Explanation**: Natural language explanation of results
- **Basic Visualization**: ASCII art or simple charts

### 3.3 Success Criteria
- [ ] Domain constraint >95% accuracy on test queries
- [ ] Framework switching works correctly
- [ ] Basic text analysis produces valid results
- [ ] Conversation context maintained across turns
- [ ] Integration with existing analysis engine successful

---

## 4. Phase 2: Enhanced Analysis Capabilities

### 4.1 Duration: 3-4 weeks

### 4.2 Deliverables

#### 4.2.1 Multi-Input Processing
```python
class InputProcessor:
    def process_url(self, url: str) -> str  # Extract text from URLs
    def process_file(self, file_upload: File) -> str  # Handle file uploads
    def process_speech_reference(self, description: str) -> str  # Find known speeches
```

**Input Sources**:
- **URL Processing**: YouTube transcripts, news articles, speech repositories
- **File Upload**: PDF, TXT, DOCX, CSV formats
- **Speech Database**: Integration with existing corpus
- **Batch Processing**: Multiple files or URLs at once

#### 4.2.2 Advanced Visualization
```python
class VisualizationEngine:
    def generate_coordinate_plot(self, analysis: AnalysisResult) -> SVG
    def generate_comparative_chart(self, analyses: List[AnalysisResult]) -> SVG
    def generate_framework_comparison(self, text: str, frameworks: List[str]) -> SVG
```

**Visualization Types**:
- **Coordinate System**: Interactive elliptical positioning
- **Comparative Analysis**: Multiple texts or frameworks
- **Temporal Analysis**: Evolution over time
- **Framework Overlays**: Same text, different frameworks

#### 4.2.3 Conversation Memory
```python
class ConversationMemory:
    def store_analysis(self, analysis_id: str, result: AnalysisResult)
    def recall_previous_analysis(self, query: str) -> Optional[AnalysisResult]
    def compare_with_previous(self, current: AnalysisResult) -> ComparisonResult
```

**Memory Features**:
- **Analysis History**: "Compare this to the Trump speech we analyzed earlier"
- **Pattern Recognition**: "Show me all speeches with high Megalothymic Thymos"
- **Context Awareness**: "How does this compare to previous Biden analyses?"

### 4.3 Success Criteria
- [ ] URL and file processing works reliably
- [ ] Visualizations embed correctly in chat responses
- [ ] Conversation memory enables comparative analysis
- [ ] Performance acceptable (<30s for complex analyses)
- [ ] Error handling graceful and informative

---

## 5. Phase 3: Research-Grade Features

### 5.1 Duration: 4-5 weeks

### 5.2 Deliverables

#### 5.2.1 Batch Analysis Capabilities
```python
class BatchProcessor:
    def analyze_corpus(self, corpus_name: str, framework: str) -> BatchResult
    def analyze_speaker_evolution(self, speaker: str, timeframe: str) -> TemporalResult
    def framework_sensitivity_analysis(self, text: str) -> SensitivityResult
```

**Batch Features**:
- **Corpus Analysis**: "Analyze all presidential speeches using Fukuyama framework"
- **Speaker Evolution**: "Show how Trump's rhetoric evolved from 2015-2020"
- **Framework Sensitivity**: "How does this text score across all frameworks?"
- **Statistical Summaries**: Means, distributions, correlations

#### 5.2.2 Export and Documentation
```python
class ExportEngine:
    def export_academic_format(self, analyses: List[AnalysisResult]) -> AcademicExport
    def generate_methodology_report(self, experiment: Experiment) -> MethodologyReport
    def create_replication_package(self, study: Study) -> ReplicationPackage
```

**Export Formats**:
- **Academic Papers**: LaTeX tables, formatted results
- **Statistical Scripts**: R/Python code for further analysis
- **Replication Packages**: Data + code + documentation
- **Presentation Formats**: PowerPoint slides, conference posters

#### 5.2.3 Advanced Query Processing
```python
class AdvancedQueryProcessor:
    def handle_complex_queries(self, query: str) -> QueryPlan
    def execute_multi_step_analysis(self, plan: QueryPlan) -> ComplexResult
    def suggest_research_directions(self, context: ResearchContext) -> List[Suggestion]
```

**Advanced Queries**:
- **Research Questions**: "Does populist rhetoric correlate with Megalothymic Thymos?"
- **Hypothesis Testing**: "Test whether democratic leaders score higher on Integrative Recognition"
- **Methodological Guidance**: "What sample size do I need for statistical significance?"

### 5.3 Success Criteria
- [ ] Batch processing handles 100+ texts efficiently
- [ ] Export formats meet academic standards
- [ ] Complex queries execute successfully
- [ ] Statistical analysis integration works
- [ ] Research guidance provides value

---

## 6. Technical Requirements

### 6.1 Performance
- **Response Time**: <2s for simple queries, <30s for complex analysis
- **Throughput**: Handle 10 concurrent users
- **Scalability**: Architecture supports horizontal scaling
- **Reliability**: 99% uptime, graceful error recovery

### 6.2 Security and Privacy
- **API Key Management**: Secure storage and rotation
- **Data Privacy**: No storage of analyzed texts without consent
- **Access Control**: Research group collaboration features
- **Audit Logging**: Complete operation tracking

### 6.3 Integration
- **Existing APIs**: Seamless integration with current FastAPI backend
- **Database**: Use existing PostgreSQL schema
- **Authentication**: JWT token system (existing)
- **Framework System**: Direct integration with framework manager

---

## 7. User Experience Design

### 7.1 Interface Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Narrative Gravity Analysis Assistant                       │
├─────────────────────────────────────────────────────────────┤
│ 🎯 Current Framework: Fukuyama Identity                    │
│ 📊 Last Analysis: Trump 2015 Speech                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ User: Analyze this Biden speech transcript                  │
│                                                             │
│ Bot: I'll analyze this using the Fukuyama Identity         │
│      framework. Here are the results:                      │
│                                                             │
│      [EMBEDDED VISUALIZATION]                               │
│                                                             │
│      Key findings:                                          │
│      • High Creedal Identity (0.85)                       │
│      • Strong Democratic Thymos (0.78)                     │
│      • Low Ethnic Identity (0.12)                         │
│                                                             │
│      Would you like me to compare this to the Trump        │
│      speech we analyzed earlier?                            │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Type your message... [SEND] [📎 Upload] [🔗 URL]          │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Conversation Patterns

#### 7.2.1 Analysis Request
```
User: "Analyze this Trump 2015 campaign announcement"
Bot:  "I'll analyze using the Fukuyama Identity framework..."
      [Results + Visualization]
      "Would you like to try a different framework or compare with other speeches?"
```

#### 7.2.2 Framework Exploration  
```
User: "What does Megalothymic Thymos mean?"
Bot:  "Megalothymic Thymos represents destructive desire for superior recognition..."
      "Here's how it manifests in political rhetoric..."
      "Would you like to see examples from recent analyses?"
```

#### 7.2.3 Comparative Analysis
```
User: "Compare this to the previous Biden speech"
Bot:  "Comparing current analysis to Biden 2020 DNC speech..."
      [Comparative visualization]
      "Key differences: Increased Creedal Identity (+0.15), Similar Democratic Thymos..."
```

---

## 8. Development Timeline

### 8.1 Phase 1: Foundation (Weeks 1-3)
- **Week 1**: Domain constraint engine, basic chat interface
- **Week 2**: Framework integration, simple analysis
- **Week 3**: Testing, refinement, basic visualizations

### 8.2 Phase 2: Enhancement (Weeks 4-7)
- **Week 4**: Multi-input processing (URL, file upload)
- **Week 5**: Advanced visualizations, conversation memory
- **Week 6**: Comparative analysis features
- **Week 7**: Testing, performance optimization

### 8.3 Phase 3: Research Features (Weeks 8-12)
- **Week 8**: Batch processing capabilities
- **Week 9**: Export and documentation features
- **Week 10**: Advanced query processing
- **Week 11**: Statistical integration
- **Week 12**: Final testing, documentation, deployment

---

## 9. Success Metrics

### 9.1 Technical Metrics
- **Domain Constraint Accuracy**: >95%
- **Response Time**: <2s average, <30s maximum
- **Analysis Accuracy**: Match existing engine results
- **System Reliability**: 99% uptime

### 9.2 User Experience Metrics
- **Query Success Rate**: >90% of queries result in useful responses
- **Conversation Flow**: Average 5+ exchanges per session
- **User Satisfaction**: >4.5/5 rating from research users
- **Adoption Rate**: 80% of researchers prefer chatbot to web forms

### 9.3 Research Value Metrics
- **Export Usage**: 70% of analyses exported for further research
- **Comparative Analysis**: 60% of sessions include comparisons
- **Framework Exploration**: Users try multiple frameworks per session
- **Research Output**: Measurable contribution to published research

---

## 10. Risk Assessment and Mitigation

### 10.1 Technical Risks
- **Domain Drift**: Risk of chatbot handling off-topic queries
  - *Mitigation*: Robust testing, continuous monitoring, fallback mechanisms
- **Performance Degradation**: Complex analyses may be slow
  - *Mitigation*: Caching, optimization, progress indicators, async processing
- **Integration Complexity**: Chatbot integration with existing systems
  - *Mitigation*: Incremental development, API-first approach, thorough testing

### 10.2 User Experience Risks
- **Expectation Mismatch**: Users expect general AI capabilities
  - *Mitigation*: Clear domain boundaries, educational onboarding
- **Learning Curve**: Researchers unfamiliar with conversational interfaces
  - *Mitigation*: Guided tutorials, example conversations, fallback to traditional UI

### 10.3 Academic Risks
- **Methodological Concerns**: Questions about AI-mediated analysis
  - *Mitigation*: Transparent methodology, human oversight, validation studies
- **Reproducibility**: Ensuring consistent results across sessions
  - *Mitigation*: Deterministic analysis engine, complete provenance tracking

---

## 11. Future Enhancements

### 11.1 Advanced AI Features
- **Natural Language Framework Creation**: "Create a framework for environmental discourse"
- **Automated Pattern Discovery**: AI identifies recurring themes across corpora
- **Predictive Analysis**: "Predict likely public reaction to this speech"

### 11.2 Collaboration Features
- **Multi-User Sessions**: Research teams working together
- **Annotation Tools**: Collaborative text markup and discussion
- **Version Control**: Track analysis evolution across research projects

### 11.3 Integration Expansions
- **External Corpora**: Integration with academic databases, news archives
- **Real-Time Analysis**: Monitor social media, news feeds for narrative patterns
- **Cross-Linguistic Analysis**: Support for non-English political discourse

---

This specification provides a comprehensive roadmap for building a research-grade chatbot interface that maintains academic rigor while dramatically improving user experience. The phased approach ensures steady progress while allowing for validation and iteration at each stage. 