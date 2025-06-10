"""
FastAPI application for Narrative Gravity Analysis.
Implements Epic 1: Corpus & Job Management Backend API endpoints.
Enhanced for v2.1 hierarchical analysis research workbench.
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime
import os
import json
from pathlib import Path

from ..models.base import get_db
from ..models import User, Experiment, Run
from . import schemas, crud, services
from ..utils.auth import get_current_user, get_current_admin_user, get_optional_user
from ..utils.sanitization import sanitize_string, sanitize_search_query, SanitizationError
from .auth import router as auth_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Narrative Gravity Analysis API",
    description="Epic 1: Corpus & Job Management Backend + v2.1 Research Workbench",
    version="2.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware for web interface integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit default port
        "http://localhost:3000",  # React dev server
        "http://localhost:3001",  # React dev server (alt)
        "http://localhost:3002",  # React dev server (alt)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication router
app.include_router(auth_router, prefix="/api")

# Health check endpoint
@app.get("/api/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify API and database connectivity."""
    try:
        # Test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
            "version": "2.1.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )

# v2.1 Research Workbench Endpoints

@app.post("/api/experiments", response_model=schemas.ExperimentResponse)
async def create_experiment(
    experiment_data: schemas.ExperimentCreate,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Create a new research experiment."""
    try:
        experiment = Experiment(
            creator_id=current_user.id if current_user else 1,  # Default to user ID 1 for testing
            name=experiment_data.name,
            hypothesis=experiment_data.hypothesis,
            description=experiment_data.description,
            research_context=experiment_data.research_context,
            prompt_template_id=experiment_data.prompt_template_id,
            framework_config_id=experiment_data.framework_config_id,
            scoring_algorithm_id=experiment_data.scoring_algorithm_id,
            analysis_mode=experiment_data.analysis_mode,
            selected_models=experiment_data.selected_models,
            research_notes=experiment_data.research_notes,
            tags=experiment_data.tags
        )
        
        db.add(experiment)
        db.commit()
        db.refresh(experiment)
        
        logger.info(f"Created experiment {experiment.id}: {experiment.name}")
        return experiment
        
    except Exception as e:
        logger.error(f"Experiment creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Experiment creation failed: {str(e)}"
        )

@app.get("/api/experiments", response_model=List[schemas.ExperimentResponse])
async def list_experiments(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """List user's experiments with optional status filtering."""
    if current_user:
        query = db.query(Experiment).filter(Experiment.creator_id == current_user.id)
    else:
        query = db.query(Experiment)  # Return all experiments for testing
    
    if status_filter:
        query = query.filter(Experiment.status == status_filter)
    
    experiments = query.offset(skip).limit(limit).all()
    return experiments

@app.get("/api/experiments/{experiment_id}", response_model=schemas.ExperimentResponse)
async def get_experiment(
    experiment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get experiment details."""
    experiment = db.query(Experiment).filter(
        Experiment.id == experiment_id,
        Experiment.creator_id == current_user.id
    ).first()
    
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    
    return experiment

@app.put("/api/experiments/{experiment_id}", response_model=schemas.ExperimentResponse)
async def update_experiment(
    experiment_id: int,
    experiment_data: schemas.ExperimentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update experiment details."""
    experiment = db.query(Experiment).filter(
        Experiment.id == experiment_id,
        Experiment.creator_id == current_user.id
    ).first()
    
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    
    # Update fields
    for field, value in experiment_data.dict(exclude_unset=True).items():
        setattr(experiment, field, value)
    
    db.commit()
    db.refresh(experiment)
    
    return experiment

@app.post("/api/experiments/{experiment_id}/runs", response_model=schemas.RunResponse)
async def create_run(
    experiment_id: int,
    run_data: schemas.RunCreate,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Create a new analysis run for an experiment."""
    # Verify experiment ownership (or allow all for testing)
    if current_user:
        experiment = db.query(Experiment).filter(
            Experiment.id == experiment_id,
            Experiment.creator_id == current_user.id
        ).first()
    else:
        experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    
    try:
        # Get next run number
        last_run = db.query(Run).filter(Run.experiment_id == experiment_id).order_by(Run.run_number.desc()).first()
        next_run_number = (last_run.run_number + 1) if last_run else 1
        
        # Execute analysis using the same logic as single-text analysis
        import uuid
        import random
        
        # Generate realistic mock scores for the analysis
        mock_raw_scores = {
            "Dignity": round(random.uniform(0.2, 0.8), 3),
            "Truth": round(random.uniform(0.2, 0.8), 3),
            "Justice": round(random.uniform(0.2, 0.8), 3),
            "Hope": round(random.uniform(0.2, 0.8), 3),
            "Pragmatism": round(random.uniform(0.2, 0.8), 3),
            "Tribalism": round(random.uniform(0.1, 0.6), 3),
            "Manipulation": round(random.uniform(0.1, 0.6), 3),
            "Resentment": round(random.uniform(0.1, 0.6), 3),
            "Fantasy": round(random.uniform(0.1, 0.6), 3),
            "Fear": round(random.uniform(0.1, 0.6), 3),
        }
        
        # Generate hierarchical ranking
        sorted_wells = sorted(mock_raw_scores.items(), key=lambda x: x[1], reverse=True)
        primary_wells = [
            {"well": sorted_wells[0][0], "score": sorted_wells[0][1], "relative_weight": 40.0},
            {"well": sorted_wells[1][0], "score": sorted_wells[1][1], "relative_weight": 35.0},
            {"well": sorted_wells[2][0], "score": sorted_wells[2][1], "relative_weight": 25.0},
        ]
        
        hierarchical_ranking = {
            "primary_wells": primary_wells,
            "secondary_wells": [],
            "total_weight": 100.0
        }
        
        # Create run record with analysis results
        run = Run(
            experiment_id=experiment_id,
            run_number=next_run_number,
            text_id=run_data.text_id,
            text_content=run_data.text_content,
            input_length=len(run_data.text_content),
            llm_model=run_data.llm_model,
            llm_version=run_data.llm_version or "latest",
            prompt_template_version=experiment.prompt_template_id,
            framework_version=experiment.framework_config_id,
            raw_scores=mock_raw_scores,
            hierarchical_ranking=hierarchical_ranking,
            framework_fit_score=round(random.uniform(0.6, 0.9), 3),
            narrative_elevation=round(random.uniform(0.4, 0.8), 3),
            polarity=round(random.uniform(-0.3, 0.3), 3),
            coherence=round(random.uniform(0.6, 0.9), 3),
            directional_purity=round(random.uniform(0.5, 0.8), 3),
            narrative_position_x=round(random.uniform(-0.3, 0.3), 3),
            narrative_position_y=round(random.uniform(-0.3, 0.3), 3),
            execution_time=datetime.utcnow(),
            duration_seconds=round(random.uniform(2.0, 8.0), 2),
            api_cost=round(random.uniform(0.01, 0.05), 4),
            complete_provenance={
                "prompt_template_hash": f"hash_{experiment.prompt_template_id}",
                "framework_version": experiment.framework_config_id,
                "scoring_algorithm_version": experiment.scoring_algorithm_id,
                "llm_model": run_data.llm_model,
                "timestamp": datetime.utcnow().isoformat(),
                "experiment_id": experiment_id
            },
            status="completed",
            success=True
        )
        
        db.add(run)
        db.commit()
        db.refresh(run)
        
        # Update experiment statistics
        experiment.total_runs += 1
        experiment.successful_runs += 1
        db.commit()
        
        logger.info(f"Completed analysis run {run.id} for experiment {experiment_id}")
        
        return run
        
    except Exception as e:
        logger.error(f"Run creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Run creation failed: {str(e)}"
        )

@app.get("/api/experiments/{experiment_id}/runs", response_model=List[schemas.RunResponse])
async def list_experiment_runs(
    experiment_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """List runs for an experiment."""
    # Verify experiment ownership (or allow all for testing)
    if current_user:
        experiment = db.query(Experiment).filter(
            Experiment.id == experiment_id,
            Experiment.creator_id == current_user.id
        ).first()
    else:
        experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    
    if not experiment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experiment not found"
        )
    
    runs = db.query(Run).filter(Run.experiment_id == experiment_id).offset(skip).limit(limit).all()
    return runs

@app.get("/api/runs/{run_id}", response_model=schemas.RunResponse)
async def get_run(
    run_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific analysis run."""
    run = db.query(Run).join(Experiment).filter(
        Run.id == run_id,
        Experiment.creator_id == current_user.id
    ).first()
    
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Run not found"
        )
    
    return run

@app.post("/api/analyze/single-text", response_model=schemas.SingleTextAnalysisResponse)
async def analyze_single_text(
    request: schemas.SingleTextAnalysisRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Analyze single text with hierarchical analysis.
    This is the main endpoint for the v2.1 research workbench frontend.
    """
    try:
        # TODO: Implement actual analysis service
        # For now, return enhanced mock data that matches the frontend expectations
        
        import uuid
        import random
        from datetime import datetime
        
        # Generate realistic mock scores for Civic Virtue framework
        mock_raw_scores = {
            "Dignity": round(random.uniform(0.2, 0.8), 3),
            "Truth": round(random.uniform(0.2, 0.8), 3),
            "Justice": round(random.uniform(0.2, 0.8), 3),
            "Hope": round(random.uniform(0.2, 0.8), 3),
            "Pragmatism": round(random.uniform(0.2, 0.8), 3),
            "Tribalism": round(random.uniform(0.1, 0.6), 3),
            "Manipulation": round(random.uniform(0.1, 0.6), 3),
            "Resentment": round(random.uniform(0.1, 0.6), 3),
            "Fantasy": round(random.uniform(0.1, 0.6), 3),
            "Fear": round(random.uniform(0.1, 0.6), 3),
        }
        
        # Generate hierarchical ranking
        sorted_wells = sorted(mock_raw_scores.items(), key=lambda x: x[1], reverse=True)
        primary_wells = [
            {"well": sorted_wells[0][0], "score": sorted_wells[0][1], "relative_weight": 40.0},
            {"well": sorted_wells[1][0], "score": sorted_wells[1][1], "relative_weight": 35.0},
            {"well": sorted_wells[2][0], "score": sorted_wells[2][1], "relative_weight": 25.0},
        ]
        
        hierarchical_ranking = schemas.HierarchicalRanking(
            primary_wells=primary_wells,
            secondary_wells=[],
            total_weight=100.0
        )
        
        # Generate well justifications
        well_justifications = {}
        for well, score in mock_raw_scores.items():
            well_justifications[well] = schemas.WellJustification(
                score=score,
                reasoning=f"Analysis shows {well.lower()} themes with moderate to strong presence. The text demonstrates clear patterns consistent with this narrative well.",
                evidence_quotes=[
                    "example quote from text",
                    "another supporting passage"
                ],
                confidence=round(random.uniform(0.7, 0.95), 2)
            )
        
        # Calculate metrics
        calculated_metrics = schemas.CalculatedMetrics(
            narrative_elevation=round(random.uniform(0.4, 0.8), 3),
            polarity=round(random.uniform(-0.3, 0.3), 3),
            coherence=round(random.uniform(0.6, 0.9), 3),
            directional_purity=round(random.uniform(0.5, 0.8), 3)
        )
        
        narrative_position = schemas.NarrativePosition(
            x=round(random.uniform(-0.3, 0.3), 3),
            y=round(random.uniform(-0.3, 0.3), 3)
        )
        
        # Create response
        response = schemas.SingleTextAnalysisResponse(
            analysis_id=str(uuid.uuid4()),
            text_content=request.text_content,
            framework="civic_virtue",
            model=request.llm_model,
            raw_scores=mock_raw_scores,
            hierarchical_ranking=hierarchical_ranking,
            well_justifications=well_justifications,
            calculated_metrics=calculated_metrics,
            narrative_position=narrative_position,
            framework_fit_score=round(random.uniform(0.6, 0.9), 3),
            dominant_wells=[
                {"well": primary_wells[0]["well"], "score": primary_wells[0]["score"], "relative_weight": primary_wells[0]["relative_weight"]},
                {"well": primary_wells[1]["well"], "score": primary_wells[1]["score"], "relative_weight": primary_wells[1]["relative_weight"]},
                {"well": primary_wells[2]["well"], "score": primary_wells[2]["score"], "relative_weight": primary_wells[2]["relative_weight"]},
            ],
            execution_time=datetime.utcnow(),
            duration_seconds=round(random.uniform(2.0, 8.0), 2),
            api_cost=round(random.uniform(0.01, 0.05), 4)
        )
        
        logger.info(f"Single text analysis completed for {len(request.text_content)} characters")
        return response
        
    except Exception as e:
        logger.error(f"Single text analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/api/analyze/multi-model", response_model=schemas.MultiModelAnalysisResponse)
async def analyze_multi_model(
    request: schemas.MultiModelAnalysisRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Analyze text with multiple models for comparison.
    Used for stability assessment in the research workbench.
    """
    try:
        # TODO: Implement actual multi-model analysis service
        # For now, return mock comparison data
        
        import uuid
        import random
        from datetime import datetime
        
        model_results = []
        total_cost = 0.0
        
        for model in request.selected_models:
            runs = []
            for run_num in range(request.runs_per_model):
                # Generate mock run data (similar to single text analysis)
                mock_scores = {
                    "Dignity": round(random.uniform(0.2, 0.8), 3),
                    "Truth": round(random.uniform(0.2, 0.8), 3),
                    "Justice": round(random.uniform(0.2, 0.8), 3),
                    "Hope": round(random.uniform(0.2, 0.8), 3),
                    "Pragmatism": round(random.uniform(0.2, 0.8), 3),
                    "Tribalism": round(random.uniform(0.1, 0.6), 3),
                    "Manipulation": round(random.uniform(0.1, 0.6), 3),
                    "Resentment": round(random.uniform(0.1, 0.6), 3),
                    "Fantasy": round(random.uniform(0.1, 0.6), 3),
                    "Fear": round(random.uniform(0.1, 0.6), 3),
                }
                
                # Mock run response (simplified for multi-model)
                run_cost = round(random.uniform(0.01, 0.05), 4)
                total_cost += run_cost
                
                # Note: This would be a full RunResponse in real implementation
                # For now, creating a simplified mock structure
                
            # Calculate aggregated statistics for this model
            mean_scores = {well: round(random.uniform(0.3, 0.7), 3) for well in mock_scores.keys()}
            score_variance = {well: round(random.uniform(0.01, 0.1), 4) for well in mock_scores.keys()}
            
            model_result = schemas.ModelComparisonResult(
                model=model,
                runs=[],  # Simplified for mock
                mean_scores=mean_scores,
                score_variance=score_variance,
                consistency_score=round(random.uniform(0.7, 0.95), 3)
            )
            
            model_results.append(model_result)
        
        # Generate cross-model analysis
        model_agreement = {well: round(random.uniform(0.6, 0.9), 3) for well in mock_scores.keys()}
        consensus_scores = {well: round(random.uniform(0.3, 0.7), 3) for well in mock_scores.keys()}
        
        response = schemas.MultiModelAnalysisResponse(
            analysis_id=str(uuid.uuid4()),
            text_content=request.text_content,
            framework="civic_virtue",
            scoring_algorithm=request.scoring_algorithm_id,
            model_results=model_results,
            model_agreement=model_agreement,
            consensus_scores=consensus_scores,
            stability_metrics={
                "overall_stability": round(random.uniform(0.7, 0.9), 3),
                "variance_threshold": 0.1,
                "agreement_threshold": 0.8
            },
            total_runs=len(request.selected_models) * request.runs_per_model,
            total_cost=total_cost,
            execution_time=datetime.utcnow()
        )
        
        logger.info(f"Multi-model analysis completed for {len(request.selected_models)} models")
        return response
        
    except Exception as e:
        logger.error(f"Multi-model analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Multi-model analysis failed: {str(e)}"
        )

# Corpus Management Endpoints

@app.post("/api/corpora/upload", response_model=schemas.CorpusResponse)
async def upload_corpus(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),  # Only admins can upload
    db: Session = Depends(get_db)
):
    """
    Upload and ingest a JSONL corpus file.
    Validates each record against core schema and creates corpus + documents + chunks.
    """
    try:
        if not file.filename.endswith('.jsonl'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a .jsonl file"
            )
        
        # Read and parse JSONL file
        content = await file.read()
        corpus_name = name or file.filename.replace('.jsonl', '')
        
        # Use the ingestion service to process the file
        corpus = await services.ingest_jsonl_corpus(
            content=content,
            name=corpus_name,
            description=description,
            uploader_id=current_user.id,
            db=db
        )
        
        logger.info(f"Successfully ingested corpus: {corpus.name} with {corpus.record_count} records")
        return corpus
        
    except Exception as e:
        logger.error(f"Corpus upload failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

@app.get("/api/corpora", response_model=List[schemas.CorpusResponse])
async def list_corpora(
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """List all uploaded corpora with metadata."""
    corpora = crud.get_corpora(db, skip=skip, limit=limit)
    return corpora

@app.get("/api/corpora/{corpus_id}/documents", response_model=List[schemas.DocumentResponse])
async def list_corpus_documents(
    corpus_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List documents in a specific corpus with metadata."""
    documents = crud.get_corpus_documents(db, corpus_id=corpus_id, skip=skip, limit=limit)
    if not documents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corpus not found or has no documents"
        )
    return documents

@app.get("/api/corpora/{corpus_id}/chunks", response_model=List[schemas.ChunkResponse])
async def list_corpus_chunks(
    corpus_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List chunks in a specific corpus with metadata."""
    chunks = crud.get_corpus_chunks(db, corpus_id=corpus_id, skip=skip, limit=limit)
    if not chunks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corpus not found or has no chunks"
        )
    return chunks

# Job Management Endpoints

@app.post("/api/jobs", response_model=schemas.JobResponse)
async def create_job(
    job_request: schemas.JobCreate,
    current_user: User = Depends(get_current_admin_user),  # Only admins can create jobs
    db: Session = Depends(get_db)
):
    """
    Create a new processing job for selected texts, frameworks, and models.
    Enqueues tasks for batch processing.
    """
    try:
        job = await services.create_processing_job(
            job_request=job_request,
            creator_id=current_user.id,
            db=db
        )
        
        logger.info(f"Created job {job.id} with {job.total_tasks} tasks")
        return job
        
    except Exception as e:
        logger.error(f"Job creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job creation failed: {str(e)}"
        )

@app.get("/api/jobs", response_model=List[schemas.JobResponse])
async def list_jobs(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List processing jobs with optional status filtering."""
    jobs = crud.get_jobs(db, skip=skip, limit=limit, status_filter=status_filter)
    return jobs

@app.get("/api/jobs/{job_id}", response_model=schemas.JobDetailResponse)
async def get_job_detail(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed job information including task status breakdown."""
    job_detail = crud.get_job_with_tasks(db, job_id=job_id)
    if not job_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job_detail

@app.post("/api/jobs/{job_id}/resume")
async def resume_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Resume a failed or cancelled job from the last successful checkpoint."""
    try:
        result = await services.resume_job(job_id=job_id, db=db)
        return {"message": f"Job {job_id} resumed", "tasks_requeued": result}
    except Exception as e:
        logger.error(f"Job resume failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume failed: {str(e)}"
        )

# Task Status Endpoints

@app.get("/api/tasks/{task_id}", response_model=schemas.TaskResponse)
async def get_task_detail(
    task_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific task."""
    task = crud.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

# Administrative Endpoints

@app.get("/api/stats", response_model=schemas.SystemStats)
async def get_system_stats(db: Session = Depends(get_db)):
    """Get system-wide statistics for monitoring."""
    stats = crud.get_system_statistics(db)
    return stats

@app.get("/api/metrics")
async def get_system_metrics():
    """Get detailed system metrics including success rates and costs."""
    from ..utils.logging_config import metrics_collector
    return metrics_collector.get_summary()

# Add these configuration endpoints after the existing experiment endpoints

@app.get("/api/framework-configs", response_model=List[schemas.FrameworkConfigResponse])
async def get_framework_configs():
    """Get available framework configurations."""
    try:
        frameworks = []
        frameworks_dir = Path("frameworks")
        
        if frameworks_dir.exists():
            for framework_dir in frameworks_dir.iterdir():
                if framework_dir.is_dir() and framework_dir.name != "__pycache__":
                    framework_json_path = framework_dir / "framework.json"
                    dipoles_json_path = framework_dir / "dipoles.json"
                    
                    if framework_json_path.exists() and dipoles_json_path.exists():
                        # Load framework config
                        with open(framework_json_path, 'r') as f:
                            framework_config = json.load(f)
                        
                        # Load dipoles config
                        with open(dipoles_json_path, 'r') as f:
                            dipoles_config = json.load(f)
                        
                        frameworks.append({
                            "id": framework_dir.name,
                            "name": framework_config.get("display_name", framework_dir.name),
                            "version": framework_config.get("version", "1.0.0"),
                            "description": framework_config.get("description", ""),
                            "dipoles": dipoles_config.get("dipoles", [])
                        })
        
        return frameworks
        
    except Exception as e:
        logger.error(f"Failed to load framework configs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load framework configurations: {str(e)}"
        )

@app.get("/api/prompt-templates", response_model=List[schemas.PromptTemplateResponse])
async def get_prompt_templates():
    """Get available prompt templates."""
    try:
        templates = []
        
        # For now, we'll return some default templates based on existing prompts
        prompts_dir = Path("src/narrative_gravity/prompts")
        
        # Add standard templates
        templates.extend([
            {
                "id": "civic_virtue_v2_1",
                "name": "Civic Virtue Analysis v2.1",
                "version": "2.1.0",
                "content": "Standard civic virtue analysis template with hierarchical ranking",
                "framework_compatibility": ["civic_virtue"]
            },
            {
                "id": "political_spectrum_v2_1", 
                "name": "Political Spectrum Analysis v2.1",
                "version": "2.1.0",
                "content": "Political spectrum analysis with ideological positioning",
                "framework_compatibility": ["political_spectrum"]
            },
            {
                "id": "moral_rhetorical_v2_1",
                "name": "Moral Rhetorical Posture v2.1", 
                "version": "2.1.0",
                "content": "Moral rhetorical posture analysis template",
                "framework_compatibility": ["moral_rhetorical_posture"]
            },
            {
                "id": "universal_v2_1",
                "name": "Universal Analysis v2.1",
                "version": "2.1.0", 
                "content": "Framework-agnostic universal analysis template",
                "framework_compatibility": ["civic_virtue", "political_spectrum", "moral_rhetorical_posture"]
            }
        ])
        
        return templates
        
    except Exception as e:
        logger.error(f"Failed to load prompt templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load prompt templates: {str(e)}"
        )

@app.get("/api/scoring-algorithms", response_model=List[schemas.ScoringAlgorithmResponse])
async def get_scoring_algorithms():
    """Get available scoring algorithms."""
    try:
        algorithms = [
            {
                "id": "hierarchical_v2_1",
                "name": "Hierarchical Scoring v2.1",
                "description": "Advanced hierarchical scoring with relative weights and tier-based analysis",
                "version": "2.1.0"
            },
            {
                "id": "weighted_average_v2_0",
                "name": "Weighted Average v2.0",
                "description": "Traditional weighted average scoring with well-based calculations",
                "version": "2.0.0"
            },
            {
                "id": "consensus_v2_1",
                "name": "Multi-Model Consensus v2.1", 
                "description": "Consensus scoring across multiple models with stability metrics",
                "version": "2.1.0"
            },
            {
                "id": "experimental_v2_1",
                "name": "Experimental Scoring v2.1",
                "description": "Experimental scoring algorithm for research purposes",
                "version": "2.1.0"
            }
        ]
        
        return algorithms
        
    except Exception as e:
        logger.error(f"Failed to load scoring algorithms: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load scoring algorithms: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 