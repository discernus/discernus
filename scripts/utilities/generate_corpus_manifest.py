#!/usr/bin/env python3
"""
Corpus Hash Manifest Generator

Generates SHA-256 hash manifests for corpus files and collections.
Part of Phase 3: Corpus Management for the comprehensive experiment orchestrator.

Usage:
    python scripts/generate_corpus_manifest.py <path> [options]
"""

import argparse
import json
import hashlib
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def calculate_file_hash(file_path: Path) -> str:
    """Calculate SHA-256 hash of file"""
    hash_sha256 = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    
    return hash_sha256.hexdigest()

def generate_file_manifest(file_path: Path) -> Dict[str, Any]:
    """Generate manifest for a single file"""
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_hash = calculate_file_hash(file_path)
    stat = file_path.stat()
    
    manifest = {
        "version": "1.0.0",
        "type": "single_file",
        "file": {
            "name": file_path.name,
            "path": str(file_path),
            "hash": file_hash,
            "size_bytes": stat.st_size,
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "generated_at": datetime.now().isoformat()
        }
    }
    
    return manifest

def generate_collection_manifest(directory: Path, pattern: str = "*.txt", recursive: bool = False) -> Dict[str, Any]:
    """Generate manifest for a collection of files"""
    
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    # Find files
    if recursive:
        files = list(directory.rglob(pattern))
    else:
        files = list(directory.glob(pattern))
    
    files = [f for f in files if f.is_file()]  # Only files, not directories
    
    manifest = {
        "version": "1.0.0",
        "type": "collection",
        "collection": {
            "name": directory.name,
            "path": str(directory),
            "pattern": pattern,
            "recursive": recursive,
            "total_files": len(files),
            "generated_at": datetime.now().isoformat()
        },
        "files": {}
    }
    
    print(f"🔍 Found {len(files)} files matching pattern '{pattern}'")
    
    # Calculate hashes for all files
    for i, file_path in enumerate(files, 1):
        try:
            print(f"📄 Processing {i}/{len(files)}: {file_path.name}")
            
            file_hash = calculate_file_hash(file_path)
            stat = file_path.stat()
            
            # Use relative path as key
            rel_path = str(file_path.relative_to(directory))
            
            manifest["files"][rel_path] = {
                "name": file_path.name,
                "hash": file_hash,
                "size_bytes": stat.st_size,
                "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
            
        except Exception as e:
            print(f"⚠️  Error processing {file_path}: {e}")
            manifest["files"][str(file_path.relative_to(directory))] = {
                "error": str(e),
                "processed_at": datetime.now().isoformat()
            }
    
    return manifest

def save_manifest(manifest: Dict[str, Any], output_file: Path, pretty: bool = True):
    """Save manifest to JSON file"""
    
    indent = 2 if pretty else None
    
    with open(output_file, 'w') as f:
        json.dump(manifest, f, indent=indent)
    
    print(f"💾 Manifest saved: {output_file}")

def validate_manifest(manifest_file: Path, target_path: Path) -> bool:
    """Validate existing manifest against current files"""
    
    if not manifest_file.exists():
        print(f"❌ Manifest file not found: {manifest_file}")
        return False
    
    try:
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"❌ Error reading manifest: {e}")
        return False
    
    print(f"🔍 Validating manifest: {manifest_file}")
    
    manifest_type = manifest.get("type", "unknown")
    
    if manifest_type == "single_file":
        # Validate single file
        file_info = manifest.get("file", {})
        current_hash = calculate_file_hash(target_path)
        expected_hash = file_info.get("hash")
        
        if current_hash == expected_hash:
            print(f"✅ File validation passed: {target_path}")
            return True
        else:
            print(f"❌ Hash mismatch for {target_path}")
            print(f"   Expected: {expected_hash}")
            print(f"   Current:  {current_hash}")
            return False
    
    elif manifest_type == "collection":
        # Validate collection
        files_info = manifest.get("files", {})
        validation_passed = True
        
        print(f"📊 Validating {len(files_info)} files in collection...")
        
        for rel_path, file_info in files_info.items():
            file_path = target_path / rel_path
            
            if "error" in file_info:
                print(f"⚠️  Skipping file with previous error: {rel_path}")
                continue
            
            if not file_path.exists():
                print(f"❌ File missing: {rel_path}")
                validation_passed = False
                continue
            
            try:
                current_hash = calculate_file_hash(file_path)
                expected_hash = file_info.get("hash")
                
                if current_hash == expected_hash:
                    print(f"✅ {rel_path}")
                else:
                    print(f"❌ Hash mismatch: {rel_path}")
                    print(f"   Expected: {expected_hash}")
                    print(f"   Current:  {current_hash}")
                    validation_passed = False
            except Exception as e:
                print(f"❌ Error validating {rel_path}: {e}")
                validation_passed = False
        
        return validation_passed
    
    else:
        print(f"❌ Unknown manifest type: {manifest_type}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Generate SHA-256 hash manifests for corpus files and collections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate manifest for a single file
  python scripts/generate_corpus_manifest.py corpus/validation_set/dignity/speech.txt
  
  # Generate manifest for a directory collection
  python scripts/generate_corpus_manifest.py corpus/validation_set/dignity/ --pattern "*.txt"
  
  # Generate manifest recursively
  python scripts/generate_corpus_manifest.py corpus/validation_set/ --recursive
  
  # Validate existing manifest
  python scripts/generate_corpus_manifest.py corpus/validation_set/ --validate manifest.json
  
  # Generate with custom output file
  python scripts/generate_corpus_manifest.py corpus/raw_sources/ --output my_corpus_manifest.json
        """
    )
    
    parser.add_argument(
        'path',
        type=Path,
        help='File or directory path to process'
    )
    
    parser.add_argument(
        '--pattern', '-p',
        default='*.txt',
        help='File pattern for collections (default: *.txt)'
    )
    
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Search subdirectories recursively'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='Output manifest file (default: auto-generated based on input)'
    )
    
    parser.add_argument(
        '--validate', '-v',
        type=Path,
        help='Validate existing manifest file against current files'
    )
    
    parser.add_argument(
        '--compact', '-c',
        action='store_true',
        help='Generate compact JSON (no pretty printing)'
    )
    
    args = parser.parse_args()
    
    try:
        # Validation mode
        if args.validate:
            if not args.validate.exists():
                print(f"❌ Manifest file not found: {args.validate}")
                sys.exit(1)
            
            success = validate_manifest(args.validate, args.path)
            sys.exit(0 if success else 1)
        
        # Generation mode
        print(f"🎯 Generating hash manifest for: {args.path}")
        
        if args.path.is_file():
            # Single file manifest
            manifest = generate_file_manifest(args.path)
            
            # Default output file
            if not args.output:
                args.output = args.path.with_suffix('.manifest.json')
                
        elif args.path.is_dir():
            # Collection manifest
            manifest = generate_collection_manifest(
                args.path, 
                args.pattern, 
                args.recursive
            )
            
            # Default output file
            if not args.output:
                args.output = args.path / '.corpus_manifest.json'
                
        else:
            print(f"❌ Path does not exist: {args.path}")
            sys.exit(1)
        
        # Save manifest
        save_manifest(manifest, args.output, pretty=not args.compact)
        
        # Summary
        if manifest.get("type") == "collection":
            total_files = manifest["collection"]["total_files"]
            print(f"📊 Summary: {total_files} files processed")
        else:
            print(f"📊 Summary: Single file manifest generated")
        
        print(f"🎉 Manifest generation complete!")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 