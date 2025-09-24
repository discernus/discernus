#!/usr/bin/env python3
"""
Command Line Interface for Transcript Extraction Infrastructure

This module provides a simple command-line interface for the durable
transcript extraction infrastructure.
"""

import argparse
import sys
from pathlib import Path
from typing import List

# Import our infrastructure - handle both direct execution and module import
try:
    from .transcript_extractor import TranscriptExtractor
except ImportError:
    # When running directly, import from current directory
    from transcript_extractor import TranscriptExtractor


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Durable Transcript Extraction Infrastructure for Discernus",
        epilog="Example: python -m scripts.corpus_tools.transcript_extractor_cli 'https://youtube.com/watch?v=VIDEO_ID' -o ./output"
    )
    
    parser.add_argument(
        "url",
        nargs="?",
        help="Media source URL (YouTube, audio file, etc.)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=Path("./transcript_extractions"),
        help="Output directory for results (default: ./transcript_extractions)"
    )
    
    parser.add_argument(
        "--prefer-method",
        choices=["youtube", "whisper", "auto"],
        default="auto",
        help="Preferred extraction method (default: auto)"
    )
    
    parser.add_argument(
        "--whisper-model",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help="Whisper model size (default: base)"
    )
    
    parser.add_argument(
        "--languages", "-l",
        nargs="+",
        default=["en"],
        help="Preferred languages (default: en)"
    )
    
    parser.add_argument(
        "--rate-limit",
        type=int,
        default=5,
        help="Delay between requests in seconds (default: 5)"
    )
    
    parser.add_argument(
        "--retry-attempts",
        type=int,
        default=3,
        help="Number of retry attempts (default: 3)"
    )
    
    parser.add_argument(
        "--output-format",
        choices=["txt", "json", "both"],
        default="both",
        help="Output format (default: both)"
    )
    
    parser.add_argument(
        "--experiment-context",
        help="Experiment context for provenance tracking"
    )
    
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check dependencies and exit"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Check dependencies if requested
    if args.check_deps:
        check_dependencies()
        return 0
    
    # If checking deps, we don't need a URL
    if args.check_deps:
        return 0
    
    # Set up logging
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    try:
        # Initialize extractor
        extractor = TranscriptExtractor(
            prefer_method=args.prefer_method,
            whisper_model=args.whisper_model,
            rate_limit=args.rate_limit,
            retry_attempts=args.retry_attempts,
            output_format=args.output_format
        )
        
        # Extract transcript
        result = extractor.extract_from_url(
            url=args.url,
            output_dir=args.output_dir,
            languages=args.languages,
            experiment_context=args.experiment_context
        )
        
        # Display results
        display_results(result, extractor)
        
        return 0 if result.success else 1
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Extraction canceled by user")
        return 130
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


def check_dependencies():
    """Check and display dependency status"""
    print("🔍 Checking Transcript Extraction Infrastructure Dependencies")
    print("=" * 60)
    
    # Check YouTube Transcript API
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        print("✅ YouTube Transcript API: Available")
    except ImportError:
        print("❌ YouTube Transcript API: Missing")
        print("   Install with: pip install youtube-transcript-api")
    
    # Check Whisper
    try:
        import whisper
        import torch
        print("✅ OpenAI Whisper: Available")
        print(f"   PyTorch version: {torch.__version__}")
    except ImportError:
        print("❌ OpenAI Whisper: Missing")
        print("   Install with: pip install openai-whisper")
    
    # Check yt-dlp
    try:
        import yt_dlp
        print("✅ yt-dlp: Available")
        print(f"   Version: {yt_dlp.version.__version__}")
    except ImportError:
        print("❌ yt-dlp: Missing")
        print("   Install with: pip install yt-dlp")
    
    # Check FFmpeg (required for audio processing)
    try:
        import subprocess
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg: Available")
        else:
            print("❌ FFmpeg: Not working properly")
    except FileNotFoundError:
        print("❌ FFmpeg: Not found in PATH")
        print("   Install FFmpeg for your platform")
    
    print("\n📋 Summary:")
    print("   - YouTube API: For direct transcript extraction")
    print("   - Whisper: For audio-based transcription fallback")
    print("   - yt-dlp: For audio/video download")
    print("   - FFmpeg: For audio format conversion")


def display_results(result, extractor):
    """Display extraction results in a user-friendly format"""
    print("\n" + "=" * 60)
    
    if result.success:
        print("✅ Transcript Extraction Completed Successfully!")
        print(f"📄 Method: {result.method}")
        print(f"📊 Confidence: {result.confidence:.1f}%")
        print(f"📝 Transcript Length: {result.quality_metrics.transcript_length:,} characters")
        print(f"📚 Word Count: {result.quality_metrics.word_count:,}")
        print(f"🌐 Language: {result.language}")
        
        if result.output_filename:
            print(f"💾 Files Created:")
            print(f"   - Transcript: {result.output_filename}")
            print(f"   - Metadata: {result.output_filename.replace('.txt', '_metadata.json')}")
        
        if result.processing_time_seconds:
            print(f"⏱️  Processing Time: {result.processing_time_seconds:.1f} seconds")
        
        if result.fallback_attempted:
            print("🔄 Fallback Method Used: Yes")
        
    else:
        print("❌ Transcript Extraction Failed")
        print(f"🔍 Error Type: {result.error_type}")
        print(f"📝 Error Message: {result.error_message}")
        
        if result.retry_after:
            print(f"⏰ Retry After: {result.retry_after} seconds")
        
        if result.can_retry():
            print("🔄 Can Retry: Yes")
        else:
            print("🔄 Can Retry: No")
    
    # Display statistics
    stats = extractor.get_statistics()
    print(f"\n📊 Extraction Statistics:")
    print(f"   Total Attempts: {stats['total_attempts']}")
    print(f"   Successful: {stats['successful_extractions']}")
    print(f"   Failed: {stats['failed_extractions']}")
    
    if stats['total_attempts'] > 0:
        success_rate = stats['successful_extractions'] / stats['total_attempts'] * 100
        print(f"   Success Rate: {success_rate:.1f}%")
    
    if stats['youtube_api_successes'] > 0:
        print(f"   YouTube API Successes: {stats['youtube_api_successes']}")
    
    if stats['whisper_successes'] > 0:
        print(f"   Whisper Successes: {stats['whisper_successes']}")
    
    if stats['total_processing_time'] > 0:
        avg_time = stats['total_processing_time'] / stats['total_attempts']
        print(f"   Average Processing Time: {avg_time:.1f} seconds")


if __name__ == "__main__":
    sys.exit(main())
