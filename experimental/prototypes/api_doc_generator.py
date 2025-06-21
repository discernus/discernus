"""
Custom API Documentation Generator for Discernus
Parses Python files directly to extract docstrings and generates Markdown documentation.
This approach avoids import dependency issues that plague Sphinx autodoc.
"""

import ast
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class ApiDocumentationGenerator:
    """
    Generates API documentation by parsing Python source files directly.
    Outputs Markdown files that integrate with the existing MkDocs setup.
    """
    
    def __init__(self, src_dir: str, output_dir: str):
        """
        Initialize the documentation generator.
        
        Args:
            src_dir: Path to the source code directory
            output_dir: Path where documentation will be generated
        """
        self.src_dir = Path(src_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_docs(self, api_modules: List[str]) -> None:
        """
        Generate documentation for specified API modules.
        
        Args:
            api_modules: List of module names to document (e.g., ['analysis_service', 'schemas'])
        """
        print(f"🚀 Generating API documentation for {len(api_modules)} modules...")
        
        # Generate individual module docs
        module_docs = []
        for module_name in api_modules:
            module_path = self.src_dir / "api" / f"{module_name}.py"
            if module_path.exists():
                doc_content = self._parse_module(module_path, module_name)
                output_file = self.output_dir / f"{module_name}.md"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(doc_content)
                
                module_docs.append({
                    'name': module_name,
                    'title': self._format_module_title(module_name),
                    'file': f"{module_name}.md"
                })
                print(f"✅ Generated documentation for {module_name}")
            else:
                print(f"⚠️ Module file not found: {module_path}")
        
        # Generate index page
        self._generate_index(module_docs)
        print(f"📋 Generated API documentation index")
        
    def _parse_module(self, module_path: Path, module_name: str) -> str:
        """Parse a Python module and extract documentation."""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            
            # Extract module docstring
            module_docstring = ast.get_docstring(tree) or ""
            
            # Extract classes and functions
            classes = []
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(self._parse_class(node, source))
                elif isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    functions.append(self._parse_function(node, source))
            
            # Generate markdown
            return self._generate_module_markdown(
                module_name, module_docstring, classes, functions
            )
            
        except Exception as e:
            print(f"❌ Error parsing {module_path}: {e}")
            return f"# {self._format_module_title(module_name)}\n\nError parsing module: {e}"
    
    def _parse_class(self, node: ast.ClassDef, source: str) -> Dict[str, Any]:
        """Parse a class definition."""
        class_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node) or "",
            'methods': [],
            'line_number': node.lineno
        }
        
        # Extract base classes
        base_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
            elif isinstance(base, ast.Attribute):
                base_classes.append(f"{base.value.id}.{base.attr}")
        
        class_info['bases'] = base_classes
        
        # Extract methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._parse_function(item, source, is_method=True)
                class_info['methods'].append(method_info)
        
        return class_info
    
    def _parse_function(self, node: ast.FunctionDef, source: str, is_method: bool = False) -> Dict[str, Any]:
        """Parse a function or method definition."""
        function_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node) or "",
            'line_number': node.lineno,
            'is_method': is_method,
            'signature': self._extract_signature(node)
        }
        
        return function_info
    
    def _extract_signature(self, node: ast.FunctionDef) -> str:
        """Extract function signature."""
        args = []
        
        # Regular arguments
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {self._get_annotation_string(arg.annotation)}"
            args.append(arg_str)
        
        # *args
        if node.args.vararg:
            vararg_str = f"*{node.args.vararg.arg}"
            if node.args.vararg.annotation:
                vararg_str += f": {self._get_annotation_string(node.args.vararg.annotation)}"
            args.append(vararg_str)
        
        # **kwargs
        if node.args.kwarg:
            kwarg_str = f"**{node.args.kwarg.arg}"
            if node.args.kwarg.annotation:
                kwarg_str += f": {self._get_annotation_string(node.args.kwarg.annotation)}"
            args.append(kwarg_str)
        
        signature = f"{node.name}({', '.join(args)})"
        
        # Return annotation
        if node.returns:
            signature += f" -> {self._get_annotation_string(node.returns)}"
        
        return signature
    
    def _get_annotation_string(self, annotation) -> str:
        """Convert annotation AST node to string."""
        try:
            if isinstance(annotation, ast.Name):
                return annotation.id
            elif isinstance(annotation, ast.Attribute):
                return f"{annotation.value.id}.{annotation.attr}"
            elif isinstance(annotation, ast.Subscript):
                value = self._get_annotation_string(annotation.value)
                slice_value = self._get_annotation_string(annotation.slice)
                return f"{value}[{slice_value}]"
            elif isinstance(annotation, ast.Constant):
                return repr(annotation.value)
            else:
                return "Any"
        except:
            return "Any"
    
    def _generate_module_markdown(self, module_name: str, module_docstring: str, 
                                 classes: List[Dict], functions: List[Dict]) -> str:
        """Generate Markdown documentation for a module."""
        md = []
        
        # Header
        title = self._format_module_title(module_name)
        md.append(f"# {title}")
        md.append("")
        
        # Module docstring
        if module_docstring:
            md.append(module_docstring)
            md.append("")
        
        # Table of contents
        if classes or functions:
            md.append("## Table of Contents")
            md.append("")
            
            if classes:
                md.append("### Classes")
                for cls in classes:
                    md.append(f"- [{cls['name']}](#{cls['name'].lower()})")
                md.append("")
            
            if functions:
                md.append("### Functions")
                for func in functions:
                    md.append(f"- [{func['name']}](#{func['name'].lower()})")
                md.append("")
        
        # Classes
        if classes:
            md.append("## Classes")
            md.append("")
            
            for cls in classes:
                md.append(f"### {cls['name']}")
                if cls['bases']:
                    md.append(f"*Inherits from: {', '.join(cls['bases'])}*")
                md.append("")
                
                if cls['docstring']:
                    md.append(cls['docstring'])
                    md.append("")
                
                # Methods
                if cls['methods']:
                    md.append("#### Methods")
                    md.append("")
                    
                    for method in cls['methods']:
                        md.append(f"##### {method['signature']}")
                        if method['docstring']:
                            md.append(method['docstring'])
                        md.append("")
                
                md.append("---")
                md.append("")
        
        # Functions
        if functions:
            md.append("## Functions")
            md.append("")
            
            for func in functions:
                md.append(f"### {func['signature']}")
                if func['docstring']:
                    md.append(func['docstring'])
                md.append("")
                md.append("---")
                md.append("")
        
        # Footer
        md.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(md)
    
    def _generate_index(self, module_docs: List[Dict]) -> None:
        """Generate index page for API documentation."""
        md = []
        
        md.append("# Discernus API Documentation")
        md.append("")
        md.append("Auto-generated API documentation for the Discernus platform.")
        md.append("")
        
        if module_docs:
            md.append("## Modules")
            md.append("")
            
            for module in module_docs:
                md.append(f"- **[{module['title']}]({module['file']})** - {module['name']} module")
            md.append("")
        
        md.append("## Overview")
        md.append("")
        md.append("The Discernus API provides comprehensive endpoints for narrative analysis, ")
        md.append("corpus management, and experiment orchestration. The API is built using ")
        md.append("modern Python frameworks and follows RESTful design principles.")
        md.append("")
        
        md.append("### Key Components")
        md.append("")
        md.append("- **Analysis Service**: Core analysis functionality using LLM integrations")
        md.append("- **Schemas**: Pydantic models for request/response validation")
        md.append("- **Database Models**: SQLAlchemy models for data persistence")
        md.append("")
        
        md.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        # Write index file
        index_file = self.output_dir / "index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(md))
    
    def _format_module_title(self, module_name: str) -> str:
        """Format module name as title."""
        return f"API Module: {module_name.replace('_', ' ').title()}"


def main():
    """Main entry point for the API documentation generator."""
    # Configuration - fix paths relative to this script location
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent  # Go up to project root
    src_dir = project_root / "src"
    output_dir = project_root / "docs_site" / "docs" / "api"
    
    # Modules to document
    api_modules = [
        "analysis_service",
        "schemas"
    ]
    
    # Generate documentation
    generator = ApiDocumentationGenerator(str(src_dir), str(output_dir))
    generator.generate_docs(api_modules)
    
    print("✅ API documentation generation complete!")
    print(f"📁 Documentation generated in: {output_dir}")


if __name__ == "__main__":
    main() 