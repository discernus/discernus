from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import uuid
import yaml # For loading the experiment file
from typing import Dict, Any, Tuple, List
from celery.result import AsyncResult
import os
from pathlib import Path

from src.reboot.gateway.llm_gateway import get_llm_analysis
from src.reboot.engine.signature_engine import calculate_coordinates, _extract_anchors_from_framework
from src.reboot.reporting.report_builder import ReportBuilder
from src.reboot.tasks import analyze_text_task

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
        
        # Step 3: Generate the comparison visual report
        anchors = _extract_anchors_from_framework(experiment_def)
        report_path = report_builder.generate_comparison_report(
            anchors=anchors,
            analysis_a=analysis_a,
            label_a=request.label_a,
            analysis_b=analysis_b,
            label_b=request.label_b,
            run_id=run_id
        )

        return ComparisonResponse(
            report_url=f"/{report_path}",
            text_a_centroid=analysis_a["centroid"],
            text_b_centroid=analysis_b["centroid"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-corpus", response_model=JobResponse)
async def analyze_corpus(request: CorpusAnalysisRequest):
    """
    Submits a batch of texts for analysis.
    """
    job_id = str(uuid.uuid4())
    job_dir = TEMP_RESULTS_DIR / job_id
    job_dir.mkdir()

    try:
        with open(request.experiment_file_path, 'r') as f:
            experiment_def = yaml.safe_load(f)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not load experiment file: {e}")

    for i, file_path in enumerate(request.file_paths):
        try:
            with open(file_path, 'r') as f:
                text = f.read()
            
            # Create a unique filename for the result
            result_filename = f"result_{i}_{Path(file_path).stem}.json"
            
            # Dispatch a task for each file, including job_id and filename
            analyze_text_task.delay(
                text=text,
                experiment_def=experiment_def,
                model=request.model,
                job_id=job_id,
                result_filename=result_filename
            )
        except Exception as e:
            # Log this error but continue
            print(f"Failed to process file {file_path}: {e}")
    
    return JobResponse(job_id=job_id)

@app.get("/results/{job_id}", response_model=ResultResponse)
async def get_results(job_id: str):
    """
    Retrieves the status and results of a job from the temporary file store.
    """
    job_dir = TEMP_RESULTS_DIR / job_id
    if not job_dir.is_dir():
        raise HTTPException(status_code=404, detail="Job ID not found.")

    results = []
    # Note: We don't know the total number of expected files here yet.
    # This is a limitation of the simple file-based approach.
    for result_file in job_dir.glob("*.json"):
        with open(result_file, 'r') as f:
            results.append(json.load(f))
            
    # A more robust system would know the total tasks dispatched.
    # For now, we'll just return what we have.
    status = "COMPLETE" # Placeholder status
    if not results:
        status = "PENDING"

    return ResultResponse(job_id=job_id, status=status, results=results)

@app.post("/compare-groups", response_model=GroupComparisonResponse)
async def compare_groups(request: GroupComparisonRequest):
    """
    Retrieves results for two jobs, calculates the centroid for each group,
    and generates a comparative report.
    """
    run_id = str(uuid.uuid4())
    try:
        # Step 1: Fetch results for both jobs
        results_a = await get_results(request.job_id_a)
        results_b = await get_results(request.job_id_b)
        
        # Step 2: Load experiment definition to get anchors
        with open(request.experiment_file_path, 'r') as f:
            experiment_def = yaml.safe_load(f)
        anchors = _extract_anchors_from_framework(experiment_def)

        # Step 3: Generate the group comparison report
        report_path = report_builder.generate_group_comparison_report(
            anchors=anchors,
            group_a_signatures=results_a.results,
            label_a=request.label_a,
            group_b_signatures=results_b.results,
            label_b=request.label_b,
            run_id=run_id
        )
        
        # Calculate centroids to return in the response
        def _calculate_centroid(signatures):
            if not signatures: return (0.0, 0.0)
            coords = [s['centroid'] for s in signatures if 'centroid' in s]
            if not coords: return (0.0, 0.0)
            return sum(c[0] for c in coords)/len(coords), sum(c[1] for c in coords)/len(coords)

        centroid_a = _calculate_centroid(results_a.results)
        centroid_b = _calculate_centroid(results_b.results)

        return GroupComparisonResponse(
            report_url=f"/{report_path}",
            group_a_centroid=centroid_a,
            group_b_centroid=centroid_b,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"} 