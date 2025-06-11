#!/usr/bin/env python3
"""
Component Version Manager (manage_components.py)
Priority 1 CLI Infrastructure Component

Create, update, and track component versions with complete provenance tracking.
Manages prompt templates, framework versions, and weighting methodologies.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc

from ..models import (
    PromptTemplate, FrameworkVersion, WeightingMethodology, 
    ComponentCompatibility, DevelopmentSession, User
)
from ..utils.database import get_database_url


class ComponentVersionManager:
    """Manages component version creation, updating, and tracking."""
    
    def __init__(self):
        """Initialize database connection."""
        self.engine = create_engine(get_database_url())
        self.Session = sessionmaker(bind=self.engine)
    
    def create_prompt_template(self, name: str, version: str, template_content: str, 
                             template_type: str = "standard", description: str = None,
                             parent_version: str = None, development_notes: str = None) -> str:
        """Create new prompt template version."""
        session = self.Session()
        try:
            # Check if version already exists
            existing = session.query(PromptTemplate).filter_by(name=name, version=version).first()
            if existing:
                raise ValueError(f"Prompt template {name}:{version} already exists")
            
            # Get parent version if specified
            parent_version_id = None
            if parent_version:
                parent = session.query(PromptTemplate).filter_by(name=name, version=parent_version).first()
                if not parent:
                    raise ValueError(f"Parent version {name}:{parent_version} not found")
                parent_version_id = parent.id
            
            # Create new prompt template
            prompt = PromptTemplate(
                name=name,
                version=version,
                template_content=template_content,
                template_type=template_type,
                description=description,
                parent_version_id=parent_version_id,
                development_notes=development_notes,
                validation_status="draft"
            )
            
            session.add(prompt)
            session.commit()
            
            print(f"✅ Created prompt template: {name}:{version}")
            return prompt.id
            
        finally:
            session.close()
    
    def create_framework_version(self, framework_name: str, version: str, 
                                dipoles_file: str, weights_file: str,
                                description: str = None, parent_version: str = None,
                                theoretical_foundation: str = None) -> str:
        """Create new framework version."""
        session = self.Session()
        try:
            # Check if version already exists
            existing = session.query(FrameworkVersion).filter_by(framework_name=framework_name, version=version).first()
            if existing:
                raise ValueError(f"Framework {framework_name}:{version} already exists")
            
            # Load configuration files
            with open(dipoles_file, 'r') as f:
                dipoles_json = json.load(f)
            
            with open(weights_file, 'r') as f:
                weights_json = json.load(f)
            
            # Create framework configuration
            framework_json = {
                'name': framework_name,
                'version': version,
                'dipoles': dipoles_json,
                'weights': weights_json,
                'created_at': datetime.now().isoformat()
            }
            
            # Get parent version if specified
            parent_version_id = None
            if parent_version:
                parent = session.query(FrameworkVersion).filter_by(framework_name=framework_name, version=parent_version).first()
                if not parent:
                    raise ValueError(f"Parent version {framework_name}:{parent_version} not found")
                parent_version_id = parent.id
            
            # Create new framework version
            framework = FrameworkVersion(
                framework_name=framework_name,
                version=version,
                dipoles_json=dipoles_json,
                framework_json=framework_json,
                weights_json=weights_json,
                description=description,
                parent_version_id=parent_version_id,
                theoretical_foundation=theoretical_foundation,
                validation_status="draft"
            )
            
            session.add(framework)
            session.commit()
            
            print(f"✅ Created framework version: {framework_name}:{version}")
            return framework.id
            
        finally:
            session.close()
    
    def create_weighting_methodology(self, name: str, version: str, algorithm_type: str,
                                   algorithm_description: str, parameters_file: str,
                                   mathematical_formula: str = None, parent_version: str = None,
                                   implementation_notes: str = None) -> str:
        """Create new weighting methodology version."""
        session = self.Session()
        try:
            # Check if version already exists
            existing = session.query(WeightingMethodology).filter_by(name=name, version=version).first()
            if existing:
                raise ValueError(f"Weighting methodology {name}:{version} already exists")
            
            # Load parameters
            with open(parameters_file, 'r') as f:
                parameters_json = json.load(f)
            
            # Get parent version if specified
            parent_version_id = None
            if parent_version:
                parent = session.query(WeightingMethodology).filter_by(name=name, version=parent_version).first()
                if not parent:
                    raise ValueError(f"Parent version {name}:{parent_version} not found")
                parent_version_id = parent.id
            
            # Create new weighting methodology
            weighting = WeightingMethodology(
                name=name,
                version=version,
                algorithm_type=algorithm_type,
                algorithm_description=algorithm_description,
                mathematical_formula=mathematical_formula,
                implementation_notes=implementation_notes,
                parameters_json=parameters_json,
                parent_version_id=parent_version_id,
                validation_status="draft"
            )
            
            session.add(weighting)
            session.commit()
            
            print(f"✅ Created weighting methodology: {name}:{version}")
            return weighting.id
            
        finally:
            session.close()
    
    def list_components(self, component_type: str, show_all_versions: bool = False) -> None:
        """List all components of specified type."""
        session = self.Session()
        try:
            if component_type == "prompt_templates":
                if show_all_versions:
                    components = session.query(PromptTemplate).order_by(PromptTemplate.name, PromptTemplate.version).all()
                else:
                    # Get latest version of each prompt template
                    components = []
                    names = session.query(PromptTemplate.name).distinct().all()
                    for (name,) in names:
                        latest = session.query(PromptTemplate).filter_by(name=name).order_by(desc(PromptTemplate.created_at)).first()
                        components.append(latest)
                
                print(f"\n📝 Prompt Templates ({len(components)} {'versions' if show_all_versions else 'templates'})")
                for pt in components:
                    status_icon = "✅" if pt.validation_status == "validated" else "🟡" if pt.validation_status == "tested" else "⚪"
                    print(f"   {status_icon} {pt.name}:{pt.version} ({pt.template_type}) - {pt.validation_status}")
                    if pt.description:
                        print(f"      {pt.description}")
            
            elif component_type == "frameworks":
                if show_all_versions:
                    components = session.query(FrameworkVersion).order_by(FrameworkVersion.framework_name, FrameworkVersion.version).all()
                else:
                    # Get latest version of each framework
                    components = []
                    names = session.query(FrameworkVersion.framework_name).distinct().all()
                    for (name,) in names:
                        latest = session.query(FrameworkVersion).filter_by(framework_name=name).order_by(desc(FrameworkVersion.created_at)).first()
                        components.append(latest)
                
                print(f"\n🏗️  Framework Versions ({len(components)} {'versions' if show_all_versions else 'frameworks'})")
                for fv in components:
                    status_icon = "✅" if fv.validation_status == "validated" else "🟡" if fv.validation_status == "tested" else "⚪"
                    print(f"   {status_icon} {fv.framework_name}:{fv.version} - {fv.validation_status}")
                    if fv.description:
                        print(f"      {fv.description}")
            
            elif component_type == "weighting_methods":
                if show_all_versions:
                    components = session.query(WeightingMethodology).order_by(WeightingMethodology.name, WeightingMethodology.version).all()
                else:
                    # Get latest version of each weighting methodology
                    components = []
                    names = session.query(WeightingMethodology.name).distinct().all()
                    for (name,) in names:
                        latest = session.query(WeightingMethodology).filter_by(name=name).order_by(desc(WeightingMethodology.created_at)).first()
                        components.append(latest)
                
                print(f"\n⚖️  Weighting Methodologies ({len(components)} {'versions' if show_all_versions else 'methodologies'})")
                for wm in components:
                    status_icon = "✅" if wm.validation_status == "validated" else "🟡" if wm.validation_status == "tested" else "⚪"
                    print(f"   {status_icon} {wm.name}:{wm.version} ({wm.algorithm_type}) - {wm.validation_status}")
                    if wm.algorithm_description:
                        print(f"      {wm.algorithm_description}")
            
            else:
                print(f"❌ Unknown component type: {component_type}")
                
        finally:
            session.close()
    
    def show_component_details(self, component_type: str, name: str, version: str = None) -> None:
        """Show detailed information about a component."""
        session = self.Session()
        try:
            if component_type == "prompt_templates":
                if version:
                    component = session.query(PromptTemplate).filter_by(name=name, version=version).first()
                else:
                    component = session.query(PromptTemplate).filter_by(name=name).order_by(desc(PromptTemplate.created_at)).first()
                
                if not component:
                    print(f"❌ Prompt template not found: {name}" + (f":{version}" if version else ""))
                    return
                
                print(f"\n📝 Prompt Template: {component.name}:{component.version}")
                print(f"   Type: {component.template_type}")
                print(f"   Status: {component.validation_status}")
                print(f"   Created: {component.created_at}")
                print(f"   Usage Count: {component.usage_count or 0}")
                if component.success_rate:
                    print(f"   Success Rate: {component.success_rate:.1%}")
                if component.description:
                    print(f"   Description: {component.description}")
                if component.development_notes:
                    print(f"   Development Notes: {component.development_notes}")
                
                print(f"\n   Template Content:")
                print(f"   {'-' * 50}")
                print(f"   {component.template_content}")
                print(f"   {'-' * 50}")
            
            elif component_type == "frameworks":
                if version:
                    component = session.query(FrameworkVersion).filter_by(framework_name=name, version=version).first()
                else:
                    component = session.query(FrameworkVersion).filter_by(framework_name=name).order_by(desc(FrameworkVersion.created_at)).first()
                
                if not component:
                    print(f"❌ Framework not found: {name}" + (f":{version}" if version else ""))
                    return
                
                print(f"\n🏗️  Framework: {component.framework_name}:{component.version}")
                print(f"   Status: {component.validation_status}")
                print(f"   Created: {component.created_at}")
                print(f"   Usage Count: {component.usage_count or 0}")
                if component.average_coherence:
                    print(f"   Avg Coherence: {component.average_coherence:.3f}")
                if component.framework_fit_average:
                    print(f"   Avg Framework Fit: {component.framework_fit_average:.3f}")
                if component.description:
                    print(f"   Description: {component.description}")
                if component.theoretical_foundation:
                    print(f"   Theoretical Foundation: {component.theoretical_foundation}")
                
                print(f"\n   Dipoles ({len(component.dipoles_json)} dipoles):")
                for dipole_name, dipole_config in component.dipoles_json.items():
                    print(f"      {dipole_name}: {dipole_config}")
            
            elif component_type == "weighting_methods":
                if version:
                    component = session.query(WeightingMethodology).filter_by(name=name, version=version).first()
                else:
                    component = session.query(WeightingMethodology).filter_by(name=name).order_by(desc(WeightingMethodology.created_at)).first()
                
                if not component:
                    print(f"❌ Weighting methodology not found: {name}" + (f":{version}" if version else ""))
                    return
                
                print(f"\n⚖️  Weighting Methodology: {component.name}:{component.version}")
                print(f"   Algorithm Type: {component.algorithm_type}")
                print(f"   Status: {component.validation_status}")
                print(f"   Created: {component.created_at}")
                print(f"   Usage Count: {component.usage_count or 0}")
                print(f"   Mathematical Validation: {'✅' if component.mathematical_validation else '❌'}")
                if component.stability_coefficient:
                    print(f"   Stability Coefficient: {component.stability_coefficient:.3f}")
                print(f"   Description: {component.algorithm_description}")
                if component.mathematical_formula:
                    print(f"   Formula: {component.mathematical_formula}")
                if component.implementation_notes:
                    print(f"   Implementation Notes: {component.implementation_notes}")
                
                print(f"\n   Parameters:")
                for param_name, param_value in component.parameters_json.items():
                    print(f"      {param_name}: {param_value}")
            
            else:
                print(f"❌ Unknown component type: {component_type}")
                
        finally:
            session.close()
    
    def update_component_status(self, component_type: str, name: str, version: str, 
                              status: str, notes: str = None) -> None:
        """Update component validation status."""
        session = self.Session()
        try:
            valid_statuses = ["draft", "tested", "validated", "deprecated"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
            
            component = None
            if component_type == "prompt_templates":
                component = session.query(PromptTemplate).filter_by(name=name, version=version).first()
            elif component_type == "frameworks":
                component = session.query(FrameworkVersion).filter_by(framework_name=name, version=version).first()
            elif component_type == "weighting_methods":
                component = session.query(WeightingMethodology).filter_by(name=name, version=version).first()
            
            if not component:
                print(f"❌ Component not found: {name}:{version}")
                return
            
            old_status = component.validation_status
            component.validation_status = status
            
            if notes and hasattr(component, 'development_notes'):
                component.development_notes = notes
            
            session.commit()
            
            print(f"✅ Updated {component_type} {name}:{version}")
            print(f"   Status: {old_status} → {status}")
            if notes:
                print(f"   Notes: {notes}")
                
        finally:
            session.close()


def main():
    """CLI entry point for component version manager."""
    parser = argparse.ArgumentParser(description="Component Version Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create prompt template
    create_prompt_parser = subparsers.add_parser('create-prompt', help='Create new prompt template')
    create_prompt_parser.add_argument('--name', required=True, help='Prompt template name')
    create_prompt_parser.add_argument('--version', required=True, help='Version string')
    create_prompt_parser.add_argument('--template-file', required=True, help='File containing template content')
    create_prompt_parser.add_argument('--type', default='standard', choices=['standard', 'hierarchical'], help='Template type')
    create_prompt_parser.add_argument('--description', help='Description of the template')
    create_prompt_parser.add_argument('--parent-version', help='Parent version for this iteration')
    create_prompt_parser.add_argument('--notes', help='Development notes')
    
    # Create framework
    create_framework_parser = subparsers.add_parser('create-framework', help='Create new framework version')
    create_framework_parser.add_argument('--name', required=True, help='Framework name')
    create_framework_parser.add_argument('--version', required=True, help='Version string')
    create_framework_parser.add_argument('--dipoles-file', required=True, help='JSON file with dipole definitions')
    create_framework_parser.add_argument('--weights-file', required=True, help='JSON file with weight configuration')
    create_framework_parser.add_argument('--description', help='Description of the framework')
    create_framework_parser.add_argument('--parent-version', help='Parent version for this iteration')
    create_framework_parser.add_argument('--foundation', help='Theoretical foundation description')
    
    # Create weighting methodology
    create_weighting_parser = subparsers.add_parser('create-weighting', help='Create new weighting methodology')
    create_weighting_parser.add_argument('--name', required=True, help='Methodology name')
    create_weighting_parser.add_argument('--version', required=True, help='Version string')
    create_weighting_parser.add_argument('--type', required=True, help='Algorithm type (e.g., linear, winner_take_most)')
    create_weighting_parser.add_argument('--description', required=True, help='Algorithm description')
    create_weighting_parser.add_argument('--parameters-file', required=True, help='JSON file with parameters')
    create_weighting_parser.add_argument('--formula', help='Mathematical formula')
    create_weighting_parser.add_argument('--parent-version', help='Parent version for this iteration')
    create_weighting_parser.add_argument('--notes', help='Implementation notes')
    
    # List components
    list_parser = subparsers.add_parser('list', help='List components')
    list_parser.add_argument('type', choices=['prompt_templates', 'frameworks', 'weighting_methods'], help='Component type')
    list_parser.add_argument('--all-versions', action='store_true', help='Show all versions, not just latest')
    
    # Show component details
    show_parser = subparsers.add_parser('show', help='Show component details')
    show_parser.add_argument('type', choices=['prompt_templates', 'frameworks', 'weighting_methods'], help='Component type')
    show_parser.add_argument('name', help='Component name')
    show_parser.add_argument('--version', help='Specific version (default: latest)')
    
    # Update status
    status_parser = subparsers.add_parser('update-status', help='Update component validation status')
    status_parser.add_argument('type', choices=['prompt_templates', 'frameworks', 'weighting_methods'], help='Component type')
    status_parser.add_argument('name', help='Component name')
    status_parser.add_argument('version', help='Component version')
    status_parser.add_argument('status', choices=['draft', 'tested', 'validated', 'deprecated'], help='New status')
    status_parser.add_argument('--notes', help='Status update notes')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        manager = ComponentVersionManager()
        
        if args.command == 'create-prompt':
            with open(args.template_file, 'r') as f:
                template_content = f.read()
            manager.create_prompt_template(
                args.name, args.version, template_content, args.type,
                args.description, args.parent_version, args.notes
            )
        
        elif args.command == 'create-framework':
            manager.create_framework_version(
                args.name, args.version, args.dipoles_file, args.weights_file,
                args.description, args.parent_version, args.foundation
            )
        
        elif args.command == 'create-weighting':
            manager.create_weighting_methodology(
                args.name, args.version, args.type, args.description,
                args.parameters_file, args.formula, args.parent_version, args.notes
            )
        
        elif args.command == 'list':
            manager.list_components(args.type, args.all_versions)
        
        elif args.command == 'show':
            manager.show_component_details(args.type, args.name, args.version)
        
        elif args.command == 'update-status':
            manager.update_component_status(args.type, args.name, args.version, args.status, args.notes)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 