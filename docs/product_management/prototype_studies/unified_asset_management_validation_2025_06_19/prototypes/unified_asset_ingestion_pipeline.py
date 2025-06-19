#!/usr/bin/env python3
"""
Unified Asset Ingestion Pipeline - Prototype Implementation
Extends corpus hash-based pattern to all asset types for unified asset management.

This prototype implements the content-addressable storage system described
in the unified asset management architecture strategy.
"""

import hashlib
import json
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum


class AssetType(Enum):
    """Supported asset types for unified management."""
    FRAMEWORK = "framework"
    PROMPT_TEMPLATE = "prompt_template"
    WEIGHTING_SCHEME = "weighting_scheme"
    EVALUATOR_CONFIG = "evaluator_config"
    EXPERIMENT = "experiment"


@dataclass
class AssetStorageResult:
    """Result of asset ingestion operation."""
    success: bool
    asset_id: Optional[str] = None
    content_hash: Optional[str] = None
    storage_path: Optional[Path] = None
    duplicate: bool = False
    existing_id: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class AssetMetadata:
    """Metadata for stored assets."""
    asset_type: AssetType
    name: str
    version: str
    content_hash: str
    storage_path: str
    development_path: str
    created_at: datetime
    format_version: str
    validation_status: str


class UnifiedAssetIngestion:
    """
    Content-addressable storage system for all asset types.
    Extends proven corpus pattern to frameworks, templates, etc.
    """
    
    def __init__(self, storage_root: str = "asset_storage", workspace_root: str = "research_workspaces"):
        self.storage_root = Path(storage_root)
        self.workspace_root = Path(workspace_root)
        
        # Create storage directories
        for asset_type in AssetType:
            (self.storage_root / asset_type.value).mkdir(parents=True, exist_ok=True)
    
    def calculate_asset_hash(self, asset_path: Path) -> str:
        """Calculate content hash for any asset type."""
        if asset_path.suffix.lower() == '.yaml':
            # For YAML files, normalize and hash content
            with open(asset_path, 'r') as f:
                content = yaml.safe_load(f)
            # Convert to canonical JSON for consistent hashing
            canonical_content = json.dumps(content, sort_keys=True, separators=(',', ':'))
            return hashlib.sha256(canonical_content.encode()).hexdigest()
        
        elif asset_path.suffix.lower() == '.json':
            # For JSON files, normalize and hash
            with open(asset_path, 'r') as f:
                content = json.load(f)
            canonical_content = json.dumps(content, sort_keys=True, separators=(',', ':'))
            return hashlib.sha256(canonical_content.encode()).hexdigest()
        
        else:
            # For other files, hash raw content
            with open(asset_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
    
    def create_hash_storage_path(self, content_hash: str, asset_type: AssetType) -> Path:
        """Create content-addressable storage path using corpus pattern."""
        hash_prefix = content_hash[:2]
        hash_middle = content_hash[2:4]
        
        storage_dir = self.storage_root / asset_type.value / hash_prefix / hash_middle / content_hash
        storage_dir.mkdir(parents=True, exist_ok=True)
        
        return storage_dir
    
    def check_existing_hash(self, content_hash: str, asset_type: AssetType) -> Optional[str]:
        """Check if asset with this hash already exists."""
        hash_prefix = content_hash[:2]
        hash_middle = content_hash[2:4]
        
        existing_path = self.storage_root / asset_type.value / hash_prefix / hash_middle / content_hash
        
        if existing_path.exists():
            # Return the content hash as asset ID for now
            return content_hash
        
        return None
    
    def ingest_framework(self, development_path: Path) -> AssetStorageResult:
        """Ingest framework from development workspace to content-addressable storage."""
        return self._ingest_asset(development_path, AssetType.FRAMEWORK)
    
    def ingest_prompt_template(self, development_path: Path) -> AssetStorageResult:
        """Ingest prompt template to content-addressable storage."""
        return self._ingest_asset(development_path, AssetType.PROMPT_TEMPLATE)
    
    def ingest_weighting_scheme(self, development_path: Path) -> AssetStorageResult:
        """Ingest weighting scheme to content-addressable storage."""
        return self._ingest_asset(development_path, AssetType.WEIGHTING_SCHEME)
    
    def _ingest_asset(self, development_path: Path, asset_type: AssetType) -> AssetStorageResult:
        """Generic asset ingestion implementation."""
        try:
            # Calculate content hash
            if development_path.is_file():
                # Single file asset
                content_hash = self.calculate_asset_hash(development_path)
                main_file = development_path
            else:
                # Directory asset - look for main file
                main_file = self._find_main_asset_file(development_path, asset_type)
                if not main_file:
                    return AssetStorageResult(
                        success=False,
                        error_message=f"No main asset file found in {development_path}"
                    )
                content_hash = self.calculate_asset_hash(main_file)
            
            # Check for existing version
            existing_id = self.check_existing_hash(content_hash, asset_type)
            if existing_id:
                return AssetStorageResult(
                    success=True,
                    duplicate=True,
                    existing_id=existing_id,
                    content_hash=content_hash
                )
            
            # Create content-addressable storage directory
            storage_dir = self.create_hash_storage_path(content_hash, asset_type)
            
            # Copy asset files to storage
            if development_path.is_file():
                # Single file - copy directly
                shutil.copy2(development_path, storage_dir / development_path.name)
            else:
                # Directory - copy all files
                for file_path in development_path.rglob('*'):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(development_path)
                        dest_path = storage_dir / rel_path
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, dest_path)
            
            # Create metadata file
            metadata = AssetMetadata(
                asset_type=asset_type,
                name=main_file.stem,
                version="auto",  # TODO: Extract from asset content
                content_hash=content_hash,
                storage_path=str(storage_dir),
                development_path=str(development_path),
                created_at=datetime.now(),
                format_version="yaml_v1.0",
                validation_status="pending"
            )
            
            metadata_path = storage_dir / ".metadata.yaml"
            with open(metadata_path, 'w') as f:
                yaml.dump(asdict(metadata), f, default_flow_style=False)
            
            # Create provenance file
            provenance = {
                "source_type": "development_workspace",
                "source_path": str(development_path),
                "ingestion_date": datetime.now().isoformat(),
                "ingestion_method": "unified_asset_pipeline",
                "content_hash": content_hash
            }
            
            provenance_path = storage_dir / ".provenance.yaml"
            with open(provenance_path, 'w') as f:
                yaml.dump(provenance, f, default_flow_style=False)
            
            return AssetStorageResult(
                success=True,
                asset_id=content_hash,
                content_hash=content_hash,
                storage_path=storage_dir
            )
            
        except Exception as e:
            return AssetStorageResult(
                success=False,
                error_message=f"Asset ingestion failed: {str(e)}"
            )
    
    def _find_main_asset_file(self, asset_dir: Path, asset_type: AssetType) -> Optional[Path]:
        """Find the main asset file in a directory."""
        if asset_type == AssetType.FRAMEWORK:
            # Look for framework.yaml
            for candidate in ["framework.yaml", "framework.json"]:
                main_file = asset_dir / candidate
                if main_file.exists():
                    return main_file
        
        elif asset_type == AssetType.PROMPT_TEMPLATE:
            # Look for template.yaml
            for candidate in ["template.yaml", "template.json"]:
                main_file = asset_dir / candidate
                if main_file.exists():
                    return main_file
        
        elif asset_type == AssetType.WEIGHTING_SCHEME:
            # Look for scheme.yaml
            for candidate in ["scheme.yaml", "scheme.json"]:
                main_file = asset_dir / candidate
                if main_file.exists():
                    return main_file
        
        return None
    
    def list_stored_assets(self, asset_type: AssetType) -> List[Dict[str, Any]]:
        """List all stored assets of given type."""
        assets = []
        asset_storage_dir = self.storage_root / asset_type.value
        
        for hash_dir in asset_storage_dir.rglob("*"):
            if hash_dir.is_dir() and len(hash_dir.name) == 64:  # Full hash length
                metadata_file = hash_dir / ".metadata.yaml"
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = yaml.safe_load(f)
                    assets.append(metadata)
        
        return assets
    
    def get_asset_by_hash(self, content_hash: str, asset_type: AssetType) -> Optional[Path]:
        """Retrieve asset path by content hash."""
        hash_prefix = content_hash[:2]
        hash_middle = content_hash[2:4]
        
        storage_path = self.storage_root / asset_type.value / hash_prefix / hash_middle / content_hash
        
        if storage_path.exists():
            return storage_path
        
        return None


def demo_asset_ingestion():
    """Demonstrate unified asset ingestion pipeline."""
    print("🚀 Unified Asset Ingestion Pipeline Demo")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = UnifiedAssetIngestion()
    
    # Ingest frameworks
    workspace_path = Path("research_workspaces/june_2025_research_dev_workspace")
    
    if workspace_path.exists():
        print("\n📁 Ingesting Frameworks...")
        
        for framework_dir in (workspace_path / "frameworks").iterdir():
            if framework_dir.is_dir():
                print(f"  Processing: {framework_dir.name}")
                result = pipeline.ingest_framework(framework_dir)
                
                if result.success:
                    if result.duplicate:
                        print(f"    ✅ Already exists: {result.existing_id[:8]}...")
                    else:
                        print(f"    ✅ Stored: {result.content_hash[:8]}...")
                        print(f"    📍 Path: {result.storage_path}")
                else:
                    print(f"    ❌ Failed: {result.error_message}")
        
        print("\n📝 Ingesting Prompt Templates...")
        
        templates_dir = workspace_path / "prompt_templates"
        if templates_dir.exists():
            for template_dir in templates_dir.iterdir():
                if template_dir.is_dir():
                    print(f"  Processing: {template_dir.name}")
                    result = pipeline.ingest_prompt_template(template_dir)
                    
                    if result.success:
                        if result.duplicate:
                            print(f"    ✅ Already exists: {result.existing_id[:8]}...")
                        else:
                            print(f"    ✅ Stored: {result.content_hash[:8]}...")
                    else:
                        print(f"    ❌ Failed: {result.error_message}")
    
    # List stored assets
    print("\n📊 Stored Assets Summary:")
    for asset_type in AssetType:
        assets = pipeline.list_stored_assets(asset_type)
        print(f"  {asset_type.value}: {len(assets)} assets")
        for asset in assets:
            print(f"    - {asset.get('name', 'unknown')} [{asset.get('content_hash', '')[:8]}...]")


if __name__ == "__main__":
    demo_asset_ingestion() 