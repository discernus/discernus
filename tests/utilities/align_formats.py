#!/usr/bin/env python3
import os
import csv
import glob

def align_formats_from_csv():
    """Align TXT and MD files to match CSV paragraph boundaries."""
    
    processed_files = []
    
    # Process each CSV file
    for csv_file in sorted(glob.glob('csv/*.csv')):
        base_name = os.path.basename(csv_file).replace('.csv', '')
        txt_file = f'txt/{base_name}.txt'
        md_file = f'md/{base_name}.md'
        
        print(f"Processing {base_name}...")
        
        # Read CSV to get paragraph content
        paragraphs = []
        president = ""
        speech_type = ""
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                paragraphs.append(row['content'])
                if not president:  # Get metadata from first row
                    president = row['president']
                    speech_type = row['speech_type']
        
        if not paragraphs:
            print(f"  Warning: No paragraphs found in {csv_file}")
            continue
        
        # Create properly formatted TXT file
        with open(txt_file, 'w', encoding='utf-8') as f:
            for i, paragraph in enumerate(paragraphs):
                f.write(paragraph)
                # Add empty line between paragraphs (except after last paragraph)
                if i < len(paragraphs) - 1:
                    f.write('\n\n')
            f.write('\n')  # End with single newline
        
        # Create properly formatted MD file
        with open(md_file, 'w', encoding='utf-8') as f:
            # Add appropriate title
            if speech_type == 'INAUGURAL':
                f.write(f"# {president} Inaugural Address\n\n")
            elif speech_type == 'SOTU':
                f.write(f"# {president} State of the Union Address\n\n")
            elif speech_type == 'JOINT':
                f.write(f"# {president} Address to Joint Session of Congress\n\n")
            else:
                f.write(f"# {president} Speech\n\n")
            
            # Process each paragraph
            for i, paragraph in enumerate(paragraphs):
                # Format the paragraph for markdown
                formatted_paragraph = format_paragraph_for_markdown(paragraph)
                f.write(formatted_paragraph)
                
                # Add empty line between paragraphs (except after last paragraph)
                if i < len(paragraphs) - 1:
                    f.write('\n\n')
            f.write('\n')  # End with single newline
        
        processed_files.append({
            'name': base_name,
            'paragraphs': len(paragraphs),
            'president': president,
            'speech_type': speech_type
        })
        
        print(f"  ✓ Aligned {len(paragraphs)} paragraphs across TXT and MD formats")
    
    return processed_files

def format_paragraph_for_markdown(paragraph):
    """Apply markdown formatting to a paragraph."""
    # Check if line might be a section header (all caps, short)
    if len(paragraph) < 100 and paragraph.isupper() and len(paragraph.split()) < 10:
        return f"## {paragraph.title()}"
    
    # Check for applause or audience reactions
    elif ('(Applause' in paragraph or '(Laughter' in paragraph or 
          '(Standing ovation' in paragraph or
          (paragraph.startswith('(') and paragraph.endswith(')'))):
        return f"*{paragraph}*"
    
    # Regular paragraph
    else:
        return paragraph

def validate_alignment():
    """Validate that all formats have consistent paragraph counts."""
    print("\n" + "="*50)
    print("VALIDATION: Checking format alignment...")
    print("="*50)
    
    issues = []
    
    for csv_file in sorted(glob.glob('csv/*.csv')):
        base_name = os.path.basename(csv_file).replace('.csv', '')
        txt_file = f'txt/{base_name}.txt'
        md_file = f'md/{base_name}.md'
        
        # Count CSV paragraphs
        csv_count = 0
        with open(csv_file, 'r', encoding='utf-8') as f:
            csv_count = sum(1 for line in f) - 1  # Subtract header
        
        # Count TXT paragraphs (empty line separated)
        with open(txt_file, 'r', encoding='utf-8') as f:
            txt_content = f.read().strip()
            txt_paragraphs = [p.strip() for p in txt_content.split('\n\n') if p.strip()]
            txt_count = len(txt_paragraphs)
        
        # Count MD paragraphs (skip title, count content paragraphs)
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
            md_lines = md_content.split('\n')
            # Skip title and empty lines at start
            content_start = 0
            for i, line in enumerate(md_lines):
                if line.startswith('# '):
                    content_start = i + 2  # Skip title and empty line
                    break
            
            md_content_part = '\n'.join(md_lines[content_start:]).strip()
            md_paragraphs = [p.strip() for p in md_content_part.split('\n\n') if p.strip()]
            md_count = len(md_paragraphs)
        
        # Check alignment
        if csv_count == txt_count == md_count:
            print(f"✓ {base_name}: {csv_count} paragraphs (aligned)")
        else:
            issue = f"✗ {base_name}: CSV={csv_count}, TXT={txt_count}, MD={md_count}"
            print(issue)
            issues.append(issue)
    
    if not issues:
        print("\n🎉 All formats perfectly aligned!")
    else:
        print(f"\n⚠️  Found {len(issues)} alignment issues:")
        for issue in issues:
            print(f"   {issue}")
    
    return len(issues) == 0

# Main execution
if __name__ == "__main__":
    print("Aligning TXT and MD formats with CSV paragraph boundaries...")
    print("="*60)
    
    processed_files = align_formats_from_csv()
    
    print(f"\nProcessed {len(processed_files)} files:")
    for file_info in processed_files:
        print(f"  {file_info['name']}: {file_info['paragraphs']} paragraphs ({file_info['speech_type']})")
    
    # Validate the alignment
    is_aligned = validate_alignment()
    
    if is_aligned:
        print("\n✅ SUCCESS: All formats now have semantic consistency!")
        print("   Each paragraph in CSV corresponds to the same semantic unit in TXT and MD.")
    else:
        print("\n❌ Some alignment issues detected. Please review the output above.") 