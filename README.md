# ConnectSphere

A full-stack social media web app built for learning and as a portfolio project.

**Status:** Phase 0 – project setup and architecture planning. No app code yet.

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

Run instructions for the frontend, backend, and database are added in Phase 1.

## Known setup issues (Windows)

- **Port 5432 already in use:** a locally installed PostgreSQL service uses it.
  The Docker database is mapped to **5433** instead (see `.env.example`).
- **`pip` fails with "Could not find a suitable TLS CA certificate bundle":**
  the PostgreSQL installer may set `CURL_CA_BUNDLE` to a file that does not exist.
  Remove that system environment variable (see Phase 0 notes) or clear it per session:
  `Remove-Item Env:CURL_CA_BUNDLE`

## Project structure (planned)

```
ConnectSphere/
  frontend/          React app (Phase 1)
  backend/           FastAPI app (Phase 1)
  infrastructure/    Docker and deployment config
  docs/              Architecture and decisions
  docker-compose.yml (Phase 1)
  .env.example
```
