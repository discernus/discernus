"""
Security boundary for experiment isolation.

Enforces filesystem boundaries and prevents access outside experiment directory.
"""

from pathlib import Path
from typing import Union


class SecurityError(Exception):
    """Security boundary violation."""
    pass


class ExperimentSecurityBoundary:
    """
    Security boundary for experiment isolation.
    
    Enforces filesystem boundaries and prevents access outside experiment directory.
    """
    
    def __init__(self, experiment_path: Union[str, Path]):
        """
        Initialize security boundary.
        
        Args:
            experiment_path: Path to experiment directory
        """
        self.experiment_path = Path(experiment_path).resolve()
        self.experiment_name = self.experiment_path.name
        
        if not self.experiment_path.exists():
            raise SecurityError(f"Experiment directory not found: {self.experiment_path}")
        
        if not self.experiment_path.is_dir():
            raise SecurityError(f"Not a directory: {self.experiment_path}")
    
    def secure_read_text(self, file_path: Union[str, Path]) -> str:
        """
        Securely read text file within experiment boundary.
        
        Args:
            file_path: Path to file (relative to experiment directory)
            
        Returns:
            File contents as string
            
        Raises:
            SecurityError: If file is outside experiment boundary
        """
        file_path = Path(file_path).resolve()
        
        if not file_path.exists():
            raise SecurityError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise SecurityError(f"Not a file: {file_path}")
        
        try:
            relative = file_path.relative_to(self.experiment_path)
        except ValueError:
            raise SecurityError(f"File outside experiment boundary: {file_path}")
        
        return file_path.read_text()
    
    def secure_read_bytes(self, file_path: Union[str, Path]) -> bytes:
        """
        Securely read binary file within experiment boundary.
        
        Args:
            file_path: Path to file (relative to experiment directory)
            
        Returns:
            File contents as bytes
            
        Raises:
            SecurityError: If file is outside experiment boundary
        """
        file_path = Path(file_path).resolve()
        
        if not file_path.exists():
            raise SecurityError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise SecurityError(f"Not a file: {file_path}")
        
        try:
            relative = file_path.relative_to(self.experiment_path)
        except ValueError:
            raise SecurityError(f"File outside experiment boundary: {file_path}")
        
        return file_path.read_bytes()
    
    def secure_write_text(self, file_path: Union[str, Path], content: str) -> None:
        """
        Securely write text file within experiment boundary.
        
        Args:
            file_path: Path to file (relative to experiment directory)
            content: Text content to write
            
        Raises:
            SecurityError: If file is outside experiment boundary
        """
        file_path = Path(file_path).resolve()
        
        try:
            relative = file_path.relative_to(self.experiment_path)
        except ValueError:
            raise SecurityError(f"File outside experiment boundary: {file_path}")
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
    
    def secure_write_bytes(self, file_path: Union[str, Path], content: bytes) -> None:
        """
        Securely write binary file within experiment boundary.
        
        Args:
            file_path: Path to file (relative to experiment directory)
            content: Binary content to write
            
        Raises:
            SecurityError: If file is outside experiment boundary
        """
        file_path = Path(file_path).resolve()
        
        try:
            relative = file_path.relative_to(self.experiment_path)
        except ValueError:
            raise SecurityError(f"File outside experiment boundary: {file_path}")
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content) 