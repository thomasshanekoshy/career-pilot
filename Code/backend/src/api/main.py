from fastapi import FastAPI
from src.api.routes import job_submission, approval

app = FastAPI(
    title="Career Artifacts API", 
    version="0.1.0",
    description="Agentic Orchestration and Database Manager API"
)

# Incorporate API Sub-Routers
app.include_router(job_submission.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(approval.router, prefix="/api/approval", tags=["Approvals"])

@app.get("/health")
def health_check():
    """Simple lifecycle check."""
    return {"status": "ok"}
