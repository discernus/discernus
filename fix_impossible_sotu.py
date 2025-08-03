#!/usr/bin/env python3
"""
Fix impossible SOTU documents by recategorizing them as joint_session addresses.
"""

import json

def fix_impossible_sotu(manifest_path):
    """Fix impossible SOTU documents in manifest."""
    
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    # Documents that are impossible as SOTU (outgoing presidents don't give SOTU)
    impossible_sotu = [
        "Clinton_SOTU_2001.txt",  # Clinton left office Jan 20, 2001
        "Bush_SOTU_2009.txt",     # Bush left office Jan 20, 2009  
        "Obama_SOTU_2017.txt"     # Obama left office Jan 20, 2017
    ]
    
    documents_fixed = 0
    
    for doc in manifest['file_manifest']:
        if doc['name'] in impossible_sotu:
            print(f"🔧 Fixing {doc['name']}: {doc['document_type']} → joint_session")
            doc['document_type'] = 'joint_session'
            documents_fixed += 1
    
    # Update the document_types list in analysis_dimensions
    if 'joint_session' not in manifest['analysis_dimensions']['document_types']:
        manifest['analysis_dimensions']['document_types'].append('joint_session')
        print("✅ Added 'joint_session' to document_types enumeration")
    
    # Write back to file
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Fixed {documents_fixed} impossible SOTU documents")
    return documents_fixed

if __name__ == '__main__':
    manifest_path = 'projects/3_large_batch_test/corpus/manifest.json'
    fix_impossible_sotu(manifest_path)