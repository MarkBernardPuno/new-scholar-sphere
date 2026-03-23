from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user
from app.auth_api import service
from app.auth_api.schemas import LoginRequest, SignupRequest, TokenResponse
from app.users_api.schemas import UserResponse
from database.database import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    return service.signup_user(db, payload.full_name, payload.email, payload.password)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return service.login_user(db, payload)


@router.get("/me", response_model=UserResponse)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user
