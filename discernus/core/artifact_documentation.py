"""
Artifact Documentation Module

Generates comprehensive README files for experiment artifacts using CAS discovery
and LLM-powered content generation for human-readable descriptions.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .local_artifact_storage import LocalArtifactStorage
from ..gateway.llm_gateway import LLMGateway


class ArtifactDocumentationGenerator:
    """
    Generates comprehensive README files for experiment artifacts.
    
    Uses CAS discovery to find all artifacts and LLM to generate human-readable
    descriptions and navigation guides.
    """
    
    def __init__(self, storage: LocalArtifactStorage, gateway: LLMGateway):
        self.storage = storage
        self.gateway = gateway
        self.logger = logging.getLogger(__name__)
    
    def generate_artifact_readme(self, experiment_dir: Path) -> str:
        """
        Generate comprehensive README for experiment artifacts.
        
        Args:
            experiment_dir: Path to experiment directory
            
        Returns:
            Generated README content
        """
        try:
            # Discover experiment context from CAS
            run_context = self._discover_run_context()
            
            # Discover all artifacts by type
            artifacts_by_type = self._discover_artifacts_by_type()
            
            # Build artifact inventory
            artifact_inventory = self._build_artifact_inventory(artifacts_by_type)
            
            # Generate README content using LLM
            readme_content = self._generate_readme_content(
                run_context, artifact_inventory, experiment_dir
            )
            
            return readme_content
            
        except Exception as e:
            self.logger.error(f"Failed to generate artifact README: {e}")
            return self._generate_fallback_readme(experiment_dir)
    
    def _discover_run_context(self) -> Dict[str, Any]:
        """Discover experiment context from CAS."""
        try:
            run_context_artifacts = self.storage.find_artifacts_by_metadata(
                artifact_type="run_context"
            )
            
            if run_context_artifacts and len(run_context_artifacts) > 0:
                # Get the most recent run context
                run_context_artifact = run_context_artifacts[0]
                
                # Handle both dict and string formats
                if isinstance(run_context_artifact, dict):
                    artifact_hash = run_context_artifact.get('hash', run_context_artifact)
                else:
                    artifact_hash = run_context_artifact
                    
                run_context_content = self.storage.get_artifact(artifact_hash)
                
                if run_context_content:
                    return json.loads(run_context_content.decode('utf-8'))
            
            return {}
            
        except Exception as e:
            self.logger.warning(f"Could not discover run context: {e}")
            return {}
    
    def _discover_artifacts_by_type(self) -> Dict[str, List[Dict[str, Any]]]:
        """Discover all artifacts organized by type."""
        artifact_types = [
            "experiment_spec", "framework", "corpus_manifest", "corpus_document",
            "composite_analysis", "evidence_extraction", "score_extraction", 
            "marked_up_document", "statistical_analysis", "synthesis_report",
            "final_synthesis_report", "validation_report", "run_context"
        ]
        
        artifacts_by_type = {}
        
        for artifact_type in artifact_types:
            try:
                artifacts = self.storage.find_artifacts_by_metadata(
                    artifact_type=artifact_type
                )
                if artifacts:
                    artifacts_by_type[artifact_type] = artifacts
                else:
                    artifacts_by_type[artifact_type] = []
            except Exception as e:
                self.logger.warning(f"Could not discover {artifact_type} artifacts: {e}")
                artifacts_by_type[artifact_type] = []
        
        return artifacts_by_type
    
    def _build_artifact_inventory(self, artifacts_by_type: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """Build comprehensive artifact inventory with metadata."""
        inventory = {}
        
        for artifact_type, artifacts in artifacts_by_type.items():
            if not artifacts:
                continue
                
            type_inventory = []
            for artifact in artifacts:
                try:
                    # Get artifact metadata
                    if isinstance(artifact, dict):
                        artifact_hash = artifact.get('hash', artifact)
                        metadata = artifact.get('metadata', {})
                    else:
                        artifact_hash = artifact
                        metadata = {}
                    
                    # Get artifact content for description
                    content = self.storage.get_artifact(artifact_hash)
                    content_preview = ""
                    if content:
                        try:
                            # Try to decode as text for preview
                            text_content = content.decode('utf-8')
                            content_preview = text_content[:200] + "..." if len(text_content) > 200 else text_content
                        except:
                            content_preview = f"Binary content ({len(content)} bytes)"
                    
                    type_inventory.append({
                        "hash": artifact_hash,
                        "metadata": metadata,
                        "content_preview": content_preview,
                        "size": len(content) if content else 0
                    })
                    
                except Exception as e:
                    self.logger.warning(f"Could not process {artifact_type} artifact: {e}")
                    continue
            
            if type_inventory:
                inventory[artifact_type] = type_inventory
        
        return inventory
    
    def _generate_readme_content(self, run_context: Dict[str, Any], 
                               artifact_inventory: Dict[str, List[Dict[str, Any]]], 
                               experiment_dir: Path) -> str:
        """Generate README content using LLM."""
        try:
            # Build prompt for LLM
            prompt = self._build_readme_prompt(run_context, artifact_inventory, experiment_dir)
            
            # Call LLM to generate content
            content, metadata = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                temperature=0.3
            )
            
            if content:
                return content
            else:
                return self._generate_fallback_readme(experiment_dir)
                
        except Exception as e:
            self.logger.error(f"LLM README generation failed: {e}")
            return self._generate_fallback_readme(experiment_dir)
    
    def _build_readme_prompt(self, run_context: Dict[str, Any], 
                           artifact_inventory: Dict[str, List[Dict[str, Any]]], 
                           experiment_dir: Path) -> str:
        """Build comprehensive prompt for README generation."""
        
        # Experiment overview
        experiment_name = run_context.get('experiment_name', 'Unknown Experiment')
        framework_name = run_context.get('framework_name', 'Unknown Framework')
        corpus_name = run_context.get('corpus_name', 'Unknown Corpus')
        document_count = run_context.get('document_count', 0)
        run_id = run_context.get('run_id', 'Unknown Run')
        completion_date = run_context.get('completion_date', 'Unknown Date')
        
        # Build artifact summary
        artifact_summary = []
        for artifact_type, artifacts in artifact_inventory.items():
            if artifacts:
                artifact_summary.append(f"- **{artifact_type}**: {len(artifacts)} artifacts")
        
        artifact_summary_text = "\n".join(artifact_summary) if artifact_summary else "No artifacts found"
        
        prompt = f"""
Generate a comprehensive README file for a Discernus research experiment.

EXPERIMENT OVERVIEW:
- Name: {experiment_name}
- Framework: {framework_name}
- Corpus: {corpus_name}
- Documents: {document_count}
- Run ID: {run_id}
- Completion Date: {completion_date}
- Directory: {experiment_dir}

ARTIFACT INVENTORY:
{artifact_summary_text}

REQUIREMENTS:
1. Create a professional, academic-style README
2. Include clear navigation structure
3. Explain what each artifact type contains
4. Provide provenance information
5. Make it discoverable for researchers and auditors
6. Use clear, professional language
7. Include directory structure explanation
8. Add usage instructions for researchers

FORMAT:
- Use markdown formatting
- Include table of contents
- Add clear section headers
- Provide artifact descriptions
- Include navigation links
- Add provenance information

Generate a complete README that makes this experiment directory self-contained and discoverable.
"""
        
        return prompt
    
    def _generate_fallback_readme(self, experiment_dir: Path) -> str:
        """Generate basic fallback README if LLM generation fails."""
        return f"""# Discernus Research Experiment

**Directory**: {experiment_dir}
**Generated**: {datetime.now().isoformat()}

## Overview

This directory contains artifacts from a Discernus research experiment.

## Directory Structure

- `experiment/` - Experiment specification and framework files
- `source_documents/` - Original corpus documents
- `analysis/` - Analysis results and intermediate artifacts
- `results/` - Final statistical analysis and synthesis reports
- `provenance/` - Run context and metadata
- `misc/` - Additional artifacts

## Usage

This directory contains all artifacts needed to understand, reproduce, and audit this research experiment.

## Note

This README was generated automatically. For detailed artifact information, examine the individual files in each subdirectory.
"""
