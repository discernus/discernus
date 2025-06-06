#!/usr/bin/env python3
"""
Demonstration of Corpus Generation Tooling

This script demonstrates the automated tools for generating JSON Schema skeletons
and creating JSONL corpus files from various source formats.
"""

import sys
import subprocess
from pathlib import Path
import json

def run_command(cmd, description):
    """Run a command and display results"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stdout:
            print("✅ Output:")
            print(result.stdout)
        if result.stderr:
            print("⚠️  Warnings:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error:", e.stderr)

def create_sample_files():
    """Create sample files for demonstration"""
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Create a sample markdown file with frontmatter
    markdown_content = """---
text_id: "sample_speech_001"
title: "The Future of Democracy"
document_type: "speech"
author: "Jane Doe"
date: "2024-01-15T14:30:00Z"
publication: "Democracy Conference 2024"
medium: "online"
campaign_name: "Future Leaders Initiative"
audience_size: 500
source_url: "https://example.com/speech"
document_metadata:
  venue: "Washington DC"
  event_type: "keynote"
  duration_minutes: 45
---

# The Future of Democracy

Ladies and gentlemen, distinguished guests, thank you for joining us today for this important conversation about the future of democracy.

## Challenges We Face

In our interconnected world, we face unprecedented challenges that test the very foundations of democratic institutions. From misinformation campaigns to economic inequality, from climate change to technological disruption, these forces require us to rethink how democracy can adapt and thrive.

We must acknowledge that traditional approaches may not be sufficient for the complex problems of the 21st century. The speed of change demands new forms of civic engagement and decision-making processes.

## Opportunities for Innovation

However, within these challenges lie tremendous opportunities. Digital technologies can enhance transparency and participation. Artificial intelligence can help us process complex policy data. Blockchain technology might secure voting systems.

The key is ensuring that these innovations serve to strengthen, not weaken, democratic values and institutions.

## A Call to Action

I call upon each of you to become active participants in shaping this future. Democracy is not a spectator sport - it requires the engagement of informed, committed citizens who are willing to work together across differences.

Together, we can build a democracy that is more inclusive, more responsive, and more resilient than ever before.

Thank you."""
    
    with open(examples_dir / "sample_speech.md", "w") as f:
        f.write(markdown_content)
    
    # Create a sample CSV file
    csv_content = """text_id,title,document_type,author,date,content
op_ed_001,The Digital Divide,op_ed,John Smith,2024-01-10T09:00:00Z,"The digital divide represents one of the most pressing challenges of our time. As technology advances at breakneck speed, we risk leaving behind entire communities who lack access to high-speed internet, modern devices, or digital literacy skills."
article_002,Climate Action Now,article,Maria Garcia,2024-01-12T15:30:00Z,"Climate change is not a distant threat - it is happening now, and its effects are being felt across the globe. From rising sea levels to extreme weather events, the evidence is overwhelming that immediate action is required."
pamphlet_003,Voter Registration Guide,pamphlet,Election Commission,2024-01-05T10:00:00Z,"This guide provides step-by-step instructions for registering to vote in the upcoming election. Every eligible citizen has the right and responsibility to participate in our democratic process."
"""
    
    with open(examples_dir / "sample_documents.csv", "w") as f:
        f.write(csv_content)
    
    # Create a plain text file
    text_content = """The Constitution of the United States begins with the words 'We the People,' establishing the fundamental principle that government derives its power from the consent of the governed.

This revolutionary concept, first articulated in the Declaration of Independence and later enshrined in our founding documents, represents a radical departure from the monarchical systems that dominated the world in the 18th century.

The framers understood that democracy is not merely about majority rule, but about protecting the rights of all citizens while ensuring that government remains accountable to the people it serves."""
    
    with open(examples_dir / "constitution_excerpt.txt", "w") as f:
        f.write(text_content)
    
    print("✅ Created sample files:")
    print(f"  - {examples_dir / 'sample_speech.md'} (Markdown with frontmatter)")
    print(f"  - {examples_dir / 'sample_documents.csv'} (CSV format)")
    print(f"  - {examples_dir / 'constitution_excerpt.txt'} (Plain text)")

def main():
    """Main demonstration function"""
    print("🚀 Corpus Generation Tooling Demonstration")
    print("This demo shows how to use the schema generator and JSONL generator tools")
    
    # Create sample files
    create_sample_files()
    
    # Paths
    examples_dir = Path("examples")
    schema_path = Path("schemas/core_schema_v1.0.0.json")
    cli_dir = Path("src/cli")
    
    # 1. Test schema generation from existing JSONL
    print("\n" + "="*80)
    print("🔧 PART 1: JSON Schema Generation")
    print("="*80)
    
    run_command([
        sys.executable, str(cli_dir / "schema_generator.py"),
        "--input", "test_data/sample_corpus.jsonl",
        "--output", str(examples_dir / "generated_schema.json"),
        "--title", "Generated Schema from Sample Data",
        "--description", "Auto-generated schema from existing corpus data"
    ], "Generate schema from existing JSONL file")
    
    # 2. Validate existing data against core schema
    run_command([
        sys.executable, str(cli_dir / "schema_generator.py"),
        "--input", "test_data/sample_corpus.jsonl",
        "--validate-against", str(schema_path),
        "--show-errors"
    ], "Validate existing data against core schema")
    
    # 3. Generate JSONL from different source formats
    print("\n" + "="*80)
    print("🏗️  PART 2: JSONL Corpus Generation")
    print("="*80)
    
    # From Markdown with frontmatter
    run_command([
        sys.executable, str(cli_dir / "jsonl_generator.py"),
        "--input", str(examples_dir / "sample_speech.md"),
        "--output", str(examples_dir / "from_markdown.jsonl"),
        "--format", "markdown",
        "--chunk-type", "sectional",
        "--schema", str(schema_path)
    ], "Generate JSONL from Markdown file with frontmatter")
    
    # From CSV
    run_command([
        sys.executable, str(cli_dir / "jsonl_generator.py"),
        "--input", str(examples_dir / "sample_documents.csv"),
        "--output", str(examples_dir / "from_csv.jsonl"),
        "--format", "csv",
        "--csv-text-column", "content",
        "--chunk-type", "fixed",
        "--chunk-size", "500",
        "--schema", str(schema_path)
    ], "Generate JSONL from CSV file")
    
    # From plain text with metadata override
    run_command([
        sys.executable, str(cli_dir / "jsonl_generator.py"),
        "--input", str(examples_dir / "constitution_excerpt.txt"),
        "--output", str(examples_dir / "from_text.jsonl"),
        "--format", "text",
        "--chunk-type", "semantic",
        "--metadata", '{"author": "Founding Fathers", "document_type": "article", "title": "Constitutional Principles"}',
        "--schema", str(schema_path)
    ], "Generate JSONL from plain text with metadata override")
    
    # 4. Combine all generated files
    print("\n" + "="*80)
    print("🔗 PART 3: Combining Multiple Sources")
    print("="*80)
    
    run_command([
        sys.executable, str(cli_dir / "jsonl_generator.py"),
        "--input", 
        str(examples_dir / "sample_speech.md"),
        str(examples_dir / "sample_documents.csv"),
        str(examples_dir / "constitution_excerpt.txt"),
        "--output", str(examples_dir / "combined_corpus.jsonl"),
        "--format", "auto",
        "--chunk-type", "fixed",
        "--chunk-size", "800",
        "--schema", str(schema_path)
    ], "Generate combined JSONL from multiple source formats")
    
    # 5. Validate generated corpus
    run_command([
        sys.executable, str(cli_dir / "jsonl_generator.py"),
        "--input", str(examples_dir / "combined_corpus.jsonl"),
        "--validate-only",
        "--schema", str(schema_path)
    ], "Validate the generated combined corpus")
    
    # Show summary
    print("\n" + "="*80)
    print("📊 GENERATION SUMMARY")
    print("="*80)
    
    output_files = [
        examples_dir / "generated_schema.json",
        examples_dir / "from_markdown.jsonl", 
        examples_dir / "from_csv.jsonl",
        examples_dir / "from_text.jsonl",
        examples_dir / "combined_corpus.jsonl"
    ]
    
    for file_path in output_files:
        if file_path.exists():
            size = file_path.stat().st_size
            if file_path.suffix == '.jsonl':
                with open(file_path, 'r') as f:
                    record_count = sum(1 for line in f if line.strip())
                print(f"✅ {file_path}: {size} bytes, {record_count} records")
            else:
                print(f"✅ {file_path}: {size} bytes")
        else:
            print(f"❌ {file_path}: Not found")
    
    print("\n🎉 Demonstration complete! Check the examples/ directory for generated files.")
    print("\nNext steps:")
    print("  1. Review the generated schema and JSONL files")
    print("  2. Test uploading the JSONL files to your API")
    print("  3. Customize the chunking strategies for your specific use case")
    print("  4. Create your own source files and generate a production corpus")

if __name__ == "__main__":
    main() 