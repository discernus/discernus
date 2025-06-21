# Corpus Organization Guide - Smart File Management

## Overview

The Narrative Gravity corpus system helps you manage documents through three organized stages, preventing confusion and ensuring your processed files are never lost or duplicated.

## 🗂️ Three-Stage Organization

### **Stage 1: Discovery Area** (User-Managed)
```
corpus/raw_sources/
├── batch_2025_june/           # Organize however you want
├── presidential_speeches/     # Any structure works
├── new_findings/             # Keep adding files here
└── messy_documents/          # No cleanup required
```

**Purpose**: Your "inbox" for new documents
- ✅ Add files in any organization
- ✅ Rename and reorganize freely
- ✅ No impact on processed documents
- ❌ Don't rely on this for stable references

### **Stage 2: Processed Storage** (System-Managed)
```
corpus/processed/
├── .manifest.json                        # Index of all processed files
├── ab/cd/abcd1234567890.../              # Content-addressable directories
│   ├── lincoln_inaugural_1865.txt        # Stable semantic filename
│   ├── .metadata.json                   # Extracted metadata
│   └── .provenance.json                 # Processing history
└── ef/gh/efgh0987654321.../
    ├── obama_sotu_2012.txt
    ├── .metadata.json
    └── .provenance.json
```

**Purpose**: Permanent, stable storage for processed documents
- ✅ **Never move or edit these files**
- ✅ Content-addressable (prevents duplicates)
- ✅ Database references point here
- ✅ Safe for long-term citations

### **Stage 3: Database Registry**
- Metadata and relationships tracked in PostgreSQL
- References point to stable processed storage
- Academic metadata for citations
- Analysis results and annotations

## 🚀 Recommended Workflow

### **1. Add New Documents**
```bash
# Put new files anywhere in raw_sources
cp ~/Downloads/*.txt corpus/raw_sources/new_batch/

# Or organize by source
mkdir corpus/raw_sources/presidential_library_2025
cp library_docs/*.txt corpus/raw_sources/presidential_library_2025/
```

### **2. Check Status**
```bash
# See what's processed vs what needs processing
python3 scripts/corpus_status.py

# List all processed documents
python3 scripts/corpus_status.py --list-processed

# Get details about a specific document
python3 scripts/corpus_status.py --details lincoln_inaugural_1865
```

### **3. Process New Files**
```bash
# Process everything in raw_sources (skips duplicates automatically)
python3 scripts/intelligent_ingest.py corpus/raw_sources --verbose

# Or process a specific subdirectory
python3 scripts/intelligent_ingest.py corpus/raw_sources/new_batch
```

### **4. Organize Your Discovery Area**
```bash
# After processing, you can safely reorganize raw_sources
mkdir corpus/raw_sources/archive_2025
mv corpus/raw_sources/old_batch corpus/raw_sources/archive_2025/

# Processed files remain safe in corpus/processed/
```

## 🎯 Key Benefits

### **Duplicate Prevention**
- **Content hashing**: Same content = same storage location
- **Automatic detection**: System tells you "already processed as lincoln_inaugural_1865"
- **No wasted processing**: Skip re-analysis of identical content

### **Stable References**
- **Database integrity**: References never break when you reorganize
- **Academic citations**: Stable text_ids for publication references
- **Long-term storage**: Files organized by content, not user preferences

### **Incremental Discovery**
- **Add files anytime**: Drop new documents in raw_sources freely
- **Batch processing**: Process hundreds of files efficiently
- **Progress tracking**: Always know what's been processed

### **User Freedom**
- **Organize raw_sources**: Any structure, rename freely
- **No system impact**: Changes don't affect processed documents
- **Clear separation**: Discovery vs permanent storage

## 📋 Status Commands

### **Overview Status**
```bash
python3 scripts/corpus_status.py
```
**Output:**
```
🗂️  Narrative Gravity Corpus Organization Status
============================================================

📦 PROCESSED STORAGE: corpus/processed
  ✅ Total processed: 15
  📅 Last updated: 2025-06-11T19:45:23
  📄 Recent documents:
     • lincoln_inaugural_1865 (100% confidence, 2025-06-11)
     • obama_sotu_2012 (95% confidence, 2025-06-11)

📁 DISCOVERY AREA: corpus/raw_sources
  📝 Total text files: 23

📊 PROCESSING STATUS:
  🆕 Unprocessed files: 8
  🔄 Already processed: 15

🆕 NEEDS PROCESSING:
     • new_batch/speech_001.txt (4,523 bytes)
     • presidential_docs/state_union_2024.txt (12,045 bytes)

💡 RECOMMENDATIONS:
  🚀 Process new files:
     python3 scripts/intelligent_ingest.py corpus/raw_sources --verbose
```

### **List Processed Files**
```bash
python3 scripts/corpus_status.py --list-processed
```

### **File Details**
```bash
python3 scripts/corpus_status.py --details lincoln_inaugural_1865
```

## ⚠️ Important Guidelines

### **DO NOT Touch Processed Storage**
- ❌ **Never edit files in `corpus/processed/`**
- ❌ **Never move or rename processed files**
- ❌ **Never delete from processed storage**
- ✅ **Use corpus management tools only**

### **Discovery Area Freedom**
- ✅ **Reorganize `corpus/raw_sources/` freely**
- ✅ **Create any subdirectory structure**
- ✅ **Rename files before processing**
- ✅ **Archive old batches after processing**

### **Processing Guidelines**
- ✅ **Always check status before processing**
- ✅ **Use `--dry-run` to test first**
- ✅ **Review uncertain results manually**
- ✅ **Keep temporary processing results for debugging**

## 🔧 Advanced Usage

### **Content Hash Verification**
```bash
# Check integrity of processed storage
python3 -c "
from src.narrative_gravity.corpus.registry import CorpusRegistry
registry = CorpusRegistry()
integrity = registry.validate_integrity()
print(f'Valid: {len(integrity[\"valid\"])}')
print(f'Issues: {len(integrity[\"hash_mismatches\"])}')
"
```

### **Batch Organization**
```bash
# Organize raw_sources by date
mkdir corpus/raw_sources/batch_$(date +%Y_%m_%d)
mv corpus/raw_sources/*.txt corpus/raw_sources/batch_$(date +%Y_%m_%d)/

# Process specific batch
python3 scripts/intelligent_ingest.py corpus/raw_sources/batch_2025_06_11
```

### **Export from Processed Storage**
```bash
# Export corpus for analysis (references processed storage)
python3 -c "
from src.narrative_gravity.corpus.exporter import CorpusExporter
exporter = CorpusExporter()
exporter.export_csv('my_corpus.csv')
"
```

## 🏗️ Directory Structure Example

```
narrative_gravity_analysis/
├── corpus/
│   ├── raw_sources/              # 🗂️ DISCOVERY AREA (yours to organize)
│   │   ├── archive_2025/
│   │   ├── new_batch_june/
│   │   └── presidential_stuff/
│   └── processed/                # 🔒 PROCESSED STORAGE (system managed)
│       ├── .manifest.json
│       ├── ab/cd/abcd1234.../
│       │   ├── lincoln_inaugural_1865.txt
│       │   ├── .metadata.json
│       │   └── .provenance.json
│       └── ef/gh/efgh5678.../
├── tmp/                          # 🚧 TEMPORARY (processing workspace)
│   └── intelligent_ingestion_*/
└── scripts/
    ├── corpus_status.py          # 📊 Your status dashboard
    └── intelligent_ingest.py     # 🚀 Processing engine
```

This organization ensures your corpus grows systematically while maintaining full academic integrity for long-term research projects. 