# NL2SQL Explorer

A full-stack application that lets users upload SQL schema or dump files, import them into PostgreSQL, inspect extracted schema metadata, ask questions in natural language, generate SQL using a Hugging Face model, validate it for safety, execute read-only queries, and inspect query history.

## Features

- React + Tailwind frontend
- FastAPI backend
- PostgreSQL metadata and workspace storage
- Hugging Face text-to-SQL integration
- Read-only SQL validation
- Query history and dashboard
- CSV export
- Docker Compose setup

## Project Structure

```text
nl2sql-explorer/
  frontend/
  backend/
  docker-compose.yml
  README.md
```

## Quick Start with Docker

1. Copy environment variables:

```bash
cd backend
cp .env.example .env
cd ..
```

2. Start the stack:

```bash
docker compose up --build
```

3. Open:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

## Local Run

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Main APIs

- `POST /api/v1/upload`
- `GET /api/v1/schema`
- `POST /api/v1/generate-sql`
- `POST /api/v1/execute-query`
- `GET /api/v1/history`
- `GET /api/v1/tables/{database_id}`

## Important Notes

- The current importer uses simple statement splitting for `.sql` files and works best with typical schema and seed dumps.
- The validator blocks destructive SQL and only allows `SELECT` and read-only `WITH` queries.
- Large Hugging Face models may require GPU or a smaller open-source checkpoint for local development.
- For production, add Alembic migrations, background jobs, stronger auth, better SQL parsing, and rate limiting.
