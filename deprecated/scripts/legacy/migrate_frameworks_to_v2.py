#!/usr/bin/env python3
"""
Framework Migration Tool v1.x → v2.0
====================================

Automatically migrates existing framework configurations to the new v2.0 specification.
Adds required fields, updates structure, and preserves existing data.

Usage:
    python scripts/migrate_frameworks_to_v2.py --all
    python scripts/migrate_frameworks_to_v2.py frameworks/civic_virtue/framework.json
    python scripts/migrate_frameworks_to_v2.py --framework civic_virtue --dry-run
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class FrameworkMigrator:
    """Migrates frameworks from v1.x to v2.0 specification."""
    
    def __init__(self):
        self.migration_log = []
        
    def migrate_framework(self, framework_path: str, dry_run: bool = False) -> Dict[str, Any]:
        """Migrate a single framework to v2.0 specification."""
        framework_name = Path(framework_path).parent.name
        
        print(f"🔄 Migrating {framework_name} to v2.0 specification...")
        
        # Load existing framework
        try:
            with open(framework_path, 'r') as f:
                old_framework = json.load(f)
        except FileNotFoundError:
            print(f"❌ Framework file not found: {framework_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in framework file: {e}")
            return None
        
        # Create new v2.0 framework structure
        new_framework = self._create_v2_framework(old_framework, framework_name)
        
        # Log changes
        changes = self._log_changes(old_framework, new_framework, framework_name)
        
        if not dry_run:
            # Backup original
            backup_path = f"{framework_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_path, 'w') as f:
                json.dump(old_framework, f, indent=2)
            print(f"📁 Backup created: {backup_path}")
            
            # Write new framework
            with open(framework_path, 'w') as f:
                json.dump(new_framework, f, indent=2)
            print(f"✅ Framework migrated: {framework_path}")
        else:
            print("🔍 DRY RUN - No files modified")
        
        # Print changes summary
        self._print_changes_summary(changes)
        
        return new_framework
    
    def _create_v2_framework(self, old_framework: Dict[str, Any], framework_name: str) -> Dict[str, Any]:
        """Create v2.0 framework structure from old framework."""
        
        # Start with required v2.0 structure
        new_framework = {
            "framework_name": old_framework.get("framework_name", framework_name),
            "display_name": old_framework.get("display_name", self._generate_display_name(framework_name)),
            "version": old_framework.get("version", f"v{datetime.now().strftime('%Y.%m.%d')}"),
            "description": old_framework.get("description", self._generate_description(framework_name))
        }
        
        # Add coordinate_system (required in v2.0)
        if "circle" in old_framework:
            new_framework["coordinate_system"] = {
                "type": "circle",
                "radius": old_framework["circle"].get("radius", 1.0),
                "description": old_framework["circle"].get("description", "Circular coordinate system for framework-agnostic positioning")
            }
        elif "ellipse" in old_framework:
            # Convert ellipse to circle
            new_framework["coordinate_system"] = {
                "type": "circle", 
                "radius": 1.0,
                "description": "Migrated from elliptical to circular coordinate system"
            }
        else:
            # Default circular system
            new_framework["coordinate_system"] = {
                "type": "circle",
                "radius": 1.0,
                "description": "Default circular coordinate system"
            }
        
        # Add positioning_strategy (required in v2.0)
        if "positioning_strategy" in old_framework:
            new_framework["positioning_strategy"] = old_framework["positioning_strategy"]
        else:
            # Infer positioning strategy from wells
            new_framework["positioning_strategy"] = self._infer_positioning_strategy(old_framework, framework_name)
        
        # Migrate wells (required in v2.0)
        if "wells" in old_framework:
            new_framework["wells"] = self._migrate_wells(old_framework["wells"])
        else:
            print(f"⚠️  No wells found in {framework_name} - this will need manual attention")
            new_framework["wells"] = {}
        
        # Add well_type_colors if present
        if "well_type_colors" in old_framework:
            new_framework["well_type_colors"] = old_framework["well_type_colors"]
        else:
            new_framework["well_type_colors"] = self._generate_default_colors(new_framework["wells"])
        
        # Add theoretical_foundation (required in v2.0)
        if "theoretical_foundation" in old_framework:
            new_framework["theoretical_foundation"] = old_framework["theoretical_foundation"]
        else:
            new_framework["theoretical_foundation"] = self._generate_theoretical_foundation(framework_name)
        
        # Migrate metrics if present
        if "metrics" in old_framework:
            new_framework["metrics"] = self._migrate_metrics(old_framework["metrics"])
        
        # Add compatibility section
        new_framework["compatibility"] = self._generate_compatibility(framework_name)
        
        # Preserve other fields
        optional_fields = ["scaling_factor", "created_by", "created_at", "last_modified"]
        for field in optional_fields:
            if field in old_framework:
                new_framework[field] = old_framework[field]
        
        # Add migration metadata
        new_framework["last_modified"] = datetime.now().isoformat()
        
        return new_framework
    
    def _migrate_wells(self, old_wells: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate wells to v2.0 format."""
        new_wells = {}
        
        for well_name, well_data in old_wells.items():
            new_well = {
                "angle": well_data.get("angle", 0),
                "weight": abs(well_data.get("weight", 1.0)),  # Ensure positive weights
                "type": well_data.get("type", "default")
            }
            
            # Add optional fields if present
            if "tier" in well_data:
                new_well["tier"] = well_data["tier"]
            if "description" in well_data:
                new_well["description"] = well_data["description"]
            else:
                new_well["description"] = f"Analysis dimension for {well_name.lower()} in narrative content"
            
            new_wells[well_name] = new_well
        
        return new_wells
    
    def _migrate_metrics(self, old_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate metrics to v2.0 format."""
        new_metrics = {}
        
        for metric_code, metric_data in old_metrics.items():
            new_metric = {
                "name": metric_data.get("name", metric_code.upper()),
                "description": metric_data.get("description", f"Metric calculation for {metric_code}")
            }
            
            # Add optional fields if present
            optional_fields = ["formula", "interpretation", "range"]
            for field in optional_fields:
                if field in metric_data:
                    new_metric[field] = metric_data[field]
            
            new_metrics[metric_code] = new_metric
        
        return new_metrics
    
    def _infer_positioning_strategy(self, old_framework: Dict[str, Any], framework_name: str) -> Dict[str, Any]:
        """Infer positioning strategy from framework characteristics."""
        wells = old_framework.get("wells", {})
        
        if not wells:
            return {
                "type": "even_distribution",
                "description": "Default even distribution positioning strategy"
            }
        
        # Check if wells are clustered
        well_types = [well.get("type", "default") for well in wells.values()]
        unique_types = set(well_types)
        
        if len(unique_types) > 1:
            # Multiple types suggest clustering
            if framework_name in ["civic_virtue", "fukuyama_identity", "moral_rhetorical_posture"]:
                return {
                    "type": "clustered_positioning",
                    "description": "Wells clustered around vertical dipoles to emphasize moral hierarchy",
                    "clusters": {
                        "top_cluster": {
                            "center_angle": 90,
                            "span": 80,
                            "well_types": ["integrative"],
                            "description": "Virtue wells clustered around top (90°) within 80° span"
                        },
                        "bottom_cluster": {
                            "center_angle": 270,
                            "span": 80,
                            "well_types": ["disintegrative"],
                            "description": "Problem wells clustered around bottom (270°) within 80° span"
                        }
                    }
                }
            elif framework_name == "political_spectrum":
                return {
                    "type": "clustered_positioning",
                    "description": "Wells clustered around horizontal axis for political left-right emphasis",
                    "clusters": {
                        "left_cluster": {
                            "center_angle": 180,
                            "span": 80,
                            "well_types": ["progressive"],
                            "description": "Progressive/left wells clustered around left (180°)"
                        },
                        "right_cluster": {
                            "center_angle": 0,
                            "span": 80,
                            "well_types": ["conservative"],
                            "description": "Conservative/right wells clustered around right (0°)"
                        }
                    }
                }
        
        # Default to even distribution
        return {
            "type": "even_distribution",
            "description": "Wells distributed evenly around circle to avoid visual hierarchy"
        }
    
    def _generate_display_name(self, framework_name: str) -> str:
        """Generate display name from framework name."""
        name_map = {
            "civic_virtue": "Civic Virtue Framework",
            "political_spectrum": "Political Spectrum Framework", 
            "mft_persuasive_force": "MFT Persuasive Force Framework",
            "fukuyama_identity": "Fukuyama Identity Framework",
            "moral_rhetorical_posture": "Moral Rhetorical Posture Framework"
        }
        return name_map.get(framework_name, framework_name.replace("_", " ").title())
    
    def _generate_description(self, framework_name: str) -> str:
        """Generate description for framework."""
        descriptions = {
            "civic_virtue": "A specialized framework for analyzing moral dimensions of political discourse through civic virtue theory, emphasizing dignity, truth, justice, and democratic values.",
            "political_spectrum": "Framework for analyzing political orientation and ideological positioning across progressive-conservative dimensions in political discourse.",
            "mft_persuasive_force": "Framework based on Moral Foundations Theory for analyzing persuasive communication through empirically-validated moral foundations.",
            "fukuyama_identity": "Framework for analyzing democratic sustainability through identity, recognition, and thymos dynamics based on Francis Fukuyama's theoretical insights.",
            "moral_rhetorical_posture": "Framework for analyzing moral-rhetorical positioning in political communication, focusing on restorative vs retributive approaches."
        }
        return descriptions.get(framework_name, f"Analysis framework for {framework_name.replace('_', ' ')} dimensions in narrative content.")
    
    def _generate_theoretical_foundation(self, framework_name: str) -> Dict[str, Any]:
        """Generate theoretical foundation for framework."""
        foundations = {
            "civic_virtue": {
                "primary_sources": [
                    "Aristotle. Nicomachean Ethics. Book VI.",
                    "Sandel, M. (2012). What Money Can't Buy: The Moral Limits of Markets.",
                    "Putnam, R. (2000). Bowling Alone: The Collapse and Revival of American Community."
                ],
                "theoretical_approach": "Draws from classical virtue ethics and contemporary civic republican theory to identify moral dimensions that strengthen or weaken democratic discourse and civic engagement. Emphasizes the role of character virtues in political communication."
            },
            "political_spectrum": {
                "primary_sources": [
                    "Converse, P. E. (1964). The nature of belief systems in mass publics.",
                    "Jost, J. T. (2006). The end of the end of ideology.",
                    "Hetherington, M. J. (2001). Resurgent mass partisanship."
                ],
                "theoretical_approach": "Based on political science research on ideological positioning and partisan identity. Analyzes political discourse along established progressive-conservative dimensions with attention to policy preferences and value orientations."
            },
            "mft_persuasive_force": {
                "primary_sources": [
                    "Haidt, J. (2012). The righteous mind: Why good people are divided by politics and religion.",
                    "Graham, J., et al. (2013). Moral foundations theory: The pragmatic validity of moral pluralism.",
                    "Clifford, S., et al. (2015). Moral foundations vignettes: A standardized stimulus database."
                ],
                "theoretical_approach": "Applies Moral Foundations Theory to analyze persuasive communication through empirically-validated moral foundations. Examines how different moral concerns resonate with different cultural and political groups."
            },
            "fukuyama_identity": {
                "primary_sources": [
                    "Fukuyama, F. (2018). Identity: The Demand for Dignity and the Politics of Resentment.",
                    "Fukuyama, F. (1992). The End of History and the Last Man.",
                    "Taylor, C. (1992). Multiculturalism and the Politics of Recognition."
                ],
                "theoretical_approach": "Analyzes democratic sustainability through identity, recognition, and thymos dynamics based on Francis Fukuyama's theoretical insights about the role of identity in modern politics and democratic institutions."
            },
            "moral_rhetorical_posture": {
                "primary_sources": [
                    "Aristotle. Rhetoric. Books I-III.",
                    "Burke, K. (1969). A Rhetoric of Motives.",
                    "Perelman, C. (1982). The Realm of Rhetoric."
                ],
                "theoretical_approach": "Combines classical rhetorical theory with moral psychology to analyze how political communication adopts different moral-rhetorical postures. Focuses on restorative vs retributive approaches to political discourse."
            }
        }
        
        default = {
            "primary_sources": [
                "Framework-specific academic sources to be added"
            ],
            "theoretical_approach": f"Theoretical foundation for {framework_name.replace('_', ' ')} analysis framework. Academic grounding and methodology to be documented."
        }
        
        return foundations.get(framework_name, default)
    
    def _generate_default_colors(self, wells: Dict[str, Any]) -> Dict[str, str]:
        """Generate default colors for well types."""
        well_types = set(well.get("type", "default") for well in wells.values())
        
        color_map = {
            "integrative": "#2E7D32",
            "disintegrative": "#C62828", 
            "progressive": "#1976D2",
            "conservative": "#C62828",
            "default": "#757575"
        }
        
        return {well_type: color_map.get(well_type, "#757575") for well_type in well_types}
    
    def _generate_compatibility(self, framework_name: str) -> Dict[str, List[str]]:
        """Generate compatibility declarations."""
        return {
            "prompt_templates": ["hierarchical_v2.1", "standard_v2.0"],
            "weighting_schemes": ["winner_take_most", "proportional"],
            "visualization_types": ["circular", "comparative"]
        }
    
    def _log_changes(self, old_framework: Dict[str, Any], new_framework: Dict[str, Any], framework_name: str) -> List[str]:
        """Log changes made during migration."""
        changes = []
        
        # Check for added fields
        old_keys = set(old_framework.keys())
        new_keys = set(new_framework.keys())
        added_keys = new_keys - old_keys
        
        for key in added_keys:
            changes.append(f"Added required field: {key}")
        
        # Check for structure changes
        if "ellipse" in old_framework and "coordinate_system" in new_framework:
            changes.append("Converted elliptical to circular coordinate system")
        
        if "wells" in old_framework and "wells" in new_framework:
            old_wells = old_framework["wells"]
            new_wells = new_framework["wells"]
            for well_name, well_data in new_wells.items():
                if well_name in old_wells:
                    old_weight = old_wells[well_name].get("weight", 1.0)
                    new_weight = well_data.get("weight", 1.0)
                    if old_weight < 0 and new_weight > 0:
                        changes.append(f"Converted negative weight to positive for well: {well_name}")
        
        return changes
    
    def _print_changes_summary(self, changes: List[str]):
        """Print summary of changes made."""
        if changes:
            print(f"\n📝 Migration Changes:")
            for i, change in enumerate(changes, 1):
                print(f"  {i}. {change}")
        else:
            print("\n📝 No structural changes needed")

def migrate_all_frameworks(migrator: FrameworkMigrator, dry_run: bool = False):
    """Migrate all frameworks in the frameworks directory."""
    frameworks_dir = Path("frameworks")
    
    if not frameworks_dir.exists():
        print("❌ Frameworks directory not found")
        return
    
    migrated_count = 0
    
    for framework_dir in frameworks_dir.iterdir():
        if framework_dir.is_dir():
            framework_file = framework_dir / "framework.json"
            if framework_file.exists():
                result = migrator.migrate_framework(str(framework_file), dry_run)
                if result:
                    migrated_count += 1
                print()  # Add spacing between frameworks
            else:
                print(f"⚠️  No framework.json found in {framework_dir.name}")
    
    print(f"🎉 Migration complete! {migrated_count} frameworks processed.")

def main():
    parser = argparse.ArgumentParser(
        description="Migrate frameworks from v1.x to v2.0 specification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Migrate all frameworks:
    python scripts/migrate_frameworks_to_v2.py --all
    
  Migrate single framework:
    python scripts/migrate_frameworks_to_v2.py frameworks/civic_virtue/framework.json
    
  Dry run (preview changes):
    python scripts/migrate_frameworks_to_v2.py --all --dry-run
        """
    )
    
    parser.add_argument(
        "framework_file",
        nargs="?",
        help="Path to framework.json file to migrate"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Migrate all frameworks in frameworks/ directory"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    
    args = parser.parse_args()
    
    if not args.framework_file and not args.all:
        parser.print_help()
        sys.exit(1)
    
    migrator = FrameworkMigrator()
    
    print("🔄 Framework Migration Tool v1.x → v2.0")
    print("=" * 50)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print()
    
    if args.all:
        migrate_all_frameworks(migrator, args.dry_run)
    else:
        migrator.migrate_framework(args.framework_file, args.dry_run)

if __name__ == "__main__":
    main() 