#!/usr/bin/env python3
"""
Add missing 'author' field to all documents in corpus manifest.
"""

import json
import sys

def add_author_field(manifest_path):
    """Add author field to all documents in manifest."""
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    documents_updated = 0
    
    for doc in manifest['file_manifest']:
        if 'author' not in doc:
            # Determine author based on document type
            if doc['document_type'] == 'platform':
                # Party platforms authored by party organizations
                party = doc.get('political_party', '')
                if party == 'Democratic':
                    doc['author'] = 'Democratic National Committee'
                elif party == 'Republican':
                    doc['author'] = 'Republican National Committee'
                else:
                    doc['author'] = f"{party} Party"
            elif doc['document_type'] == 'resolution':
                # Resolutions also by party organizations
                party = doc.get('political_party', '')
                if party == 'Republican':
                    doc['author'] = 'Republican National Committee'
                else:
                    doc['author'] = f"{party} Party"
            else:
                # Individual speeches authored by the speaker
                doc['author'] = doc.get('speaker', 'Unknown')
            
            documents_updated += 1
    
    # Write back to file
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Added 'author' field to {documents_updated} documents")
    return documents_updated

if __name__ == '__main__':
    manifest_path = 'projects/3_large_batch_test/corpus/manifest.json'
    add_author_field(manifest_path)