#!/usr/bin/env python3
"""
Convert .docx files to .txt in Trump Populism Corpus

This script converts all Word documents to plain text format to ensure
compliance with the v8.0 corpus specification requirement for ".txt files only".
"""

import os
import sys
from pathlib import Path
from docx import Document
import argparse

def convert_docx_to_txt(docx_path, txt_path):
    """Convert a single .docx file to .txt"""
    try:
        # Load the Word document
        doc = Document(docx_path)
        
        # Extract text from all paragraphs
        text_content = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Only add non-empty paragraphs
                text_content.append(paragraph.text)
        
        # Join paragraphs with double newlines for readability
        full_text = '\n\n'.join(text_content)
        
        # Write to text file
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        return True, len(full_text)
        
    except Exception as e:
        return False, str(e)

def process_corpus_directory(corpus_dir):
    """Process all .docx files in the corpus directory"""
    corpus_path = Path(corpus_dir)
    
    if not corpus_path.exists():
        print(f"❌ Corpus directory not found: {corpus_path}")
        return
    
    # Find all .docx files
    docx_files = list(corpus_path.rglob("*.docx"))
    
    if not docx_files:
        print("✅ No .docx files found in corpus directory")
        return
    
    print(f"🔍 Found {len(docx_files)} .docx files to convert")
    
    successful_conversions = 0
    failed_conversions = 0
    total_words = 0
    
    for docx_file in docx_files:
        # Create corresponding .txt path
        txt_file = docx_file.with_suffix('.txt')
        
        print(f"📄 Converting: {docx_file.name}")
        
        # Convert the file
        success, result = convert_docx_to_txt(docx_file, txt_file)
        
        if success:
            word_count = result
            total_words += word_count
            print(f"   ✅ Success: {txt_file.name} ({word_count} characters)")
            successful_conversions += 1
            
            # Optionally remove the original .docx file
            # Uncomment the next line if you want to delete originals
            # docx_file.unlink()
            
        else:
            print(f"   ❌ Failed: {result}")
            failed_conversions += 1
    
    # Summary
    print(f"\n📊 Conversion Summary:")
    print(f"   ✅ Successful: {successful_conversions}")
    print(f"   ❌ Failed: {failed_conversions}")
    print(f"   📝 Total characters: {total_words:,}")
    
    if successful_conversions > 0:
        print(f"\n🎯 Next steps:")
        print(f"   1. Verify text quality in converted files")
        print(f"   2. Update corpus manifest if needed")
        print(f"   3. Consider archiving original .docx files")
        print(f"   4. Run corpus validation to ensure compliance")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Convert .docx files to .txt in Trump Populism Corpus"
    )
    parser.add_argument(
        "--corpus-dir",
        default="projects/2d_trump_populism/corpus",
        help="Path to corpus directory (default: projects/2d_trump_populism/corpus)"
    )
    parser.add_argument(
        "--remove-originals",
        action="store_true",
        help="Remove original .docx files after conversion"
    )
    
    args = parser.parse_args()
    
    print("🚀 Starting .docx to .txt conversion...")
    print(f"📁 Corpus directory: {args.corpus_dir}")
    
    process_corpus_directory(args.corpus_dir)
    
    print("\n🎉 Conversion process complete!")

if __name__ == "__main__":
    main()
