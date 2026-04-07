# Data Map & Dictionary

## 1. Data Architecture Philosophy

- **Single Source of Truth:** SQLite/DuckDB. Both relational application tracking and analytical dashboarding query the database.
- **Version Control & Documentation:** Flat `.csv` files stored in the repository. They serve as human-readable audit trails and Git diff targets for Python scripts and manual review in VS Code/Obsidian.

## 2. Table Definitions & Entity Mapping

The database schema mirrors the repository's core CSV structures:

### 2.1 Tracker Tables (Job Applications)

**`Applications_Tracker`** (`Tracker/Applications/Applications_Tracker.csv`)
- **Primary Key**: `Application_ID` (e.g. APP-001)
- **Columns**: `Date_Applied`, `Company`, `Role_Title`, `Role_Type`, `Sector`, `Source`, `Salary_Min`, `Salary_Max`, `Location`, `Work_Mode`, `Status`, `Recruiter_Name`, `Recruiter_Contact`, `Next_Action`, `Outcome`, `Notes`
- **Relations**: Links to `Interview_Log` via `Application_ID` (Implicit).

**`Interview_Log`** (`Tracker/Interview_Experience/Interview_Log.csv`)
- **Primary Key**: `Interview_ID` (e.g. INT-001)
- **Columns**: `Date`, `Company`, `Role_Title`, `Role_Type`, `Round`, `Format`, `Interviewer`, `Duration_mins`, `Status`, `Outcome`, `Detail_File` (Path to MD notes), `Notes`
- **Relations**: `Detail_File` connects directly to Obsidian markdown records.

**`Preferred_Companies`** (`Tracker/Preferred_Companies/Preferred_Companies.csv`)
- **Primary Key**: `Company_ID` (e.g. CO-001)
- **Columns**: `Company`, `Sector`, `Why_Preferred`, `Target_Division`, `Known_Roles`, `Website`, `LinkedIn`, `Status`, `Last_Checked`, `Notes`

### 2.2 Skills & Qualifications

**`Skills_Inventory`** (`Skills/General/Skills_Inventory.csv`)
- **Data Shape**: `Category`, `Skill`, `Proficiency`, `Years_Experience`, `Last_Used`, `Evidence / Where Used`, `Gap_SA`, `Gap_TPM`, `Gap_TBA`, `Priority_to_Improve`, `Notes`

**`Certifications_Tracker`** (`Skills/Certifications/Certifications_Tracker.csv`)
- **Primary Key**: `Cert_ID`
- **Columns**: `Certification Name`, `Issuing Body`, `Date Obtained`, `Credential ID`, `Status`, `Expiry / Renewal`, `URL`, `Relevant Roles`, `Priority`, `Notes`

**`Courses_Tracker`** (`Skills/Courses/Courses_Tracker.csv`)
- **Primary Key**: `Course_ID`
- **Columns**: `Course Name`, `Provider`, `Type`, `Format`, `Completion Date`, `Status`, `URL`, `Certificate (Y/N)`, `Skills Covered`, `Relevant Roles`, `Notes`

**`Publications_Tracker`** (`Skills/Publications/Publications_Tracker.csv`)
- **Primary Key**: `Pub_ID`
- **Columns**: `Title`, `Publication Type`, `Publisher / Journal`, `Date Published`, `Role`, `Co-Authors`, `URL`, `Paper ID`, `Citations`, `Domain`, `Notes`

### 2.3 Goals & Visa Trackers

**`Professional_Tracker`** (`Goals/Professional/Professional_Tracker.csv`)
- **Columns**: `Phase`, `KPI Category`, `Metric / Objective`, `Base State`, `Target Goal`, `Target Salary Impact`, `Timeline Deadline`, `Notes`

**`Visa_Tracker`** (`Goals/UK_Global_Talent_Visa/Visa_Tracker.csv`)
- **Columns**: `Criteria Category`, `Criteria Sub-Type`, `Evidence Description`, `Verifier/Signatory`, `Artifact Source` (Link to MD), `Status`, `Impact / Scale`, `Notes`

### 2.4 External Datasets

**`UK_Gov_Sponsors`** (`Tracker/UK_Gov/2026-04-02_-_Worker_and_Temporary_Worker.csv`)
- **Columns**: `Organisation Name`, `Town/City`, `County`, `Type & Rating`, `Route`
- **Usage**: DuckDB joins the `Applications_Tracker.Company` against `Organisation Name` to verify UK sponsorship capability during analytics queries.

---

## 3. Operations & Loading Logic

- **CSVs to DB Build:** Python initialization script leveraging `duckdb.read_csv()` to hydrate the analytical store during React frontend startup. 
- **DB to CSV Sync:** Upon approval of new data inside the React UI (e.g. CrewAI parsed a new application), the API executes `INSERT INTO` against the DuckDB/SQLite instance, then triggers a pandas/SQL macro to export the tables and overwrite the corresponding `.csv` files automatically.
