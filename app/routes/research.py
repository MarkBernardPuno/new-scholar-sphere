from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.auth import get_current_user
from app.research_api import service
from app.research_api.schemas import (
    AuthorCreate,
    AuthorResponse,
    PaperCreate,
    PaperResponse,
    PaperUpdate,
    ResearchOutputTypeCreate,
    ResearchOutputTypeResponse,
    ResearchTypeCreate,
    ResearchTypeResponse,
)
from database.database import get_db


router = APIRouter(prefix="/research", tags=["Research"])


@router.post("/types", response_model=ResearchTypeResponse)
def create_research_type(
    payload: ResearchTypeCreate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.create_research_type(db, payload.name, payload.description)


@router.get("/types", response_model=list[ResearchTypeResponse])
def list_research_types(
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.list_research_types(db)


@router.post("/output-types", response_model=ResearchOutputTypeResponse)
def create_research_output_type(
    payload: ResearchOutputTypeCreate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.create_research_output_type(db, payload.name, payload.description)


@router.get("/output-types", response_model=list[ResearchOutputTypeResponse])
def list_research_output_types(
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.list_research_output_types(db)


@router.post("/authors", response_model=AuthorResponse)
def create_author(
    payload: AuthorCreate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.create_author(db, payload)


@router.get("/authors", response_model=list[AuthorResponse])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.list_authors(db, skip, limit)


@router.post("/papers", response_model=PaperResponse)
def create_paper(
    payload: PaperCreate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.create_paper(db, payload)


@router.get("/papers", response_model=list[PaperResponse])
def list_papers(
    q: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.list_papers(db, q, skip, limit)


@router.get("/papers/{paper_id}", response_model=PaperResponse)
def get_paper(
    paper_id: UUID,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.get_paper(db, str(paper_id))


@router.put("/papers/{paper_id}", response_model=PaperResponse)
def update_paper(
    paper_id: UUID,
    payload: PaperUpdate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.update_paper(db, str(paper_id), payload)


@router.delete("/papers/{paper_id}", status_code=204)
def delete_paper(
    paper_id: UUID,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    service.delete_paper(db, str(paper_id))
    return None
