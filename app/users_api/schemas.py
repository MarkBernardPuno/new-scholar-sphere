from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserRole(BaseModel):
    role_id: int
    role_name: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    role: UserRole | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class UpdateUserRoleRequest(BaseModel):
    role_id: int