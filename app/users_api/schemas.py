from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    user_id: UUID
    full_name: str
    email: EmailStr
    role_id: UUID | None = None
    role_name: str | None = None
    created_at: datetime


class UpdateUserRoleRequest(BaseModel):
    role_id: UUID