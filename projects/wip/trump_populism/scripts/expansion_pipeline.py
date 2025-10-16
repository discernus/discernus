#!/usr/bin/env python3
"""
Trump Populism Corpus Expansion Pipeline
=======================================

This script provides automated tools for corpus expansion using the centralized
corpus tools infrastructure. It integrates with the adversarial review expansion plan.

Usage:
    python expansion_pipeline.py --phase presidential --week 1
    python expansion_pipeline.py --phase business --week 2
    python expansion_pipeline.py --validate-all
    python expansion_pipeline.py --generate-report

Author: Discernus Project
Version: 1.0
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path("/Volumes/code/discernus/projects/2d_trump_populism")
CORPUS_ROOT = Path("/Volumes/code/discernus/corpus")
TOOLS_ROOT = CORPUS_ROOT / "tools"

class CorpusExpansionPipeline:
    """Main pipeline for Trump Populism corpus expansion using centralized tools."""

    def __init__(self):
        self.project_root = PROJECT_ROOT
        self.corpus_root = CORPUS_ROOT
        self.tools_root = TOOLS_ROOT

        # Phase configurations
        self.phases = {
            "presidential": {
                "week_1": self._expand_presidential_week1,
                "description": "Presidential governance content (SOTU 2017, foreign policy)"
            },
            "business": {
                "week_2": self._expand_business_week2,
                "description": "Business era content (1980s-2000s interviews, books)"
            },
            "direct": {
                "week_3": self._expand_direct_week3,
                "description": "Direct communication (social media, press conferences)"
            },
            "institutional": {
                "week_4": self._expand_institutional_week4,
                "description": "Institutional context (Congressional addresses, hearings)"
            }
        }

    def _run_tool(self, tool_name, args, cwd=None):
        """Run a centralized corpus tool."""
        tool_path = self.tools_root / tool_name
        if not tool_path.exists():
            # Try scripts directory
            tool_path = Path("/Volumes/code/discernus/scripts/corpus_tools") / tool_name

        cmd = ["python", str(tool_path)] + args
        print(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, cwd=cwd or self.corpus_root,
                                  capture_output=True, text=True, check=True)
            print(f"✅ Success: {tool_name}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running {tool_name}: {e}")
            print(f"Error output: {e.stderr}")
            return None

    def _expand_presidential_week1(self):
        """Week 1: Presidential governance content expansion."""
        print("🚀 Starting Week 1: Presidential Governance Content")
        print("=" * 60)

        # Step 1: Search existing political corpus
        print("\n📊 Step 1: Searching existing political corpus...")
        self._run_tool("query_corpus.py", [
            "--domain", "political",
            "--speaker", "Donald Trump",
            "--date-range", "2017-2020",
            "--output", str(self.project_root / "docs/expansion_reports/presidential_search.json")
        ])

        # Step 2: Extract missing 2017 SOTU
        print("\n📄 Step 2: Extracting 2017 State of the Union...")
        sotu_2017_url = "https://www.whitehouse.gov/briefing-room/speeches-remarks/2017/02/28/president-trumps-address-joint-session-congress/"
        output_dir = self.project_root / "corpus/analysis_ready/02_presidential_2017_2020/governance_core"

        self._run_tool("html_transcript_extractor.py", [
            "--url", sotu_2017_url,
            "--output", str(output_dir)
        ])

        # Step 3: Generate metadata
        print("\n🏷️ Step 3: Generating metadata...")
        self._run_tool("generate_corpus_metadata.py", [
            "--input", str(output_dir),
            "--schema", str(self.corpus_root / "metadata_schema.json"),
            "--output", str(self.project_root / "corpus/metadata")
        ])

        # Step 4: Validate content
        print("\n✅ Step 4: Validating content...")
        self._run_tool("validate_corpus.py", [
            "--input", str(output_dir),
            "--report", str(self.project_root / "docs/expansion_reports/week1_validation.html")
        ])

        print("\n🎉 Week 1 Complete!")

    def _expand_business_week2(self):
        """Week 2: Business era content expansion."""
        print("🚀 Starting Week 2: Business Era Content")
        print("=" * 60)

        # Step 1: Cross-reference business corpus
        print("\n📊 Step 1: Cross-referencing business corpus...")
        self._run_tool("query_corpus.py", [
            "--domain", "business",
            "--keywords", "real estate", "deal making",
            "--date-range", "1980-2000"
        ])

        # Step 2: Extract key interviews
        print("\n🎙️ Step 2: Extracting key interviews...")
        output_dir = self.project_root / "corpus/analysis_ready/05_baseline_1988_2000/media_appearances"

        # Oprah interview (if available)
        oprah_urls = [
            "https://example.com/oprah-trump-1988"  # Replace with actual URL
        ]

        for url in oprah_urls:
            self._run_tool("html_transcript_extractor.py", [
                "--url", url,
                "--output", str(output_dir)
            ])

        # Step 3: Standardize metadata
        print("\n🏷️ Step 3: Standardizing metadata...")
        self._run_tool("standardize_metadata.py", [
            "--input", str(output_dir),
            "--target-schema", str(self.corpus_root / "metadata_schema.json")
        ])

        print("\n🎉 Week 2 Complete!")

    def _expand_direct_week3(self):
        """Week 3: Direct communication expansion."""
        print("🚀 Starting Week 3: Direct Communication")
        print("=" * 60)

        # Step 1: Batch social media extraction
        print("\n📱 Step 1: Batch social media extraction...")

        # This would use the batch extraction tools
        print("Note: Social media extraction requires specific API access")
        print("Using available tools for press conference extraction...")

        # Step 2: Press conference extraction
        print("\n🎤 Step 2: Press conference extraction...")
        output_dir = self.project_root / "corpus/analysis_ready/02_presidential_2017_2020/crisis_response"

        # COVID briefings would go here
        covid_urls = [
            "https://example.com/covid-briefing-march-2020"  # Replace with actual URLs
        ]

        for url in covid_urls:
            self._run_tool("html_transcript_extractor.py", [
                "--url", url,
                "--output", str(output_dir)
            ])

        print("\n🎉 Week 3 Complete!")

    def _expand_institutional_week4(self):
        """Week 4: Institutional context expansion."""
        print("🚀 Starting Week 4: Institutional Context")
        print("=" * 60)

        # Step 1: Search congressional content
        print("\n🏛️ Step 1: Searching congressional content...")
        self._run_tool("query_corpus.py", [
            "--domain", "political",
            "--category", "congressional",
            "--keywords", "trump",
            "--date-range", "2017-2020"
        ])

        # Step 2: Extract joint session addresses
        print("\n📜 Step 2: Extracting joint session addresses...")
        output_dir = self.project_root / "corpus/analysis_ready/02_presidential_2017_2020/institutional"

        # Additional joint sessions beyond what we have
        joint_session_urls = [
            "https://example.com/joint-session-2019"  # Replace with actual URLs
        ]

        for url in joint_session_urls:
            self._run_tool("html_transcript_extractor.py", [
                "--url", url,
                "--output", str(output_dir)
            ])

        print("\n🎉 Week 4 Complete!")

    def run_expansion(self, phase, week):
        """Run expansion for specified phase and week."""
        if phase not in self.phases:
            print(f"❌ Invalid phase: {phase}")
            print(f"Available phases: {list(self.phases.keys())}")
            return

        if f"week_{week}" not in self.phases[phase]:
            print(f"❌ Invalid week: {week}")
            print(f"Available weeks for {phase}: {[w.replace('week_', '') for w in self.phases[phase].keys() if w.startswith('week_')]}")
            return

        print(f"🎯 Starting {phase} expansion - Week {week}")
        print(f"Description: {self.phases[phase]['description']}")
        print("=" * 80)

        # Run the expansion
        self.phases[phase][f"week_{week}"]()

    def validate_all(self):
        """Validate all corpus content."""
        print("🔍 Validating all corpus content...")
        print("=" * 60)

        analysis_ready = self.project_root / "corpus/analysis_ready"

        self._run_tool("validate_corpus.py", [
            "--input", str(analysis_ready),
            "--comprehensive",
            "--report", str(self.project_root / "docs/expansion_reports/full_validation.html")
        ])

        print("✅ Validation complete!")

    def generate_report(self):
        """Generate expansion progress report."""
        print("📊 Generating expansion progress report...")
        print("=" * 60)

        # Count documents in each phase
        analysis_ready = self.project_root / "corpus/analysis_ready"
        phase_counts = {}

        for phase_dir in analysis_ready.iterdir():
            if phase_dir.is_dir():
                count = len(list(phase_dir.glob("*.txt")))
                phase_counts[phase_dir.name] = count

        # Generate report
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_documents": sum(phase_counts.values()),
            "phase_breakdown": phase_counts,
            "target_documents": 180,
            "completion_percentage": round(sum(phase_counts.values()) / 180 * 100, 1)
        }

        report_path = self.project_root / "docs/expansion_reports/progress_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📊 Report generated: {report_path}")
        print(f"Current progress: {report['total_documents']}/180 documents ({report['completion_percentage']}%)")


def main():
    parser = argparse.ArgumentParser(description="Trump Populism Corpus Expansion Pipeline")
    parser.add_argument("--phase", choices=["presidential", "business", "direct", "institutional"],
                       help="Expansion phase to run")
    parser.add_argument("--week", type=int, choices=[1, 2, 3, 4],
                       help="Week number for the phase")
    parser.add_argument("--validate-all", action="store_true",
                       help="Validate all corpus content")
    parser.add_argument("--generate-report", action="store_true",
                       help="Generate progress report")

    args = parser.parse_args()

    pipeline = CorpusExpansionPipeline()

    if args.validate_all:
        pipeline.validate_all()
    elif args.generate_report:
        pipeline.generate_report()
    elif args.phase and args.week:
        pipeline.run_expansion(args.phase, args.week)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
