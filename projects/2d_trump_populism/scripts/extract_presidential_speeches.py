#!/usr/bin/env python3
"""
Presidential Speeches Extraction Script
========================================

Extracts and processes presidential speeches from the Van der Veen et al. (2024)
replication study for PDAF v10.0 analysis.

Usage:
    python extract_presidential_speeches.py --source vanderveen
    python extract_presidential_speeches.py --source biden
    python extract_presidential_speeches.py --source historical
    python extract_presidential_speeches.py --all

Author: Discernus Project
Version: 1.0
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
import shutil

class PresidentialSpeechesExtractor:
    """Extract and process presidential speeches for PDAF analysis."""

    def __init__(self):
        self.project_root = Path("/Volumes/code/discernus/projects/2d_trump_populism")
        self.source_root = Path("/Volumes/code/discernus/pm/paper_replication_experiment_vanderveen")
        self.biden_root = Path("/Volumes/code/discernus/projects/1b_chf_constitutional_health/corpus")
        self.output_root = self.project_root / "corpus" / "analysis_ready" / "06_presidential_replication"

        # Create output directory
        self.output_root.mkdir(parents=True, exist_ok=True)

    def extract_vanderveen_trump_speeches(self) -> List[Dict[str, Any]]:
        """Extract Trump speeches from Van der Veen replication study."""
        speeches = []

        # Trump announcement speech
        trump_file = self.source_root / "trump_announcement_2016_06_16.txt"
        if trump_file.exists():
            with open(trump_file, 'r', encoding='utf-8') as f:
                content = f.read()

            speech = {
                "id": "trump_2016_announcement",
                "speaker": "Donald Trump",
                "date": "2016-06-16",
                "title": "Presidential Campaign Announcement Speech",
                "context": "campaign_announcement",
                "source": "vanderveen_replication",
                "content": content,
                "word_count": len(content.split()),
                "file_path": str(self.output_root / "trump_2016_announcement.txt")
            }
            speeches.append(speech)

            # Write to output file
            with open(speech["file_path"], 'w', encoding='utf-8') as f:
                f.write(content)

        # Look for other Trump speeches in subdirectories
        trump_speeches_dir = self.source_root / "Republican Candidates Speeches and Party Platform" / "Trump Speeches"
        if trump_speeches_dir.exists():
            for txt_file in trump_speeches_dir.glob("*.txt"):
                try:
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract metadata from filename
                    filename = txt_file.stem
                    speech_id = f"trump_{filename.replace(' ', '_').lower()}"

                    speech = {
                        "id": speech_id,
                        "speaker": "Donald Trump",
                        "date": "2016-01-01",  # Default, would need manual curation
                        "title": filename.replace('_', ' ').title(),
                        "context": "campaign_2016",
                        "source": "vanderveen_replication",
                        "content": content,
                        "word_count": len(content.split()),
                        "file_path": str(self.output_root / f"{speech_id}.txt")
                    }
                    speeches.append(speech)

                    # Write to output file
                    with open(speech["file_path"], 'w', encoding='utf-8') as f:
                        f.write(content)

                except Exception as e:
                    print(f"Error processing {txt_file}: {e}")

        return speeches

    def extract_biden_speeches(self) -> List[Dict[str, Any]]:
        """Extract Biden speeches from constitutional health project."""
        speeches = []

        if not self.biden_root.exists():
            print(f"Biden corpus not found at {self.biden_root}")
            return speeches

        # Look for Biden SOTU and other presidential addresses
        biden_files = [
            "Biden_SOTU_2021.txt",
            "Biden_SOTU_2022.txt",
            "Biden_SOTU_2023.txt",
            "Biden_SOTU_2024.txt"
        ]

        for filename in biden_files:
            file_path = self.biden_root / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    year = filename.split('_')[2][:4]
                    speech_id = f"biden_{year}_sotu"

                    speech = {
                        "id": speech_id,
                        "speaker": "Joe Biden",
                        "date": f"{year}-01-01",  # Approximate
                        "title": f"State of the Union Address {year}",
                        "context": "state_of_union",
                        "source": "constitutional_health_project",
                        "content": content,
                        "word_count": len(content.split()),
                        "file_path": str(self.output_root / f"{speech_id}.txt")
                    }
                    speeches.append(speech)

                    # Write to output file
                    with open(speech["file_path"], 'w', encoding='utf-8') as f:
                        f.write(content)

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        return speeches

    def extract_historical_speeches(self) -> List[Dict[str, Any]]:
        """Extract historical presidential speeches for comparison."""
        speeches = []

        if not self.biden_root.exists():
            print(f"Historical corpus not found at {self.biden_root}")
            return speeches

        # Look for historical presidential speeches
        historical_files = [
            "Trump_SOTU_2018.txt",
            "Trump_SOTU_2019.txt",
            "Trump_SOTU_2020.txt",
            "Obama_SOTU_2016.txt",
            "Bush_SOTU_2008.txt",
            "Clinton_SOTU_2000.txt"
        ]

        for filename in historical_files:
            file_path = self.biden_root / filename
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract speaker and year from filename
                    parts = filename.split('_')
                    speaker = parts[0]
                    year = parts[2][:4] if len(parts) > 2 else "unknown"

                    speech_id = f"{speaker.lower()}_{year}_sotu"

                    speech = {
                        "id": speech_id,
                        "speaker": speaker,
                        "date": f"{year}-01-01",
                        "title": f"State of the Union Address {year}",
                        "context": "state_of_union",
                        "source": "constitutional_health_project",
                        "content": content,
                        "word_count": len(content.split()),
                        "file_path": str(self.output_root / f"{speech_id}.txt")
                    }
                    speeches.append(speech)

                    # Write to output file
                    with open(speech["file_path"], 'w', encoding='utf-8') as f:
                        f.write(content)

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        return speeches

    def create_manifest(self, speeches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create manifest.json for the presidential corpus."""
        manifest = {
            "experiment": "Presidential Populism Replication Study",
            "framework": "PDAF v10.0",
            "description": "Replication of Van der Veen et al. (2024) using PDAF v10.0 framework",
            "created": "2025-01-30",
            "total_speeches": len(speeches),
            "sources": list(set(s["source"] for s in speeches)),
            "speakers": list(set(s["speaker"] for s in speeches)),
            "contexts": list(set(s["context"] for s in speeches)),
            "speeches": speeches
        }

        # Add statistics
        manifest["statistics"] = {
            "total_words": sum(s["word_count"] for s in speeches),
            "avg_words_per_speech": round(sum(s["word_count"] for s in speeches) / len(speeches), 0),
            "speakers_count": len(set(s["speaker"] for s in speeches)),
            "contexts_count": len(set(s["context"] for s in speeches))
        }

        return manifest

    def run_extraction(self, sources: List[str]) -> Dict[str, Any]:
        """Run extraction for specified sources."""
        all_speeches = []

        if "vanderveen" in sources or "all" in sources:
            print("📄 Extracting Van der Veen Trump speeches...")
            all_speeches.extend(self.extract_vanderveen_trump_speeches())

        if "biden" in sources or "all" in sources:
            print("📄 Extracting Biden speeches...")
            all_speeches.extend(self.extract_biden_speeches())

        if "historical" in sources or "all" in sources:
            print("📄 Extracting historical presidential speeches...")
            all_speeches.extend(self.extract_historical_speeches())

        print(f"✅ Extracted {len(all_speeches)} speeches")

        # Create manifest
        manifest = self.create_manifest(all_speeches)

        # Save manifest
        manifest_path = self.output_root / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        print(f"📋 Manifest saved to {manifest_path}")

        return manifest


def main():
    parser = argparse.ArgumentParser(description="Extract presidential speeches for PDAF analysis")
    parser.add_argument("--source", choices=["vanderveen", "biden", "historical", "all"],
                       action='append', help="Source to extract from")
    parser.add_argument("--output-dir", help="Output directory (default: auto-generated)")

    args = parser.parse_args()

    if not args.source:
        args.source = ["vanderveen"]  # Default to Van der Veen study

    extractor = PresidentialSpeechesExtractor()

    if args.output_dir:
        extractor.output_root = Path(args.output_dir)
        extractor.output_root.mkdir(parents=True, exist_ok=True)

    print("🎯 Starting Presidential Speeches Extraction")
    print("=" * 50)

    manifest = extractor.run_extraction(args.source)

    print("\n📊 Extraction Summary:")
    print(f"Total speeches: {manifest['total_speeches']}")
    print(f"Total words: {manifest['statistics']['total_words']:,}")
    print(f"Avg words/speech: {manifest['statistics']['avg_words_per_speech']:,}")
    print(f"Speakers: {', '.join(manifest['speakers'])}")
    print(f"Sources: {', '.join(manifest['sources'])}")

    print("\n✅ Extraction complete!")
    print(f"Output directory: {extractor.output_root}")
    print(f"Manifest: {extractor.output_root}/manifest.json")


if __name__ == "__main__":
    main()
