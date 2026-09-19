# Traffic Safety Intelligence Platform

An end-to-end data engineering platform analyzing nationwide fatal motor vehicle crashes using NHTSA FARS data (2020-2024). The system extracts and standardizes over 900,000 records, loads them into a relational MySQL database, and serves analytics through a FastAPI backend and an interactive Streamlit dashboard.

---

## Architecture Overview

```text
NHTSA FARS (2020-2024 Archives)
            |
            v
   Python ETL Pipeline
  (Extract, Clean, Deduplicate)
            |
            v
      MySQL Database
   (crashes, vehicles, people)
            |
            v
      FastAPI Backend
   (REST Endpoints, CORS)
            |
            v
    Streamlit Dashboard
   (Interactive Plotly UI)
```

---

## Tech Stack

- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Database:** MySQL 8.0
- **API Layer:** FastAPI, Uvicorn
- **Frontend:** Streamlit, Plotly
- **DevOps:** Docker, Docker Compose

---

## Key Features

- **Multi-Year Data Pipeline:** Automated ingestion and extraction for five years of federal crash data.
- **Relational Schema:** Normalized database with composite keys (year, st_case, veh_no, per_no) to track crashes, vehicles, and occupants.
- **Analytical Queries:** SQL analytics using CTEs, window functions, and joins to calculate fatality rates and peak risk factors.
- **REST API:** Modular endpoints delivering structured JSON metrics.
- **Interactive Visualization:** Streamlit application providing state rankings, temporal trends, and behavioral breakdowns.
- **Containerized Deployment:** Entire system orchestrated via Docker Compose.

---

## Project Structure

```text
traffic-safety-intelligence/

├── data/
│   ├── raw/
│   └── processed/
├── sql/
│   ├── schema.sql
│   └── queries/
├── src/
│   ├── database/
│   ├── etl/
│   ├── api/
│   └── dashboard/
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Setup and Installation

### Running with Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/Lucas-Gates/traffic-safety-intelligence.git
   cd traffic-safety-intelligence
   ```

2. Start all services:

   ```bash
   docker compose up --build -d
   ```

3. Access applications:

   - **Streamlit Dashboard:** http://localhost:8501
   - **FastAPI Docs:** http://localhost:8000/docs

---

## Data Source

Data is sourced from the National Highway Traffic Safety Administration (NHTSA) Fatality Analysis Reporting System (FARS).