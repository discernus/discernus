#!/usr/bin/env python3
"""
Update Corpus Manifest with Custom Analytical Groupings
=======================================================

Adds candidate_type and electoral_success fields to all documents
in the corpus manifest to ensure experiment-corpus metadata alignment.

Author: Discernus Project
"""

import re
from pathlib import Path

def update_corpus_manifest():
    """Update corpus.md with missing metadata fields"""
    
    # Define mappings based on experiment requirements
    candidate_mappings = {
        'Trump': {'candidate_type': 'outsider', 'electoral_success': 3},
        'Clinton': {'candidate_type': 'establishment', 'electoral_success': 3},
        'Sanders': {'candidate_type': 'outsider', 'electoral_success': 2},
        'Cruz': {'candidate_type': 'challenger', 'electoral_success': 2},
        'Rubio': {'candidate_type': 'establishment', 'electoral_success': 1},
        'Kasich': {'candidate_type': 'establishment', 'electoral_success': 1}
    }
    
    corpus_path = Path("/Volumes/code/discernus/projects/vanderveen_presidential_pdaf/corpus.md")
    
    # Read current content
    with open(corpus_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process each document entry
    def update_document_entry(match):
        entry = match.group(0)
        
        # Extract candidate_short
        candidate_match = re.search(r'candidate_short: "([^"]+)"', entry)
        if not candidate_match:
            return entry
            
        candidate = candidate_match.group(1)
        mapping = candidate_mappings.get(candidate, {'candidate_type': 'unknown', 'electoral_success': 0})
        
        # Check if already has the fields
        if 'candidate_type:' in entry and 'electoral_success:' in entry:
            return entry
            
        # Add the fields after speech_type
        speech_type_line = re.search(r'(\s+speech_type: "[^"]+"\n)', entry)
        if speech_type_line:
            insertion_point = speech_type_line.end()
            new_fields = f'    candidate_type: "{mapping["candidate_type"]}"\n    electoral_success: {mapping["electoral_success"]}\n'
            entry = entry[:insertion_point] + new_fields + entry[insertion_point:]
        
        return entry
    
    # Find all document entries and update them
    document_pattern = r'  - filename: "[^"]+"\n(?:    [^\n]+\n)*'
    updated_content = re.sub(document_pattern, update_document_entry, content)
    
    # Write updated content
    with open(corpus_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ Corpus manifest updated with custom analytical groupings")
    print("📊 Added candidate_type and electoral_success fields to all documents")

if __name__ == "__main__":
    update_corpus_manifest()
