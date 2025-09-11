#!/usr/bin/env python3
"""
Security Boundary System for Discernus THIN v2.0
================================================

Enforces filesystem access restrictions to prevent agents from accessing
files outside their designated experiment boundaries.

Based on the incident where .env files were nearly sent to LLMs,
this system ensures that once an experiment starts, no agent can access
files outside the experiment directory tree.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
from pathlib import Path
from typing import Union, BinaryIO, TextIO


class SecurityError(Exception):
    """Security boundary violation exceptions"""
    pass


class ExperimentSecurityBoundary:
    """
    Filesystem security boundary that restricts all file access to within
    an experiment directory tree.
    
    Once initialized, all file operations must go through this boundary
    and are restricted to the allowed experiment root and its subdirectories.
    """
    
    def __init__(self, experiment_path: Path):
        """
        Initialize security boundary for an experiment.
        
        Args:
            experiment_path: Path to the experiment directory (containing experiment.md)
        """
        # Convert to absolute path and resolve any symlinks
        self.experiment_root = experiment_path.resolve()
        
        # Ensure this is actually an experiment directory (support both v7.3 and v8.0)
        has_v7_experiment = (self.experiment_root / "experiment.md").exists()
        has_v8_experiment = (self.experiment_root / "experiment_v8.md").exists()
        
        if not (has_v7_experiment or has_v8_experiment):
            raise SecurityError(f"Invalid experiment directory: {experiment_path} (missing experiment.md or experiment_v8.md)")
        
        # Store the boundary info for logging
        self.experiment_name = self.experiment_root.name
        
        print(f"🛡️ Security: Boundary established for experiment '{self.experiment_name}'")
        print(f"🛡️ Security: Allowed root = {self.experiment_root}")
    
    def validate_path(self, target_path: Union[str, Path]) -> Path:
        """
        Validate that a path is within the security boundary.
        
        Args:
            target_path: Path to validate
            
        Returns:
            Resolved absolute path if valid
            
        Raises:
            SecurityError: If path is outside the boundary
        """
        # Convert to Path and resolve
        path = Path(target_path).resolve()
        
        # Check if the resolved path starts with our allowed root
        try:
            path.relative_to(self.experiment_root)
        except ValueError:
            raise SecurityError(
                f"🚨 Security violation: Path '{target_path}' resolves to '{path}' "
                f"which is outside experiment boundary '{self.experiment_root}'"
            )
        
        return path
    
    def secure_open(self, filepath: Union[str, Path], mode: str = 'r', **kwargs) -> Union[TextIO, BinaryIO]:
        """
        Secure file open that enforces boundary restrictions.
        
        Args:
            filepath: Path to open (will be validated)
            mode: File open mode
            **kwargs: Additional arguments passed to open()
            
        Returns:
            File handle
            
        Raises:
            SecurityError: If path violates boundary
        """
        secure_path = self.validate_path(filepath)
        return open(secure_path, mode, **kwargs)
    
    def secure_read_bytes(self, filepath: Union[str, Path]) -> bytes:
        """
        Securely read file as bytes.
        
        Args:
            filepath: Path to read
            
        Returns:
            File contents as bytes
        """
        with self.secure_open(filepath, 'rb') as f:
            return f.read()
    
    def secure_read_text(self, filepath: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        Securely read file as text.
        
        Args:
            filepath: Path to read
            encoding: Text encoding
            
        Returns:
            File contents as string
        """
        with self.secure_open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    
    def secure_write_bytes(self, filepath: Union[str, Path], content: bytes) -> None:
        """
        Securely write bytes to file.
        
        Args:
            filepath: Path to write
            content: Bytes to write
        """
        secure_path = self.validate_path(filepath)
        # Ensure parent directory exists
        secure_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(secure_path, 'wb') as f:
            f.write(content)
    
    def secure_write_text(self, filepath: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
        """
        Securely write text to file.
        
        Args:
            filepath: Path to write
            content: Text to write
            encoding: Text encoding
        """
        secure_path = self.validate_path(filepath)
        # Ensure parent directory exists
        secure_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(secure_path, 'w', encoding=encoding) as f:
            f.write(content)
    
    def secure_mkdir(self, dirpath: Union[str, Path], parents: bool = True, exist_ok: bool = True) -> Path:
        """
        Securely create directory within boundary.
        
        Args:
            dirpath: Directory path to create
            parents: Whether to create parent directories
            exist_ok: Whether to ignore if directory already exists
            
        Returns:
            Created directory path
        """
        secure_path = self.validate_path(dirpath)
        secure_path.mkdir(parents=parents, exist_ok=exist_ok)
        return secure_path
    
    def is_within_boundary(self, target_path: Union[str, Path]) -> bool:
        """
        Check if a path is within the security boundary without raising an exception.
        
        Args:
            target_path: Path to check
            
        Returns:
            True if path is within boundary, False otherwise
        """
        try:
            self.validate_path(target_path)
            return True
        except SecurityError:
            return False
    
    def get_boundary_info(self) -> dict:
        """
        Get information about the security boundary for logging/auditing.
        
        Returns:
            Dictionary with boundary information
        """
        return {
            "experiment_name": self.experiment_name,
            "experiment_root": str(self.experiment_root),
            "boundary_type": "filesystem",
            "security_level": "experiment_scoped"
        } 