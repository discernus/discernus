# YouTube Transcript Ingestion - Quick Start Guide

## TL;DR: Extract Political Speech Transcripts from YouTube

```bash
# Set up environment
source venv/bin/activate && source scripts/setup_dev_env.sh

# Install YouTube dependencies
pip install youtube-transcript-api yt-dlp

# Process YouTube video (LLM version - requires OpenAI API key)
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --verbose

# OR demo version (no API key needed for testing)
python3 scripts/demo_youtube_ingestion.py

# Test the improved accuracy features
python3 scripts/test_youtube_improvements.py

# Check results
cat tmp/youtube_ingestion_*/VIDEO_ID_result.json
```

## What You Get

**Input**: YouTube URLs like `https://www.youtube.com/watch?v=lipnBHeyvII`
**Output**: Research-ready corpus entries with enhanced metadata:
- `davison_speech_2010_lipnBHey` with title, author, date, type, description
- **Plus YouTube metadata**: Views, channel, duration, upload date
- **Cross-validated speaker identification** with conflict detection
- Automatically registered in your research database
- Ready for narrative gravity analysis

## 🆕 NEW: Enhanced Accuracy Features (June 2025)

### Cross-Validation System
The tool now **automatically detects speaker identification conflicts** between AI analysis and YouTube metadata:

```bash
# When processing, you may see warnings like:
⚠️  Speaker identification conflict detected!
   LLM identified: Greg Abbott
   YouTube title: Gov Perry ALEC 2016

# Confidence score automatically reduced by 15 points
# Conflict flagged in extraction notes for manual review
```

### Enhanced Speaker Extraction
**Improved accuracy** through better content analysis:
- ✅ **Direct introductions**: "My name is Rick Perry..."
- ✅ **Political titles**: "Governor Abbott speaking..."
- ✅ **Validation patterns**: Filters out organization names
- ✅ **Extended content analysis**: Checks first 2000 characters

### Quality Assurance Testing
```bash
# Test the accuracy improvements
python3 scripts/test_youtube_improvements.py

# Expected output:
# ✅ Perry/Abbott misidentification - PASS
# ✅ Correct identification - PASS  
# ✅ Enhanced speaker extraction - PASS
```

## Success Expectations

| Content Type | Success Rate | Example |
|--------------|--------------|---------|
| 📺 Professional political videos | 90-100% | Presidential addresses, UN speeches |
| 📺 News channel content | 80-95% | CNN, BBC, major news outlets |
| 📺 User content with captions | 70-90% | Political commentary, campaign videos |
| 📺 No captions available | 0% | Graceful failure with clear message |

## Essential Commands

### Basic Processing
```bash
# Process one video with defaults (70% confidence threshold)
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL"

# High-quality only (85% threshold)  
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --confidence-threshold 85

# Test without database changes
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --dry-run --verbose
```

### Demo Version (No API Key)
```bash
# Test YouTube extraction capabilities
python3 scripts/demo_youtube_ingestion.py
```

### Batch Processing
```bash
# Process multiple videos with rate limiting
videos=(
    "https://www.youtube.com/watch?v=VIDEO1"
    "https://www.youtube.com/watch?v=VIDEO2" 
    "https://www.youtube.com/watch?v=VIDEO3"
)

for url in "${videos[@]}"; do
    python3 scripts/intelligent_ingest_youtube.py "$url" --verbose
    sleep 3  # Rate limiting
done
```

### Check Results
```bash
# View processing results
cat tmp/youtube_ingestion_*/VIDEO_ID_result.json

# Check what was added to corpus
python3 -c "
from src.narrative_gravity.corpus.discovery import CorpusDiscovery
discovery = CorpusDiscovery()
results = discovery.search('source:youtube_intelligent_ingestion')
print(f'Added {results.total_matches} YouTube videos to corpus')
"
```

## Confidence Levels

| Level | Score | What Happens | Action Needed |
|-------|-------|--------------|---------------|
| ✅ **Successful** | ≥70% | Auto-registered in corpus | ✅ Ready for analysis |
| ⚠️ **Uncertain** | 40-69% | Saved but not registered | 📝 Review & manually register |
| 🚨 **Conflict Detected** | -15 points | Speaker ID conflict flagged | 🔍 **Manual review required** |
| ❌ **Failed** | <40% | Basic fallback metadata | 🔧 Manual processing required |

### Understanding Conflict Detection
When the system detects a **speaker identification conflict** between AI analysis and YouTube metadata:
- **Confidence score reduced by 15 points** (e.g., 85% → 70%)
- **Warning message displayed** during processing
- **Extraction notes flagged** with conflict details
- **Manual review recommended** before using for research

## Common Issues & Quick Fixes

### "No transcript available for this video"
```bash
# Check if video has captions first (manually on YouTube)
# Try different language preferences
python3 scripts/intelligent_ingest_youtube.py "URL" --languages en es fr

# Some videos simply don't have captions - this is normal
```

### "OpenAI API key not set"
```bash
# Set API key for enhanced metadata
export OPENAI_API_KEY=sk-your-key-here

# OR use basic YouTube-only processing (still works!)
# Processing continues with YouTube metadata only
```

### "Could not extract video ID from URL"
```bash
# Ensure URL format is correct:
# ✅ https://www.youtube.com/watch?v=VIDEO_ID
# ✅ https://youtu.be/VIDEO_ID
# ❌ Don't use playlist URLs or other formats
```

### Low success rate
```bash
# Lower confidence threshold for uncertain content
python3 scripts/intelligent_ingest_youtube.py "URL" --confidence-threshold 50

# Check uncertain results for manual processing
cat tmp/youtube_ingestion_*/VIDEO_ID_result.json
```

### 🚨 Speaker identification conflict detected
```bash
# When you see conflict warnings:
⚠️  Speaker identification conflict detected!
   LLM identified: Greg Abbott
   YouTube title: Gov Perry ALEC 2016

# Check the extraction notes in result file:
jq '.metadata.extraction_notes' tmp/youtube_ingestion_*/VIDEO_ID_result.json

# Manually verify the correct speaker and register:
# 1. Watch/listen to video to confirm actual speaker
# 2. Use manual registration with correct metadata
# 3. Report pattern to improve future accuracy
```

## Manual Correction for Uncertain Results

```bash
# Register manually with corrected metadata
python3 -c "
from src.narrative_gravity.corpus.registry import CorpusRegistry
registry = CorpusRegistry()
registry.register_document(
    text_id='corrected_speaker_speech_2020',
    file_path='path/to/transcript.txt',
    metadata={
        'title': 'Corrected Speech Title',
        'author': 'Speaker Name', 
        'date': 'YYYY-MM-DD',
        'document_type': 'speech|address|debate|interview',
        'description': 'Brief description',
        'youtube_video_id': 'VIDEO_ID',
        'youtube_url': 'https://www.youtube.com/watch?v=VIDEO_ID',
        'source': 'youtube_manual_correction'
    }
)
"
```

## Installation Requirements

### Required Dependencies
```bash
pip install youtube-transcript-api yt-dlp
```

### System Requirements
✅ **Internet connection** for YouTube access
✅ **YouTube videos with captions/subtitles** enabled  
✅ **Valid YouTube URLs** (not private/restricted)
❌ **No video download** - only transcript extraction

## Cost Estimates (LLM Version)

- **Single video**: ~$0.01-0.03
- **Small batch (10 videos)**: ~$0.10-0.30  
- **Medium batch (50 videos)**: ~$0.50-1.50
- **Large batch (100+ videos)**: ~$1.00-5.00

*Prices based on GPT-3.5-turbo rates as of June 2025*
*Note: YouTube transcript extraction itself is free*

## Video Selection Tips

### ✅ **Best Success Rates**
- Major news channels (CNN, BBC, Fox News)
- Government/official channels
- Professional political content
- Recent videos (better metadata)
- Videos with manual captions

### ⚠️ **Moderate Success** 
- User-generated political content
- Auto-generated captions only
- Older videos (limited metadata)
- Non-English content

### ❌ **Will Not Work**
- Videos without any captions
- Private/unlisted videos
- Age-restricted content
- Live streams (incomplete captions)

## YouTube-Specific Text ID Format

Generated automatically: `{author}_{type}_{year}_{video_id_prefix}`

**Examples:**
- `davison_speech_2010_lipnBHey` (Phil Davidson treasurer speech)
- `obama_address_2009_AbCdEfGh` (Obama presidential address)
- `youtube_interview_2020_XyZ12345` (Generic format when unclear)

## Enhanced Metadata Features

YouTube ingestion provides **extra metadata** beyond regular text files:

### 📺 **Video Metadata**
- Channel name and credibility
- Upload date and view count
- Video duration and engagement metrics
- Like/dislike ratios (where available)

### 🎯 **Content Classification**
- Automatic speech type detection (address, debate, interview)
- Speaker identification from channel and content
- Political context awareness
- Audience reaction tracking (applause, laughter)

### 🔗 **Citation Information**
- Complete YouTube URL preservation
- Video ID for permanent reference
- Upload date for temporal analysis
- Channel attribution for source tracking

## Next Steps After Processing

### Export for Analysis
```bash
# Export YouTube corpus for research
python3 -c "
from src.narrative_gravity.corpus.exporter import CorpusExporter
exporter = CorpusExporter()
exporter.export_csv('youtube_political_corpus.csv')
"
```

### Generate Citations
```bash
# Create academic citation list
python3 -c "
import json
from pathlib import Path

citations = []
for result_file in Path('tmp/youtube_ingestion_*').glob('*_result.json'):
    with open(result_file) as f:
        data = json.load(f)
        video_info = data.get('video_info', {})
        citations.append({
            'title': video_info.get('title'),
            'channel': video_info.get('channel'),
            'url': video_info.get('url'),
            'date': video_info.get('upload_date')
        })

with open('video_citations.json', 'w') as f:
    json.dump(citations, f, indent=2)
print(f'Generated citations for {len(citations)} videos')
"
```

### Integrate with Analysis
```bash
# Use your YouTube corpus with existing tools
# All YouTube videos appear in regular corpus searches
# Enhanced with video-specific metadata fields
```

## Multi-Language Support

```bash
# Extract transcripts in preferred language order
python3 scripts/intelligent_ingest_youtube.py "URL" --languages en es fr de

# Spanish political content
python3 scripts/intelligent_ingest_youtube.py "URL" --languages es en

# French political speeches  
python3 scripts/intelligent_ingest_youtube.py "URL" --languages fr en
```

## Security & Privacy Notes

- ✅ **No video download** - only transcript text
- ✅ **Local processing** - results stored locally
- ⚠️ **YouTube terms** - subject to YouTube's terms of service
- ⚠️ **API usage** - transcript content may be sent to OpenAI for metadata extraction

For sensitive content:
```bash
# Process without sending to external APIs
unset OPENAI_API_KEY
python3 scripts/intelligent_ingest_youtube.py "SENSITIVE_URL" --dry-run
```

## Perfect for Political Research

YouTube ingestion is ideal for:
- **Presidential addresses and speeches**
- **UN General Assembly speeches**
- **Political debates and town halls**
- **Campaign rallies and events**
- **Press conferences and briefings**
- **Legislative hearings and testimony**
- **International diplomatic addresses**

---

**Need more details?** See the complete [YouTube Transcript Ingestion Guide](YOUTUBE_TRANSCRIPT_INGESTION_GUIDE.md) for comprehensive documentation, advanced usage, and troubleshooting.

**Questions?** Run with `--verbose` flag for detailed processing logs or check the troubleshooting section in the complete guide. 