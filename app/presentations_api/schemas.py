from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class PresentationBase(BaseModel):
    paper_id: UUID
    venue: str | None = None
    conference_name: str | None = None
    presentation_date: date | None = None


class PresentationCreate(PresentationBase):
    pass


class PresentationUpdate(BaseModel):
    paper_id: UUID | None = None
    venue: str | None = None
    conference_name: str | None = None
    presentation_date: date | None = None


class PresentationResponse(PresentationBase):
    id: UUID
    created_at: datetime
