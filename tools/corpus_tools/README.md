# Transcript Extraction Infrastructure

**Durable, reusable infrastructure for extracting transcripts from various media sources that can be used across all Discernus projects and experiments.**

## 🚀 Quick Start

### Basic Usage
```bash
# Extract transcript with Whisper (recommended)
python -m scripts.corpus_tools.transcript_extractor_cli \
    "https://youtube.com/watch?v=VIDEO_ID" \
    --output-dir ./output \
    --whisper-model small

# Check dependencies
python -m scripts.corpus_tools.transcript_extractor_cli --check-deps
```

### Python API
```python
from scripts.corpus_tools.transcript_extractor import TranscriptExtractor
from pathlib import Path

extractor = TranscriptExtractor(
    prefer_method="whisper",
    whisper_model="small",  # Standardized on small for best quality/speed
    output_format="both"
)

result = extractor.extract_from_url(
    url="https://youtube.com/watch?v=VIDEO_ID",
    output_dir=Path("./output"),
    languages=["en"]
)
```

## 🎯 What This Tool Does

This infrastructure provides **framework-agnostic transcript extraction** with:

- **Multi-method extraction**: YouTube API + Whisper fallback
- **Robust error handling**: Graceful degradation when methods fail
- **Standardized output**: Consistent formatting and metadata
- **Quality assessment**: Confidence scores and completeness metrics

## 📋 Prerequisites

### Dependencies
- Python 3.8+
- OpenAI Whisper
- yt-dlp
- youtube-transcript-api
- FFmpeg (for audio processing)

### Check Installation
```bash
python -m scripts.corpus_tools.transcript_extractor_cli --check-deps
```

## 🔧 Configuration Options

### Command Line Arguments
```bash
python -m scripts.corpus_tools.transcript_extractor_cli [URL] [OPTIONS]

Options:
  --output-dir, -o        Output directory (default: ./transcript_extractions)
  --prefer-method         youtube, whisper, or auto (default: auto)
  --whisper-model         tiny, base, small, medium, large (default: base)
  --languages, -l         Preferred languages (default: en)
  --rate-limit            Delay between requests in seconds (default: 5)
  --retry-attempts        Number of retry attempts (default: 3)
  --output-format         txt, json, or both (default: both)
  --experiment-context    Context for provenance tracking
  --verbose, -v           Enable verbose logging
```

### Whisper Model Selection
| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| **tiny** | 39 MB | Fastest | Lower | Quick testing |
| **base** | 74 MB | Fast | Lower | Development |
| **small** | 244 MB | Good | High | ⭐ **Production** |
| **medium** | 769 MB | Slower | Higher | Final quality |
| **large** | 1550 MB | Slowest | Highest | Research |

**Recommendation**: Use **`small`** for production work - excellent quality/speed balance.

## 📁 Output Structure

### Files Created
```
output_directory/
├── video_title_date_method.txt          # Transcript file
└── video_title_date_method_metadata.json # Metadata file
```

### Transcript File Format
```
# Video Title
# Channel: Channel Name
# Upload Date: 2024-06-15
# Video URL: https://youtube.com/watch?v=VIDEO_ID
# Language: en
# Extraction Method: whisper
# Confidence: 85.2%
# Whisper Model: small
# Extracted: 2025-08-21 16:08:40

================================================================================

[Transcript content with proper line breaks and formatting]
```

### Metadata File Format
```json
{
  "success": true,
  "url": "https://youtube.com/watch?v=VIDEO_ID",
  "method": "whisper",
  "confidence": 85.2,
  "transcript_length": 15000,
  "word_count": 2500,
  "language": "en",
  "extraction_timestamp": "2025-08-21T16:08:40Z",
  "processing_time": 45.2,
  "fallback_attempted": true,
  "fallback_success": true,
  "video_info": {
    "title": "Video Title",
    "channel": "Channel Name",
    "duration": 1800,
    "upload_date": "2024-06-15",
    "video_id": "VIDEO_ID"
  }
}
```

## 🔄 Extraction Methods

### 1. YouTube Transcript API (Primary)
- **Pros**: Fastest, highest quality, official transcripts
- **Cons**: May be blocked by IP bans, rate limits
- **Use**: When available and not blocked

### 2. Whisper Fallback (Secondary)
- **Pros**: Always works, high quality, local processing
- **Cons**: Slower, more CPU intensive
- **Use**: When YouTube API fails or for highest quality

### 3. Automatic Fallback
- **Behavior**: Try YouTube API first, fall back to Whisper
- **Command**: `--prefer-method auto` (default)

## 🚨 Error Handling

### Common Error Types
- **`api_rate_limit`**: YouTube API blocked - use Whisper
- **`content_unavailable`**: Video is private/deleted
- **`network_error`**: Connection issues
- **`whisper_error`**: Audio processing failed

### Error Response
```json
{
  "success": false,
  "error_type": "api_rate_limit",
  "error_message": "YouTube API rate limit exceeded",
  "retry_after": 3600,
  "can_retry": true
}
```

### Retry Logic
- **Automatic**: System attempts fallback methods
- **Manual**: Check `can_retry` and `retry_after` fields
- **Rate Limiting**: Built-in delays prevent overwhelming services

## 📊 Performance & Quality

### Processing Times (M4 Mac Mini)
| Model | Time per 3.5-min video | Quality |
|-------|------------------------|---------|
| tiny | ~13 seconds | 75% |
| base | ~32 seconds | 75% |
| **small** | **~64 seconds** | **85%** ⭐ |
| medium | ~163 seconds | 90% |

### Quality Metrics
- **Confidence Score**: 0-100% accuracy assessment
- **Completeness**: Estimated transcript coverage
- **Word Count**: Total words extracted
- **Language Detection**: Automatically detected language

## 🎯 Use Cases

### Single Video Extraction
```bash
python -m scripts.corpus_tools.transcript_extractor_cli \
    "https://youtube.com/watch?v=VIDEO_ID" \
    --output-dir ./transcripts \
    --whisper-model small
```

### Batch Processing
```python
from scripts.corpus_tools.transcript_extractor import TranscriptExtractor
from pathlib import Path

extractor = TranscriptExtractor(
    prefer_method="whisper",
    whisper_model="small",
    rate_limit=10  # 10 second delay between requests
)

urls = [
    "https://youtube.com/watch?v=VIDEO1",
    "https://youtube.com/watch?v=VIDEO2",
    # ... more URLs
]

for url in urls:
    result = extractor.extract_from_url(
        url=url,
        output_dir=Path("./batch_output"),
        languages=["en"]
    )
    print(f"Processed {url}: {'✅' if result.success else '❌'}")
```

### Discernus Integration
```bash
# Extract to experiment corpus directory
python -m scripts.corpus_tools.transcript_extractor_cli \
    "https://youtube.com/watch?v=VIDEO_ID" \
    --output-dir projects/my_experiment/corpus/transcripts \
    --whisper-model small \
    --experiment-context "my_experiment"
```

## 🛠️ Troubleshooting

### YouTube API Blocked
```bash
# Force Whisper usage
python -m scripts.corpus_tools.transcript_extractor_cli \
    "https://youtube.com/watch?v=VIDEO_ID" \
    --prefer-method whisper \
    --whisper-model small
```

### Audio Download Issues
- Check FFmpeg installation: `ffmpeg -version`
- Verify yt-dlp: `pip list | grep yt-dlp`
- Check disk space and permissions

### Whisper Model Issues
- Verify model download: Check `~/.cache/whisper/`
- Try smaller model first: `--whisper-model tiny`
- Check PyTorch installation: `python -c "import torch; print(torch.__version__)"`

### Performance Issues
- Use smaller Whisper models for speed
- Increase rate limiting: `--rate-limit 15`
- Process in smaller batches

## 📈 Monitoring & Statistics

### Built-in Statistics
```python
extractor = TranscriptExtractor()
# ... process some videos ...

stats = extractor.get_statistics()
print(f"Success Rate: {stats['success_rate']:.1%}")
print(f"Total Processing Time: {stats['total_processing_time']:.1f}s")
print(f"Whisper Successes: {stats['whisper_successes']}")
```

### Logging
- **INFO**: Normal operations, successful extractions
- **WARNING**: Fallback attempts, minor issues
- **ERROR**: Failed extractions, system errors
- **DEBUG**: Detailed processing information (use `--verbose`)

## 🔮 Future Enhancements

- Support for additional video platforms (Vimeo, etc.)
- Cloud-based transcription services integration
- Advanced audio processing and enhancement
- Machine learning-based quality assessment
- Plugin architecture for custom extraction methods

## 📚 Additional Resources

- **Source Code**: `scripts/corpus_tools/transcript_extractor.py`
- **Data Structures**: `scripts/corpus_tools/extraction_result.py`
- **Command Line**: `scripts/corpus_tools/transcript_extractor_cli.py`
- **Unit Tests**: `tests/test_transcript_extraction_infrastructure.py`

## 🤝 Contributing

This infrastructure is designed to be:
- **Framework agnostic**: Works with any experiment structure
- **Extensible**: Easy to add new extraction methods
- **Maintainable**: Clean code with comprehensive testing
- **Documented**: Clear interfaces and examples

For questions or issues, check the error messages and logging output first, then refer to the source code documentation.

---

**Version**: 2.0.0  
**Last Updated**: 2025-08-21  
**Status**: Production Ready