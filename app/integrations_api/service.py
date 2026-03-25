from database.database import fetch_one


def populate_defaults(db):
    created_roles = 0
    created_semesters = 0
    created_research_types = 0
    created_output_types = 0

    for role_name in ["admin", "researcher", "reviewer"]:
        existing = fetch_one(db, "SELECT id FROM roles WHERE name = %s", (role_name,))
        if not existing:
            fetch_one(db, "INSERT INTO roles (name) VALUES (%s) RETURNING id", (role_name,))
            created_roles += 1

    for semester_name in ["1st Semester", "2nd Semester", "Summer"]:
        existing = fetch_one(db, "SELECT id FROM semesters WHERE name = %s", (semester_name,))
        if not existing:
            fetch_one(db, "INSERT INTO semesters (name) VALUES (%s) RETURNING id", (semester_name,))
            created_semesters += 1

    for type_name in ["Basic Research", "Applied Research", "Action Research"]:
        existing = fetch_one(db, "SELECT id FROM research_types WHERE name = %s", (type_name,))
        if not existing:
            fetch_one(db, "INSERT INTO research_types (name) VALUES (%s) RETURNING id", (type_name,))
            created_research_types += 1

    for output_name in ["Presentation", "Publication", "Intl Presentation", "Intl Publication"]:
        existing = fetch_one(db, "SELECT id FROM research_output_types WHERE name = %s", (output_name,))
        if not existing:
            fetch_one(db, "INSERT INTO research_output_types (name) VALUES (%s) RETURNING id", (output_name,))
            created_output_types += 1

    db.commit()
    return {
        "message": "Defaults populated",
        "created_roles": created_roles,
        "created_semesters": created_semesters,
        "created_research_types": created_research_types,
        "created_research_output_types": created_output_types,
    }


def email_test(recipient: str):
    return {
        "message": "Email test accepted",
        "recipient": recipient,
        "status": "queued",
    }