from fastapi import HTTPException
from psycopg2 import Error

from app.auth import create_access_token, hash_password, verify_password
from app.auth_api.schemas import LoginRequest, TokenResponse
from app.db_errors import raise_db_http_error
from database.database import fetch_one


def signup_user(db, full_name: str, email: str, password: str):
    existing = fetch_one(db, "SELECT id FROM users WHERE email = %s", (email,))
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        default_role = fetch_one(db, "SELECT id, name FROM roles WHERE name = %s", ("researcher",))
        if not default_role:
            default_role = fetch_one(
                db,
                "INSERT INTO roles (name, description) VALUES (%s, %s) RETURNING id, name",
                ("researcher", "Default public signup role"),
            )

        user = fetch_one(
            db,
            """
            INSERT INTO users (department_id, role_id, full_name, email, password_hash)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id AS user_id, full_name, email, role_id, created_at
            """,
            (
                None,
                default_role["id"] if default_role else None,
                full_name,
                email,
                hash_password(password),
            ),
        )
        db.commit()
        return user
    except Error as exc:
        raise_db_http_error(db, exc, conflict_detail="Email already registered")


def login_user(db, payload: LoginRequest) -> TokenResponse:
    user = fetch_one(
        db,
        """
        SELECT u.id AS user_id, u.email, u.password_hash, r.name AS role_name
        FROM users u
        LEFT JOIN roles r ON r.id = u.role_id
        WHERE u.email = %s
        """,
        (payload.email,),
    )
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user["user_id"], user["email"], user.get("role_name"))
    return TokenResponse(access_token=token)