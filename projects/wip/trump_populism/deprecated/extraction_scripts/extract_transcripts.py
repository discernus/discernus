#!/usr/bin/env python3
"""
Extract 2024 Campaign Speech Transcripts

This script uses the enhanced_transcript_extractor.py to extract transcripts
from the 74 Trump 2024 campaign speeches identified in the brownepres repository.
"""

import subprocess
import json
import os
from pathlib import Path

def extract_transcript(url, output_file):
    """Extract transcript from YouTube URL"""
    cmd = [
        "python3", "../../scripts/corpus_tools/enhanced_transcript_extractor.py",
        url,  # URL is positional argument
        "--output-dir", str(output_file.parent)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ Extracted: {output_file.name}")
            return True
        else:
            print(f"❌ Failed: {output_file.name} - {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {output_file.name}")
        return False
    except Exception as e:
        print(f"❌ Error: {output_file.name} - {e}")
        return False

def main():
    # Load metadata from current directory
    metadata_path = Path("2024_campaign_metadata.json")
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print(f"🎯 Starting transcript extraction for {len(metadata)} speeches...")
    
    success_count = 0
    for speech in metadata:
        url = speech['youtube_url']
        output_file = Path(speech['file_path'])
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if extract_transcript(url, output_file):
            success_count += 1
        
        # Rate limiting - wait between extractions
        import time
        time.sleep(2)
    
    print(f"\n🎉 Extraction complete: {success_count}/{len(metadata)} successful")

if __name__ == "__main__":
    main()
