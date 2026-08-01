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

router = APIRouter(prefix="/leads", tags=["Lead Extraction"])


@router.post("/extract", response_model=Lead, status_code=status.HTTP_200_OK)
async def extract_lead(
    lead_message: LeadRequest,
    user: User = Depends(get_user),
    session: Session = Depends(get_session),
):

    lead_data = await LeadService.lead_extraction(lead_message)

    if not lead_data:
        raise HTTPException(
            detail="Error! Model is not working well.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    lead = Lead(user_id=user.user_id, **lead_data.model_dump())

    return LeadRepo.add_response(session, lead)
