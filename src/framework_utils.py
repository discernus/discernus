from pathlib import Path
from typing import Optional


def get_framework_yaml_path(framework_name: str) -> Optional[str]:
    """Resolve the YAML configuration path for a given framework name.

    Searches the research workspace first then the main ``frameworks`` directory
    for a YAML configuration file. Returns the absolute path if found or ``None``
    otherwise.
    """
    # Normalize framework name for consistent lookup
    normalized = framework_name.replace("_", "").lower()

    # Map common shorthand or alternative names to their canonical directory
    mappings = {
        "moralfoundationstheory": "moral_foundations_theory",
        "mft": "moral_foundations_theory",
        "moralfoundations": "moral_foundations_theory",
        "civicvirtue": "civic_virtue",
        "iditi": "iditi",
    }
    canonical = mappings.get(normalized, normalized)

    # Determine project root (src/ -> repo root)
    project_root = Path(__file__).resolve().parents[1]

    search_paths = [
        project_root / f"research_workspaces/june_2025_research_dev_workspace/frameworks/{canonical}/{canonical}_framework.yaml",
        project_root / f"research_workspaces/june_2025_research_dev_workspace/frameworks/{canonical}/framework.yaml",
        project_root / f"frameworks/{canonical}/framework.yaml",
        project_root / f"frameworks/{canonical}/{canonical}_framework.yaml",
    ]

    for path in search_paths:
        if path.exists():
            return str(path)
    return None
