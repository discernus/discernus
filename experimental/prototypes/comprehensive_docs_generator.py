"""
Comprehensive Documentation Generator for Discernus
Auto-discovers all Python modules and generates complete documentation ecosystem.
Solves the broader documentation challenge beyond just API files.
"""

import ast
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from datetime import datetime


class ComprehensiveDocumentationGenerator:
    """
    Generates comprehensive documentation for the entire Discernus codebase.
    Auto-discovers modules, creates cross-references, and integrates with MkDocs.
    """
    
    def __init__(self, project_root: str):
        """
        Initialize the comprehensive documentation generator.
        
        Args:
            project_root: Path to the project root directory
        """
        self.project_root = Path(project_root)
        self.src_dir = self.project_root / "src"
        self.scripts_dir = self.project_root / "scripts"
        self.output_dir = self.project_root / "docs_site" / "docs" / "code_reference"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Track all discovered classes and functions for cross-referencing
        self.all_classes = {}  # class_name -> (module_path, class_info)
        self.all_functions = {}  # function_name -> (module_path, function_info)
        self.module_dependencies = {}  # module -> set of imported modules
        
    def discover_and_generate_all_docs(self) -> None:
        """
        Auto-discover all Python modules and generate comprehensive documentation.
        """
        print("🔍 Discovering all Python modules...")
        
        # Discover all Python files
        src_modules = self._discover_python_modules(self.src_dir, "src")
        script_modules = self._discover_python_modules(self.scripts_dir, "scripts")
        
        all_modules = src_modules + script_modules
        print(f"📊 Found {len(all_modules)} Python modules to document")
        
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
    
    def _discover_python_modules(self, base_dir: Path, prefix: str) -> List[Dict[str, Any]]:
        """Recursively discover all Python modules in a directory."""
        modules = []
        
        if not base_dir.exists():
            return modules
            
        for py_file in base_dir.rglob("*.py"):
            # Skip __pycache__ and test files
            if "__pycache__" in str(py_file) or py_file.name.startswith("test_"):
                continue
                
            # Calculate module path relative to base
            relative_path = py_file.relative_to(base_dir)
            module_path = str(relative_path).replace("/", ".").replace("\\", ".")[:-3]  # Remove .py
            
            modules.append({
                "file_path": py_file,
                "module_path": f"{prefix}.{module_path}",
                "category": prefix,
                "package": str(relative_path.parent) if relative_path.parent != Path('.') else None
            })
        
        return modules
    
    def _index_module_for_cross_refs(self, module_info: Dict[str, Any]) -> None:
        """Parse module and index classes/functions for cross-referencing."""
        try:
            with open(module_info["file_path"], 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            
            # Extract classes and functions for cross-ref index
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self.all_classes[node.name] = (module_info["module_path"], {
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or "",
                        'line_number': node.lineno
                    })
                elif isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    self.all_functions[node.name] = (module_info["module_path"], {
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or "",
                        'line_number': node.lineno
                    })
            
            # Extract imports for dependency tracking
            imports = self._extract_imports(tree)
            self.module_dependencies[module_info["module_path"]] = imports
            
        except Exception as e:
            print(f"⚠️ Warning: Could not index {module_info['file_path']}: {e}")
    
    def _extract_imports(self, tree: ast.AST) -> Set[str]:
        """Extract all imports from an AST."""
        imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module)
        
        return imports
    
    def _generate_module_documentation(self, module_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate comprehensive documentation for a single module."""
        try:
            with open(module_info["file_path"], 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            
            # Extract module docstring
            module_docstring = ast.get_docstring(tree) or ""
            
            # Extract classes and functions
            classes = []
            functions = []
            
            # Track method names to avoid duplicating them as standalone functions
            method_names = set()
            
            # First pass: collect all class method names
            for node in tree.body:  # Only look at top-level nodes
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_names.add(item.name)
            
            # Second pass: collect classes and only module-level functions
            for node in tree.body:  # Only look at top-level nodes
                if isinstance(node, ast.ClassDef):
                    classes.append(self._parse_class_comprehensive(node, source))
                elif isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                    # Only include if it's not a method name we've seen in classes
                    if node.name not in method_names:
                        functions.append(self._parse_function_comprehensive(node, source))
            
            # Generate markdown with cross-references
            markdown_content = self._generate_comprehensive_markdown(
                module_info, module_docstring, classes, functions
            )
            
            # Save module documentation
            output_file = self._get_module_output_path(module_info)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return {
                'module_info': module_info,
                'classes': len(classes),
                'functions': len(functions),
                'output_file': output_file,
                'title': self._format_module_title(module_info),
                'category': module_info['category']
            }
            
        except Exception as e:
            print(f"❌ Error generating docs for {module_info['file_path']}: {e}")
            return None
    
    def _parse_class_comprehensive(self, node: ast.ClassDef, source: str) -> Dict[str, Any]:
        """Parse class with comprehensive information including cross-references."""
        class_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node) or "",
            'line_number': node.lineno,
            'methods': []
        }
        
        # Extract base classes with cross-references
        base_classes = []
        for base in node.bases:
            base_name = self._get_base_class_name(base)
            if base_name in self.all_classes:
                module_path, _ = self.all_classes[base_name]
                base_classes.append(f"[{base_name}]({self._get_cross_ref_link(module_path, base_name)})")
            else:
                base_classes.append(base_name)
        
        class_info['bases'] = base_classes
        
        # Extract methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._parse_function_comprehensive(item, source, is_method=True)
                class_info['methods'].append(method_info)
        
        return class_info
    
    def _parse_function_comprehensive(self, node: ast.FunctionDef, source: str, is_method: bool = False) -> Dict[str, Any]:
        """Parse function with comprehensive signature information."""
        function_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node) or "",
            'line_number': node.lineno,
            'is_method': is_method,
            'signature': self._extract_comprehensive_signature(node)
        }
        
        return function_info
    
    def _extract_comprehensive_signature(self, node: ast.FunctionDef) -> str:
        """Extract function signature with type annotations."""
        args = []
        
        # Regular arguments
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {self._annotation_to_string(arg.annotation)}"
            args.append(arg_str)
        
        # *args and **kwargs
        if node.args.vararg:
            vararg_str = f"*{node.args.vararg.arg}"
            if node.args.vararg.annotation:
                vararg_str += f": {self._annotation_to_string(node.args.vararg.annotation)}"
            args.append(vararg_str)
        
        if node.args.kwarg:
            kwarg_str = f"**{node.args.kwarg.arg}"
            if node.args.kwarg.annotation:
                kwarg_str += f": {self._annotation_to_string(node.args.kwarg.annotation)}"
            args.append(kwarg_str)
        
        signature = f"{node.name}({', '.join(args)})"
        
        # Return annotation
        if node.returns:
            signature += f" -> {self._annotation_to_string(node.returns)}"
        
        return signature
    
    def _annotation_to_string(self, annotation) -> str:
        """Convert type annotation to string with cross-references."""
        try:
            if isinstance(annotation, ast.Name):
                type_name = annotation.id
                # Add cross-reference if it's a known class
                if type_name in self.all_classes:
                    module_path, _ = self.all_classes[type_name]
                    return f"[{type_name}]({self._get_cross_ref_link(module_path, type_name)})"
                return type_name
            elif isinstance(annotation, ast.Attribute):
                return f"{annotation.value.id}.{annotation.attr}"
            elif isinstance(annotation, ast.Subscript):
                value = self._annotation_to_string(annotation.value)
                slice_value = self._annotation_to_string(annotation.slice)
                return f"{value}[{slice_value}]"
            elif isinstance(annotation, ast.Constant):
                return repr(annotation.value)
            else:
                return "Any"
        except:
            return "Any"
    
    def _get_cross_ref_link(self, module_path: str, item_name: str) -> str:
        """Generate cross-reference link to another module item."""
        # Convert module path to relative file path
        relative_path = module_path.replace(".", "/") + ".md"
        anchor = self._create_anchor(item_name)
        return f"{relative_path}#{anchor}"
    
    def _generate_comprehensive_markdown(self, module_info: Dict[str, Any], 
                                       module_docstring: str, classes: List[Dict], 
                                       functions: List[Dict]) -> str:
        """Generate comprehensive Markdown with cross-references."""
        md = []
        
        # Header
        title = self._format_module_title(module_info)
        md.append(f"# {title}")
        md.append("")
        
        # Module info
        md.append(f"**Module:** `{module_info['module_path']}`")
        md.append(f"**File:** `{module_info['file_path']}`")
        if module_info.get('package'):
            md.append(f"**Package:** `{module_info['package']}`")
        md.append("")
        
        # Module docstring
        if module_docstring:
            md.append(module_docstring)
            md.append("")
        
        # Dependencies
        deps = self.module_dependencies.get(module_info['module_path'], set())
        if deps:
            md.append("## Dependencies")
            md.append("")
            for dep in sorted(deps):
                md.append(f"- `{dep}`")
            md.append("")
        
        # Table of contents
        if classes or functions:
            md.append("## Table of Contents")
            md.append("")
            
            if classes:
                md.append("### Classes")
                for cls in classes:
                    md.append(f"- [{cls['name']}](#{self._create_anchor(cls['name'])})")
                md.append("")
            
            if functions:
                md.append("### Functions")
                for func in functions:
                    md.append(f"- [{func['name']}](#{self._create_anchor(func['name'])})")
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
                        md.append(f"##### `{method['name']}`")
                        md.append(f"```python\n{method['signature']}\n```")
                        if method['docstring']:
                            md.append(f"\n{method['docstring']}")
                        md.append("")
                
                md.append("---")
                md.append("")
        
        # Functions
        if functions:
            md.append("## Functions")
            md.append("")
            
            for func in functions:
                md.append(f"### `{func['name']}`")
                md.append(f"```python\n{func['signature']}\n```")
                if func['docstring']:
                    md.append(f"\n{func['docstring']}")
                md.append("")
                md.append("---")
                md.append("")
        
        # Footer
        md.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(md)
    
    def _generate_comprehensive_index(self, module_docs: List[Dict]) -> None:
        """Generate comprehensive index with navigation by category."""
        md = []
        
        md.append("# Discernus Code Reference")
        md.append("")
        md.append("Comprehensive auto-generated documentation for the entire Discernus codebase.")
        md.append("")
        
        # Organize by category
        src_modules = [m for m in module_docs if m['category'] == 'src']
        script_modules = [m for m in module_docs if m['category'] == 'scripts']
        
        if src_modules:
            md.append("## Source Code (`src/`)")
            md.append("")
            md.append("Core application modules.")
            md.append("")
            
            # Group by package
            packages = {}
            for module in src_modules:
                package = module['module_info'].get('package', 'root')
                if package is None:
                    package = 'root'
                if package not in packages:
                    packages[package] = []
                packages[package].append(module)
            
            for package, modules in sorted(packages.items(), key=lambda x: (x[0] or 'root')):
                if package != 'root':
                    md.append(f"### {package}/")
                    md.append("")
                
                for module in sorted(modules, key=lambda x: x['module_info']['module_path']):
                    relative_path = os.path.relpath(module['output_file'], self.output_dir)
                    md.append(f"- **[{module['title']}]({relative_path})** - {module['classes']} classes, {module['functions']} functions")
                
                md.append("")
        
        if script_modules:
            md.append("## Scripts (`scripts/`)")
            md.append("")
            md.append("Utility and application scripts.")
            md.append("")
            
            for module in sorted(script_modules, key=lambda x: x['module_info']['module_path']):
                relative_path = os.path.relpath(module['output_file'], self.output_dir)
                md.append(f"- **[{module['title']}]({relative_path})** - {module['classes']} classes, {module['functions']} functions")
            
            md.append("")
        
        # Statistics
        total_classes = sum(m['classes'] for m in module_docs)
        total_functions = sum(m['functions'] for m in module_docs)
        
        md.append("## Documentation Statistics")
        md.append("")
        md.append(f"- **{len(module_docs)} modules** documented")
        md.append(f"- **{total_classes} classes** with methods and properties")
        md.append(f"- **{total_functions} functions** with type annotations")
        md.append(f"- **{len(self.all_classes)} classes** cross-referenced")
        md.append(f"- **{len(self.all_functions)} functions** cross-referenced")
        md.append("")
        
        md.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        # Write index
        index_file = self.output_dir / "index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(md))
    
    def _generate_cross_reference_index(self) -> None:
        """Generate cross-reference index for quick navigation."""
        md = []
        
        md.append("# Cross-Reference Index")
        md.append("")
        md.append("Quick navigation index for all classes and functions across the codebase.")
        md.append("")
        
        # Classes index
        if self.all_classes:
            md.append("## Classes")
            md.append("")
            
            for class_name, (module_path, class_info) in sorted(self.all_classes.items()):
                link = self._get_cross_ref_link(module_path, class_name)
                md.append(f"- **[{class_name}]({link})** - `{module_path}`")
            
            md.append("")
        
        # Functions index
        if self.all_functions:
            md.append("## Functions")
            md.append("")
            
            for func_name, (module_path, func_info) in sorted(self.all_functions.items()):
                link = self._get_cross_ref_link(module_path, func_name)
                md.append(f"- **[{func_name}]({link})** - `{module_path}`")
            
            md.append("")
        
        # Write cross-reference index
        cross_ref_file = self.output_dir / "cross_reference.md"
        with open(cross_ref_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(md))
    
    # Helper methods
    def _get_module_output_path(self, module_info: Dict[str, Any]) -> Path:
        """Get output file path for a module."""
        module_path = module_info['module_path'].replace('.', '/')
        return self.output_dir / f"{module_path}.md"
    
    def _format_module_title(self, module_info: Dict[str, Any]) -> str:
        """Format module name as title."""
        module_name = module_info['module_path'].split('.')[-1]
        return f"{module_name.replace('_', ' ').title()}"
    
    def _get_base_class_name(self, base) -> str:
        """Extract base class name from AST node."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{base.value.id}.{base.attr}"
        else:
            return str(base)

    def _create_anchor(self, name: str) -> str:
        """Create a proper markdown anchor from a name."""
        # Convert to lowercase and replace special characters
        import re
        # Remove parentheses and parameters for function names
        clean_name = re.sub(r'\([^)]*\)', '', name)
        # Convert to lowercase and replace non-alphanumeric with hyphens
        anchor = re.sub(r'[^a-zA-Z0-9]+', '-', clean_name.lower())
        # Remove leading/trailing hyphens
        anchor = anchor.strip('-')
        return anchor


def main():
    """Main entry point for comprehensive documentation generation."""
    project_root = Path(__file__).parent.parent.parent
    
    print("🚀 Starting comprehensive documentation generation...")
    print(f"📁 Project root: {project_root}")
    
    generator = ComprehensiveDocumentationGenerator(str(project_root))
    generator.discover_and_generate_all_docs()
    
    print("\n✅ Comprehensive documentation generation complete!")
    print(f"📖 Documentation generated in: {generator.output_dir}")
    print("\n💡 To integrate with MkDocs, add this to mkdocs.yml navigation:")
    print("  - 'Code Reference':")
    print("    - 'Overview': 'code_reference/index.md'")
    print("    - 'Cross-Reference': 'code_reference/cross_reference.md'")
    print("\n🌐 Then run: cd docs_site && python3 -m mkdocs serve")


if __name__ == "__main__":
    main() 