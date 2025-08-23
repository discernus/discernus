# Audio Processing Workflow for Downloaded YouTube Files

## Overview
This workflow processes manually downloaded YouTube audio files to generate high-quality transcripts using Whisper AI. This approach bypasses YouTube's anti-scraping measures.

## Prerequisites
- Python 3.8+
- Whisper AI (`pip install openai-whisper`)
- FFmpeg (for audio format support)
- Downloaded YouTube audio files

## Workflow Steps

### 1. Download YouTube Audio Files
Use your preferred method to download YouTube audio:
- **yt-dlp** (recommended): `yt-dlp -x --audio-format mp3 [URL]`
- **youtube-dl**: `youtube-dl -x --audio-format mp3 [URL]`
- **Browser extensions** for audio download
- **Manual download** from YouTube Premium

### 2. Organize Audio Files
Place downloaded audio files in a directory structure:
```
downloaded_audio/
├── trump_speech_2021_03_01.mp3
├── trump_rally_2022_06_15.m4a
├── trump_cpac_2023_02_25.wav
└── ...
```

### 3. Process with Whisper
Run the audio processor script:
```bash
python3 scripts/corpus_tools/process_downloaded_audio.py \
    --input-dir /path/to/downloaded_audio \
    --output-dir projects/2d_trump_populism/corpus/post_presidency_2021_2023 \
    --whisper-model base
```

### 4. Review Output
The script generates:
- **Transcripts**: Clean text files in `transcripts/` directory
- **Metadata**: JSON files with speech information in `metadata/` directory
- **Summary**: Processing report in `processing_summary.json`

## Whisper Model Options
- **tiny**: Fastest, lowest quality
- **base**: Good balance of speed/quality (default)
- **small**: Better quality, slower
- **medium**: High quality, slower
- **large**: Best quality, slowest

## Supported Audio Formats
- MP3, WAV, M4A, FLAC, AAC, OGG, OPUS

## Filename Metadata Extraction
The script automatically extracts metadata from filenames:
- **Date patterns**: 2021, 2022, 2023, 2024
- **Event types**: CPAC, rally, ellipse
- **Locations**: Washington DC, CPAC, etc.

## Example Usage

### Basic Processing
```bash
cd /Volumes/code/discernus
python3 scripts/corpus_tools/process_downloaded_audio.py \
    --input-dir ~/Downloads/trump_speeches \
    --output-dir projects/2d_trump_populism/corpus/post_presidency_2021_2023
```

### High-Quality Processing
```bash
python3 scripts/corpus_tools/process_downloaded_audio.py \
    --input-dir ~/Downloads/trump_speeches \
    --output-dir projects/2d_trump_populism/corpus/post_presidency_2021_2023 \
    --whisper-model medium
```

## Benefits of This Approach
1. **Bypasses YouTube blocking** - No more HTTP 403 errors
2. **Higher quality control** - Choose audio format and quality
3. **Batch processing** - Process multiple files at once
4. **Consistent output** - Standardized transcript and metadata format
5. **Offline processing** - No internet dependency after download

## Tips for Best Results
1. **Use high-quality audio** - Better audio = better transcription
2. **Descriptive filenames** - Include date, event, location for metadata
3. **Consistent format** - Use same audio format for batch processing
4. **Monitor processing** - Check logs for any failed transcriptions

## Troubleshooting
- **Audio format issues**: Ensure FFmpeg supports your audio format
- **Memory issues**: Use smaller Whisper models for long audio files
- **Quality issues**: Try larger Whisper models for better accuracy
- **File access**: Ensure script has read/write permissions to directories

