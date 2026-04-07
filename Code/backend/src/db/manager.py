import os
import duckdb
import pandas as pd
import pandera as pa
from src.schemas.csv_schemas import (
    ApplicationCSVSchema,
    InterviewLogCSVSchema,
    PreferredCompanyCSVSchema,
    SkillInventoryCSVSchema,
    CertificationCSVSchema,
    CourseCSVSchema,
    PublicationCSVSchema,
    ProfessionalTrackerCSVSchema,
    VisaTrackerCSVSchema
)

# Map target SQL table names to their Pandera schema constraints
SCHEMA_MAPPING = {
    "Applications_Tracker": ApplicationCSVSchema,
    "Interview_Log": InterviewLogCSVSchema,
    "Preferred_Companies": PreferredCompanyCSVSchema,
    "Skills_Inventory": SkillInventoryCSVSchema,
    "Certifications_Tracker": CertificationCSVSchema,
    "Courses_Tracker": CourseCSVSchema,
    "Publications_Tracker": PublicationCSVSchema,
    "Professional_Tracker": ProfessionalTrackerCSVSchema,
    "Visa_Tracker": VisaTrackerCSVSchema
}


def hydrate_db_from_csv(csv_path: str, table_name: str, conn: duckdb.DuckDBPyConnection) -> bool:
    """
    Parses a CSV file, validates it against the appropriate Pandera schema,
    and inserts/replaces the resulting dataframe in DuckDB.
    """
    if not os.path.exists(csv_path):
        print(f"Warning: CSV file not found at {csv_path}")
        return False
        
    if table_name not in SCHEMA_MAPPING:
        raise ValueError(f"No schema mapping found for table: {table_name}")
        
    schema = SCHEMA_MAPPING[table_name]
    
    try:
        # 1. Read CSV into Pandas DataFrame
        df = pd.read_csv(csv_path)
        
        # 2. Validate DataFrame against Pandera Schema
        validated_df = schema.validate(df)
        
        # 3. Create or Replace DuckDB table from pandas dataframe variable `validated_df`
        conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM validated_df")
        return True
        
    except pa.errors.SchemaError as e:
        print(f"Schema validation failed for {table_name} in {csv_path}: {e}")
        return False
    except Exception as e:
        print(f"Hydration failed: {e}")
        return False


def export_db_to_csv(table_name: str, export_path: str, conn: duckdb.DuckDBPyConnection) -> bool:
    """
    Queries the DuckDB table and overwrites the target CSV,
    maintaining the column shape defined by Pandera schemas.
    """
    try:
        # Check if table exists securely
        tables = [t[0] for t in conn.execute("SHOW TABLES").fetchall()]
        if table_name not in tables:
            print(f"Table {table_name} does not exist in the database.")
            return False
            
        # Extract DuckDB table to Pandas Dataframe
        df = conn.execute(f"SELECT * FROM {table_name}").df()
        
        # Run Dataframe through schema validation one more time to guarantee file integrity
        if table_name in SCHEMA_MAPPING:
             schema = SCHEMA_MAPPING[table_name]
             df = schema.validate(df)
             
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(os.path.abspath(export_path)), exist_ok=True)
        
        # Export
        df.to_csv(export_path, index=False)
        return True
        
    except pa.errors.SchemaError as e:
        print(f"Schema validation failed upon export from {table_name}: {e}")
        return False
    except Exception as e:
        print(f"Export failed: {e}")
        return False


def hydrate_all_directories(base_csv_dir: str, conn: duckdb.DuckDBPyConnection):
    """
    Utility to walk a directory layout and hydrate all detected CSVs automatically.
    Assumes file names match SCHEMA_MAPPING keys exactly (e.g. Applications_Tracker.csv).
    """
    for root, _, files in os.walk(base_csv_dir):
        for file in files:
            if file.endswith(".csv"):
                table_name = os.path.splitext(file)[0]
                if table_name in SCHEMA_MAPPING:
                    csv_path = os.path.join(root, file)
                    hydrate_db_from_csv(csv_path, table_name, conn)
                    print(f"Hydrated table: {table_name}")
