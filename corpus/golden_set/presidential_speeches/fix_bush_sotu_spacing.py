#!/usr/bin/env python3
import csv

def fix_bush_sotu_txt():
    """Fix the Bush SOTU txt file by reading from the properly segmented CSV."""
    
    # Read the CSV file (which was processed correctly)
    paragraphs = []
    with open('csv/golden_bush_sotu_01.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            paragraphs.append(row['content'])
    
    # Write the TXT file with proper paragraph spacing
    with open('txt/golden_bush_sotu_01.txt', 'w', encoding='utf-8') as f:
        for i, paragraph in enumerate(paragraphs):
            f.write(paragraph)
            # Add double line break between paragraphs for visual clarity
            if i < len(paragraphs) - 1:
                f.write('\n\n')
        f.write('\n')
    
    print(f"✅ Fixed golden_bush_sotu_01.txt with {len(paragraphs)} paragraphs and proper spacing")

if __name__ == "__main__":
    fix_bush_sotu_txt() 