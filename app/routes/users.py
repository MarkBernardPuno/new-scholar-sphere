from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.users_api import service
from app.users_api.schemas import UpdateUserRoleRequest, UserResponse
from database.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])

DbSession = Annotated[object, Depends(get_db)]
SkipParam = Annotated[int, Query(0, ge=0)]
LimitParam = Annotated[int, Query(20, ge=1, le=100)]


@router.get("/collections", response_model=dict[str, list[dict]])
def get_user_collections(
    skip: SkipParam,
    limit: LimitParam,
    db: DbSession,
):
    return {
        "users": service.list_users(db, skip, limit),
    }


@router.get("/", response_model=list[UserResponse])
def list_users(
    skip: SkipParam,
    limit: LimitParam,
    db: DbSession,
):
    return service.list_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: DbSession,
):
    return service.get_user(db, user_id)


@router.patch("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    payload: UpdateUserRoleRequest,
    db: DbSession,
):
    return service.update_user_role(db, user_id, payload.role_id)
