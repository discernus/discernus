#!/usr/bin/env python3
import csv

def fix_bush_sotu_md():
    """Fix the Bush SOTU md file by reading from the properly segmented CSV."""
    
    # Read the CSV file (which was processed correctly)
    paragraphs = []
    with open('csv/golden_bush_sotu_01.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            paragraphs.append(row['content'])
    
    # Write the MD file with proper formatting
    with open('md/golden_bush_sotu_01.md', 'w', encoding='utf-8') as f:
        f.write("# Bush State of the Union Address\n\n")
        
        for i, paragraph in enumerate(paragraphs):
            # Check for applause or audience reactions and italicize them
            if ('(Applause' in paragraph or '(Laughter' in paragraph or 
                '(Standing ovation' in paragraph):
                formatted_paragraph = f"*{paragraph}*"
            else:
                formatted_paragraph = paragraph
                
            f.write(formatted_paragraph)
            # Add double line break between paragraphs for visual clarity
            if i < len(paragraphs) - 1:
                f.write('\n\n')
        f.write('\n')
    
    print(f"✅ Fixed golden_bush_sotu_01.md with {len(paragraphs)} paragraphs and proper spacing")

if __name__ == "__main__":
    fix_bush_sotu_md() 