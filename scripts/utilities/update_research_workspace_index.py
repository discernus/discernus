import re
from pathlib import Path
import argparse

def update_index(readme_path: Path, frameworks_path: Path, experiments_path: Path):
    """
    Scans the frameworks and experiments directories and updates the index tables
    in the specified README.md file.

    Args:
        readme_path (Path): The path to the README.md file to update.
        frameworks_path (Path): The path to the frameworks directory.
        experiments_path (Path): The path to the experiments directory.
    """
    print("🚀 Starting research workspace index update...")

    # --- Generate Frameworks Table ---
    frameworks_md = "| Framework Name | Purpose & Key Results |\n| :--- | :--- |\n"
    for item in sorted(frameworks_path.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            frameworks_md += f"| `{item.name}` | |\n"
    print(f"  - Found {len(frameworks_md.splitlines()) - 2} frameworks.")

    # --- Generate Experiments Table ---
    experiments_md = "| Experiment Name | Type | Purpose & Notes |\n| :--- | :--- | :--- |\n"
    for item in sorted(experiments_path.iterdir()):
        if not item.name.startswith('.'):
            item_type = "Directory" if item.is_dir() else "File"
            experiments_md += f"| `{item.name}` | {item_type} | |\n"
    print(f"  - Found {len(experiments_md.splitlines()) - 2} experiments.")

    # --- Update README.md ---
    readme_content = readme_path.read_text()

    # Replace frameworks index
    new_content = re.sub(
        r"<!-- FRAMEWORK_INDEX_START -->.*<!-- FRAMEWORK_INDEX_END -->",
        f"<!-- FRAMEWORK_INDEX_START -->\n{frameworks_md}<!-- FRAMEWORK_INDEX_END -->",
        readme_content,
        flags=re.DOTALL
    )

    # Replace experiments index
    new_content = re.sub(
        r"<!-- EXPERIMENTS_INDEX_START -->.*<!-- EXPERIMENTS_INDEX_END -->",
        f"<!-- EXPERIMENTS_INDEX_START -->\n{experiments_md}<!-- EXPERIMENTS_INDEX_END -->",
        new_content,
        flags=re.DOTALL
    )

    readme_path.write_text(new_content)
    print(f"✅ Successfully updated index in: {readme_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Automatically update the frameworks and experiments index in the research workspace README."
    )
    parser.add_argument(
        "--workspace_path",
        type=str,
        default="research_workspaces/june_2025_research_dev_workspace",
        help="Path to the specific research workspace directory."
    )
    args = parser.parse_args()

    workspace_path = Path(args.workspace_path)
    readme_path = workspace_path / "README.md"
    frameworks_path = workspace_path / "frameworks"
    experiments_path = workspace_path / "experiments"

    if not all([readme_path.exists(), frameworks_path.exists(), experiments_path.exists()]):
        print("❌ Error: README.md, frameworks/, or experiments/ directory not found in the specified workspace path.")
        return

    update_index(readme_path, frameworks_path, experiments_path)

if __name__ == "__main__":
    main() 