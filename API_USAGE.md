# Scholar Sphere API Usage Guide

## Running the API (for deployment and frontend use)

### 1. Using Docker Compose (Recommended)

1. Make sure Docker and Docker Compose are installed.
2. In the project root, run:

   ```sh
   docker-compose up --build
   ```

3. The API will be available at: http://localhost:8000
4. The PostgreSQL database will be available at: localhost:5432 (user: postgres, password: admin123, db: NewScholarSphere)

### 2. API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These pages show all available endpoints, request/response formats, and allow you to test the API interactively.

### 3. Example API Usage

- **Base URL:** `http://localhost:8000`
- **Authentication:** Endpoints are public and do not require a token.
- **Headers:**
  - `Content-Type: application/json`

#### Example: Fetch all users

```http
GET /users
````

#### Example: Create a campus

```http
POST /lookups/campuses
Content-Type: application/json

{
  "name": "Main Campus",
  "address": "123 Main St",
  "is_active": true
}
```

---

## For Frontend Developers
- Use the `/docs` endpoint for live API testing and to see all routes.
- All endpoints, request bodies, and responses are documented there.
- All IDs are integer auto-increment values.
- If you need a sample request for a specific endpoint, check Swagger UI or ask the backend team.

---

## Troubleshooting
- If the API or DB fails to start, check Docker logs for errors.
- Ensure ports 8000 (API) and 5432 (DB) are not in use by other applications.
- Environment variables can be changed in `docker-compose.yml` as needed.

---

For further help, contact the backend team or check the README.md.
