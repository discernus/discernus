#!/usr/bin/env python3
"""
Demo: Consolidated Framework Structure
Shows how a single-file framework definition simplifies everything
"""

import json
from pathlib import Path
from typing import Dict, Any

class ConsolidatedFrameworkManager:
    """Framework manager using single-file framework definitions"""
    
    def __init__(self, frameworks_dir: str = "frameworks"):
        self.frameworks_dir = Path(frameworks_dir)
    
    def load_framework(self, framework_name: str) -> Dict[str, Any]:
        """Load complete framework definition from single file"""
        framework_file = self.frameworks_dir / framework_name / "framework_consolidated.json"
        
        if not framework_file.exists():
            # Fallback to old multi-file approach
            return self._load_legacy_framework(framework_name)
        
        with open(framework_file, 'r') as f:
            return json.load(f)
    
    def _load_legacy_framework(self, framework_name: str) -> Dict[str, Any]:
        """Legacy loader for backward compatibility"""
        framework_dir = self.frameworks_dir / framework_name
        
        # Load multiple files (current approach)
        dipoles_file = framework_dir / "dipoles.json"
        framework_file = framework_dir / "framework.json"
        weights_file = framework_dir / "weights.json"
        
        framework_data = {}
        
        if dipoles_file.exists():
            with open(dipoles_file, 'r') as f:
                framework_data['dipoles'] = json.load(f)
        
        if framework_file.exists():
            with open(framework_file, 'r') as f:
                framework_data['framework'] = json.load(f)
        
        if weights_file.exists():
            with open(weights_file, 'r') as f:
                framework_data['weights'] = json.load(f)
        
        return framework_data

class ConsolidatedPromptGenerator:
    """Simplified prompt generation using consolidated framework data"""
    
    def __init__(self):
        self.framework_manager = ConsolidatedFrameworkManager()
    
    def generate_prompt(self, framework_name: str, text: str = None, mode: str = "api") -> str:
        """Generate prompt from consolidated framework definition"""
        
        # Load complete framework in one operation
        framework = self.framework_manager.load_framework(framework_name)
        
        # Extract information that was previously scattered across files
        meta = framework.get('framework_meta', {})
        dipoles = framework.get('dipoles', [])
        prompt_config = framework.get('prompt_configuration', {})
        weighting = framework.get('weighting_philosophy', {})
        
        # Build prompt components
        components = []
        
        # Header with version info
        components.append(f"# {meta.get('display_name', framework_name)} Analysis")
        components.append(f"Framework Version: {meta.get('version', 'unknown')}")
        components.append("")
        
        # Role definition from framework
        if 'expert_role' in prompt_config:
            components.append(prompt_config['expert_role'])
            components.append("")
        
        # Analysis focus
        if 'analysis_focus' in prompt_config:
            components.append("## Analysis Focus")
            components.append(prompt_config['analysis_focus'])
            components.append("")
        
        # Framework wells (from dipoles)
        components.append("## Framework Wells")
        components.append("")
        
        for dipole in dipoles:
            positive = dipole['positive']
            negative = dipole['negative']
            
            components.append(f"**{positive['name']} vs. {negative['name']} ({dipole['name']} Dimension)**")
            components.append(f"- {positive['name']}: {positive['description']}")
            
            # Language cues directly from framework
            pos_cues = positive.get('language_cues', [])[:5]  # Limit for brevity
            if pos_cues:
                components.append(f"  Language cues: {', '.join(pos_cues)}")
            
            components.append(f"- {negative['name']}: {negative['description']}")
            
            neg_cues = negative.get('language_cues', [])[:5]
            if neg_cues:
                components.append(f"  Language cues: {', '.join(neg_cues)}")
            
            components.append("")
        
        # Weighting philosophy
        if 'tiers' in weighting:
            components.append("## Scoring Guidelines")
            components.append(weighting.get('description', ''))
            components.append("")
            
            for tier_name, tier_info in weighting['tiers'].items():
                weight = tier_info['weight']
                wells = ', '.join(tier_info['wells'])
                components.append(f"**{tier_name.title()} Tier** ({weight:.1f}): {wells}")
                components.append(f"  {tier_info['description']}")
                components.append("")
        
        # Evidence requirements
        if 'evidence_requirements' in prompt_config:
            components.append("## Evidence Requirements")
            components.append(prompt_config['evidence_requirements'])
            components.append("")
        
        # JSON format (could be derived from dipoles automatically)
        components.append("## Response Format")
        components.append("```json")
        components.append("{")
        components.append('  "metadata": {')
        components.append(f'    "framework": "{framework_name}",')
        components.append('    "version": "' + meta.get('version', 'unknown') + '"')
        components.append('  },')
        components.append('  "wells": [')
        
        for i, dipole in enumerate(dipoles):
            pos_name = dipole['positive']['name']
            neg_name = dipole['negative']['name']
            pos_angle = dipole['positive']['angle']
            neg_angle = dipole['negative']['angle']
            
            components.append(f'    {{"name": "{pos_name}", "angle": {pos_angle}, "score": 0.0}},')
            components.append(f'    {{"name": "{neg_name}", "angle": {neg_angle}, "score": 0.0}}{"" if i == len(dipoles)-1 else ","}')
        
        components.append('  ]')
        components.append('}')
        components.append("```")
        components.append("")
        
        # Add text if provided
        if text:
            components.append("## Text to Analyze")
            components.append(f'"{text}"')
            components.append("")
        
        return "\n".join(components)

def demo_comparison():
    """Demonstrate the difference between old and new approaches"""
    
    print("🧪 Framework Definition Comparison Demo")
    print("=" * 60)
    
    # Old approach simulation
    print("\n📁 OLD APPROACH - Multi-file Loading:")
    print("   ❌ Load dipoles.json (148 lines)")
    print("   ❌ Load framework.json (146 lines)")
    print("   ❌ Load weights.json (85 lines)")
    print("   ❌ Cross-reference well names across files")
    print("   ❌ Merge duplicate weight information")
    print("   ❌ Handle inconsistent file presence")
    print("   ❌ Total: 379 lines across 3+ files")
    
    # New approach
    print("\n📄 NEW APPROACH - Single-file Loading:")
    print("   ✅ Load framework_consolidated.json (1 file)")
    print("   ✅ All information in logical structure")
    print("   ✅ No duplication or cross-referencing")
    print("   ✅ Consistent across all frameworks")
    
    # Demonstrate actual usage
    print("\n🚀 PROMPT GENERATION DEMO:")
    print("-" * 40)
    
    generator = ConsolidatedPromptGenerator()
    
    try:
        # Try consolidated approach first
        prompt = generator.generate_prompt(
            "civic_virtue", 
            "We must work together with dignity and respect.",
            mode="api"
        )
        
        print("✅ Generated prompt using consolidated framework!")
        print(f"   Prompt length: {len(prompt)} characters")
        lines_count = len(prompt.split('\n'))
        print(f"   Lines: {lines_count}")
        
        # Show first few lines
        lines = prompt.split('\n')[:15]
        print("\n   First 15 lines:")
        for i, line in enumerate(lines, 1):
            print(f"   {i:2d}: {line}")
        print("   ...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n💡 BENEFITS OF CONSOLIDATED APPROACH:")
    print("   🎯 Single source of truth per framework")
    print("   🔧 Easier maintenance and updates")
    print("   📦 Self-contained framework definitions")
    print("   🚀 Simpler loading and validation")
    print("   🧪 Easier testing and development")
    print("   📝 Framework-specific prompt configurations")
    print("   🔄 Better version control and changes")

if __name__ == "__main__":
    demo_comparison() 