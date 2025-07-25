#!/usr/bin/env python3
"""
Discernus Pre-flight Validation Script
=====================================

Collaborative validation combining Phase 1 methodology with Virtual Colleague philosophy.

Approach:
- Specification compliance validation with full Discernus specs
- Collaborative assistance: help complete missing elements 
- Methodological advisory reports (don't block, inform)
- Virtual Colleague mindset: peer reviewer, not gatekeeper
- Expert workflow support: informed consent over infallibility

Usage:
    python3 scripts/validate_experiment.py --experiment projects/my_experiment/
    python3 scripts/validate_experiment.py --experiment projects/my_experiment/ --fix-compliance
"""

import argparse
import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import os

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# from discernus.gateway.llm_gateway import LLMGateway  # TODO: Add for advanced validation

class PreFlightValidator:
    """
    Collaborative pre-flight validation for Discernus experiments.
    
    Philosophy: Virtual Colleague - helpful peer reviewer, not rigid gatekeeper.
    Goal: Help researchers achieve specification compliance and understand trade-offs.
    """
    
    def __init__(self, experiment_path: Path, fix_compliance: bool = False):
        self.experiment_path = Path(experiment_path)
        self.fix_compliance = fix_compliance
        # self.llm_gateway = LLMGateway()  # TODO: Add for LLM-powered validation
        self.issues = []
        self.advisories = []
        self.compliance_help = []
        
    def validate_experiment(self) -> Dict:
        """
        Main validation orchestration following Phase 1 collaborative methodology.
        
        Returns comprehensive report with compliance status, missing elements,
        methodological advisories, and constructive assistance.
        """
        print(f"🔍 Validating experiment: {self.experiment_path.name}")
        print("📋 Using collaborative validation methodology...")
        
        # Phase 1 Pattern: Present actual file structures, not summaries
        structure = self._analyze_file_structure()
        
        # Specification compliance validation
        experiment_compliance = self._validate_experiment_spec(structure)
        framework_compliance = self._validate_framework_spec(structure)
        corpus_compliance = self._validate_corpus_spec(structure)
        
        # Collaborative assistance: help create missing elements
        if self.fix_compliance:
            self._provide_compliance_assistance(structure)
        
        # Virtual Colleague: methodological advisory report
        methodological_advisories = self._generate_methodological_advisories(structure)
        
        # Generate final report
        report = {
            "experiment": self.experiment_path.name,
            "validation_timestamp": "2025-07-25T12:00:00Z",  # TODO: Use actual timestamp
            "overall_status": self._determine_overall_status(),
            "file_structure": structure,
            "compliance": {
                "experiment": experiment_compliance,
                "framework": framework_compliance, 
                "corpus": corpus_compliance
            },
            "issues": self.issues,
            "methodological_advisories": methodological_advisories,
            "compliance_assistance": self.compliance_help,
            "recommendations": self._generate_recommendations()
        }
        
        self._print_report(report)
        return report
    
    def _analyze_file_structure(self) -> Dict:
        """
        Phase 1 Learning: Present actual file structures, not summaries.
        """
        structure = {
            "experiment_file": None,
            "framework_file": None,
            "corpus_dir": None,
            "corpus_files": [],
            "missing_files": []
        }
        
        # Check for experiment specification
        experiment_files = list(self.experiment_path.glob("experiment.*"))
        if experiment_files:
            structure["experiment_file"] = str(experiment_files[0])
        else:
            structure["missing_files"].append("experiment.md or experiment.yaml")
            
        # Check for framework specification  
        framework_files = list(self.experiment_path.glob("framework.*"))
        if framework_files:
            structure["framework_file"] = str(framework_files[0])
        else:
            structure["missing_files"].append("framework.md")
            
        # Check for corpus directory
        corpus_dir = self.experiment_path / "corpus"
        if corpus_dir.exists():
            structure["corpus_dir"] = str(corpus_dir)
            structure["corpus_files"] = [str(f) for f in corpus_dir.glob("*") if f.is_file()]
        else:
            structure["missing_files"].append("corpus/ directory")
            
        return structure
    
    def _validate_experiment_spec(self, structure: Dict) -> Dict:
        """
        Validate against Experiment Specification v2.0 with collaborative assistance.
        """
        compliance = {"valid": True, "version": "v2.0", "issues": [], "missing_elements": []}
        
        if not structure["experiment_file"]:
            compliance["valid"] = False
            compliance["issues"].append("Missing experiment specification file")
            compliance["missing_elements"].append("experiment.md with YAML frontmatter")
            return compliance
            
        # Phase 1 Pattern: Extract YAML from markdown frontmatter
        try:
            with open(structure["experiment_file"], 'r') as f:
                content = f.read()
                
            # Phase 1 Technical Pattern: YAML frontmatter extraction
            if '---' in content:
                parts = content.split('---')
                if len(parts) >= 2:
                    yaml_content = parts[1].strip()
                else:
                    yaml_content = parts[0].strip()
            else:
                yaml_content = content
                
            experiment = yaml.safe_load(yaml_content)
            
            # Check required fields per Experiment Specification v2.0
            required_fields = ['name', 'corpus_path', 'frameworks']
            for field in required_fields:
                if field not in experiment:
                    compliance["valid"] = False
                    compliance["missing_elements"].append(f"Required field: {field}")
                    
        except Exception as e:
            compliance["valid"] = False
            compliance["issues"].append(f"Error parsing experiment file: {e}")
            
        return compliance
    
    def _validate_framework_spec(self, structure: Dict) -> Dict:
        """
        Validate against Framework Specification v4.0 with collaborative assistance.
        """
        compliance = {"valid": True, "version": "v4.0", "issues": [], "missing_elements": []}
        
        if not structure["framework_file"]:
            compliance["valid"] = False
            compliance["issues"].append("Missing framework specification file")
            compliance["missing_elements"].append("framework.md with YAML appendix")
            return compliance
            
        try:
            with open(structure["framework_file"], 'r') as f:
                content = f.read()
                
            # Check for v4.0 YAML appendix (Phase 1 learning: missing JSON appendixes)
            if '```yaml' not in content and '```json' not in content:
                compliance["valid"] = False
                compliance["missing_elements"].append("Framework v4.0 requires machine-readable YAML/JSON appendix")
                
        except Exception as e:
            compliance["valid"] = False
            compliance["issues"].append(f"Error reading framework file: {e}")
            
        return compliance
    
    def _validate_corpus_spec(self, structure: Dict) -> Dict:
        """
        Validate against Corpus Specification v2.0 with collaborative assistance.
        """
        compliance = {"valid": True, "version": "v2.0", "issues": [], "missing_elements": []}
        
        if not structure["corpus_dir"]:
            compliance["valid"] = False
            compliance["issues"].append("Missing corpus directory")
            compliance["missing_elements"].append("corpus/ directory with manifest")
            return compliance
            
        # Check for corpus manifest (Phase 1 learning: missing manifests)
        corpus_manifest = Path(structure["corpus_dir"]) / "corpus.md"
        if not corpus_manifest.exists():
            compliance["valid"] = False
            compliance["missing_elements"].append("corpus.md manifest file per Corpus Specification v2.0")
            
        # Basic corpus statistics
        corpus_files = structure["corpus_files"]
        if len(corpus_files) == 0:
            compliance["valid"] = False
            compliance["issues"].append("Empty corpus directory")
        else:
            compliance["stats"] = {
                "document_count": len(corpus_files),
                "estimated_tokens": self._estimate_corpus_tokens(corpus_files)
            }
            
        return compliance
    
    def _generate_methodological_advisories(self, structure: Dict) -> List[Dict]:
        """
        Sarah Chen Journey: Generate methodological advisory reports, don't block workflows.
        
        Goal: Informed consent over infallibility. Document trade-offs for expert users.
        """
        advisories = []
        
        # Check for potential methodological concerns (Sarah Chen pattern)
        if structure["framework_file"]:
            try:
                with open(structure["framework_file"], 'r') as f:
                    framework_content = f.read()
                    
                # Look for dimensions that might rely on LLM's latent knowledge
                if 'ideology' in framework_content.lower() or 'political' in framework_content.lower():
                    advisories.append({
                        "type": "methodological_concern",
                        "severity": "advisory",
                        "title": "Latent Knowledge Dependency Detected",
                        "description": "Framework appears to classify political/ideological dimensions. Ensure explicit linguistic markers are provided or validate LLM classifications manually.",
                        "sarah_chen_pattern": True,
                        "recommendation": "Consider providing explicit classification criteria or plan for manual validation of results."
                    })
                    
            except Exception:
                pass
                
        return advisories
    
    def _provide_compliance_assistance(self, structure: Dict):
        """
        Phase 1 Learning: Collaborative assistance - help create missing elements.
        """
        print("\n🔧 Providing compliance assistance...")
        
        # Help create missing corpus manifest
        if structure["corpus_dir"] and not (Path(structure["corpus_dir"]) / "corpus.md").exists():
            self._create_corpus_manifest(structure["corpus_dir"], structure["corpus_files"])
            
        # Help add framework YAML appendix
        if structure["framework_file"]:
            self._suggest_framework_appendix(structure["framework_file"])
    
    def _create_corpus_manifest(self, corpus_dir: str, corpus_files: List[str]):
        """
        Phase 1 Pattern: Create missing manifests for researchers.
        """
        manifest_path = Path(corpus_dir) / "corpus.md"
        
        manifest_content = f"""# Corpus Manifest

## Metadata
- **Document Count**: {len(corpus_files)}
- **Collection Date**: 2025-07-25
- **Preparation Method**: Manual curation

## Document Inventory

```json
{{
    "documents": [
"""
        
        for i, file_path in enumerate(corpus_files):
            filename = Path(file_path).name
            manifest_content += f'        {{"id": "{i+1:03d}", "filename": "{filename}", "type": "text"}}'
            if i < len(corpus_files) - 1:
                manifest_content += ","
            manifest_content += "\n"
                
        manifest_content += """    ]
}
```

## Notes
Generated by Discernus pre-flight validation. Please review and customize as needed.
"""
        
        with open(manifest_path, 'w') as f:
            f.write(manifest_content)
            
        self.compliance_help.append(f"✅ Created corpus manifest: {manifest_path}")
        print(f"    ✅ Created corpus manifest: {manifest_path}")
    
    def _suggest_framework_appendix(self, framework_file: str):
        """
        Phase 1 Learning: Help with missing Framework v4.0 JSON appendixes.
        """
        with open(framework_file, 'r') as f:
            content = f.read()
            
        if '```yaml' not in content and '```json' not in content:
            suggestion = """
Consider adding a Framework v4.0 machine-readable appendix:

```yaml
# Framework Configuration (v4.0)
output_contract:
  dimensions:
    - name: "primary_dimension"
      type: "numeric"
      range: [0.0, 1.0]
      description: "Primary analytical dimension"
  format: "structured_json"
  validation: "schema_required"
```
"""
            self.compliance_help.append(f"💡 Framework appendix suggestion for {framework_file}")
            print(f"    💡 Consider adding Framework v4.0 YAML appendix to {framework_file}")
    
    def _estimate_corpus_tokens(self, corpus_files: List[str]) -> Dict:
        """
        Provide token estimates for cost planning (pre-flight value).
        """
        total_chars = 0
        for file_path in corpus_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    total_chars += len(f.read())
            except Exception:
                continue
                
        # Rough estimate: ~4 chars per token
        estimated_tokens = total_chars // 4
        
        return {
            "total_characters": total_chars,
            "estimated_tokens": estimated_tokens,
            "estimated_cost_gemini_pro": f"${(estimated_tokens * 0.00125 / 1000):.2f}"
        }
    
    def _determine_overall_status(self) -> str:
        """
        Virtual Colleague philosophy: Focus on actionable guidance over pass/fail.
        """
        if len(self.issues) == 0:
            return "compliant"
        elif len([i for i in self.issues if "missing" in i.lower()]) > 0:
            return "fixable_gaps"
        else:
            return "needs_attention"
    
    def _generate_recommendations(self) -> List[str]:
        """
        Constructive recommendations following Phase 1 collaborative approach.
        """
        recommendations = []
        
        if self.compliance_help:
            recommendations.append("Review auto-generated compliance elements and customize as needed")
            
        if self.advisories:
            recommendations.append("Consider methodological advisories for publication-quality research")
            
        if not self.issues:
            recommendations.append("Experiment appears ready for processing - consider running cost estimates")
            
        return recommendations
    
    def _print_report(self, report: Dict):
        """
        Human-readable report output following Virtual Colleague philosophy.
        """
        print(f"\n📊 Pre-flight Validation Report: {report['experiment']}")
        print("=" * 60)
        
        # Overall status
        status_emoji = {"compliant": "✅", "fixable_gaps": "🔧", "needs_attention": "⚠️"}
        print(f"Status: {status_emoji.get(report['overall_status'], '❓')} {report['overall_status'].title()}")
        
        # File structure summary
        print(f"\n📁 File Structure:")
        structure = report['file_structure']
        print(f"  Experiment: {'✅' if structure['experiment_file'] else '❌'}")
        print(f"  Framework:  {'✅' if structure['framework_file'] else '❌'}")
        print(f"  Corpus:     {'✅' if structure['corpus_dir'] else '❌'} ({len(structure['corpus_files'])} files)")
        
        # Compliance summary
        print(f"\n📋 Specification Compliance:")
        for spec_type, compliance in report['compliance'].items():
            status = "✅" if compliance['valid'] else "❌"
            print(f"  {spec_type.title()} {compliance['version']}: {status}")
            
        # Issues (if any)
        if report['issues']:
            print(f"\n⚠️  Issues Found:")
            for issue in report['issues']:
                print(f"    • {issue}")
                
        # Methodological advisories (Sarah Chen approach)
        if report['methodological_advisories']:
            print(f"\n🔬 Methodological Advisories:")
            for advisory in report['methodological_advisories']:
                print(f"    • {advisory['title']}: {advisory['description']}")
                
        # Compliance assistance provided
        if report['compliance_assistance']:
            print(f"\n🔧 Compliance Assistance Provided:")
            for help_item in report['compliance_assistance']:
                print(f"    • {help_item}")
                
        # Recommendations
        if report['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"    • {rec}")
                
        # Cost estimates (if available)
        for spec_type, compliance in report['compliance'].items():
            if 'stats' in compliance:
                stats = compliance['stats']
                if 'estimated_cost_gemini_pro' in stats:
                    print(f"\n💰 Cost Estimate: ~{stats['estimated_cost_gemini_pro']} (Gemini 2.5 Pro)")
                    print(f"    Estimated tokens: ~{stats['estimated_tokens']:,}")


def main():
    parser = argparse.ArgumentParser(
        description="Discernus Pre-flight Validation - Collaborative experiment validation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 scripts/validate_experiment.py --experiment projects/my_study/
    python3 scripts/validate_experiment.py --experiment projects/my_study/ --fix-compliance
    
Philosophy:
    Virtual Colleague approach - helpful peer reviewer, not rigid gatekeeper.
    Goal: Help researchers achieve compliance and understand methodological trade-offs.
        """
    )
    
    parser.add_argument('--experiment', required=True, help='Path to experiment directory')
    parser.add_argument('--fix-compliance', action='store_true', 
                       help='Automatically create missing compliance elements')
    parser.add_argument('--output', help='Save validation report to JSON file')
    
    args = parser.parse_args()
    
    # Validate experiment path
    experiment_path = Path(args.experiment)
    if not experiment_path.exists():
        print(f"❌ Error: Experiment path does not exist: {experiment_path}")
        sys.exit(1)
        
    if not experiment_path.is_dir():
        print(f"❌ Error: Experiment path is not a directory: {experiment_path}")
        sys.exit(1)
    
    # Run validation
    validator = PreFlightValidator(experiment_path, args.fix_compliance)
    report = validator.validate_experiment()
    
    # Save report if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Report saved to: {output_path}")
    
    # Exit with appropriate code
    if report['overall_status'] == 'compliant':
        sys.exit(0)
    elif report['overall_status'] == 'fixable_gaps':
        print(f"\n🔧 Run with --fix-compliance to auto-generate missing elements")
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == '__main__':
    main() 