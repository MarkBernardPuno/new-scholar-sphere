from fastapi import HTTPException
from psycopg2 import Error

from app.db_errors import raise_db_http_error
from database.database import fetch_all, fetch_one


# Campuses

def create_campus(db, payload):
    try:
        row = fetch_one(
            db,
            """
            INSERT INTO campuses (name, address, is_active)
            VALUES (%s, %s, %s)
            RETURNING id, name, address, is_active, created_at
            """,
            (payload.name, payload.address, payload.is_active),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc)


def list_campuses(db, skip: int, limit: int):
    return fetch_all(
        db,
        """
        SELECT id, name, address, is_active, created_at
        FROM campuses
        ORDER BY created_at DESC
        OFFSET %s LIMIT %s
        """,
        (skip, limit),
    )


def get_campus(db, campus_id: str):
    row = fetch_one(
        db,
        "SELECT id, name, address, is_active, created_at FROM campuses WHERE id = %s",
        (campus_id,),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Campus not found")
    return row


def update_campus(db, campus_id: str, payload):
    current = get_campus(db, campus_id)
    data = payload.model_dump(exclude_unset=True)

    try:
        row = fetch_one(
            db,
            """
            UPDATE campuses
            SET name = %s,
                address = %s,
                is_active = %s
            WHERE id = %s
            RETURNING id, name, address, is_active, created_at
            """,
            (
                data.get("name", current["name"]),
                data.get("address", current["address"]),
                data.get("is_active", current["is_active"]),
                campus_id,
            ),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc)


def delete_campus(db, campus_id: str):
    try:
        row = fetch_one(db, "DELETE FROM campuses WHERE id = %s RETURNING id", (campus_id,))
        if not row:
            raise HTTPException(status_code=404, detail="Campus not found")
        db.commit()
    except Error as exc:
        raise_db_http_error(db, exc)


# Colleges

def create_college(db, payload):
    campus = fetch_one(db, "SELECT id FROM campuses WHERE id = %s", (str(payload.campus_id),))
    if not campus:
        raise HTTPException(status_code=400, detail="Campus not found")

    try:
        row = fetch_one(
            db,
            """
            INSERT INTO colleges (campus_id, name, is_active)
            VALUES (%s, %s, %s)
            RETURNING id, campus_id, name, is_active, created_at
            """,
            (str(payload.campus_id), payload.name, payload.is_active),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc)


def list_colleges(db, campus_id: str | None, skip: int, limit: int):
    return fetch_all(
        db,
        """
        SELECT id, campus_id, name, is_active, created_at
        FROM colleges
        WHERE (%s IS NULL OR campus_id = %s)
        ORDER BY created_at DESC
        OFFSET %s LIMIT %s
        """,
        (campus_id, campus_id, skip, limit),
    )


def get_college(db, college_id: str):
    row = fetch_one(
        db,
        "SELECT id, campus_id, name, is_active, created_at FROM colleges WHERE id = %s",
        (college_id,),
    )
    if not row:
        raise HTTPException(status_code=404, detail="College not found")
    return row


def update_college(db, college_id: str, payload):
    current = get_college(db, college_id)
    data = payload.model_dump(exclude_unset=True)

    next_campus_id = str(data["campus_id"]) if data.get("campus_id") else str(current["campus_id"])
    campus = fetch_one(db, "SELECT id FROM campuses WHERE id = %s", (next_campus_id,))
    if not campus:
        raise HTTPException(status_code=400, detail="Campus not found")

    try:
        row = fetch_one(
            db,
            """
            UPDATE colleges
            SET campus_id = %s,
                name = %s,
                is_active = %s
            WHERE id = %s
            RETURNING id, campus_id, name, is_active, created_at
            """,
            (
                next_campus_id,
                data.get("name", current["name"]),
                data.get("is_active", current["is_active"]),
                college_id,
            ),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc)


def delete_college(db, college_id: str):
    try:
        row = fetch_one(db, "DELETE FROM colleges WHERE id = %s RETURNING id", (college_id,))
        if not row:
            raise HTTPException(status_code=404, detail="College not found")
        db.commit()
    except Error as exc:
        raise_db_http_error(db, exc)


# Departments

def create_department(db, payload):
    college = fetch_one(db, "SELECT id FROM colleges WHERE id = %s", (str(payload.college_id),))
    if not college:
        raise HTTPException(status_code=400, detail="College not found")

    try:
        row = fetch_one(
            db,
            """
            INSERT INTO departments (college_id, name, is_active)
            VALUES (%s, %s, %s)
            RETURNING id, college_id, name, is_active, created_at
            """,
            (str(payload.college_id), payload.name, payload.is_active),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc)


def list_departments(db, college_id: str | None, skip: int, limit: int):
    return fetch_all(
        db,
        """
        SELECT id, college_id, name, is_active, created_at
        FROM departments
        WHERE (%s IS NULL OR college_id = %s)
        ORDER BY created_at DESC
        OFFSET %s LIMIT %s
        """,
        (college_id, college_id, skip, limit),
    )


def get_department(db, department_id: str):
    row = fetch_one(
        db,
        "SELECT id, college_id, name, is_active, created_at FROM departments WHERE id = %s",
        (department_id,),
    )
    if not row:
        raise HTTPException(status_code=404, detail="Department not found")
    return row


def update_department(db, department_id: str, payload):
    current = get_department(db, department_id)
    data = payload.model_dump(exclude_unset=True)

    next_college_id = str(data["college_id"]) if data.get("college_id") else str(current["college_id"])
    college = fetch_one(db, "SELECT id FROM colleges WHERE id = %s", (next_college_id,))
    if not college:
        raise HTTPException(status_code=400, detail="College not found")

    try:
        row = fetch_one(
            db,
            """
            UPDATE departments
            SET college_id = %s,
                name = %s,
                is_active = %s
            WHERE id = %s
            RETURNING id, college_id, name, is_active, created_at
            """,
            (
                next_college_id,
                data.get("name", current["name"]),
                data.get("is_active", current["is_active"]),
                department_id,
            ),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc)


def delete_department(db, department_id: str):
    try:
        row = fetch_one(db, "DELETE FROM departments WHERE id = %s RETURNING id", (department_id,))
        if not row:
            raise HTTPException(status_code=404, detail="Department not found")
        db.commit()
    except Error as exc:
        raise_db_http_error(db, exc)


# School years

def create_school_year(db, payload):
    try:
        row = fetch_one(
            db,
            """
            INSERT INTO school_years (year_from, year_to)
            VALUES (%s, %s)
            RETURNING id, year_from, year_to
            """,
            (payload.year_from, payload.year_to),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc, conflict_detail="School year already exists")


def list_school_years(db, skip: int, limit: int):
    return fetch_all(
        db,
        """
        SELECT id, year_from, year_to
        FROM school_years
        ORDER BY year_from DESC, year_to DESC
        OFFSET %s LIMIT %s
        """,
        (skip, limit),
    )


def get_school_year(db, school_year_id: str):
    row = fetch_one(db, "SELECT id, year_from, year_to FROM school_years WHERE id = %s", (school_year_id,))
    if not row:
        raise HTTPException(status_code=404, detail="School year not found")
    return row


def update_school_year(db, school_year_id: str, payload):
    current = get_school_year(db, school_year_id)
    data = payload.model_dump(exclude_unset=True)

    try:
        row = fetch_one(
            db,
            """
            UPDATE school_years
            SET year_from = %s,
                year_to = %s
            WHERE id = %s
            RETURNING id, year_from, year_to
            """,
            (
                data.get("year_from", current["year_from"]),
                data.get("year_to", current["year_to"]),
                school_year_id,
            ),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc, conflict_detail="School year already exists")


def delete_school_year(db, school_year_id: str):
    try:
        row = fetch_one(db, "DELETE FROM school_years WHERE id = %s RETURNING id", (school_year_id,))
        if not row:
            raise HTTPException(status_code=404, detail="School year not found")
        db.commit()
    except Error as exc:
        raise_db_http_error(db, exc)


# Semesters

def create_semester(db, payload):
    try:
        row = fetch_one(
            db,
            "INSERT INTO semesters (name) VALUES (%s) RETURNING id, name",
            (payload.name,),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc)


def list_semesters(db, skip: int, limit: int):
    return fetch_all(
        db,
        "SELECT id, name FROM semesters ORDER BY name ASC OFFSET %s LIMIT %s",
        (skip, limit),
    )


def get_semester(db, semester_id: str):
    row = fetch_one(db, "SELECT id, name FROM semesters WHERE id = %s", (semester_id,))
    if not row:
        raise HTTPException(status_code=404, detail="Semester not found")
    return row


def update_semester(db, semester_id: str, payload):
    current = get_semester(db, semester_id)
    data = payload.model_dump(exclude_unset=True)

    try:
        row = fetch_one(
            db,
            """
            UPDATE semesters
            SET name = %s
            WHERE id = %s
            RETURNING id, name
            """,
            (data.get("name", current["name"]), semester_id),
        )
        db.commit()
        return row
    except Error as exc:
        raise_db_http_error(db, exc)


def delete_semester(db, semester_id: str):
    try:
        row = fetch_one(db, "DELETE FROM semesters WHERE id = %s RETURNING id", (semester_id,))
        if not row:
            raise HTTPException(status_code=404, detail="Semester not found")
        db.commit()
    except Error as exc:
        raise_db_http_error(db, exc)
