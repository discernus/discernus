# Evidence Matching Wrapper Specification
## Framework-Agnostic txtai Integration for Evidence Retrieval Infrastructure

**Project**: Evidence Matching Wrapper  
**Status**: Specification Phase  
**Priority**: High - Critical for synthesis agent functionality  
**Created**: 2025-01-27  
**Architect Review**: Pending  

---

## 1. Executive Summary

### Problem Statement
The current synthesis agent cannot effectively retrieve evidence that supports statistical findings from any analytical framework. The existing txtai integration is too generic and lacks the ability to translate statistical findings into evidence queries within the context of different frameworks.

### Solution Overview
Create a framework-agnostic wrapper around txtai that can retrieve supporting evidence quotes for any statistical finding in any analytical framework. This wrapper will bridge the gap between abstract statistical results and concrete textual evidence, enabling evidence-based synthesis reports across all research domains.

### Key Benefits
- **Framework Agnostic**: Works with any analytical framework (CAF, moral foundations, populism studies, etc.)
- **Semantic Matching**: Finds evidence that exemplifies concepts, not just contains keywords
- **Contextual Intelligence**: Uses framework context to generate relevant evidence queries
- **Cursor Agent Friendly**: Simple interface that Cursor agents can implement successfully
- **Durable Infrastructure**: Reusable across all experiments without framework-specific modifications

---

## 2. Current State Analysis

### Existing txtai Integration Issues
1. **Generic Interface**: Current txtai wrapper provides basic search without framework context
2. **Query Generation Gap**: No mechanism to translate statistical findings into evidence queries
3. **Evidence Mismatch**: Retrieved evidence often doesn't support the statistical narrative
4. **Integration Complexity**: Cursor agents struggle with the current txtai implementation
5. **Framework Coupling**: Current approaches are tied to specific frameworks, violating experiment agnosticism

### What's Working
- Evidence extraction during analysis phase
- txtai indexing and basic search functionality
- Evidence storage with metadata (dimension, confidence, document_name)

### What's Broken
- Synthesis agent cannot find relevant evidence for statistical findings
- No intelligent query generation based on framework context
- Evidence retrieval is keyword-based rather than concept-based
- Framework-specific hardcoding prevents reuse across different experiments

---

## 3. Technical Specification

### 3.1 Core Architecture

```python
class EvidenceMatchingWrapper:
    """
    Framework-agnostic wrapper for matching evidence quotes to statistical findings.
    
    This wrapper provides intelligent evidence retrieval that works with any analytical
    framework, maintaining experiment agnosticism while enabling evidence-based synthesis.
    """
    
    def __init__(self, model: str, artifact_storage: LocalArtifactStorage):
        self.model = model
        self.artifact_storage = artifact_storage
        self.llm_gateway = LLMGateway(ModelRegistry())
        self.index = None
        self.evidence_data = []
```

### 3.2 Core Methods

#### Evidence Index Building
```python
def build_index(self, evidence_artifact_hashes: List[str]) -> bool:
    """
    Build txtai index from evidence artifacts with CAF metadata preservation.
    
    Args:
        evidence_artifact_hashes: List of evidence artifact hashes
        
    Returns:
        True if index built successfully, False otherwise
    """
```

#### Framework-Agnostic Evidence Retrieval
```python
def find_supporting_evidence(
    self,
    statistical_finding: str,
    framework_context: str,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Find evidence that supports any statistical finding within any framework context.
    
    Args:
        statistical_finding: Description of the statistical finding
        framework_context: Framework description for context
        limit: Maximum number of evidence pieces to return
        
    Returns:
        List of evidence dictionaries with relevance scores
    """
```

#### Generic Evidence Search
```python
def search_evidence(
    self,
    query: str,
    filters: Optional[Dict[str, Any]] = None,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Generic evidence search with optional filtering.
    
    Args:
        query: Search query string
        filters: Optional metadata filters (dimension, confidence, document_name)
        limit: Maximum number of evidence pieces to return
        
    Returns:
        List of evidence dictionaries matching the query and filters
    """
```

#### Evidence by Metadata
```python
def get_evidence_by_metadata(
    self,
    metadata_filters: Dict[str, Any],
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Retrieve evidence based on metadata filters without semantic search.
    
    Args:
        metadata_filters: Dictionary of metadata filters to apply
        limit: Maximum number of evidence pieces to return
        
    Returns:
        List of evidence dictionaries matching the metadata filters
    """
```

#### Intelligent Evidence Matching
```python
def find_supporting_evidence(
    self,
    statistical_finding: str,
    framework_context: str,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Find evidence that directly supports a statistical finding using LLM intelligence.
    
    Args:
        statistical_finding: Description of the statistical finding
        framework_context: Framework description for context
        limit: Maximum number of evidence pieces to return
        
    Returns:
        List of evidence dictionaries ranked by relevance to the finding
    """
```

### 3.3 LLM Integration for Query Generation

```python
def _generate_evidence_query(
    self,
    finding: str,
    framework_context: str
) -> str:
    """
    Use LLM to generate intelligent evidence queries.
    
    This is the core intelligence that translates statistical findings
    into evidence search queries within any framework context.
    """
    
    prompt = f"""
    You are an expert in computational social science evidence retrieval.
    
    STATISTICAL FINDING: {finding}
    FRAMEWORK CONTEXT: {framework_context}
    
    TASK: Generate a search query that would find evidence supporting this finding.
    
    REQUIREMENTS:
    1. Focus on what the evidence should demonstrate, not just keywords
    2. Consider the conceptual relationship within the framework context
    3. Generate a query that would find semantically relevant evidence
    4. Keep the query concise but specific
    5. Make the query framework-agnostic and reusable
    
    EXAMPLE:
    Finding: "Strong negative correlation between dignity and tribalism (r = -0.81)"
    Framework: "Civic Analysis Framework analyzing political discourse"
    Query: "evidence showing opposition between dignity and tribalism in political discourse"
    
    YOUR QUERY:
    """
    
    response = self.llm_gateway.execute_call(
        model=self.model,
        prompt=prompt,
        max_tokens=100
    )
    
    return response.choices[0].message.content.strip()
```

### 3.4 Evidence Ranking and Filtering

```python
def _rank_evidence_by_relevance(
    self,
    evidence_results: List[Dict[str, Any]],
    statistical_context: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Rank evidence by relevance to the statistical finding.
    
    Uses multiple factors:
    - Semantic similarity score from txtai
    - Confidence score from analysis
    - Dimensional alignment
    - Contextual fit
    """
```

---

## 4. Implementation Phases

### Phase 1: Foundation (Week 1-2)
**Goal**: Basic wrapper with txtai integration

#### Deliverables
- [ ] `EvidenceMatchingWrapper` class with basic txtai integration
- [ ] Evidence index building from artifacts
- [ ] Basic search functionality
- [ ] Unit tests for core functionality

#### Success Criteria
- Wrapper can build index from evidence artifacts
- Basic search returns evidence with metadata
- All unit tests pass

### Phase 2: Framework Intelligence (Week 3-4)
**Goal**: Add framework-agnostic evidence matching methods

#### Deliverables
- [ ] `find_supporting_evidence()` method with framework context
- [ ] `search_evidence()` method with filtering
- [ ] `get_evidence_by_metadata()` method
- [ ] Integration tests with real experiment data

#### Success Criteria
- Methods can find evidence for any statistical finding
- Methods work with different analytical frameworks
- Methods can filter evidence by metadata
- Integration tests pass with sample experiments

### Phase 3: LLM Query Generation (Week 5-6)
**Goal**: Intelligent query generation using LLM

#### Deliverables
- [ ] `_generate_evidence_query()` method
- [ ] `find_supporting_evidence()` method
- [ ] LLM integration for query generation
- [ ] Query quality validation

#### Success Criteria
- LLM generates contextually appropriate queries
- Generated queries find relevant evidence
- Query quality meets minimum relevance thresholds

### Phase 4: Integration and Testing (Week 7-8)
**Goal**: Full integration with synthesis pipeline

#### Deliverables
- [ ] Integration with synthesis agent
- [ ] End-to-end testing with real experiments
- [ ] Performance optimization
- [ ] Documentation and examples

#### Success Criteria
- Synthesis agent can retrieve relevant evidence
- Evidence supports statistical narratives
- Performance meets scalability requirements (1000+ documents)
- Cursor agents can successfully implement the wrapper

---

## 5. Technical Requirements

### 5.1 Dependencies
- `txtai` for vector search and indexing
- `discernus.gateway.llm_gateway` for LLM integration
- `discernus.core.local_artifact_storage` for evidence access
- `discernus.core.audit_logger` for operation tracking

### 5.2 Performance Requirements
- **Index Building**: < 30 seconds for 1000 evidence pieces
- **Search Response**: < 2 seconds for typical queries
- **Memory Usage**: < 500MB for 1000 evidence pieces
- **Scalability**: Support up to 10,000 evidence pieces

### 5.3 Error Handling
- Graceful degradation when txtai operations fail
- Fallback to basic search when LLM query generation fails
- Comprehensive logging for debugging
- User-friendly error messages for Cursor agents

---

## 6. Testing Strategy

### 6.1 Unit Testing
- Test each method in isolation with mock data
- Test error conditions and edge cases
- Test evidence ranking and filtering logic
- Test LLM query generation with various finding types

### 6.2 Integration Testing
- Test with real evidence artifacts from CAF experiments
- Test evidence retrieval for actual statistical findings
- Test performance with varying evidence corpus sizes
- Test integration with synthesis agent

### 6.3 Validation Testing
- Validate that retrieved evidence actually supports findings
- Validate query generation quality and relevance
- Validate performance under load
- Validate error handling and recovery

---

## 7. Success Metrics

### 7.1 Functional Metrics
- **Evidence Relevance**: >80% of retrieved evidence supports the statistical finding
- **Query Quality**: >90% of generated queries find relevant evidence
- **Framework Coverage**: >95% of statistical findings can find supporting evidence across all frameworks
- **Reusability**: 100% of methods work with any analytical framework without modification

### 7.2 Performance Metrics
- **Response Time**: <2 seconds for evidence retrieval
- **Scalability**: Support 1000+ documents without degradation
- **Memory Efficiency**: <500MB memory usage for large corpora

### 7.3 Usability Metrics
- **Cursor Agent Success**: >90% of Cursor agents can implement successfully
- **Integration Time**: <1 day to integrate with synthesis pipeline
- **Error Rate**: <5% of operations result in errors

---

## 8. Risk Assessment

### 8.1 Technical Risks
- **txtai Integration Complexity**: Risk that txtai remains difficult to work with
- **LLM Query Quality**: Risk that generated queries are not effective
- **Performance Degradation**: Risk that wrapper adds significant overhead

### 8.2 Mitigation Strategies
- **Incremental Development**: Build and test each phase before proceeding
- **Fallback Mechanisms**: Provide simple search when complex methods fail
- **Performance Monitoring**: Continuous performance testing throughout development
- **Extensive Testing**: Comprehensive testing with real CAF data

---

## 9. Future Enhancements

### 9.1 Advanced Features
- **Evidence Synthesis**: Automatically combine multiple evidence pieces
- **Pattern Recognition**: Identify evidence patterns across multiple findings
- **Confidence Scoring**: Provide confidence scores for evidence relevance
- **Caching**: Intelligent caching of frequently accessed evidence

### 9.2 Integration Opportunities
- **Framework Validation**: Use evidence to validate CAF framework assumptions
- **Corpus Analysis**: Analyze evidence patterns across different corpora
- **Comparative Studies**: Compare evidence patterns across different frameworks

---

## 10. Conclusion

The Evidence Matching Wrapper addresses a critical gap in the evidence retrieval infrastructure by providing framework-agnostic intelligence for evidence matching. This wrapper will enable synthesis agents to find relevant evidence that supports statistical findings across any analytical framework, leading to more compelling and evidence-based research reports.

The phased implementation approach ensures that each component is thoroughly tested before proceeding, reducing risk and ensuring successful integration. The wrapper's framework-agnostic design makes it accessible to Cursor agents while providing the sophisticated functionality needed for evidence-based synthesis across all research domains.

The wrapper maintains the project's commitment to experiment agnosticism and durable infrastructure, ensuring it can be reused across different frameworks without modification.

**Next Steps**: Architect review and approval, followed by Phase 1 implementation with comprehensive testing.

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-27  
**Review Status**: Pending Architect Review  
**Implementation Status**: Not Started
