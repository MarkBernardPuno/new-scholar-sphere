import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import init_schema
from app.routes import (
    auth,
    integrations,
    lookups,
    presentations,
    research,
    research_evaluations,
    research_outputs,
    users,
)

# Create tables only when explicitly enabled for local/dev convenience.
db_auto_create = os.getenv("DB_AUTO_CREATE", "false").strip().lower() in {"1", "true", "yes", "on"}
if db_auto_create:
    init_schema("database/schema.sql")

# Initialize FastAPI app
app = FastAPI(
    title="Scholar Sphere API",
    description="ScholarSphere backend API with JWT auth, role management, and research data services",
    version="2.0.0"
)

<<<<<<< HEAD
# UNIVERSAL CORS FOR DEVELOPMENT: Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dev/testing
=======
# CORS for browser-based clients (configure via CORS_ALLOW_ORIGINS env var).
raw_origins = os.getenv("CORS_ALLOW_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins or ["*"],
>>>>>>> b96a08110657e89c15f427110eb642caa7c9a340
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(research.router)
app.include_router(research_evaluations.router)
app.include_router(research_outputs.router)
app.include_router(lookups.router)
app.include_router(presentations.router)
app.include_router(integrations.router)


# ======================== ROOT ENDPOINT ========================

@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Scholar Sphere API",
        "version": "2.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
