from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user
from app.research_evaluations import service
from app.research_evaluations.schemas import (
    ResearchEvaluationCreate,
    ResearchEvaluationResponse,
    ResearchEvaluationUpdate,
)
from database.database import get_db


router = APIRouter(prefix="/research-evaluations", tags=["Research Evaluations"])


@router.post("/", response_model=ResearchEvaluationResponse, status_code=status.HTTP_201_CREATED)
def create_research_evaluation(
    payload: ResearchEvaluationCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.create_research_evaluation(db, payload)


@router.get("/", response_model=list[ResearchEvaluationResponse])
def list_research_evaluations(
    campus_id: str | None = None,
    college_id: str | None = None,
    department_id: str | None = None,
    school_year_id: str | None = None,
    semester_id: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.list_research_evaluations(
        db,
        campus_id,
        college_id,
        department_id,
        school_year_id,
        semester_id,
        search,
        skip,
        limit,
    )


@router.get("/{re_id}", response_model=ResearchEvaluationResponse)
def get_research_evaluation(
    re_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.get_research_evaluation(db, re_id)


@router.put("/{re_id}", response_model=ResearchEvaluationResponse)
def update_research_evaluation(
    re_id: int,
    payload: ResearchEvaluationUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.update_research_evaluation(db, re_id, payload)


@router.delete("/{re_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_evaluation(
    re_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    service.delete_research_evaluation(db, re_id)
    return None
