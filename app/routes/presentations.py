from fastapi import APIRouter, Depends, Query, status

from app.presentations_api import service
from app.presentations_api.schemas import PresentationCreate, PresentationResponse, PresentationUpdate
from database.database import get_db


router = APIRouter(prefix="/presentations", tags=["Presentations"])


@router.post("/", response_model=PresentationResponse, status_code=status.HTTP_201_CREATED)
def create_presentation(payload: PresentationCreate, db=Depends(get_db)):
    return service.create_presentation(db, payload)


@router.get("/", response_model=list[PresentationResponse])
def list_presentations(
    paper_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db=Depends(get_db),
):
    return service.list_presentations(db, paper_id, skip, limit)


@router.get("/{presentation_id}", response_model=PresentationResponse)
def get_presentation(presentation_id: int, db=Depends(get_db)):
    return service.get_presentation(db, presentation_id)


@router.put("/{presentation_id}", response_model=PresentationResponse)
def update_presentation(
    presentation_id: int,
    payload: PresentationUpdate,
    db=Depends(get_db),
):
    return service.update_presentation(db, presentation_id, payload)


@router.delete("/{presentation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_presentation(presentation_id: int, db=Depends(get_db)):
    service.delete_presentation(db, presentation_id)
    return None
