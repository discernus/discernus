import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import numpy as np
import math

# Set up a logger for this module
logger = logging.getLogger(__name__)

# Attempt to import yaml, but don't fail if it's not available.
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    yaml = None

class FrameworkLoader:
    """
    Loads framework definition files from the filesystem.
    This is a simplified version of the ConsolidatedFrameworkLoader,
    focused solely on loading framework files for the rebooted application.
    """
    def __init__(self, frameworks_base_dir: str):
        self.frameworks_base_dir = Path(frameworks_base_dir)
        if not self.frameworks_base_dir.is_dir():
            raise FileNotFoundError(f"Frameworks base directory does not exist: {self.frameworks_base_dir}")

    def load_framework(self, framework_name: str) -> Optional[Dict[str, Any]]:
        """Load framework using a pattern-matching strategy."""
        framework_dir = self.frameworks_base_dir / framework_name
        if not framework_dir.is_dir():
            logger.error(f"Framework directory not found: {framework_dir}")
            return None

        # Define search patterns for framework files
        patterns = ["*_framework.yaml", "*_framework.json", "framework.yaml", "framework.json"]
        
        for pattern in patterns:
            matches = list(framework_dir.glob(pattern))
            if matches:
                # Prefer the first match for consistency
                framework_file = sorted(matches)[0]
                logger.info(f"Loading framework '{framework_name}' from '{framework_file.name}'")
                try:
                    with open(framework_file, 'r', encoding='utf-8') as f:
                        if framework_file.suffix.lower() == '.yaml' and YAML_AVAILABLE:
                            return yaml.safe_load(f)
                        elif framework_file.suffix.lower() == '.json':
                            return json.load(f)
                except Exception as e:
                    logger.error(f"Error loading framework file {framework_file}: {e}")
                    return None
        
        logger.error(f"No valid framework file found for '{framework_name}' in {framework_dir}")
        return None

def _extract_anchors_from_framework(framework_def: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts a flat dictionary of all anchors from a framework definition."""
    anchors = {}
    axes = framework_def.get("framework", {}).get("axes", {})
    for axis in axes.values():
        if 'integrative' in axis:
            anchors[axis['integrative']['name']] = axis['integrative']
        if 'disintegrative' in axis:
            anchors[axis['disintegrative']['name']] = axis['disintegrative']
    return anchors

def calculate_coordinates(
    experiment_def: Dict[str, Any], 
    llm_scores: Dict[str, float], 
    circle_radius: float = 1.0
) -> Tuple[float, float]:
    """
    Calculates the (x, y) centroid for a set of LLM scores based on a framework.
    """
    anchors = _extract_anchors_from_framework(experiment_def)

    if not anchors:
        logger.error("Could not extract any anchors from the framework definition.")
        return 0.0, 0.0

    weighted_x, weighted_y, total_weight = 0.0, 0.0, 0.0
    
    for anchor_name, score in llm_scores.items():
        if anchor_name in anchors:
            anchor_info = anchors[anchor_name]
            angle = anchor_info.get('angle', 0)
            weight = abs(anchor_info.get('weight', 1.0))
            
            x_pos = circle_radius * np.cos(np.deg2rad(angle))
            y_pos = circle_radius * np.sin(np.deg2rad(angle))
            
            force = score * weight
            weighted_x += x_pos * force
            weighted_y += y_pos * force
            total_weight += force
            
    if total_weight > 0:
        return weighted_x / total_weight, weighted_y / total_weight
        
    return 0.0, 0.0

def _get_anchor_coordinates(experiment_def: Dict[str, Any]) -> Dict[str, Tuple[float, float]]:
    anchors = _extract_anchors_from_framework(experiment_def)
    return {anchor: calculate_coordinates(experiment_def, {anchor: 1.0}) for anchor in anchors}

def calculate_distance(point_a: Tuple[float, float], point_b: Tuple[float, float]) -> float:
    """Calculates the Euclidean distance between two points."""
    return math.sqrt((point_b[0] - point_a[0])**2 + (point_b[1] - point_a[1])**2) 