#!/usr/bin/env python3
"""
Corpus Organization Status Tool

Shows users what files have been processed, where they are stored,
and what still needs processing in their discovery areas.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

# Add src to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from narrative_gravity.corpus.intelligent_ingestion import IntelligentIngestionService
from narrative_gravity.corpus.registry import CorpusRegistry


def analyze_corpus_status():
    """Analyze current corpus organization and processing status."""
    
    # Paths
    raw_sources = Path("corpus/raw_sources")
    processed_storage = Path("corpus/processed")
    manifest_file = processed_storage / ".manifest.json"
    
    print("🗂️  Narrative Gravity Corpus Organization Status")
    print("=" * 60)
    
    # Check processed storage
    processed_files = {}
    processed_hashes = set()
    
    if manifest_file.exists():
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)
        
        processed_files = manifest.get("processed_files", {})
        processed_hashes = {info["content_hash"] for info in processed_files.values()}
        
        print(f"\n📦 PROCESSED STORAGE: {processed_storage}")
        print(f"  ✅ Total processed: {len(processed_files)}")
        print(f"  📅 Last updated: {manifest.get('last_updated', 'Unknown')}")
        
        # Show recent processing
        if processed_files:
            print(f"  📄 Recent documents:")
            sorted_files = sorted(
                processed_files.items(), 
                key=lambda x: x[1].get('processed_at', ''), 
                reverse=True
            )[:5]
            
            for text_id, info in sorted_files:
                confidence = info.get('confidence_score', 0)
                processed_at = info.get('processed_at', 'Unknown')[:10]  # Just date
                print(f"     • {text_id} ({confidence:.0f}% confidence, {processed_at})")
    else:
        print(f"\n📦 PROCESSED STORAGE: {processed_storage}")
        print(f"  ❌ No processed files found (manifest missing)")
    
    # Analyze raw sources
    print(f"\n📁 DISCOVERY AREA: {raw_sources}")
    
    if not raw_sources.exists():
        print(f"  ❌ Discovery area not found")
        return
    
    # Find all text files in raw sources
    text_files = list(raw_sources.glob("**/*.txt"))
    
    if not text_files:
        print(f"  📝 No text files found")
        return
    
    print(f"  📝 Total text files: {len(text_files)}")
    
    # Categorize files
    unprocessed_files = []
    duplicate_files = []
    
    # Quick content hash check
    ingestion_service = IntelligentIngestionService(None)  # No registry needed for hash check
    
    for file_path in text_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            import hashlib
            content_hash = hashlib.sha256(content.encode()).hexdigest()
            
            if content_hash in processed_hashes:
                # Find which text_id this corresponds to
                for text_id, info in processed_files.items():
                    if info.get("content_hash") == content_hash:
                        duplicate_files.append((file_path, text_id))
                        break
            else:
                unprocessed_files.append(file_path)
                
        except Exception as e:
            print(f"  ⚠️  Error reading {file_path.name}: {e}")
    
    # Report status
    print(f"\n📊 PROCESSING STATUS:")
    print(f"  🆕 Unprocessed files: {len(unprocessed_files)}")
    print(f"  🔄 Already processed: {len(duplicate_files)}")
    
    if unprocessed_files:
        print(f"\n🆕 NEEDS PROCESSING:")
        for file_path in unprocessed_files[:10]:  # Show first 10
            rel_path = file_path.relative_to(raw_sources)
            file_size = file_path.stat().st_size
            print(f"     • {rel_path} ({file_size:,} bytes)")
        
        if len(unprocessed_files) > 10:
            print(f"     ... and {len(unprocessed_files) - 10} more files")
    
    if duplicate_files:
        print(f"\n🔄 ALREADY PROCESSED:")
        for file_path, text_id in duplicate_files[:5]:  # Show first 5
            rel_path = file_path.relative_to(raw_sources)
            print(f"     • {rel_path} → {text_id}")
        
        if len(duplicate_files) > 5:
            print(f"     ... and {len(duplicate_files) - 5} more duplicates")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    
    if unprocessed_files:
        print(f"  🚀 Process new files:")
        print(f"     python3 scripts/intelligent_ingest.py corpus/raw_sources --verbose")
    
    if duplicate_files:
        print(f"  🗂️  Consider organizing raw_sources/ (duplicates found)")
        print(f"     You can safely move processed files to an archive folder")
    
    if not unprocessed_files and not duplicate_files:
        print(f"  ✅ All files in raw_sources have been processed!")
        print(f"  🎯 Ready for analysis or add more documents to raw_sources/")


def show_processed_file_details(text_id: str):
    """Show detailed information about a specific processed file."""
    processed_storage = Path("corpus/processed")
    manifest_file = processed_storage / ".manifest.json"
    
    if not manifest_file.exists():
        print(f"❌ No processed files manifest found")
        return
    
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
    
    processed_files = manifest.get("processed_files", {})
    
    if text_id not in processed_files:
        print(f"❌ File '{text_id}' not found in processed files")
        print(f"Available files: {', '.join(list(processed_files.keys())[:10])}")
        return
    
    info = processed_files[text_id]
    
    print(f"📄 PROCESSED FILE DETAILS: {text_id}")
    print("=" * 50)
    print(f"Title: {info.get('title', 'Unknown')}")
    print(f"Author: {info.get('author', 'Unknown')}")
    print(f"Date: {info.get('date', 'Unknown')}")
    print(f"Type: {info.get('document_type', 'Unknown')}")
    print(f"Confidence: {info.get('confidence_score', 0):.1f}%")
    print(f"Processed: {info.get('processed_at', 'Unknown')}")
    print(f"Content Hash: {info.get('content_hash', 'Unknown')[:16]}...")
    print(f"Stable Path: {info.get('file_path', 'Unknown')}")
    
    # Try to find metadata files
    stable_path = Path(info.get('file_path', ''))
    if stable_path.exists():
        metadata_file = stable_path.parent / ".metadata.json"
        provenance_file = stable_path.parent / ".provenance.json"
        
        if metadata_file.exists():
            print(f"\n📋 METADATA FILE: {metadata_file}")
        
        if provenance_file.exists():
            print(f"🔍 PROVENANCE FILE: {provenance_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Corpus Organization Status - See what's processed and what needs processing"
    )
    
    parser.add_argument(
        "--details", "-d",
        help="Show detailed information about a specific processed file (by text_id)"
    )
    
    parser.add_argument(
        "--list-processed", "-l",
        action="store_true",
        help="List all processed files"
    )
    
    args = parser.parse_args()
    
    if args.details:
        show_processed_file_details(args.details)
    elif args.list_processed:
        processed_storage = Path("corpus/processed")
        manifest_file = processed_storage / ".manifest.json"
        
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
            
            processed_files = manifest.get("processed_files", {})
            print(f"📦 PROCESSED FILES ({len(processed_files)} total):")
            
            for text_id, info in sorted(processed_files.items()):
                confidence = info.get('confidence_score', 0)
                title = info.get('title', 'Unknown')[:50]
                print(f"  {text_id:<25} {confidence:>3.0f}% {title}")
        else:
            print("❌ No processed files found")
    else:
        analyze_corpus_status()


if __name__ == "__main__":
    main() 