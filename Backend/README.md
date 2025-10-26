# Backend (Flask API)

This service exposes the REST API, manages the SQLite database via SQLAlchemy, handles JWT authentication, integrates Redis caching, and runs Celery background jobs.

## Features

- JWT auth with access/refresh tokens (single admin via env; users register)
- Role-based access control (admin vs user)
- Parking lots, spots, and reservations
- Auto-allocation to first available spot on booking
- CSV export via Celery and email
- Redis caching for hot endpoints

## Requirements

- Python 3.13
- Redis (for Celery broker/result and cache)

## Setup

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set values (at minimum `ADMIN_EMAIL` and `ADMIN_PASSWORD`). See below.

### Environment Variables

See `config.py` for defaults. Common variables:

- SECRET_KEY
- JWT_SECRET_KEY
- ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NAME
- DATABASE_URL (e.g., `sqlite:///parking_app.db`)
- CELERY_BROKER_URL (e.g., `redis://localhost:6379/0`)
- RESULT_BACKEND (e.g., `redis://localhost:6379/0`)
- REDIS_CACHE_URL (e.g., `redis://localhost:6379/1`)
- MAIL_USERNAME, MAIL_PASSWORD, MAIL_DEFAULT_SENDER (for email)
- BACKEND_URL (e.g., `http://localhost:5000`)
- EXPORT_FOLDER (e.g., `./exports`)

### Database Initialization

```powershell
# Reset and seed sample data
python init_db.py --reset

# Show DB stats anytime
python init_db.py --stats
```

By default SQLite lives at the path in `DATABASE_URL`. Use an absolute path or keep the default.

### Run the API

```powershell
python app.py
# API: http://localhost:5000
# Health: http://localhost:5000/api/health
```

### Start Background Jobs

Ensure Redis is running, then start worker and beat:

```powershell
# From project root or Backend/
celery -A Backend.app.celery worker -l info
celery -A Backend.app.celery beat -l info
```

Scheduled jobs (configured in `jobs/celery_app.py`):
- Daily reminders to inactive users
- Monthly activity report (HTML email)

User-triggered job:
- CSV export of parking history with email notification

## API Documentation

- OpenAPI spec: `../Backend/api_routes.yaml` (browse with Swagger/Redoc viewer)
- Summary of key routes:
  - Auth: `/api/auth/login`, `/api/auth/register`, `/api/auth/refresh`, `/api/auth/logout`, `/api/auth/me`
  - Admin: `/api/admin/users`, `/api/admin/pkl/create`, `/api/admin/pkl/update/<lot_id>`, `/api/admin/pkl/delete/<lot_id>`, `/api/admin/pkl/<lot_id>`, `/api/admin/pkl/list`
  - User: `/api/user/profile`, `/api/user/profile/update`, `/api/user/pkl/list`, `/api/user/pkl/book/<lot_id>`, `/api/user/pkl/release`, `/api/user/pkl/book/list`, `/api/user/export-csv`, `/api/user/export-status/<task_id>`, `/api/user/download-csv/<filename>`

### Auth Notes

- Admin login uses `ADMIN_EMAIL` as the username and `ADMIN_PASSWORD` as the password.
- Users register then login with their username or email + password.
- Include `Authorization: Bearer <access_token>` for protected endpoints.

## Development Tips

- SQL echo is enabled in dev (`SQLALCHEMY_ECHO=True`); turn off in production.
- CORS is enabled for `/api/*`.
- Cache TTLs are defined in `config.py` (`CACHE_EXPIRY`).
