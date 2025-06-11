# Intelligent Corpus Ingestion - Quick Start Guide

## TL;DR: Convert Messy Text Files to Research Corpus

```bash
# Set up environment
source venv/bin/activate && source scripts/setup_dev_env.sh

# Process your files (LLM version - requires OpenAI API key)
python3 scripts/intelligent_ingest.py /path/to/your/documents --verbose

# OR demo version (no API key needed)
python3 scripts/demo_intelligent_ingest.py

# Check results
cat tmp/intelligent_ingestion_*/ingestion_results.json
```

## What You Get

**Input**: Messy files like `random_speech.txt`, `inaugural_something.txt`
**Output**: Research-ready corpus entries with metadata:
- `lincoln_inaugural_1865` with title, author, date, type, description
- Automatically registered in your research database
- Ready for narrative gravity analysis

## Success Expectations

| File Quality | Success Rate | Example |
|--------------|--------------|---------|
| 📄 Clean historical docs | 85-100% | Presidential speeches, famous addresses |
| 📄 Moderate quality | 60-85% | OCR'd documents, informal texts |
| 📄 Poor/damaged | 30-60% | Corrupted files, fragments |

## Essential Commands

### Basic Processing
```bash
# Process directory with defaults (70% confidence threshold)
python3 scripts/intelligent_ingest.py /path/to/documents

# High-quality only (85% threshold)  
python3 scripts/intelligent_ingest.py /path/to/documents --confidence-threshold 85

# Test without database changes
python3 scripts/intelligent_ingest.py /path/to/documents --dry-run --verbose
```

### Demo Version (No API Key)
```bash
# Rule-based extraction for common document types
python3 scripts/demo_intelligent_ingest.py
```

### Check Results
```bash
# View processing summary
cat tmp/intelligent_ingestion_*/ingestion_results.json

# Check what was added to corpus
python3 -c "
from src.narrative_gravity.corpus.discovery import CorpusDiscovery
discovery = CorpusDiscovery()
results = discovery.search('source:intelligent_ingestion')
print(f'Added {results.total_matches} documents to corpus')
"
```

## Confidence Levels

| Level | Score | What Happens | Action Needed |
|-------|-------|--------------|---------------|
| ✅ **Successful** | ≥70% | Auto-registered in corpus | ✅ Ready for analysis |
| ⚠️ **Uncertain** | 40-69% | Saved but not registered | 📝 Review & manually register |
| ❌ **Failed** | <40% | Basic fallback metadata | 🔧 Manual processing required |

## Common Issues & Quick Fixes

### "OpenAI API key not set"
```bash
# Set API key
export OPENAI_API_KEY=sk-your-key-here

# OR use demo version instead
python3 scripts/demo_intelligent_ingest.py
```

### Low success rate
```bash
# Lower confidence threshold
python3 scripts/intelligent_ingest.py /path/to/docs --confidence-threshold 50

# Check uncertain results for manual processing
cat tmp/intelligent_ingestion_*/uncertain_file_result.json
```

### Database connection errors
```bash
# Check database status
python3 check_database.py

# Fix if needed
python3 launch.py --setup-db
```

## Manual Correction for Uncertain Results

```bash
# Register manually with corrected metadata
python3 -c "
from src.narrative_gravity.corpus.registry import CorpusRegistry
registry = CorpusRegistry()
registry.register_document(
    text_id='corrected_author_type_year',
    file_path='/path/to/file.txt',
    metadata={
        'title': 'Corrected Title',
        'author': 'Corrected Author', 
        'date': 'YYYY-MM-DD',
        'document_type': 'speech|inaugural|address|letter',
        'description': 'Brief description',
        'source': 'manual_correction'
    }
)
"
```

## File Requirements

✅ **Supported**: .txt, .md files in UTF-8 encoding
✅ **Size**: 100-50,000 characters per file  
✅ **Content**: English text with clear structure
❌ **Not supported**: PDFs, images, binary files, non-text content

## Cost Estimates (LLM Version)

- **Small batch (10-20 files)**: ~$0.10-0.50
- **Medium batch (50-100 files)**: ~$0.50-2.00  
- **Large batch (200+ files)**: ~$2.00-10.00

*Prices based on GPT-3.5-turbo rates as of June 2025*

## Text ID Format

Generated automatically: `{author_lastname}_{document_type}_{year}`

**Examples:**
- `lincoln_inaugural_1865`
- `churchill_speech_1940`
- `mandela_address_1994`

## Next Steps After Processing

```bash
# Export your corpus for analysis
python3 -c "
from src.narrative_gravity.corpus.exporter import CorpusExporter
exporter = CorpusExporter()
exporter.export_csv('my_corpus.csv')
"

# Analyze with narrative gravity
# (Use your corpus documents with existing analysis tools)
```

---

**Need more details?** See the complete [Intelligent Corpus Ingestion Guide](INTELLIGENT_CORPUS_INGESTION_GUIDE.md) for troubleshooting, advanced usage, and technical details.

**Questions?** Check the troubleshooting section or run with `--verbose` flag for detailed processing logs. 