# Scholar Sphere API

FastAPI backend for authentication, user management, research records, research outputs, and integration hooks.

## Features

- JWT authentication (`/auth/*`)
- Role-aware user operations (`/users/*`)
- Research module CRUD and filters (`/research/*`)
- Research evaluations CRUD and filters (`/research-evaluations/*`)
- Research outputs CRUD and filters (`/research-outputs/*`)
- API key protected integration endpoints (`/integrations/*`)
- PostgreSQL + raw SQL (`psycopg2`)
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
DB_AUTO_CREATE=false
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

- `POST /research/types`
- `GET /research/types`
- `POST /research/output-types`
- `GET /research/output-types`
- `POST /research/authors`
- `GET /research/authors`
- `POST /research/papers`
- `GET /research/papers`
- `GET /research/papers/{paper_id}`
- `PUT /research/papers/{paper_id}`
- `DELETE /research/papers/{paper_id}`

### Research Outputs

- `POST /research-outputs/` (maps to `publications`)
- `GET /research-outputs/`
- `GET /research-outputs/{publication_id}`
- `PUT /research-outputs/{publication_id}`
- `DELETE /research-outputs/{publication_id}`

### Presentations

- `POST /presentations/`
- `GET /presentations/`
- `GET /presentations/{presentation_id}`
- `PUT /presentations/{presentation_id}`
- `DELETE /presentations/{presentation_id}`

### Research Evaluations

- `POST /research-evaluations/`
- `GET /research-evaluations/`
- `GET /research-evaluations/{evaluation_id}`
- `PUT /research-evaluations/{evaluation_id}`
- `DELETE /research-evaluations/{evaluation_id}`

### Lookups

- `POST /lookups/campuses`
- `GET /lookups/campuses`
- `GET /lookups/campuses/{campus_id}`
- `PUT /lookups/campuses/{campus_id}`
- `DELETE /lookups/campuses/{campus_id}`
- `POST /lookups/colleges`
- `GET /lookups/colleges`
- `GET /lookups/colleges/{college_id}`
- `PUT /lookups/colleges/{college_id}`
- `DELETE /lookups/colleges/{college_id}`
- `POST /lookups/departments`
- `GET /lookups/departments`
- `GET /lookups/departments/{department_id}`
- `PUT /lookups/departments/{department_id}`
- `DELETE /lookups/departments/{department_id}`
- `POST /lookups/school-years`
- `GET /lookups/school-years`
- `GET /lookups/school-years/{school_year_id}`
- `PUT /lookups/school-years/{school_year_id}`
- `DELETE /lookups/school-years/{school_year_id}`
- `POST /lookups/semesters`
- `GET /lookups/semesters`
- `GET /lookups/semesters/{semester_id}`
- `PUT /lookups/semesters/{semester_id}`
- `DELETE /lookups/semesters/{semester_id}`

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
    "paper_id": "00000000-0000-0000-0000-000000000000",
    "status": "Pending",
    "document_links": {"turnitin": "https://example.com/turnitin"},
    "authorship_from_link": "https://example.com/authorship",
    "journal_conference_info": {"venue": "Sample Conference"}
  }'
```
```

## Notes

- Tables are created on startup by executing `database/schema.sql` when `DB_AUTO_CREATE=true` (default is false).
- `database/schema.sql` is the source of truth for schema.
- Pagination is supported via `skip` and `limit` on list endpoints.