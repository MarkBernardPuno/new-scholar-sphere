from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.auth import get_current_user
from app.research_outputs import service
from app.research_outputs.schemas import ResearchOutputCreate, ResearchOutputResponse, ResearchOutputUpdate
from database.database import get_db


router = APIRouter(prefix="/research-outputs", tags=["Research Outputs"])


@router.post("/", response_model=ResearchOutputResponse, status_code=status.HTTP_201_CREATED)
def create_research_output(
    payload: ResearchOutputCreate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.create_research_output(db, payload)


@router.get("/", response_model=list[ResearchOutputResponse])
def list_research_outputs(
    paper_id: UUID | None = None,
    doi: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.list_research_outputs(
        db,
        str(paper_id) if paper_id else None,
        doi,
        search,
        skip,
        limit,
    )


@router.get("/{publication_id}", response_model=ResearchOutputResponse)
def get_research_output(
    publication_id: UUID,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.get_research_output(db, str(publication_id))


@router.put("/{publication_id}", response_model=ResearchOutputResponse)
def update_research_output(
    publication_id: UUID,
    payload: ResearchOutputUpdate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.update_research_output(db, str(publication_id), payload)


@router.delete("/{publication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_output(
    publication_id: UUID,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    service.delete_research_output(db, str(publication_id))
    return None
