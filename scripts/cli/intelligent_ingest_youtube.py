#!/usr/bin/env python3
"""
CLI tool for YouTube Transcript Intelligent Ingestion Service

Usage:
    python scripts/intelligent_ingest_youtube.py <youtube_url> [options]
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to Python path so we can import our modules
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

try:
    from src.corpus.registry import CorpusRegistry
    from src.corpus.youtube_ingestion import YouTubeCorpusIngestionService
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you've run: source scripts/setup_dev_env.sh")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Transcript Intelligent Ingestion Service - Extract transcripts and metadata from YouTube videos"
    )
    
    parser.add_argument(
        "url",
        help="YouTube video URL (supports youtube.com/watch, youtu.be, etc.)"
    )
    
    parser.add_argument(
        "--output-dir", "-o",
        help="Output directory for results (default: tmp/youtube_ingestion_TIMESTAMP)"
    )
    
    parser.add_argument(
        "--confidence-threshold", "-c",
        type=float,
        default=70.0,
        help="Confidence threshold for automatic registration (default: 70.0)"
    )
    
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Process video but don't register in corpus database"
    )
    
    parser.add_argument(
        "--languages", "-l",
        nargs="+",
        default=["en"],
        help="Preferred transcript languages (default: en)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("❌ Error: youtube-transcript-api not installed")
        print("💡 Install with: pip install youtube-transcript-api")
        sys.exit(1)
    
    # Optional: check for yt-dlp for enhanced metadata
    try:
        import yt_dlp
        print("✅ yt-dlp available for enhanced metadata extraction")
    except ImportError:
        print("⚠️  yt-dlp not available - basic metadata only")
        print("💡 For enhanced metadata, install with: pip install yt-dlp")
    
    # Set up environment variables if needed
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   LLM-enhanced metadata extraction may not work")
        print("   Transcript extraction will still work with YouTube metadata")
    
    try:
        print("🎬 Starting YouTube Transcript Intelligent Ingestion Service...")
        print(f"📺 Video URL: {args.url}")
        print(f"🎯 Confidence Threshold: {args.confidence_threshold}%")
        print(f"🌐 Languages: {', '.join(args.languages)}")
        
        if args.dry_run:
            print("🧪 Dry Run Mode: Will not register video in corpus database")
        
        # Initialize services
        if not args.dry_run:
            try:
                corpus_registry = CorpusRegistry()
                print("✅ CorpusRegistry connected")
            except Exception as e:
                print(f"⚠️  CorpusRegistry unavailable: {e}")
                print("   Proceeding without database registration...")
                corpus_registry = None
        else:
            corpus_registry = None
        
        # Create YouTube ingestion service
        ingestion_service = YouTubeCorpusIngestionService(
            corpus_registry=corpus_registry,
            confidence_threshold=args.confidence_threshold
        )
        
        # Run the ingestion
        result = ingestion_service.ingest_youtube_video(
            url=args.url,
            output_dir=args.output_dir
        )
        
        # Check for errors
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            if "video_info" in result:
                video_info = result["video_info"]
                print(f"📺 Video ID: {video_info.video_id}")
                print(f"📺 Title: {video_info.title or 'Unknown'}")
            sys.exit(1)
        
        print(f"\n🎉 YouTube Ingestion Complete!")
        
        # Show results
        print(f"\n📊 Results:")
        print(f"  Video ID: {result['video_id']}")
        print(f"  Confidence: {result['confidence']:.1f}%")
        print(f"  Content Length: {result['content_length']} characters")
        
        if args.verbose and "metadata" in result:
            metadata = result["metadata"]
            print(f"\n📋 Extracted Metadata:")
            print(f"  Title: {metadata.get('title', 'N/A')}")
            print(f"  Author: {metadata.get('author', 'N/A')}")
            print(f"  Date: {metadata.get('date', 'N/A')}")
            print(f"  Type: {metadata.get('document_type', 'N/A')}")
            print(f"  Description: {metadata.get('description', 'N/A')}")
        
        if args.verbose and "video_info" in result:
            video_info = result["video_info"]
            print(f"\n📺 YouTube Metadata:")
            print(f"  Channel: {video_info.get('channel', 'N/A')}")
            print(f"  Upload Date: {video_info.get('upload_date', 'N/A')}")
            print(f"  Duration: {video_info.get('duration', 'N/A')} seconds")
            print(f"  Views: {video_info.get('view_count', 'N/A')}")
        
        # Show registration status
        if "text_id" in result:
            print(f"\n✅ Registered in corpus as: {result['text_id']}")
        elif "registration_error" in result:
            print(f"\n⚠️  Registration failed: {result['registration_error']}")
        elif args.dry_run:
            print(f"\n🧪 Dry run - would register with confidence {result['confidence']:.1f}%")
        else:
            print(f"\n⚠️  Not registered (confidence {result['confidence']:.1f}% < {args.confidence_threshold}%)")
        
        # Show output location
        output_files = [
            result.get('file_path'),
            result.get('file_path', '').replace('_transcript.txt', '_result.json')
        ]
        
        print(f"\n💾 Output files:")
        for file_path in output_files:
            if file_path and os.path.exists(file_path):
                print(f"  📄 {file_path}")
        
        print(f"\n🔗 Original video: {result['video_url']}")
        
        # Return appropriate exit code
        if result["confidence"] >= args.confidence_threshold:
            sys.exit(0)
        else:
            print(f"\n⚠️  Low confidence score: {result['confidence']:.1f}%")
            print("💡 Consider manual review or lower confidence threshold")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 