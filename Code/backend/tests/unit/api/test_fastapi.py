import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    """Verify backend serves traffic properly."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_extract_job_description_validation_failure():
    """TDD: Ensure empty/garbage payloads fail immediately (FR-01)."""
    payload = {"jd_text": "   ", "target_resume_path": ""}
    response = client.post("/api/jobs/extract", json=payload)
    
    assert response.status_code == 422
    assert "Job description text is required" in response.text

def test_extract_job_description_success_mock():
    """TDD: SDD adherence. Response must comply strictly with ApplicationRecord schema."""
    payload = {"jd_text": "Looking for a Senior Python Developer at Google."}
    response = client.post("/api/jobs/extract", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["application_id"] == "APP-MOCK"
    assert data["company"] == "Mock Company"

def test_approve_and_commit_success():
    """TDD: Ensuring frontend UI saves trigger a successful response (FR-08)."""
    valid_record = {
        "application_id": "APP-999",
        "date_applied": "2026-04-06",
        "company": "DeepMind",
        "role_title": "AI Engineer",
        "role_type": "Full-Time",
        "sector": "AI",
        "source": "Direct",
        "location": "London",
        "work_mode": "Hybrid",
        "status": "Applied"
    }
    
    response = client.post("/api/approval/commit", json=valid_record)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "APP-999" in response.json()["message"]
