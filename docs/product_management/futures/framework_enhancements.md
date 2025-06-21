# Framework Enhancement Ideas

Ideas for future framework system enhancements that maintain clean architectural separation.

## Framework-Defined Document Types

**Concept**: Allow frameworks to define domain-specific document types as part of their theoretical structure.

**Current Issue**: Corpus management system currently has hardcoded political speech document types:
```python
# These are framework-specific, not corpus-generic
'inaugural', 'sotu', 'speech', 'statement', 'address', 
'debate', 'interview', 'press_conference', 'campaign'
```

**Proposed Architecture**:
- **Corpus System**: Framework-agnostic with generic types ('text', 'document', 'media')
- **Framework Definition**: Each framework can specify relevant document types
- **Validation Integration**: Corpus validator can optionally use framework-specific types when a framework context is available

**Example Framework Extension**:
```yaml
# frameworks/civic_virtue/v2.1.0/config.yaml
framework:
  name: "civic_virtue"
  version: "2.1.0"
  document_types:
    primary: ["inaugural", "sotu", "campaign_speech"]
    secondary: ["debate", "interview", "statement"] 
    applicable: ["address", "press_conference"]
    excluded: ["private_correspondence", "personal_diary"]
```

**Benefits**:
- Clean separation: corpus management remains domain-agnostic
- Framework specificity: political frameworks can specify political document types
- Future flexibility: other frameworks (literary analysis, corporate communications) can define their own relevant types
- Validation context: can validate document appropriateness for specific analytical frameworks

**Implementation Considerations**:
- Framework loading: document types loaded with framework configuration
- Corpus integration: optional framework context in corpus validation
- Cross-framework studies: handling documents that span multiple framework domains
- Migration: existing documents with framework-specific types need graceful handling

## Corpus Management Future Features

### Stable URI Web Service
**Concept**: Implement actual web service to resolve stable document URIs for academic citations.

**Current Status**: URI generation creates placeholder URIs (`placeholder://corpus/{text_id}`) but no web service exists
**Required Infrastructure**:
- Web service at `https://narrative-gravity.org/corpus/` (or chosen domain)
- Document resolution endpoints `/document/{text_id}`
- Content negotiation (HTML for humans, JSON-LD for machines)
- Persistent identifier registration (DOI integration?)
- Content delivery with proper academic metadata headers

**Implementation Phases**:
1. **Domain & Hosting**: Acquire domain, set up web hosting infrastructure
2. **Basic Resolution**: Simple HTTP service resolving text_ids to document metadata
3. **Rich Metadata**: Dublin Core, JSON-LD, Schema.org structured data
4. **Content Delivery**: Serve actual document content with appropriate licensing
5. **Academic Integration**: DOI registration, library system integration

**Benefits**:
- True FAIR compliance with persistent, resolvable identifiers
- Academic citation support with clickable references
- Integration with digital humanities infrastructure
- Discovery through web search and academic databases

## Other Framework Enhancement Ideas

### Framework Metadata Standards
- Author/institution attribution for frameworks
- Version lifecycle management (alpha → beta → stable → deprecated)
- Citation requirements for academic frameworks
- License and usage restrictions

### Framework Composition
- Ability to combine frameworks for multi-dimensional analysis
- Framework inheritance (specialized frameworks extending base frameworks)
- Cross-framework compatibility matrices

### Framework Performance Analytics
- Usage statistics and performance metrics per framework
- Success/failure rates across different document types
- Framework effectiveness scoring based on analysis outcomes

### Framework Validation Tools
- Automated consistency checking for framework definitions
- Theoretical coherence validation
- Empirical validation support tools

---

*Document created: June 11, 2025*
*Purpose: Architectural planning for future framework system enhancements* 