# Intelligent Corpus Ingestion Service - User Guide

## Overview

The Intelligent Corpus Ingestion Service automatically extracts metadata from messy text files using AI-powered analysis, dramatically reducing the manual effort required to build research-quality document corpora. The service can process directories of poorly-named files with minimal metadata and transform them into academically-structured corpus entries.

### What This Service Does

✅ **Automatic Metadata Extraction**: Extracts titles, authors, dates, document types, and descriptions from text content
✅ **Quality Assessment**: Scores extraction confidence (0-100%) to ensure only high-quality metadata reaches your corpus
✅ **Intelligent Processing**: Uses GPT-3.5-turbo for sophisticated understanding of historical and political documents  
✅ **Corpus Integration**: Automatically registers high-confidence documents in your research corpus with semantic text IDs
✅ **Batch Processing**: Handles entire directories of files with comprehensive reporting and audit trails

### What This Service Does NOT Do

❌ **Perfect Accuracy**: AI extraction may miss nuanced details or make incorrect inferences  
❌ **OCR or PDF Processing**: Only works with plain text files (.txt, .md)
❌ **Language Translation**: Designed primarily for English-language documents
❌ **Content Analysis**: Extracts metadata only, does not perform narrative gravity analysis

## Setting Expectations

### Success Rates
- **High-quality historical documents**: 70-95% success rate
- **Modern documents with clear structure**: 85-100% success rate  
- **Poorly formatted or damaged text**: 30-60% success rate
- **Non-English documents**: 40-70% success rate (depending on language)

### Processing Time
- **Small collection (10-50 files)**: 2-5 minutes
- **Medium collection (100-200 files)**: 10-20 minutes
- **Large collection (500+ files)**: 30-60 minutes
- **Cost**: ~$0.01-0.05 per document for LLM processing

### Quality Levels
- **Successful (≥70% confidence)**: Automatically registered in corpus, ready for analysis
- **Uncertain (40-69% confidence)**: Requires manual review, may need metadata correction
- **Failed (<40% confidence)**: LLM extraction failed, needs manual processing

## Prerequisites

### Required
1. **Narrative Gravity environment set up** with PostgreSQL database
2. **Python virtual environment activated**
3. **Text files** in .txt or .md format (UTF-8 encoding recommended)

### For LLM Version
4. **OpenAI API key** with GPT-3.5-turbo access
5. **API key configured** in environment variable `OPENAI_API_KEY`
6. **Sufficient API credits** (~$0.01-0.05 per document)

### For Demo Version (No API Required)
4. **No additional requirements** - uses rule-based extraction

## Step-by-Step Usage Guide

### Step 1: Prepare Your Environment

```bash
# Navigate to project directory
cd narrative_gravity_analysis

# Activate virtual environment  
source venv/bin/activate

# Set up development environment
source scripts/setup_dev_env.sh

# Verify environment (should show ✅ for all checks)
python3 -c "from src.narrative_gravity.corpus.registry import CorpusRegistry; print('✅ Corpus system ready')"
```

### Step 2: Prepare Your Text Files

**Organize your files:**
```
my_documents/
├── messy_speech_1.txt
├── some_inaugural_address.txt  
├── random_political_text.txt
└── historical_document.txt
```

**File requirements:**
- Plain text files (.txt or .md)
- UTF-8 encoding (or reasonably clean ASCII)
- Minimum 100 characters for meaningful extraction
- Maximum 50,000 characters per file (larger files truncated)

### Step 3: Choose Your Processing Method

#### Option A: LLM-Powered Processing (Recommended)

**Requirements:**
- OpenAI API key configured
- Internet connection
- API credits available

**Command:**
```bash
python3 scripts/intelligent_ingest.py /path/to/your/documents
```

**With options:**
```bash
python3 scripts/intelligent_ingest.py /path/to/your/documents \
    --confidence-threshold 75 \
    --output-dir my_results \
    --verbose
```

#### Option B: Demo Version (No API Required)

**Use when:**
- No OpenAI API key available
- Processing familiar document types (presidentials, inaugurals, etc.)
- Testing the system before committing to API costs

**Command:**
```bash
python3 scripts/demo_intelligent_ingest.py
```

### Step 4: Monitor Processing

**Expected output:**
```
🚀 Starting Intelligent Corpus Ingestion Service...
📁 Source Directory: /path/to/your/documents
🎯 Confidence Threshold: 70.0%

🔍 Found 15 text files to process...
📄 Processing: messy_speech_1.txt
  ✅ Success (85.0%): First Inaugural Address of John F. Kennedy
📄 Processing: some_inaugural_address.txt  
  ⚠️  Uncertain (65.0%): Presidential Address
📄 Processing: random_political_text.txt
  ❌ Failed (25.0%): random_political_text.txt

📊 Ingestion Results:
  ✅ Successful: 12/15
  ⚠️  Uncertain: 2/15  
  ❌ Failed: 1/15
  📈 Success Rate: 80.0%
```

### Step 5: Review Results

**Check the output directory:**
```bash
ls tmp/intelligent_ingestion_TIMESTAMP/
# You'll see:
# - ingestion_results.json (comprehensive results)
# - individual_file_result.json (per-file details)
```

**Review the summary:**
```bash
cat tmp/intelligent_ingestion_TIMESTAMP/ingestion_results.json
```

### Step 6: Handle Uncertain Cases

**For uncertain results (40-69% confidence):**

1. **Review the extracted metadata:**
   ```bash
   # Look at individual result files
   cat tmp/intelligent_ingestion_TIMESTAMP/uncertain_file_result.json
   ```

2. **Common issues and fixes:**
   - **Missing author**: Check if author name is mentioned differently in text
   - **Wrong date**: Look for alternative date formats or historical context
   - **Incorrect document type**: Consider if type classification makes sense
   - **Generic title**: Title might need manual refinement

3. **Manual registration option:**
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
           'date': '1861-03-04',
           'document_type': 'inaugural',
           'description': 'Manually corrected description',
           'source': 'manual_correction'
       }
   )
   "
   ```

### Step 7: Verify Corpus Integration

**Check that successful documents were registered:**
```bash
python3 -c "
from src.narrative_gravity.corpus.discovery import CorpusDiscovery
discovery = CorpusDiscovery()
stats = discovery.get_corpus_statistics()
print(f'📊 Corpus now has {stats.total_documents} documents from {stats.total_authors} authors')

# Search for recently added documents
results = discovery.search('source:intelligent_ingestion', limit=10)
print(f'🆕 {results.total_matches} documents added by intelligent ingestion')
"
```

## Understanding Results

### Confidence Scoring Explained

**Components of confidence score (0-100%):**
- **Title quality (25 points)**: Clear, meaningful title > 5 characters
- **Author identification (20 points)**: Author name successfully extracted  
- **Date validation (20 points)**: Valid date in YYYY-MM-DD format
- **Document type (15 points)**: Specific type identified (not "other")
- **Description quality (10 points)**: Meaningful description > 10 characters
- **Language detection (5 points)**: Language code identified
- **Consistency bonus (5 points)**: Title appears in document text

### Result Categories

#### ✅ Successful (≥70% confidence)
- **Automatically registered** in corpus database
- **Ready for analysis** - no manual intervention needed
- **High-quality metadata** suitable for academic research
- **Semantic text ID** generated (e.g., `lincoln_inaugural_1865`)

#### ⚠️ Uncertain (40-69% confidence)  
- **Manual review recommended** before corpus registration
- **Partial metadata extracted** - some fields may be missing/incorrect
- **Revision suggested** - check extracted data against source document
- **Registration possible** with manual correction

#### ❌ Failed (<40% confidence)
- **Manual processing required** - AI extraction unsuccessful
- **Fallback metadata only** - basic title from filename
- **Not registered** in corpus - needs human intervention
- **Common causes**: Damaged text, unclear structure, non-standard format

### Generated Text IDs

**Format**: `{author_lastname}_{document_type}_{year}`

**Examples:**
- `lincoln_inaugural_1865` (Abraham Lincoln's 1865 inaugural)
- `roosevelt_speech_1941` (Roosevelt speech from 1941)  
- `chavez_address_2006` (Chávez UN address from 2006)
- `unknown_text_20250611` (Fallback when metadata extraction fails)

## Troubleshooting Common Issues

### Processing Issues

#### "❌ Error: Directory not found"
**Cause**: Specified directory doesn't exist
**Solution**: Check path spelling, ensure directory exists
```bash
ls -la /path/to/your/documents  # Verify directory exists
```

#### "⚠️ Warning: OPENAI_API_KEY environment variable not set"
**Cause**: LLM version requires OpenAI API key
**Solutions:**
1. **Set API key**: `export OPENAI_API_KEY=sk-your-key-here`
2. **Use demo version**: Run `python3 scripts/demo_intelligent_ingest.py` instead
3. **Check .env file**: Ensure API key is in `.env` file

#### "💥 Error: Expecting value: line 1 column 1 (char 0)"
**Cause**: LLM returned invalid JSON response
**Solutions:**
1. **Retry processing** - temporary LLM service issue
2. **Check API key validity** - key might be expired/invalid
3. **Check API credits** - account might be out of credits
4. **Use demo version** as fallback

### Quality Issues

#### Low Success Rate (<50%)
**Possible causes:**
- **Poor quality source files**: Damaged, corrupted, or incomplete text
- **Non-English documents**: Service optimized for English
- **Unusual document formats**: Poetry, technical manuals, etc.
- **Very short documents**: <100 characters provide insufficient context

**Solutions:**
1. **Lower confidence threshold**: Use `--confidence-threshold 50`
2. **Manual review**: Check uncertain results for usable metadata
3. **Preprocess files**: Clean up obvious formatting issues
4. **Use domain-specific extraction**: Consider custom prompts for specialized content

#### Incorrect Metadata Extraction
**Common issues:**
- **Wrong author**: Common names confused (e.g., Roosevelt → wrong Roosevelt)
- **Wrong dates**: Historical context misunderstood
- **Generic titles**: AI generated generic description instead of actual title

**Solutions:**
1. **Review uncertain results**: Check 40-69% confidence files manually
2. **Verify against source**: Cross-check extracted metadata with document content  
3. **Manual correction**: Register corrected metadata manually
4. **Filename hints**: Use descriptive filenames to help AI understanding

#### Database/Registration Issues

#### "❌ registration_error: duplicate key value violates unique constraint"
**Cause**: Generated text_id already exists in database
**Solution**: Text ID collision - document may already be registered
```bash
# Check if text_id already exists
python3 -c "
from src.narrative_gravity.corpus.discovery import CorpusDiscovery
discovery = CorpusDiscovery()
results = discovery.search('text_id:lincoln_inaugural_1865')
print(f'Found {results.total_matches} documents with this ID')
"
```

#### Database connection errors
**Cause**: PostgreSQL database not running or misconfigured
**Solution**: Check database status
```bash
python3 check_database.py  # Verify database connectivity
python3 launch.py --setup-db  # Reset database if needed
```

## Advanced Usage

### Custom Confidence Thresholds

**Conservative approach (high quality only):**
```bash
python3 scripts/intelligent_ingest.py /path/to/docs --confidence-threshold 85
```

**Permissive approach (accept more uncertain results):**
```bash
python3 scripts/intelligent_ingest.py /path/to/docs --confidence-threshold 50
```

### Dry Run Mode (Test Without Registration)

**Test processing without database changes:**
```bash
python3 scripts/intelligent_ingest.py /path/to/docs --dry-run --verbose
```

**Benefits:**
- ✅ **Test API connectivity** without committing results
- ✅ **Estimate processing time** and costs
- ✅ **Review extraction quality** before final processing
- ✅ **Debug issues** without database side effects

### Batch Processing Large Collections

**For very large document collections (500+ files):**

1. **Split into batches:**
   ```bash
   # Process in smaller chunks
   for dir in batch_*; do
       python3 scripts/intelligent_ingest.py "$dir" --output-dir "results_$dir"
   done
   ```

2. **Monitor API usage:**
   - Check OpenAI usage dashboard regularly
   - Set up billing alerts to avoid unexpected charges
   - Consider rate limiting for very large batches

3. **Use incremental processing:**
   ```bash
   # Process only new files not already in results
   python3 scripts/intelligent_ingest.py new_documents --output-dir incremental_batch
   ```

### Integration with Existing Workflows

**Export processed results for external analysis:**
```bash
# Export corpus data including intelligent ingestion results
python3 -c "
from src.narrative_gravity.corpus.exporter import CorpusExporter
exporter = CorpusExporter()
exporter.export_csv('intelligent_ingestion_corpus.csv')
"
```

**Filter by ingestion source:**
```bash
# Find all intelligently ingested documents
python3 -c "
from src.narrative_gravity.corpus.discovery import CorpusDiscovery
discovery = CorpusDiscovery()
results = discovery.search('source:intelligent_ingestion OR source:demo_intelligent_ingestion')
print(f'Found {results.total_matches} intelligently ingested documents')
"
```

## Technical Details

### File Processing Pipeline

1. **File Discovery**: Recursive search for .txt and .md files
2. **Content Reading**: UTF-8 text extraction with error handling
3. **Metadata Extraction**: LLM-powered analysis or rule-based fallback
4. **Confidence Assessment**: Multi-factor scoring algorithm
5. **Quality Control**: Validation and consistency checking
6. **Database Integration**: Automatic registration for high-confidence results
7. **Audit Trail**: Complete provenance tracking and result logging

### LLM Integration Details

**Model**: GPT-3.5-turbo (cost-effective, reliable)
**Temperature**: 0.1 (low randomness for consistent extraction)
**Max Tokens**: 500 (sufficient for structured metadata)
**Prompt Engineering**: Specialized prompts for historical/political documents
**Error Handling**: Graceful fallback to rule-based extraction

### Database Schema Integration

**Tables affected:**
- `corpus`: Document registration with semantic text IDs
- `document`: Metadata storage with source tracking
- Maintains full compatibility with existing corpus management system

### Security and Privacy

**Data handling:**
- ✅ **No persistent storage** of document content on external servers
- ✅ **API calls minimal** - only metadata extraction, not full content
- ✅ **Local processing** - all results stored locally
- ✅ **Audit trails** - complete logging of all operations

**API considerations:**
- ⚠️ **Content sent to OpenAI** for metadata extraction
- ⚠️ **Subject to OpenAI terms** of service and data policies
- ⚠️ **Consider privacy** for sensitive historical documents

## Support and Troubleshooting

### Getting Help

1. **Check this guide** - most common issues covered above
2. **Run diagnostics**:
   ```bash
   python3 check_database.py  # Database connectivity
   python3 -c "import openai; print('OpenAI library available')"  # API setup
   ```
3. **Enable verbose output**: Add `--verbose` flag for detailed processing logs
4. **Review result files**: Check JSON output for specific error details

### Reporting Issues

When reporting problems, include:
- ✅ **Complete command used**
- ✅ **Error message or unexpected output**
- ✅ **Sample problematic file** (if not sensitive)
- ✅ **Environment details** (OS, Python version)
- ✅ **Processing statistics** from results summary

### Best Practices

1. **Start small**: Test with 5-10 files before processing large collections
2. **Use dry-run mode**: Always test before committing to database
3. **Monitor API costs**: Track OpenAI usage for budget planning
4. **Backup regularly**: Ensure corpus database backups before large ingestions
5. **Review uncertain results**: Manual review improves overall corpus quality
6. **Document sources**: Keep track of where documents originated for provenance

---

*This guide covers the Intelligent Corpus Ingestion Service as of June 2025. For technical details about the underlying corpus management system, see [Enhanced Corpus Management Guide](ENHANCED_CORPUS_MANAGEMENT_GUIDE.md).* 