from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import uuid
import yaml # For loading the experiment file
from typing import Dict, Any, Tuple

from src.reboot.gateway.llm_gateway import get_llm_analysis
from src.reboot.engine.signature_engine import calculate_coordinates, _extract_anchors_from_framework
from src.reboot.reporting.report_builder import ReportBuilder

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

app = FastAPI()

# Mount a directory to serve the static report files
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# No longer need a global framework loader, it will be loaded per request.
report_builder = ReportBuilder(output_dir="reports/reboot_mvp") # Keep reports organized

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

@app.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"} 