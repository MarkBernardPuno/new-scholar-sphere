from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ResearchEvaluationBase(BaseModel):
    paper_id: UUID
    status: str = "Pending"
    document_links: dict | None = None
    authorship_from_link: str | None = None
    journal_conference_info: dict | None = None


class ResearchEvaluationCreate(ResearchEvaluationBase):
    pass


class ResearchEvaluationUpdate(BaseModel):
    paper_id: UUID | None = None
    status: str | None = None
    document_links: dict | None = None
    authorship_from_link: str | None = None
    journal_conference_info: dict | None = None


class ResearchEvaluationResponse(ResearchEvaluationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
