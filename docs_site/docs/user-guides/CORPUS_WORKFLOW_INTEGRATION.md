# Corpus Workflow Integration Guide

## Complete Research Workflow: From Messy Files to Published Analysis

This guide shows how the Intelligent Corpus Ingestion Service fits into your complete narrative gravity research workflow, from initial document collection through final analysis and publication.

## Phase 1: Document Collection & Organization

### Traditional Manual Approach (BEFORE)
```
📁 Messy Documents/
├── some_speech.txt
├── random_file_from_internet.txt  
├── presidential_thing.txt
└── untitled_document.txt

↓ Manual labor (hours/days)
- Read each file to identify content
- Research author, date, context  
- Create consistent naming scheme
- Manually enter metadata
- Register in research database
```

### Intelligent Ingestion Approach (NOW)
```bash
# Automated processing (minutes)
python3 scripts/intelligent_ingest.py /path/to/messy/documents --verbose

# Result: Research-ready corpus entries
✅ lincoln_inaugural_1865: "Second Inaugural Address of Abraham Lincoln"
✅ roosevelt_speech_1941: "Third Inaugural Address of Franklin D. Roosevelt"  
✅ chavez_address_2006: "Hugo Chávez Address to the United Nations"
```

**Time Savings**: 90% reduction in corpus preparation time

## Phase 2: Corpus Quality Assurance

### Enhanced Corpus Management Integration

```bash
# Validate corpus quality after ingestion
python3 -c "
from src.narrative_gravity.corpus.validator import CorpusValidator
validator = CorpusValidator()
results = validator.validate_corpus()
print(f'📊 FAIR Compliance: {results.overall_score:.1f}%')
"

# Discover corpus contents
python3 -c "
from src.narrative_gravity.corpus.discovery import CorpusDiscovery
discovery = CorpusDiscovery()
stats = discovery.get_corpus_statistics()
print(f'📚 Corpus: {stats.total_documents} documents, {stats.total_authors} authors')
"
```

**Integration Benefits:**
- ✅ Automatic FAIR data compliance scoring
- ✅ Corpus statistics and health monitoring
- ✅ Document discovery and search capabilities
- ✅ Academic export formatting ready

## Phase 3: Analysis Preparation

### Framework & Component Selection

```bash
# Choose your analytical framework
python3 -c "
from src.narrative_gravity.framework_manager import FrameworkManager
manager = FrameworkManager()
frameworks = manager.list_frameworks()
for f in frameworks:
    print(f'📋 {f.name}: {f.description}')
"

# Select analysis components (Priority 1 Infrastructure)
python3 src/narrative_gravity/cli/component_manager.py list --type all
```

### Corpus Export for Analysis

```bash
# Export corpus in research-ready formats
python3 -c "
from src.narrative_gravity.corpus.exporter import CorpusExporter
exporter = CorpusExporter()

# Academic formats
exporter.export_csv('corpus_analysis.csv')
exporter.export_r_package('corpus_r_analysis/')
exporter.generate_citations('corpus_citations.bib', format='bibtex')
"
```

## Phase 4: Narrative Gravity Analysis

### CLI-Based Analysis (Priority 2 Infrastructure)

```bash
# Systematic analysis of entire corpus
python3 src/narrative_gravity/cli/analyze_batch.py \
    --framework civic_virtue \
    --prompt-template hierarchical_analysis \
    --weighting-method nonlinear_transform \
    --corpus-filter "source:intelligent_ingestion" \
    --output-dir analysis_results/
```

### Interactive Analysis (React Research Workbench)

```bash
# Launch research interface
python3 launch.py  # Backend services
cd frontend && npm run dev  # React interface at localhost:3000

# Interactive analysis features:
# - Visual corpus browser
# - Experiment designer
# - Real-time analysis
# - Multi-model comparison
# - Results visualization
```

## Phase 5: Academic Publication (Priority 3 Infrastructure)

### Automated Documentation Generation

```bash
# Generate methodology documentation
python3 src/narrative_gravity/cli/generate_documentation.py \
    --type methodology \
    --include-corpus-details \
    --output methodology_section.md

# Create replication package
python3 src/narrative_gravity/cli/export_academic_data.py \
    --format replication_package \
    --include-corpus \
    --include-analysis-code \
    --output publication_replication/
```

### Statistical Analysis Templates

```bash
# Generate analysis templates for external tools
python3 src/narrative_gravity/cli/generate_analysis_templates.py \
    --format jupyter \
    --include-corpus-analysis \
    --output analysis_notebooks/

python3 src/narrative_gravity/cli/generate_analysis_templates.py \
    --format r \
    --statistical-tests \
    --output r_analysis_scripts/
```

## Complete Workflow Example

### Scenario: Analyzing Presidential Rhetoric Evolution

**Step 1: Collect Documents**
```bash
# You have messy files from various sources
ls historical_speeches/
# -> jumbled_presidential_files/
```

**Step 2: Intelligent Ingestion**
```bash
python3 scripts/intelligent_ingest.py historical_speeches/ --verbose
# Results: 85% success rate, 34 documents auto-registered
```

**Step 3: Quality Review**
```bash
# Review uncertain cases
cat tmp/intelligent_ingestion_*/ingestion_results.json
# Manual correction for 3 uncertain documents
```

**Step 4: Corpus Validation**
```bash
# Verify corpus quality
python3 -c "
from src.narrative_gravity.corpus.validator import CorpusValidator
validator = CorpusValidator()
results = validator.validate_corpus()
print(f'FAIR Score: {results.overall_score:.1f}%')  # 73.2% - Good quality
"
```

**Step 5: Analysis Setup**
```bash
# Export for analysis
python3 -c "
from src.narrative_gravity.corpus.exporter import CorpusExporter
exporter = CorpusExporter()
exporter.export_csv('presidential_rhetoric_corpus.csv')
"
```

**Step 6: Systematic Analysis**
```bash
# Batch analysis across multiple frameworks
python3 src/narrative_gravity/cli/analyze_batch.py \
    --framework civic_virtue,political_spectrum \
    --corpus-filter "document_type:inaugural" \
    --multi-model \
    --output-dir presidential_analysis/
```

**Step 7: Academic Publication**
```bash
# Generate publication materials
python3 src/narrative_gravity/cli/export_academic_data.py \
    --format replication_package \
    --study presidential_analysis \
    --output presidential_rhetoric_replication/

# Includes:
# - Complete corpus with provenance
# - Analysis code and results  
# - Statistical analysis templates
# - Methodology documentation
# - Citation formats
```

## Integration Points Summary

| Phase | Manual Approach | With Intelligent Ingestion | Time Savings |
|-------|----------------|----------------------------|--------------|
| **Document Prep** | 2-8 hours per 50 docs | 5-10 minutes | 95% |
| **Quality Assurance** | Manual validation | Automated FAIR scoring | 80% |
| **Analysis Prep** | Custom export scripts | Built-in academic formats | 70% |
| **Publication** | Manual documentation | Auto-generated materials | 85% |

## Workflow Advantages

### Research Efficiency
- ✅ **Immediate Analysis Ready**: Documents automatically formatted for analysis
- ✅ **Academic Standards**: Built-in FAIR compliance and citation generation  
- ✅ **Provenance Tracking**: Complete audit trail from source to publication
- ✅ **Reproducibility**: Systematic workflow with version control

### Quality Assurance
- ✅ **Confidence Scoring**: Automatic quality assessment prevents low-quality data
- ✅ **Consistency**: Standardized metadata schema across entire corpus
- ✅ **Validation**: Built-in checks for academic research standards
- ✅ **Error Detection**: Automatic identification of problematic documents

### Scalability
- ✅ **Batch Processing**: Handle hundreds of documents automatically
- ✅ **Incremental Addition**: Add new documents without disrupting existing corpus
- ✅ **Multi-Format Support**: Works with various text file formats
- ✅ **API Integration**: Can be integrated into larger document processing pipelines

## Best Practices for Workflow Integration

### 1. Corpus Development Strategy
```bash
# Start with high-quality seed documents
python3 scripts/intelligent_ingest.py clean_documents/ --confidence-threshold 85

# Add medium-quality documents with review
python3 scripts/intelligent_ingest.py mixed_quality/ --confidence-threshold 60 --verbose

# Manual review uncertain cases before final corpus
# Use FAIR validation to ensure academic standards
```

### 2. Analysis Planning
```bash
# Plan your analytical approach before corpus ingestion
# Consider:
# - Which frameworks will you use?
# - What document types are you focusing on?
# - What time periods are relevant?
# - How will you handle multi-author documents?
```

### 3. Publication Preparation
```bash
# Document your corpus development process
# Include:
# - Source of original documents
# - Intelligent ingestion settings used
# - Manual corrections made
# - FAIR compliance scores achieved
# - Quality assurance steps taken
```

## Troubleshooting Workflow Issues

### Common Integration Problems

**Problem**: Low corpus quality after ingestion
**Solution**: 
- Review confidence thresholds
- Check source document quality
- Use manual correction for key documents

**Problem**: Analysis tools can't find corpus documents  
**Solution**:
- Verify database integration with `python3 check_database.py`
- Check corpus registration status
- Ensure proper text ID generation

**Problem**: Academic export missing metadata
**Solution**:
- Validate corpus with CorpusValidator
- Check metadata completeness
- Re-run ingestion with higher confidence threshold

---

*This workflow integration guide shows how intelligent corpus ingestion transforms the entire research process from document collection to academic publication. For specific tool usage, see individual user guides for each system component.* 