# ConnectSphere Architecture

Status: Phase 0 (planning). This document records decisions and is updated each phase.

## 1. Style: modular monolith

One backend process, one database, but the code is split into feature modules
(`auth`, `users`, `follows`, `posts`, ...). Each module owns its router, schemas,
service (business logic), and models. Modules talk to each other through service
functions, not by reaching into each other's tables directly.

Why not microservices: one developer, one deployable, no proven scaling need.
A clean modular monolith can be split later if a module needs it.

```
Browser (React SPA)
   |  HTTPS + JSON (REST), HttpOnly session cookie
   |  WebSocket (Phase 8, messaging)
   v
FastAPI app
   router  -> validates input (Pydantic), checks auth (dependencies)
   service -> business rules, authorization, transactions
   models  -> SQLAlchemy ORM
   v
PostgreSQL            Media storage (local disk in dev, S3-compatible later)
                      Redis (only if needed: rate limits, pub/sub for WebSockets)
```

## 2. Technology decisions

| Area | Choice | Reason |
|---|---|---|
| Frontend build | Vite + React + TypeScript | Fast dev server, type safety |
| Styling | Tailwind CSS v4 | Utility classes, no separate CSS files to manage |
| Routing | React Router | Standard SPA routing |
| Server state | TanStack Query | Caching, refetching, pagination without hand-written state |
| Backend | FastAPI | Async, automatic OpenAPI docs, Pydantic validation |
| ORM | SQLAlchemy 2.x (async) + asyncpg | Typed models, works with WebSockets later. asyncpg instead of psycopg because psycopg's async mode does not run on Windows' default ProactorEventLoop |
| Migrations | Alembic | Versioned, reviewable schema changes |
| Database | PostgreSQL 18 (Docker) | Relational data (follows, likes) fits SQL well; matches local `psql` 18 client |
| Auth | Server-side sessions in Postgres + HttpOnly cookie | Real logout and "log out all devices"; token never readable by JS |
| Passwords | Argon2 via `pwdlib` | Current recommended password hash |
| Media | Storage interface; local disk first | No extra service in dev; swap to S3/R2 for deployment |
| Tests | Pytest, Vitest + RTL, Playwright | Unit/API, component, end-to-end |

## 3. Backend module layout

```
backend/app/modules/<feature>/
  router.py    HTTP endpoints only (thin)
  schemas.py   Pydantic request/response models
  service.py   Business logic and authorization checks
  models.py    SQLAlchemy tables
```

## 4. Local ports

| Service | Host port |
|---|---|
| Frontend (Vite) | 5173 |
| Backend (FastAPI) | 8000 |
| PostgreSQL (Docker) | 5433 (5432 is used by the local PostgreSQL 18 service) |

## 5. Roadmap

| Phase | Scope |
|---|---|
| 0 | Environment check, repo setup, architecture (this document) |
| 1 | Frontend + backend skeleton, Docker Compose Postgres, `/health` endpoint |
| 2 | Database schema, SQLAlchemy models, Alembic migrations |
| 3 | Registration, login, logout, sessions |
| 4 | Profiles, avatars, follow/unfollow |
| 5 | Posts, images, likes, comments |
| 6 | Home feed with cursor pagination |
| 7 | Notifications |
| 8 | Direct messaging over WebSockets |
| 9 | Search, private profiles, blocking, reporting, moderation |
| 10 | Test coverage, security review, deployment, portfolio docs |

## 6. Request flow (Phase 1)

```
HealthStatus.tsx -> useHealth() (TanStack Query) -> apiGet('/health') -> fetch('/api/health')
  -> Vite dev proxy :5173 -> FastAPI :8000 -> health() router -> Depends(get_db) -> AsyncSession
  -> SELECT 1 on PostgreSQL :5433 -> HealthResponse (Pydantic) -> JSON 200 / 503
```

In development the backend runs on the host (fast reload, easy debugging) and only
PostgreSQL runs in Docker. The backend gets its own container in Phase 10.

## 7. Decisions log

- Phase 1: Python deps use `pip` + `venv` with pinned `requirements*.txt`.
- Phase 1: Frontend calls relative `/api` paths; Vite proxies them in dev, so no CORS config.
- Phase 1: TypeScript 6.0 (pinned by the Vite template) instead of 7.0.

## 8. Open decisions

- Redis: add only when rate limiting or multi-process WebSockets need it.
- Deployment target: decide in Phase 10.
