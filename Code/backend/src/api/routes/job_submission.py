from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime

# Import our formal SDD constraint to guarantee the output struct
from src.schemas.data_schemas import ApplicationRecord, ApplicationStatus, WorkMode

router = APIRouter()

class JDSubmissionRequest(BaseModel):
    """Payload expected from the React Frontend UI."""
    jd_text: str
    target_resume_path: Optional[str] = None

@router.post("/extract", response_model=ApplicationRecord)
async def extract_job_description(request: JDSubmissionRequest):
    """
    FR-01/FR-02: Receives raw JD text, triggers the CrewAI Orchestrator.
    Returns the *proposed* ApplicationRecord for user review (does NOT commit to DB).
    """
    if not request.jd_text.strip():
        raise HTTPException(status_code=422, detail="Job description text is required.")
        
    # TODO: Invoke CrewAI Job extraction agent here.
    
    # Stubbing a fallback mock response ensuring it hits the SDD rules
    return ApplicationRecord(
        application_id="APP-MOCK",
        date_applied=datetime.date.today(),
        company="Mock Company",
        role_title="Stubbed Role",
        role_type="Full-Time",
        sector="Tech",
        source="Direct",
        location="Remote",
        work_mode=WorkMode.REMOTE,
        status=ApplicationStatus.APPLIED
    )
