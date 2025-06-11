"""
Framework Interface for Narrative Gravity Analysis Chatbot

Provides chatbot integration with existing framework management system.
Handles framework switching, explanation, and validation.
"""

import json
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import existing framework manager
try:
    from ..framework_manager import FrameworkManager
except ImportError:
    # Fallback for testing or if import path changes
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from framework_manager import FrameworkManager

class FrameworkInterface:
    """
    Interface between chatbot and existing framework management system.
    
    Provides natural language explanations and framework operations
    while integrating with the established framework architecture.
    """
    
    def __init__(self, base_dir: str = "."):
        self.framework_manager = FrameworkManager(base_dir)
        self.frameworks_cache = {}
        self._load_framework_cache()
    
    def _load_framework_cache(self) -> None:
        """Load framework information into cache for quick access."""
        try:
            frameworks = self.framework_manager.list_frameworks()
            for fw in frameworks:
                self.frameworks_cache[fw['name']] = fw
        except Exception as e:
            print(f"Warning: Could not load frameworks cache: {e}")
    
    def get_available_frameworks(self) -> List[Dict[str, str]]:
        """
        Get list of available frameworks with descriptions.
        
        Returns:
            List of framework dictionaries with name, description, version
        """
        try:
            return self.framework_manager.list_frameworks()
        except Exception as e:
            print(f"Error getting frameworks: {e}")
            return []
    
    def get_current_framework(self) -> Optional[str]:
        """
        Get currently active framework.
        
        Returns:
            Name of active framework or None if not set
        """
        try:
            return self.framework_manager.get_active_framework()
        except Exception as e:
            print(f"Error getting active framework: {e}")
            return None
    
    def switch_framework(self, framework_name: str) -> tuple[bool, str]:
        """
        Switch to a different framework.
        
        Args:
            framework_name: Name of framework to switch to
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Map display names to framework IDs
            framework_mapping = {
                'fukuyama identity': 'fukuyama_identity',
                'fukuyama': 'fukuyama_identity',
                'civic virtue': 'civic_virtue',
                'political spectrum': 'political_spectrum',
                'moral rhetorical posture': 'moral_rhetorical_posture',
                'rhetorical posture': 'moral_rhetorical_posture'
            }
            
            # Normalize framework name
            normalized_name = framework_mapping.get(framework_name.lower(), framework_name)
            
            # Try switching
            self.framework_manager.switch_framework(normalized_name)
            
            # Verify the switch worked
            current = self.get_current_framework()
            if current == normalized_name:
                return True, f"✅ Switched to {self._get_display_name(normalized_name)} framework"
            else:
                return False, f"❌ Failed to switch to {framework_name}"
                
        except Exception as e:
            return False, f"❌ Error switching framework: {str(e)}"
    
    def explain_framework(self, framework_name: Optional[str] = None) -> str:
        """
        Generate natural language explanation of a framework.
        
        Args:
            framework_name: Framework to explain (current if None)
            
        Returns:
            Detailed explanation of the framework
        """
        if framework_name is None:
            framework_name = self.get_current_framework()
        
        if framework_name is None:
            return "❌ No framework currently active"
        
        # Load framework configuration
        framework_info = self._load_framework_details(framework_name)
        if not framework_info:
            return f"❌ Could not load information for {framework_name}"
        
        return self._generate_framework_explanation(framework_info)
    
    def explain_dipole(self, dipole_name: str, framework_name: Optional[str] = None) -> str:
        """
        Explain a specific dipole within a framework.
        
        Args:
            dipole_name: Name of dipole to explain
            framework_name: Framework context (current if None)
            
        Returns:
            Explanation of the dipole
        """
        if framework_name is None:
            framework_name = self.get_current_framework()
        
        framework_info = self._load_framework_details(framework_name)
        if not framework_info:
            return f"❌ Could not load framework information"
        
        # Search for dipole in framework
        dipole_info = self._find_dipole_info(dipole_name, framework_info)
        if not dipole_info:
            return f"❌ Dipole '{dipole_name}' not found in {framework_name} framework"
        
        return self._generate_dipole_explanation(dipole_info, framework_name)
    
    def get_framework_wells(self, framework_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get gravity wells for a framework.
        
        Args:
            framework_name: Framework to get wells for (current if None)
            
        Returns:
            Dictionary of well configurations
        """
        if framework_name is None:
            framework_name = self.get_current_framework()
        
        framework_info = self._load_framework_details(framework_name)
        if framework_info and 'wells' in framework_info:
            return framework_info['wells']
        return {}
    
    def _load_framework_details(self, framework_name: str) -> Optional[Dict]:
        """Load detailed framework configuration."""
        try:
            frameworks_dir = Path("frameworks")
            framework_path = frameworks_dir / framework_name / "framework.json"
            
            if framework_path.exists():
                with open(framework_path, 'r') as f:
                    framework_config = json.load(f)
                
                # Also load dipoles if available
                dipoles_path = frameworks_dir / framework_name / "dipoles.json"
                if dipoles_path.exists():
                    with open(dipoles_path, 'r') as f:
                        dipoles_config = json.load(f)
                    framework_config['dipoles'] = dipoles_config.get('dipoles', [])
                
                return framework_config
        except Exception as e:
            print(f"Error loading framework {framework_name}: {e}")
        
        return None
    
    def _generate_framework_explanation(self, framework_info: Dict) -> str:
        """Generate natural language explanation of framework."""
        name = framework_info.get('display_name', framework_info.get('framework_name', 'Unknown'))
        description = framework_info.get('description', 'No description available')
        version = framework_info.get('version', 'Unknown version')
        
        explanation = f"**{name}** ({version})\n\n{description}\n\n"
        
        # Explain dipoles if available
        if 'dipoles' in framework_info:
            explanation += "**Core Dipoles:**\n"
            for i, dipole in enumerate(framework_info['dipoles'], 1):
                pos_name = dipole['positive']['name']
                neg_name = dipole['negative']['name']
                dipole_desc = dipole.get('description', '')
                
                explanation += f"{i}. **{dipole['name']}**: {pos_name} vs {neg_name}\n"
                if dipole_desc:
                    explanation += f"   _{dipole_desc}_\n"
        
        # Explain wells if available
        if 'wells' in framework_info:
            explanation += f"\n**Gravity Wells** ({len(framework_info['wells'])} total):\n"
            integrative_wells = []
            disintegrative_wells = []
            
            for well_name, well_config in framework_info['wells'].items():
                well_type = well_config.get('type', 'unknown')
                weight = well_config.get('weight', 0)
                angle = well_config.get('angle', 0)
                
                well_summary = f"• **{well_name}** ({angle}°, weight: {weight})"
                
                if well_type == 'integrative':
                    integrative_wells.append(well_summary)
                else:
                    disintegrative_wells.append(well_summary)
            
            if integrative_wells:
                explanation += "\n*Integrative Wells:*\n" + "\n".join(integrative_wells)
            if disintegrative_wells:
                explanation += "\n\n*Disintegrative Wells:*\n" + "\n".join(disintegrative_wells)
        
        return explanation
    
    def _find_dipole_info(self, dipole_name: str, framework_info: Dict) -> Optional[Dict]:
        """Find specific dipole information within framework."""
        if 'dipoles' not in framework_info:
            return None
        
        dipole_name_lower = dipole_name.lower()
        
        for dipole in framework_info['dipoles']:
            # Check dipole name
            if dipole['name'].lower() == dipole_name_lower:
                return dipole
            
            # Check positive/negative pole names
            if (dipole['positive']['name'].lower() == dipole_name_lower or
                dipole['negative']['name'].lower() == dipole_name_lower):
                return dipole
        
        return None
    
    def _generate_dipole_explanation(self, dipole_info: Dict, framework_name: str) -> str:
        """Generate explanation for a specific dipole."""
        dipole_name = dipole_info['name']
        description = dipole_info.get('description', '')
        
        pos_pole = dipole_info['positive']
        neg_pole = dipole_info['negative']
        
        explanation = f"**{dipole_name}** in {self._get_display_name(framework_name)}\n\n"
        
        if description:
            explanation += f"_{description}_\n\n"
        
        explanation += f"**{pos_pole['name']}** (Integrative)\n"
        explanation += f"{pos_pole['description']}\n"
        if 'language_cues' in pos_pole:
            cues = ", ".join(pos_pole['language_cues'][:5])  # First 5 cues
            explanation += f"*Language cues*: {cues}...\n\n"
        
        explanation += f"**{neg_pole['name']}** (Disintegrative)\n"
        explanation += f"{neg_pole['description']}\n"
        if 'language_cues' in neg_pole:
            cues = ", ".join(neg_pole['language_cues'][:5])  # First 5 cues
            explanation += f"*Language cues*: {cues}...\n"
        
        return explanation
    
    def _get_display_name(self, framework_name: str) -> str:
        """Get human-readable display name for framework."""
        display_names = {
            'fukuyama_identity': 'Fukuyama Identity Framework',
            'civic_virtue': 'Civic Virtue Framework',
            'political_spectrum': 'Political Spectrum Framework',
            'moral_rhetorical_posture': 'Moral-Rhetorical Posture Framework'
        }
        return display_names.get(framework_name, framework_name)
    
    def validate_framework_exists(self, framework_name: str) -> bool:
        """
        Check if a framework exists.
        
        Args:
            framework_name: Name of framework to validate
            
        Returns:
            True if framework exists
        """
        frameworks = self.get_available_frameworks()
        framework_names = [fw['name'] for fw in frameworks]
        return framework_name in framework_names
    
    def get_framework_summary(self) -> str:
        """
        Get summary of all available frameworks.
        
        Returns:
            Summary text of available frameworks
        """
        frameworks = self.get_available_frameworks()
        current = self.get_current_framework()
        
        if not frameworks:
            return "❌ No frameworks available"
        
        summary = f"**Available Frameworks** (Current: *{self._get_display_name(current) if current else 'None'}*)\n\n"
        
        for fw in frameworks:
            name = fw['name']
            display_name = self._get_display_name(name)
            version = fw.get('version', 'Unknown')
            description = fw.get('description', 'No description')[:100] + "..."
            
            marker = "🎯 " if name == current else "• "
            summary += f"{marker}**{display_name}** ({version})\n  {description}\n\n"
        
        return summary 