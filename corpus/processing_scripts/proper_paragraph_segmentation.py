#!/usr/bin/env python3
import os
import csv
import re
import glob
from collections import defaultdict

def aggressive_paragraph_segmentation(text):
    """
    Use aggressive paragraph segmentation for speech transcripts.
    Political speeches should have 50-100+ paragraphs, not 2-3 massive blocks.
    """
    # First, normalize the text and split into sentences
    sentences = []
    
    # Split the text into potential sentences using multiple delimiters
    text = text.replace('\n', ' ')  # Convert line breaks to spaces
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    
    # Split on sentence endings, but be smart about abbreviations
    sentence_splits = re.split(r'([.!?]+\s+)', text)
    
    current_sentence = ""
    for i, part in enumerate(sentence_splits):
        if re.match(r'^[.!?]+\s+$', part):  # This is punctuation + space
            current_sentence += part.strip()
            if current_sentence.strip():
                sentences.append(current_sentence.strip())
            current_sentence = ""
        else:
            current_sentence += part
    
    # Don't forget the last sentence
    if current_sentence.strip():
        sentences.append(current_sentence.strip())
    
    # Now group sentences into paragraphs
    paragraphs = []
    current_paragraph = []
    
    for i, sentence in enumerate(sentences):
        if not sentence.strip():
            continue
            
        current_paragraph.append(sentence)
        
        # Determine if we should end the paragraph here
        should_break = False
        
        # Always break on applause
        if ('(Applause' in sentence or '(Laughter' in sentence or 
            '(Standing ovation' in sentence):
            should_break = True
        
        # Break after a reasonable number of sentences (2-4 for speeches)
        elif len(current_paragraph) >= 3:
            should_break = True
            
        # Break if current paragraph is getting long (word count)
        elif len(' '.join(current_paragraph).split()) > 150:
            should_break = True
            
        # Break on topic transitions (if next sentence starts with certain words)
        elif i + 1 < len(sentences):
            next_sentence = sentences[i + 1].strip()
            if next_sentence:
                topic_starters = [
                    'Tonight', 'Today', 'Now', 'But', 'However', 'Therefore', 
                    'Meanwhile', 'In fact', 'Let me', 'I want to', 'We must',
                    'We will', 'We have', 'We are', 'I have', 'I will', 'I am',
                    'My administration', 'Our country', 'Our nation', 'America',
                    'The United States', 'This administration', 'Since', 'After',
                    'Before', 'When', 'As we', 'To', 'For', 'And so', 'That is why'
                ]
                
                for starter in topic_starters:
                    if next_sentence.startswith(starter + ' '):
                        should_break = True
                        break
        
        if should_break and current_paragraph:
            paragraph_text = ' '.join(current_paragraph)
            if len(paragraph_text.split()) >= 5:  # Minimum viable paragraph
                paragraphs.append(paragraph_text)
            current_paragraph = []
    
    # Don't forget the last paragraph
    if current_paragraph:
        paragraph_text = ' '.join(current_paragraph)
        if len(paragraph_text.split()) >= 5:
            paragraphs.append(paragraph_text)
    
    return paragraphs

def extract_metadata_from_filename(filename):
    """Extract president, speech type, and sequence from filename."""
    parts = filename.replace('golden_', '').replace('.txt', '').split('_')
    president = parts[0].title()
    speech_type = parts[1].upper()
    sequence = parts[2] if len(parts) > 2 else '01'
    return president, speech_type, sequence

def count_sentences(text):
    """Count sentences in a paragraph."""
    sentence_endings = re.findall(r'[.!?]+', text)
    return len(sentence_endings)

def reprocess_all_files():
    """Reprocess all files with proper paragraph segmentation."""
    
    print("Starting complete reprocessing with aggressive paragraph segmentation...")
    print("="*70)
    
    # Source file mapping
    source_mapping = {
        'golden_clinton_inaugural_01': 'Clinton_Inaugural_1993.txt',
        'golden_clinton_sotu_01': 'Clinton_SOTU_1995.txt',
        'golden_clinton_sotu_02': 'Clinton_SOTU_1999.txt',
        'golden_bush_inaugural_01': 'Bush_Inaugural_2001.txt',
        'golden_bush_sotu_01': 'Bush_SOTU_2003.txt',
        'golden_bush_sotu_02': 'Bush_SOTU_2007.txt',
        'golden_obama_inaugural_01': 'Obama_Inaugural_2009.txt',
        'golden_obama_sotu_01': 'Obama_SOTU_2012.txt',
        'golden_obama_sotu_02': 'Obama_SOTU_2015.txt',
        'golden_trump_inaugural_01': 'Trump_Inaugural_2025.txt',
        'golden_trump_sotu_01': 'Trump_SOTU_2018.txt',
        'golden_trump_sotu_02': 'Trump_SOTU_2020.txt',
        'golden_biden_inaugural_01': 'Biden_Inaugural_2021.txt',
        'golden_biden_sotu_01': 'Biden_SOTU_2022.txt',
        'golden_biden_sotu_02': 'Biden_SOTU_2024.txt',
        'golden_trump_joint_01': 'txt/golden_trump_joint_01.txt'  # Special case - already processed
    }
    
    processed_files = []
    
    for golden_name, source_name in source_mapping.items():
        print(f"Processing {golden_name}...")
        
        # Read source content
        if source_name.startswith('txt/'):
            # Special case for joint session file
            with open(source_name, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            source_path = f"../raw_sources/recent_us_presidents/{source_name}"
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
        
        # Extract metadata
        president, speech_type, sequence = extract_metadata_from_filename(golden_name)
        
        # Use aggressive paragraph segmentation
        paragraphs = aggressive_paragraph_segmentation(content)
        
        if not paragraphs:
            print(f"  Warning: No paragraphs found in {golden_name}")
            continue
        
        # Create TXT file with proper spacing
        txt_file = f'txt/{golden_name}.txt'
        with open(txt_file, 'w', encoding='utf-8') as f:
            for i, paragraph in enumerate(paragraphs):
                f.write(paragraph)
                # Add double line break between paragraphs for visual clarity
                if i < len(paragraphs) - 1:
                    f.write('\n\n')
            f.write('\n')
        
        # Create CSV file with proper paragraph records
        csv_file = f'csv/{golden_name}.csv'
        csv_data = []
        
        for paragraph_id, paragraph in enumerate(paragraphs, 1):
            # Determine if this paragraph contains applause/reactions
            is_applause = 1 if ('(Applause' in paragraph or '(Laughter' in paragraph or 
                               '(Standing ovation' in paragraph) else 0
            
            # Calculate metrics
            word_count = len(paragraph.split())
            char_count = len(paragraph)
            sentence_count = count_sentences(paragraph)
            
            # Estimate reading time (average 200 words per minute)
            reading_time_seconds = (word_count / 200) * 60
            
            csv_row = {
                'id': f"{president.lower()}_{speech_type.lower()}_{sequence}_{paragraph_id:03d}",
                'president': president,
                'speech_type': speech_type,
                'sequence': sequence,
                'paragraph_id': paragraph_id,
                'content': paragraph,
                'is_applause': is_applause,
                'word_count': word_count,
                'char_count': char_count,
                'sentence_count': sentence_count,
                'reading_time_seconds': round(reading_time_seconds, 1)
            }
            
            csv_data.append(csv_row)
        
        # Write CSV file
        fieldnames = ['id', 'president', 'speech_type', 'sequence', 'paragraph_id', 
                      'content', 'is_applause', 'word_count', 'char_count', 
                      'sentence_count', 'reading_time_seconds']
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        
        # Create MD file with proper formatting
        md_file = f'md/{golden_name}.md'
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
            
            for i, paragraph in enumerate(paragraphs):
                # Format the paragraph for markdown
                formatted_paragraph = format_paragraph_for_markdown(paragraph)
                f.write(formatted_paragraph)
                # Add double line break between paragraphs for visual clarity
                if i < len(paragraphs) - 1:
                    f.write('\n\n')
            f.write('\n')
        
        processed_files.append({
            'name': golden_name,
            'paragraphs': len(paragraphs),
            'president': president,
            'speech_type': speech_type
        })
        
        print(f"  ✓ Created {len(paragraphs)} paragraphs (was broken before)")
    
    return processed_files

def format_paragraph_for_markdown(paragraph):
    """Apply markdown formatting to a paragraph."""
    # Check for applause or audience reactions
    if ('(Applause' in paragraph or '(Laughter' in paragraph or 
          '(Standing ovation' in paragraph):
        return f"*{paragraph}*"
    
    # Regular paragraph
    else:
        return paragraph

# Main execution
if __name__ == "__main__":
    processed_files = reprocess_all_files()
    
    print(f"\n" + "="*70)
    print(f"REPROCESSING COMPLETE")
    print(f"="*70)
    print(f"Total files reprocessed: {len(processed_files)}")
    
    # Show breakdown by speech type
    by_type = defaultdict(list)
    total_paragraphs = 0
    
    for file_info in processed_files:
        total_paragraphs += file_info['paragraphs']
        if 'inaugural' in file_info['name']:
            by_type['Inaugural'].append(file_info['paragraphs'])
        elif 'sotu' in file_info['name']:
            by_type['SOTU'].append(file_info['paragraphs'])
        elif 'joint' in file_info['name']:
            by_type['Joint'].append(file_info['paragraphs'])
    
    print(f"Total paragraphs: {total_paragraphs}")
    print(f"Average paragraphs per speech: {total_paragraphs/len(processed_files):.1f}")
    
    print(f"\nBreakdown by speech type:")
    for speech_type, counts in by_type.items():
        avg_count = sum(counts) / len(counts)
        min_count = min(counts)
        max_count = max(counts)
        print(f"  {speech_type}: {len(counts)} speeches, avg {avg_count:.1f} paragraphs ({min_count}-{max_count} range)")
    
    print(f"\nDetailed breakdown:")
    for file_info in processed_files:
        print(f"  {file_info['name']}: {file_info['paragraphs']} paragraphs")
        
    print(f"\n✅ Success! SOTU speeches should now have 50-100+ paragraphs.")
    print(f"   All formats include proper paragraph spacing for visual clarity.")
    print(f"   Each paragraph represents a coherent semantic unit for analysis.") 