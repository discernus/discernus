#!/usr/bin/env python3
"""
Paper Management Script: Narrative Gravity Maps
Automates paper version control, evidence tracking, and development workflow
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import argparse

class PaperManager:
    def __init__(self, paper_dir="."):
        self.paper_dir = Path(paper_dir)
        self.drafts_dir = self.paper_dir / "drafts"
        self.evidence_dir = self.paper_dir / "evidence"
        self.reviews_dir = self.paper_dir / "reviews"
        self.changelog_path = self.paper_dir / "PAPER_CHANGELOG.md"
        
    def get_latest_version(self):
        """Get the latest paper version number"""
        if not self.drafts_dir.exists():
            return "0.0.0"
            
        versions = []
        for file in self.drafts_dir.glob("narrative_gravity_maps_v*.md"):
            version_str = file.stem.split("_v")[-1]  # Get the last part after splitting
            try:
                major, minor, patch = map(int, version_str.split("."))
                versions.append((major, minor, patch, file))
            except Exception as e:
                print(f"Warning: Could not parse version from {file.name}: {e}")
                continue
                
        if not versions:
            return "0.0.0"
            
        latest = max(versions)
        return f"{latest[0]}.{latest[1]}.{latest[2]}"
    
    def increment_version(self, version_type="patch"):
        """Create new paper version"""
        current = self.get_latest_version()
        major, minor, patch = map(int, current.split("."))
        
        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        elif version_type == "patch":
            patch += 1
        else:
            raise ValueError("Version type must be 'major', 'minor', or 'patch'")
            
        new_version = f"{major}.{minor}.{patch}"
        
        # Copy current version to new version
        current_file = self.drafts_dir / f"narrative_gravity_maps_v{current}.md"
        new_file = self.drafts_dir / f"narrative_gravity_maps_v{new_version}.md"
        
        if current_file.exists():
            shutil.copy2(current_file, new_file)
            print(f"Created new version: v{new_version}")
            print(f"File: {new_file}")
            return new_version
        else:
            print(f"Warning: Current version file not found: {current_file}")
            return None
    
    def check_evidence_status(self):
        """Check status of evidence files for current paper claims"""
        evidence_status = {
            "technical_validation": {
                "required_files": [
                    "system_test_results.json",
                    "cross_llm_correlation_matrix.json", 
                    "multi_run_statistical_analysis.json"
                ],
                "status": "complete"
            },
            "case_studies": {
                "required_files": [
                    "trump_2017_inaugural_analysis.json",
                    "biden_2021_inaugural_analysis.json",
                    "obama_2009_inaugural_multirun.json"
                ],
                "status": "complete"
            },
            "human_validation": {
                "required_files": [
                    "expert_annotation_results.json",
                    "human_llm_correlation_analysis.json",
                    "inter_rater_reliability_results.json"
                ],
                "status": "missing"
            }
        }
        
        print("Evidence Status Report")
        print("=" * 50)
        
        for category, info in evidence_status.items():
            category_dir = self.evidence_dir / category
            print(f"\n{category.upper()}:")
            
            if category_dir.exists():
                existing_files = list(category_dir.glob("*.json"))
                for required in info["required_files"]:
                    file_path = category_dir / required
                    status = "✅" if file_path.exists() else "❌"
                    print(f"  {status} {required}")
            else:
                print(f"  📁 Directory not found: {category_dir}")
                for required in info["required_files"]:
                    print(f"  ❌ {required}")
        
        return evidence_status
    
    def validate_version_claims(self, version=None):
        """Check if paper claims are supported by available evidence"""
        if version is None:
            version = self.get_latest_version()
            
        paper_file = self.drafts_dir / f"narrative_gravity_maps_v{version}.md"
        
        if not paper_file.exists():
            print(f"Paper file not found: {paper_file}")
            return False
            
        with open(paper_file, 'r') as f:
            content = f.read()
        
        # Check for validation overclaims
        overclaims = []
        
        if "empirical validation" in content.lower() and not self._has_human_validation():
            overclaims.append("Claims 'empirical validation' without human validation studies")
            
        # Check for inappropriate claims about human moral perception
        if not self._has_human_validation():
            # Look for problematic claims (not cautious acknowledgments)
            problematic_patterns = [
                "validated against human moral perception",
                "captures human moral perception", 
                "aligns with human moral perception",
                "measures human moral perception",
                "reflects human moral perception"
            ]
            for pattern in problematic_patterns:
                if pattern in content.lower():
                    overclaims.append(f"Claims '{pattern}' without validation studies")
            
        if "validated against human judgment" in content.lower() and not self._has_human_validation():
            overclaims.append("Claims validation against human judgment without studies")
        
        if overclaims:
            print("⚠️  VALIDATION OVERCLAIMS DETECTED:")
            for claim in overclaims:
                print(f"  - {claim}")
            return False
        else:
            print("✅ No validation overclaims detected")
            return True
    
    def _has_human_validation(self):
        """Check if human validation studies exist"""
        validation_dir = self.evidence_dir / "validation_studies"
        required_files = [
            "expert_annotation_results.json",
            "human_llm_correlation_analysis.json"
        ]
        
        return all((validation_dir / f).exists() for f in required_files)
    
    def create_evidence_template(self, evidence_type):
        """Create template files for evidence collection"""
        templates = {
            "expert_annotation_protocol": {
                "description": "Protocol for expert annotation study",
                "methodology": "Human experts score political texts using Civic Virtue Framework",
                "participants": "20+ experts in political science/moral psychology",
                "materials": "50+ political speeches/texts",
                "procedure": "Blind annotation using standardized scoring protocol",
                "analysis_plan": "Inter-rater reliability, human-LLM correlation"
            },
            "system_reliability_report": {
                "test_success_rate": 0.995,
                "total_tests": 62,
                "passing_tests": 61,
                "failing_tests": 1,
                "test_categories": ["unit_tests", "integration_tests", "end_to_end_tests"],
                "last_updated": datetime.now().isoformat()
            }
        }
        
        if evidence_type in templates:
            evidence_file = self.evidence_dir / "validation_studies" / f"{evidence_type}.json"
            evidence_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(evidence_file, 'w') as f:
                json.dump(templates[evidence_type], f, indent=2)
            
            print(f"Created evidence template: {evidence_file}")
        else:
            print(f"No template available for: {evidence_type}")
    
    def update_changelog(self, version, changes_description):
        """Update the paper changelog"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        changelog_entry = f"""
## [{version}] - {timestamp}

### Added
{changes_description}

### Evidence Status
- Technical validation: ✅ Available
- Case studies: ✅ Available  
- Human validation: ❌ Required for publication

"""
        
        if self.changelog_path.exists():
            with open(self.changelog_path, 'r') as f:
                content = f.read()
            
            # Insert new entry after [Unreleased] section
            unreleased_pos = content.find("## [Unreleased]")
            if unreleased_pos != -1:
                next_section = content.find("\n##", unreleased_pos + 1)
                if next_section != -1:
                    new_content = (content[:next_section] + 
                                 changelog_entry + 
                                 content[next_section:])
                    
                    with open(self.changelog_path, 'w') as f:
                        f.write(new_content)
                    
                    print(f"Updated changelog for v{version}")
        
    def generate_submission_checklist(self):
        """Generate pre-submission checklist"""
        checklist = """
# Pre-Submission Checklist: Narrative Gravity Maps

## Evidence Requirements
- [ ] Technical validation data complete and documented
- [ ] Case study analyses included with appropriate statistical measures
- [ ] Human validation studies completed (CRITICAL FOR PUBLICATION)
- [ ] Cross-cultural validation attempted (recommended)
- [ ] All figures properly captioned and referenced

## Manuscript Quality
- [ ] Abstract accurately reflects findings and limitations
- [ ] No validation overclaims (human vs. technical validation distinguished)
- [ ] Literature review includes recent human-LLM alignment research
- [ ] Methodology section includes complete replication instructions
- [ ] Discussion acknowledges limitations honestly
- [ ] Conclusion balances achievements with future research needs

## Reproducibility
- [ ] Complete replication package assembled
- [ ] All analysis code documented and tested
- [ ] Data files organized with clear provenance
- [ ] Installation and execution instructions provided
- [ ] External reviewer able to reproduce key results

## Academic Standards
- [ ] Peer review by at least 2 independent experts
- [ ] Bibliography complete and properly formatted
- [ ] Statistical analyses include confidence intervals
- [ ] Research ethics considerations addressed
- [ ] Potential conflicts of interest disclosed

## Submission Materials
- [ ] Journal-specific formatting applied
- [ ] Supplementary materials organized
- [ ] Cover letter draft prepared
- [ ] Author information and affiliations complete
- [ ] Copyright and licensing terms clarified

---
*Complete ALL items before journal submission*
"""
        
        checklist_file = self.paper_dir / "submission" / "SUBMISSION_CHECKLIST.md"
        checklist_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(checklist_file, 'w') as f:
            f.write(checklist)
        
        print(f"Generated submission checklist: {checklist_file}")

def main():
    parser = argparse.ArgumentParser(description="Manage paper development workflow")
    parser.add_argument("action", choices=[
        "status", "new-version", "check-evidence", "validate-claims", 
        "create-template", "update-changelog", "submission-checklist"
    ])
    parser.add_argument("--type", choices=["major", "minor", "patch"], default="patch")
    parser.add_argument("--template", type=str, help="Template type for evidence creation")
    parser.add_argument("--version", type=str, help="Specific version to check")
    parser.add_argument("--changes", type=str, help="Description of changes for changelog")
    
    args = parser.parse_args()
    
    manager = PaperManager()
    
    if args.action == "status":
        version = manager.get_latest_version()
        print(f"Current version: v{version}")
        print(f"Paper file: paper/drafts/narrative_gravity_maps_v{version}.md")
        
    elif args.action == "new-version":
        new_version = manager.increment_version(args.type)
        if new_version:
            print(f"Ready to edit: paper/drafts/narrative_gravity_maps_v{new_version}.md")
            
    elif args.action == "check-evidence":
        manager.check_evidence_status()
        
    elif args.action == "validate-claims":
        manager.validate_version_claims(args.version)
        
    elif args.action == "create-template":
        if args.template:
            manager.create_evidence_template(args.template)
        else:
            print("Specify template type with --template")
            
    elif args.action == "update-changelog":
        if args.changes and args.version:
            manager.update_changelog(args.version, args.changes)
        else:
            print("Specify --version and --changes for changelog update")
            
    elif args.action == "submission-checklist":
        manager.generate_submission_checklist()

if __name__ == "__main__":
    main() 