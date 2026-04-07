# Functional Requirements Document (FRD)

## 1. Overview
This document specifies the functional requirements for the Career Artifacts tracking subsystem. The system automates the processing of job descriptions and resumes, handles metadata tracking via databases and CSVs, and provides a review interface.

## 2. Core Functional Requirements

### 2.1 Agentic Data Extraction & Job Processing (CrewAI + Ollama)
- **FR-01: Job Description Parsing:** The system must accept unstructured job description text or files and extract critical fields (Role Name, Company, Salary, Location, Required Skills).
- **FR-02: Resume Context Evaluation:** The system must evaluate a provided base Resume against the parsed Job Description to identify gaps and suggest tailored bullet points.
- **FR-03: Partial Resume Update Restrictions:** The agentic layer MUST NOT overwrite or hallucinate core factual data (such as employment dates and university degrees). Certain sections of the `.md` files must remain strictly hardcoded or locked.

### 2.2 Data Synchronization & Persistence (DuckDB / SQLite / CSV)
- **FR-04: Single Source of Truth Compilation:** The system's actual data state must be reliably maintained in a relational database (SQLite) or analytical database (DuckDB).
- **FR-05: CSV as Version Control:** The system must generate plain text `.csv` files from the database state to act as a viewable, human-readable documentation layer.
- **FR-06: Two-Way Data Sync (Optional Base):** The system should provide a mechanism to rebuild the DuckDB/SQLite database solely from the CSV files, allowing manual edits in VS Code to be ingested back into the database.

### 2.3 Document Formatting (Pandoc)
- **FR-07: Strict Formatting Enforcement:** All `.md` to `.pdf` or `.docx` conversions must be managed via standard tools (e.g., Pandoc) to ensure the resume meets UK ATS-compliant styling. LLMs must NOT control visual styling.

### 2.4 User Interface & Review (React + FastAPI)
- **FR-08: React Review Mechanism:** The React frontend must provide a view detailing the LLM's proposed updates to the Database and the Resume. The user must actively hit "Approve" before data is committed to DuckDB/CSVs.
- **FR-09: Agent Visibility Layer:** The frontend must provide a "chat interface" or log console to display real-time statuses and thinking paths of the CrewAI agents.
- **FR-10: Form Data Entry:** The frontend must provide structured forms to manually execute database updates without using the AI.

## 3. Out of Scope functionalities
- **Markdown Editing:** The React application is NOT responsible for editing `.md` documents. The user will rely on VS Code and Obsidian for editing documents. React is strictly for AI visibility and database UI.
- **Direct Submission:** The system is not responsible for automatically sending emails or directly applying to jobs on company portals.
