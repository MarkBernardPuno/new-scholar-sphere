from datetime import datetime

from pydantic import BaseModel, Field


class ResearchEvaluationBase(BaseModel):
    author_id: str = Field(min_length=1)
    campus_id: int
    college_id: int
    department_id: str = Field(min_length=1)
    school_year_id: str = Field(min_length=1)
    semester_id: str = Field(min_length=1)
    title_of_research: str = Field(min_length=1)
    authorship_form_link: str = Field(min_length=1)
    evaluation_form: str = Field(min_length=1)
    full_paper: str = Field(min_length=1)
    turnitin_report: str = Field(min_length=1)
    grammarly_report: str = Field(min_length=1)
    journal_conference_info: str = Field(min_length=1)


class ResearchEvaluationCreate(ResearchEvaluationBase):
    pass


class ResearchEvaluationUpdate(BaseModel):
    author_id: str | None = None
    campus_id: int | None = None
    college_id: int | None = None
    department_id: str | None = None
    school_year_id: str | None = None
    semester_id: str | None = None
    title_of_research: str | None = None
    authorship_form_link: str | None = None
    evaluation_form: str | None = None
    full_paper: str | None = None
    turnitin_report: str | None = None
    grammarly_report: str | None = None
    journal_conference_info: str | None = None


class ResearchEvaluationResponse(ResearchEvaluationBase):
    re_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
