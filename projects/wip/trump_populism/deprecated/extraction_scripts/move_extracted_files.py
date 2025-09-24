#!/usr/bin/env python3
"""
Move Extracted 2024 Campaign Files

This script moves the extracted transcript files from the wrong location
(corpus/2024_campaign/) to the correct location (projects/2d_trump_populism/corpus/2024_campaign/).
"""

import os
import shutil
from pathlib import Path

def move_extracted_files():
    """Move extracted files from wrong location to correct location"""
    source_dir = Path("corpus/2024_campaign")
    target_dir = Path("projects/2d_trump_populism/corpus/2024_campaign")
    
    if not source_dir.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return
    
    if not target_dir.exists():
        print(f"❌ Target directory not found: {target_dir}")
        return
    
    print("🔄 Moving extracted 2024 campaign files...")
    print(f"   From: {source_dir}")
    print(f"   To: {target_dir}")
    
    moved_count = 0
    error_count = 0
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(source_dir):
        # Calculate relative path from source directory
        rel_path = Path(root).relative_to(source_dir)
        target_subdir = target_dir / rel_path
        
        # Create target subdirectory if it doesn't exist
        target_subdir.mkdir(parents=True, exist_ok=True)
        
        # Move files in this subdirectory
        for file in files:
            source_file = Path(root) / file
            target_file = target_subdir / file
            
            try:
                if target_file.exists():
                    print(f"⚠️  File already exists, skipping: {target_file}")
                    continue
                
                shutil.move(str(source_file), str(target_file))
                print(f"✅ Moved: {file}")
                moved_count += 1
                
            except Exception as e:
                print(f"❌ Error moving {file}: {e}")
                error_count += 1
    
    print(f"\n🎉 File moving complete!")
    print(f"   Moved: {moved_count} files")
    print(f"   Errors: {error_count} files")
    
    # Check if source directory is now empty
    if source_dir.exists() and not any(source_dir.iterdir()):
        try:
            source_dir.rmdir()
            print(f"🗑️  Removed empty source directory: {source_dir}")
        except Exception as e:
            print(f"⚠️  Could not remove source directory: {e}")
    
    # List what we have in the target directory
    print(f"\n📁 Files in target directory:")
    for root, dirs, files in os.walk(target_dir):
        if files:
            rel_path = Path(root).relative_to(target_dir)
            print(f"   {rel_path}: {len(files)} files")

if __name__ == "__main__":
    move_extracted_files()
