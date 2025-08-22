#!/usr/bin/env python3
"""
Enhanced Transcript Extractor for APDES Corpus Collection

Combines multiple extraction methods for maximum success rate:
1. YouTube transcript API (fastest, good quality)  
2. OpenAI Whisper (highest quality, works on any audio/video)
3. Manual transcript search (web-based official transcripts)

Usage:
    python3 scripts/enhanced_transcript_extractor.py <youtube_url> [options]
"""

import argparse
import json
import os
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

# Import existing YouTube extractor
import sys
sys.path.append('scripts')
from youtube_transcript_extractor import YouTubeTranscriptExtractor, YouTubeVideoInfo, generate_filename, save_results, TranscriptExtractionResult

# Check for Whisper availability
try:
    import whisper
    import torch
    WHISPER_AVAILABLE = True
    print("🎙️  Whisper available for high-quality transcription")
except ImportError:
    WHISPER_AVAILABLE = False
    print("⚠️  Whisper not available - install with: pip install openai-whisper")

# Check for yt-dlp availability  
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False


@dataclass
class EnhancedTranscriptResult:
    """Enhanced result with multiple extraction methods"""
    success: bool
    video_info: Optional[YouTubeVideoInfo]
    transcript_text: Optional[str]
    language: Optional[str]
    extraction_method: Optional[str] = None
    confidence_score: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    whisper_model_used: Optional[str] = None


class EnhancedTranscriptExtractor:
    """Enhanced transcript extractor with multiple fallback methods"""
    
    def __init__(self, whisper_model: str = "base"):
        self.youtube_extractor = YouTubeTranscriptExtractor()
        self.whisper_model = whisper_model
        
        # Load Whisper model if available
        if WHISPER_AVAILABLE:
            print(f"🔄 Loading Whisper model: {whisper_model}")
            try:
                self.whisper = whisper.load_model(whisper_model)
                print(f"✅ Whisper {whisper_model} model loaded successfully")
            except Exception as e:
                print(f"❌ Failed to load Whisper model: {e}")
                self.whisper = None
        else:
            self.whisper = None

    def extract_from_url(self, url: str, languages: List[str] = ['en'], 
                        prefer_whisper: bool = False) -> EnhancedTranscriptResult:
        """
        Extract transcript using multiple methods with intelligent fallback
        
        Priority order:
        1. YouTube transcript API (if not prefer_whisper)
        2. Whisper transcription (if available and prefer_whisper OR API failed)
        3. Return best available result
        """
        
        print(f"🎯 Enhanced Transcript Extraction")
        print(f"📋 URL: {url}")
        print(f"🌐 Languages: {', '.join(languages)}")
        print(f"🎙️  Prefer Whisper: {prefer_whisper}")
        print("-" * 60)
        
        # Extract video info first
        video_id = self.youtube_extractor.extract_video_id(url)
        if not video_id:
            return EnhancedTranscriptResult(
                success=False,
                video_info=None,
                transcript_text=None,
                language=None,
                error_message="Could not extract video ID from URL"
            )
        
        # Get video metadata
        video_info = self.youtube_extractor.get_video_metadata(video_id)
        print(f"🎬 Video: {video_info.title or 'Unknown'}")
        print(f"📺 Channel: {video_info.channel or 'Unknown'}")
        
        # Method 1: Try YouTube transcript API first (unless prefer Whisper)
        youtube_result = None
        if not prefer_whisper:
            print("\n📝 Attempting YouTube transcript extraction...")
            youtube_transcript, youtube_language = self.youtube_extractor.get_transcript(video_id, languages)
            
            if youtube_transcript:
                cleaned_transcript = self.youtube_extractor._clean_transcript(youtube_transcript)
                confidence = self._assess_youtube_confidence(youtube_transcript, youtube_language)
                
                youtube_result = EnhancedTranscriptResult(
                    success=True,
                    video_info=video_info,
                    transcript_text=cleaned_transcript,
                    language=youtube_language,
                    extraction_method="youtube_api",
                    confidence_score=confidence,
                    metadata={
                        "transcript_length": len(cleaned_transcript),
                        "extraction_date": datetime.now().isoformat(),
                        "source": "youtube_transcript_api"
                    }
                )
                print(f"✅ YouTube API success: {len(cleaned_transcript)} chars, confidence: {confidence:.1f}%")
                
                # If confidence is high enough, return YouTube result
                if confidence >= 80:
                    return youtube_result
        
        # Method 2: Try Whisper transcription
        whisper_result = None
        if WHISPER_AVAILABLE and self.whisper:
            print("\n🎙️  Attempting Whisper transcription...")
            whisper_result = self._extract_with_whisper(url, video_info, languages)
            
            if whisper_result and whisper_result.success:
                print(f"✅ Whisper success: {len(whisper_result.transcript_text)} chars, confidence: {whisper_result.confidence_score:.1f}%")
        
        # Choose best result
        if whisper_result and whisper_result.success and youtube_result and youtube_result.success:
            # Both succeeded - choose based on confidence or preference
            if prefer_whisper or whisper_result.confidence_score > youtube_result.confidence_score:
                print(f"🏆 Selected Whisper result (confidence: {whisper_result.confidence_score:.1f}%)")
                return whisper_result
            else:
                print(f"🏆 Selected YouTube API result (confidence: {youtube_result.confidence_score:.1f}%)")  
                return youtube_result
                
        elif whisper_result and whisper_result.success:
            print(f"🏆 Using Whisper result (YouTube failed)")
            return whisper_result
            
        elif youtube_result and youtube_result.success:
            print(f"🏆 Using YouTube API result (Whisper failed/unavailable)")
            return youtube_result
            
        else:
            # Both failed
            return EnhancedTranscriptResult(
                success=False,
                video_info=video_info,
                transcript_text=None,
                language=None,
                error_message="All extraction methods failed",
                metadata={
                    "youtube_attempted": not prefer_whisper,
                    "whisper_attempted": WHISPER_AVAILABLE and self.whisper is not None,
                    "youtube_available": youtube_result is not None,
                    "whisper_available": whisper_result is not None
                }
            )

    def _extract_with_whisper(self, url: str, video_info: YouTubeVideoInfo, 
                             languages: List[str]) -> Optional[EnhancedTranscriptResult]:
        """Extract transcript using Whisper"""
        
        if not WHISPER_AVAILABLE or not self.whisper:
            return None
            
        try:
            # Download audio using yt-dlp
            with tempfile.TemporaryDirectory() as temp_dir:
                audio_path = Path(temp_dir) / f"{video_info.video_id}.wav"
                
                print(f"📥 Downloading audio to: {audio_path}")
                if not self._download_audio(url, audio_path):
                    return EnhancedTranscriptResult(
                        success=False,
                        video_info=video_info,
                        transcript_text=None,
                        language=None,
                        extraction_method="whisper",
                        error_message="Failed to download audio"
                    )
                
                print(f"🎙️  Transcribing with Whisper {self.whisper_model}...")
                
                # Transcribe with Whisper
                result = self.whisper.transcribe(
                    str(audio_path),
                    language=languages[0] if languages and languages[0] != 'en' else None,
                    task="transcribe"
                )
                
                transcript_text = result["text"].strip()
                detected_language = result.get("language", "unknown")
                
                # Calculate confidence (Whisper doesn't provide direct confidence)
                confidence = self._assess_whisper_confidence(result)
                
                return EnhancedTranscriptResult(
                    success=True,
                    video_info=video_info,
                    transcript_text=transcript_text,
                    language=f"{detected_language} (whisper)",
                    extraction_method="whisper",
                    confidence_score=confidence,
                    whisper_model_used=self.whisper_model,
                    metadata={
                        "transcript_length": len(transcript_text),
                        "extraction_date": datetime.now().isoformat(),
                        "source": "openai_whisper",
                        "model": self.whisper_model,
                        "detected_language": detected_language,
                        "segments": len(result.get("segments", []))
                    }
                )
                
        except Exception as e:
            print(f"❌ Whisper extraction failed: {e}")
            return EnhancedTranscriptResult(
                success=False,
                video_info=video_info,
                transcript_text=None,
                language=None,
                extraction_method="whisper",
                error_message=f"Whisper transcription failed: {str(e)}"
            )
    
    def _download_audio(self, url: str, output_path: Path) -> bool:
        """Download audio from YouTube video"""
        
        if not YT_DLP_AVAILABLE:
            print("❌ yt-dlp not available for audio download")
            return False
            
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(output_path.with_suffix('.%(ext)s')),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }],
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            return output_path.exists()
            
        except Exception as e:
            print(f"❌ Audio download failed: {e}")
            return False
    
    def _assess_youtube_confidence(self, transcript: str, language: str) -> float:
        """Assess confidence of YouTube transcript"""
        confidence = 70.0  # Base confidence
        
        # Boost for manual captions
        if language and "auto-generated" not in language.lower():
            confidence += 20
            
        # Boost for reasonable length
        if len(transcript) > 1000:
            confidence += 10
            
        # Reduce for very short transcripts
        if len(transcript) < 500:
            confidence -= 15
            
        return min(confidence, 100.0)
    
    def _assess_whisper_confidence(self, whisper_result: Dict) -> float:
        """Assess confidence of Whisper transcription"""
        confidence = 85.0  # Base confidence (Whisper is generally high quality)
        
        # Check for segments and average logprobs if available
        segments = whisper_result.get("segments", [])
        if segments:
            # Calculate average confidence from segments
            avg_confidence = 0
            for segment in segments:
                if "avg_logprob" in segment:
                    # Convert log probability to confidence (rough approximation)
                    log_prob = segment["avg_logprob"]
                    segment_conf = max(0, min(100, 80 + log_prob * 20))
                    avg_confidence += segment_conf
            
            if len(segments) > 0:
                confidence = avg_confidence / len(segments)
        
        return min(confidence, 100.0)


def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Transcript Extractor with YouTube API and Whisper fallback",
        epilog="Example: python3 scripts/enhanced_transcript_extractor.py 'https://www.youtube.com/watch?v=VIDEO_ID' -o ./output --whisper-model base"
    )
    
    parser.add_argument(
        "url",
        help="YouTube video URL"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        help="Output directory for results (default: ./enhanced_extractions_TIMESTAMP)"
    )
    
    parser.add_argument(
        "--languages", "-l",
        nargs="+",
        default=["en"],
        help="Preferred transcript languages (default: en)"
    )
    
    parser.add_argument(
        "--whisper-model",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help="Whisper model size (default: base)"
    )
    
    parser.add_argument(
        "--prefer-whisper",
        action="store_true",
        help="Prefer Whisper over YouTube API even when both available"
    )
    
    parser.add_argument(
        "--no-metadata",
        action="store_true", 
        help="Skip saving metadata JSON file"
    )
    
    args = parser.parse_args()
    
    # Set default output directory
    if not args.output_dir:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_dir = Path(f"./enhanced_extractions_{timestamp}")
    
    print(f"🎯 Enhanced Transcript Extractor for APDES")
    print(f"📋 URL: {args.url}")
    print(f"📁 Output: {args.output_dir}")
    print(f"🌐 Languages: {', '.join(args.languages)}")
    print(f"🎙️  Whisper Model: {args.whisper_model}")
    print(f"🔄 Prefer Whisper: {args.prefer_whisper}")
    print("=" * 60)
    
    # Initialize extractor
    try:
        extractor = EnhancedTranscriptExtractor(whisper_model=args.whisper_model)
    except Exception as e:
        print(f"❌ Failed to initialize extractor: {e}")
        return 1
    
    # Extract transcript
    result = extractor.extract_from_url(args.url, args.languages, args.prefer_whisper)
    
    if result.success:
        # Save results using existing save function (adapted)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        filename = generate_filename(result.video_info, result)
        
        # Save transcript
        transcript_file = args.output_dir / filename
        with open(transcript_file, 'w', encoding='utf-8') as f:
            # Write enhanced header
            f.write(f"# {result.video_info.title or 'YouTube Video Transcript'}\n")
            f.write(f"# Channel: {result.video_info.channel or 'Unknown'}\n")
            f.write(f"# Upload Date: {result.video_info.upload_date or 'Unknown'}\n")
            f.write(f"# Video URL: {result.video_info.url}\n")
            f.write(f"# Language: {result.language or 'Unknown'}\n")
            f.write(f"# Extraction Method: {result.extraction_method}\n")
            f.write(f"# Confidence: {result.confidence_score:.1f}%\n")
            if result.whisper_model_used:
                f.write(f"# Whisper Model: {result.whisper_model_used}\n")
            f.write(f"# Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n" + "="*80 + "\n\n")
            f.write(result.transcript_text)
        
        print(f"📄 Transcript saved: {transcript_file}")
        
        # Save metadata if requested
        if not args.no_metadata:
            metadata_file = args.output_dir / f"{filename.replace('.txt', '_metadata.json')}"
            
            full_metadata = {
                "video_info": result.video_info.__dict__ if result.video_info else None,
                "extraction_info": {
                    "method": result.extraction_method,
                    "language": result.language,
                    "confidence": result.confidence_score,
                    "success": result.success,
                    "transcript_length": len(result.transcript_text) if result.transcript_text else 0,
                    "whisper_model": result.whisper_model_used
                },
                "processing_metadata": result.metadata or {}
            }
            
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(full_metadata, f, indent=2, ensure_ascii=False)
            
            print(f"📊 Metadata saved: {metadata_file}")
        
        print("=" * 60)
        print("✅ Enhanced extraction completed successfully!")
        print(f"📊 Stats:")
        print(f"  - Method: {result.extraction_method}")
        print(f"  - Transcript length: {len(result.transcript_text):,} characters")
        print(f"  - Language: {result.language}")
        print(f"  - Confidence: {result.confidence_score:.1f}%")
        print(f"  - Title: {result.video_info.title or 'Unknown'}")
        print(f"  - Channel: {result.video_info.channel or 'Unknown'}")
        
        if result.video_info.view_count:
            print(f"  - Views: {result.video_info.view_count:,}")
        
        return 0
    else:
        print(f"❌ Enhanced extraction failed: {result.error_message}")
        if result.metadata:
            print("🔍 Debug info:")
            for key, value in result.metadata.items():
                print(f"  - {key}: {value}")
        return 1


if __name__ == "__main__":
    exit(main())