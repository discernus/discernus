#!/usr/bin/env python3
"""
Fix 2024 Campaign Metadata Paths

This script updates the file_path values in the metadata to point to the correct
project directory location.
"""

import json
from pathlib import Path

def fix_metadata_paths():
    """Fix the file_path values in the metadata"""
    metadata_path = Path("projects/2d_trump_populism/corpus/2024_campaign/2024_campaign_metadata.json")
    
    # Load metadata
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    print("🔧 Fixing 2024 Campaign Metadata Paths")
    print("=" * 50)
    
    fixed_count = 0
    for speech in metadata:
        old_path = speech['file_path']
        
        # Check if path needs fixing
        if old_path.startswith('corpus/2024_campaign/'):
            # Fix the path to point to the project directory
            new_path = f"projects/2d_trump_populism/{old_path}"
            speech['file_path'] = new_path
            fixed_count += 1
            print(f"✅ Fixed: {old_path} -> {new_path}")
    
    print(f"\n🎉 Path fixing complete!")
    print(f"   Fixed: {fixed_count} file paths")
    
    # Save updated metadata
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Updated metadata saved to: {metadata_path}")
    
    # Show sample of fixed paths
    print(f"\n📁 Sample of fixed paths:")
    for i, speech in enumerate(metadata[:3]):
        print(f"   {i+1}. {speech['file_path']}")

if __name__ == "__main__":
    fix_metadata_paths()
