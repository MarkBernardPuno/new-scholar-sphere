from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.research_api.schemas import AgendaCreate, PaperCreate, PaperUpdate


def create_status(db: Session, status_name: str, description: str | None):
    existing = db.query(models.Status).filter(models.Status.status_name == status_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Status already exists")
    record = models.Status(status_name=status_name, description=description)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_statuses(db: Session):
    return db.query(models.Status).all()


def create_keyword(db: Session, keyword_name: str):
    existing = db.query(models.Keyword).filter(models.Keyword.keyword_name == keyword_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Keyword already exists")
    record = models.Keyword(keyword_name=keyword_name)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_keywords(db: Session):
    return db.query(models.Keyword).all()


def create_author(db: Session, payload):
    record = models.Author(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_authors(db: Session, skip: int, limit: int):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_researcher(db: Session, payload):
    existing = db.query(models.Researcher).filter(models.Researcher.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Researcher email already exists")
    record = models.Researcher(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_researchers(
    db: Session,
    status_id: int | None,
    department_id: int | None,
    campus_id: int | None,
    skip: int,
    limit: int,
):
    query = db.query(models.Researcher)
    if status_id is not None:
        query = query.filter(models.Researcher.status_id == status_id)
    if department_id is not None:
        query = query.filter(models.Researcher.department_id == department_id)
    if campus_id is not None:
        query = query.filter(models.Researcher.campus_id == campus_id)
    return query.offset(skip).limit(limit).all()


def create_paper(db: Session, payload: PaperCreate, user_id: int):
    paper = models.Paper(
        title=payload.title,
        abstract=payload.abstract,
        published_at=payload.published_at,
        department_id=payload.department_id,
        campus_id=payload.campus_id,
        status_id=payload.status_id,
        researcher_id=user_id,
    )

    if payload.author_ids:
        authors = db.query(models.Author).filter(models.Author.author_id.in_(payload.author_ids)).all()
        if len(authors) != len(set(payload.author_ids)):
            raise HTTPException(status_code=400, detail="One or more authors were not found")
        paper.authors = authors

    if payload.keyword_ids:
        keywords = db.query(models.Keyword).filter(models.Keyword.keyword_id.in_(payload.keyword_ids)).all()
        if len(keywords) != len(set(payload.keyword_ids)):
            raise HTTPException(status_code=400, detail="One or more keywords were not found")
        paper.keywords = keywords

    db.add(paper)
    db.commit()
    db.refresh(paper)
    return paper


def list_papers(
    db: Session,
    q: str | None,
    status_id: int | None,
    department_id: int | None,
    campus_id: int | None,
    keyword: str | None,
    skip: int,
    limit: int,
):
    query = db.query(models.Paper)
    if q:
        query = query.filter(models.Paper.title.ilike(f"%{q}%"))
    if status_id is not None:
        query = query.filter(models.Paper.status_id == status_id)
    if department_id is not None:
        query = query.filter(models.Paper.department_id == department_id)
    if campus_id is not None:
        query = query.filter(models.Paper.campus_id == campus_id)
    if keyword:
        query = query.join(models.Paper.keywords).filter(models.Keyword.keyword_name.ilike(f"%{keyword}%"))
    return query.distinct().offset(skip).limit(limit).all()


def get_paper(db: Session, paper_id: int):
    paper = db.query(models.Paper).filter(models.Paper.paper_id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper


def update_paper(db: Session, paper_id: int, payload: PaperUpdate):
    paper = get_paper(db, paper_id)
    update_data = payload.model_dump(exclude_unset=True, exclude={"author_ids", "keyword_ids"})
    for key, value in update_data.items():
        setattr(paper, key, value)

    if payload.author_ids is not None:
        authors = db.query(models.Author).filter(models.Author.author_id.in_(payload.author_ids)).all() if payload.author_ids else []
        if payload.author_ids and len(authors) != len(set(payload.author_ids)):
            raise HTTPException(status_code=400, detail="One or more authors were not found")
        paper.authors = authors

    if payload.keyword_ids is not None:
        keywords = db.query(models.Keyword).filter(models.Keyword.keyword_id.in_(payload.keyword_ids)).all() if payload.keyword_ids else []
        if payload.keyword_ids and len(keywords) != len(set(payload.keyword_ids)):
            raise HTTPException(status_code=400, detail="One or more keywords were not found")
        paper.keywords = keywords

    db.commit()
    db.refresh(paper)
    return paper


def delete_paper(db: Session, paper_id: int):
    paper = get_paper(db, paper_id)
    db.delete(paper)
    db.commit()


def create_agenda(db: Session, payload: AgendaCreate, created_by: int):
    agenda = models.Agenda(
        title=payload.title,
        details=payload.details,
        due_date=payload.due_date,
        status_id=payload.status_id,
        created_by=created_by,
    )
    db.add(agenda)
    db.commit()
    db.refresh(agenda)
    return agenda


def list_agendas(db: Session, status_id: int | None, skip: int, limit: int):
    query = db.query(models.Agenda)
    if status_id is not None:
        query = query.filter(models.Agenda.status_id == status_id)
    return query.offset(skip).limit(limit).all()