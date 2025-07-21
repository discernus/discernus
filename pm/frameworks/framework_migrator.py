#!/usr/bin/env python3
"""
Discernus Framework Migration Tool
=================================

Migrates historical frameworks from v3.2 YAML format to v4.0 Markdown format
with JSON appendix following the Framework Specification v4.0.

This tool:
1. Analyzes existing v3.2 YAML frameworks
2. Extracts theoretical content and configuration
3. Generates v4.0 compliant Markdown files with JSON appendix
4. Preserves all academic content and methodological details
5. Ensures coherence between documentation and execution
"""

import yaml
import json
import re
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

class FrameworkMigrator:
    def __init__(self):
        self.frameworks_dir = Path("/Volumes/code/discernus/pm/frameworks")
        self.v32_dir = self.frameworks_dir / "3_2_spec_frameworks"
        self.v4_spec_path = Path("/Volumes/code/discernus/docs/specifications/FRAMEWORK_SPECIFICATION_V4.md")
        
    def discover_v32_frameworks(self) -> List[Path]:
        """Find all v3.2 YAML framework files."""
        frameworks = []
        
        if self.v32_dir.exists():
            for yaml_file in self.v32_dir.rglob("*.yaml"):
                frameworks.append(yaml_file)
        
        return frameworks
    
    def load_yaml_framework(self, yaml_path: Path) -> Dict[str, Any]:
        """Load and parse a v3.2 YAML framework."""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove comments and parse YAML
            yaml_content = yaml.safe_load(content)
            return yaml_content
            
        except Exception as e:
            print(f"Error loading {yaml_path}: {e}")
            return {}
    
    def extract_theoretical_content(self, yaml_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract human-readable theoretical content from YAML."""
        
        sections = {}
        
        # Extract basic info
        sections['name'] = yaml_data.get('display_name', yaml_data.get('name', 'Unknown Framework'))
        sections['version'] = yaml_data.get('version', 'v4.0')
        sections['description'] = yaml_data.get('description', '')
        
        # Extract theoretical foundation
        if 'theoretical_foundation' in yaml_data:
            tf = yaml_data['theoretical_foundation']
            sections['theoretical_foundation'] = tf.get('theoretical_approach', '')
            sections['academic_validation'] = tf.get('academic_validation', '')
            sections['primary_sources'] = tf.get('primary_sources', [])
        
        # Extract components/axes information
        sections['components'] = yaml_data.get('components', {})
        sections['axes'] = yaml_data.get('axes', {})
        
        return sections
    
    def generate_analysis_prompt(self, yaml_data: Dict[str, Any]) -> str:
        """Generate a natural language analysis prompt from YAML configuration."""
        
        components = yaml_data.get('components', {})
        axes = yaml_data.get('axes', {})
        
        # Start with expert role
        prompt_parts = []
        
        # Expert priming
        prompt_parts.append("You are an expert analyst with deep knowledge of moral psychology, political discourse, and value analysis.")
        
        # Framework description
        description = yaml_data.get('description', '').split('\n')[0] if yaml_data.get('description') else ''
        if description:
            prompt_parts.append(f"Your task is to analyze the provided text using {yaml_data.get('display_name', 'this framework')}. {description}")
        
        # Components analysis
        if components:
            prompt_parts.append("This framework examines the following dimensions:")
            for comp_id, comp_data in components.items():
                desc = comp_data.get('description', '')
                cues = comp_data.get('language_cues', [])
                if desc:
                    cue_text = f" (look for: {', '.join(cues[:5])})" if cues else ""
                    prompt_parts.append(f"- **{comp_id.replace('_', ' ').title()}**: {desc}{cue_text}")
        
        # Scoring instructions
        prompt_parts.append("For each dimension, follow this process:")
        prompt_parts.append("1. Read the text systematically for relevant patterns and language")
        prompt_parts.append("2. Identify specific evidence and quotations")
        prompt_parts.append("3. Score the dimension from 0.0 to 1.0 based on strength and frequency of evidence")
        prompt_parts.append("4. Provide approximately 2 direct quotations supporting each score")
        prompt_parts.append("5. Assess your confidence in the scoring based on evidence clarity")
        
        return " ".join(prompt_parts)
    
    def generate_output_schema(self, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate output contract schema from YAML components."""
        
        schema = {}
        components = yaml_data.get('components', {})
        
        # Add worldview classification
        schema['worldview'] = 'string'
        
        # Add component scores and evidence
        for comp_id in components.keys():
            schema[f"{comp_id}_score"] = 'number'
            schema[f"{comp_id}_confidence"] = 'number'
            schema[f"{comp_id}_evidence"] = 'array'
        
        # Add standard fields
        schema['overall_analysis_confidence'] = 'number'
        schema['key_patterns_observed'] = 'string'
        
        return schema
    
    def generate_v4_markdown(self, yaml_data: Dict[str, Any], original_path: Path) -> str:
        """Generate complete v4.0 Markdown framework file."""
        
        sections = self.extract_theoretical_content(yaml_data)
        
        # Start building the markdown
        markdown_parts = []
        
        # Title and metadata
        markdown_parts.append(f"# {sections['name']}")
        markdown_parts.append(f"**Version**: {sections['version']}")
        markdown_parts.append(f"**Status**: Active")
        markdown_parts.append("")
        markdown_parts.append("---")
        markdown_parts.append("")
        
        # Executive Summary
        markdown_parts.append("## Executive Summary")
        markdown_parts.append("")
        if sections['description']:
            # Clean up description
            description = sections['description'].replace('|', '').strip()
            description = re.sub(r'\n\s*\n', '\n\n', description)
            markdown_parts.append(description)
        else:
            markdown_parts.append(f"The {sections['name']} provides a comprehensive framework for analyzing text through multiple dimensions of moral and social reasoning.")
        
        markdown_parts.append("")
        markdown_parts.append("---")
        markdown_parts.append("")
        
        # Theoretical Foundation
        markdown_parts.append("## Theoretical Foundation")
        markdown_parts.append("")
        
        if sections.get('theoretical_foundation'):
            markdown_parts.append(sections['theoretical_foundation'])
        else:
            markdown_parts.append("This framework is grounded in established research in moral psychology and political discourse analysis.")
        
        markdown_parts.append("")
        
        # Academic Sources
        if sections.get('primary_sources'):
            markdown_parts.append("### Key References")
            markdown_parts.append("")
            for source in sections['primary_sources']:
                markdown_parts.append(f"- {source}")
            markdown_parts.append("")
        
        # Framework Components
        if sections.get('components'):
            markdown_parts.append("## Framework Dimensions")
            markdown_parts.append("")
            
            for comp_id, comp_data in sections['components'].items():
                comp_name = comp_id.replace('_', ' ').title()
                markdown_parts.append(f"### {comp_name}")
                markdown_parts.append("")
                
                if comp_data.get('description'):
                    markdown_parts.append(comp_data['description'])
                    markdown_parts.append("")
                
                if comp_data.get('language_cues'):
                    markdown_parts.append("**Key Indicators:**")
                    cues = comp_data['language_cues']
                    for i in range(0, len(cues), 4):
                        chunk = cues[i:i+4]
                        markdown_parts.append(f"- {', '.join(chunk)}")
                    markdown_parts.append("")
        
        # Methodology
        markdown_parts.append("## Analytical Methodology")
        markdown_parts.append("")
        markdown_parts.append("This framework employs a systematic approach to discourse analysis:")
        markdown_parts.append("")
        markdown_parts.append("1. **Dimension Scoring**: Each dimension is scored independently from 0.0 to 1.0")
        markdown_parts.append("2. **Evidence Collection**: Approximately 2 direct quotations per dimension")
        markdown_parts.append("3. **Confidence Assessment**: Analyst confidence rated based on evidence clarity")
        markdown_parts.append("4. **Pattern Recognition**: Identification of key rhetorical and value patterns")
        markdown_parts.append("")
        
        # Academic Validation
        if sections.get('academic_validation'):
            markdown_parts.append("## Academic Validation")
            markdown_parts.append("")
            markdown_parts.append(sections['academic_validation'])
            markdown_parts.append("")
        
        # Generate JSON appendix
        json_config = self.generate_json_config(yaml_data)
        
        # Machine-readable appendix
        markdown_parts.append("---")
        markdown_parts.append("")
        markdown_parts.append("<details><summary>Machine-Readable Configuration</summary>")
        markdown_parts.append("")
        markdown_parts.append("```json")
        markdown_parts.append(json.dumps(json_config, indent=2))
        markdown_parts.append("```")
        markdown_parts.append("")
        markdown_parts.append("</details>")
        
        return "\n".join(markdown_parts)
    
    def generate_json_config(self, yaml_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the JSON configuration for the appendix."""
        
        # Extract basic info
        name = yaml_data.get('name', 'unknown_framework')
        display_name = yaml_data.get('display_name', name.replace('_', ' ').title())
        
        # Generate analysis prompt
        analysis_prompt = self.generate_analysis_prompt(yaml_data)
        
        # Generate output schema
        output_schema = self.generate_output_schema(yaml_data)
        
        config = {
            "name": name,
            "version": "v4.0",
            "display_name": display_name,
            "analysis_variants": {
                "default": {
                    "description": f"Complete implementation of the {display_name} methodology",
                    "analysis_prompt": analysis_prompt
                }
            },
            "output_contract": {
                "schema": output_schema,
                "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object."
            }
        }
        
        # Add calculation specs if present
        if 'metrics' in yaml_data:
            calculations = {}
            for metric_id, metric_data in yaml_data['metrics'].items():
                if metric_data.get('calculation'):
                    calculations[metric_id] = metric_data['calculation']
            
            if calculations:
                config['calculation_spec'] = calculations
        
        return config
    
    def migrate_framework(self, yaml_path: Path) -> bool:
        """Migrate a single framework from v3.2 to v4.0."""
        
        print(f"🔄 Migrating: {yaml_path.name}")
        
        # Load YAML
        yaml_data = self.load_yaml_framework(yaml_path)
        if not yaml_data:
            print(f"❌ Failed to load YAML data")
            return False
        
        # Generate v4.0 markdown
        markdown_content = self.generate_v4_markdown(yaml_data, yaml_path)
        
        # Determine output path
        framework_name = yaml_data.get('name', yaml_path.stem.replace('_v3_2', ''))
        output_filename = f"{framework_name}_v4.md"
        output_path = self.frameworks_dir / output_filename
        
        # Write the new framework file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"✅ Created: {output_path.name}")
            return True
            
        except Exception as e:
            print(f"❌ Error writing file: {e}")
            return False
    
    def migrate_all_frameworks(self) -> Dict[str, bool]:
        """Migrate all discovered v3.2 frameworks."""
        
        frameworks = self.discover_v32_frameworks()
        results = {}
        
        print(f"📊 Found {len(frameworks)} v3.2 frameworks to migrate")
        print("=" * 50)
        
        for framework_path in frameworks:
            success = self.migrate_framework(framework_path)
            results[str(framework_path)] = success
        
        print("=" * 50)
        successful = sum(results.values())
        print(f"✅ Successfully migrated: {successful}/{len(frameworks)} frameworks")
        
        return results
    
    def generate_migration_report(self, results: Dict[str, bool]) -> str:
        """Generate a migration report."""
        
        report_parts = []
        report_parts.append("# Framework Migration Report")
        report_parts.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_parts.append(f"**Migration**: v3.2 YAML → v4.0 Markdown")
        report_parts.append("")
        
        successful = [path for path, success in results.items() if success]
        failed = [path for path, success in results.items() if not success]
        
        report_parts.append(f"## Summary")
        report_parts.append(f"- **Total Frameworks**: {len(results)}")
        report_parts.append(f"- **Successful Migrations**: {len(successful)}")
        report_parts.append(f"- **Failed Migrations**: {len(failed)}")
        report_parts.append("")
        
        if successful:
            report_parts.append("## Successfully Migrated")
            for path in successful:
                framework_name = Path(path).stem
                report_parts.append(f"- ✅ {framework_name}")
            report_parts.append("")
        
        if failed:
            report_parts.append("## Failed Migrations")
            for path in failed:
                framework_name = Path(path).stem
                report_parts.append(f"- ❌ {framework_name}")
            report_parts.append("")
        
        report_parts.append("## Next Steps")
        report_parts.append("")
        report_parts.append("1. Review migrated frameworks for accuracy")
        report_parts.append("2. Test frameworks with sample texts")
        report_parts.append("3. Validate JSON configuration syntax")
        report_parts.append("4. Archive original v3.2 files")
        
        return "\\n".join(report_parts)

def main():
    """Main migration execution."""
    
    print("🔧 Discernus Framework Migration Tool")
    print("=====================================")
    print("Migrating v3.2 YAML → v4.0 Markdown")
    print("")
    
    migrator = FrameworkMigrator()
    
    # Discover frameworks
    frameworks = migrator.discover_v32_frameworks()
    if not frameworks:
        print("❌ No v3.2 frameworks found to migrate")
        return
    
    print(f"📋 Frameworks discovered:")
    for fw in frameworks:
        print(f"   - {fw.relative_to(migrator.frameworks_dir)}")
    print("")
    
    # Confirm migration
    response = input("🚀 Proceed with migration? (y/N): ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        return
    
    # Execute migration
    results = migrator.migrate_all_frameworks()
    
    # Generate report
    report = migrator.generate_migration_report(results)
    report_path = migrator.frameworks_dir / "migration_report.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\\n📋 Migration report saved: {report_path}")

if __name__ == "__main__":
    main()
