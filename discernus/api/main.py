from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import uuid
import yaml  # For loading the experiment file
from typing import Dict, Any, Tuple, List, Optional
# Removed unused imports: AsyncResult, os
import asyncio
from pathlib import Path
from sqlalchemy.orm import Session
import numpy as np
import webbrowser
import threading

from discernus.gateway.llm_gateway import get_llm_analysis
from discernus.engine.signature_engine import (
    calculate_coordinates,
    _extract_anchors_from_framework,
    calculate_distance,
)
from discernus.reporting.report_builder import ReportBuilder
from scripts.tasks import analyze_text_task
from discernus.database.session import get_db
from discernus.database.models import AnalysisJob, AnalysisResult, JobStatus, AnalysisJobV2, AnalysisResultV2, StatisticalComparison
from discernus.analysis.statistical_methods import StatisticalMethodRegistry


class AnalysisRequest(BaseModel):
    text: Optional[str] = None  # Optional - will use experiment's default_text if not provided
    experiment: str = "mft_experiment"  # Just the experiment name, no file paths


class FinalResponse(BaseModel):
    x: float
    y: float
    framework_id: str
    model: str
    report_url: Optional[str] = None


class ComparisonRequest(BaseModel):
    text_a: str
    text_b: str
    label_a: str = "Text A"
    label_b: str = "Text B"
    experiment_file_path: str = "discernus/experiments/reboot_mft_experiment.yaml"
    model: str = "gpt-4o"


class ComparisonResponse(BaseModel):
    report_url: str
    text_a_centroid: Tuple[float, float]
    text_b_centroid: Tuple[float, float]
    distance: float


class CorpusAnalysisRequest(BaseModel):
    file_paths: List[str]
    experiment_file_path: str = "discernus/experiments/reboot_mft_experiment.yaml"
    model: str = "gpt-4o"


class JobResponse(BaseModel):
    job_id: str


class ResultResponse(BaseModel):
    job_id: str
    status: str
    results: Any | None = None


class GroupComparisonRequest(BaseModel):
    job_id_a: str
    label_a: str
    job_id_b: str
    label_b: str
    experiment_file_path: str = "discernus/experiments/reboot_mft_experiment.yaml"


class GroupComparisonResponse(BaseModel):
    report_url: str
    group_a_centroid: Tuple[float, float]
    group_b_centroid: Tuple[float, float]
    distance: float


class DirectGroupComparisonRequest(BaseModel):
    group1: Dict[str, Any]
    group2: Dict[str, Any]
    framework_id: str = "moral_foundations_theory"
    experiment_file_path: str = "discernus/experiments/reboot_mft_experiment.yaml"
    model: str = "gpt-4o"


class StatisticalComparisonRequest(BaseModel):
    comparison_type: str
    text: Optional[str] = None
    models: Optional[List[str]] = None
    frameworks: Optional[List[str]] = None
    runs_per_condition: Optional[int] = 1
    experiment_file_path: str = "discernus/experiments/reboot_mft_experiment.yaml"
    statistical_methods: List[str] = ["geometric_similarity", "dimensional_correlation"]


class ConditionResult(BaseModel):
    condition_identifier: str
    centroid: Tuple[float, float]
    raw_scores: Dict[str, float]


class StatisticalComparisonResponse(BaseModel):
    job_id: str
    comparison_type: str
    similarity_classification: str = "PENDING_ANALYSIS"
    confidence_level: float = 0.0
    condition_results: List[ConditionResult] = []
    statistical_metrics: Dict[str, Any] = {}
    significance_tests: Dict[str, Any] = {}
    report_url: Optional[str] = None


app = FastAPI()

# Mount a directory to serve the static report files
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# No longer need a global framework loader, it will be loaded per request.
report_builder = ReportBuilder(output_dir="reports/reboot_mvp")  # Keep reports organized
TEMP_RESULTS_DIR = Path("temp_results")
TEMP_RESULTS_DIR.mkdir(exist_ok=True)


async def _run_single_analysis(text: str, model: str, experiment_def: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to run the full analysis pipeline for a single text."""
    # Step 1: Get the analysis from the LLM Gateway (already parsed by robust parser)
    llm_result = await get_llm_analysis(text=text, experiment_def=experiment_def, model=model)
    if llm_result.get("error"):
        raise HTTPException(status_code=500, detail=f"LLM Error: {llm_result.get('error')}")

    # Step 2: Extract scores (already parsed by LiteLLMClient's robust parser)
    scores = llm_result.get("scores", {})
    if not scores:
        raise HTTPException(status_code=500, detail="No scores returned from LLM analysis")

    # Step 3: Calculate the centroid using the Signature Engine
    x, y = calculate_coordinates(experiment_def, scores)

    return {"scores": scores, "centroid": (x, y)}


def _load_experiment(experiment_name: str) -> Dict[str, Any]:
    """Load experiment definition by name from the experiments directory."""
    experiment_file = f"discernus/experiments/{experiment_name}.yaml"
    try:
        with open(experiment_file, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not load experiment '{experiment_name}': {e}")

@app.post("/analyze", response_model=FinalResponse)
async def analyze_text(request: AnalysisRequest):
    """
    This endpoint orchestrates a single-text analysis using a completely self-contained experiment.
    Everything (model, corpus, framework, and optionally text) comes from the experiment YAML.
    """
    run_id = str(uuid.uuid4())
    try:
        # Step 1: Load the self-contained experiment definition
        experiment_def = _load_experiment(request.experiment)
        
        # Step 2: Get model from experiment definition
        models_config = experiment_def.get("models", {})
        model = models_config.get("default_model", "gpt-4o")
        
        # Step 3: Get text - use provided text or fall back to experiment's default_text
        text_to_analyze = request.text
        if not text_to_analyze:
            corpus_config = experiment_def.get("corpus", {})
            text_to_analyze = corpus_config.get("default_text")
            if not text_to_analyze:
                raise HTTPException(status_code=400, detail="No text provided and experiment has no default_text")
        
        # Step 4: Run the analysis
        analysis_result = await _run_single_analysis(text_to_analyze, model, experiment_def)

        # Step 5: Generate the visual report (only if enabled)
        output_config = experiment_def.get("output", {})
        report_path = None
        if output_config.get("generate_visualization", True):
            anchors = _extract_anchors_from_framework(experiment_def)
            report_path = report_builder.generate_report(
                anchors=anchors, scores=analysis_result["scores"], coordinates=analysis_result["centroid"], run_id=run_id
            )

        # Step 6: Auto-launch browser to show results (only if report was generated)
        if report_path:
            def open_browser():
                # Give the response time to complete, then open browser
                import time
                time.sleep(1)  # Small delay to ensure response is sent
                full_url = f"http://127.0.0.1:8000/{report_path}"
                webbrowser.open(full_url)
                print(f"🌐 Opened browser: {full_url}")
            
            # Launch browser in background thread so API response isn't delayed
            threading.Thread(target=open_browser, daemon=True).start()
        
        # Step 7: Return the final response
        return FinalResponse(
            x=analysis_result["centroid"][0],
            y=analysis_result["centroid"][1],
            framework_id=experiment_def.get("framework", {}).get("name"),
            model=model,
            report_url=f"/{report_path}" if report_path else None,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare", response_model=ComparisonResponse)
async def compare_texts(request: ComparisonRequest):
    """
    This endpoint orchestrates a two-text comparison analysis and returns
    their centroids and a URL to a visual comparison report.
    """
    run_id = str(uuid.uuid4())
    try:
        # Step 1: Load the self-contained experiment definition
        try:
            with open(request.experiment_file_path, "r") as f:
                experiment_def = yaml.safe_load(f)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Could not load experiment file: {e}")

        # Step 2: Run independent analyses for both texts
        analysis_a = await _run_single_analysis(request.text_a, request.model, experiment_def)
        analysis_b = await _run_single_analysis(request.text_b, request.model, experiment_def)

        # Step 3: Calculate the distance between the centroids
        distance = calculate_distance(analysis_a["centroid"], analysis_b["centroid"])

        # Step 4: Generate the comparison visual report
        anchors = _extract_anchors_from_framework(experiment_def)
        report_path = report_builder.generate_comparison_report(
            anchors=anchors,
            analysis_a=analysis_a,
            label_a=request.label_a,
            analysis_b=analysis_b,
            label_b=request.label_b,
            run_id=run_id,
            distance=distance,
        )

        return ComparisonResponse(
            report_url=f"/{report_path}",
            text_a_centroid=analysis_a["centroid"],
            text_b_centroid=analysis_b["centroid"],
            distance=distance,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-corpus", response_model=JobResponse)
async def analyze_corpus(request: CorpusAnalysisRequest, db: Session = Depends(get_db)):
    """
    Submits a batch of texts for analysis.
    """
    new_job = AnalysisJob()
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    job_id = new_job.id

    try:
        with open(request.experiment_file_path, "r") as f:
            experiment_def = yaml.safe_load(f)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not load experiment file: {e}")

    task_count = 0
    for i, file_path in enumerate(request.file_paths):
        try:
            with open(file_path, "r") as f:
                text = f.read()

            analyze_text_task.delay(text=text, experiment_def=experiment_def, model=request.model, job_id=job_id)
            task_count += 1
        except Exception as e:
            # Log this error but continue
            print(f"Failed to process file {file_path}: {e}")

    if task_count == 0:
        new_job.status = JobStatus.FAILED
        db.commit()
        raise HTTPException(status_code=400, detail="No valid files were submitted for analysis.")

    return JobResponse(job_id=job_id)


@app.get("/results/{job_id}", response_model=ResultResponse)
async def get_results(job_id: str, db: Session = Depends(get_db)):
    """Retrieves the status and results of a job."""
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # A simple approach to check completion: if the number of results
    # matches the number of tasks we intended to run.
    # A more robust system might have a total_tasks count in the AnalysisJob model.
    # For now, we assume if there are results, it's 'COMPLETE' for simplicity.
    # This logic can be enhanced.

    results = db.query(AnalysisResult).filter(AnalysisResult.job_id == job_id).all()

    # Check if all tasks for the job are complete
    # A more robust implementation would store the expected task count in the job model
    # For now, if there are no results, we assume it's pending.
    # We could also add a check to see if any tasks have failed.
    if job.status == JobStatus.PENDING and results:
        # This is a simplification. A real system would have a more robust
        # way to track job completion. We could, for example, have the
        # worker update the job status.
        job.status = JobStatus.COMPLETE
        db.commit()

    return ResultResponse(
        job_id=job_id,
        status=job.status.value,
        results=[{"centroid": (r.centroid_x, r.centroid_y), "scores": json.loads(r.scores)} for r in results],
    )


@app.post("/compare-groups", response_model=GroupComparisonResponse)
async def compare_groups(request: GroupComparisonRequest, db: Session = Depends(get_db)):
    """
    Compares two groups of analysis results and generates a report.
    """
    run_id = str(uuid.uuid4())
    try:
        results_a = db.query(AnalysisResult).filter(AnalysisResult.job_id == request.job_id_a).all()
        results_b = db.query(AnalysisResult).filter(AnalysisResult.job_id == request.job_id_b).all()

        if not results_a or not results_b:
            raise HTTPException(status_code=400, detail="One or both jobs have no results yet or jobs not found.")

        # Convert SQLAlchemy objects to the dictionary format expected by the report builder
        signatures_a = [{"centroid": (r.centroid_x, r.centroid_y), "scores": json.loads(r.scores)} for r in results_a]
        signatures_b = [{"centroid": (r.centroid_x, r.centroid_y), "scores": json.loads(r.scores)} for r in results_b]

        with open(request.experiment_file_path, "r") as f:
            experiment_def = yaml.safe_load(f)
        anchors = _extract_anchors_from_framework(experiment_def)

        def _calculate_centroid(signatures):
            if not signatures:
                return (0.0, 0.0)
            coords = [s["centroid"] for s in signatures if "centroid" in s]
            if not coords:
                return (0.0, 0.0)
            avg_x = sum(c[0] for c in coords) / len(coords)
            avg_y = sum(c[1] for c in coords) / len(coords)
            return (avg_x, avg_y)

        centroid_a = _calculate_centroid(signatures_a)
        centroid_b = _calculate_centroid(signatures_b)

        distance = calculate_distance(centroid_a, centroid_b)

        report_path = report_builder.generate_group_comparison_report(
            anchors=anchors,
            group_a_signatures=signatures_a,
            label_a=request.label_a,
            group_b_signatures=signatures_b,
            label_b=request.label_b,
            run_id=run_id,
            distance=distance,
        )

        return GroupComparisonResponse(
            report_url=f"/{report_path}",
            group_a_centroid=centroid_a,
            group_b_centroid=centroid_b,
            distance=distance,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare-groups-direct", response_model=GroupComparisonResponse)
async def compare_groups_direct(request: DirectGroupComparisonRequest):
    """
    Compares two groups of texts directly without requiring separate job submissions.
    This version runs all analyses in parallel for better performance.
    """
    run_id = str(uuid.uuid4())
    try:
        # Load experiment definition
        with open(request.experiment_file_path, "r") as f:
            experiment_def = yaml.safe_load(f)

        # Create a list of all analysis tasks to run in parallel
        group1_texts = request.group1.get("texts", [])
        group2_texts = request.group2.get("texts", [])

        tasks = []
        for text in group1_texts:
            tasks.append(_run_single_analysis(text, request.model, experiment_def))
        for text in group2_texts:
            tasks.append(_run_single_analysis(text, request.model, experiment_def))

        # Run all analysis tasks concurrently
        all_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Check for errors from the gathered tasks
        for result in all_results:
            if isinstance(result, Exception):
                # Propagate the first exception found
                raise result

        # Separate the results back into their original groups
        group1_analyses = all_results[: len(group1_texts)]
        group2_analyses = all_results[len(group1_texts) :]

        # Format results for reporting
        group1_results = [{"text": t, **a} for t, a in zip(group1_texts, group1_analyses)]
        group2_results = [{"text": t, **a} for t, a in zip(group2_texts, group2_analyses)]

        def _calculate_centroid(signatures):
            if not signatures:
                return (0.0, 0.0)
            coords = [s["centroid"] for s in signatures if "centroid" in s]
            if not coords:
                return (0.0, 0.0)
            avg_x = sum(c[0] for c in coords) / len(coords)
            avg_y = sum(c[1] for c in coords) / len(coords)
            return (avg_x, avg_y)

        centroid_a = _calculate_centroid(group1_results)
        centroid_b = _calculate_centroid(group2_results)

        distance = calculate_distance(centroid_a, centroid_b)

        # Generate comparison report
        anchors = _extract_anchors_from_framework(experiment_def)
        report_path = report_builder.generate_group_comparison_report(
            anchors=anchors,
            group_a_signatures=group1_results,
            label_a=request.group1.get("name", "Group 1"),
            group_b_signatures=group2_results,
            label_b=request.group2.get("name", "Group 2"),
            run_id=run_id,
            distance=distance,
        )

        return GroupComparisonResponse(
            report_url=f"/{report_path}", group_a_centroid=centroid_a, group_b_centroid=centroid_b, distance=distance
        )
    except Exception as e:
        # This will now catch exceptions from asyncio.gather as well
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare-statistical", response_model=StatisticalComparisonResponse)
async def compare_statistical(request: StatisticalComparisonRequest, db: Session = Depends(get_db)):
    """
    Generic statistical comparison endpoint.
    Handles: multi-model, multi-framework, multi-run, corpus-based analysis
    """
    job_id = str(uuid.uuid4())
    
    # Create the AnalysisJobV2 record first
    analysis_job = AnalysisJobV2(
        id=job_id,
        job_type=request.comparison_type,
        configuration=json.dumps(request.model_dump()),
        status="PENDING"
    )
    db.add(analysis_job)
    db.commit()
    db.refresh(analysis_job)
    
    try:
        with open(request.experiment_file_path, "r") as f:
            experiment_def = yaml.safe_load(f)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not load experiment file: {e}")

    if request.comparison_type == "multi_model":
        # Check if this is corpus-based or single-text analysis
        corpus_config = experiment_def.get("corpus")
        
        if corpus_config and corpus_config.get("source_type") == "directory_collection":
            # Corpus-based multi-model analysis
            return await _handle_corpus_based_analysis(request, experiment_def, analysis_job, db, job_id)
        else:
            # Single-text multi-model analysis (existing logic)
            return await _handle_single_text_analysis(request, experiment_def, analysis_job, db, job_id)
    else:
        raise HTTPException(status_code=400, detail=f"Comparison type '{request.comparison_type}' not yet supported.")


async def _handle_corpus_based_analysis(
    request: StatisticalComparisonRequest, 
    experiment_def: Dict[str, Any], 
    analysis_job: AnalysisJobV2, 
    db: Session, 
    job_id: str
) -> StatisticalComparisonResponse:
    """Handle corpus-based multi-model statistical comparison"""
    
    corpus_config = experiment_def["corpus"]
    models_config = experiment_def.get("models", {})
    
    # Load corpus texts
    corpus_texts = await _load_corpus_texts(corpus_config)
    if not corpus_texts:
        raise HTTPException(status_code=400, detail="No texts found in corpus")
    
    # Get models to compare
    models_to_compare = _get_models_for_comparison(models_config, request.models)
    if len(models_to_compare) < 2:
        raise HTTPException(status_code=400, detail="At least 2 models required for comparison")
    
    # SEQUENTIAL PROCESSING: Process models one at a time to avoid TPM limits
    # Each model will only use ~19,500 TPM instead of combined 58,500 TPM
    analysis_results = []
    db_results_to_save = []
    
    print(f"🔄 Processing {len(models_to_compare)} models sequentially to avoid TPM limits...")
    
    for model_idx, model in enumerate(models_to_compare):
        print(f"📊 Processing model {model_idx + 1}/{len(models_to_compare)}: {model}")
        
        # Process all texts for this model concurrently (within single model TPM limit)
        model_tasks = []
        for text_info in corpus_texts:
            task = _run_single_analysis(text_info["content"], model, experiment_def)
            model_tasks.append((task, text_info["text_id"], model))
        
        # Execute all texts for this model concurrently
        for (task, text_id, model_name) in model_tasks:
            try:
                result = await task
                
                # Save to database
                db_result = AnalysisResultV2(
                    job_id=job_id,
                    text_content=text_id,  # Store text_id instead of full content
                    text_identifier=text_id,
                    model=model_name,
                    framework=experiment_def.get("framework", {}).get("name", "unknown"),
                    prompt_template=experiment_def.get("prompt_template", "unknown"),
                    centroid_x=result["centroid"][0],
                    centroid_y=result["centroid"][1],
                    raw_scores=json.dumps(result["scores"])
                )
                db_results_to_save.append(db_result)
                
                analysis_results.append({
                    "text_id": text_id,
                    "model": model_name,
                    "centroid": result["centroid"],
                    "scores": result["scores"]
                })
                
            except Exception as e:
                print(f"❌ Error analyzing {text_id} with {model_name}: {e}")
                continue
        
        print(f"✅ Completed model {model} ({model_idx + 1}/{len(models_to_compare)})")
    
    print(f"✨ Sequential processing complete! Analyzed {len(analysis_results)} text-model combinations")
    
    # Save all results to database
    db.add_all(db_results_to_save)
    db.commit()
    
    # Perform statistical analysis
    registry = StatisticalMethodRegistry()
    statistical_methods = experiment_def.get("statistical_analysis", {}).get("primary_methods", {})
    
    final_statistical_metrics = {}
    
    # Group results by model for statistical comparison
    model_groups = {}
    for result in analysis_results:
        model = result["model"]
        if model not in model_groups:
            model_groups[model] = []
        model_groups[model].append(result)
    
    # Calculate statistical metrics
    for method_name, method_config in statistical_methods.items():
        if method_config.get("enabled", False):
            try:
                if method_name == "geometric_similarity":
                    final_statistical_metrics[method_name] = _calculate_corpus_geometric_similarity(model_groups)
                elif method_name == "dimensional_correlation":
                    final_statistical_metrics[method_name] = _calculate_corpus_dimensional_correlation(model_groups)
                elif method_name == "hypothesis_testing":
                    final_statistical_metrics[method_name] = _perform_hypothesis_testing(model_groups)
                elif method_name == "effect_size_analysis":
                    final_statistical_metrics[method_name] = _calculate_effect_sizes(model_groups)
                elif method_name == "confidence_intervals":
                    final_statistical_metrics[method_name] = _calculate_confidence_intervals(model_groups)
            except Exception as e:
                final_statistical_metrics[method_name] = {"error": str(e)}
    
    # Generate overall similarity classification
    similarity_classification = _classify_corpus_similarity(final_statistical_metrics, experiment_def)
    
    # Create condition results (model averages)
    condition_results_api = []
    for model, results in model_groups.items():
        avg_centroid = _calculate_average_centroid([r["centroid"] for r in results])
        avg_scores = _calculate_average_scores([r["scores"] for r in results])
        
        condition_results_api.append(ConditionResult(
            condition_identifier=model,
            centroid=avg_centroid,
            raw_scores=avg_scores
        ))
    
    # Generate the visual report using the enhanced template with real data
    anchors = _extract_anchors_from_framework(experiment_def)
    run_id = str(uuid.uuid4())
    
    # Convert model_groups to condition_results format for enhanced template
    condition_results_for_report = []
    for model, results in model_groups.items():
        avg_centroid = _calculate_average_centroid([r["centroid"] for r in results])
        avg_scores = _calculate_average_scores([r["scores"] for r in results])
        
        condition_results_for_report.append({
            "condition_identifier": model,
            "centroid": avg_centroid,
            "raw_scores": avg_scores
        })
    
    report_path = report_builder.generate_statistical_comparison_report(
        anchors=anchors,
        condition_results=condition_results_for_report,
        statistical_metrics=final_statistical_metrics,
        comparison_type=request.comparison_type,
        job_id=job_id,
        run_id=run_id,
    )
    
    # Save statistical comparison to database
    statistical_comparison = StatisticalComparison(
        id=str(uuid.uuid4()),
        comparison_type=request.comparison_type,
        source_job_ids=[job_id],
        comparison_dimension="model",
        similarity_metrics=json.dumps(final_statistical_metrics, default=str),
        significance_tests=json.dumps(final_statistical_metrics.get("hypothesis_testing", {}), default=str),
        similarity_classification=similarity_classification,
        confidence_level=final_statistical_metrics.get("confidence_intervals", {}).get("overall_confidence", 0.0)
    )
    db.add(statistical_comparison)
    db.commit()

    # Update job status to complete
    analysis_job.status = "COMPLETE"
    db.commit()

    return StatisticalComparisonResponse(
        job_id=job_id,
        comparison_type=request.comparison_type,
        similarity_classification=similarity_classification,
        condition_results=condition_results_api,
        statistical_metrics=final_statistical_metrics,
        report_url=f"/{report_path}"
    )


async def _handle_single_text_analysis(
    request: StatisticalComparisonRequest, 
    experiment_def: Dict[str, Any], 
    analysis_job: AnalysisJobV2, 
    db: Session, 
    job_id: str
) -> StatisticalComparisonResponse:
    """Handle single-text multi-model analysis (existing logic)"""
    
    if not request.text or not request.models or len(request.models) < 2:
        raise HTTPException(status_code=400, detail="Multi-model comparison requires 'text' and at least two 'models'.")

    tasks = [_run_single_analysis(request.text, model, experiment_def) for model in request.models]
    analysis_results = await asyncio.gather(*tasks, return_exceptions=True)

    condition_results_api = []
    db_results_to_save = []
    for i, res in enumerate(analysis_results):
        model_name = request.models[i]
        if isinstance(res, Exception):
            raise HTTPException(status_code=500, detail=f"Error analyzing model {model_name}: {res}")
        
        db_result = AnalysisResultV2(
            job_id=job_id,
            text_content=request.text,
            model=model_name,
            framework=experiment_def.get("framework", {}).get("name", "unknown"),
            prompt_template=experiment_def.get("prompt_template", "unknown"),
            centroid_x=res["centroid"][0],
            centroid_y=res["centroid"][1],
            raw_scores=json.dumps(res["scores"])
        )
        db_results_to_save.append(db_result)
        
        condition_results_api.append(ConditionResult(
            condition_identifier=model_name,
            centroid=res["centroid"],
            raw_scores=res["scores"]
        ))
    
    db.add_all(db_results_to_save)
    db.commit()

    registry = StatisticalMethodRegistry()
    final_statistical_metrics = {}
    for method in request.statistical_methods:
        try:
            final_statistical_metrics[method] = registry.analyze(method, db_results_to_save)
        except Exception as e:
            final_statistical_metrics[method] = {"error": str(e)}

    # Generate the visual report (only if enabled in experiment config)
    output_config = experiment_def.get("output", {})
    report_path = None
    if output_config.get("generate_visualization", True):
        anchors = _extract_anchors_from_framework(experiment_def)
        run_id = str(uuid.uuid4())
        
        # Convert condition results to dict format for report generation
        condition_results_for_report = [
            {
                "condition_identifier": cr.condition_identifier,
                "centroid": cr.centroid,
                "raw_scores": cr.raw_scores
            }
            for cr in condition_results_api
        ]
        
        report_path = report_builder.generate_statistical_comparison_report(
            anchors=anchors,
            condition_results=condition_results_for_report,
            statistical_metrics=final_statistical_metrics,
            comparison_type=request.comparison_type,
            job_id=job_id,
            run_id=run_id,
        )

    # Update job status to complete
    analysis_job.status = "COMPLETE"
    db.commit()

    return StatisticalComparisonResponse(
        job_id=job_id,
        comparison_type=request.comparison_type,
        condition_results=condition_results_api,
        statistical_metrics=final_statistical_metrics,
        report_url=f"/{report_path}" if report_path else None
    )


async def _load_corpus_texts(corpus_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Load texts from corpus directory"""
    from pathlib import Path
    
    file_path = corpus_config.get("file_path")
    pattern = corpus_config.get("pattern", "**/*.txt")
    
    if not file_path:
        return []
    
    corpus_path = Path(file_path)
    if not corpus_path.exists():
        return []
    
    text_files = list(corpus_path.glob(pattern))
    corpus_texts = []
    
    for text_file in text_files:
        try:
            content = text_file.read_text(encoding='utf-8')
            if content.strip():  # Only include non-empty files
                corpus_texts.append({
                    "text_id": text_file.stem,
                    "content": content,
                    "file_path": str(text_file),
                    "category": text_file.parent.name if text_file.parent.name != corpus_path.name else "uncategorized"
                })
        except Exception as e:
            print(f"Error loading {text_file}: {e}")
            continue
    
    return corpus_texts


def _get_models_for_comparison(models_config: Dict[str, Any], requested_models: Optional[List[str]]) -> List[str]:
    """Extract models to compare from experiment configuration"""
    if requested_models:
        return requested_models
    
    # Extract enabled flagship models from config
    flagship_models = models_config.get("flagship_models", {})
    enabled_models = []
    
    for model_key, model_info in flagship_models.items():
        if model_info.get("enabled", True):  # Default to enabled
            enabled_models.append(model_info["model_id"])
    
    return enabled_models


def _calculate_corpus_geometric_similarity(model_groups: Dict[str, List]) -> Dict[str, Any]:
    """Calculate geometric similarity metrics across corpus"""
    import numpy as np
    from itertools import combinations
    
    results = {}
    
    # Calculate average centroids for each model
    model_centroids = {}
    for model, results_list in model_groups.items():
        centroids = [r["centroid"] for r in results_list]
        avg_centroid = _calculate_average_centroid(centroids)
        model_centroids[model] = avg_centroid
    
    # Calculate pairwise distances between model averages
    model_names = list(model_centroids.keys())
    pairwise_distances = {}
    
    for model1, model2 in combinations(model_names, 2):
        centroid1 = np.array(model_centroids[model1])
        centroid2 = np.array(model_centroids[model2])
        distance = np.linalg.norm(centroid1 - centroid2)
        pairwise_distances[f"{model1}_vs_{model2}"] = float(distance)
    
    # Calculate overall statistics
    distances = list(pairwise_distances.values())
    
    results = {
        "model_average_centroids": model_centroids,
        "pairwise_distances": pairwise_distances,
        "mean_distance": float(np.mean(distances)) if distances else 0.0,
        "max_distance": float(np.max(distances)) if distances else 0.0,
        "min_distance": float(np.min(distances)) if distances else 0.0,
        "std_distance": float(np.std(distances)) if distances else 0.0
    }
    
    return results


def _calculate_corpus_dimensional_correlation(model_groups: Dict[str, List]) -> Dict[str, Any]:
    """Calculate dimensional correlation across corpus"""
    import numpy as np
    from scipy import stats
    
    # Get all unique score dimensions
    all_dimensions = set()
    for results_list in model_groups.values():
        for result in results_list:
            all_dimensions.update(result["scores"].keys())
    
    dimensions = sorted(list(all_dimensions))
    
    # Create correlation matrix between models
    model_names = list(model_groups.keys())
    correlation_matrix = np.eye(len(model_names))
    
    for i, model1 in enumerate(model_names):
        for j, model2 in enumerate(model_names):
            if i < j:  # Only calculate upper triangle
                # Get scores for both models across all texts
                scores1 = []
                scores2 = []
                
                # Match texts between models
                for result1 in model_groups[model1]:
                    text_id = result1["text_id"]
                    # Find corresponding result in model2
                    result2 = next((r for r in model_groups[model2] if r["text_id"] == text_id), None)
                    
                    if result2:
                        # Collect scores for all dimensions
                        for dim in dimensions:
                            score1 = result1["scores"].get(dim, 0.0)
                            score2 = result2["scores"].get(dim, 0.0)
                            scores1.append(score1)
                            scores2.append(score2)
                
                if len(scores1) > 1:
                    correlation, p_value = stats.pearsonr(scores1, scores2)
                    correlation_matrix[i, j] = correlation
                    correlation_matrix[j, i] = correlation
    
    return {
        "model_names": model_names,
        "correlation_matrix": correlation_matrix.tolist(),
        "dimensions_analyzed": dimensions,
        "total_comparisons": len(model_groups[model_names[0]]) * len(dimensions) if model_names else 0
    }


def _perform_hypothesis_testing(model_groups: Dict[str, List]) -> Dict[str, Any]:
    """Perform statistical hypothesis testing"""
    from scipy import stats
    import numpy as np
    from itertools import combinations
    
    results = {}
    model_names = list(model_groups.keys())
    
    for model1, model2 in combinations(model_names, 2):
        # Get matched centroid pairs
        centroids1 = []
        centroids2 = []
        
        for result1 in model_groups[model1]:
            text_id = result1["text_id"]
            result2 = next((r for r in model_groups[model2] if r["text_id"] == text_id), None)
            
            if result2:
                centroids1.append(result1["centroid"])
                centroids2.append(result2["centroid"])
        
        if len(centroids1) > 2:  # Need minimum sample size
            # Separate x and y coordinates
            x1 = [c[0] for c in centroids1]
            y1 = [c[1] for c in centroids1]
            x2 = [c[0] for c in centroids2]
            y2 = [c[1] for c in centroids2]
            
            # Paired t-tests for x and y coordinates
            t_stat_x, p_val_x = stats.ttest_rel(x1, x2)
            t_stat_y, p_val_y = stats.ttest_rel(y1, y2)
            
            # Bonferroni correction
            alpha = 0.05 / 2
            
            results[f"{model1}_vs_{model2}"] = {
                "x_axis": {
                    "t_statistic": float(t_stat_x),
                    "p_value": float(p_val_x),
                    "significant": bool(p_val_x < alpha)
                },
                "y_axis": {
                    "t_statistic": float(t_stat_y),
                    "p_value": float(p_val_y),
                    "significant": bool(p_val_y < alpha)
                },
                "overall_similar": bool(p_val_x >= alpha and p_val_y >= alpha),
                "sample_size": len(centroids1),
                "alpha_corrected": alpha
            }
    
    return results


def _calculate_effect_sizes(model_groups: Dict[str, List]) -> Dict[str, Any]:
    """Calculate effect sizes (Cohen's d) for model comparisons"""
    import numpy as np
    from itertools import combinations
    
    results = {}
    model_names = list(model_groups.keys())
    
    for model1, model2 in combinations(model_names, 2):
        # Get matched centroid pairs
        centroids1 = []
        centroids2 = []
        
        for result1 in model_groups[model1]:
            text_id = result1["text_id"]
            result2 = next((r for r in model_groups[model2] if r["text_id"] == text_id), None)
            
            if result2:
                centroids1.append(result1["centroid"])
                centroids2.append(result2["centroid"])
        
        if len(centroids1) > 1:
            # Calculate Cohen's d for x and y coordinates
            x1 = np.array([c[0] for c in centroids1])
            y1 = np.array([c[1] for c in centroids1])
            x2 = np.array([c[0] for c in centroids2])
            y2 = np.array([c[1] for c in centroids2])
            
            # Pooled standard deviation
            def cohens_d(group1, group2):
                n1, n2 = len(group1), len(group2)
                pooled_std = np.sqrt(((n1 - 1) * np.var(group1, ddof=1) + 
                                    (n2 - 1) * np.var(group2, ddof=1)) / (n1 + n2 - 2))
                return (np.mean(group1) - np.mean(group2)) / pooled_std if pooled_std > 0 else 0.0
            
            d_x = cohens_d(x1, x2)
            d_y = cohens_d(y1, y2)
            
            # Interpretation
            def interpret_cohens_d(d):
                abs_d = abs(d)
                if abs_d < 0.2:
                    return "negligible"
                elif abs_d < 0.5:
                    return "small"
                elif abs_d < 0.8:
                    return "medium"
                else:
                    return "large"
            
            results[f"{model1}_vs_{model2}"] = {
                "cohens_d_x": float(d_x),
                "cohens_d_y": float(d_y),
                "interpretation_x": interpret_cohens_d(d_x),
                "interpretation_y": interpret_cohens_d(d_y),
                "overall_effect_size": float(np.sqrt(d_x**2 + d_y**2)),
                "sample_size": len(centroids1)
            }
    
    return results


def _calculate_confidence_intervals(model_groups: Dict[str, List]) -> Dict[str, Any]:
    """Calculate confidence intervals for model centroids"""
    import numpy as np
    from scipy import stats
    
    results = {}
    confidence_levels = [0.90, 0.95, 0.99]
    
    for model, results_list in model_groups.items():
        centroids = [r["centroid"] for r in results_list]
        
        if len(centroids) > 1:
            x_coords = [c[0] for c in centroids]
            y_coords = [c[1] for c in centroids]
            
            model_cis = {}
            
            for confidence in confidence_levels:
                n = len(centroids)
                t_val = stats.t.ppf((1 + confidence) / 2, n - 1)
                
                # X coordinate CI
                x_mean = np.mean(x_coords)
                x_std_err = stats.sem(x_coords)
                x_margin = t_val * x_std_err
                
                # Y coordinate CI
                y_mean = np.mean(y_coords)
                y_std_err = stats.sem(y_coords)
                y_margin = t_val * y_std_err
                
                model_cis[f"{int(confidence*100)}%"] = {
                    "x_axis": {
                        "mean": float(x_mean),
                        "lower": float(x_mean - x_margin),
                        "upper": float(x_mean + x_margin),
                        "margin_of_error": float(x_margin)
                    },
                    "y_axis": {
                        "mean": float(y_mean),
                        "lower": float(y_mean - y_margin),
                        "upper": float(y_mean + y_margin),
                        "margin_of_error": float(y_margin)
                    }
                }
            
            results[model] = model_cis
    
    return results


def _classify_corpus_similarity(statistical_metrics: Dict[str, Any], experiment_def: Dict[str, Any]) -> str:
    """Classify overall similarity based on statistical results"""
    
    thresholds = experiment_def.get("statistical_analysis", {}).get("similarity_classification", {}).get("thresholds", {})
    
    # Get key metrics
    geometric = statistical_metrics.get("geometric_similarity", {})
    correlation = statistical_metrics.get("dimensional_correlation", {})
    hypothesis = statistical_metrics.get("hypothesis_testing", {})
    
    mean_distance = geometric.get("mean_distance", 1.0)
    correlation_matrix = correlation.get("correlation_matrix", [[]])
    
    # Calculate average correlation (excluding diagonal)
    avg_correlation = 0.0
    if correlation_matrix and len(correlation_matrix) > 1:
        correlations = []
        for i in range(len(correlation_matrix)):
            for j in range(len(correlation_matrix[i])):
                if i != j:  # Exclude diagonal
                    correlations.append(correlation_matrix[i][j])
        avg_correlation = np.mean(correlations) if correlations else 0.0
    
    # Count significant differences
    significant_differences = 0
    total_comparisons = 0
    for comparison, results in hypothesis.items():
        if isinstance(results, dict):
            total_comparisons += 1
            if not results.get("overall_similar", True):
                significant_differences += 1
    
    # Apply classification thresholds
    highly_similar = thresholds.get("highly_similar", {})
    moderately_similar = thresholds.get("moderately_similar", {})
    
    if (mean_distance <= highly_similar.get("geometric_distance", 0.15) and
        avg_correlation >= highly_similar.get("correlation_threshold", 0.85) and
        significant_differences == 0):
        return "HIGHLY_SIMILAR"
    elif (mean_distance <= moderately_similar.get("geometric_distance", 0.35) and
          avg_correlation >= moderately_similar.get("correlation_threshold", 0.65) and
          significant_differences <= total_comparisons * 0.3):
        return "MODERATELY_SIMILAR"
    else:
        return "STATISTICALLY_DIFFERENT"


def _calculate_average_centroid(centroids: List[Tuple[float, float]]) -> Tuple[float, float]:
    """Calculate average centroid from list of centroids"""
    if not centroids:
        return (0.0, 0.0)
    
    avg_x = sum(c[0] for c in centroids) / len(centroids)
    avg_y = sum(c[1] for c in centroids) / len(centroids)
    return (avg_x, avg_y)


def _calculate_average_scores(scores_list: List[Dict[str, float]]) -> Dict[str, float]:
    """Calculate average scores from list of score dictionaries"""
    if not scores_list:
        return {}
    
    # Get all unique keys
    all_keys = set()
    for scores in scores_list:
        all_keys.update(scores.keys())
    
    # Calculate averages
    avg_scores = {}
    for key in all_keys:
        values = [scores.get(key, 0.0) for scores in scores_list]
        avg_scores[key] = sum(values) / len(values)
    
    return avg_scores


@app.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"}
