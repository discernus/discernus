from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import uuid
import yaml # For loading the experiment file

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

app = FastAPI()

# Mount a directory to serve the static report files
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# No longer need a global framework loader, it will be loaded per request.
report_builder = ReportBuilder(output_dir="reports/reboot_mvp") # Keep reports organized

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

        # Step 2: Get the raw analysis from the LLM Gateway
        llm_result = await get_llm_analysis(
            text=request.text,
            experiment_def=experiment_def,
            model=request.model
        )
        
        if llm_result.get("error"):
            raise HTTPException(status_code=500, detail=f"LLM Error: {llm_result.get('error')}")

        # Step 3: Parse the scores from the LLM response
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

        # Step 4: Calculate the centroid using the Signature Engine
        x, y = calculate_coordinates(experiment_def, scores)
        
        # Step 5: Generate the visual report
        anchors = _extract_anchors_from_framework(experiment_def)
        report_path = report_builder.generate_report(
            anchors=anchors,
            scores=scores,
            coordinates=(x, y),
            run_id=run_id
        )

        # Step 6: Return the final response
        return FinalResponse(
            x=x,
            y=y,
            framework_id=experiment_def.get("framework", {}).get("name"),
            model=request.model,
            report_url=f"/{report_path}"
        )

    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"} 