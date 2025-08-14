#!/usr/bin/env python3
"""
Discernus v8.0 Specification Loading System
===========================================

THIN-compliant, raw content loader for v8.0 specifications.
This module is intentionally simple. It performs no parsing or validation.
Its sole responsibility is to read the raw content of specification files.
All semantic understanding is delegated to the LLM agents.
"""

import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class V8ExperimentSpec:
    """A container for the raw content of a v8.0 experiment."""
    name: str
    description: str
    framework_path: Path
    corpus_path: Path
    raw_content: Dict[str, Any]
    questions: Optional[List[str]] = None

class V8SpecificationLoader:
    """
    Loads the raw content of v8.0 specifications without parsing their semantics.
    """
    def __init__(self, experiment_dir: Path):
        self.experiment_dir = experiment_dir.resolve()

    def load_experiment(self, experiment_file: str = "experiment_v8.md") -> V8ExperimentSpec:
        """
        Loads the v8.0 experiment file and returns its raw content.
        This method validates file existence but not content.
        """
        exp_path = self.experiment_dir / experiment_file
        if not exp_path.is_file():
            raise FileNotFoundError(f"Experiment file not found: {exp_path}")

        try:
            with open(exp_path, 'r') as f:
                content = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in experiment file: {exp_path}") from e

        # Basic structural check
        required_keys = ["name", "description", "framework", "corpus"]
        if not all(key in content for key in required_keys):
            raise ValueError(f"Experiment file is missing one or more required keys: {required_keys}")

        # Resolve framework and corpus paths relative to project root for canonical paths
        framework_path = Path(content["framework"])
        corpus_path = Path(content["corpus"])
        
        # If paths start with "frameworks/" or "corpus/", they're canonical paths relative to project root
        if str(framework_path).startswith("frameworks/"):
            # Find project root by walking up from experiment directory
            project_root = self.experiment_dir
            while project_root != project_root.parent:
                if (project_root / "frameworks").exists():
                    break
                project_root = project_root.parent
            framework_path = project_root / framework_path
        else:
            framework_path = self.experiment_dir / framework_path
            
        if str(corpus_path).startswith("corpus/"):
            corpus_path = self.experiment_dir / corpus_path
        else:
            corpus_path = self.experiment_dir / corpus_path
        
        return V8ExperimentSpec(
            name=content["name"],
            description=content["description"],
            framework_path=framework_path,
            corpus_path=corpus_path,
            raw_content=content,
            questions=content.get("questions")
        )

    def load_raw_framework(self, framework_path: Path) -> str:
        """Loads the raw markdown content of a framework file."""
        if not framework_path.is_file():
            raise FileNotFoundError(f"Framework file not found: {framework_path}")
        with open(framework_path, 'r') as f:
            return f.read()

    def load_raw_corpus(self, corpus_path: Path) -> str:
        """Loads the raw markdown content of a corpus file."""
        if not corpus_path.is_file():
            # Fallback to checking for corpus.md in a directory
            corpus_dir_path = corpus_path
            corpus_file_path = corpus_dir_path / "corpus_v8.md"
            if not corpus_file_path.is_file():
                 raise FileNotFoundError(f"Corpus file not found in: {corpus_dir_path}")
        else:
            corpus_file_path = corpus_path
            
        with open(corpus_file_path, 'r') as f:
            return f.read()
