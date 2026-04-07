# End-to-End System Workflow

This document details the operational workflow for managing your career artifacts using the FastAPI, React, and CrewAI local LLM architecture.

## 1. System Initialization

1. **Start Services:** The user starts the Local LLM server (e.g. Ollama via LM Studio or CLI), the FastAPI server backend, and the React frontend.
2. **Database Hydration:** On startup, FastAPI triggers a script that parses all `.csv` files inside the `career-artifacts` directory (e.g., `Applications_Tracker.csv`, `Skills_Inventory.csv`) into the DuckDB / SQLite primary data store.
   - *Result*: The React frontend now displays the accurate, up-to-date state of the SQL tables.

## 2. Automated Application & Resume Parsing Workflow

When you want to apply for a new job, follow this agentic workflow:

### Step 1: Input
- Open the React Frontend.
- Paste the raw text of the **Job Description** (or upload a PDF).
- Provide the **Target Base Resume** (from `Resume/General/_Template/`) for the targeted role constraint.
- Click **"Process Application"**.

### Step 2: Agentic Processing (CrewAI + Ollama)
- The **FastAPI Connector** receives the payload and triggers the CrewAI Orchestrator.
- **Agent 1 (Job Analyst):** Reads the Job Description and extracts metadata (Role Title, Salary, Key Requirements, Location, Sector).
- **Agent 2 (Resume Tailor):** Reads the extracted JD requirements and the Target Base Resume. It assesses gaps and edits *only* allowable bullet points (leaving hardcoded dates, degrees, etc., untouched).
- **Agent 3 (Data Structurer):** Formats the JD metadata into a JSON struct matching the `Applications_Tracker` schema.

### Step 3: Formal Formatting
- The edited Markdown output from Agent 2 is passed to **Pandoc** to enforce UK ATS-style configurations and styling (ignoring LLM hallucinated markdown styles).

### Step 4: User Review & Commit
- The **React Frontend** displays the proposed DB insertions alongside a diff of the Resume changes.
- The User reviews the data.
- If everything is accurate, the user clicks **"Approve & Commit"**.

### Step 5: Database & CSV Sync
- FastAPI inserts the structured JSON data as a new row into the DuckDB / SQLite `Applications_Tracker` table.
- A background process automatically overwrites the physical `Applications_Tracker.csv` file so that VS Code and Git detect the change immediately.
- The new tailored resume is saved to `Resume/Current_Applications/[Job_Title]/Draft_Resume.md`.

## 3. Manual Workflow & Markdown Editing

Because the system correctly treats standard files as the documentation layer:
- The user can bypass the UI entirely and manually edit `Applications_Tracker.csv` or their `Draft_Resume.md` inside **VS Code** or **Obsidian**.
- On the next API boot or sync, the system will detect the CSV edits and re-hydrate the main SQL database, maintaining total system synchrony.
