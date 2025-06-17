#!/usr/bin/env python3
"""
Cleanup Root Directory

This script moves files and directories from the root directory to their proper locations
according to project standards. It includes safety checks and logging.
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/root_cleanup.log'),
        logging.StreamHandler()
    ]
)

class RootDirectoryCleaner:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.moves = {
            # Files to move
            'iditi_validation_study.json': 'experiment_reports/',
            'iditi_validation_study.yaml': 'experiment_reports/',
            'civic_virtue_real_validation_study.json': 'experiment_reports/',
            'test_iditi_analysis.py': 'tests/',
            '.cursorrules': '.files/',
            'LAUNCH_GUIDE.md': 'docs/',
            'CONTRIBUTING.md': 'docs/',
            
            # Directories to move
            'paper': 'docs/paper/',
            'analysis_results': 'exports/analysis_results/',
            'test_output': 'tests/output/',
            'model_output': 'exports/model_output/',
            'futures': 'docs/planning/futures/',
            'schemas': 'src/narrative_gravity/schemas/',
            'templates': 'src/narrative_gravity/templates/'
        }
        
        # Files to delete
        self.files_to_delete = ['.DS_Store']
        
        # Create backup directory
        self.backup_dir = self.project_root / 'tmp' / f'root_cleanup_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def backup_file(self, file_path: Path) -> None:
        """Backup a file before moving it."""
        if file_path.exists():
            backup_path = self.backup_dir / file_path.name
            shutil.copy2(file_path, backup_path)
            logging.info(f"Backed up {file_path} to {backup_path}")

    def create_destination_dir(self, dest_path: Path) -> None:
        """Create destination directory if it doesn't exist."""
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {dest_path.parent}")

    def move_file(self, src: Path, dest: Path) -> None:
        """Move a file with safety checks."""
        if not src.exists():
            logging.warning(f"Source file not found: {src}")
            return

        self.backup_file(src)
        self.create_destination_dir(dest)

        if dest.exists():
            logging.warning(f"Destination already exists: {dest}")
            return

        try:
            shutil.move(str(src), str(dest))
            logging.info(f"Moved {src} to {dest}")
        except Exception as e:
            logging.error(f"Error moving {src} to {dest}: {e}")

    def move_directory(self, src: Path, dest: Path) -> None:
        """Move a directory with safety checks."""
        if not src.exists():
            logging.warning(f"Source directory not found: {src}")
            return

        self.create_destination_dir(dest)

        if dest.exists():
            logging.warning(f"Destination directory already exists: {dest}")
            return

        try:
            shutil.move(str(src), str(dest))
            logging.info(f"Moved directory {src} to {dest}")
        except Exception as e:
            logging.error(f"Error moving directory {src} to {dest}: {e}")

    def delete_file(self, file_path: Path) -> None:
        """Delete a file with safety checks."""
        if not file_path.exists():
            logging.warning(f"File not found for deletion: {file_path}")
            return

        self.backup_file(file_path)

        try:
            file_path.unlink()
            logging.info(f"Deleted {file_path}")
        except Exception as e:
            logging.error(f"Error deleting {file_path}: {e}")

    def cleanup(self) -> None:
        """Perform the cleanup operation."""
        logging.info("Starting root directory cleanup")
        
        # Move files
        for src_name, dest_dir in self.moves.items():
            src_path = self.project_root / src_name
            dest_path = self.project_root / dest_dir / src_name
            
            if src_path.is_file():
                self.move_file(src_path, dest_path)
            elif src_path.is_dir():
                self.move_directory(src_path, dest_path)

        # Delete files
        for file_name in self.files_to_delete:
            file_path = self.project_root / file_name
            self.delete_file(file_path)

        logging.info("Cleanup completed")
        logging.info(f"Backup directory: {self.backup_dir}")

def main():
    """Main entry point."""
    try:
        cleaner = RootDirectoryCleaner()
        cleaner.cleanup()
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")
        raise

if __name__ == "__main__":
    main() 