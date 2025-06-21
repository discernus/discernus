#!/usr/bin/env python3
"""
CLI tool for Intelligent Corpus Ingestion Service

Usage:
    python scripts/intelligent_ingest.py <directory_path> [options]
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to Python path so we can import our modules
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.corpus.registry import CorpusRegistry
from src.corpus.intelligent_ingestion import IntelligentIngestionService


def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool to intelligently ingest a directory of text files, using an LLM to extract structured metadata (e.g., author, date) and automatically register them in the corpus database.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Example Usage:
  # Process a directory and register documents with a 75% confidence threshold
  python %(prog)s ./corpus/raw_sources/recent_us_presidents/ --confidence-threshold 75.0 --verbose

  # Perform a dry run to see what the service would do without writing to the database
  python %(prog)s ./corpus/raw_sources/other_texts/ --dry-run -v

  # Process a directory and save the output to a specific location
  python %(prog)s ./my_new_texts/ --output-dir ./ingestion_results/
"""
    )
    
    # Core arguments
    parser.add_argument(
        "directory",
        help="Path to the directory containing text files to ingest."
    )
    
    # Configuration arguments
    config_group = parser.add_argument_group('Configuration', 'Fine-tune the ingestion process.')
    config_group.add_argument(
        "--output-dir", "-o",
        help="Directory to save detailed output logs. If not provided, a timestamped directory is created in 'tmp/'."
    )
    config_group.add_argument(
        "--confidence-threshold", "-c",
        type=float,
        default=70.0,
        help="The minimum confidence score (0-100) required to automatically register a document. Default: 70.0."
    )
    
    # Execution control arguments
    exec_group = parser.add_argument_group('Execution Control', 'Control how the script runs.')
    exec_group.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Perform a 'dry run'. The script will process all files and show potential results but will NOT write to the database."
    )
    exec_group.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output, showing detailed results for each file processed."
    )
    
    args = parser.parse_args()
    
    # Validate directory exists
    if not Path(args.directory).exists():
        print(f"❌ Error: Directory '{args.directory}' not found")
        sys.exit(1)
    
    # Set up environment variables if needed
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("   The service may not work without a valid OpenAI API key")
    
    try:
        print("🚀 Starting Intelligent Corpus Ingestion Service...")
        print(f"📁 Source Directory: {args.directory}")
        print(f"🎯 Confidence Threshold: {args.confidence_threshold}%")
        
        if args.dry_run:
            print("🧪 Dry Run Mode: Will not register documents in corpus database")
        
        # Initialize services
        if not args.dry_run:
            corpus_registry = CorpusRegistry()
        else:
            # Create a dummy registry for dry run
            corpus_registry = None
        
        ingestion_service = IntelligentIngestionService(
            corpus_registry=corpus_registry,
            confidence_threshold=args.confidence_threshold
        )
        
        # Temporarily override registration for dry run
        if args.dry_run:
            original_process_file = ingestion_service._process_file
            def dry_run_process_file(file_path, output_dir):
                result = original_process_file(file_path, output_dir)
                # Remove registration attempts
                if "registration" in result:
                    result["registration"] = "SKIPPED (dry run)"
                if "text_id" in result:
                    result["text_id"] = "WOULD_GENERATE_ID (dry run)"
                return result
            ingestion_service._process_file = dry_run_process_file
        
        # Run the ingestion
        results = ingestion_service.ingest_directory(
            directory_path=args.directory,
            output_dir=args.output_dir
        )
        
        print(f"\n🎉 Ingestion Complete!")
        
        # Show detailed results if verbose
        if args.verbose:
            print(f"\n📋 Detailed Results:")
            for result in results["processed"]:
                print(f"  📄 {result['filename']}")
                print(f"    Confidence: {result['confidence']:.1f}%")
                if "metadata" in result:
                    metadata = result["metadata"]
                    print(f"    Title: {metadata.get('title', 'N/A')}")
                    print(f"    Author: {metadata.get('author', 'N/A')}")
                    print(f"    Date: {metadata.get('date', 'N/A')}")
                    print(f"    Type: {metadata.get('document_type', 'N/A')}")
                print()
        
        # Show recommendations for uncertain files
        if results["uncertain"]:
            print(f"\n⚠️  {len(results['uncertain'])} files need manual review:")
            for result in results["uncertain"]:
                print(f"  📄 {result['filename']} ({result['confidence']:.1f}%)")
                if "metadata" in result:
                    print(f"    Title: {result['metadata'].get('title', 'N/A')}")
        
        # Return appropriate exit code
        if results["summary"]["success_rate"] >= 50:
            sys.exit(0)
        else:
            print(f"\n⚠️  Low success rate: {results['summary']['success_rate']:.1f}%")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 