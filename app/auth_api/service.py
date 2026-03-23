from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.auth import create_access_token, hash_password, verify_password
from app.auth_api.schemas import LoginRequest, TokenResponse


def signup_user(db: Session, full_name: str, email: str, password: str):
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Public signup is always assigned the non-privileged default role.
    default_role = db.query(models.Role).filter(models.Role.role_name == "researcher").first()
    if not default_role:
        default_role = models.Role(role_name="researcher")
        db.add(default_role)
        db.flush()

    user = models.User(
        full_name=full_name,
        email=email,
        password_hash=hash_password(password),
        role_id=default_role.role_id if default_role else None,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, payload: LoginRequest) -> TokenResponse:
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    role_name = user.role.role_name if user.role else None
    token = create_access_token(user.user_id, user.email, role_name)
    return TokenResponse(access_token=token)