import os
import pytest
import duckdb
import pandas as pd
from src.db.manager import hydrate_db_from_csv, export_db_to_csv, hydrate_all_directories

@pytest.fixture
def memory_db():
    """Provides a fresh, isolated in-memory DuckDB instance per test."""
    conn = duckdb.connect(':memory:')
    yield conn
    conn.close()

@pytest.fixture
def valid_applications_csv(tmp_path):
    """Creates a temporary valid CSV aligning with Pandera schema mapping."""
    df = pd.DataFrame({
        "Application_ID": ["APP-001"],
        "Date_Applied": ["2026-04-06"],
        "Company": ["OpenAI"],
        "Role_Title": ["Research Engineer"],
        "Role_Type": ["Full-Time"],
        "Sector": ["AI"],
        "Source": ["LinkedIn"],
        "Salary_Min": [200000.0],
        "Salary_Max": [250000.0],
        "Location": ["San Francisco"],
        "Work_Mode": ["Hybrid"],
        "Status": ["Applied"],
        "Recruiter_Name": ["John Doe"],
        "Recruiter_Contact": ["john@example.com"],
        "Next_Action": ["Wait"],
        "Outcome": [""],
        "Notes": ["Exciting role!"]
    })
    
    # Save the dataframe as CSV to the temp directory
    csv_file = tmp_path / "Applications_Tracker.csv"
    df.to_csv(csv_file, index=False)
    return str(csv_file)

def test_hydrate_db_from_csv_success(memory_db, valid_applications_csv):
    """Tests the round-trip read of CSV -> Pandera validation -> DuckDB storage."""
    result = hydrate_db_from_csv(valid_applications_csv, "Applications_Tracker", memory_db)
    assert result is True
    
    # Query DuckDB directly to verify injection
    df_out = memory_db.execute("SELECT * FROM Applications_Tracker").df()
    assert len(df_out) == 1
    assert df_out.iloc[0]["Application_ID"] == "APP-001"

def test_hydrate_db_from_csv_invalid_schema_fails(memory_db, tmp_path):
    """Tests that incorrect Data schemas get blocked by Pandera."""
    df = pd.DataFrame({
        "Application_ID": ["APP-BAD"], # Fails regex matching APP-\d{3}
        "Date_Applied": ["2026-04-06"],
        "Company": ["OpenAI"],
        "Role_Title": ["Research Engineer"]
        # Missing other necessary columns
    })
    csv_file = tmp_path / "Bad_Tracker.csv"
    df.to_csv(csv_file, index=False)
    
    result = hydrate_db_from_csv(str(csv_file), "Applications_Tracker", memory_db)
    
    # Hydration MUST fail securely, avoiding DuckDB corruption
    assert result is False
    with pytest.raises(duckdb.CatalogException):
        memory_db.execute("SELECT * FROM Applications_Tracker")

def test_export_db_to_csv_success(memory_db, valid_applications_csv, tmp_path):
    """Tests db to CSV export preserving correct data shapes and headers."""
    # Setup initial valid state
    hydrate_db_from_csv(valid_applications_csv, "Applications_Tracker", memory_db)
    
    # Extract to new file location
    export_file = tmp_path / "export" / "Exported_Tracker.csv"
    result = export_db_to_csv("Applications_Tracker", str(export_file), memory_db)
    
    assert result is True
    assert os.path.exists(export_file)
    
    # Validate final CSV integrity via Pandas read
    df_exported = pd.read_csv(export_file)
    assert len(df_exported) == 1
    assert df_exported.iloc[0]["Application_ID"] == "APP-001"
