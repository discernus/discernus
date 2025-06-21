#!/usr/bin/env python3
"""
Production API Documentation Generator for Discernus
Automatically generates API documentation from source code and integrates with MkDocs.

This script solves the API documentation challenge by parsing Python files directly,
avoiding the import dependency issues that plagued Sphinx autodoc attempts.

Usage:
    python3 scripts/applications/generate_api_docs.py
    python3 scripts/applications/generate_api_docs.py --modules analysis_service schemas
"""

import sys
import argparse
from pathlib import Path

# Add the experimental prototype to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "experimental" / "prototypes"))

from api_doc_generator import ApiDocumentationGenerator


def main():
    """Main entry point for the production API documentation generator."""
    parser = argparse.ArgumentParser(description="Generate API documentation for Discernus")
    parser.add_argument(
        "--modules",
        nargs="+",
        default=["analysis_service", "schemas"],
        help="API modules to document (default: analysis_service schemas)"
    )
    parser.add_argument(
        "--output",
        default="docs_site/docs/api",
        help="Output directory for documentation (default: docs_site/docs/api)"
    )
    parser.add_argument(
        "--src",
        default="src",
        help="Source directory (default: src)"
    )
    
    args = parser.parse_args()
    
    # Calculate absolute paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    src_dir = project_root / args.src
    output_dir = project_root / args.output
    
    print(f"🚀 Generating API documentation...")
    print(f"📁 Source: {src_dir}")
    print(f"📁 Output: {output_dir}")
    print(f"📋 Modules: {', '.join(args.modules)}")
    print()
    
    # Generate documentation
    generator = ApiDocumentationGenerator(str(src_dir), str(output_dir))
    generator.generate_docs(args.modules)
    
    print()
    print("✅ API documentation generation complete!")
    print(f"📖 View documentation: http://localhost:8000/api/")
    print()
    print("💡 To serve the documentation locally:")
    print("   cd docs_site && mkdocs serve")
    print()
    print("🔄 To update MkDocs navigation, edit: docs_site/mkdocs.yml")


if __name__ == "__main__":
    main() 