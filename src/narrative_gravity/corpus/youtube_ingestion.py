#!/usr/bin/env python3
"""
YouTube Transcript Extraction for Intelligent Corpus Ingestion

Extends the corpus ingestion service to handle YouTube videos with transcripts,
particularly useful for speeches, debates, and addresses across any domain.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import hashlib

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter
    YOUTUBE_TRANSCRIPT_AVAILABLE = True
except ImportError:
    YOUTUBE_TRANSCRIPT_AVAILABLE = False

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False

from .intelligent_ingestion import IntelligentIngestionService, ExtractedMetadata, MetadataExtractor


@dataclass
class YouTubeVideoInfo:
    """Container for YouTube video metadata"""
    video_id: str
    title: Optional[str] = None
    channel: Optional[str] = None
    upload_date: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    url: str = None
    
    def __post_init__(self):
        if self.url is None:
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"


class YouTubeTranscriptExtractor:
    """Extract transcripts and metadata from YouTube videos"""
    
    def __init__(self):
        if not YOUTUBE_TRANSCRIPT_AVAILABLE:
            raise ImportError(
                "youtube-transcript-api not available. Install with: pip install youtube-transcript-api"
            )
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract YouTube video ID from various URL formats"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_info(self, video_id: str) -> YouTubeVideoInfo:
        """Get video metadata using yt-dlp if available"""
        video_info = YouTubeVideoInfo(video_id=video_id)
        
        if YT_DLP_AVAILABLE:
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                    
                    video_info.title = info.get('title')
                    video_info.channel = info.get('uploader') or info.get('channel')
                    video_info.description = info.get('description', '')[:500]  # Truncate description
                    video_info.duration = info.get('duration')
                    video_info.view_count = info.get('view_count')
                    video_info.like_count = info.get('like_count')
                    
                    # Parse upload date
                    upload_date = info.get('upload_date')
                    if upload_date:
                        try:
                            # Convert YYYYMMDD to YYYY-MM-DD
                            video_info.upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
                        except:
                            pass
                            
            except Exception as e:
                print(f"Warning: Could not extract video metadata: {e}")
        
        return video_info
    
    def get_transcript(self, video_id: str, languages: List[str] = ['en']) -> Optional[str]:
        """Extract transcript from YouTube video"""
        try:
            # Try to get transcript in preferred languages
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # First try manually created transcripts
            for lang in languages:
                try:
                    transcript = transcript_list.find_manually_created_transcript([lang])
                    transcript_data = transcript.fetch()
                    formatter = TextFormatter()
                    return formatter.format_transcript(transcript_data)
                except:
                    continue
            
            # Fall back to auto-generated transcripts
            for lang in languages:
                try:
                    transcript = transcript_list.find_generated_transcript([lang])
                    transcript_data = transcript.fetch()
                    formatter = TextFormatter()
                    return formatter.format_transcript(transcript_data)
                except:
                    continue
                    
            return None
            
        except Exception as e:
            print(f"Error extracting transcript: {e}")
            return None
    
    def clean_transcript(self, transcript: str) -> str:
        """Clean and format transcript text"""
        if not transcript:
            return ""
        
        # Remove timestamps and formatting artifacts
        text = re.sub(r'\[\d+:\d+:\d+\]', '', transcript)
        text = re.sub(r'\d+:\d+', '', text)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text


class YouTubeCorpusIngestionService(IntelligentIngestionService):
    """Extended ingestion service with YouTube transcript support"""
    
    def __init__(self, corpus_registry, confidence_threshold: float = 70.0):
        super().__init__(corpus_registry, confidence_threshold)
        self.youtube_extractor = YouTubeTranscriptExtractor()
    
    def ingest_youtube_video(self, url: str, output_dir: str = None) -> Dict[str, Any]:
        """Ingest a single YouTube video"""
        
        # Extract video ID
        video_id = self.youtube_extractor.extract_video_id(url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")
        
        print(f"🎬 Processing YouTube video: {video_id}")
        
        # Get video info
        video_info = self.youtube_extractor.get_video_info(video_id)
        print(f"📺 Title: {video_info.title or 'Unknown'}")
        print(f"📺 Channel: {video_info.channel or 'Unknown'}")
        
        # Extract transcript
        transcript = self.youtube_extractor.get_transcript(video_id)
        if not transcript:
            return {
                "error": "No transcript available for this video",
                "video_id": video_id,
                "video_info": video_info
            }
        
        # Clean transcript
        cleaned_transcript = self.youtube_extractor.clean_transcript(transcript)
        
        # Set up output directory
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"tmp/youtube_ingestion_{timestamp}"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save transcript as text file
        transcript_file = output_path / f"{video_id}_transcript.txt"
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_transcript)
        
        # Process with enhanced metadata extraction
        result = self._process_youtube_file(transcript_file, video_info, output_path)
        
        print(f"✅ Processed transcript ({len(cleaned_transcript)} chars)")
        print(f"📊 Confidence: {result['confidence']:.1f}%")
        
        return result
    
    def ingest_youtube_playlist(self, playlist_url: str, output_dir: str = None) -> Dict[str, Any]:
        """Ingest all videos from a YouTube playlist"""
        # This would require additional implementation with yt-dlp
        # to extract playlist video IDs, then process each one
        raise NotImplementedError("Playlist ingestion not yet implemented")
    
    def _process_youtube_file(self, file_path: Path, video_info: YouTubeVideoInfo, output_dir: Path) -> Dict[str, Any]:
        """Process YouTube transcript file with enhanced metadata"""
        
        # Read transcript content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create enhanced metadata using video info
        metadata = self._extract_youtube_metadata(content, video_info)
        
        result = {
            "filename": file_path.name,
            "file_path": str(file_path),
            "video_id": video_info.video_id,
            "video_url": video_info.url,
            "confidence": metadata.confidence_score,
            "metadata": metadata.__dict__,
            "video_info": video_info.__dict__,
            "content_length": len(content),
            "content_hash": hashlib.sha256(content.encode()).hexdigest()[:16]
        }
        
        # Register in corpus if confidence is high enough
        if metadata.confidence_score >= self.confidence_threshold:
            try:
                text_id = self._generate_youtube_text_id(metadata, video_info)
                if self.registry:  # Check if registry is available (not in dry-run)
                    registration_result = self.registry.register_document(
                        text_id=text_id,
                        file_path=str(file_path),
                        metadata={
                            "title": metadata.title,
                            "author": metadata.author,
                            "date": metadata.date,
                            "document_type": metadata.document_type,
                            "description": metadata.description,
                            "language": metadata.language,
                            "source": "youtube_intelligent_ingestion",
                            "youtube_video_id": video_info.video_id,
                            "youtube_url": video_info.url,
                            "youtube_channel": video_info.channel,
                            "confidence_score": metadata.confidence_score
                        }
                    )
                    result["registration"] = registration_result
                    result["text_id"] = text_id
            except Exception as e:
                result["registration_error"] = str(e)
        
        # Save result
        result_file = output_dir / f"{video_info.video_id}_result.json"
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        return result
    
    def _extract_youtube_metadata(self, content: str, video_info: YouTubeVideoInfo) -> ExtractedMetadata:
        """Extract metadata with YouTube video context"""
        
        # Use LLM extraction but enhance with video metadata
        metadata = self.extractor.extract_metadata(content, f"{video_info.video_id}_transcript.txt")
        
        # Cross-validate speaker identification with YouTube title
        if metadata.author and video_info.title:
            potential_conflict = self._check_speaker_conflict(metadata.author, video_info.title)
            if potential_conflict:
                metadata.confidence_score -= 15
                metadata.extraction_notes.append(
                    f"POTENTIAL SPEAKER CONFLICT: LLM identified '{metadata.author}' but YouTube title '{video_info.title}' suggests different speaker"
                )
                print(f"⚠️  Speaker identification conflict detected!")
                print(f"   LLM identified: {metadata.author}")
                print(f"   YouTube title: {video_info.title}")
        
        # Enhance with YouTube metadata
        if not metadata.title and video_info.title:
            metadata.title = video_info.title
        
        if not metadata.author and video_info.channel:
            # Try to extract speaker from channel name or content
            metadata.author = self._extract_speaker_from_youtube(video_info.channel, content)
        
        if not metadata.date and video_info.upload_date:
            metadata.date = video_info.upload_date
        
        if not metadata.document_type:
            metadata.document_type = self._classify_youtube_content(video_info.title or "", content)
        
        if not metadata.description:
            metadata.description = f"YouTube video: {video_info.title or 'Persuasive discourse'}"
        
        # Boost confidence for YouTube videos with good metadata
        if video_info.title and video_info.channel and video_info.upload_date:
            metadata.confidence_score = min(metadata.confidence_score + 10, 100)
        
        metadata.extraction_notes.append("Enhanced with YouTube metadata")
        
        return metadata
    
    def _check_speaker_conflict(self, llm_speaker: str, youtube_title: str) -> bool:
        """Check if LLM speaker conflicts with YouTube title patterns"""
        
        # Extract potential speakers from YouTube title
        title_patterns = [
            r'(President|Governor|Senator|Mayor|Rep\.|Sen\.) ([A-Z][a-z]+)',
            r'Gov\s+([A-Z][a-z]+)',  # "Gov Perry" pattern
            r'([A-Z][a-z]+) (speech|address|remarks)',
        ]
        
        youtube_speakers = []
        for pattern in title_patterns:
            matches = re.findall(pattern, youtube_title, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    youtube_speakers.extend([part.strip() for part in match if part.strip() and len(part.strip()) > 2])
                else:
                    youtube_speakers.append(match.strip())
        
        if not youtube_speakers:
            return False  # No conflict if we can't extract speaker from title
        
        # Check if LLM speaker shares any name parts with YouTube speakers
        llm_name_parts = set(llm_speaker.lower().split())
        for youtube_speaker in youtube_speakers:
            youtube_name_parts = set(youtube_speaker.lower().split())
            if llm_name_parts & youtube_name_parts:  # Any overlap
                return False  # No conflict
        
        return True  # Conflict detected
    
    def _extract_speaker_from_youtube(self, channel: str, content: str) -> str:
        """Try to identify the actual speaker from channel name and content"""
        
        # Enhanced content analysis for speaker identification
        content_start = content[:2000]  # Analyze more content for better accuracy
        
        # Look for direct speaker identification patterns (most reliable)
        direct_patterns = [
            r'I am ([A-Z][a-z]+ [A-Z][a-z]+)',
            r'My name is ([A-Z][a-z]+ [A-Z][a-z]+)',
            r'I\'m ([A-Z][a-z]+ [A-Z][a-z]+)',
            r'This is ([A-Z][a-z]+ [A-Z][a-z]+)',
            r'([A-Z][a-z]+ [A-Z][a-z]+) speaking',
            r'Thank you.*I\'m ([A-Z][a-z]+ [A-Z][a-z]+)',
        ]
        
        for pattern in direct_patterns:
            match = re.search(pattern, content_start, re.IGNORECASE)
            if match:
                speaker_name = match.group(1)
                # Validate it's a real name (not common words)
                name_parts = speaker_name.split()
                if len(name_parts) >= 2 and all(part.istitle() and len(part) > 1 for part in name_parts):
                    return speaker_name
        
        # Look for political title + name patterns
        title_patterns = [
            r'(Governor|President|Senator|Mayor|Representative) ([A-Z][a-z]+ [A-Z][a-z]+)',
            r'(Gov\.|Pres\.|Sen\.|Rep\.) ([A-Z][a-z]+ [A-Z][a-z]+)',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, content_start)
            if match:
                return f"{match.group(1)} {match.group(2)}"
        
        # If channel contains person's name, use it (but with validation)
        person_patterns = [
            r'([A-Z][a-z]+ [A-Z][a-z]+)',  # First Last
            r'(President [A-Z][a-z]+)',    # President Name
            r'(Senator [A-Z][a-z]+)',     # Senator Name
            r'(Governor [A-Z][a-z]+)',    # Governor Name
        ]
        
        for pattern in person_patterns:
            match = re.search(pattern, channel)
            if match:
                potential_name = match.group(1)
                # Don't use organization names that might match the pattern
                org_words = ['council', 'committee', 'center', 'institute', 'foundation', 'association']
                if not any(org_word in potential_name.lower() for org_word in org_words):
                    return potential_name
        
        return channel  # Fallback to channel name
    
    def _classify_youtube_content(self, title: str, content: str) -> str:
        """Classify YouTube content type"""
        title_lower = title.lower()
        content_lower = content.lower()[:500]
        
        if any(word in title_lower for word in ['speech', 'address', 'remarks']):
            return 'speech'
        elif any(word in title_lower for word in ['debate', 'discussion']):
            return 'debate'
        elif any(word in title_lower for word in ['interview', 'conversation']):
            return 'interview'
        elif any(word in title_lower for word in ['press conference', 'briefing']):
            return 'press_conference'
        elif any(word in content_lower for word in ['thank you', 'fellow americans', 'my fellow']):
            return 'address'
        else:
            return 'video'
    
    def _generate_youtube_text_id(self, metadata: ExtractedMetadata, video_info: YouTubeVideoInfo) -> str:
        """Generate semantic text ID for YouTube content"""
        
        # Extract author part
        author_part = ""
        if metadata.author:
            name_parts = metadata.author.split()
            if name_parts:
                author_part = name_parts[-1].lower()
                author_part = re.sub(r'[^a-z]', '', author_part)
        
        # Use video type
        type_part = metadata.document_type or "video"
        
        # Extract year
        year_part = ""
        if metadata.date:
            try:
                year_part = metadata.date.split('-')[0]
            except:
                pass
        
        # Combine with video ID for uniqueness
        if author_part and year_part:
            return f"{author_part}_{type_part}_{year_part}_{video_info.video_id[:8]}"
        else:
            return f"youtube_{type_part}_{video_info.video_id[:8]}" 