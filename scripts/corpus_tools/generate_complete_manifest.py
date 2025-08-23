#!/usr/bin/env python3
"""
Generate Complete Corpus Manifest

This script generates a complete v10-compliant corpus manifest
listing all documents in the Trump populism corpus.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

def extract_metadata_from_filename(filename: str) -> Dict[str, Any]:
    """Extract metadata from filename using pattern matching."""
    filename_lower = filename.lower()
    
    # Initialize metadata with defaults
    metadata = {
        "speaker": "Donald Trump",
        "filename": filename,
        "event_type": "Unknown",
        "political_phase": "Unknown",
        "date": "Unknown"  # Ensure date field always exists
    }
    
    # Determine political phase based on directory structure
    if "early" in filename_lower or "1988" in filename or "2000" in filename:
        metadata["political_phase"] = "Early Political Period (1988-2000)"
        metadata["date"] = "1988-2000"
    elif "2011" in filename or "2013" in filename or "2014" in filename:
        metadata["political_phase"] = "Pre-Campaign Positioning (2011-2015)"
        metadata["date"] = "2011-2015"
    elif "2015" in filename or "2016" in filename:
        metadata["political_phase"] = "Campaign Launch (2015-2016)"
        metadata["date"] = "2015-2016"
    elif "2017" in filename or "2018" in filename or "2019" in filename or "2020" in filename:
        metadata["political_phase"] = "First Presidency (2017-2020)"
        metadata["date"] = "2017-2020"
    elif "2021" in filename or "2022" in filename or "2023" in filename:
        if "2021" in filename and "january" in filename_lower and "6" in filename:
            metadata["political_phase"] = "Between Presidencies (2021-2023)"
            metadata["date"] = "2021-01-06"
            metadata["event_type"] = "Political Rally"
            metadata["historical_significance"] = "Critical - Preceded historic events"
        elif "2022" in filename and "november" in filename_lower and "7" in filename:
            metadata["political_phase"] = "Between Presidencies (2021-2023)"
            metadata["date"] = "2022-11-07"
            metadata["event_type"] = "Campaign Rally"
        else:
            metadata["political_phase"] = "Between Presidencies (2021-2023)"
            metadata["date"] = "2021-2023"
    elif "2024" in filename:
        metadata["political_phase"] = "Campaign to Second Presidency (2023-2024)"
        metadata["date"] = "2024"
    elif "2025" in filename:
        metadata["political_phase"] = "Second Presidency (2025-present)"
        metadata["date"] = "2025"
    
    # Determine event type based on filename patterns
    if "cpac" in filename_lower:
        metadata["event_type"] = "CPAC Speech"
        metadata["location"] = "Conservative Political Action Conference"
    elif "rally" in filename_lower:
        metadata["event_type"] = "Campaign Rally"
    elif "speech" in filename_lower:
        metadata["event_type"] = "Political Speech"
    elif "interview" in filename_lower:
        metadata["event_type"] = "Media Interview"
    elif "campaign" in filename_lower:
        metadata["event_type"] = "Campaign Event"
    
    # Extract location if present
    if "florida" in filename_lower:
        metadata["location"] = "Florida"
    elif "pennsylvania" in filename_lower:
        metadata["location"] = "Pennsylvania"
    elif "ohio" in filename_lower:
        metadata["location"] = "Ohio"
    elif "new hampshire" in filename_lower:
        metadata["location"] = "New Hampshire"
    elif "north carolina" in filename_lower:
        metadata["location"] = "North Carolina"
    elif "michigan" in filename_lower:
        metadata["location"] = "Michigan"
    elif "washington" in filename_lower:
        metadata["location"] = "Washington"
    elif "colorado" in filename_lower:
        metadata["location"] = "Colorado"
    elif "virginia" in filename_lower:
        metadata["location"] = "Virginia"
    
    # Generate document ID
    base_name = Path(filename).stem
    safe_id = base_name.replace(" ", "_").replace("-", "_").replace("|", "_").replace("___", "_")
    metadata["document_id"] = f"doc_{safe_id[:50]}"  # Limit length
    
    return metadata

def generate_complete_manifest(corpus_dir):
    """Generate a complete v10-compliant corpus manifest."""
    corpus_dir = Path(corpus_dir)
    
    # Find all text files in the corpus directory
    text_files = list(corpus_dir.rglob("*.txt"))
    
    # Filter out non-document files
    excluded_files = {
        "extraction_log.txt",
        "log.txt",
        "error_log.txt",
        "debug_log.txt"
    }
    
    # Filter out files that are not actual corpus documents
    document_files = []
    for file_path in text_files:
        filename = file_path.name
        # Skip if it's in the excluded list or looks like a log file
        if filename in excluded_files or filename.startswith("log") or "log" in filename.lower():
            continue
        document_files.append(file_path)
    
    print(f"Found {len(document_files)} document files (excluded {len(text_files) - len(document_files)} non-document files)")
    
    documents = []
    used_ids = set()
    for file_path in sorted(document_files):
        # Get relative path from corpus directory root
        relative_path = file_path.relative_to(corpus_dir)
        filename = str(relative_path)
        
        metadata = extract_metadata_from_filename(filename)
        
        # Ensure unique document ID
        base_id = metadata["document_id"]
        counter = 1
        while metadata["document_id"] in used_ids:
            metadata["document_id"] = f"{base_id}_{counter}"
            counter += 1
        used_ids.add(metadata["document_id"])
        
        documents.append(metadata)
    
    # Create manifest structure
    manifest = {
        "name": "Trump Political Discourse Corpus",
        "version": "10.0",
        "description": "Complete corpus covering Donald Trump's political discourse from 1988-2025, including early positioning, campaigns, two presidencies, and complete CPAC series evolution.",
        "total_documents": len(documents),
        "date_range": "1988-2025",
        "political_phases": 7,
        "framework_compatibility": "PDAF v10.0",
        "documents": documents
    }
    
    return manifest

def main():
    """Main function to generate complete manifest."""
    
    # Get corpus directory
    if len(sys.argv) > 1:
        corpus_dir = Path(sys.argv[1])
    else:
        # Default to Trump populism corpus
        corpus_dir = Path("projects/2d_trump_populism/corpus")
    
    if not corpus_dir.exists():
        print(f"❌ Corpus directory not found: {corpus_dir}")
        sys.exit(1)
    
    print(f"🔍 Generating complete manifest for: {corpus_dir}")
    
    # Generate manifest
    manifest = generate_complete_manifest(corpus_dir)
    
    # Save manifest
    output_file = corpus_dir.parent / "corpus_complete_manifest.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Complete manifest generated: {output_file}")
    print(f"📊 Total documents: {manifest['total_documents']}")
    
    # Also generate YAML format for corpus.md
    yaml_output = corpus_dir.parent / "corpus_manifest_yaml.txt"
    
    with open(yaml_output, 'w', encoding='utf-8') as f:
        f.write("```yaml\n")
        f.write(f"name: \"{manifest['name']}\"\n")
        f.write(f"version: \"{manifest['version']}\"\n")
        f.write(f"description: \"{manifest['description']}\"\n")
        f.write(f"total_documents: {manifest['total_documents']}\n")
        f.write(f"date_range: \"{manifest['date_range']}\"\n")
        f.write(f"political_phases: {manifest['political_phases']}\n")
        f.write(f"framework_compatibility: \"{manifest['framework_compatibility']}\"\n")
        f.write("\ndocuments:\n")
        
        for doc in manifest['documents']:
            f.write(f"  - filename: \"{doc['filename']}\"\n")
            f.write(f"    document_id: \"{doc['document_id']}\"\n")
            f.write(f"    metadata:\n")
            f.write(f"      speaker: \"{doc['speaker']}\"\n")
            f.write(f"      date: \"{doc['date']}\"\n")
            f.write(f"      event_type: \"{doc['event_type']}\"\n")
            f.write(f"      political_phase: \"{doc['political_phase']}\"\n")
            
            if 'location' in doc and doc['location'] != 'Unknown':
                f.write(f"      location: \"{doc['location']}\"\n")
            if 'historical_significance' in doc:
                f.write(f"      historical_significance: \"{doc['historical_significance']}\"\n")
            
            f.write("\n")
        
        f.write("```\n")
    
    print(f"📝 YAML format saved to: {yaml_output}")
    print(f"💡 Copy the YAML content to replace the documents section in corpus.md")

if __name__ == "__main__":
    main()
