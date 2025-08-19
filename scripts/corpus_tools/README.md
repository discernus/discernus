# Corpus Tools

This directory contains specialized tools for extracting and processing corpus data from various sources, particularly for political discourse analysis and social science research.

## Tools

### `youtube_transcript_extractor.py`
**Purpose**: Extract transcripts and metadata from YouTube videos  
**Usage**: `python3 scripts/corpus_tools/youtube_transcript_extractor.py <youtube_url> [options]`  
**Features**:
- Political speeches and campaign rally extraction
- Congressional hearings and debates
- Press conferences and policy announcements
- Metadata extraction (title, date, speaker, context)
- Content-addressed filename generation
- JSON metadata output

**Example**:
```bash
python3 scripts/corpus_tools/youtube_transcript_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" -o /path/to/output
```

**Dependencies**: `youtube-transcript-api`, `yt-dlp`

### `enhanced_transcript_extractor.py`
**Purpose**: Enhanced transcript extraction with additional processing features  
**Usage**: `python3 scripts/corpus_tools/enhanced_transcript_extractor.py <input> [options]`  
**Features**:
- Advanced transcript processing and cleaning
- Speaker identification and segmentation
- Temporal alignment and timestamping
- Enhanced metadata extraction
- Multiple output format support

### `stealth_transcript_scraper.py`
**Purpose**: Advanced transcript scraping with anti-detection capabilities  
**Usage**: `python3 scripts/corpus_tools/stealth_transcript_scraper.py <target> [options]`  
**Features**:
- Robust scraping for difficult-to-access content
- Rate limiting and respectful crawling
- Multiple extraction strategies
- Fallback mechanisms for various platforms
- Advanced error handling and retry logic

### `download_github_corpora.py`
**Purpose**: Download and organize corpus data from GitHub repositories  
**Usage**: `python3 scripts/corpus_tools/download_github_corpora.py <repo_url> [options]`  
**Features**:
- Automated corpus collection from GitHub
- Repository structure preservation
- Metadata extraction and organization
- Batch processing capabilities

## Documentation

### `YOUTUBE_EXTRACTION_GUIDE.md`
**Purpose**: Comprehensive guide for YouTube transcript extraction  
**Content**:
- Step-by-step extraction procedures
- Best practices for political content
- Troubleshooting common issues
- Legal and ethical considerations
- Quality assurance guidelines

## Integration Status

❌ **NOT INTEGRATED** - These tools are currently **NOT INTEGRATED** into the main Discernus pipeline and are provided for standalone corpus preparation use cases.

## Use Cases

1. **Political Discourse Research**: Extract speeches, debates, and political content
2. **Corpus Preparation**: Build research corpora from online video sources  
3. **Data Collection**: Gather transcripts for computational social science
4. **Research Reproducibility**: Standardized extraction with provenance tracking

## Target Content Types

- **Political Speeches**: Campaign rallies, policy addresses, inaugural speeches
- **Congressional Content**: Hearings, committee meetings, floor debates
- **Media Appearances**: Press conferences, interviews, town halls
- **Academic Content**: Lectures, panels, research presentations

## Output Format

All tools generate:
- **Text Files**: Clean transcript content with content-addressed filenames
- **JSON Metadata**: Structured metadata including speaker, date, context, source
- **Provenance Data**: Extraction timestamp, tool version, source URL
- **Quality Metrics**: Confidence scores, completeness indicators

## Dependencies

- `youtube-transcript-api`: YouTube transcript extraction
- `yt-dlp`: Video metadata and download capabilities  
- `requests`: HTTP requests for web scraping
- `beautifulsoup4`: HTML parsing (for some extractors)
- Standard Python libraries (json, pathlib, datetime, etc.)

## Installation

```bash
pip install youtube-transcript-api yt-dlp requests beautifulsoup4
```

## Ethical Guidelines

These tools are designed for academic research and must be used in compliance with:
- Platform terms of service
- Copyright and fair use laws
- Research ethics guidelines
- Data privacy regulations
- Respectful crawling practices (rate limiting, robots.txt compliance)