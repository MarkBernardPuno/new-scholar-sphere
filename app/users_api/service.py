from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models


def list_users(db: Session, skip: int, limit: int):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user_role(db: Session, user_id: int, role_id: int):
    user = get_user(db, user_id)
    role = db.query(models.Role).filter(models.Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user.role_id = role.role_id
    db.commit()
    db.refresh(user)
    return user