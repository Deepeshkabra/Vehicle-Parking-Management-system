# Vehicle Parking Management System

A full-stack parking management application with role-based access (Admin/User), Flask API backend, Vue 3 + Bootstrap frontend, SQLite database, Redis caching, and Celery background jobs.

## Monorepo Layout

```
vehicle-parking-app/
├── Backend/           # Flask API, models, routes, jobs
└── frontend/          # Vue 3 SPA with Bootstrap styling
```

The previous project report has been moved to `docs/PROJECT-REPORT.md`.

## Prerequisites

- Python 3.13 (see `Backend/.python-version`)
- Node 18+ (or 20+) and pnpm (or npm/yarn)
- Redis (for caching and Celery)

## Quick Start (Windows PowerShell)

### 1) Backend API

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env

# Edit .env and set at least ADMIN_EMAIL and ADMIN_PASSWORD

# Initialize database (creates sample data if you don't pass --no-sample)
python init_db.py --reset

# Run API (http://localhost:5000)
python app.py
```

### 2) Background Jobs (Celery + Redis)

Start Redis (one of):

- If you have Docker: `docker run --name redis -p 6379:6379 -d redis:7`
- If installed locally: run the Redis server

Open two terminals from project root:

```powershell
# Terminal A - Celery worker
celery -A Backend.app.celery worker -l info

# Terminal B - Celery beat (scheduled jobs)
celery -A Backend.app.celery beat -l info
```

### 3) Frontend (Vue 3)

```powershell
cd frontend
pnpm install
pnpm dev
```

Open http://localhost:5173 (default Vite port).

## First Run and Login

- User registration: Use the Register page or POST `/api/auth/register`.
- Admin login: Use the credentials set in `.env` (`ADMIN_EMAIL` as username, `ADMIN_PASSWORD` as password) at `/api/auth/login`.

## Health Check

```powershell
curl http://localhost:5000/api/health
```

## Environment Variables

Copy `Backend/.env.example` to `Backend/.env` and set values:

- SECRET_KEY, JWT_SECRET_KEY
- ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NAME
- DATABASE_URL (e.g., `sqlite:///parking_app.db`)
- CELERY_BROKER_URL, RESULT_BACKEND (default Redis URLs)
- MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER (for email features)
- BACKEND_URL (defaults to `http://localhost:5000`)
- EXPORT_FOLDER (CSV exports)

See `Backend/config.py` for defaults and details.

## API Overview

Full OpenAPI spec is in `Backend/api_routes.yaml`. High-level summary below.

### Authentication

- POST `/api/auth/login`
- POST `/api/auth/register`
- POST `/api/auth/refresh`
- POST `/api/auth/logout`
- GET  `/api/auth/me`

### Admin (Bearer token with role=admin)

- GET  `/api/admin/users`
- POST `/api/admin/pkl/create`
- POST `/api/admin/pkl/update/<lot_id>`
- DELETE `/api/admin/pkl/delete/<lot_id>`
- GET  `/api/admin/pkl/<lot_id>`
- GET  `/api/admin/pkl/list`

### User (Bearer token with role=user)

- GET  `/api/user/profile`
- POST `/api/user/profile/update`
- GET  `/api/user/pkl/list`
- POST `/api/user/pkl/book/<lot_id>`
- POST `/api/user/pkl/release`
- GET  `/api/user/pkl/book/list`
- POST `/api/user/export-csv`
- GET  `/api/user/export-status/<task_id>`
- GET  `/api/user/download-csv/<filename>`

## Background Jobs

- Daily Reminders (Celery Beat): notify inactive users and announce new lots
- Monthly Report (Celery Beat): generate and email HTML reports
- CSV Export (User-triggered): async export and email download link

## Caching

Redis caches frequently accessed data (parking lots, user profiles, etc.). See `Backend/utils/cache_manager.py` and `Backend/config.py` for keys and TTLs.

## Troubleshooting

- 401/403 errors: ensure Authorization header uses `Bearer <access_token>` and role matches route.
- CSV export not arriving: check Redis, Celery worker/beat logs, and mail credentials.
- Redis connection errors: verify Redis is running and URLs in `.env` are correct.

## Useful Files

- `Backend/api_routes.yaml` — OpenAPI 3.0 spec for all endpoints
- `Backend/README.md` — Backend-specific setup and ops
- `frontend/README.md` — Frontend-specific setup

