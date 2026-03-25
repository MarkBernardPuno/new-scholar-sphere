from fastapi import APIRouter, Depends

from app.integrations_api import service
from app.security import require_api_key
from database.database import get_db


router = APIRouter(prefix="/integrations", tags=["Integrations"])


@router.post("/populate-defaults", dependencies=[Depends(require_api_key)])
def populate_defaults(db=Depends(get_db)):
    """Seed default roles and statuses for scripts/tests."""
    return service.populate_defaults(db)


@router.post("/email/test", dependencies=[Depends(require_api_key)])
def email_test(recipient: str):
    """Email integration stub endpoint for external service hooks."""
    return service.email_test(recipient)
