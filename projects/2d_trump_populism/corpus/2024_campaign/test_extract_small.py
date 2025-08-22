#!/usr/bin/env python3
"""
Test Small Batch Extraction

This script tests the corrected extraction process with just 2 speeches
to verify all path issues are resolved.
"""

import subprocess
import json
from pathlib import Path

def extract_transcript(url, output_file):
    """Extract transcript from YouTube URL"""
    cmd = [
        "python3", "../../scripts/corpus_tools/enhanced_transcript_extractor.py",
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
    metadata_path = Path("corpus/2024_campaign/2024_campaign_metadata.json")
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print("🧪 Testing Small Batch Extraction (Fixed Paths)")
    print("=" * 60)
    
    # Test with speeches 7-8 (different from previous tests)
    test_speeches = metadata[6:8]
    
    print(f"🎯 Testing with {len(test_speeches)} speeches...")
    
    success_count = 0
    for speech in test_speeches:
        url = speech['youtube_url']
        output_file = Path(speech['file_path'])
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if extract_transcript(url, output_file):
            success_count += 1
        
        print()  # Add spacing between speeches
    
    print(f"🎉 Test complete: {success_count}/{len(test_speeches)} successful")
    
    if success_count == len(test_speeches):
        print("✅ All tests passed! Path issues resolved. Ready for full extraction.")
    else:
        print("⚠️  Some tests failed. Review errors before full extraction.")

if __name__ == "__main__":
    main()
