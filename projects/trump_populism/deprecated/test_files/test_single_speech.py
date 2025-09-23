#!/usr/bin/env python3
"""
Test single speech extraction to verify infrastructure works.
"""

import json
import sys
from pathlib import Path

# Add the scripts directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from corpus_tools.transcript_extractor import TranscriptExtractor

def test_single_speech():
    """Test extraction of a single speech."""
    
    # Load metadata to get a test speech
    metadata_path = Path("corpus/2024_campaign/2024_campaign_metadata.json")
    
    if not metadata_path.exists():
        print(f"❌ Metadata file not found: {metadata_path}")
        return
    
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Get the first speech that hasn't been processed yet
    test_speech = None
    for speech in metadata:
        file_path = Path(speech['file_path'])
        if not file_path.exists() or file_path.stat().st_size < 1000:
            test_speech = speech
            break
    
    if not test_speech:
        print("✅ All speeches have been processed!")
        return
    
    speech_id = test_speech['document_id']
    youtube_url = test_speech['youtube_url']
    
    print(f"🧪 Testing with speech: {speech_id}")
    print(f"   YouTube URL: {youtube_url}")
    print(f"   Campaign Phase: {test_speech['campaign_phase']}")
    print()
    
    # Initialize the transcript extractor with tiny model
    print("🔧 Initializing TranscriptExtractor...")
    extractor = TranscriptExtractor(
        prefer_method="whisper",
        whisper_model="tiny",  # Use tiny for speed and stability
        rate_limit=5,
        retry_attempts=1,
        output_format="both"
    )
    
    # Test extraction
    output_dir = Path("corpus/2024_campaign/test_single")
    output_dir.mkdir(exist_ok=True)
    
    print(f"🎯 Starting extraction...")
    print(f"   Output directory: {output_dir}")
    print(f"   Whisper model: {extractor.whisper_model}")
    print()
    
    try:
        result = extractor.extract_from_url(
            url=youtube_url,
            output_dir=output_dir,
            languages=["en"],
            experiment_context="trump_2024_campaign_single_test"
        )
        
        print("📊 EXTRACTION RESULTS:")
        print("=" * 50)
        
        if result.success:
            print(f"✅ SUCCESS!")
            print(f"   Method: {result.method}")
            print(f"   Confidence: {result.confidence:.1f}%")
            print(f"   Transcript length: {result.quality_metrics.transcript_length:,} characters")
            print(f"   Word count: {result.quality_metrics.word_count:,}")
            print(f"   Language: {result.language}")
            print(f"   Processing time: {result.processing_time_seconds:.1f} seconds")
            
            # Check if files were created
            transcript_files = list(output_dir.glob("*.txt"))
            metadata_files = list(output_dir.glob("*.json"))
            
            print(f"\n📁 Files created:")
            print(f"   Transcript files: {len(transcript_files)}")
            for f in transcript_files:
                print(f"     - {f.name}")
            
            print(f"   Metadata files: {len(metadata_files)}")
            for f in metadata_files:
                print(f"     - {f.name}")
                
        else:
            print(f"❌ FAILED!")
            print(f"   Error type: {result.error_type}")
            print(f"   Error message: {result.error_message}")
            print(f"   Can retry: {result.can_retry}")
    
    except Exception as e:
        print(f"💥 EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_single_speech()
