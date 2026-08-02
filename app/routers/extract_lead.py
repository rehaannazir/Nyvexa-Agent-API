from fastapi import Depends, status, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.auth.dependencies import get_user
from app.repositories.lead_repo import LeadRepo
from fastapi.routing import APIRouter
from app.models.lead import Lead
from app.models.user import User
from app.schemas.lead_schema import LeadRequest
from app.services.lead_services import LeadService

from fastapi import Request
from app.core.limiter import limiter

router = APIRouter(prefix="/leads", tags=["Lead Extraction"])


@router.post("/extract", response_model=Lead, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def extract_lead(
    lead_message: LeadRequest,
    request: Request,
    user: User = Depends(get_user),
    session: Session = Depends(get_session),
):

    lead = await LeadService.lead_extraction(lead_message, session, user, request)

    if not lead:
        raise HTTPException(
            detail="Error! Model is not working well.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return lead
