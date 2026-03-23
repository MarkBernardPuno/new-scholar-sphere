from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class StatusBase(BaseModel):
    status_name: str
    description: str | None = None


class StatusCreate(StatusBase):
    pass


class StatusResponse(StatusBase):
    status_id: int

    class Config:
        from_attributes = True


class KeywordBase(BaseModel):
    keyword_name: str


class KeywordCreate(KeywordBase):
    pass


class KeywordResponse(KeywordBase):
    keyword_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    full_name: str
    email: EmailStr | None = None
    affiliation: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorResponse(AuthorBase):
    author_id: int

    class Config:
        from_attributes = True


class ResearcherBase(BaseModel):
    full_name: str
    email: EmailStr
    department_id: int | None = None
    campus_id: int | None = None
    status_id: int | None = None


class ResearcherCreate(ResearcherBase):
    pass


class ResearcherResponse(ResearcherBase):
    researcher_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaperBase(BaseModel):
    title: str
    abstract: str | None = None
    published_at: datetime | None = None
    department_id: int | None = None
    campus_id: int | None = None
    status_id: int | None = None


class PaperCreate(PaperBase):
    author_ids: list[int] = Field(default_factory=list)
    keyword_ids: list[int] = Field(default_factory=list)


class PaperUpdate(BaseModel):
    title: str | None = None
    abstract: str | None = None
    published_at: datetime | None = None
    department_id: int | None = None
    campus_id: int | None = None
    status_id: int | None = None
    author_ids: list[int] | None = None
    keyword_ids: list[int] | None = None


class PaperResponse(PaperBase):
    paper_id: int
    researcher_id: int | None = None
    created_at: datetime
    authors: list[AuthorResponse] = Field(default_factory=list)
    keywords: list[KeywordResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class AgendaBase(BaseModel):
    title: str
    details: str | None = None
    due_date: datetime | None = None
    status_id: int | None = None


class AgendaCreate(AgendaBase):
    pass


class AgendaResponse(AgendaBase):
    agenda_id: int
    created_by: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True