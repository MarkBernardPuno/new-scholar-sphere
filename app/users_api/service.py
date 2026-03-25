from fastapi import HTTPException

from database.database import fetch_all, fetch_one


def list_users(db, skip: int, limit: int):
    return fetch_all(
        db,
        """
        SELECT u.id AS user_id, u.full_name, u.email, u.created_at,
               r.id AS role_id, r.name AS role_name
        FROM users u
        LEFT JOIN roles r ON r.id = u.role_id
        ORDER BY u.created_at DESC
        OFFSET %s LIMIT %s
        """,
        (skip, limit),
    )


def get_user(db, user_id: str):
    user = fetch_one(
        db,
        """
        SELECT u.id AS user_id, u.full_name, u.email, u.created_at,
               r.id AS role_id, r.name AS role_name
        FROM users u
        LEFT JOIN roles r ON r.id = u.role_id
        WHERE u.id = %s
        """,
        (user_id,),
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user_role(db, user_id: str, role_id: str):
    user = get_user(db, user_id)
    role = fetch_one(db, "SELECT id, name FROM roles WHERE id = %s", (role_id,))
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    updated = fetch_one(
        db,
        """
        UPDATE users
        SET role_id = %s, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        RETURNING id AS user_id, full_name, email, created_at
        """,
        (role_id, user_id),
    )
    db.commit()
    updated["role_id"] = role["id"]
    updated["role_name"] = role["name"]
    return updated