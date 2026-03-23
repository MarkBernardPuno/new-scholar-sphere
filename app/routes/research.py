from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models
from app.auth import get_current_user
from app.research_api import service
from app.research_api.schemas import (
    AgendaCreate,
    AgendaResponse,
    AuthorCreate,
    AuthorResponse,
    KeywordCreate,
    KeywordResponse,
    PaperCreate,
    PaperResponse,
    PaperUpdate,
    ResearcherCreate,
    ResearcherResponse,
    StatusCreate,
    StatusResponse,
)
from database.database import get_db


router = APIRouter(prefix="/research", tags=["Research"])


@router.post("/statuses", response_model=StatusResponse)
def create_status(
    payload: StatusCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.create_status(db, payload.status_name, payload.description)


@router.get("/statuses", response_model=list[StatusResponse])
def list_statuses(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.list_statuses(db)


@router.post("/keywords", response_model=KeywordResponse)
def create_keyword(
    payload: KeywordCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.create_keyword(db, payload.keyword_name)


@router.get("/keywords", response_model=list[KeywordResponse])
def list_keywords(
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.list_keywords(db)


@router.post("/authors", response_model=AuthorResponse)
def create_author(
    payload: AuthorCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.create_author(db, payload)


@router.get("/authors", response_model=list[AuthorResponse])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.list_authors(db, skip, limit)


@router.post("/researchers", response_model=ResearcherResponse)
def create_researcher(
    payload: ResearcherCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.create_researcher(db, payload)


@router.get("/researchers", response_model=list[ResearcherResponse])
def list_researchers(
    status_id: int | None = None,
    department_id: int | None = None,
    campus_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.list_researchers(db, status_id, department_id, campus_id, skip, limit)


@router.post("/papers", response_model=PaperResponse)
def create_paper(
    payload: PaperCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return service.create_paper(db, payload, current_user.user_id)


@router.get("/papers", response_model=list[PaperResponse])
def list_papers(
    q: str | None = None,
    status_id: int | None = None,
    department_id: int | None = None,
    campus_id: int | None = None,
    keyword: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.list_papers(db, q, status_id, department_id, campus_id, keyword, skip, limit)


@router.get("/papers/{paper_id}", response_model=PaperResponse)
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.get_paper(db, paper_id)


@router.put("/papers/{paper_id}", response_model=PaperResponse)
def update_paper(
    paper_id: int,
    payload: PaperUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.update_paper(db, paper_id, payload)


@router.delete("/papers/{paper_id}", status_code=204)
def delete_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    service.delete_paper(db, paper_id)
    return None


@router.post("/agendas", response_model=AgendaResponse)
def create_agenda(
    payload: AgendaCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return service.create_agenda(db, payload, current_user.user_id)


@router.get("/agendas", response_model=list[AgendaResponse])
def list_agendas(
    status_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),
):
    return service.list_agendas(db, status_id, skip, limit)
