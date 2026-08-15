**Job Market Pipeline** is a data engineering project that ingests tech job postings from public ATS feeds, tracks how they change over time, and turns raw job descriptions into queryable data about in-demand skills, roles, and location.

## Getting started
 
Requirements: Docker Desktop, Python 3.11+.
 
```bash
git clone https://github.com/<your-username>/job-market-pipeline.git
cd job-market-pipeline
 
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
 
cp .env.example .env           # fill in local DB credentials if needed
 
docker compose up              # starts Postgres
```
 
In a second terminal, create the schema:
 
```bash
docker exec -it job-market-pipeline-postgres-1 psql -U jobs -d jobs
# paste the contents of sql/schema.sql, then \q
```
 
Run the pipeline:
 
```bash
python -m src/ingestion/main.py
```
 
## Status
 
Early development 