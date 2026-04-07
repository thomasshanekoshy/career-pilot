# System Architecture

This document describes the software architecture of the Career Artifacts System, adhering to the C4 model for visualizing software architecture.

## 1. System Context Diagram (Level 1)

This diagram shows the Career Artifacts System in the context of its user and the external tools it interacts with.

```mermaid
C4Context
  title System Context Diagram for Career Artifacts System

  Person(user, "Professional", "A user managing their career artifacts, tracking applications, and targeting visas.")
  
  System(careerSystem, "Career Artifacts System", "Automates extraction of job descriptions and resumes, updates databases, and provides a review UI.")
  
  System_Ext(ollama, "Ollama Server", "Local LLM inference server (or external APIs via orchestration layer long-term).")
  System_Ext(obsidianVsCode, "VS Code / Obsidian", "Plain text and Markdown editors for manual document manipulation.")
  
  Rel(user, careerSystem, "Interacts with chat interface, reviews updates")
  Rel(user, obsidianVsCode, "Manually edits core markdown files (e.g. Master Resumes)")
  Rel(careerSystem, ollama, "Sends prompts, receives LLM generations")
  Rel(careerSystem, obsidianVsCode, "Modifies/reads files consumed by Editors")
```

---

## 2. Container Diagram (Level 2)

This diagram breaks down the Career Artifacts System into its major executables/containers.

```mermaid
C4Container
  title Container Diagram for Career Artifacts System

  Person(user, "Professional", "Local User")

  System_Boundary(c1, "Career Artifacts Local Environment") {
    
    Container(reactApp, "React Frontend", "React, TypeScript", "Acts as form input, chat interface, and agent communication visibility layer.")
    Container(fastApi, "FastAPI Connector", "Python, FastAPI", "API routing, acts as an entry point for frontend and orchestrates backend processes.")
    Container(crewAI, "Agentic Layer", "Python, CrewAI", "Manages AI agents to parse Job Descriptions, update CSV data, and interface with LLMs.")
    
    ContainerDb(dbTruth, "Source of Truth DB", "SQLite / DuckDB", "Primary database tracking all relational tracker data.")
    ContainerDb(csvLayer, "CSV Documentation Layer", "File System (*.csv)", "Version control and document layer for scripts/manual edits. Mirrors DB.")
    Container(pandoc, "Pandoc Subsystem", "CLI / Python Wrapper", "Ensures consistent and rigid document formatting.")
  }

  System_Ext(ollama, "Ollama / LLMs", "AI Models")
  
  Rel(user, reactApp, "Reviews AI outputs, tracks agent progress (HTTPS)")
  Rel(reactApp, fastApi, "Triggers workflows, fetches database state (REST/JSON)")
  Rel(fastApi, crewAI, "Initiates agent tasks (Internal call)")
  Rel(crewAI, ollama, "Prompts extraction & mapping (REST)")
  Rel(crewAI, pandoc, "Applies rigid formatting to generated Markdown resumes (CLI)")
  Rel(crewAI, dbTruth, "Reads existing data, inserts new application/skills data (SQL)")
  Rel(dbTruth, csvLayer, "Exports/Generates CSVs (or vice-versa) for version control")
```

---

## 3. Component Diagram (Level 3: Backend Logic)

Below is a breakdown of the Agentic flow mediated by FastAPI and CrewAI. 

```mermaid
C4Component
  title Component Diagram: FastAPI & CrewAI Backend

  ContainerDb(dbTruth, "Source of Truth DB", "DuckDB", "Main data store")
  ContainerDb(csvLayer, "CSV Directory", "File Stream", "Version control layer")

  Container_Boundary(backend, "Python Backend") {
    Component(apiRoutes, "API Controllers", "FastAPI", "Endpoints for Triggering Job Match, Fetching state, and Streaming chat.")
    Component(dbManager, "DB Manager", "Python", "Manages the sync between DuckDB <-> CSVs.")
    
    Boundary(b_crew, "CrewAI Orchestrator") {
      Component(jobAgent, "Job Extraction Agent", "CrewAI Agent", "Extracts key data from Job Description text.")
      Component(resumeAgent, "Resume Tailor Agent", "CrewAI Agent", "Modifies specific sections of the Draft Resume (leaves hardcoded sections alone).")
      Component(csvAgent, "Data Entry Agent", "CrewAI Agent", "Maps extracted job info into the database schema formats.")
    }
    
    Component(pandocWrapper, "Formatter", "Python docs", "Calls Pandoc to finalize markdown.")
  }

  Rel(apiRoutes, jobAgent, "Triggers flow")
  Rel(jobAgent, resumeAgent, "Passes extracted skills/requirements")
  Rel(resumeAgent, pandocWrapper, "Passes raw markdown")
  Rel(jobAgent, csvAgent, "Passes JD metadata")
  Rel(csvAgent, dbManager, "Sends structured data")
  Rel(dbManager, dbTruth, "Writes SQL")
  Rel(dbManager, csvLayer, "Dumps to CSV")
```

---

## 4. Architectural Principles

1. **Database as Source of Truth, CSV as Version Control:** 
   The application directly queried for analytics or data integrity checks is SQLite or DuckDB. The CSV files are treated as representations of this database, ensuring clean version control through Git.
2. **Loosely Coupled UI:** 
   FastAPI and React are used for the review layer and visibility. They are NOT required to edit `.md` documents. VS Code and Obsidian exclusively manage `.md` authoring.
3. **Agent Orchestration Abstraction:** 
   CrewAI handles agent logic to safely separate the reasoning layer from the API layer. Moving away from local Ollama to a commercial cloud API only requires swapping the LLM tool within CrewAI.
4. **Formatting Consistency via Pandoc:** 
   LLMs have poor formatting adherence. Pandoc will enforce strict UK ATS-friendly styles onto the markdown outputs generated by the Resume Agent.
