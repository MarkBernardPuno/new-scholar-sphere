from sqlalchemy.orm import Session

from app import models


def populate_defaults(db: Session):
    default_roles = ["admin", "researcher", "reviewer"]
    default_statuses = ["draft", "submitted", "reviewed", "published"]

    created_roles = 0
    created_statuses = 0

    for role_name in default_roles:
        existing = db.query(models.Role).filter(models.Role.role_name == role_name).first()
        if not existing:
            db.add(models.Role(role_name=role_name))
            created_roles += 1

    for status_name in default_statuses:
        existing = db.query(models.Status).filter(models.Status.status_name == status_name).first()
        if not existing:
            db.add(models.Status(status_name=status_name))
            created_statuses += 1

    db.commit()
    return {
        "message": "Defaults populated",
        "created_roles": created_roles,
        "created_statuses": created_statuses,
    }


def email_test(recipient: str):
    return {
        "message": "Email test accepted",
        "recipient": recipient,
        "status": "queued",
    }