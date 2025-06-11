# User Guides - Narrative Gravity Corpus Management

## 🤖 Intelligent Corpus Ingestion Service

Transform messy text files and YouTube videos into research-ready corpus entries using AI-powered metadata extraction.

### 📚 Documentation Index

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[Quick Start Guide](INTELLIGENT_INGESTION_QUICKSTART.md)** | Essential commands & workflows | ⚡ **Start here** - get running in 5 minutes |
| **[Complete User Guide](INTELLIGENT_CORPUS_INGESTION_GUIDE.md)** | Comprehensive documentation | 📖 Detailed setup, troubleshooting, advanced usage |
| **[YouTube Quick Start](YOUTUBE_INGESTION_QUICKSTART.md)** | YouTube transcript extraction | 📺 Extract political speeches from YouTube |
| **[YouTube Complete Guide](YOUTUBE_TRANSCRIPT_INGESTION_GUIDE.md)** | Comprehensive YouTube docs | 🎬 Advanced YouTube processing & troubleshooting |
| **[Workflow Integration Guide](CORPUS_WORKFLOW_INTEGRATION.md)** | Research workflow context | 🔗 Understand how this fits your research process |

## Quick Start: 3 Steps to Success

### 1. Environment Setup
```bash
source venv/bin/activate && source scripts/setup_dev_env.sh

# For YouTube processing, also install dependencies
pip install youtube-transcript-api yt-dlp
```

### 2. Process Your Content

#### Text Files
```bash
# LLM-powered (requires OpenAI API key)
python3 scripts/intelligent_ingest.py /path/to/your/documents --verbose

# OR demo version (no API key needed)
python3 scripts/demo_intelligent_ingest.py
```

#### YouTube Videos
```bash
# Extract political speech transcripts from YouTube
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --verbose

# OR demo version (no API key needed)
python3 scripts/demo_youtube_ingestion.py
```

### 3. Check Results
```bash
# Text files
cat tmp/intelligent_ingestion_*/ingestion_results.json

# YouTube videos
cat tmp/youtube_ingestion_*/VIDEO_ID_result.json
```

**✅ Success!** Your messy files and YouTube videos are now research-ready corpus entries.

## What You Get

### From Text Files
**Input**: `random_speech.txt`, `inaugural_something.txt`, `untitled_document.txt`
**Output**: 
- `lincoln_inaugural_1865`: Complete metadata (title, author, date, type, description)
- `roosevelt_speech_1941`: Automatically registered in research database  
- `chavez_address_2006`: Ready for narrative gravity analysis

### From YouTube Videos
**Input**: `https://www.youtube.com/watch?v=lipnBHeyvII`
**Output**: 
- `davison_speech_2010_lipnBHey`: Complete metadata plus video information
- **Enhanced with**: Channel, views, duration, upload date, video ID
- `obama_address_2009_AbCdEfGh`: Presidential speeches with engagement metrics
- **Automatic classification**: Speech type detection (address, debate, interview)

## Success Expectations

| File Quality | Success Rate |
|--------------|--------------|
| 📄 Clean historical documents | 85-100% |
| 📄 Moderate quality texts | 60-85% |
| 📄 Poor/damaged files | 30-60% |

## Common Use Cases

### 🏛️ Historical Research
- Presidential speeches and addresses
- Political campaign materials
- Historical letters and documents
- UN speeches and international addresses
- **YouTube**: Official government channels, historical speech archives

### 📊 Political Analysis  
- Legislative speeches
- Party manifestos
- Debate transcripts
- Policy documents
- **YouTube**: Political debates, press conferences, campaign rallies

### 🎓 Academic Research
- Document corpus preparation
- Metadata standardization
- FAIR data compliance
- Publication preparation
- **YouTube**: Contemporary political discourse, international diplomacy

### 📺 Video Content Analysis
- **Presidential addresses** on official channels
- **UN General Assembly speeches** with captions
- **Political debates** from news organizations
- **Press conferences** and briefings
- **Campaign speeches** and town halls
- **International diplomatic** addresses

## Documentation Guide

### New Users
1. **[Quick Start Guide](INTELLIGENT_INGESTION_QUICKSTART.md)** - Get running immediately
2. **[Workflow Integration](CORPUS_WORKFLOW_INTEGRATION.md)** - Understand the big picture
3. **[Complete Guide](INTELLIGENT_CORPUS_INGESTION_GUIDE.md)** - When you need details

### Experienced Users
- **[Complete Guide](INTELLIGENT_CORPUS_INGESTION_GUIDE.md)** - Advanced features, troubleshooting
- **[Workflow Integration](CORPUS_WORKFLOW_INTEGRATION.md)** - Optimize your research process

### Troubleshooting
- **[Complete Guide](INTELLIGENT_CORPUS_INGESTION_GUIDE.md)** - Comprehensive troubleshooting section
- **[Quick Start Guide](INTELLIGENT_INGESTION_QUICKSTART.md)** - Common issues & quick fixes

## Integration with Other Systems

The Intelligent Corpus Ingestion Service (including YouTube support) works seamlessly with:

✅ **Enhanced Corpus Management System** - FAIR data compliance and academic standards
✅ **Priority 1 Infrastructure** - Component versioning and systematic analysis
✅ **Priority 2 CLI Tools** - Batch analysis and orchestration
✅ **Priority 3 Academic Tools** - Publication and replication packages
✅ **React Research Workbench** - Interactive analysis interface
✅ **YouTube Transcript API** - Free transcript extraction without API costs
✅ **Multi-Language Support** - Process political content in various languages

## Key Features

### 🤖 AI-Powered Extraction
- GPT-3.5-turbo metadata extraction
- Confidence scoring (0-100%)
- Automatic quality assessment
- Graceful error handling
- **YouTube**: Enhanced metadata with video information

### 📊 Quality Control
- Automatic categorization (successful/uncertain/failed)
- Manual review workflows
- Confidence threshold controls
- Complete audit trails
- **YouTube**: Video quality indicators (manual vs auto captions)

### 🔗 Corpus Integration
- Automatic database registration
- Semantic text ID generation
- FAIR data compliance
- Academic export ready
- **YouTube**: Enhanced with video metrics and engagement data

### 🛠️ Production Ready
- CLI tools for batch processing
- Dry-run mode for testing
- Comprehensive error handling
- Professional result reporting
- **YouTube**: Rate limiting and bulk video processing

### 📺 YouTube-Specific Features
- **Free transcript extraction** - No YouTube API costs
- **Multi-language support** - Extract captions in various languages
- **Enhanced metadata** - Channel, views, upload date, duration
- **Political content detection** - Automatic speech classification
- **Citation generation** - Academic referencing for video sources

## Support & Next Steps

### Getting Help
1. Check the appropriate guide above
2. Run with `--verbose` flag for detailed logs
3. Use `--dry-run` to test without committing changes

### Cost Considerations (LLM Version)

#### Text Files
- Small batch (10-20 files): ~$0.10-0.50
- Medium batch (50-100 files): ~$0.50-2.00
- Large batch (200+ files): ~$2.00-10.00

#### YouTube Videos
- **Transcript extraction**: FREE (no YouTube API costs)
- **LLM metadata enhancement**: ~$0.01-0.03 per video
- Small batch (10 videos): ~$0.10-0.30
- Medium batch (50 videos): ~$0.50-1.50
- Large batch (100+ videos): ~$1.00-5.00

### Best Practices

#### Text Files
- Start with small test batches
- Use demo version to understand workflow
- Review uncertain results manually
- Monitor API costs for large collections

#### YouTube Videos
- **Check captions availability** - Verify videos have captions before processing
- **Start with professional content** - News channels, government sources for best results
- **Use rate limiting** - Add delays for bulk processing (3-5 seconds between videos)
- **Prefer recent videos** - Better metadata and caption quality
- **Review manual vs auto captions** - Manual captions provide higher quality results

## Related Documentation

- **[Enhanced Corpus Management Guide](ENHANCED_CORPUS_MANAGEMENT_GUIDE.md)** - Underlying corpus system
- **[Component Versioning Guide](../development/component_versioning_guide.md)** - Analysis infrastructure
- **[Launch Guide](../../LAUNCH_GUIDE.md)** - System setup and operation

---

**Questions?** Start with the [Quick Start Guide](INTELLIGENT_INGESTION_QUICKSTART.md) for immediate help, or dive into the [Complete User Guide](INTELLIGENT_CORPUS_INGESTION_GUIDE.md) for comprehensive documentation. 