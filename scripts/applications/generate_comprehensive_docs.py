#!/usr/bin/env python3
"""
Comprehensive Documentation Generator for Discernus
Auto-discovers ALL Python modules and generates complete documentation ecosystem.

This addresses the limitation of the narrow API-only documentation approach
by providing comprehensive coverage similar to Sphinx autodoc but without
the dependency issues.

Usage:
    python3 scripts/applications/generate_comprehensive_docs.py
    python3 scripts/applications/generate_comprehensive_docs.py --include-scripts
"""

import sys
import argparse
from pathlib import Path

# Add the experimental prototype to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "experimental" / "prototypes"))

from comprehensive_docs_generator import ComprehensiveDocumentationGenerator


def main():
    """Main entry point for comprehensive documentation generation."""
    parser = argparse.ArgumentParser(description="Generate comprehensive documentation for entire Discernus codebase")
    parser.add_argument(
        "--include-scripts",
        action="store_true",
        help="Include scripts directory in documentation (default: False)"
    )
    parser.add_argument(
        "--output",
        default="docs_site/docs/code_reference",
        help="Output directory for documentation (default: docs_site/docs/code_reference)"
    )
    
    args = parser.parse_args()
    
    # Calculate project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    print("🚀 Starting COMPREHENSIVE documentation generation...")
    print("📋 This generates docs for ALL Python modules, not just API files")
    print(f"📁 Project root: {project_root}")
    print(f"📁 Output: {project_root / args.output}")
    print(f"📜 Include scripts: {args.include_scripts}")
    print()
    
    # Create generator with modified settings if needed
    class ConfigurableComprehensiveGenerator(ComprehensiveDocumentationGenerator):
        def __init__(self, project_root: str, include_scripts: bool = True):
            super().__init__(project_root)
            self.include_scripts = include_scripts
        
        def discover_and_generate_all_docs(self) -> None:
            """Modified to optionally exclude scripts."""
            print("🔍 Discovering all Python modules...")
            
            # Always discover src modules
            src_modules = self._discover_python_modules(self.src_dir, "src")
            all_modules = src_modules
            
            # Optionally include scripts
            if self.include_scripts:
                script_modules = self._discover_python_modules(self.scripts_dir, "scripts")
                all_modules += script_modules
            
            print(f"📊 Found {len(all_modules)} Python modules to document")
            print(f"   - {len(src_modules)} source modules")
            if self.include_scripts and 'script_modules' in locals():
                print(f"   - {len(script_modules)} script modules")
            print()
            
            # First pass: Parse all modules and build cross-reference index
            print("🗂️ Building cross-reference index...")
            for module_info in all_modules:
                self._index_module_for_cross_refs(module_info)
            
            # Second pass: Generate documentation with cross-references
            print("📝 Generating comprehensive documentation...")
            module_docs = []
            
            for module_info in all_modules:
                doc_content = self._generate_module_documentation(module_info)
                if doc_content:
                    module_docs.append(doc_content)
            
            # Generate navigation structure
            self._generate_comprehensive_index(module_docs)
            self._generate_cross_reference_index()
            
            print(f"✅ Generated comprehensive documentation for {len(module_docs)} modules")
            print(f"📊 Cross-referenced {len(self.all_classes)} classes and {len(self.all_functions)} functions")
    
    # Generate documentation
    generator = ConfigurableComprehensiveGenerator(str(project_root), args.include_scripts)
    generator.discover_and_generate_all_docs()
    
    print()
    print("🎉 COMPREHENSIVE documentation generation complete!")
    print()
    print("📊 Coverage comparison:")
    print("  - Previous solution: 2 API files")
    print(f"  - This solution: ALL {len(list(project_root.glob('src/**/*.py')))} source files")
    print()
    print("✨ Advanced features provided:")
    print("  - ✅ Auto-discovery of all modules")
    print("  - ✅ Cross-references between classes/functions")
    print("  - ✅ Inheritance tracking with links")
    print("  - ✅ Type annotation parsing")
    print("  - ✅ Dependency mapping")
    print("  - ✅ Comprehensive navigation structure")
    print("  - ✅ Organized by package/category")
    print()
    print("💡 To integrate with MkDocs:")
    print("1. Add to mkdocs.yml navigation:")
    print("   - 'Code Reference':")
    print("     - 'Overview': 'code_reference/index.md'")
    print("     - 'Cross-Reference': 'code_reference/cross_reference.md'")
    print()
    print("2. Run: cd docs_site && python3 -m mkdocs serve")
    print("3. Visit: http://localhost:8000/code_reference/")
    print()
    print("🔗 This provides the comprehensive documentation ecosystem")
    print("   that Sphinx would offer, but without dependency issues!")


if __name__ == "__main__":
    main() 