from fastapi import APIRouter, Depends, Query, status

from app.research_outputs import service
from app.research_outputs.schemas import ResearchOutputCreate, ResearchOutputResponse, ResearchOutputUpdate
from database.database import get_db


router = APIRouter(prefix="/research-outputs", tags=["Research Outputs"])


@router.post("/", response_model=ResearchOutputResponse, status_code=status.HTTP_201_CREATED)
def create_research_output(
    payload: ResearchOutputCreate,
    db=Depends(get_db),
):
    return service.create_research_output(db, payload)


@router.get("/", response_model=list[ResearchOutputResponse])
def list_research_outputs(
    paper_id: int | None = None,
    doi: str | None = None,
    search: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
):
    return service.list_research_outputs(
        db,
        paper_id,
        doi,
        search,
        skip,
        limit,
    )


@router.get("/{publication_id}", response_model=ResearchOutputResponse)
def get_research_output(
    publication_id: int,
    db=Depends(get_db),
):
    return service.get_research_output(db, publication_id)


@router.put("/{publication_id}", response_model=ResearchOutputResponse)
def update_research_output(
    publication_id: int,
    payload: ResearchOutputUpdate,
    db=Depends(get_db),
):
    return service.update_research_output(db, publication_id, payload)


@router.delete("/{publication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_research_output(
    publication_id: int,
    db=Depends(get_db),
):
    service.delete_research_output(db, publication_id)
    return None
