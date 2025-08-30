#!/usr/bin/env python3
"""
Run 2024 Campaign Speech Extraction

This script runs from the project root to extract all 74 Trump 2024 campaign speeches.
"""

import subprocess
import json
import os
from pathlib import Path

def extract_transcript(url, output_file):
    """Extract transcript from YouTube URL"""
    cmd = [
        "python3", "scripts/corpus_tools/enhanced_transcript_extractor.py",
        url,  # URL is positional argument
        "--output-dir", str(output_file.parent)
    ]
    
    print(f"🎯 Extracting: {output_file.name}")
    print(f"   URL: {url}")
    print(f"   Output dir: {output_file.parent}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ Success: {output_file.name}")
            return True
        else:
            print(f"❌ Failed: {output_file.name}")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {output_file.name}")
        return False
    except Exception as e:
        print(f"❌ Error: {output_file.name} - {e}")
        return False

def main():
    # Load metadata
    metadata_path = Path("projects/2d_trump_populism/corpus/2024_campaign/2024_campaign_metadata.json")
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print("🚀 Starting 2024 Campaign Transcript Extraction")
    print("=" * 60)
    print(f"🎯 Total speeches to extract: {len(metadata)}")
    
    # Skip already extracted speeches (first 8)
    start_index = 8
    remaining_speeches = metadata[start_index:]
    
    print(f"📊 Already extracted: {start_index} speeches")
    print(f"📊 Remaining to extract: {len(remaining_speeches)} speeches")
    print("=" * 60)
    
    success_count = 0
    for i, speech in enumerate(remaining_speeches):
        print(f"\n📝 Processing speech {start_index + i + 1}/{len(metadata)}")
        
        url = speech['youtube_url']
        output_file = Path(speech['file_path'])
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if extract_transcript(url, output_file):
            success_count += 1
        
        # Rate limiting - wait between extractions
        import time
        time.sleep(2)
    
    print(f"\n🎉 Extraction complete!")
    print(f"   Total successful: {start_index + success_count}/{len(metadata)}")
    print(f"   Newly extracted: {success_count}/{len(remaining_speeches)}")

if __name__ == "__main__":
    main()
