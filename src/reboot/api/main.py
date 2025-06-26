from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import uuid

from src.reboot.gateway.llm_gateway import get_llm_analysis
from src.reboot.engine.signature_engine import FrameworkLoader, calculate_coordinates
from src.reboot.reporting.report_builder import ReportBuilder

class AnalysisRequest(BaseModel):
    text: str
    framework_id: str
    model: str = "gpt-4o" # Default to a known good model
    # In the future, this could include user session, comparison context, etc.

class FinalResponse(BaseModel):
    x: float
    y: float
    framework_id: str
    model: str
    report_url: str

app = FastAPI()
# Correctly instantiate the loader with the path to the frameworks
frameworks_path = "research_workspaces/june_2025_research_dev_workspace/frameworks"
framework_loader = FrameworkLoader(frameworks_base_dir=frameworks_path)
report_builder = ReportBuilder(output_dir="reports/reboot_mvp") # Keep reports organized

@app.post("/analyze", response_model=FinalResponse)
async def analyze_text(request: AnalysisRequest):
    """
    This endpoint receives a text and a framework choice,
    and returns the final geometric coordinates and a visual report.
    """
    run_id = str(uuid.uuid4())
    try:
        # Step 1: Get the raw analysis from the LLM Gateway
        llm_result = await get_llm_analysis(
            text=request.text,
            framework=request.framework_id,
            model=request.model
        )
        
        if llm_result.get("error"):
            raise HTTPException(status_code=500, detail=f"LLM Error: {llm_result.get('error')}")

        # Step 2: Load the framework definition
        framework_def = framework_loader.load_framework(request.framework_id)
        if not framework_def:
            raise HTTPException(status_code=404, detail=f"Framework '{request.framework_id}' not found.")

        # Step 3: Extract the scores from the nested LLM response
        try:
            # The actual scores are in a JSON string inside the 'raw_response'
            raw_response_str = llm_result.get("raw_response", "")
            
            # Clean the string: remove markdown backticks and surrounding whitespace
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

        # Step 4: Calculate the coordinates using the Signature Engine
        x, y = calculate_coordinates(framework_def, scores)
        
        # Step 5: Generate the visual report
        report_path = report_builder.generate_report(
            framework_def=framework_def,
            scores=scores,
            coordinates=(x, y),
            run_id=run_id
        )

        # Step 6: Return the final response
        return FinalResponse(
            x=x,
            y=y,
            framework_id=request.framework_id,
            model=request.model,
            report_url=report_path
        )

    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"} 