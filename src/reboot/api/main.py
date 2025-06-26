from fastapi import FastAPI
from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    text: str
    framework_id: str
    # In the future, this could include user session, comparison context, etc.

class AnalysisResponse(BaseModel):
    message: str
    # In the future, this will contain the visualization data, coordinates, etc.

app = FastAPI()

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest):
    """
    This endpoint receives a text and a framework choice,
    and will eventually return a geometric narrative analysis.
    """
    # For now, just confirm receipt of the request.
    # This is where the magic will happen.
    
    # 1. (Future) Call LLM Gateway
    # 2. (Future) Call Signature Engine
    # 3. (Future) Call Report Builder (Visualizer)
    
    return AnalysisResponse(
        message=f"Analysis requested for framework '{request.framework_id}'. Content length: {len(request.text)} chars."
    )

@app.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"} 