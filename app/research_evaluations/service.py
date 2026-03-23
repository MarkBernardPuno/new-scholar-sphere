from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import models
from app.research_evaluations.schemas import ResearchEvaluationCreate, ResearchEvaluationUpdate


def _validate_campus_college(db: Session, campus_id: int, college_id: int) -> None:
    campus = db.query(models.Campus).filter(models.Campus.campus_id == campus_id).first()
    if not campus:
        raise HTTPException(status_code=400, detail="Campus not found")

    college = db.query(models.College).filter(models.College.college_id == college_id).first()
    if not college:
        raise HTTPException(status_code=400, detail="College not found")


def create_research_evaluation(db: Session, payload: ResearchEvaluationCreate) -> models.ResearchEvaluation:
    _validate_campus_college(db, payload.campus_id, payload.college_id)

    record = models.ResearchEvaluation(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_research_evaluations(
    db: Session,
    campus_id: str | None,
    college_id: str | None,
    department_id: str | None,
    school_year_id: str | None,
    semester_id: str | None,
    search: str | None,
    skip: int,
    limit: int,
) -> list[models.ResearchEvaluation]:
    query = db.query(models.ResearchEvaluation)

    if campus_id:
        query = query.filter(models.ResearchEvaluation.campus_id == campus_id)
    if college_id:
        query = query.filter(models.ResearchEvaluation.college_id == college_id)
    if department_id:
        query = query.filter(models.ResearchEvaluation.department_id == department_id)
    if school_year_id:
        query = query.filter(models.ResearchEvaluation.school_year_id == school_year_id)
    if semester_id:
        query = query.filter(models.ResearchEvaluation.semester_id == semester_id)
    if search:
        query = query.filter(models.ResearchEvaluation.title_of_research.ilike(f"%{search}%"))

    return query.order_by(models.ResearchEvaluation.re_id.desc()).offset(skip).limit(limit).all()


def get_research_evaluation(db: Session, re_id: int) -> models.ResearchEvaluation:
    record = db.query(models.ResearchEvaluation).filter(models.ResearchEvaluation.re_id == re_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Research evaluation not found")
    return record


def update_research_evaluation(
    db: Session,
    re_id: int,
    payload: ResearchEvaluationUpdate,
) -> models.ResearchEvaluation:
    record = get_research_evaluation(db, re_id)
    update_data = payload.model_dump(exclude_unset=True)

    next_campus_id = update_data.get("campus_id", record.campus_id)
    next_college_id = update_data.get("college_id", record.college_id)
    _validate_campus_college(db, next_campus_id, next_college_id)

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_research_evaluation(db: Session, re_id: int) -> None:
    record = get_research_evaluation(db, re_id)
    db.delete(record)
    db.commit()
