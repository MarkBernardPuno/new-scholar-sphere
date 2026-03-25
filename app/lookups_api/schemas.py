from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CampusBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    address: str | None = None
    is_active: bool = True


class CampusCreate(CampusBase):
    pass


class CampusUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    address: str | None = None
    is_active: bool | None = None


class CampusResponse(CampusBase):
    id: UUID
    created_at: datetime


class CollegeBase(BaseModel):
    campus_id: UUID
    name: str = Field(min_length=1, max_length=255)
    is_active: bool = True


class CollegeCreate(CollegeBase):
    pass


class CollegeUpdate(BaseModel):
    campus_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = None


class CollegeResponse(CollegeBase):
    id: UUID
    created_at: datetime


class DepartmentBase(BaseModel):
    college_id: UUID
    name: str = Field(min_length=1, max_length=255)
    is_active: bool = True


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    college_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = None


class DepartmentResponse(DepartmentBase):
    id: UUID
    created_at: datetime


class SchoolYearBase(BaseModel):
    year_from: int
    year_to: int


class SchoolYearCreate(SchoolYearBase):
    pass


class SchoolYearUpdate(BaseModel):
    year_from: int | None = None
    year_to: int | None = None


class SchoolYearResponse(SchoolYearBase):
    id: UUID


class SemesterBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class SemesterCreate(SemesterBase):
    pass


class SemesterUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)


class SemesterResponse(SemesterBase):
    id: UUID
