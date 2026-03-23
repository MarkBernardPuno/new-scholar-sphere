# Scholar Sphere API Contract

Integration contract for teammates consuming this backend.

## Service Basics

- Base URL: http://localhost:8000
- Swagger: /docs
- ReDoc: /redoc

## Auth Rules

- Bearer token (most protected endpoints):
  - Authorization: Bearer <access_token>
- API key (integration endpoints only):
  - X-API-Key: <api_key>

## Global Request Rules

- Content-Type: application/json for JSON bodies
- Pagination (where supported):
  - skip >= 0
  - 1 <= limit <= 100

## Endpoint Groups

### Root

- GET /
  - Auth: None
  - Success: 200

### Auth

- POST /auth/signup
  - Auth: None
  - Body: full_name, email, password
  - Rules: unknown fields rejected, minimum password length 8
  - Success: 201
- POST /auth/login
  - Auth: None
  - Body: email, password
  - Success: 200 (access_token, token_type)
- GET /auth/me
  - Auth: Bearer
  - Success: 200

### Users

- GET /users/
  - Auth: Bearer
  - Query: skip, limit
  - Success: 200
- GET /users/{user_id}
  - Auth: Bearer
  - Success: 200
- PATCH /users/{user_id}/role
  - Auth: Bearer + admin role
  - Body: role_id
  - Success: 200

### Research

- POST /research/statuses
- GET /research/statuses
- POST /research/keywords
- GET /research/keywords
- POST /research/authors
- GET /research/authors
- POST /research/researchers
- GET /research/researchers
- POST /research/papers
- GET /research/papers
- GET /research/papers/{paper_id}
- PUT /research/papers/{paper_id}
- DELETE /research/papers/{paper_id}
- POST /research/agendas
- GET /research/agendas

Rules:
- All /research/* endpoints require Bearer token.
- List endpoints support global pagination rules.

### Research Outputs

- POST /research-outputs/
- GET /research-outputs/
- GET /research-outputs/{paper_id}
- PUT /research-outputs/{paper_id}
- DELETE /research-outputs/{paper_id}

Rules:
- Auth: Bearer token required for all endpoints.
- List filter query params:
  - school_year_id
  - semester_id
  - output_type
  - research_type_id
  - college_id
  - program_department_id
  - search
  - skip, limit
- research_output_type_id accepted values:
  - Presentation
  - Publication
  - Intl Presentation
  - Intl Publication
- doi is unique when provided.

### Research Evaluations

- POST /research-evaluations/
- GET /research-evaluations/
- GET /research-evaluations/{re_id}
- PUT /research-evaluations/{re_id}
- DELETE /research-evaluations/{re_id}

Rules:
- Auth: Bearer token required for all endpoints.
- campus_id and college_id must reference existing records.
- List filter query params:
  - campus_id
  - college_id
  - department_id
  - school_year_id
  - semester_id
  - search
  - skip, limit

Create/Update payload fields:
- author_id
- campus_id
- college_id
- department_id
- school_year_id
- semester_id
- title_of_research
- authorship_form_link
- evaluation_form
- full_paper
- turnitin_report
- grammarly_report
- journal_conference_info

### Integrations

- POST /integrations/populate-defaults
  - Auth: X-API-Key
- POST /integrations/email/test
  - Auth: X-API-Key
  - Query: recipient

## Environment Contract

- DATABASE_URL
- JWT_SECRET
- JWT_ALGORITHM (default: HS256)
- JWT_EXPIRE_MINUTES (default: 60)
- API_KEY
- CORS_ALLOW_ORIGINS (comma-separated list or *)
- DB_AUTO_CREATE (true/false)

## Team Handoff Steps

1. Share this file and .env.example with teammates.
2. Integrate login first, then attach Bearer token on protected routes.
3. Use X-API-Key only for /integrations/* endpoints.
4. Validate integration with a smoke test: signup, login, auth/me, research-outputs CRUD, research-evaluations CRUD.
