from typing import Optional
from sqlmodel import Session
from app.models.user import User
from app.models.lead import Lead
from app.repositories.lead_repo import LeadRepo
from app.schemas.lead_schema import LeadRequest
from app.chains.extract_lead import extract_lead_chain


class LeadService:

    @staticmethod
    async def lead_extraction(
        message: LeadRequest, session: Session, user: User
    ) -> Optional[Lead]:

        response = await extract_lead_chain.ainvoke({"text": message.text})

        if not response:
            return None

        lead = Lead(user_id=user.user_id, **response.model_dump())

        return LeadRepo.add_response(session, lead)
