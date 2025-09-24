#!/usr/bin/env python3
"""
Transcript Extractor Infrastructure

This module provides durable, reusable infrastructure for extracting transcripts
from various media sources that can be used across all Discernus projects.
"""

import time
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urlparse

# Import our data structures - handle both direct execution and module import
try:
    from .extraction_result import (
        ExtractionResult, VideoInfo, QualityMetrics,
        YouTubeAPIError, WhisperError, NetworkError, ContentUnavailableError
    )
except ImportError:
    # When running directly, import from current directory
    from extraction_result import (
        ExtractionResult, VideoInfo, QualityMetrics,
        YouTubeAPIError, WhisperError, NetworkError, ContentUnavailableError
    )

# Check for optional dependencies
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YOUTUBE_TRANSCRIPT_AVAILABLE = True
except ImportError:
    YOUTUBE_TRANSCRIPT_AVAILABLE = False

try:
    import whisper
    import torch
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False


class TranscriptExtractor:
    """
    Durable transcript extraction infrastructure for Discernus platform.
    
    This class provides a framework-agnostic, multi-method approach to
    transcript extraction with robust error handling and fallback mechanisms.
    """
    
    def __init__(
        self,
        prefer_method: str = "auto",
        whisper_model: str = "base",
        rate_limit: int = 5,
        retry_attempts: int = 3,
        output_format: str = "both"
    ):
        """
        Initialize the transcript extractor.
        
        Args:
            prefer_method: Preferred extraction method ("youtube", "whisper", "auto")
            whisper_model: Whisper model size ("tiny", "base", "small", "medium", "large")
            rate_limit: Delay between requests in seconds
            retry_attempts: Number of retry attempts for failed extractions
            output_format: Output format ("txt", "json", "both")
        """
        self.prefer_method = prefer_method
        self.whisper_model = whisper_model
        self.rate_limit = rate_limit
        self.retry_attempts = retry_attempts
        self.output_format = output_format
        
        # Initialize logging
        self.logger = self._setup_logging()
        
        # Initialize extraction methods
        self.youtube_extractor = self._init_youtube_extractor()
        self.whisper_extractor = self._setup_whisper()
        
        # Track extraction statistics
        self.stats = {
            "total_attempts": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "youtube_api_successes": 0,
            "whisper_successes": 0,
            "total_processing_time": 0.0
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the extractor"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _init_youtube_extractor(self):
        """Initialize YouTube transcript extractor if available"""
        if not YOUTUBE_TRANSCRIPT_AVAILABLE:
            self.logger.warning("YouTube Transcript API not available")
            return None
        
        try:
            return YouTubeTranscriptApi()
        except Exception as e:
            self.logger.error(f"Failed to initialize YouTube API: {e}")
            return None
    
    def _setup_whisper(self):
        """Set up Whisper model if available"""
        if not WHISPER_AVAILABLE:
            self.logger.warning("Whisper not available")
            return None
        
        try:
            self.logger.info(f"Loading Whisper model: {self.whisper_model}")
            model = whisper.load_model(self.whisper_model)
            self.logger.info(f"Whisper {self.whisper_model} model loaded successfully")
            return model
        except Exception as e:
            self.logger.error(f"Failed to load Whisper model: {e}")
            return None
    
    def extract_from_url(
        self,
        url: str,
        output_dir: Path,
        languages: List[str] = None,
        experiment_context: Optional[str] = None
    ) -> ExtractionResult:
        """
        Extract transcript from a media URL.
        
        Args:
            url: Media source URL
            output_dir: Output directory for results
            languages: Preferred languages (default: ["en"])
            experiment_context: Optional experiment context for provenance
            
        Returns:
            ExtractionResult with complete extraction information
        """
        start_time = time.time()
        self.stats["total_attempts"] += 1
        
        print(f"🎯 Starting transcript extraction from: {url}")
        self.logger.info(f"Starting transcript extraction from: {url}")
        
        try:
            # Extract video information
            print("📹 Extracting video information...")
            video_info = self._extract_video_info(url)
            print(f"   Video ID: {video_info.video_id}")
            
            # Attempt extraction based on preferred method
            if self.prefer_method == "youtube" or self.prefer_method == "auto":
                print("🌐 Attempting YouTube transcript extraction...")
                result = self._try_youtube_extraction(url, video_info, languages)
                if result.success:
                    print("✅ YouTube extraction successful!")
                    self.stats["youtube_api_successes"] += 1
                    return self._finalize_result(result, output_dir, start_time, experiment_context)
                else:
                    print(f"❌ YouTube extraction failed: {result.error_message}")
            
            # Fall back to Whisper if YouTube failed or not preferred
            if self.whisper_extractor and (self.prefer_method == "whisper" or not result.success):
                print("🎤 Attempting Whisper transcription...")
                self.logger.info("Attempting Whisper fallback")
                result = self._try_whisper_extraction(url, video_info, languages)
                if result.success:
                    print("✅ Whisper transcription successful!")
                    self.stats["whisper_successes"] += 1
                    return self._finalize_result(result, output_dir, start_time, experiment_context)
                else:
                    print(f"❌ Whisper transcription failed: {result.error_message}")
            
            # If we get here, both methods failed
            print("💥 All extraction methods failed")
            return self._create_failure_result(
                url, video_info, "All extraction methods failed", "extraction_failed"
            )
            
        except Exception as e:
            self.logger.error(f"Unexpected error during extraction: {e}")
            return self._create_failure_result(
                url, VideoInfo(video_id="unknown"), str(e), "unexpected_error"
            )
        finally:
            processing_time = time.time() - start_time
            self.stats["total_processing_time"] += processing_time
    
    def _extract_video_info(self, url: str) -> VideoInfo:
        """Extract video information from URL"""
        video_id = self._extract_video_id(url)
        return VideoInfo(video_id=video_id, url=url)
    
    def _extract_video_id(self, url: str) -> str:
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
        
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def _try_youtube_extraction(
        self, url: str, video_info: VideoInfo, languages: List[str]
    ) -> ExtractionResult:
        """Attempt YouTube API extraction"""
        if not self.youtube_extractor:
            return self._create_failure_result(
                url, video_info, "YouTube API not available", "api_unavailable"
            )
        
        try:
            self.logger.info("Attempting YouTube transcript extraction")
            
            # Extract transcript using YouTube API
            transcript_data = self.youtube_extractor.fetch(video_info.video_id)
            
            # Convert to text
            transcript_text = self._convert_youtube_transcript_to_text(transcript_data)
            
            # Create quality metrics
            quality_metrics = QualityMetrics(
                transcript_length=len(transcript_text),
                word_count=len(transcript_text.split()),
                completeness_score=0.95,  # YouTube transcripts are usually complete
                confidence_score=90.0,    # High confidence for official transcripts
                extraction_method="youtube_api",
                language_detected=languages[0] if languages else "en"
            )
            
            return ExtractionResult(
                success=True,
                url=url,
                video_info=video_info,
                transcript_text=transcript_text,
                language=languages[0] if languages else "en",
                quality_metrics=quality_metrics,
                fallback_attempted=False,
                fallback_success=False
            )
            
        except Exception as e:
            error_type = self._classify_youtube_error(e)
            return self._create_failure_result(
                url, video_info, str(e), error_type
            )
    
    def _try_whisper_extraction(
        self, url: str, video_info: VideoInfo, languages: List[str]
    ) -> ExtractionResult:
        """Attempt Whisper-based extraction"""
        if not self.whisper_extractor:
            return self._create_failure_result(
                url, video_info, "Whisper not available", "whisper_unavailable"
            )
        
        try:
            print("🎤 Starting Whisper transcription...")
            self.logger.info("Attempting Whisper transcription")
            
            # Download audio
            print("📥 Downloading audio from YouTube...")
            audio_path = self._download_audio(url)
            if not audio_path:
                print("❌ Audio download failed")
                return self._create_failure_result(
                    url, video_info, "Failed to download audio", "audio_download_failed"
                )
            
            print(f"✅ Audio downloaded: {audio_path.name} ({audio_path.stat().st_size:,} bytes)")
            
            # Transcribe with Whisper
            print("🎯 Transcribing with Whisper...")
            result = self.whisper_extractor.transcribe(
                str(audio_path),
                language=languages[0] if languages and languages[0] != 'en' else None
            )
            
            transcript_text = result["text"].strip()
            print(f"✅ Transcription complete: {len(transcript_text):,} characters")
            
            # Create quality metrics
            quality_metrics = QualityMetrics(
                transcript_length=len(transcript_text),
                word_count=len(transcript_text.split()),
                completeness_score=0.85,  # Whisper may miss some content
                confidence_score=75.0,    # Moderate confidence for AI transcription
                extraction_method="whisper",
                language_detected=result.get("language", "en"),
                whisper_model_used=self.whisper_model
            )
            
            # Clean up audio file
            print("🧹 Cleaning up audio file...")
            audio_path.unlink()
            
            return ExtractionResult(
                success=True,
                url=url,
                video_info=video_info,
                transcript_text=transcript_text,
                language=languages[0] if languages else "en",
                quality_metrics=quality_metrics,
                fallback_attempted=True,
                fallback_success=True
            )
            
        except Exception as e:
            print(f"💥 Whisper transcription failed: {e}")
            return self._create_failure_result(
                url, video_info, f"Whisper transcription failed: {e}", "whisper_error"
            )
    
    def _download_audio(self, url: str) -> Optional[Path]:
        """Download audio from YouTube video"""
        if not YT_DLP_AVAILABLE:
            print("❌ yt-dlp not available for audio download")
            self.logger.error("yt-dlp not available for audio download")
            return None
        
        try:
            import tempfile
            
            print("📁 Creating temporary file for audio...")
            # Create a temporary file that won't be auto-deleted
            temp_fd, temp_path = tempfile.mkstemp(suffix='.wav')
            audio_path = Path(temp_path)
            
            # Close the file descriptor since yt-dlp will create its own file
            import os
            os.close(temp_fd)
            
            print("⬇️  Downloading audio with yt-dlp...")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(audio_path.with_suffix('.%(ext)s')),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }],
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Check if the file was created
            if audio_path.exists() and audio_path.stat().st_size > 0:
                print(f"✅ Audio file created: {audio_path.name}")
                return audio_path
            
            # Sometimes yt-dlp creates files with different extensions
            # Look for any audio file with our base name
            print("🔍 Looking for audio file with different extension...")
            parent_dir = audio_path.parent
            base_name = audio_path.stem
            
            for ext in ['.wav', '.mp3', '.m4a', '.webm']:
                potential_file = parent_dir / f"{base_name}{ext}"
                if potential_file.exists() and potential_file.stat().st_size > 0:
                    print(f"✅ Found audio file: {potential_file.name}")
                    return potential_file
            
            print("❌ No audio file was created by yt-dlp")
            self.logger.error("No audio file was created by yt-dlp")
            return None
                
        except Exception as e:
            print(f"💥 Audio download failed: {e}")
            self.logger.error(f"Audio download failed: {e}")
            return None
    
    def _convert_youtube_transcript_to_text(self, transcript_data: List[Dict]) -> str:
        """Convert YouTube transcript data to plain text"""
        text_parts = []
        for segment in transcript_data:
            text_parts.append(segment.get('text', ''))
        
        return ' '.join(text_parts)
    
    def _classify_youtube_error(self, error: Exception) -> str:
        """Classify YouTube API errors for appropriate handling"""
        error_str = str(error).lower()
        
        if "rate limit" in error_str or "blocked" in error_str:
            return "api_rate_limit"
        elif "unavailable" in error_str or "private" in error_str:
            return "content_unavailable"
        elif "network" in error_str or "connection" in error_str:
            return "network_error"
        else:
            return "api_error"
    
    def _create_failure_result(
        self, url: str, video_info: VideoInfo, error_message: str, error_type: str
    ) -> ExtractionResult:
        """Create a failure result with appropriate error information"""
        return ExtractionResult(
            success=False,
            url=url,
            video_info=video_info,
            error_type=error_type,
            error_message=error_message,
            fallback_attempted=self.prefer_method == "auto"
        )
    
    def _finalize_result(
        self,
        result: ExtractionResult,
        output_dir: Path,
        start_time: float,
        experiment_context: Optional[str]
    ) -> ExtractionResult:
        """Finalize the extraction result with file output and metadata"""
        try:
            print("💾 Finalizing extraction result...")
            
            # Generate output filename
            filename = self._generate_filename(result.video_info, result)
            result.output_filename = filename
            result.output_directory = output_dir
            print(f"📝 Output filename: {filename}")
            
            # Set processing time
            result.processing_time_seconds = time.time() - start_time
            print(f"⏱️  Total processing time: {result.processing_time_seconds:.1f} seconds")
            
            # Save transcript file
            if self.output_format in ["txt", "both"]:
                print("📄 Saving transcript file...")
                self._save_transcript_file(result, output_dir)
            
            # Save metadata file
            if self.output_format in ["json", "both"]:
                print("📊 Saving metadata file...")
                self._save_metadata_file(result, output_dir)
            
            # Update statistics
            self.stats["successful_extractions"] += 1
            
            print(f"✅ Extraction completed successfully: {filename}")
            self.logger.info(f"Extraction completed successfully: {filename}")
            return result
            
        except Exception as e:
            print(f"💥 Failed to save results: {e}")
            self.logger.error(f"Failed to save results: {e}")
            # Return the result even if saving failed
            return result
    
    def _generate_filename(self, video_info: VideoInfo, result: ExtractionResult) -> str:
        """Generate consistent, predictable filename"""
        # Extract date from video info or use current date
        date_str = video_info.upload_date or datetime.now().strftime("%Y-%m-%d")
        
        # Use video ID if title is not available to ensure unique filenames
        if video_info.title and video_info.title != "unknown":
            # Clean title for filename
            title_clean = re.sub(r'[^\w\s-]', '', video_info.title)
            title_clean = re.sub(r'[-\s]+', '_', title_clean).strip('_')
            base_name = title_clean
        else:
            # Use video ID as fallback
            base_name = f"video_{video_info.video_id}"
        
        # Create filename: base_name_date_method.txt
        filename = f"{base_name}_{date_str}_{result.method}.txt"
        return filename
    
    def _save_transcript_file(self, result: ExtractionResult, output_dir: Path):
        """Save transcript to text file with proper formatting"""
        output_dir.mkdir(parents=True, exist_ok=True)
        transcript_file = output_dir / result.output_filename
        
        print(f"📝 Writing transcript to: {transcript_file}")
        with open(transcript_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"# {result.video_info.title or 'YouTube Video Transcript'}\n")
            f.write(f"# Channel: {result.video_info.channel or 'Unknown'}\n")
            f.write(f"# Upload Date: {result.video_info.upload_date or 'Unknown'}\n")
            f.write(f"# Video URL: {result.url}\n")
            f.write(f"# Language: {result.language or 'Unknown'}\n")
            f.write(f"# Extraction Method: {result.method}\n")
            f.write(f"# Confidence: {result.confidence:.1f}%\n")
            if result.quality_metrics.whisper_model_used:
                f.write(f"# Whisper Model: {result.quality_metrics.whisper_model_used}\n")
            f.write(f"# Extracted: {result.extraction_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + "="*80 + "\n\n")
            
            # Write transcript content
            f.write(result.transcript_text)
        
        print(f"✅ Transcript saved: {transcript_file}")
        self.logger.info(f"Transcript saved: {transcript_file}")
    
    def _save_metadata_file(self, result: ExtractionResult, output_dir: Path):
        """Save metadata to JSON file"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate metadata filename
        base_name = result.output_filename.replace('.txt', '')
        metadata_file = output_dir / f"{base_name}_metadata.json"
        
        print(f"📊 Writing metadata to: {metadata_file}")
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write(result.to_json())
        
        print(f"✅ Metadata saved: {metadata_file}")
        self.logger.info(f"Metadata saved: {metadata_file}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get extraction statistics"""
        stats = self.stats.copy()
        if stats["total_attempts"] > 0:
            stats["success_rate"] = stats["successful_extractions"] / stats["total_attempts"]
            stats["average_processing_time"] = stats["total_processing_time"] / stats["total_attempts"]
        return stats
    
    def reset_statistics(self):
        """Reset extraction statistics"""
        self.stats = {
            "total_attempts": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "youtube_api_successes": 0,
            "whisper_successes": 0,
            "total_processing_time": 0.0
        }
