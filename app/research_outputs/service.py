from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.research_outputs.schemas import ResearchOutputCreate, ResearchOutputUpdate


def create_research_output(db: Session, payload: ResearchOutputCreate) -> models.ResearchOutput:
    if payload.doi:
        existing = db.query(models.ResearchOutput).filter(models.ResearchOutput.doi == payload.doi).first()
        if existing:
            raise HTTPException(status_code=400, detail="DOI already exists")

    record = models.ResearchOutput(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_research_outputs(
    db: Session,
    school_year_id: str | None,
    semester_id: str | None,
    output_type: str | None,
    research_type_id: str | None,
    college_id: str | None,
    program_department_id: str | None,
    search: str | None,
    skip: int,
    limit: int,
) -> list[models.ResearchOutput]:
    query = db.query(models.ResearchOutput)

    if school_year_id:
        query = query.filter(models.ResearchOutput.school_year_id == school_year_id)
    if semester_id:
        query = query.filter(models.ResearchOutput.semester_id == semester_id)
    if output_type:
        query = query.filter(models.ResearchOutput.research_output_type_id == output_type)
    if research_type_id:
        query = query.filter(models.ResearchOutput.research_type_id == research_type_id)
    if college_id:
        query = query.filter(models.ResearchOutput.college_id == college_id)
    if program_department_id:
        query = query.filter(models.ResearchOutput.program_department_id == program_department_id)
    if search:
        query = query.filter(models.ResearchOutput.research_title.ilike(f"%{search}%"))

    return query.order_by(models.ResearchOutput.paper_id.desc()).offset(skip).limit(limit).all()


def get_research_output(db: Session, paper_id: int) -> models.ResearchOutput:
    record = db.query(models.ResearchOutput).filter(models.ResearchOutput.paper_id == paper_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Research output not found")
    return record


def update_research_output(db: Session, paper_id: int, payload: ResearchOutputUpdate) -> models.ResearchOutput:
    record = get_research_output(db, paper_id)
    update_data = payload.model_dump(exclude_unset=True)

    doi = update_data.get("doi")
    if doi:
        existing = (
            db.query(models.ResearchOutput)
            .filter(models.ResearchOutput.doi == doi, models.ResearchOutput.paper_id != paper_id)
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="DOI already exists")

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_research_output(db: Session, paper_id: int) -> None:
    record = get_research_output(db, paper_id)
    db.delete(record)
    db.commit()