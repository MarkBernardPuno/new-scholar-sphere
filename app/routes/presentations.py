from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.auth import get_current_user
from app.presentations_api import service
from app.presentations_api.schemas import PresentationCreate, PresentationResponse, PresentationUpdate
from database.database import get_db


router = APIRouter(prefix="/presentations", tags=["Presentations"])


@router.post("/", response_model=PresentationResponse, status_code=status.HTTP_201_CREATED)
def create_presentation(payload: PresentationCreate, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.create_presentation(db, payload)


@router.get("/", response_model=list[PresentationResponse])
def list_presentations(
    paper_id: UUID | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.list_presentations(db, str(paper_id) if paper_id else None, skip, limit)


@router.get("/{presentation_id}", response_model=PresentationResponse)
def get_presentation(presentation_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
    return service.get_presentation(db, str(presentation_id))


@router.put("/{presentation_id}", response_model=PresentationResponse)
def update_presentation(
    presentation_id: UUID,
    payload: PresentationUpdate,
    db=Depends(get_db),
    _: dict = Depends(get_current_user),
):
    return service.update_presentation(db, str(presentation_id), payload)


@router.delete("/{presentation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_presentation(presentation_id: UUID, db=Depends(get_db), _: dict = Depends(get_current_user)):
    service.delete_presentation(db, str(presentation_id))
    return None
