from celery import Celery
import yaml
import json
from typing import Dict, Any
from pathlib import Path
import os

from src.reboot.gateway.llm_gateway import get_llm_analysis
from src.reboot.engine.signature_engine import calculate_coordinates, _extract_anchors_from_framework

# For now, we assume a local Redis server is running.
# In a production setup, this would come from a config file.
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

celery_app = Celery(
    'reboot_tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# Temporary directory for storing task results
TEMP_RESULTS_DIR = Path("temp_results")
TEMP_RESULTS_DIR.mkdir(exist_ok=True)

@celery_app.task(name='reboot.analyze_text_task')
def analyze_text_task(text: str, experiment_def: Dict[str, Any], model: str, job_id: str, result_filename: str) -> bool:
    """
    Celery task to run the full analysis pipeline for a single text and save the result to a file.
    """
    # This task is synchronous internally, but runs asynchronously as a Celery worker.
    # The 'async' keyword is not used here, but we need to handle the async call
    # to the LLM gateway.
    import asyncio

    async def run_analysis():
        # Step 1: Get the raw analysis from the LLM Gateway
        llm_result = await get_llm_analysis(
            text=text,
            experiment_def=experiment_def,
            model=model
        )
        if llm_result.get("error"):
            # In a real setup, we'd have more robust error handling here
            return {"error": f"LLM Error: {llm_result.get('error')}"}

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
            return {"error": f"Failed to parse scores from LLM response: {e}"}

        # Step 3: Calculate the centroid using the Signature Engine
        x, y = calculate_coordinates(experiment_def, scores)
        
        return {"scores": scores, "centroid": (x, y)}

    # Run the analysis
    result_data = asyncio.run(run_analysis())

    # Save the result to a file in the job-specific directory
    try:
        job_dir = TEMP_RESULTS_DIR / job_id
        job_dir.mkdir(exist_ok=True) # Ensure directory exists
        result_file_path = job_dir / result_filename
        
        with open(result_file_path, 'w') as f:
            json.dump(result_data, f)
        
        return True
    except Exception as e:
        # In a real system, we would have more robust error logging here.
        print(f"Failed to save result for job {job_id}: {e}")
        return False 