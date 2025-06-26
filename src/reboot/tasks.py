from celery import Celery
import json
from typing import Dict, Any
import os

from src.reboot.gateway.llm_gateway import get_llm_analysis
from src.reboot.engine.signature_engine import calculate_coordinates
from src.reboot.database.session import SessionLocal
from src.reboot.database.models import AnalysisResult, AnalysisJob, JobStatus

# For now, we assume a local Redis server is running.
# In a production setup, this would come from a config file.
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("reboot_tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery_app.task(name="reboot.analyze_text_task")
def analyze_text_task(text: str, experiment_def: Dict[str, Any], model: str, job_id: str) -> bool:
    """
    Celery task to run the full analysis pipeline for a single text and save the result to the database.
    """
    db = SessionLocal()
    try:
        # This task is synchronous internally, but runs asynchronously as a Celery worker.
        # The 'async' keyword is not used here, but we need to handle the async call
        # to the LLM gateway.
        import asyncio

        async def run_analysis():
            # Step 1: Get the raw analysis from the LLM Gateway
            llm_result = await get_llm_analysis(text=text, experiment_def=experiment_def, model=model)
            if llm_result.get("error"):
                raise Exception(f"LLM Error: {llm_result.get('error')}")

            # Step 2: Parse the scores from the LLM response
            raw_response_str = llm_result.get("raw_response", "")
            if raw_response_str.startswith("```json"):
                raw_response_str = raw_response_str[7:]
            if raw_response_str.endswith("```"):
                raw_response_str = raw_response_str[:-3]
            raw_response_str = raw_response_str.strip()
            raw_response_json = json.loads(raw_response_str)
            scores = {
                k: v.get("score", 0.0) for k, v in raw_response_json.items() if isinstance(v, dict) and "score" in v
            }
            if not scores:
                raise ValueError("Could not extract scores from the parsed JSON.")

            # Step 3: Calculate the centroid using the Signature Engine
            x, y = calculate_coordinates(experiment_def, scores)

            return {"scores": scores, "centroid": (x, y)}

        # Run the analysis
        result_data = asyncio.run(run_analysis())

        # Save the result to the database
        new_result = AnalysisResult(
            job_id=job_id,
            centroid_x=result_data["centroid"][0],
            centroid_y=result_data["centroid"][1],
            scores=json.dumps(result_data["scores"]),
        )
        db.add(new_result)
        db.commit()

        return True
    except Exception as e:
        job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
        if job:
            job.status = JobStatus.FAILED
            db.commit()
        # In a real system, we would have more robust error logging here.
        print(f"Failed to process and save result for job {job_id}: {e}")
        return False
    finally:
        db.close()
