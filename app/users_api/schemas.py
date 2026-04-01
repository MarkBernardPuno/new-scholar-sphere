from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    role_id: int | None = None
    role_name: str | None = None
    created_at: datetime


class UpdateUserRoleRequest(BaseModel):
    role_id: int