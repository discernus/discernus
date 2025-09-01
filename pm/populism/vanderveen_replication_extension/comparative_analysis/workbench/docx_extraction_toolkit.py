#!/usr/bin/env python3
"""
DOCX Extraction Toolkit for Van der Veen Scoring Sheets
Automatically extracts structured scoring data from Word documents
"""

import zipfile
import xml.etree.ElementTree as ET
import re
import csv
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json

@dataclass
class ScoringDimension:
    """Represents a scoring dimension with its metadata and descriptions."""
    name: str
    score: int
    populist_description: str
    pluralist_description: str
    examples: List[str]
    raw_text: str

@dataclass
class ScoringSheet:
    """Represents a complete scoring sheet."""
    metadata: Dict[str, str]
    dimensions: List[ScoringDimension]
    final_grade: Optional[int]
    raw_content: str
    file_path: str

class DOCXExtractor:
    """Extracts structured data from Word documents."""
    
    def __init__(self):
        self.namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
            'w15': 'http://schemas.microsoft.com/office/word/2012/wordml'
        }
    
    def extract_docx_content(self, docx_path: str) -> str:
        """Extract the main document content from a .docx file."""
        try:
            with zipfile.ZipFile(docx_path, 'r') as zip_file:
                # Get the main document XML
                xml_content = zip_file.read('word/document.xml')
                return xml_content.decode('utf-8')
        except Exception as e:
            print(f"Error reading DOCX file {docx_path}: {e}")
            return ""
    
    def parse_docx_xml(self, xml_content: str) -> ET.Element:
        """Parse the DOCX XML content."""
        try:
            root = ET.fromstring(xml_content)
            return root
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return None
    
    def extract_text_from_paragraphs(self, root: ET.Element) -> List[str]:
        """Extract text content from all paragraphs."""
        paragraphs = []
        for para in root.findall('.//w:p', self.namespaces):
            text_elements = para.findall('.//w:t', self.namespaces)
            para_text = ''.join([elem.text or '' for elem in text_elements])
            if para_text.strip():
                paragraphs.append(para_text.strip())
        return paragraphs
    
    def extract_table_data(self, root: ET.Element) -> List[List[str]]:
        """Extract data from tables in the document."""
        tables = []
        for table in root.findall('.//w:tbl', self.namespaces):
            table_data = []
            for row in table.findall('.//w:tr', self.namespaces):
                row_data = []
                for cell in row.findall('.//w:tc', self.namespaces):
                    text_elements = cell.findall('.//w:t', self.namespaces)
                    cell_text = ''.join([elem.text or '' for elem in text_elements])
                    row_data.append(cell_text.strip())
                if any(cell.strip() for cell in row_data):
                    table_data.append(row_data)
            if table_data:
                tables.append(table_data)
        return tables
    
    def extract_metadata(self, paragraphs: List[str]) -> Dict[str, str]:
        """Extract metadata from document paragraphs."""
        metadata = {}
        
        # Look for key metadata patterns
        patterns = {
            'politician': r'Name of politician:\s*(.+)',
            'speech_title': r'Title of Speech:\s*(.+)',
            'speech_date': r'Date of Speech:\s*(.+)',
            'grader': r'Grader:\s*(.+)',
            'grading_date': r'Date of grading:\s*(.+)',
            'category': r'Category:\s*(.+)'
        }
        
        for pattern_name, pattern in patterns.items():
            for para in paragraphs:
                match = re.search(pattern, para, re.IGNORECASE)
                if match:
                    metadata[pattern_name] = match.group(1).strip()
                    break
        
        return metadata
    
    def extract_final_grade(self, paragraphs: List[str]) -> Optional[int]:
        """Extract the final grade from the document."""
        for para in paragraphs:
            # Look for final grade patterns
            grade_match = re.search(r'Final Grade.*?(\d+)', para, re.IGNORECASE | re.DOTALL)
            if grade_match:
                return int(grade_match.group(1))
            
            # Also look for standalone grade numbers
            grade_match = re.search(r'^\s*(\d+)\s*$', para)
            if grade_match and 0 <= int(grade_match.group(1)) <= 2:
                return int(grade_match.group(1))
        
        return None
    
    def identify_scoring_dimensions(self, paragraphs: List[str], tables: List[List[str]]) -> List[ScoringDimension]:
        """Identify and extract scoring dimensions from the document."""
        dimensions = []
        
        # Define the expected scoring dimensions
        dimension_names = [
            'Manichaean vision',
            'Populist notion of the people', 
            'Evil elite'
        ]
        
        # Extract dimension descriptions from the document
        dimension_descriptions = {
            'Manichaean vision': {
                'populist': 'It conveys a Manichaean vision of the world, that is, one that is moral (every issue has a strong moral dimension) and dualistic (everything is in one category or the other, "right" or "wrong," "good" or "evil")',
                'pluralist': 'The discourse does not frame issues in moral terms or paint them in black-and-white. Instead, there is a strong tendency to focus on narrow, particular issues.'
            },
            'Populist notion of the people': {
                'populist': 'Although Manichaean, the discourse is still democratic, in the sense that the good is embodied in the will of the majority, which is seen as a unified whole, perhaps but not necessarily expressed in references to the "voluntad del pueblo"; however, the speaker ascribes a kind of unchanging essentialism to that will, rather than letting it be whatever 50 percent of the people want at any particular moment.',
                'pluralist': 'Democracy is simply the calculation of votes. This should be respected and is seen as the foundation of legitimate government, but it is not meant to be an exercise in arriving at a preexisting, knowable "will."'
            },
            'Evil elite': {
                'populist': 'The evil is embodied in a minority—more specifically, an elite—whose specific identity will vary according to context. Domestically, in Latin America it is often an economic elite, perhaps the "oligarchy," but it may also be a racial elite; internationally, it may be the United States or the capitalist, industrialized nations or international financiers or simply an ideology such as neoliberalism and capitalism.',
                'pluralist': 'The discourse avoids a conspiratorial tone and does not single out any evil ruling minority. It avoids labeling opponents as evil and may not even mention them in an effort to maintain a positive tone and keep passions low.'
            }
        }
        
        # Look for scores in tables
        table_scores = {}
        for table in tables:
            for row in table:
                if len(row) >= 2:
                    # Look for dimension names in first column
                    for dim_name in dimension_names:
                        if any(dim_name.lower() in cell.lower() for cell in row):
                            # Look for score in the same row
                            for cell in row[1:]:
                                score_match = re.search(r'(\d+)', cell)
                                if score_match:
                                    table_scores[dim_name] = int(score_match.group(1))
                                    break
        
        # Look for scores in paragraphs
        paragraph_scores = {}
        for para in paragraphs:
            for dim_name in dimension_names:
                if dim_name.lower() in para.lower():
                    # Look for score in the same paragraph
                    score_match = re.search(r'(\d+)', para)
                    if score_match:
                        paragraph_scores[dim_name] = int(score_match.group(1))
        
        # Combine scores from both sources
        all_scores = {**table_scores, **paragraph_scores}
        
        # Extract examples (quoted text)
        examples = []
        for para in paragraphs:
            quote_matches = re.findall(r'"([^"]+)"', para)
            for quote in quote_matches:
                if len(quote) > 20:  # Only keep substantial quotes
                    examples.append(quote)
        
        # Create dimension objects
        for dim_name in dimension_names:
            score = all_scores.get(dim_name, 0)
            desc = dimension_descriptions.get(dim_name, {})
            
            dimension = ScoringDimension(
                name=dim_name,
                score=score,
                populist_description=desc.get('populist', ''),
                pluralist_description=desc.get('pluralist', ''),
                examples=examples.copy(),  # Each dimension gets all examples for now
                raw_text=''  # Could extract specific text for each dimension
            )
            dimensions.append(dimension)
        
        return dimensions
    
    def extract_scoring_sheet(self, docx_path: str) -> ScoringSheet:
        """Extract a complete scoring sheet from a DOCX file."""
        print(f"Processing: {Path(docx_path).name}")
        
        # Extract content
        xml_content = self.extract_docx_content(docx_path)
        if not xml_content:
            return None
        
        # Parse XML
        root = self.parse_docx_xml(xml_content)
        if root is None:
            return None
        
        # Extract structured data
        paragraphs = self.extract_text_from_paragraphs(root)
        tables = self.extract_table_data(root)
        
        # Extract components
        metadata = self.extract_metadata(paragraphs)
        final_grade = self.extract_final_grade(paragraphs)
        dimensions = self.identify_scoring_dimensions(paragraphs, tables)
        
        return ScoringSheet(
            metadata=metadata,
            dimensions=dimensions,
            final_grade=final_grade,
            raw_content='\n'.join(paragraphs),
            file_path=docx_path
        )
    
    def extract_all_sheets(self, directory_path: str) -> List[ScoringSheet]:
        """Extract scoring data from all DOCX files in a directory."""
        docx_files = list(Path(directory_path).rglob("*.docx"))
        print(f"Found {len(docx_files)} DOCX files")
        
        all_sheets = []
        for docx_file in docx_files:
            try:
                sheet = self.extract_scoring_sheet(str(docx_file))
                if sheet:
                    all_sheets.append(sheet)
            except Exception as e:
                print(f"Error processing {docx_file.name}: {e}")
                continue
        
        return all_sheets
    
    def save_to_csv(self, sheets: List[ScoringSheet], output_path: str):
        """Save extracted data to CSV format."""
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'politician', 'speech_title', 'speech_date', 'grader', 'grading_date',
                'category', 'final_grade', 'manichaean_score', 'people_score', 'elite_score',
                'manichaean_populist_desc', 'manichaean_pluralist_desc',
                'people_populist_desc', 'people_pluralist_desc',
                'elite_populist_desc', 'elite_pluralist_desc',
                'examples', 'raw_content', 'file_path'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for sheet in sheets:
                # Find scores for each dimension
                manichaean_score = next((d.score for d in sheet.dimensions if 'manichaean' in d.name.lower()), '')
                people_score = next((d.score for d in sheet.dimensions if 'people' in d.name.lower()), '')
                elite_score = next((d.score for d in sheet.dimensions if 'elite' in d.name.lower()), '')
                
                # Get descriptions
                manichaean_dim = next((d for d in sheet.dimensions if 'manichaean' in d.name.lower()), None)
                people_dim = next((d for d in sheet.dimensions if 'people' in d.name.lower()), None)
                elite_dim = next((d for d in sheet.dimensions if 'elite' in d.name.lower()), None)
                
                row = {
                    'politician': sheet.metadata.get('politician', ''),
                    'speech_title': sheet.metadata.get('speech_title', ''),
                    'speech_date': sheet.metadata.get('speech_date', ''),
                    'grader': sheet.metadata.get('grader', ''),
                    'grading_date': sheet.metadata.get('grading_date', ''),
                    'category': sheet.metadata.get('category', ''),
                    'final_grade': sheet.final_grade or '',
                    'manichaean_score': manichaean_score,
                    'people_score': people_score,
                    'elite_score': elite_score,
                    'manichaean_populist_desc': manichaean_dim.populist_description if manichaean_dim else '',
                    'manichaean_pluralist_desc': manichaean_dim.pluralist_description if manichaean_dim else '',
                    'people_populist_desc': people_dim.populist_description if people_dim else '',
                    'people_pluralist_desc': people_dim.pluralist_description if people_dim else '',
                    'elite_populist_desc': elite_dim.populist_description if elite_dim else '',
                    'elite_pluralist_desc': elite_dim.pluralist_description if elite_dim else '',
                    'examples': ' | '.join(set([ex for d in sheet.dimensions for ex in d.examples])),
                    'raw_content': sheet.raw_content[:1000],  # Truncate for CSV
                    'file_path': sheet.file_path
                }
                writer.writerow(row)
        
        print(f"Data saved to: {output_path}")
    
    def save_to_json(self, sheets: List[ScoringSheet], output_path: str):
        """Save extracted data to JSON format for detailed analysis."""
        data = []
        for sheet in sheets:
            sheet_data = {
                'metadata': sheet.metadata,
                'final_grade': sheet.final_grade,
                'dimensions': [
                    {
                        'name': d.name,
                        'score': d.score,
                        'populist_description': d.populist_description,
                        'pluralist_description': d.pluralist_description,
                        'examples': d.examples
                    }
                    for d in sheet.dimensions
                ],
                'raw_content': sheet.raw_content,
                'file_path': sheet.file_path
            }
            data.append(sheet_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Detailed data saved to: {output_path}")

def main():
    """Main function to demonstrate the extraction toolkit."""
    
    # Initialize extractor
    extractor = DOCXExtractor()
    
    # Paths to directories containing DOCX files
    base_directory = "/Volumes/code/discernus/pm/vanderveen_replication_extension/original_data/Democratic and Republican Candidates Coded Speeches"
    democratic_dir = os.path.join(base_directory, "Democratic Candidates")
    republican_dir = os.path.join(base_directory, "Republican Candidates")
    
    print("DOCX Extraction Toolkit for Van der Veen Scoring Sheets")
    print("=" * 60)
    
    # Extract from both directories
    all_sheets = []
    
    print("Processing Democratic Candidates...")
    democratic_sheets = extractor.extract_all_sheets(democratic_dir)
    all_sheets.extend(democratic_sheets)
    
    print("Processing Republican Candidates...")
    republican_sheets = extractor.extract_all_sheets(republican_dir)
    all_sheets.extend(republican_sheets)
    
    if not all_sheets:
        print("No scoring sheets found. Please check the directory paths.")
        return
    
    print(f"Successfully extracted data from {len(all_sheets)} scoring sheets total")
    print(f"  - Democratic: {len(democratic_sheets)}")
    print(f"  - Republican: {len(republican_sheets)}")
    
    # Save to multiple formats
    csv_path = "/Volumes/code/discernus/pm/vanderveen_replication_extension/comparative_analysis/enhanced_training_data.csv"
    json_path = "/Volumes/code/discernus/pm/vanderveen_replication_extension/comparative_analysis/enhanced_training_data.json"
    
    extractor.save_to_csv(all_sheets, csv_path)
    extractor.save_to_json(all_sheets, json_path)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(f"Total scoring sheets processed: {len(all_sheets)}")
    
    # Count scores by dimension
    manichaean_scores = [d.score for sheet in all_sheets for d in sheet.dimensions if 'manichaean' in d.name.lower()]
    people_scores = [d.score for sheet in all_sheets for d in sheet.dimensions if 'people' in d.name.lower()]
    elite_scores = [d.score for sheet in all_sheets for d in sheet.dimensions if 'elite' in d.name.lower()]
    
    if manichaean_scores:
        print(f"Manichaean vision scores: {len(manichaean_scores)} (avg: {sum(manichaean_scores)/len(manichaean_scores):.2f})")
    if people_scores:
        print(f"People notion scores: {len(people_scores)} (avg: {sum(people_scores)/len(people_scores):.2f})")
    if elite_scores:
        print(f"Evil elite scores: {len(elite_scores)} (avg: {sum(elite_scores)/len(elite_scores):.2f})")
    
    # Count by party
    democratic_count = len([s for s in all_sheets if 'Democratic' in s.file_path])
    republican_count = len([s for s in all_sheets if 'Republican' in s.file_path])
    print(f"\nBreakdown by party:")
    print(f"  - Democratic candidates: {democratic_count}")
    print(f"  - Republican candidates: {republican_count}")
    
    print(f"\nTraining data ready for PDAF tuning!")
    print(f"CSV format: {csv_path}")
    print(f"JSON format: {json_path}")

if __name__ == "__main__":
    main()
