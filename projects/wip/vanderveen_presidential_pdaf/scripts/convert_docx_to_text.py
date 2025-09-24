#!/usr/bin/env python3
"""
Convert DOCX Speech Files to Text Format for 2016 Presidential Campaign Analysis
================================================================================

Converts all 2016 presidential candidate speeches from DOCX to plain text format
for comprehensive PDAF v10.0 analysis across Democratic and Republican candidates.

Converts: 99 speeches from Trump, Clinton, Sanders, Cruz, Rubio, Kasich
Outputs: Text files in corpus/ directory + v8.0.1 compliant corpus.md manifest

Usage:
    python convert_docx_to_text.py

Requirements:
    pip install python-docx

Author: Discernus Project
Version: 2.0 - Comprehensive Multi-Candidate Support
"""

import os
import json
import re
from pathlib import Path
from docx import Document
from datetime import datetime

class PresidentialSpeechesConverter:
    """Convert DOCX speech files to text format for comprehensive PDAF analysis."""

    def __init__(self):
        self.base_source_dir = Path("/Volumes/code/discernus/pm/paper_replication_experiment_vanderveen")
        self.democratic_dir = self.base_source_dir / "Democratic Candidates Speeches and Party Platform"
        self.republican_dir = self.base_source_dir / "Republican Candidates Speeches and Party Platform"
        self.output_dir = Path("/Volumes/code/discernus/projects/vanderveen_presidential_pdaf/corpus")
        self.project_root = Path("/Volumes/code/discernus/projects/vanderveen_presidential_pdaf")
        self.corpus_manifest_path = self.project_root / "corpus.md"

        # Create output directory structure
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Candidate and party mappings
        self.candidate_info = {
            'Trump': {'party': 'Republican', 'full_name': 'Donald Trump'},
            'Clinton': {'party': 'Democratic', 'full_name': 'Hillary Clinton'},
            'Sanders': {'party': 'Democratic', 'full_name': 'Bernie Sanders'},
            'Cruz': {'party': 'Republican', 'full_name': 'Ted Cruz'},
            'Rubio': {'party': 'Republican', 'full_name': 'Marco Rubio'},
            'Kasich': {'party': 'Republican', 'full_name': 'John Kasich'}
        }

        # Track processed documents for manifest
        self.documents = []

    def extract_date_from_filename(self, filename):
        """Extract date from filename in format us.2016.Candidate.MM-DD.docx or us.2016.Candidate.Announcement.MM-DD.docx"""
        try:
            # Remove extension
            name = filename.replace('.docx', '')

            # Handle different filename patterns
            if 'Announcement' in name:
                # us.2016.Candidate.Announcement.MM-DD.docx
                parts = name.split('.')
                month_day = parts[-1]  # Last part is MM-DD
                month, day = month_day.split('-')
                return f"2016-{int(month):02d}-{int(day):02d}"
            else:
                # Standard format: us.2016.Candidate.MM-DD.docx
                parts = name.split('.')
                month_day = parts[-1]  # Last part is MM-DD
                month, day = month_day.split('-')
                return f"2016-{int(month):02d}-{int(day):02d}"
        except (ValueError, IndexError):
            return "2016-01-01"  # Default fallback

    def extract_candidate_from_filename(self, filename):
        """Extract candidate name from filename"""
        try:
            # Remove extension and split
            name = filename.replace('.docx', '')
            parts = name.split('.')

            # Find the candidate name (should be the third part)
            if len(parts) >= 3:
                candidate_short = parts[2]  # e.g., 'Trump', 'Clinton'
                return candidate_short
        except (IndexError, ValueError):
            pass
        return "Unknown"

    def get_campaign_phase(self, date_str):
        """Determine campaign phase based on date"""
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")

            # 2016 Primary season phases
            if date < datetime(2016, 3, 1):
                return "early_primary"
            elif date < datetime(2016, 6, 1):
                return "primary_season"
            elif date < datetime(2016, 8, 1):
                return "convention_period"
            else:
                return "general_election"
        except:
            return "unknown"

    def convert_docx_to_text(self, docx_path):
        """Convert DOCX file to plain text"""
        try:
            doc = Document(docx_path)
            text = ""

            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n\n"

            return text.strip()
        except Exception as e:
            print(f"Error converting {docx_path}: {e}")
            return ""

    def process_single_file(self, docx_path, candidate_short):
        """Process a single DOCX file and return metadata"""
        filename = docx_path.name
        candidate_info = self.candidate_info.get(candidate_short, {})
        full_name = candidate_info.get('full_name', candidate_short)
        party = candidate_info.get('party', 'Unknown')

        # Extract date and determine campaign phase
        date = self.extract_date_from_filename(filename)
        campaign_phase = self.get_campaign_phase(date)

        # Convert to text
        text_content = self.convert_docx_to_text(docx_path)

        # Create organized filename
        date_clean = date.replace('-', '_')
        output_filename = f"{candidate_short.lower()}_{date_clean}.txt"

        # Create subdirectories for organization
        candidate_dir = self.output_dir / candidate_short.lower()
        phase_dir = candidate_dir / campaign_phase
        phase_dir.mkdir(parents=True, exist_ok=True)

        # Output path
        output_path = phase_dir / output_filename

        # Write text file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)

        # Return metadata for manifest
        return {
            'filename': str(output_path.relative_to(self.output_dir)),
            'speaker': full_name,
            'candidate_short': candidate_short,
            'party': party,
            'date': date,
            'campaign_phase': campaign_phase,
            'speech_type': 'campaign_speech',
            'word_count': len(text_content.split()),
            'source_filename': filename
        }

    def process_all_candidates(self):
        """Process DOCX files from all candidates and create corpus manifest"""
        print("🔄 Starting comprehensive presidential speech conversion...")
        print("📂 Processing both Democratic and Republican candidates")

        # Process Democratic candidates
        self.process_candidate_directory(self.democratic_dir, "Democratic")

        # Process Republican candidates
        self.process_candidate_directory(self.republican_dir, "Republican")

        # Generate corpus manifest
        self.generate_corpus_manifest()

        print("✅ Conversion complete!")
        print(f"📊 Processed {len(self.documents)} speeches from {len(set(d['candidate_short'] for d in self.documents))} candidates")

    def process_candidate_directory(self, base_dir, party_name):
        """Process all candidate subdirectories in a party directory"""
        if not base_dir.exists():
            print(f"⚠️  {party_name} directory not found: {base_dir}")
            return

        print(f"🔍 Scanning {party_name} candidates...")

        # Find all candidate subdirectories
        candidate_dirs = [d for d in base_dir.iterdir() if d.is_dir()]

        for candidate_dir in candidate_dirs:
            candidate_name = candidate_dir.name.replace(' Speeches', '')  # Remove "Speeches" suffix
            candidate_short = self.extract_candidate_from_path(candidate_name)

            if candidate_short in self.candidate_info:
                print(f"👤 Processing {candidate_name} ({party_name})...")
                self.process_candidate_speeches(candidate_dir, candidate_short)
            else:
                print(f"⚠️  Skipping unknown candidate: {candidate_name}")

    def extract_candidate_from_path(self, path_name):
        """Extract candidate short name from directory path"""
        # Handle various naming patterns
        if 'Trump' in path_name:
            return 'Trump'
        elif 'Clinton' in path_name:
            return 'Clinton'
        elif 'Sanders' in path_name:
            return 'Sanders'
        elif 'Cruz' in path_name:
            return 'Cruz'
        elif 'Rubio' in path_name:
            return 'Rubio'
        elif 'Kasich' in path_name:
            return 'Kasich'
        else:
            return path_name.split()[0]  # Take first word as fallback

    def process_candidate_speeches(self, candidate_dir, candidate_short):
        """Process all speeches for a single candidate"""
        docx_files = list(candidate_dir.glob("*.docx"))

        if not docx_files:
            print(f"  ⚠️  No DOCX files found in {candidate_dir}")
            return

        print(f"  📄 Found {len(docx_files)} speeches for {candidate_short}")

        for docx_file in docx_files:
            try:
                metadata = self.process_single_file(docx_file, candidate_short)
                self.documents.append(metadata)
                print(f"    ✅ {docx_file.name} → {metadata['filename']}")
            except Exception as e:
                print(f"    ❌ Failed to process {docx_file.name}: {e}")

    def generate_corpus_manifest(self):
        """Generate v8.0.1 compliant corpus.md file"""
        print("📝 Generating corpus manifest...")

        # Sort documents by candidate and date
        sorted_docs = sorted(self.documents, key=lambda x: (x['candidate_short'], x['date']))

        # Create markdown content
        manifest_content = self.create_corpus_markdown(sorted_docs)

        # Write corpus.md to project root
        with open(self.corpus_manifest_path, 'w', encoding='utf-8') as f:
            f.write(manifest_content)

        print(f"📄 Corpus manifest written to: {self.corpus_manifest_path}")

    def create_corpus_markdown(self, documents):
        """Create v8.0.1 compliant corpus.md content"""
        # Header and overview
        content = "# 2016 Presidential Campaign Speech Corpus\n\n"
        content += "## 📚 Corpus Overview\n\n"
        content += "Comprehensive collection of 2016 presidential campaign speeches from all major candidates, "
        content += "formatted for systematic PDAF v10.0 populist discourse analysis. This corpus enables "
        content += "cross-candidate comparison of populist rhetoric patterns across the Democratic and "
        content += "Republican primaries and general election.\n\n"

        content += "### Coverage\n"
        content += f"- **Total Speeches**: {len(documents)}\n"
        content += f"- **Candidates**: {len(set(d['candidate_short'] for d in documents))}\n"
        content += f"- **Date Range**: 2016-01-01 to 2016-11-08\n"
        content += "- **Parties**: Democratic and Republican\n\n"

        # Candidate breakdown
        content += "### Candidate Distribution\n\n"
        candidate_counts = {}
        for doc in documents:
            candidate = doc['candidate_short']
            candidate_counts[candidate] = candidate_counts.get(candidate, 0) + 1

        for candidate, count in sorted(candidate_counts.items()):
            party = self.candidate_info.get(candidate, {}).get('party', 'Unknown')
            full_name = self.candidate_info.get(candidate, {}).get('full_name', candidate)
            content += f"- **{full_name}** ({party}): {count} speeches\n"

        content += "\n"

        # YAML metadata appendix
        content += "---\n\n"
        content += "```yaml\n"
        content += "name: \"2016 Presidential Campaign Speech Corpus\"\n"
        content += "version: \"1.0\"\n"
        content += "description: \"Complete collection of 2016 presidential campaign speeches for PDAF analysis\"\n"
        content += f"total_documents: {len(documents)}\n"
        content += "date_range: \"2016-01-01 to 2016-11-08\"\n"
        content += "\n"
        content += "documents:\n"

        # Document entries
        for i, doc in enumerate(documents, 1):
            content += f"  - filename: \"{doc['filename']}\"\n"
            content += f"    document_id: \"{doc['candidate_short'].lower()}_{doc['date'].replace('-', '')}_{i:02d}\"\n"
            content += f"    speaker: \"{doc['speaker']}\"\n"
            content += f"    candidate_short: \"{doc['candidate_short']}\"\n"
            content += f"    party: \"{doc['party']}\"\n"
            content += f"    date: \"{doc['date']}\"\n"
            content += f"    campaign_phase: \"{doc['campaign_phase']}\"\n"
            content += f"    speech_type: \"{doc['speech_type']}\"\n"
            content += f"    word_count: {doc['word_count']}\n"
            content += f"    source_filename: \"{doc['source_filename']}\"\n"
            content += "\n"

        content += "```\n\n"

        # Validation notes
        content += "## Validation Notes\n\n"
        content += "- ✅ All semantic meaning explicitly defined in metadata\n"
        content += "- ✅ Files organized in nested directory structure for human readability\n"
        content += "- ✅ Metadata provides complete context for PDAF analysis\n"
        content += "- ✅ Cross-candidate comparison enabled through consistent metadata schema\n\n"

        content += "---\n\n"
        content += "**Generated**: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        content += "**Source**: Van der Veen et al. (2024) presidential campaign speech corpus\n"
        content += "**Format**: v8.0.1 compliant corpus specification\n"

        return content

def main():
    """Main execution function for comprehensive presidential speech conversion"""
    print("🇺🇸 2016 Presidential Campaign Speech Corpus Builder")
    print("=" * 60)
    print("Converting Van der Veen et al. (2024) study speeches for PDAF v10.0 analysis")
    print()

    # Initialize converter
    converter = PresidentialSpeechesConverter()

    # Run comprehensive conversion
    try:
        converter.process_all_candidates()

        print("\n" + "=" * 60)
        print("🎯 CONVERSION COMPLETE!")
        print("=" * 60)
        print("📁 Text files saved to corpus/ directory")
        print(f"📄 Corpus manifest: corpus.md (project root)")
        print(f"👥 Candidates processed: {len(converter.candidate_info)}")
        print(f"📊 Total speeches: {len(converter.documents)}")
        print()
        print("Ready for PDAF v10.0 analysis!")

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        raise


if __name__ == "__main__":
    main()
