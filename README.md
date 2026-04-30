# AI-Powered HCP CRM Interaction System

## Overview

This project is an AI-powered Pharmaceutical CRM Assistant built using:

- FastAPI
- React + Redux
- LangGraph
- Groq LLM
- Docker
- PostgreSQL

The system allows pharmaceutical sales representatives to:

- Log HCP (Healthcare Professional) interactions
- Extract structured CRM data using AI
- Normalize natural language dates and times
- Validate compliance risks
- Generate follow-up tasks
- Generate HCP recommendations
- Maintain interaction state across edits

---

# Features

## AI CRM Extraction

Users can type natural language such as:

```text
Met Dr. Sharma today. Discussed GlucoX efficacy.
```

The system extracts:

- HCP Name
- Product
- Sentiment
- Summary
- Date
- Time
- Follow-up information

---

## Natural Language Date Parsing

Supports:

```text
last saturday
next monday
after 7 days
after 3 months
tomorrow
12th april 2026
14/08/2025
```

Dates are normalized into:

```text
YYYY-MM-DD
```

The backend uses browser time as the reference datetime.

---

## Compliance Validation

Detects risky pharmaceutical claims such as:

- guaranteed cure
- 100% effective
- cure

Returns:

```json
{
  "status": "warning"
}
```

---

## Recommendation Engine

Suggestions are generated based on sentiment.

### Positive

- Schedule another meeting
- Share efficacy studies

### Neutral

- Send educational materials

### Negative

- Escalate to senior sales manager

---

## Follow-Up Scheduler

Automatically generates CRM follow-up tasks.

---

# Project Architecture

```text
Frontend (React + Redux)
        ↓
FastAPI Backend
        ↓
LangGraph Workflow
        ↓
Tools Layer
        ↓
Groq LLM + Date Normalization
        ↓
Structured CRM Output
```

---

# LangGraph Workflow

```text
log_interaction
      ↓
compliance_check
      ↓
recommendations
      ↓
followup_scheduler
      ↓
finalize
```

---

# Tech Stack

## Frontend

- React
- Redux Toolkit
- Tailwind CSS
- Axios
- Lucide React

## Backend

- FastAPI
- LangGraph
- LangChain
- Groq API
- SQLAlchemy
- PostgreSQL
- dateparser

## DevOps

- Docker
- Docker Compose

---

# Folder Structure

```text
project/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── tools.py
│   │   ├── agent.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   └── services/
│   │
│   ├── package.json
│   └── Dockerfile
│
└── docker-compose.yml
```

---

# Environment Variables

Create a `.env` file inside backend:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Backend Requirements

```txt
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
langgraph
langchain
langchain-core
groq
pydantic
python-multipart
dateparser>=1.2.0
```

---

# Running the Project with Docker

## 1. Clone the Repository

```bash
git clone <repo-url>
cd <project-folder>
```

---

## 2. Start Docker Containers

```bash
docker compose up --build
```

---

## 3. Access Applications

### Frontend

```text
http://localhost:5173
```

### Backend API

```text
http://localhost:8000
```

### Swagger Docs

```text
http://localhost:8000/docs
```

---

# Docker Commands

## Start Containers

```bash
docker compose up
```

## Rebuild Containers

```bash
docker compose up --build
```

## Stop Containers

```bash
docker compose down
```

## Restart Backend

```bash
docker compose restart backend
```

---

# Example API Request

## POST `/api/chat`

```json
{
  "message": "Met Dr. Sharma today. Discussed GlucoX efficacy.",
  "existing_data": {},
  "current_datetime": "2026-04-29T19:06:15.866Z"
}
```

---

# Example Response

```json
{
  "interaction": {
    "hcp_name": "Dr. Sharma",
    "product": "GlucoX",
    "sentiment": "neutral",
    "summary": "Discussed GlucoX efficacy",
    "date": "2026-04-29",
    "time": "12:45"
  },
  "compliance": {
    "status": "approved",
    "violations": []
  },
  "recommendations": [
    "Send educational materials"
  ],
  "followups": [
    {
      "task": "Schedule follow-up meeting",
      "priority": "high"
    }
  ]
}
```

---

# AI Workflow Explanation

## `generate_summary()`

Uses Groq LLM to:

- extract doctor names
- extract products
- detect sentiment
- detect summaries
- understand corrections
- preserve previous CRM values

---

## `normalize_date()`

Converts natural language dates into standardized format.

Uses:

- `search_dates()`
- browser current datetime
- automatic past/future detection

---

## `safe_merge()`

Prevents accidental overwriting of existing CRM data.

---

## `compliance_validation_tool()`

Checks risky pharmaceutical statements.

---

## `hcp_recommendation_tool()`

Generates sales recommendations based on HCP sentiment.

---

## `followup_scheduler_tool()`

Creates structured follow-up tasks.

---

# Future Improvements

- Authentication
- Multi-user CRM
- Persistent database storage
- Vector memory
- RAG integration
- Calendar integration
- Email reminders
- Analytics dashboard
- Voice interaction logging
- Real-time streaming responses

---

# Author

AI-Powered HCP CRM Assistant using LangGraph + FastAPI + React + Groq.


set backend/.env 

DATABASE_URL=postgresql://postgres:postgres@db:5432/hcpcrm
GROQ_API_KEY=
