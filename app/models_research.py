from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base


paper_authors = Table(
    "paper_authors",
    Base.metadata,
    Column("paper_id", Integer, ForeignKey("papers.paper_id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.author_id"), primary_key=True),
)


paper_keywords = Table(
    "paper_keywords",
    Base.metadata,
    Column("paper_id", Integer, ForeignKey("papers.paper_id"), primary_key=True),
    Column("keyword_id", Integer, ForeignKey("keywords.keyword_id"), primary_key=True),
)


class Status(Base):
    __tablename__ = "statuses"

    status_id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    researchers = relationship("Researcher", back_populates="status")
    papers = relationship("Paper", back_populates="status")
    agendas = relationship("Agenda", back_populates="status")


class Researcher(Base):
    __tablename__ = "researchers"

    researcher_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    department_id = Column(Integer, ForeignKey("departments.dept_id"), nullable=True)
    campus_id = Column(Integer, ForeignKey("campuses.campus_id"), nullable=True)
    status_id = Column(Integer, ForeignKey("statuses.status_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    status = relationship("Status", back_populates="researchers")


class Author(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=True, index=True)
    affiliation = Column(String(255), nullable=True)

    papers = relationship("Paper", secondary=paper_authors, back_populates="authors")


class Keyword(Base):
    __tablename__ = "keywords"

    keyword_id = Column(Integer, primary_key=True, index=True)
    keyword_name = Column(String(100), unique=True, nullable=False, index=True)

    papers = relationship("Paper", secondary=paper_keywords, back_populates="keywords")


class Paper(Base):
    __tablename__ = "papers"

    paper_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    abstract = Column(Text, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.dept_id"), nullable=True)
    campus_id = Column(Integer, ForeignKey("campuses.campus_id"), nullable=True)
    status_id = Column(Integer, ForeignKey("statuses.status_id"), nullable=True)
    researcher_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    status = relationship("Status", back_populates="papers")
    researcher = relationship("User", back_populates="papers")
    authors = relationship("Author", secondary=paper_authors, back_populates="papers")
    keywords = relationship("Keyword", secondary=paper_keywords, back_populates="papers")


class Agenda(Base):
    __tablename__ = "agendas"

    agenda_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    status_id = Column(Integer, ForeignKey("statuses.status_id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    status = relationship("Status", back_populates="agendas")
    creator = relationship("User", back_populates="agendas")