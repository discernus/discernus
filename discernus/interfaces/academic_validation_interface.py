#!/usr/bin/env python3
"""
Academic Validation Interface - THIN Implementation

Simple interface for researchers to validate scores in <5 minutes.
Provides framework-agnostic score validation workflow.
"""

import json
import click
from pathlib import Path
from typing import Optional

from discernus.orchestration.score_validation_orchestrator import (
    ScoreValidationOrchestrator, 
    ScoreValidationRequest
)


def validate_score_impl(experiment_path: str, document_name: str, score_name: str, 
                       score_value: float, confidence: float, framework: Optional[str], 
                       output: Optional[str], model: str) -> int:
    """
    Validate a numerical score using THIN academic validation pipeline.
    
    Provides <5 minute academic validation workflow for any numerical score.
    """
    experiment_path = Path(experiment_path)
    
    # Auto-detect framework if not specified
    if not framework:
        framework = _detect_framework(experiment_path)
    
    # Find analysis artifact
    analysis_artifact_path = _find_analysis_artifact(experiment_path, document_name)
    if not analysis_artifact_path:
        click.echo(f"❌ Analysis artifact not found for document: {document_name}")
        return 1
    
    # Find corpus manifest
    corpus_manifest_path = experiment_path / "corpus" / "corpus.md"
    if not corpus_manifest_path.exists():
        click.echo(f"❌ Corpus manifest not found: {corpus_manifest_path}")
        return 1
    
    # Auto-detect model from analysis artifact
    analysis_model = _detect_analysis_model(analysis_artifact_path)
    if not analysis_model:
        analysis_model = model  # Fallback to specified model
    
    # Create validation request
    request = ScoreValidationRequest(
        document_name=document_name,
        score_name=score_name,
        score_value=score_value,
        confidence=confidence,
        framework_name=framework,
        analysis_artifact_path=str(analysis_artifact_path),
        corpus_manifest_path=str(corpus_manifest_path)
    )
    
    # Run validation
    click.echo(f"🔍 Validating score: {score_name} = {score_value} from {document_name}")
    click.echo(f"📄 Framework: {framework}")
    click.echo(f"🤖 Model: {analysis_model or model}")
    click.echo(f"⏱️  Target: <5 minutes")
    
    orchestrator = ScoreValidationOrchestrator(model=analysis_model or model)
    result = orchestrator.validate_score(request)
    
    if result.success:
        click.echo(f"✅ Validation completed in {result.validation_time_seconds:.1f} seconds")
        
        # Generate and display report
        report = orchestrator.generate_validation_report(result, request)
        
        if output:
            with open(output, 'w') as f:
                f.write(report)
            click.echo(f"📄 Report saved to: {output}")
        else:
            click.echo("\n" + "="*60)
            click.echo(report)
            click.echo("="*60)
        
        # Performance check
        if result.validation_time_seconds > 300:  # 5 minutes
            click.echo(f"⚠️  Validation took {result.validation_time_seconds:.1f}s (target: <300s)")
        else:
            click.echo(f"🎯 Performance target met: {result.validation_time_seconds:.1f}s")
            
    else:
        click.echo(f"❌ Validation failed: {result.error_message}")
        return 1
    
    return 0


@click.command()
@click.argument('experiment_path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('document_name', type=str)
@click.argument('score_name', type=str)
@click.option('--score-value', type=float, required=True, help='Numerical score value to validate')
@click.option('--confidence', type=float, default=0.8, help='Confidence level (0.0-1.0)')
@click.option('--framework', type=str, help='Framework name (auto-detected if not specified)')
@click.option('--output', type=click.Path(), help='Output file for validation report')
@click.option('--model', default='vertex_ai/gemini-2.5-flash-lite', help='LLM model for validation')
def validate_score(experiment_path: str, document_name: str, score_name: str, 
                  score_value: float, confidence: float, framework: Optional[str], 
                  output: Optional[str], model: str):
    """Validate a numerical score using THIN academic validation pipeline (<5 minutes)."""
    import sys
    sys.exit(validate_score_impl(experiment_path, document_name, score_name, 
                                score_value, confidence, framework, output, model))


def _detect_framework(experiment_path: Path) -> str:
    """Auto-detect framework from experiment configuration."""
    experiment_file = experiment_path / "experiment.md"
    if experiment_file.exists():
        with open(experiment_file, 'r') as f:
            content = f.read()
            
        # Extract framework from YAML frontmatter
        if content.startswith('---'):
            import yaml
            parts = content.split('---', 2)
            if len(parts) >= 3:
                config = yaml.safe_load(parts[1])
                framework = config.get('framework', 'unknown')
                
                # Extract framework name from path
                if framework.startswith('../../frameworks/'):
                    framework_name = Path(framework).stem
                    return framework_name
                else:
                    return framework
    
    return "unknown_framework"


def _find_analysis_artifact(experiment_path: Path, document_name: str) -> Optional[Path]:
    """Find analysis artifact for document."""
    # Look in runs directory for most recent run
    runs_dir = experiment_path / "runs"
    if not runs_dir.exists():
        return None
    
    # Find most recent run
    run_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
    if not run_dirs:
        return None
    
    latest_run = max(run_dirs, key=lambda d: d.name)
    
    # Look for analysis artifacts
    artifacts_dir = latest_run / "artifacts" / "analysis_results"
    if artifacts_dir.exists():
        # Look for artifact containing document name
        for artifact_file in artifacts_dir.glob("*.json"):
            try:
                # Extract filename and use direct shared_cache path
                filename = artifact_file.name
                actual_file = experiment_path / "shared_cache" / "artifacts" / filename
                with open(actual_file, 'r') as f:
                    data = json.load(f)
                    
                    # Check if this is a multi-document analysis response
                    if 'document_analyses' in data:
                        for doc_analysis in data['document_analyses']:
                            if doc_analysis.get('document_name') == document_name:
                                return artifact_file
                    # Check single document format
                    elif 'document_name' in data and data['document_name'] == document_name:
                        return artifact_file
                    elif 'analysis_scores' in data:
                        # Check if any analysis contains this document
                        for analysis in data['analysis_scores']:
                            if analysis.get('document_name') == document_name:
                                return artifact_file
            except Exception as e:
                print(f"Error reading {artifact_file}: {e}")
                continue
    
    return None


def _detect_analysis_model(analysis_artifact_path: Path) -> Optional[str]:
    """Auto-detect the model used in the analysis."""
    try:
        # Extract filename and use direct shared_cache path
        filename = analysis_artifact_path.name
        experiment_path = analysis_artifact_path.parent.parent.parent.parent
        actual_file = experiment_path / "shared_cache" / "artifacts" / filename
        
        if not actual_file.exists():
            return None
        
        with open(actual_file, 'r') as f:
            data = json.load(f)
        
        # Extract model from analysis metadata
        if 'analysis_metadata' in data:
            return data['analysis_metadata'].get('model_used')
        
        # Check document analyses for model info
        if 'document_analyses' in data:
            for doc_analysis in data['document_analyses']:
                if 'extraction_metadata' in doc_analysis:
                    return doc_analysis['extraction_metadata'].get('model_used')
        
        return None
        
    except Exception as e:
        print(f"Warning: Could not detect analysis model: {e}")
        return None


if __name__ == "__main__":
    validate_score() 