#!/usr/bin/env python3
"""
Fix Trump_SOTU_2025.txt to be correctly categorized as AJSC (Address to Joint Session of Congress).
"""

import json

def fix_trump_ajsc(manifest_path):
    """Fix Trump 2025 document categorization."""
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    documents_fixed = 0
    
    for doc in manifest['file_manifest']:
        if doc['name'] == 'Trump_SOTU_2025.txt':
            print(f"🔧 Fixing {doc['name']}: {doc['document_type']} → ajsc")
            doc['document_type'] = 'ajsc'
            documents_fixed += 1
    
    # Update the document_types list in analysis_dimensions
    if 'ajsc' not in manifest['analysis_dimensions']['document_types']:
        manifest['analysis_dimensions']['document_types'].append('ajsc')
        print("✅ Added 'ajsc' to document_types enumeration")
    
    # Write back to file
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Fixed {documents_fixed} Trump AJSC document")
    return documents_fixed

if __name__ == '__main__':
    manifest_path = 'projects/3_large_batch_test/corpus/manifest.json'
    fix_trump_ajsc(manifest_path)