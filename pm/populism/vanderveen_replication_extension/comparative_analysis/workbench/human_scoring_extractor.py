#!/usr/bin/env python3
"""
Human Scoring Extractor for PDAF Training Data
Extracts human-coded scores and commentary from Van der Veen XML scoring sheets
"""

import xml.etree.ElementTree as ET
import re
import csv
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

def extract_text_from_xml(xml_content: str) -> str:
    """Extract readable text from Word XML content."""
    # Remove XML tags and extract text content
    text = re.sub(r'<[^>]+>', ' ', xml_content)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def parse_scoring_sheet(xml_file_path: str) -> Dict[str, Any]:
    """Parse a single XML scoring sheet and extract scoring data."""
    
    with open(xml_file_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    # Extract basic metadata
    metadata = {}
    
    # Extract politician name - look for text between "Name of politician:" and next tag
    name_match = re.search(r'Name of politician:\s*([^<]+)', xml_content)
    if name_match:
        metadata['politician'] = name_match.group(1).strip()
    
    # Extract speech title
    title_match = re.search(r'Title of Speech:\s*([^<]+)', xml_content)
    if title_match:
        metadata['speech_title'] = title_match.group(1).strip()
    
    # Extract date
    date_match = re.search(r'Date of Speech:\s*([^<]+)', xml_content)
    if date_match:
        metadata['speech_date'] = date_match.group(1).strip()
    
    # Extract grader
    grader_match = re.search(r'Grader:\s*([^<]+)', xml_content)
    if grader_match:
        metadata['grader'] = grader_match.group(1).strip()
    
    # Extract grading date
    grading_date_match = re.search(r'Date of grading:\s*([^<]+)', xml_content)
    if grading_date_match:
        metadata['grading_date'] = grading_date_match.group(1).strip()
    
    # Extract final grade - look for the actual number after "Final Grade"
    final_grade_match = re.search(r'Final Grade.*?(\d+)', xml_content, re.DOTALL)
    if final_grade_match:
        metadata['final_grade'] = int(final_grade_match.group(1))
    
    # Extract scoring table data
    scoring_data = {}
    
    # Look for the scoring table structure
    # The table has columns: Dimension, Score, Populist, Pluralist
    
    # Extract Manichaean vision score and commentary
    # Look for the actual score in the table cell
    manichaean_score_match = re.search(
        r'Manichaean vision.*?<w:t>(\d+)</w:t>', 
        xml_content, re.DOTALL
    )
    if manichaean_score_match:
        scoring_data['manichaean_vision'] = {
            'score': int(manichaean_score_match.group(1)),
            'populist_description': 'It conveys a Manichaean vision of the world, that is, one that is moral (every issue has a strong moral dimension) and dualistic (everything is in one category or the other, "right" or "wrong," "good" or "evil")',
            'pluralist_description': 'The discourse does not frame issues in moral terms or paint them in black-and-white. Instead, there is a strong tendency to focus on narrow, particular issues.'
        }
    
    # Extract Populist notion of the people score
    people_score_match = re.search(
        r'Populist notion of the people.*?<w:t>(\d+)</w:t>', 
        xml_content, re.DOTALL
    )
    if people_score_match:
        scoring_data['populist_notion_people'] = {
            'score': int(people_score_match.group(1)),
            'populist_description': 'Although Manichaean, the discourse is still democratic, in the sense that the good is embodied in the will of the majority, which is seen as a unified whole, perhaps but not necessarily expressed in references to the "voluntad del pueblo"; however, the speaker ascribes a kind of unchanging essentialism to that will, rather than letting it be whatever 50 percent of the people want at any particular moment.',
            'pluralist_description': 'Democracy is simply the calculation of votes. This should be respected and is seen as the foundation of legitimate government, but it is not meant to be an exercise in arriving at a preexisting, knowable "will."'
        }
    
    # Extract Evil elite score
    elite_score_match = re.search(
        r'Evil elite.*?<w:t>(\d+)</w:t>', 
        xml_content, re.DOTALL
    )
    if elite_score_match:
        scoring_data['evil_elite'] = {
            'score': int(elite_score_match.group(1)),
            'populist_description': 'The evil is embodied in a minority—more specifically, an elite—whose specific identity will vary according to context. Domestically, in Latin America it is often an economic elite, perhaps the "oligarchy," but it may also be a racial elite; internationally, it may be the United States or the capitalist, industrialized nations or international financiers or simply an ideology such as neoliberalism and capitalism.',
            'pluralist_description': 'The discourse avoids a conspiratorial tone and does not single out any evil ruling minority. It avoids labeling opponents as evil and may not even mention them in an effort to maintain a positive tone and keep passions low.'
        }
    
    # Extract additional commentary and examples
    examples = []
    
    # Look for quoted examples in the text - these are in <w:t> tags
    quote_matches = re.findall(r'<w:t>"([^"]+)"</w:t>', xml_content)
    for quote in quote_matches:
        if len(quote) > 20:  # Only keep substantial quotes
            examples.append(quote)
    
    return {
        'metadata': metadata,
        'scoring_data': scoring_data,
        'examples': examples,
        'raw_xml_path': xml_file_path
    }

def extract_all_scoring_sheets(directory_path: str) -> List[Dict[str, Any]]:
    """Extract scoring data from all XML files in a directory."""
    
    xml_files = list(Path(directory_path).rglob("*.xml"))
    print(f"Found {len(xml_files)} XML files")
    
    all_scores = []
    
    for xml_file in xml_files:
        try:
            print(f"Processing: {xml_file.name}")
            scores = parse_scoring_sheet(str(xml_file))
            all_scores.append(scores)
        except Exception as e:
            print(f"Error processing {xml_file.name}: {e}")
            continue
    
    return all_scores

def save_training_data_to_csv(scores: List[Dict[str, Any]], output_path: str):
    """Save extracted scoring data to CSV for training."""
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'politician', 'speech_title', 'speech_date', 'grader', 'grading_date',
            'final_grade', 'manichaean_score', 'people_score', 'elite_score',
            'manichaean_populist_desc', 'manichaean_pluralist_desc',
            'people_populist_desc', 'people_pluralist_desc',
            'elite_populist_desc', 'elite_pluralist_desc',
            'examples', 'xml_file'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for score in scores:
            row = {
                'politician': score['metadata'].get('politician', ''),
                'speech_title': score['metadata'].get('speech_title', ''),
                'speech_date': score['metadata'].get('speech_date', ''),
                'grader': score['metadata'].get('grader', ''),
                'grading_date': score['metadata'].get('grading_date', ''),
                'final_grade': score['metadata'].get('final_grade', ''),
                'manichaean_score': score['scoring_data'].get('manichaean_vision', {}).get('score', ''),
                'people_score': score['scoring_data'].get('populist_notion_people', {}).get('score', ''),
                'elite_score': score['scoring_data'].get('evil_elite', {}).get('score', ''),
                'manichaean_populist_desc': score['scoring_data'].get('manichaean_vision', {}).get('populist_description', ''),
                'manichaean_pluralist_desc': score['scoring_data'].get('manichaean_vision', {}).get('pluralist_description', ''),
                'people_populist_desc': score['scoring_data'].get('populist_notion_people', {}).get('populist_description', ''),
                'people_pluralist_desc': score['scoring_data'].get('populist_notion_people', {}).get('pluralist_description', ''),
                'elite_populist_desc': score['scoring_data'].get('evil_elite', {}).get('populist_description', ''),
                'elite_pluralist_desc': score['scoring_data'].get('evil_elite', {}).get('pluralist_description', ''),
                'examples': ' | '.join(score['examples']),
                'xml_file': score['raw_xml_path']
            }
            writer.writerow(row)
    
    print(f"Training data saved to: {output_path}")

def main():
    """Main function to extract human scoring data."""
    
    # Path to the directory containing XML scoring sheets
    xml_directory = "/Volumes/code/discernus/pm/vanderveen_replication_extension/original_data/Democratic and Republican Candidates Coded Speeches"
    
    # Extract all scoring data
    print("Extracting human scoring data from XML files...")
    all_scores = extract_all_scoring_sheets(xml_directory)
    
    print(f"Successfully extracted data from {len(all_scores)} scoring sheets")
    
    # Save to CSV for training
    output_path = "/Volumes/code/discernus/pm/vanderveen_replication_extension/comparative_analysis/human_training_data.csv"
    save_training_data_to_csv(all_scores, output_path)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total scoring sheets processed: {len(all_scores)}")
    
    # Count scores by dimension
    manichaean_scores = [s['scoring_data'].get('manichaean_vision', {}).get('score', 0) for s in all_scores if 'manichaean_vision' in s['scoring_data']]
    people_scores = [s['scoring_data'].get('populist_notion_people', {}).get('score', 0) for s in all_scores if 'populist_notion_people' in s['scoring_data']]
    elite_scores = [s['scoring_data'].get('evil_elite', {}).get('score', 0) for s in all_scores if 'evil_elite' in s['scoring_data']]
    
    if manichaean_scores:
        print(f"Manichaean vision scores: {len(manichaean_scores)} (avg: {sum(manichaean_scores)/len(manichaean_scores):.2f})")
    else:
        print("Manichaean vision scores: 0")
        
    if people_scores:
        print(f"People notion scores: {len(people_scores)} (avg: {sum(people_scores)/len(people_scores):.2f})")
    else:
        print("People notion scores: 0")
        
    if elite_scores:
        print(f"Evil elite scores: {len(elite_scores)} (avg: {sum(elite_scores)/len(elite_scores):.2f})")
    else:
        print("Evil elite scores: 0")
    
    print(f"\nTraining data ready for PDAF tuning at: {output_path}")

if __name__ == "__main__":
    main()
