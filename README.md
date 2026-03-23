# Scholar Sphere API

FastAPI backend for authentication, user management, research records, research outputs, and integration hooks.

## Features

- JWT authentication (`/auth/*`)
- Role-aware user operations (`/users/*`)
- Research module CRUD and filters (`/research/*`)
- Research evaluations CRUD and filters (`/research-evaluations/*`)
- Research outputs CRUD and filters (`/research-outputs/*`)
- API key protected integration endpoints (`/integrations/*`)
- PostgreSQL + SQLAlchemy ORM
- Pydantic validation
- Interactive API docs

## Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip

## Setup

1. Clone and enter the project:

```bash
cd /workspaces/new-scholar-sphere
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.example .env
```

Set these values in `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/scholar_db
API_KEY=replace_with_a_secure_random_key
JWT_SECRET=replace_with_a_secure_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
DB_AUTO_CREATE=true
CORS_ALLOW_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

5. Ensure PostgreSQL is running and the database exists.

6. Start the API:

```bash
python -m uvicorn app.main:app --reload
```

## API Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Current Endpoints

### Root

- `GET /`

### Auth

- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`

### Users

- `GET /users/`
- `GET /users/{user_id}`
- `PATCH /users/{user_id}/role` (admin)

### Research

- `POST /research/statuses`
- `GET /research/statuses`
- `POST /research/keywords`
- `GET /research/keywords`
- `POST /research/authors`
- `GET /research/authors`
- `POST /research/researchers`
- `GET /research/researchers`
- `POST /research/papers`
- `GET /research/papers`
- `GET /research/papers/{paper_id}`
- `PUT /research/papers/{paper_id}`
- `DELETE /research/papers/{paper_id}`
- `POST /research/agendas`
- `GET /research/agendas`

### Research Outputs

- `POST /research-outputs/`
- `GET /research-outputs/`
- `GET /research-outputs/{paper_id}`
- `PUT /research-outputs/{paper_id}`
- `DELETE /research-outputs/{paper_id}`

### Research Evaluations

- `POST /research-evaluations/`
- `GET /research-evaluations/`
- `GET /research-evaluations/{re_id}`
- `PUT /research-evaluations/{re_id}`
- `DELETE /research-evaluations/{re_id}`

### Integrations (API key required)

- `POST /integrations/populate-defaults`
- `POST /integrations/email/test`

Use request header:

```http
X-API-Key: <your_api_key>
```

## Quick Smoke Test

Create account:

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test User","email":"test@example.com","password":"Pass123!"}'
```

Login:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Pass123!"}'
```

Use returned bearer token on protected routes:

```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <access_token>"

Create research evaluation (protected):

```bash
curl -X POST http://localhost:8000/research-evaluations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "author_id": "A1,A2",
    "campus_id": 1,
    "college_id": 1,
    "department_id": "CS",
    "school_year_id": "2025-2026",
    "semester_id": "1st",
    "title_of_research": "AI Impact Study",
    "authorship_form_link": "https://example.com/authorship",
    "evaluation_form": "https://example.com/evaluation",
    "full_paper": "https://example.com/full-paper",
    "turnitin_report": "https://example.com/turnitin",
    "grammarly_report": "https://example.com/grammarly",
    "journal_conference_info": "Conference details"
  }'
```
```

## Notes

- Tables are created on startup via SQLAlchemy metadata.
- Table auto-creation can be toggled with `DB_AUTO_CREATE`.
- `database/schema.sql` is kept as reference schema.
- Pagination is supported via `skip` and `limit` on list endpoints.