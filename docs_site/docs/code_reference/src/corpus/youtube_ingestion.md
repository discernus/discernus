# Youtube Ingestion

**Module:** `src.corpus.youtube_ingestion`
**File:** `/Volumes/dev/discernus/src/corpus/youtube_ingestion.py`
**Package:** `corpus`

YouTube Transcript Extraction for Intelligent Corpus Ingestion

Extends the corpus ingestion service to handle YouTube videos with transcripts,
particularly useful for speeches, debates, and addresses across any domain.

## Dependencies

- `dataclasses`
- `datetime`
- `hashlib`
- `intelligent_ingestion`
- `json`
- `os`
- `pathlib`
- `re`
- `typing`
- `youtube_transcript_api`
- `youtube_transcript_api.formatters`
- `yt_dlp`

## Table of Contents

### Classes
- [YouTubeVideoInfo](#youtubevideoinfo)
- [YouTubeTranscriptExtractor](#youtubetranscriptextractor)
- [YouTubeCorpusIngestionService](#youtubecorpusingestionservice)

## Classes

### YouTubeVideoInfo

Container for YouTube video metadata

#### Methods

##### `__post_init__`
```python
__post_init__(self)
```

---

### YouTubeTranscriptExtractor

Extract transcripts and metadata from YouTube videos

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `extract_video_id`
```python
extract_video_id(self, url: str) -> Optional[str]
```

Extract YouTube video ID from various URL formats

##### `get_video_info`
```python
get_video_info(self, video_id: str) -> [YouTubeVideoInfo](src/corpus/youtube_ingestion.md#youtubevideoinfo)
```

Get video metadata using yt-dlp if available

##### `get_transcript`
```python
get_transcript(self, video_id: str, languages: List[str]) -> Optional[str]
```

Extract transcript from YouTube video

##### `clean_transcript`
```python
clean_transcript(self, transcript: str) -> str
```

Clean and format transcript text

---

### YouTubeCorpusIngestionService
*Inherits from: [IntelligentIngestionService](src/corpus/intelligent_ingestion.md#intelligentingestionservice)*

Extended ingestion service with YouTube transcript support

#### Methods

##### `__init__`
```python
__init__(self, corpus_registry, confidence_threshold: float)
```

##### `ingest_youtube_video`
```python
ingest_youtube_video(self, url: str, output_dir: str) -> Dict[Any]
```

Ingest a single YouTube video

##### `ingest_youtube_playlist`
```python
ingest_youtube_playlist(self, playlist_url: str, output_dir: str) -> Dict[Any]
```

Ingest all videos from a YouTube playlist

##### `_process_youtube_file`
```python
_process_youtube_file(self, file_path: Path, video_info: [YouTubeVideoInfo](src/corpus/youtube_ingestion.md#youtubevideoinfo), output_dir: Path) -> Dict[Any]
```

Process YouTube transcript file with enhanced metadata

##### `_extract_youtube_metadata`
```python
_extract_youtube_metadata(self, content: str, video_info: [YouTubeVideoInfo](src/corpus/youtube_ingestion.md#youtubevideoinfo)) -> [ExtractedMetadata](src/corpus/intelligent_ingestion.md#extractedmetadata)
```

Extract metadata with YouTube video context

##### `_check_speaker_conflict`
```python
_check_speaker_conflict(self, llm_speaker: str, youtube_title: str) -> bool
```

Check if LLM speaker conflicts with YouTube title patterns

##### `_extract_speaker_from_youtube`
```python
_extract_speaker_from_youtube(self, channel: str, content: str) -> str
```

Try to identify the actual speaker from channel name and content

##### `_classify_youtube_content`
```python
_classify_youtube_content(self, title: str, content: str) -> str
```

Classify YouTube content type

##### `_generate_youtube_text_id`
```python
_generate_youtube_text_id(self, metadata: [ExtractedMetadata](src/corpus/intelligent_ingestion.md#extractedmetadata), video_info: [YouTubeVideoInfo](src/corpus/youtube_ingestion.md#youtubevideoinfo)) -> str
```

Generate semantic text ID for YouTube content

---

*Generated on 2025-06-21 18:56:11*