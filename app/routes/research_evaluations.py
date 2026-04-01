from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.research_evaluations import service
from app.research_evaluations.schemas import (
    ResearchEvaluationCreate,
    ResearchEvaluationResponse,
    ResearchEvaluationUpdate,
)
from database.database import get_db


router = APIRouter(prefix="/research-evaluations", tags=["Research Evaluations"])

DbSession = Annotated[object, Depends(get_db)]
SkipParam = Annotated[int, Query(0, ge=0)]
LimitParam = Annotated[int, Query(50, ge=1, le=100)]
PaperFilterParam = Annotated[int | None, Query(None, ge=1)]
StatusFilterParam = Annotated[str | None, Query(None)]
SearchFilterParam = Annotated[str | None, Query(None)]


@router.get("/collections", response_model=dict[str, list[dict]])
def get_research_evaluation_collections(
    paper_id: PaperFilterParam,
    status_value: StatusFilterParam,
    search: SearchFilterParam,
    skip: SkipParam,
    limit: LimitParam,
    db: DbSession,
):
    return {
        "research_evaluations": service.list_research_evaluations(
            db,
            paper_id,
            status_value,
            search,
            skip,
            limit,
        ),
    }


@router.post("/", response_model=ResearchEvaluationResponse, status_code=status.HTTP_201_CREATED)
def create_research_evaluation(
    payload: ResearchEvaluationCreate,
    db: DbSession,
):
    return service.create_research_evaluation(db, payload)


@router.get("/", response_model=list[ResearchEvaluationResponse])
def list_research_evaluations(
    paper_id: PaperFilterParam,
    status_value: StatusFilterParam,
    search: SearchFilterParam,
    skip: SkipParam,
    limit: LimitParam,
    db: DbSession,
):
    return service.list_research_evaluations(
        db,
        paper_id,
        status_value,
        search,
        skip,
        limit,
    )


@router.get("/{evaluation_id}", response_model=ResearchEvaluationResponse)
def get_research_evaluation(
    evaluation_id: int,
    db: DbSession,
):
    return service.get_research_evaluation(db, evaluation_id)


@router.put("/{evaluation_id}", response_model=ResearchEvaluationResponse)
def update_research_evaluation(
    evaluation_id: int,
    payload: ResearchEvaluationUpdate,
    db: DbSession,
):
    return service.update_research_evaluation(db, evaluation_id, payload)


@router.delete("/{evaluation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_evaluation(
    evaluation_id: int,
    db: DbSession,
):
    service.delete_research_evaluation(db, evaluation_id)
    return None
