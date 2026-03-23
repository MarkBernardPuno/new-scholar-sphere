from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from database.database import Base


class ResearchEvaluation(Base):
    __tablename__ = "research_evaluations"

    re_id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Text, nullable=False)
    campus_id = Column(Integer, ForeignKey("campuses.campus_id"), nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.college_id"), nullable=False)
    department_id = Column(String(100), nullable=False)
    school_year_id = Column(String(20), nullable=False)
    semester_id = Column(String(50), nullable=False)
    title_of_research = Column(String(255), nullable=False)
    authorship_form_link = Column(Text, nullable=False)
    evaluation_form = Column(Text, nullable=False)
    full_paper = Column(Text, nullable=False)
    turnitin_report = Column(Text, nullable=False)
    grammarly_report = Column(Text, nullable=False)
    journal_conference_info = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
