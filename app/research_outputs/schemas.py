from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class ResearchOutputBase(BaseModel):
    school_year_id: str = Field(min_length=1, max_length=9)
    semester_id: str
    research_output_type_id: Literal[
        "Presentation",
        "Publication",
        "Intl Presentation",
        "Intl Publication",
    ]
    research_title: str
    research_type_id: str
    authors_id: str
    college_id: str
    program_department_id: str

    presentation_venue: Optional[str] = None
    conference_name: Optional[str] = None
    presentation_abstract: Optional[str] = None
    presentation_keywords: Optional[str] = None

    doi: Optional[str] = None
    manuscript_link: Optional[str] = None
    journal_publisher: Optional[str] = None
    volume: Optional[str] = None
    issue_number: Optional[str] = None
    page_number: Optional[str] = None
    publication_date: Optional[date] = None
    indexing: Optional[str] = None
    cite_score: Optional[float] = None
    impact_factor: Optional[float] = None

    editorial_board: Optional[str] = None
    journal_website: Optional[str] = None
    apa_format: Optional[str] = None
    publication_abstract: Optional[str] = None
    publication_keywords: Optional[str] = None


class ResearchOutputCreate(ResearchOutputBase):
    pass


class ResearchOutputUpdate(BaseModel):
    school_year_id: Optional[str] = Field(default=None, min_length=1, max_length=9)
    semester_id: Optional[str] = None
    research_output_type_id: Optional[
        Literal[
            "Presentation",
            "Publication",
            "Intl Presentation",
            "Intl Publication",
        ]
    ] = None
    research_title: Optional[str] = None
    research_type_id: Optional[str] = None
    authors_id: Optional[str] = None
    college_id: Optional[str] = None
    program_department_id: Optional[str] = None

    presentation_venue: Optional[str] = None
    conference_name: Optional[str] = None
    presentation_abstract: Optional[str] = None
    presentation_keywords: Optional[str] = None

    doi: Optional[str] = None
    manuscript_link: Optional[str] = None
    journal_publisher: Optional[str] = None
    volume: Optional[str] = None
    issue_number: Optional[str] = None
    page_number: Optional[str] = None
    publication_date: Optional[date] = None
    indexing: Optional[str] = None
    cite_score: Optional[float] = None
    impact_factor: Optional[float] = None

    editorial_board: Optional[str] = None
    journal_website: Optional[str] = None
    apa_format: Optional[str] = None
    publication_abstract: Optional[str] = None
    publication_keywords: Optional[str] = None


class ResearchOutputResponse(ResearchOutputBase):
    paper_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True