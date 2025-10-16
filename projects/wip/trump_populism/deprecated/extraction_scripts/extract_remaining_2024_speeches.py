#!/usr/bin/env python3
"""
Extract Remaining 2024 Campaign Speeches with Fixed Whisper Formatting

This script processes the remaining 64 speeches using the fixed enhanced transcript extractor
with proper rate limiting and progress tracking for Whisper-based extraction.
"""

import subprocess
import json
import time
import os
from pathlib import Path
from datetime import datetime

def extract_transcript_with_fixed_extractor(url, output_file, batch_num, total_in_batch):
    """Extract transcript using the fixed enhanced transcript extractor"""
    
    print(f"📝 [{batch_num}/{total_in_batch}] Processing: {output_file.name}")
    print(f"   URL: {url}")
    print(f"   Output: {output_file}")
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Use the fixed enhanced transcript extractor with Whisper preference
    cmd = [
        "python3", "../../scripts/corpus_tools/enhanced_transcript_extractor.py",
        url,
        "--output-dir", str(output_file.parent),
        "--prefer-whisper",
        "--whisper-model", "base"
    ]
    
    try:
        print("   🔄 Starting extraction...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)  # 10 minute timeout
        
        if result.returncode == 0:
            print(f"   ✅ Success: {output_file.name}")
            return True
        else:
            print(f"   ❌ Failed: {output_file.name}")
            print(f"      Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ Timeout: {output_file.name}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {output_file.name} - {e}")
        return False

def process_batch(metadata_batch, batch_num, total_batches):
    """Process a batch of speeches with proper rate limiting"""
    print(f"\n🔄 Processing Batch {batch_num}/{total_batches} ({len(metadata_batch)} speeches)")
    print("=" * 80)
    
    success_count = 0
    for i, speech in enumerate(metadata_batch, 1):
        url = speech['youtube_url']
        output_file = Path(speech['file_path'])
        
        if extract_transcript_with_fixed_extractor(url, output_file, i, len(metadata_batch)):
            success_count += 1
        
        # Rate limiting between speeches (longer delays for Whisper)
        if i < len(metadata_batch):
            delay = 15  # 15 seconds between extractions
            print(f"   ⏳ Waiting {delay} seconds before next extraction...")
            time.sleep(delay)
    
    print(f"\n✅ Batch {batch_num} complete: {success_count}/{len(metadata_batch)} successful")
    return success_count

def main():
    # Load metadata
    metadata_path = Path("corpus/2024_campaign/2024_campaign_metadata.json")
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Check how many are already extracted
    existing_count = 0
    for speech in metadata:
        output_file = Path(speech['file_path'])
        if output_file.exists():
            existing_count += 1
    
    remaining_count = len(metadata) - existing_count
    
    print(f"🎯 2024 Campaign Transcript Extraction (Fixed Whisper)")
    print(f"📊 Total speeches: {len(metadata)}")
    print(f"✅ Already extracted: {existing_count}")
    print(f"🔄 Remaining: {remaining_count}")
    print(f"🔧 Using: Fixed enhanced transcript extractor with Whisper fallback")
    
    if remaining_count == 0:
        print("🎉 All speeches already extracted!")
        return
    
    # Filter to only unextracted speeches
    unextracted = [s for s in metadata if not Path(s['file_path']).exists()]
    
    # Ask user for batch size
    print(f"\n📋 Choose batch size for Whisper processing:")
    print(f"   1. Small (3 speeches) - Conservative, good for testing")
    print(f"   2. Medium (5 speeches) - Balanced approach")
    print(f"   3. Large (8 speeches) - Faster but more intensive")
    
    while True:
        try:
            choice = input("\nEnter choice (1-3): ").strip()
            if choice == "1":
                batch_size = 3
                break
            elif choice == "2":
                batch_size = 5
                break
            elif choice == "3":
                batch_size = 8
                break
            else:
                print("Please enter 1, 2, or 3")
        except KeyboardInterrupt:
            print("\n\n⏹️ Extraction canceled by user")
            return
    
    # Process in batches
    total_batches = (len(unextracted) + batch_size - 1) // batch_size
    total_success = 0
    
    print(f"\n🚀 Starting extraction with batch size {batch_size}")
    print(f"📅 Estimated time: ~{len(unextracted) * 15 / 60:.1f} minutes (15s per speech)")
    
    for i in range(0, len(unextracted), batch_size):
        batch = unextracted[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        success_count = process_batch(batch, batch_num, total_batches)
        total_success += success_count
        
        # Ask if user wants to continue
        if i + batch_size < len(unextracted):
            print(f"\n⏸️ Batch {batch_num} complete. Continue with next batch?")
            try:
                response = input("Continue? (y/n): ").strip().lower()
                if response not in ['y', 'yes']:
                    print(f"\n⏹️ Extraction stopped after batch {batch_num}")
                    break
            except KeyboardInterrupt:
                print(f"\n\n⏹️ Extraction stopped after batch {batch_num}")
                break
        
        # Longer break between batches
        if i + batch_size < len(unextracted):
            delay = 30  # 30 second break between batches
            print(f"   ⏳ Taking a {delay}-second break between batches...")
            time.sleep(delay)
    
    print(f"\n🎉 Extraction Summary:")
    print(f"   Total processed: {total_success}")
    print(f"   Total remaining: {len(unextracted) - total_success}")
    print(f"   Overall success rate: {total_success}/{len(unextracted)} ({total_success/len(unextracted)*100:.1f}%)")
    
    if total_success > 0:
        print(f"\n✅ Successfully extracted {total_success} new transcripts!")
        print(f"📁 Check the corpus directories for new files.")
    
    if total_success < len(unextracted):
        print(f"\n⚠️ {len(unextracted) - total_success} speeches failed to extract.")
        print(f"   Review the error messages above for troubleshooting.")

if __name__ == "__main__":
    main()
