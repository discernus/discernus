#!/usr/bin/env python3
"""
Component Version Manager CLI
Manages prompt templates, framework versions, and weighting methodologies.
"""

import argparse
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import sys
import os

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

from src.narrative_gravity.models.component_models import (
    PromptTemplate, FrameworkVersion, WeightingMethodology, 
    ComponentCompatibility, DevelopmentSession
)
from src.narrative_gravity.models.base import Base

load_dotenv()

class ComponentManager:
    """CLI manager for component versioning operations."""
    
    def __init__(self):
        self.engine = create_engine(os.getenv('DATABASE_URL'))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def list_components(self, component_type: Optional[str] = None):
        """List all components or components of a specific type."""
        
        print("🔧 Component Version Inventory")
        print("=" * 60)
        
        if not component_type or component_type == 'prompt':
            templates = self.session.query(PromptTemplate).order_by(
                PromptTemplate.name, PromptTemplate.version
            ).all()
            print(f"\n📝 Prompt Templates ({len(templates)} found):")
            for template in templates:
                status = f"[{template.validation_status}]"
                usage = f"({template.usage_count} uses)" if template.usage_count else "(unused)"
                print(f"  - {template.name} v{template.version} {status} {usage}")
                if template.description:
                    print(f"    └─ {template.description[:60]}...")
        
        if not component_type or component_type == 'framework':
            frameworks = self.session.query(FrameworkVersion).order_by(
                FrameworkVersion.framework_name, FrameworkVersion.version
            ).all()
            print(f"\n🏗️  Framework Versions ({len(frameworks)} found):")
            for framework in frameworks:
                status = f"[{framework.validation_status}]"
                usage = f"({framework.usage_count} uses)" if framework.usage_count else "(unused)"
                print(f"  - {framework.framework_name} v{framework.version} {status} {usage}")
                if framework.description:
                    print(f"    └─ {framework.description[:60]}...")
        
        if not component_type or component_type == 'weighting':
            weightings = self.session.query(WeightingMethodology).order_by(
                WeightingMethodology.name, WeightingMethodology.version
            ).all()
            print(f"\n⚖️  Weighting Methodologies ({len(weightings)} found):")
            for weighting in weightings:
                status = f"[{weighting.validation_status}]"
                usage = f"({weighting.usage_count} uses)" if weighting.usage_count else "(unused)"
                print(f"  - {weighting.name} v{weighting.version} ({weighting.algorithm_type}) {status} {usage}")
                if weighting.algorithm_description:
                    print(f"    └─ {weighting.algorithm_description[:60]}...")
    
    def create_prompt_template(self, name: str, version: str, template_file: str, description: str = None):
        """Create a new prompt template version."""
        
        # Check if version already exists
        existing = self.session.query(PromptTemplate).filter_by(name=name, version=version).first()
        if existing:
            print(f"❌ Error: Prompt template {name} v{version} already exists")
            return False
        
        # Read template content
        try:
            with open(template_file, 'r') as f:
                template_content = f.read()
        except FileNotFoundError:
            print(f"❌ Error: Template file {template_file} not found")
            return False
        
        # Create new template
        template = PromptTemplate(
            name=name,
            version=version,
            template_content=template_content,
            description=description,
            template_type="hierarchical" if "hierarchical" in template_content.lower() else "standard"
        )
        
        self.session.add(template)
        self.session.commit()
        
        print(f"✅ Created prompt template: {name} v{version}")
        print(f"   ID: {template.id}")
        print(f"   Type: {template.template_type}")
        print(f"   Content length: {len(template_content)} characters")
        
        return True
    
    def create_framework_version(self, name: str, version: str, config_file: str, description: str = None):
        """Create a new framework version."""
        
        # Check if version already exists
        existing = self.session.query(FrameworkVersion).filter_by(framework_name=name, version=version).first()
        if existing:
            print(f"❌ Error: Framework {name} v{version} already exists")
            return False
        
        # Read framework configuration
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"❌ Error reading framework config: {e}")
            return False
        
        # Validate required fields
        if 'dipoles' not in config or 'wells' not in config:
            print("❌ Error: Framework config must include 'dipoles' and 'wells' fields")
            return False
        
        # Create framework version
        framework = FrameworkVersion(
            framework_name=name,
            version=version,
            dipoles_json=config['dipoles'],
            framework_json=config,
            weights_json=config.get('scoring', {}),
            description=description,
            weighting_rationale=config.get('weighting_rationale', '')
        )
        
        self.session.add(framework)
        self.session.commit()
        
        print(f"✅ Created framework version: {name} v{version}")
        print(f"   ID: {framework.id}")
        print(f"   Wells: {len(config['wells'].get('constructive', []) + config['wells'].get('destructive', []))}")
        print(f"   Dipoles: {len(config['dipoles'])}")
        
        return True
    
    def create_weighting_methodology(self, name: str, version: str, algorithm_type: str, 
                                   description: str, formula: str = None, parameters: dict = None):
        """Create a new weighting methodology."""
        
        # Check if version already exists
        existing = self.session.query(WeightingMethodology).filter_by(name=name, version=version).first()
        if existing:
            print(f"❌ Error: Weighting methodology {name} v{version} already exists")
            return False
        
        # Create weighting methodology
        weighting = WeightingMethodology(
            name=name,
            version=version,
            algorithm_type=algorithm_type,
            algorithm_description=description,
            mathematical_formula=formula,
            parameters_json=parameters or {}
        )
        
        self.session.add(weighting)
        self.session.commit()
        
        print(f"✅ Created weighting methodology: {name} v{version}")
        print(f"   ID: {weighting.id}")
        print(f"   Type: {algorithm_type}")
        print(f"   Parameters: {len(parameters or {})}")
        
        return True
    
    def validate_compatibility(self, prompt_id: str, framework_id: str, weighting_id: str):
        """Check or create component compatibility entry."""
        
        # Check if combination already exists
        existing = self.session.query(ComponentCompatibility).filter_by(
            prompt_template_id=prompt_id,
            framework_id=framework_id,
            weighting_method_id=weighting_id
        ).first()
        
        if existing:
            print(f"✅ Compatibility entry exists:")
            print(f"   Status: {existing.validation_status}")
            print(f"   Score: {existing.compatibility_score}")
            print(f"   Runs: {existing.test_run_count}")
            return existing
        
        # Create new compatibility entry
        compatibility = ComponentCompatibility(
            prompt_template_id=prompt_id,
            framework_id=framework_id,
            weighting_method_id=weighting_id,
            validation_status="untested"
        )
        
        self.session.add(compatibility)
        self.session.commit()
        
        print(f"✅ Created compatibility entry (untested)")
        print(f"   ID: {compatibility.id}")
        
        return compatibility
    
    def export_component(self, component_type: str, name: str, version: str, output_file: str):
        """Export a component to JSON file."""
        
        if component_type == 'prompt':
            component = self.session.query(PromptTemplate).filter_by(name=name, version=version).first()
            if not component:
                print(f"❌ Prompt template {name} v{version} not found")
                return False
            
            export_data = {
                'type': 'prompt_template',
                'name': component.name,
                'version': component.version,
                'template_content': component.template_content,
                'template_type': component.template_type,
                'description': component.description,
                'validation_status': component.validation_status,
                'exported_at': datetime.utcnow().isoformat()
            }
        
        elif component_type == 'framework':
            component = self.session.query(FrameworkVersion).filter_by(framework_name=name, version=version).first()
            if not component:
                print(f"❌ Framework {name} v{version} not found")
                return False
            
            export_data = {
                'type': 'framework_version',
                'framework_name': component.framework_name,
                'version': component.version,
                'dipoles': component.dipoles_json,
                'framework_config': component.framework_json,
                'weights': component.weights_json,
                'description': component.description,
                'validation_status': component.validation_status,
                'exported_at': datetime.utcnow().isoformat()
            }
        
        elif component_type == 'weighting':
            component = self.session.query(WeightingMethodology).filter_by(name=name, version=version).first()
            if not component:
                print(f"❌ Weighting methodology {name} v{version} not found")
                return False
            
            export_data = {
                'type': 'weighting_methodology',
                'name': component.name,
                'version': component.version,
                'algorithm_type': component.algorithm_type,
                'algorithm_description': component.algorithm_description,
                'mathematical_formula': component.mathematical_formula,
                'parameters': component.parameters_json,
                'description': component.description,
                'validation_status': component.validation_status,
                'exported_at': datetime.utcnow().isoformat()
            }
        
        else:
            print(f"❌ Unknown component type: {component_type}")
            return False
        
        # Write to file
        try:
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            print(f"✅ Exported {component_type} to {output_file}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def __del__(self):
        """Clean up database session."""
        if hasattr(self, 'session'):
            self.session.close()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Component Version Manager CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List components')
    list_parser.add_argument('--type', choices=['prompt', 'framework', 'weighting'], 
                           help='Filter by component type')
    
    # Create prompt template
    prompt_parser = subparsers.add_parser('create-prompt', help='Create prompt template')
    prompt_parser.add_argument('name', help='Template name')
    prompt_parser.add_argument('version', help='Template version')
    prompt_parser.add_argument('template_file', help='Template file path')
    prompt_parser.add_argument('--description', help='Template description')
    
    # Create framework
    framework_parser = subparsers.add_parser('create-framework', help='Create framework version')
    framework_parser.add_argument('name', help='Framework name')
    framework_parser.add_argument('version', help='Framework version')
    framework_parser.add_argument('config_file', help='Framework config JSON file')
    framework_parser.add_argument('--description', help='Framework description')
    
    # Create weighting methodology
    weighting_parser = subparsers.add_parser('create-weighting', help='Create weighting methodology')
    weighting_parser.add_argument('name', help='Methodology name')
    weighting_parser.add_argument('version', help='Methodology version')
    weighting_parser.add_argument('algorithm_type', help='Algorithm type')
    weighting_parser.add_argument('description', help='Algorithm description')
    weighting_parser.add_argument('--formula', help='Mathematical formula')
    weighting_parser.add_argument('--parameters', help='Parameters JSON string')
    
    # Validate compatibility
    compat_parser = subparsers.add_parser('validate-compatibility', help='Validate component compatibility')
    compat_parser.add_argument('prompt_id', help='Prompt template ID')
    compat_parser.add_argument('framework_id', help='Framework ID')
    compat_parser.add_argument('weighting_id', help='Weighting methodology ID')
    
    # Export component
    export_parser = subparsers.add_parser('export', help='Export component to JSON')
    export_parser.add_argument('type', choices=['prompt', 'framework', 'weighting'])
    export_parser.add_argument('name', help='Component name')
    export_parser.add_argument('version', help='Component version')
    export_parser.add_argument('output_file', help='Output JSON file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = ComponentManager()
    
    try:
        if args.command == 'list':
            manager.list_components(args.type)
        
        elif args.command == 'create-prompt':
            manager.create_prompt_template(args.name, args.version, args.template_file, args.description)
        
        elif args.command == 'create-framework':
            manager.create_framework_version(args.name, args.version, args.config_file, args.description)
        
        elif args.command == 'create-weighting':
            parameters = json.loads(args.parameters) if args.parameters else {}
            manager.create_weighting_methodology(
                args.name, args.version, args.algorithm_type, 
                args.description, args.formula, parameters
            )
        
        elif args.command == 'validate-compatibility':
            manager.validate_compatibility(args.prompt_id, args.framework_id, args.weighting_id)
        
        elif args.command == 'export':
            manager.export_component(args.type, args.name, args.version, args.output_file)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 