from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user
from app.research_outputs import service
from app.research_outputs.schemas import ResearchOutputCreate, ResearchOutputResponse, ResearchOutputUpdate
from database.database import get_db


router = APIRouter(prefix="/research-outputs", tags=["Research Outputs"])


@router.post("/", response_model=ResearchOutputResponse, status_code=status.HTTP_201_CREATED)
def create_research_output(
    payload: ResearchOutputCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.create_research_output(db, payload)


@router.get("/", response_model=list[ResearchOutputResponse])
def list_research_outputs(
    school_year_id: str | None = None,
    semester_id: str | None = None,
    output_type: str | None = None,
    research_type_id: str | None = None,
    college_id: str | None = None,
    program_department_id: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.list_research_outputs(
        db,
        school_year_id,
        semester_id,
        output_type,
        research_type_id,
        college_id,
        program_department_id,
        search,
        skip,
        limit,
    )


@router.get("/{paper_id}", response_model=ResearchOutputResponse)
def get_research_output(
    paper_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.get_research_output(db, paper_id)


@router.put("/{paper_id}", response_model=ResearchOutputResponse)
def update_research_output(
    paper_id: int,
    payload: ResearchOutputUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.update_research_output(db, paper_id, payload)


@router.delete("/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_output(
    paper_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    service.delete_research_output(db, paper_id)
    return None
