#!/usr/bin/env python3
"""
Extract 2024 Campaign Speech Transcripts - Batch Processing Version

This script processes speeches in small batches to avoid CPU overload
and provide better progress visibility.
"""

import subprocess
import json
import os
import time
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

def process_batch(metadata_batch, batch_num, total_batches):
    """Process a batch of speeches"""
    print(f"\n🔄 Processing Batch {batch_num}/{total_batches} ({len(metadata_batch)} speeches)")
    print("=" * 60)
    
    success_count = 0
    for i, speech in enumerate(metadata_batch, 1):
        url = speech['youtube_url']
        output_file = Path(speech['file_path'])
        
        print(f"\n📝 [{i}/{len(metadata_batch)}] Processing: {output_file.name}")
        print(f"   URL: {url}")
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if extract_transcript(url, output_file):
            success_count += 1
        
        # Rate limiting between speeches
        if i < len(metadata_batch):  # Don't wait after the last one
            print("   ⏳ Waiting 3 seconds...")
            time.sleep(3)
    
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
    
    print(f"🎯 2024 Campaign Transcript Extraction")
    print(f"📊 Total speeches: {len(metadata)}")
    print(f"✅ Already extracted: {existing_count}")
    print(f"🔄 Remaining: {remaining_count}")
    
    if remaining_count == 0:
        print("🎉 All speeches already extracted!")
        return
    
    # Ask user for batch size
    print(f"\n📋 Choose batch size:")
    print(f"   1. Small (5 speeches) - Good for testing")
    print(f"   2. Medium (10 speeches) - Balanced")
    print(f"   3. Large (20 speeches) - Faster but more CPU intensive")
    
    while True:
        try:
            choice = input("\nEnter choice (1-3): ").strip()
            if choice == "1":
                batch_size = 5
                break
            elif choice == "2":
                batch_size = 10
                break
            elif choice == "3":
                batch_size = 20
                break
            else:
                print("Please enter 1, 2, or 3")
        except KeyboardInterrupt:
            print("\n\n⏹️ Extraction canceled by user")
            return
    
    # Filter to only unextracted speeches
    unextracted = [s for s in metadata if not Path(s['file_path']).exists()]
    
    # Process in batches
    total_batches = (len(unextracted) + batch_size - 1) // batch_size
    total_success = 0
    
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
            print("   ⏳ Taking a 10-second break between batches...")
            time.sleep(10)
    
    print(f"\n🎉 Extraction Summary:")
    print(f"   Total processed: {total_success}")
    print(f"   Total remaining: {len(unextracted) - total_success}")
    print(f"   Overall success rate: {total_success}/{len(unextracted)} ({total_success/len(unextracted)*100:.1f}%)")

if __name__ == "__main__":
    main()
