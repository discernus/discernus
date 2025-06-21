import argparse
from pathlib import Path

def setup_research_workspace(base_path: str):
    """
    Creates the standard directory structure for a new research workspace.
    This ensures that a new user has the necessary folders to begin
    creating frameworks, experiments, and other research assets without
    having to create them manually.

    Args:
        base_path (str): The root path where the 'research_workspaces'
                         directory should be created or verified.
    """
    workspace_path = Path(base_path) / 'research_workspaces' / 'june_2025_research_dev_workspace'
    
    print(f"Setting up research workspace at: {workspace_path}")

    # Define the directory structure
    dirs_to_create = [
        'experiments',
        'frameworks',
        'prompt_templates',
        'validation_studies',
        'evaluator_configs',
        'weighting_schemes',
        'collaboration/summaries',
        'collaboration/reviews',
        'collaboration/notes'
    ]

    # Create all directories
    for sub_dir in dirs_to_create:
        (workspace_path / sub_dir).mkdir(parents=True, exist_ok=True)
        print(f"  - Created: {workspace_path / sub_dir}")

    # Create a placeholder README in the main workspace directory
    readme_content = """# Research Development Workspace

This workspace is structured to support the Discernus research workflow.

- **/experiments**: Contains YAML definitions for experiments.
- **/frameworks**: Holds the analytical frameworks used for analysis.
- **/prompt_templates**: Stores prompt templates for the LLMs.
- **/validation_studies**: For materials related to validation work.
- **/evaluator_configs**: Configurations for different evaluators.
- **/weighting_schemes**: Contains different weighting schemes for analysis.
"""
    readme_path = workspace_path / 'README.md'
    readme_path.write_text(readme_content)
    print(f"  - Created: {readme_path}")
    
    print("\n✅ Research workspace setup complete.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Set up the standard research workspace directory structure."
    )
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help="The base path where the 'research_workspaces' directory should be set up. Defaults to the current directory."
    )
    args = parser.parse_args()
    
    setup_research_workspace(args.path) 