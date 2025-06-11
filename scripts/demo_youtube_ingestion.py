#!/usr/bin/env python3
"""
Demo: YouTube Transcript Intelligent Ingestion

Demonstrates the YouTube transcript extraction capabilities of the 
intelligent corpus ingestion service.

This demo works without API keys by using fallback metadata extraction.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

def demo_youtube_ingestion():
    """Demonstrate YouTube transcript ingestion"""
    
    print("🎬 YouTube Transcript Intelligent Ingestion Demo")
    print("=" * 50)
    
    # Check if YouTube dependencies are available
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        print("✅ youtube-transcript-api available")
    except ImportError:
        print("❌ youtube-transcript-api not installed")
        print("💡 Install with: pip install youtube-transcript-api")
        return False
    
    try:
        import yt_dlp
        print("✅ yt-dlp available for enhanced metadata")
    except ImportError:
        print("⚠️  yt-dlp not available - will use basic metadata only")
        print("💡 For enhanced metadata, install with: pip install yt-dlp")
    
    # Import our YouTube ingestion service
    try:
        from narrative_gravity.corpus.youtube_ingestion import (
            YouTubeTranscriptExtractor, 
            YouTubeCorpusIngestionService
        )
        print("✅ YouTube ingestion service imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import YouTube service: {e}")
        print("💡 Make sure you've run: source scripts/setup_dev_env.sh")
        return False
    
    # Demo URLs - various types of political content
    demo_urls = [
        {
            "url": "https://www.youtube.com/watch?v=lipnBHeyvII",
            "description": "User-provided URL",
            "expected_type": "Unknown"
        },
        # Backup URLs in case the first doesn't have transcripts
        {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "description": "Rick Astley - Never Gonna Give You Up (testing transcript availability)",
            "expected_type": "Music Video"
        }
    ]
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"tmp/youtube_demo_{timestamp}"
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Output directory: {output_dir}")
    
    # Initialize extractor
    extractor = YouTubeTranscriptExtractor()
    
    successful_demos = 0
    
    for i, demo in enumerate(demo_urls, 1):
        print(f"\n🎯 Demo {i}: {demo['description']}")
        print(f"🔗 URL: {demo['url']}")
        
        try:
            # Extract video ID
            video_id = extractor.extract_video_id(demo['url'])
            if not video_id:
                print("❌ Could not extract video ID")
                continue
            
            print(f"📺 Video ID: {video_id}")
            
            # Get video metadata
            video_info = extractor.get_video_info(video_id)
            print(f"📺 Title: {video_info.title or 'Unknown'}")
            print(f"📺 Channel: {video_info.channel or 'Unknown'}")
            print(f"📺 Upload Date: {video_info.upload_date or 'Unknown'}")
            
            # Try to get transcript
            transcript = extractor.get_transcript(video_id)
            if transcript:
                cleaned_transcript = extractor.clean_transcript(transcript)
                print(f"✅ Transcript extracted ({len(cleaned_transcript)} characters)")
                
                # Save transcript for inspection
                transcript_file = output_path / f"demo_{i}_{video_id}_transcript.txt"
                with open(transcript_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_transcript)
                
                print(f"💾 Saved to: {transcript_file}")
                
                # Show preview
                preview = cleaned_transcript[:200] + "..." if len(cleaned_transcript) > 200 else cleaned_transcript
                print(f"📋 Preview: {preview}")
                
                successful_demos += 1
                
                # For demo purposes, just show first successful extraction
                if successful_demos >= 1:
                    break
                    
            else:
                print("❌ No transcript available for this video")
                print("💡 This video may not have captions/subtitles enabled")
                
        except Exception as e:
            print(f"❌ Error processing {demo['url']}: {e}")
            continue
    
    print(f"\n📊 Demo Results:")
    print(f"  Successful extractions: {successful_demos}")
    print(f"  Output directory: {output_dir}")
    
    if successful_demos > 0:
        print(f"\n✅ YouTube Transcript Ingestion Demo Successful!")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Install dependencies: pip install youtube-transcript-api yt-dlp")
        print(f"   2. Try with your URLs: python scripts/intelligent_ingest_youtube.py <youtube_url>")
        print(f"   3. Add --verbose for detailed metadata extraction")
        print(f"   4. Use --dry-run to test without database registration")
        
        return True
    else:
        print(f"\n⚠️  No transcripts were successfully extracted")
        print(f"💡 This could be because:")
        print(f"   - Videos don't have transcripts/captions enabled")
        print(f"   - Network issues or API rate limits")
        print(f"   - Private or restricted videos")
        
        return False


if __name__ == "__main__":
    success = demo_youtube_ingestion()
    sys.exit(0 if success else 1) 