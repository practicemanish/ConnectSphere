# ConnectSphere

A full-stack social media web app built for learning and as a portfolio project.

**Status:** Phase 1 – frontend and backend skeleton with a working `/api/health` check.

## Tech stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, React Router, TanStack Query
- **Backend:** Python 3.13, FastAPI, SQLAlchemy 2.x, Pydantic, Alembic
- **Database:** PostgreSQL (Docker)
- **Testing:** Pytest, Vitest + React Testing Library, Playwright
- **Dev tooling:** Docker Compose, Git

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design decisions and the roadmap.

## Prerequisites

| Tool | Version used | Check with |
|---|---|---|
| Python | 3.13 | `py -3.13 --version` |
| Node.js | 24.x | `node --version` |
| npm | 11.x | `npm --version` |
| Git | 2.5x | `git --version` |
| Docker Desktop | 29.x (Compose v5) | `docker compose version` |

> On Windows, plain `python` may point to an older version. Use `py -3.13`.

## Setup

```powershell
git clone <repo-url> ConnectSphere
cd ConnectSphere
copy .env.example .env   # then edit .env with your own values
```

Make sure `POSTGRES_PASSWORD` and the password inside `DATABASE_URL` match.

### 1. Database (Docker)

```powershell
docker compose up -d db      # start PostgreSQL on localhost:5433
docker compose ps            # wait for "(healthy)"
```

### 2. Backend (FastAPI)

```powershell
cd backend
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

- Health check: http://localhost:8000/api/health
- API docs (Swagger): http://localhost:8000/docs

### 3. Frontend (React + Vite)

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Vite forwards `/api/*` requests to the backend on port 8000.

## Tests

```powershell
# Backend (needs the Docker database running)
cd backend; .venv\Scripts\python.exe -m pytest -v

# Frontend
cd frontend; npm test
```

## Stopping

```powershell
docker compose stop          # stop the DB, keep data
docker compose down          # remove the container, keep data (volume stays)
# docker compose down -v     # DANGER: also deletes all database data
```

## Known setup issues (Windows)

- **Port 5432 already in use:** a locally installed PostgreSQL service uses it.
  The Docker database is mapped to **5433** instead (see `.env.example`).
- **`pip` fails with "Could not find a suitable TLS CA certificate bundle":**
  the PostgreSQL installer may set `CURL_CA_BUNDLE` to a file that does not exist.
  Remove that system environment variable (see Phase 0 notes) or clear it per session:
  `Remove-Item Env:CURL_CA_BUNDLE`

- **`.venv\Scripts\Activate.ps1` is blocked ("running scripts is disabled"):**
  run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or skip activation and
  call `.venv\Scripts\python.exe -m ...` directly.

## Project structure

```
ConnectSphere/
  backend/
    app/
      core/config.py          settings from .env
      db/session.py           async engine + get_db dependency
      modules/health/         router.py, schemas.py
      main.py                 app factory, routers
    tests/
    requirements*.txt
  frontend/
    src/
      app/                    App, router, query client
      api/client.ts           fetch wrapper
      features/health/        useHealth hook, HealthStatus component + test
      pages/                  route-level components
      test/setup.ts
  docs/ARCHITECTURE.md
  docker-compose.yml
  .env.example
```
