from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import uuid
import yaml # For loading the experiment file
from typing import Dict, Any, Tuple, List
from celery.result import AsyncResult
import os
import asyncio
from pathlib import Path
from sqlalchemy.orm import Session

from src.reboot.gateway.llm_gateway import get_llm_analysis
from src.reboot.engine.signature_engine import calculate_coordinates, _extract_anchors_from_framework, calculate_distance
from src.reboot.reporting.report_builder import ReportBuilder
from src.reboot.tasks import analyze_text_task
from src.reboot.database.session import get_db
from src.reboot.database.models import AnalysisJob, AnalysisResult, JobStatus

class AnalysisRequest(BaseModel):
    text: str
    experiment_file_path: str = "src/reboot/experiments/reboot_mft_experiment.yaml"
    model: str = "gpt-4o"

class FinalResponse(BaseModel):
    x: float
    y: float
    framework_id: str
    model: str
    report_url: str

class ComparisonRequest(BaseModel):
    text_a: str
    text_b: str
    label_a: str = "Text A"
    label_b: str = "Text B"
    experiment_file_path: str = "src/reboot/experiments/reboot_mft_experiment.yaml"
    model: str = "gpt-4o"

class ComparisonResponse(BaseModel):
    report_url: str
    text_a_centroid: Tuple[float, float]
    text_b_centroid: Tuple[float, float]
    distance: float

class CorpusAnalysisRequest(BaseModel):
    file_paths: List[str]
    experiment_file_path: str = "src/reboot/experiments/reboot_mft_experiment.yaml"
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
    experiment_file_path: str = "src/reboot/experiments/reboot_mft_experiment.yaml"

class GroupComparisonResponse(BaseModel):
    report_url: str
    group_a_centroid: Tuple[float, float]
    group_b_centroid: Tuple[float, float]
    distance: float

class DirectGroupComparisonRequest(BaseModel):
    group1: Dict[str, Any]  # {"name": "Group Name", "texts": ["text1", "text2", ...]}
    group2: Dict[str, Any]  # {"name": "Group Name", "texts": ["text1", "text2", ...]}
    framework_id: str = "moral_foundations_theory"
    experiment_file_path: str = "src/reboot/experiments/reboot_mft_experiment.yaml"
    model: str = "gpt-4o"

app = FastAPI()

# Mount a directory to serve the static report files
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# No longer need a global framework loader, it will be loaded per request.
report_builder = ReportBuilder(output_dir="reports/reboot_mvp") # Keep reports organized
TEMP_RESULTS_DIR = Path("temp_results")
TEMP_RESULTS_DIR.mkdir(exist_ok=True)

async def _run_single_analysis(text: str, model: str, experiment_def: Dict[str, Any]) -> Dict[str, Any]:
    """Helper function to run the full analysis pipeline for a single text."""
    # Step 1: Get the raw analysis from the LLM Gateway
    llm_result = await get_llm_analysis(
        text=text,
        experiment_def=experiment_def,
        model=model
    )
    if llm_result.get("error"):
        raise HTTPException(status_code=500, detail=f"LLM Error: {llm_result.get('error')}")

    # Step 2: Parse the scores from the LLM response
    try:
        raw_response_str = llm_result.get("raw_response", "")
        if raw_response_str.startswith("```json"):
            raw_response_str = raw_response_str[7:]
        if raw_response_str.endswith("```"):
            raw_response_str = raw_response_str[:-3]
        raw_response_str = raw_response_str.strip()
        raw_response_json = json.loads(raw_response_str)
        scores = {k: v.get('score', 0.0) for k, v in raw_response_json.items() if isinstance(v, dict) and 'score' in v}
        if not scores:
            raise ValueError("Could not extract scores from the parsed JSON.")
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse scores from LLM response: {e}")

    # Step 3: Calculate the centroid using the Signature Engine
    x, y = calculate_coordinates(experiment_def, scores)
    
    return {"scores": scores, "centroid": (x, y)}

@app.post("/analyze", response_model=FinalResponse)
async def analyze_text(request: AnalysisRequest):
    """
    This endpoint orchestrates a single-text analysis and returns the
    centroid coordinates and a URL to a visual report.
    """
    run_id = str(uuid.uuid4())
    try:
        # Step 1: Load the self-contained experiment definition
        try:
            with open(request.experiment_file_path, 'r') as f:
                experiment_def = yaml.safe_load(f)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Could not load experiment file: {e}")

        # Step 2: Run the analysis
        analysis_result = await _run_single_analysis(request.text, request.model, experiment_def)
        
        # Step 3: Generate the visual report
        anchors = _extract_anchors_from_framework(experiment_def)
        report_path = report_builder.generate_report(
            anchors=anchors,
            scores=analysis_result["scores"],
            coordinates=analysis_result["centroid"],
            run_id=run_id
        )

        # Step 4: Return the final response
        return FinalResponse(
            x=analysis_result["centroid"][0],
            y=analysis_result["centroid"][1],
            framework_id=experiment_def.get("framework", {}).get("name"),
            model=request.model,
            report_url=f"/{report_path}"
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
            with open(request.experiment_file_path, 'r') as f:
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
            distance=distance
        )

        return ComparisonResponse(
            report_url=f"/{report_path}",
            text_a_centroid=analysis_a["centroid"],
            text_b_centroid=analysis_b["centroid"],
            distance=distance
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
        with open(request.experiment_file_path, 'r') as f:
            experiment_def = yaml.safe_load(f)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not load experiment file: {e}")

    task_count = 0
    for i, file_path in enumerate(request.file_paths):
        try:
            with open(file_path, 'r') as f:
                text = f.read()
            
            analyze_text_task.delay(
                text=text,
                experiment_def=experiment_def,
                model=request.model,
                job_id=job_id
            )
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
        results=[
            {
                "centroid": (r.centroid_x, r.centroid_y),
                "scores": json.loads(r.scores)
            } for r in results
        ]
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

        with open(request.experiment_file_path, 'r') as f:
            experiment_def = yaml.safe_load(f)
        anchors = _extract_anchors_from_framework(experiment_def)
        
        def _calculate_centroid(signatures):
            if not signatures: return (0.0, 0.0)
            coords = [s['centroid'] for s in signatures if 'centroid' in s]
            if not coords: return (0.0, 0.0)
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
            distance=distance
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
        with open(request.experiment_file_path, 'r') as f:
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
        group1_analyses = all_results[:len(group1_texts)]
        group2_analyses = all_results[len(group1_texts):]

        # Format results for reporting
        group1_results = [{"text": t, **a} for t, a in zip(group1_texts, group1_analyses)]
        group2_results = [{"text": t, **a} for t, a in zip(group2_texts, group2_analyses)]
        
        def _calculate_centroid(signatures):
            if not signatures: return (0.0, 0.0)
            coords = [s['centroid'] for s in signatures if 'centroid' in s]
            if not coords: return (0.0, 0.0)
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
            distance=distance
        )
        
        return GroupComparisonResponse(
            report_url=f"/{report_path}",
            group_a_centroid=centroid_a,
            group_b_centroid=centroid_b,
            distance=distance
        )
    except Exception as e:
        # This will now catch exceptions from asyncio.gather as well
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"} 