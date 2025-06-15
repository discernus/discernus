# YouTube Transcript Intelligent Ingestion Service - User Guide

## Overview

The YouTube Transcript Intelligent Ingestion Service extends the corpus management system to automatically extract transcripts and metadata from YouTube videos, making it easy to build research corpora from video content. This is particularly valuable for political speeches, debates, and addresses that are frequently published on YouTube.

### What This Service Does

✅ **Automatic Transcript Extraction**: Downloads transcripts from YouTube videos with captions/subtitles  
✅ **Enhanced Metadata Extraction**: Combines YouTube video metadata with AI-powered content analysis  
✅ **Cross-Validation System**: Detects conflicts between AI and YouTube metadata for improved accuracy  
✅ **Enhanced Speaker Identification**: Advanced pattern matching for political figures and titles  
✅ **Multi-Language Support**: Can extract transcripts in various languages (English preferred)  
✅ **Video Information Capture**: Records view counts, upload dates, channel information, and video metrics  
✅ **Intelligent Content Classification**: Automatically identifies speech types (address, debate, interview, etc.)  
✅ **Corpus Integration**: Seamlessly integrates with existing corpus management system  

### What This Service Does NOT Do

❌ **Video Download**: Only extracts text transcripts, not video files  
❌ **Audio Processing**: Requires existing captions/subtitles, doesn't generate transcripts  
❌ **Private Content**: Cannot access private, unlisted, or age-restricted videos  
❌ **Perfect Accuracy**: YouTube auto-generated captions may contain errors  
❌ **Real-time Processing**: Works with uploaded videos, not live streams  

## Setting Expectations

### Success Rates by Content Type
- **Professional political videos with manual captions**: 90-100% success rate  
- **Major news channels with auto-captions**: 80-95% success rate  
- **User-uploaded content with captions**: 70-90% success rate  
- **Videos without any captions**: 0% success rate (graceful failure)  
- **Private/restricted videos**: 0% success rate (graceful failure)  

### Processing Time & Costs
- **Single video processing**: 10-30 seconds  
- **API cost per video**: ~$0.01-0.03 (for LLM metadata extraction)  
- **Bulk processing**: Limited by API rate limits (typically 100-200 videos/hour)  
- **No additional YouTube API costs**: Uses free transcript extraction  

### Quality Expectations
- **Manual captions**: Excellent quality, punctuation preserved  
- **Auto-generated captions**: Good quality, may lack punctuation  
- **Metadata confidence**: 85-100% for videos with good titles and descriptions  
- **Speaker identification**: 80-95% accuracy with enhanced pattern matching and conflict detection  
- **Cross-validation**: Automatically flags potential speaker misidentification (15-point confidence reduction)  
- **Conflict detection**: Warns users when AI and YouTube metadata disagree  

## Prerequisites

### Required Dependencies
```bash
# Install YouTube transcript dependencies
pip install youtube-transcript-api yt-dlp

# Verify installation
python3 -c "import youtube_transcript_api, yt_dlp; print('✅ YouTube dependencies installed')"
```

### System Requirements
1. **Narrative Gravity environment** set up with database
2. **Python virtual environment** activated
3. **Internet connection** for YouTube access
4. **Valid YouTube URLs** with available transcripts

### Optional (for Enhanced Metadata)
- **OpenAI API key** for LLM-powered metadata enhancement
- **API credits** for processing (typically $0.01-0.03 per video)

## Installation & Setup

### Step 1: Environment Setup
```bash
# Navigate to project directory
cd narrative_gravity_analysis

# Activate virtual environment
source venv/bin/activate

# Set up development environment  
source scripts/setup_dev_env.sh

# Install YouTube dependencies
pip install youtube-transcript-api yt-dlp
```

### Step 2: Verify Installation
```bash
# Test YouTube transcript extraction
python3 scripts/demo_youtube_ingestion.py
```

**Expected output:**
```
🎬 YouTube Transcript Intelligent Ingestion Demo
✅ youtube-transcript-api available
✅ yt-dlp available for enhanced metadata
✅ YouTube ingestion service imported successfully
```

### Step 3: Test with Sample Video
```bash
# Test with a known working video (dry-run mode)
python3 scripts/intelligent_ingest_youtube.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --dry-run --verbose
```

### Step 4: Test Enhanced Accuracy Features
```bash
# Test the improved cross-validation and speaker identification
python3 scripts/test_youtube_improvements.py

# Expected output shows all tests passing:
# ✅ Perry/Abbott misidentification - PASS
# ✅ Correct identification - PASS  
# ✅ Enhanced speaker extraction - PASS
```

## 🆕 Enhanced Accuracy Features (June 2025)

### Cross-Validation System
The service now includes **automatic conflict detection** between AI analysis and YouTube metadata:

**What it does:**
- Compares LLM speaker identification with YouTube title patterns
- Detects potential misidentifications (e.g., "Greg Abbott" vs "Gov Perry")
- Automatically reduces confidence scores by 15 points when conflicts detected
- Flags extraction notes for manual review

**Example conflict detection:**
```bash
⚠️  Speaker identification conflict detected!
   LLM identified: Greg Abbott
   YouTube title: Gov Perry ALEC 2016

# Result: Confidence reduced from 85% to 70%
# Flagged for manual review in extraction notes
```

### Enhanced Speaker Extraction
**Improved accuracy** through advanced pattern matching:

✅ **Direct speaker identification**:
- "My name is Rick Perry..."
- "I'm Governor Abbott..."
- "This is Senator Warren..."

✅ **Political title recognition**:
- "Governor Abbott speaking..."
- "President Obama addresses..."
- "Senator McCain remarks..."

✅ **Content validation**:
- Analyzes first 2000 characters (vs 1000 previously)
- Filters out organization names that match person patterns
- Validates name components for realistic human names

✅ **Fallback hierarchy**:
1. Direct speaker introductions (highest priority)
2. Political title + name patterns  
3. Channel name analysis (with validation)
4. Channel name as fallback

### Quality Assurance Testing
```bash
# Verify the improvements work correctly
python3 scripts/test_youtube_improvements.py

# Test specific conflict scenarios
python3 -c "
from src.narrative_gravity.corpus.youtube_ingestion import YouTubeCorpusIngestionService
service = YouTubeCorpusIngestionService(None)
conflict = service._check_speaker_conflict('Greg Abbott', 'Gov Perry ALEC 2016')
print(f'Conflict detected: {conflict}')  # Should be True
"
```

## Usage Guide

### Basic Video Processing

#### Single Video Processing
```bash
# Process one video with defaults
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL"

# With verbose output
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --verbose

# Test without database registration
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --dry-run --verbose
```

#### Custom Output Directory
```bash
# Specify output location
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --output-dir my_youtube_analysis/
```

#### Confidence Threshold Control
```bash
# High-quality only (85% confidence)
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --confidence-threshold 85

# More permissive (50% confidence)  
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --confidence-threshold 50
```

### Advanced Features

#### Multi-Language Support
```bash
# Prefer specific languages (fallback order)
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --languages en es fr

# French-first extraction
python3 scripts/intelligent_ingest_youtube.py "YOUTUBE_URL" --languages fr en
```

#### Batch Processing Multiple Videos
```bash
# Process multiple videos (create shell script)
#!/bin/bash
videos=(
    "https://www.youtube.com/watch?v=VIDEO1"
    "https://www.youtube.com/watch?v=VIDEO2"
    "https://www.youtube.com/watch?v=VIDEO3"
)

for url in "${videos[@]}"; do
    echo "Processing: $url"
    python3 scripts/intelligent_ingest_youtube.py "$url" --verbose
    sleep 2  # Rate limiting
done
```

## Understanding Results

### Processing Output

**Successful processing shows:**
```
🎬 Processing YouTube video: lipnBHeyvII
📺 Title: Phil Davidson Stump Speech
📺 Channel: National Review
✅ Processed transcript (3904 chars)
📊 Confidence: 100.0%

📊 Results:
  Video ID: lipnBHeyvII
  Confidence: 100.0%
  Content Length: 3904 characters

📋 Extracted Metadata:
  Title: Speech by Phil Davison at Star County Republican Party Executive Committee
  Author: Phil Davison
  Date: 2010-11-10
  Type: speech
  Description: Phil Davison's speech seeking nomination for Star County Treasurer

📺 YouTube Metadata:
  Channel: National Review
  Upload Date: 2010-09-09
  Duration: 356 seconds
  Views: 126594

✅ Registered in corpus as: davison_speech_2010_lipnBHey
```

### Result Files Generated

Each processed video creates:
- **`{video_id}_transcript.txt`**: Clean transcript text
- **`{video_id}_result.json`**: Complete processing results and metadata
- **Processing summary**: Overall statistics and status

### Confidence Scoring for YouTube Content

**Enhanced scoring includes:**
- **Base extraction confidence** (0-100% from intelligent ingestion)
- **YouTube metadata bonus** (+10 points for complete video info)
- **Channel credibility** (news channels, official accounts get bonus)
- **Video engagement** (high view/like counts improve confidence)
- **Transcript quality** (manual captions score higher than auto-generated)

### Generated Text IDs for YouTube Content

**Format**: `{author}_{type}_{year}_{video_id_prefix}`

**Examples:**
- `davison_speech_2010_lipnBHey` (Phil Davidson treasurer speech)
- `obama_address_2009_AbCdEfGh` (Obama address from 2009)
- `youtube_interview_2020_XyZ12345` (Generic format when speaker unclear)

## Troubleshooting Common Issues

### Video Access Problems

#### "❌ Error: No transcript available for this video"
**Causes:**
- Video has no captions/subtitles enabled
- Captions are only available in unsupported languages
- Video is private, unlisted, or age-restricted

**Solutions:**
```bash
# Check if video has captions manually on YouTube
# Try different language preferences
python3 scripts/intelligent_ingest_youtube.py "URL" --languages en es fr de

# Check video accessibility in browser first
```

#### "❌ Error: Could not extract video ID from URL"
**Causes:**
- Malformed YouTube URL
- URL contains additional parameters
- Not a valid YouTube URL

**Solutions:**
```bash
# Verify URL format - supported formats:
# https://www.youtube.com/watch?v=VIDEO_ID
# https://youtu.be/VIDEO_ID
# https://www.youtube.com/embed/VIDEO_ID

# Clean URL by removing extra parameters
# Use just: https://www.youtube.com/watch?v=VIDEO_ID
```

### Processing Issues

#### "⚠️ Warning: yt-dlp not available - basic metadata only"
**Impact**: Limited video metadata (title, channel may be missing)
**Solution:**
```bash
pip install yt-dlp
# Then retry processing
```

#### "⚠️ Warning: OPENAI_API_KEY environment variable not set"
**Impact**: Basic metadata extraction only (no AI enhancement)
**Solutions:**
```bash
# Set API key for enhanced processing
export OPENAI_API_KEY=sk-your-key-here

# OR proceed with YouTube metadata only (still functional)
# Processing will work but with basic metadata extraction
```

#### Low confidence scores for political content
**Causes:**
- Auto-generated captions with poor punctuation
- Unclear speaker identification
- Generic video titles

**Solutions:**
```bash
# Lower confidence threshold
python3 scripts/intelligent_ingest_youtube.py "URL" --confidence-threshold 50

# Review uncertain results for manual correction
cat output_dir/VIDEO_ID_result.json

# Manual registration with corrected metadata
python3 -c "
from src.narrative_gravity.corpus.registry import CorpusRegistry
registry = CorpusRegistry()
registry.register_document(
    text_id='corrected_speaker_speech_2020',
    file_path='path/to/transcript.txt',
    metadata={
        'title': 'Corrected Speech Title',
        'author': 'Speaker Name',
        'date': '2020-01-15',
        'document_type': 'speech',
        'youtube_video_id': 'VIDEO_ID',
        'youtube_url': 'https://www.youtube.com/watch?v=VIDEO_ID'
    }
)
"
```

#### 🚨 Speaker identification conflict detected
**What you'll see:**
```bash
⚠️  Speaker identification conflict detected!
   LLM identified: Greg Abbott
   YouTube title: Gov Perry ALEC 2016
```

**Causes:**
- AI misidentified speaker from transcript content
- YouTube title contains correct speaker information
- Cross-validation system caught the discrepancy

**Solutions:**
```bash
# 1. Check the extraction notes for details
jq '.metadata.extraction_notes' output_dir/VIDEO_ID_result.json

# 2. Manually verify the actual speaker
# Watch a portion of the video to confirm who is speaking

# 3. Use manual registration with correct speaker
python3 -c "
from src.narrative_gravity.corpus.registry import CorpusRegistry
registry = CorpusRegistry()
registry.register_document(
    text_id='perry_alec_speech_2016',
    file_path='path/to/transcript.txt', 
    metadata={
        'title': 'Gov Perry ALEC 2016 Speech',
        'author': 'Rick Perry',  # Corrected speaker
        'date': '2016-08-04',
        'document_type': 'speech',
        'youtube_video_id': 'VIDEO_ID',
        'youtube_url': 'https://www.youtube.com/watch?v=VIDEO_ID',
        'source': 'youtube_manual_correction'
    }
)
print('✅ Registered with correct speaker identification')
"

# 4. Report the pattern for future improvement
# Document the misidentification case for training data
```

**Prevention:**
```bash
# Use the test suite to verify accuracy improvements
python3 scripts/test_youtube_improvements.py

# This specific Perry/Abbott case should now be caught automatically
```

### Network and Rate Limiting

#### Processing failures or slow responses
**Causes:**
- Network connectivity issues
- YouTube API rate limiting
- Server-side restrictions

**Solutions:**
```bash
# Add delays between requests for batch processing
for url in "${urls[@]}"; do
    python3 scripts/intelligent_ingest_youtube.py "$url"
    sleep 5  # 5-second delay
done

# Test connectivity first
python3 -c "
import requests
response = requests.get('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
print('✅ YouTube accessible' if response.status_code == 200 else '❌ Connection issue')
"
```

## Best Practices

### Content Curation Strategy

#### 1. Video Selection Criteria
```bash
# Prioritize videos with:
# ✅ Manual captions (professional content)
# ✅ Clear titles indicating content type
# ✅ Established channels (news, government, institutions)
# ✅ Recent upload dates (better metadata)
# ✅ High engagement (views, likes)

# Avoid:
# ❌ User-generated content without captions
# ❌ Very old videos (may lack metadata)
# ❌ Compilation videos (mixed content)
# ❌ Live streams (incomplete transcripts)
```

#### 2. Quality Assurance Workflow
```bash
# Step 1: Test with small sample
python3 scripts/intelligent_ingest_youtube.py "TEST_URL" --dry-run --verbose

# Step 2: Process with confidence threshold
python3 scripts/intelligent_ingest_youtube.py "URL" --confidence-threshold 75

# Step 3: Review uncertain cases
cat output_dir/*_result.json | grep -A5 -B5 '"confidence": [4-6][0-9]'

# Step 4: Manual correction for key videos
# (Use manual registration code from troubleshooting section)
```

### Batch Processing Strategy

#### For Large Video Collections
```bash
# Create video list file
cat > video_list.txt << 'EOF'
https://www.youtube.com/watch?v=VIDEO1  # Presidential Address 2020
https://www.youtube.com/watch?v=VIDEO2  # UN Speech 2019
https://www.youtube.com/watch?v=VIDEO3  # Campaign Rally 2018
EOF

# Process with rate limiting
#!/bin/bash
while IFS= read -r line; do
    # Skip comments and empty lines
    [[ $line =~ ^#.*$ ]] && continue
    [[ -z "${line// }" ]] && continue
    
    # Extract URL (first word)
    url=$(echo $line | awk '{print $1}')
    echo "Processing: $url"
    
    python3 scripts/intelligent_ingest_youtube.py "$url" --verbose
    
    # Rate limiting - adjust as needed
    sleep 3
done < video_list.txt
```

### Cost Management

#### API Usage Optimization
```bash
# Process without LLM enhancement first (free)
unset OPENAI_API_KEY
python3 scripts/intelligent_ingest_youtube.py "URL" --dry-run

# Review basic results, then decide which need LLM enhancement
export OPENAI_API_KEY=sk-your-key-here
python3 scripts/intelligent_ingest_youtube.py "IMPORTANT_URL" --confidence-threshold 80
```

## Integration with Research Workflows

### Academic Research Pipeline
```bash
# 1. Curate video collection (political speeches, debates)
# 2. Process with YouTube ingestion
for url in "${political_videos[@]}"; do
    python3 scripts/intelligent_ingest_youtube.py "$url" --confidence-threshold 75
done

# 3. Verify corpus integration
python3 -c "
from src.narrative_gravity.corpus.discovery import CorpusDiscovery
discovery = CorpusDiscovery()
results = discovery.search('source:youtube_intelligent_ingestion')
print(f'📺 YouTube corpus: {results.total_matches} videos ingested')
"

# 4. Export for analysis
python3 -c "
from src.narrative_gravity.corpus.exporter import CorpusExporter
exporter = CorpusExporter()
exporter.export_csv('youtube_political_corpus.csv')
"
```

### Replication and Citation
```bash
# Document video sources for academic citation
python3 -c "
import json
from pathlib import Path

# Collect all YouTube processing results
results_dir = Path('tmp/youtube_ingestion_*')
video_citations = []

for result_file in results_dir.glob('*_result.json'):
    with open(result_file) as f:
        data = json.load(f)
        video_info = data.get('video_info', {})
        citation = {
            'title': video_info.get('title'),
            'channel': video_info.get('channel'),
            'url': video_info.get('url'),
            'upload_date': video_info.get('upload_date'),
            'view_count': video_info.get('view_count'),
            'duration': video_info.get('duration')
        }
        video_citations.append(citation)

# Save citation information
with open('youtube_video_citations.json', 'w') as f:
    json.dump(video_citations, f, indent=2)

print(f'📋 Saved citations for {len(video_citations)} videos')
"
```

## Technical Architecture

### System Components

#### 1. YouTubeTranscriptExtractor
- **Handles**: Video ID extraction, transcript download, content cleaning
- **Dependencies**: youtube-transcript-api
- **Features**: Multi-language support, auto/manual caption preference

#### 2. YouTubeCorpusIngestionService  
- **Extends**: IntelligentIngestionService
- **Enhancements**: Video metadata integration, speaker identification
- **Dependencies**: yt-dlp (optional for enhanced metadata)

#### 3. Enhanced Metadata Pipeline
- **Combines**: YouTube metadata + LLM content analysis
- **Confidence boost**: +10 points for complete video information
- **Speaker extraction**: Pattern matching for political figures

### Data Flow
```
YouTube URL → Video ID extraction → Transcript download → Content cleaning → 
Metadata extraction (YouTube + LLM) → Confidence scoring → 
Corpus registration (if high confidence) → Result storage
```

### Database Integration
- **Extends existing corpus schema** with YouTube-specific fields
- **Preserves compatibility** with existing analysis tools
- **Adds tracking fields**: video_id, youtube_url, channel, view_count, etc.

### Error Handling
- **Graceful fallback**: YouTube-only metadata when LLM fails
- **Network resilience**: Retry logic for temporary failures
- **Validation**: URL format checking, video accessibility verification
- **Comprehensive logging**: Full audit trail for troubleshooting

## Security and Privacy Considerations

### Data Handling
- ✅ **No video download**: Only transcript text is processed
- ✅ **Local storage**: All results stored locally, not on external servers
- ✅ **API transparency**: Clear documentation of what data goes to OpenAI
- ⚠️ **YouTube terms**: Subject to YouTube's terms of service for transcript access
- ⚠️ **Content sensitivity**: Consider privacy implications for political content

### Best Practices for Sensitive Content
```bash
# Use dry-run mode for sensitive videos
python3 scripts/intelligent_ingest_youtube.py "SENSITIVE_URL" --dry-run

# Process without LLM enhancement to avoid sending content to external APIs
unset OPENAI_API_KEY
python3 scripts/intelligent_ingest_youtube.py "SENSITIVE_URL"

# Review extracted content before corpus registration
cat output_dir/VIDEO_ID_transcript.txt
```

## Performance and Scaling

### Expected Performance
- **Single video**: 10-30 seconds processing time
- **Network-bound**: Limited by YouTube response times
- **LLM-bound**: Limited by OpenAI API rate limits (3000 requests/minute)
- **Storage**: Minimal - transcripts typically 1-50KB per video

### Scaling Considerations
```bash
# For large-scale processing (100+ videos):
# 1. Implement proper rate limiting
# 2. Use batch processing with delays
# 3. Monitor API usage and costs
# 4. Consider processing in stages (YouTube metadata first, LLM enhancement later)
```

## Related Documentation

- **[Intelligent Corpus Ingestion Guide](INTELLIGENT_CORPUS_INGESTION_GUIDE.md)** - Base ingestion system
- **[Enhanced Corpus Management Guide](ENHANCED_CORPUS_MANAGEMENT_GUIDE.md)** - Corpus system overview
- **[Corpus Workflow Integration Guide](CORPUS_WORKFLOW_INTEGRATION.md)** - Research workflow context
- **[Launch Guide](../../LAUNCH_GUIDE.md)** - System setup and operation

---

*This guide covers YouTube Transcript Intelligent Ingestion as of June 2025. The service extends the core intelligent ingestion system with YouTube-specific capabilities for video transcript extraction and enhanced metadata processing.* 