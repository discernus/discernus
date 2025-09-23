#!/usr/bin/env python3
"""
Simple Trump 2024 Campaign Transcript Extraction
Uses the working infrastructure directly without complex imports.
"""

import json
import subprocess
import time
from pathlib import Path

def extract_single_speech(youtube_url: str, output_dir: str, speech_id: str):
    """Extract a single speech using the working CLI tool."""
    
    # Use the working CLI command we tested
    cmd = [
        "python3", "-m", "scripts.corpus_tools.transcript_extractor_cli",
        youtube_url,
        "--output-dir", output_dir,
        "--prefer-method", "whisper",
        "--whisper-model", "tiny",
        "--experiment-context", "trump_2024_campaign"
    ]
    
    print(f"🎯 Extracting: {speech_id}")
    print(f"   URL: {youtube_url}")
    print(f"   Output: {output_dir}")
    
    try:
        # Run the extraction
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent)
        
        if result.returncode == 0:
            print(f"✅ Success: {speech_id}")
            print(f"   Output: {result.stdout}")
        else:
            print(f"❌ Failed: {speech_id}")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False
    
    return True

def main():
    """Main function to extract a few speeches."""
    
    # Load metadata
    metadata_path = Path("corpus/2024_campaign/2024_campaign_metadata.json")
    
    if not metadata_path.exists():
        print(f"❌ Metadata file not found: {metadata_path}")
        return
    
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Get first few unprocessed speeches
    pending_speeches = []
    for speech in metadata:
        file_path = Path(speech['file_path'])
        if not file_path.exists() or file_path.stat().st_size < 1000:
            pending_speeches.append(speech)
            if len(pending_speeches) >= 3:  # Process only 3 at a time
                break
    
    if not pending_speeches:
        print("✅ All speeches have been processed!")
        return
    
    print(f"🎯 Processing {len(pending_speeches)} speeches...")
    
    # Process each speech
    for speech in pending_speeches:
        speech_id = speech['document_id']
        youtube_url = speech['youtube_url']
        campaign_phase = speech['campaign_phase']
        
        # Create output directory
        output_dir = f"corpus/2024_campaign/{campaign_phase}"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Extract transcript
        success = extract_single_speech(youtube_url, output_dir, speech_id)
        
        if success:
            print(f"✅ Completed: {speech_id}")
        else:
            print(f"❌ Failed: {speech_id}")
        
        # Wait between extractions
        if speech != pending_speeches[-1]:  # Not the last one
            print("⏳ Waiting 15 seconds...")
            time.sleep(15)
    
    print("🎉 Batch processing complete!")

if __name__ == "__main__":
    main()
