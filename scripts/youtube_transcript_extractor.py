#!/usr/bin/env python3
"""
YouTube Transcript Extractor for APDES Corpus Collection

Extracts transcripts and metadata from YouTube videos, particularly useful for:
- Political speeches and addresses
- Campaign rallies and events
- Congressional hearings and debates
- Press conferences and policy announcements

Based on the Discernus YouTube Transcript Intelligent Ingestion Service (June 2025)
Modernized for APDES corpus collection requirements.

Usage:
    python scripts/youtube_transcript_extractor.py <youtube_url> [options]

Example:
    python scripts/youtube_transcript_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID" -o /path/to/output
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import hashlib

# Check for required dependencies
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


@dataclass
class TranscriptExtractionResult:
    """Result container for transcript extraction"""
    success: bool
    video_info: Optional[YouTubeVideoInfo]
    transcript_text: Optional[str]
    language: Optional[str]
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class YouTubeTranscriptExtractor:
    """Extract transcripts and metadata from YouTube videos"""
    
    def __init__(self):
        if not YOUTUBE_TRANSCRIPT_AVAILABLE:
            raise ImportError(
                "youtube-transcript-api not available. Install with: pip install youtube-transcript-api"
            )
        self.api = YouTubeTranscriptApi()
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})',
            r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def get_video_metadata(self, video_id: str) -> YouTubeVideoInfo:
        """Get video metadata using yt-dlp if available"""
        video_info = YouTubeVideoInfo(video_id=video_id)
        
        if not YT_DLP_AVAILABLE:
            print("⚠️  yt-dlp not available. Limited metadata will be extracted.")
            return video_info
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extractaudio': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
                
                video_info.title = info.get('title')
                video_info.channel = info.get('uploader') or info.get('channel')
                video_info.description = info.get('description')
                video_info.duration = info.get('duration')
                video_info.view_count = info.get('view_count')
                video_info.like_count = info.get('like_count')
                
                # Format upload date
                upload_date = info.get('upload_date')
                if upload_date:
                    try:
                        date_obj = datetime.strptime(upload_date, '%Y%m%d')
                        video_info.upload_date = date_obj.strftime('%Y-%m-%d')
                    except:
                        video_info.upload_date = upload_date
                        
        except Exception as e:
            print(f"⚠️  Could not extract enhanced metadata: {e}")
        
        return video_info
    
    def get_transcript(self, video_id: str, languages: List[str] = ['en']) -> Tuple[Optional[str], Optional[str]]:
        """Extract transcript from YouTube video"""
        try:
            # Try to get transcript in preferred languages
            transcript_list = self.api.list(video_id)
            
            # First try manual transcripts in preferred languages
            for lang in languages:
                try:
                    transcript = transcript_list.find_manually_created_transcript([lang])
                    transcript_data = transcript.fetch()
                    formatter = TextFormatter()
                    text = formatter.format_transcript(transcript_data)
                    return self._clean_transcript(text), lang
                except:
                    continue
            
            # Then try auto-generated transcripts in preferred languages
            for lang in languages:
                try:
                    transcript = transcript_list.find_generated_transcript([lang])
                    transcript_data = transcript.fetch()
                    formatter = TextFormatter()
                    text = formatter.format_transcript(transcript_data)
                    return self._clean_transcript(text), f"{lang} (auto-generated)"
                except:
                    continue
            
            # Finally, try any available transcript
            try:
                available_transcripts = list(transcript_list)
                if available_transcripts:
                    transcript = available_transcripts[0]
                    transcript_data = transcript.fetch()
                    formatter = TextFormatter()
                    text = formatter.format_transcript(transcript_data)
                    lang_code = transcript.language_code
                    auto_label = " (auto-generated)" if transcript.is_generated else ""
                    return self._clean_transcript(text), f"{lang_code}{auto_label}"
            except:
                pass
                
            return None, None
            
        except Exception as e:
            print(f"❌ Error extracting transcript: {e}")
            return None, None
    
    def _clean_transcript(self, text: str) -> str:
        """Clean and format transcript text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Remove common transcript artifacts
        text = re.sub(r'\[.*?\]', '', text)  # Remove [Music], [Applause], etc.
        text = re.sub(r'\(.*?\)', '', text)  # Remove (inaudible), etc.
        
        # Clean up spacing
        text = text.strip()
        text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
        
        return text
    
    def extract_from_url(self, url: str, languages: List[str] = ['en']) -> TranscriptExtractionResult:
        """Complete transcript extraction workflow"""
        
        # Extract video ID
        video_id = self.extract_video_id(url)
        if not video_id:
            return TranscriptExtractionResult(
                success=False,
                video_info=None,
                transcript_text=None,
                language=None,
                error_message="Could not extract video ID from URL"
            )
        
        print(f"🎬 Processing video ID: {video_id}")
        
        # Get video metadata
        try:
            video_info = self.get_video_metadata(video_id)
            print(f"📹 Title: {video_info.title or 'Unknown'}")
            print(f"📺 Channel: {video_info.channel or 'Unknown'}")
            print(f"📅 Upload date: {video_info.upload_date or 'Unknown'}")
        except Exception as e:
            print(f"⚠️  Metadata extraction failed: {e}")
            video_info = YouTubeVideoInfo(video_id=video_id)
        
        # Extract transcript
        print("📝 Extracting transcript...")
        transcript_text, language = self.get_transcript(video_id, languages)
        
        if not transcript_text:
            return TranscriptExtractionResult(
                success=False,
                video_info=video_info,
                transcript_text=None,
                language=None,
                error_message="No transcript available for this video"
            )
        
        print(f"✅ Transcript extracted ({len(transcript_text)} characters, language: {language})")
        
        # Create metadata
        metadata = {
            "extraction_date": datetime.now().isoformat(),
            "transcript_length": len(transcript_text),
            "source": "youtube_transcript_api",
            "video_url": url,
            "processing_notes": []
        }
        
        if YT_DLP_AVAILABLE:
            metadata["processing_notes"].append("Enhanced metadata extracted with yt-dlp")
        else:
            metadata["processing_notes"].append("Basic metadata only (yt-dlp not available)")
        
        return TranscriptExtractionResult(
            success=True,
            video_info=video_info,
            transcript_text=transcript_text,
            language=language,
            metadata=metadata
        )


def generate_filename(video_info: YouTubeVideoInfo, transcript_result: TranscriptExtractionResult) -> str:
    """Generate appropriate filename for the extracted content"""
    
    # Base filename from title if available
    if video_info.title:
        # Clean title for filename
        clean_title = re.sub(r'[^\w\s-]', '', video_info.title)
        clean_title = re.sub(r'[-\s]+', '_', clean_title)
        clean_title = clean_title.lower().strip('_')[:50]  # Limit length
    else:
        clean_title = "unknown_title"
    
    # Add date if available
    date_part = ""
    if video_info.upload_date:
        try:
            date_obj = datetime.strptime(video_info.upload_date, '%Y-%m-%d')
            date_part = f"_{date_obj.strftime('%Y_%m_%d')}"
        except:
            date_part = f"_{video_info.upload_date.replace('-', '_')}"
    
    # Add video ID for uniqueness
    video_id_part = f"_{video_info.video_id[:8]}"
    
    return f"{clean_title}{date_part}{video_id_part}.txt"


def save_results(result: TranscriptExtractionResult, output_dir: Path, save_metadata: bool = True):
    """Save extraction results to files"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not result.success:
        print(f"❌ Cannot save results: {result.error_message}")
        return
    
    # Generate filename
    filename = generate_filename(result.video_info, result)
    
    # Save transcript
    transcript_file = output_dir / filename
    with open(transcript_file, 'w', encoding='utf-8') as f:
        # Write header with basic info
        f.write(f"# {result.video_info.title or 'YouTube Video Transcript'}\n")
        f.write(f"# Channel: {result.video_info.channel or 'Unknown'}\n")
        f.write(f"# Upload Date: {result.video_info.upload_date or 'Unknown'}\n")
        f.write(f"# Video URL: {result.video_info.url}\n")
        f.write(f"# Language: {result.language or 'Unknown'}\n")
        f.write(f"# Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n" + "="*80 + "\n\n")
        f.write(result.transcript_text)
    
    print(f"📄 Transcript saved: {transcript_file}")
    
    # Save metadata if requested
    if save_metadata:
        metadata_file = output_dir / f"{filename.replace('.txt', '_metadata.json')}"
        
        full_metadata = {
            "video_info": asdict(result.video_info),
            "extraction_info": {
                "language": result.language,
                "success": result.success,
                "transcript_length": len(result.transcript_text) if result.transcript_text else 0
            },
            "processing_metadata": result.metadata
        }
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(full_metadata, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Metadata saved: {metadata_file}")


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Transcript Extractor for APDES Corpus Collection",
        epilog="Example: python scripts/youtube_transcript_extractor.py 'https://www.youtube.com/watch?v=VIDEO_ID' -o ./output"
    )
    
    parser.add_argument(
        "url",
        help="YouTube video URL (supports youtube.com/watch, youtu.be, etc.)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        help="Output directory for results (default: ./youtube_extractions_TIMESTAMP)"
    )
    
    parser.add_argument(
        "--languages", "-l",
        nargs="+",
        default=["en"],
        help="Preferred transcript languages (default: en)"
    )
    
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Skip saving metadata JSON file"
    )
    
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check dependencies and exit"
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    if args.check_deps:
        print("🔍 Checking dependencies:")
        print(f"  youtube-transcript-api: {'✅ Available' if YOUTUBE_TRANSCRIPT_AVAILABLE else '❌ Missing'}")
        print(f"  yt-dlp: {'✅ Available' if YT_DLP_AVAILABLE else '❌ Missing (optional)'}")
        
        if not YOUTUBE_TRANSCRIPT_AVAILABLE:
            print("\n📦 To install missing dependencies:")
            print("  pip install youtube-transcript-api")
            print("  pip install yt-dlp  # Optional, for enhanced metadata")
        
        return
    
    # Validate dependencies
    if not YOUTUBE_TRANSCRIPT_AVAILABLE:
        print("❌ Required dependency missing: youtube-transcript-api")
        print("📦 Install with: pip install youtube-transcript-api")
        return 1
    
    # Set default output directory
    if not args.output_dir:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_dir = Path(f"./youtube_extractions_{timestamp}")
    
    print(f"🎯 YouTube Transcript Extractor for APDES")
    print(f"📋 URL: {args.url}")
    print(f"📁 Output: {args.output_dir}")
    print(f"🌐 Languages: {', '.join(args.languages)}")
    print("-" * 60)
    
    # Initialize extractor
    try:
        extractor = YouTubeTranscriptExtractor()
    except ImportError as e:
        print(f"❌ Failed to initialize extractor: {e}")
        return 1
    
    # Extract transcript
    result = extractor.extract_from_url(args.url, args.languages)
    
    if result.success:
        # Save results
        save_results(result, args.output_dir, save_metadata=not args.no_metadata)
        
        print("-" * 60)
        print("✅ Extraction completed successfully!")
        print(f"📊 Stats:")
        print(f"  - Transcript length: {len(result.transcript_text):,} characters")
        print(f"  - Language: {result.language}")
        print(f"  - Title: {result.video_info.title or 'Unknown'}")
        print(f"  - Channel: {result.video_info.channel or 'Unknown'}")
        
        if result.video_info.view_count:
            print(f"  - Views: {result.video_info.view_count:,}")
        
        return 0
    else:
        print(f"❌ Extraction failed: {result.error_message}")
        return 1


if __name__ == "__main__":
    exit(main())