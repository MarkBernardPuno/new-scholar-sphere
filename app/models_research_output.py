from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String, Text
from sqlalchemy.sql import func

from database.database import Base


class ResearchOutput(Base):
    __tablename__ = "research_outputs"

    paper_id = Column(Integer, primary_key=True, index=True)
    school_year_id = Column(String(9), nullable=False)
    semester_id = Column(String(50), nullable=False)
    research_output_type_id = Column(String(50), nullable=False)
    research_title = Column(Text, nullable=False)
    research_type_id = Column(String(100), nullable=False)
    authors_id = Column(Text, nullable=False)
    college_id = Column(String(100), nullable=False)
    program_department_id = Column(String(100), nullable=False)

    presentation_venue = Column(String(255), nullable=True)
    conference_name = Column(String(255), nullable=True)
    presentation_abstract = Column(Text, nullable=True)
    presentation_keywords = Column(Text, nullable=True)

    doi = Column(String(255), nullable=True, unique=True, index=True)
    manuscript_link = Column(Text, nullable=True)
    journal_publisher = Column(String(255), nullable=True)
    volume = Column(String(50), nullable=True)
    issue_number = Column(String(50), nullable=True)
    page_number = Column(String(50), nullable=True)
    publication_date = Column(Date, nullable=True)
    indexing = Column(String(255), nullable=True)
    cite_score = Column(Numeric(10, 2), nullable=True)
    impact_factor = Column(Numeric(10, 2), nullable=True)

    editorial_board = Column(Text, nullable=True)
    journal_website = Column(Text, nullable=True)
    apa_format = Column(Text, nullable=True)
    publication_abstract = Column(Text, nullable=True)
    publication_keywords = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())