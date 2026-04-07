from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import date
from enum import Enum

# --- ENUMS --- 
class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    SCREENING = "Screening"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"
    STALLED = "Stalled"

class WorkMode(str, Enum):
    REMOTE = "Remote"
    HYBRID = "Hybrid"
    ONSITE = "On-site"

class InterviewFormat(str, Enum):
    BEHAVIORAL = "Behavioral"
    TECHNICAL = "Technical"
    SYSTEM_DESIGN = "System Design"
    TAKE_HOME = "Take-home"
    OTHER = "Other"

# --- CORE SCHEMAS ---

class ApplicationRecord(BaseModel):
    """Corresponds to Applications_Tracker.csv"""
    application_id: str = Field(pattern=r"^APP-\d{3}$")
    date_applied: date
    company: str
    role_title: str
    role_type: str
    sector: str
    source: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    location: str
    work_mode: WorkMode
    status: ApplicationStatus = ApplicationStatus.APPLIED
    recruiter_name: Optional[str] = None
    recruiter_contact: Optional[str] = None
    next_action: Optional[str] = None
    outcome: Optional[str] = None
    notes: Optional[str] = None

class InterviewLogRecord(BaseModel):
    """Corresponds to Interview_Log.csv"""
    interview_id: str = Field(pattern=r"^INT-\d{3}$")
    date: date
    company: str
    role_title: str
    role_type: str
    round: int
    format: str  # InterviewFormat but kept loose as string natively
    interviewer: Optional[str] = None
    duration_mins: Optional[int] = None
    status: str
    outcome: Optional[str] = None
    detail_file: Optional[str] = None
    notes: Optional[str] = None

class PreferredCompanyRecord(BaseModel):
    """Corresponds to Preferred_Companies.csv"""
    company_id: str = Field(pattern=r"^CO-\d{3}$")
    company: str
    sector: str
    why_preferred: str
    target_division: Optional[str] = None
    known_roles: Optional[str] = None
    website: Optional[str] = None
    linkedin: Optional[str] = None
    status: str
    last_checked: Optional[date] = None
    notes: Optional[str] = None

# --- SKILLS & QUALIFICATIONS SCHEMAS ---

class SkillInventoryRecord(BaseModel):
    """Corresponds to Skills_Inventory.csv"""
    category: str
    skill: str
    proficiency: int = Field(ge=1, le=5)
    years_experience: float
    last_used: str  
    evidence_where_used: str
    gap_sa: bool = False
    gap_tpm: bool = False
    gap_tba: bool = False
    priority_to_improve: str
    notes: Optional[str] = None

class CertificationRecord(BaseModel):
    """Corresponds to Certifications_Tracker.csv"""
    cert_id: str = Field(pattern=r"^CRT-\d{3}$")
    certification_name: str
    issuing_body: str
    date_obtained: date
    credential_id: Optional[str] = None
    status: str
    expiry_renewal: Optional[str] = None
    url: Optional[str] = None
    relevant_roles: str
    priority: str
    notes: Optional[str] = None

class CourseRecord(BaseModel):
    """Corresponds to Courses_Tracker.csv"""
    course_id: str = Field(pattern=r"^CRS-\d{3}$")
    course_name: str
    provider: str
    type: str
    format: str
    completion_date: Optional[date] = None
    status: str
    url: Optional[str] = None
    certificate_yn: bool = False
    skills_covered: str
    relevant_roles: str
    notes: Optional[str] = None

class PublicationRecord(BaseModel):
    """Corresponds to Publications_Tracker.csv"""
    pub_id: str = Field(pattern=r"^PUB-\d{3}$")
    title: str
    publication_type: str
    publisher_journal: str
    date_published: date
    role: str
    co_authors: Optional[str] = None
    url: Optional[str] = None
    paper_id: Optional[str] = None
    citations: Optional[int] = 0
    domain: str
    notes: Optional[str] = None

# --- GOALS SCHEMAS ---

class ProfessionalTrackerRecord(BaseModel):
    """Corresponds to Professional_Tracker.csv"""
    phase: str
    kpi_category: str
    metric_objective: str
    base_state: str
    target_goal: str
    target_salary_impact: Optional[str] = None
    timeline_deadline: str
    notes: Optional[str] = None

class VisaTrackerRecord(BaseModel):
    """Corresponds to Visa_Tracker.csv"""
    criteria_category: str
    criteria_sub_type: str
    evidence_description: str
    verifier_signatory: str
    artifact_source: str
    status: str
    impact_scale: str
    notes: Optional[str] = None
