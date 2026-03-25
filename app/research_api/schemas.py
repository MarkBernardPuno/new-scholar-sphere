from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ResearchTypeCreate(BaseModel):
    name: str
    description: str | None = None


class ResearchTypeResponse(ResearchTypeCreate):
    id: UUID


class ResearchOutputTypeCreate(BaseModel):
    name: str
    description: str | None = None


class ResearchOutputTypeResponse(ResearchOutputTypeCreate):
    id: UUID


class AuthorCreate(BaseModel):
    user_id: UUID | None = None
    department_id: UUID | None = None
    first_name: str
    middle_name: str | None = None
    last_name: str


class AuthorResponse(AuthorCreate):
    id: UUID
    created_at: datetime


class ResearchAuthorLink(BaseModel):
    author_id: UUID
    is_primary_author: bool = False
    author_order: int | None = None


class PaperCreate(BaseModel):
    research_type_id: UUID | None = None
    research_output_type_id: UUID | None = None
    school_year_id: UUID | None = None
    semester_id: UUID | None = None
    title: str
    abstract: str | None = None
    keywords: list[str] = Field(default_factory=list)
    is_active: bool = True
    authors: list[ResearchAuthorLink] = Field(default_factory=list)


class PaperUpdate(BaseModel):
    research_type_id: UUID | None = None
    research_output_type_id: UUID | None = None
    school_year_id: UUID | None = None
    semester_id: UUID | None = None
    title: str | None = None
    abstract: str | None = None
    keywords: list[str] | None = None
    is_active: bool | None = None
    authors: list[ResearchAuthorLink] | None = None


class PaperResponse(BaseModel):
    id: UUID
    research_type_id: UUID | None = None
    research_output_type_id: UUID | None = None
    school_year_id: UUID | None = None
    semester_id: UUID | None = None
    title: str
    abstract: str | None = None
    keywords: list[str] = Field(default_factory=list)
    is_active: bool
    created_at: datetime
    updated_at: datetime
    author_ids: list[UUID] = Field(default_factory=list)
