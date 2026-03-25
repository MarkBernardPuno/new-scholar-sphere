from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

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
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.create_research_evaluation(db, payload)


@router.get("/", response_model=list[ResearchEvaluationResponse])
def list_research_evaluations(
    paper_id: UUID | None = None,
    status_value: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.list_research_evaluations(
        db,
        str(paper_id) if paper_id else None,
        status_value,
        search,
        skip,
        limit,
    )


@router.get("/{evaluation_id}", response_model=ResearchEvaluationResponse)
def get_research_evaluation(
    evaluation_id: UUID,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.get_research_evaluation(db, str(evaluation_id))


@router.put("/{evaluation_id}", response_model=ResearchEvaluationResponse)
def update_research_evaluation(
    evaluation_id: UUID,
    payload: ResearchEvaluationUpdate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.update_research_evaluation(db, str(evaluation_id), payload)


@router.delete("/{evaluation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_evaluation(
    evaluation_id: UUID,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    service.delete_research_evaluation(db, str(evaluation_id))
    return None
