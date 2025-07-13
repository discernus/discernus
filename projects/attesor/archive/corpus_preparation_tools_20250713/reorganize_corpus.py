#!/usr/bin/env python3
"""
Attesor Corpus Reorganization Script
Reorganizes files with secure hashes and creates secure mapping.
"""

import json
import shutil
from pathlib import Path
from hash_generator import create_speaker_mapping

def create_directories():
    """Create the secure directory structure"""
    base_path = Path(__file__).parent.parent
    
    # Create corpus directory for LLM-accessible files
    corpus_path = base_path / 'corpus'
    corpus_path.mkdir(exist_ok=True)
    
    # Create analysis directory for results
    analysis_path = base_path / 'analysis'
    analysis_path.mkdir(exist_ok=True)
    
    return corpus_path, analysis_path

def save_secure_mapping(mapping):
    """Save the secure mapping to JSONL format"""
    mapping_file = Path(__file__).parent / 'speaker_mapping.jsonl'
    
    with open(mapping_file, 'w') as f:
        for secure_hash, info in mapping.items():
            # Don't include temp_hash in the secure mapping
            secure_info = {
                'hash': secure_hash,
                'speaker': info['speaker'],
                'title': info['title'],
                'source': info['source'],
                'processed': info['processed']
            }
            f.write(json.dumps(secure_info) + '\n')
    
    print(f"Secure mapping saved to: {mapping_file}")
    return mapping_file

def clean_sanitized_content(content):
    """Remove speaker information from sanitized content"""
    lines = content.split('\n')
    
    # Remove the first line which contains speaker filename
    if lines and lines[0].startswith('#') and '.txt' in lines[0]:
        # Remove the header line and any empty line that follows
        result_lines = []
        skip_next_empty = True
        for i, line in enumerate(lines[1:], 1):
            if skip_next_empty and line.strip() == '':
                skip_next_empty = False
                continue
            result_lines.append(line)
            skip_next_empty = False
        return '\n'.join(result_lines)
    
    return content

def copy_and_organize_files(mapping, corpus_path):
    """Copy files with new secure hashed names"""
    base_path = Path(__file__).parent.parent
    sanitized_path = base_path / 'sanitized'
    esperanto_path = base_path / 'esperanto'
    
    # Mapping from esperanto translation numbers to temp hashes
    esperanto_mapping = {
        'speech_translation_1.md': 'f9b8c2d7',  # Romney
        'speech_translation_2.md': 'a1c5e7d2',  # McCain  
        'speech_translation_3.md': 'e2b9f5c1',  # Vance
        'speech_translation_4.md': 'b3f7d2a6',  # Booker
        'speech_translation_5.md': '7f9a2b8c',  # AOC
        'speech_translation_6.md': 'c6d4a3e8',  # Lewis
        'speech_translation_7.md': 'd8a7b4f3',  # King
        'speech_translation_8.md': 'a4c8e1d9',  # Sanders
    }
    
    # Reverse mapping to find secure hash from temp hash
    temp_to_secure = {}
    for secure_hash, info in mapping.items():
        temp_to_secure[info['temp_hash']] = secure_hash
    
    copied_files = []
    
    # Copy sanitized files (cleaned)
    for sanitized_file in sanitized_path.glob('*.md'):
        temp_hash = sanitized_file.stem.split('_')[-1]  # Extract hash from filename
        if temp_hash in temp_to_secure:
            secure_hash = temp_to_secure[temp_hash]
            
            # Read and clean content
            with open(sanitized_file, 'r') as f:
                content = f.read()
            
            cleaned_content = clean_sanitized_content(content)
            
            # Write to new location with secure hash
            new_filename = f"{secure_hash}_sanitized.txt"
            new_path = corpus_path / new_filename
            
            with open(new_path, 'w') as f:
                f.write(cleaned_content)
            
            copied_files.append(f"Sanitized: {sanitized_file.name} → {new_filename}")
    
    # Copy Esperanto files
    for esperanto_file in esperanto_path.glob('*.md'):
        if esperanto_file.name in esperanto_mapping:
            temp_hash = esperanto_mapping[esperanto_file.name]
            if temp_hash in temp_to_secure:
                secure_hash = temp_to_secure[temp_hash]
                
                # Read content
                with open(esperanto_file, 'r') as f:
                    content = f.read()
                
                # Write to new location with secure hash
                new_filename = f"{secure_hash}_esperanto.txt"
                new_path = corpus_path / new_filename
                
                with open(new_path, 'w') as f:
                    f.write(content)
                
                copied_files.append(f"Esperanto: {esperanto_file.name} → {new_filename}")
    
    return copied_files

def spot_check_files(mapping, corpus_path):
    """Perform spot checks on the reorganized files"""
    print("\n" + "="*60)
    print("SPOT CHECK RESULTS")
    print("="*60)
    
    issues = []
    
    # Check that all expected files exist
    for secure_hash, info in mapping.items():
        sanitized_file = corpus_path / f"{secure_hash}_sanitized.txt"
        esperanto_file = corpus_path / f"{secure_hash}_esperanto.txt"
        
        if not sanitized_file.exists():
            issues.append(f"Missing sanitized file: {secure_hash} ({info['speaker']})")
        
        if not esperanto_file.exists():
            issues.append(f"Missing Esperanto file: {secure_hash} ({info['speaker']})")
        
        # Check that sanitized files don't contain speaker names
        if sanitized_file.exists():
            with open(sanitized_file, 'r') as f:
                content = f.read()
            
            # Check for speaker name leakage (using word boundaries)
            import re
            speaker_words = info['speaker'].lower().split()
            for word in speaker_words:
                if len(word) > 3:
                    # Use word boundary regex to avoid false positives
                    pattern = r'\b' + re.escape(word) + r'\b'
                    if re.search(pattern, content.lower()):
                        issues.append(f"Potential speaker leak in {secure_hash}: '{word}' found")
            
            # Check that header was removed
            if content.startswith('#') and '.txt' in content.split('\n')[0]:
                issues.append(f"Header not removed from {secure_hash}")
    
    if issues:
        print("ISSUES FOUND:")
        for issue in issues:
            print(f"  ❌ {issue}")
    else:
        print("✅ All checks passed!")
        
        # Show sample mapping
        print(f"\nSample secure hashes (first 3):")
        for i, (secure_hash, info) in enumerate(list(mapping.items())[:3]):
            print(f"  {secure_hash} → {info['speaker']} ({info['title']})")
        
        print(f"\nTotal files created: {len(mapping) * 2}")
        print(f"Corpus directory: {corpus_path}")
    
    return len(issues) == 0

def main():
    """Main reorganization function"""
    print("Attesor Corpus Reorganization")
    print("=" * 40)
    
    # Generate secure mapping
    print("1. Generating secure hashes...")
    mapping = create_speaker_mapping()
    
    # Create directories
    print("2. Creating directory structure...")
    corpus_path, analysis_path = create_directories()
    
    # Save secure mapping
    print("3. Saving secure mapping...")
    mapping_file = save_secure_mapping(mapping)
    
    # Copy and organize files
    print("4. Copying and organizing files...")
    copied_files = copy_and_organize_files(mapping, corpus_path)
    
    print(f"\nFiles copied:")
    for file_info in copied_files:
        print(f"  {file_info}")
    
    # Spot check
    print("\n5. Performing spot checks...")
    success = spot_check_files(mapping, corpus_path)
    
    if success:
        print(f"\n🎉 Attesor corpus successfully reorganized!")
        print(f"   Secure files: {corpus_path}")
        print(f"   Mapping: {mapping_file}")
        print(f"   Ready for bias-free analysis!")
    else:
        print(f"\n❌ Issues found. Please review and fix.")
    
    return success

if __name__ == "__main__":
    main() 