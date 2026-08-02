from typing import Optional
from fastapi import Request
from sqlmodel import Session
from app.models.user import User
from app.models.lead import Lead
from app.repositories.lead_repo import LeadRepo
from app.schemas.lead_schema import LeadRequest
from app.chains.extract_lead import extract_lead_chain
from app.core.logging import logger
from app.utils.usage import accumulate_usage


class LeadService:

    @staticmethod
    async def lead_extraction(
        message: LeadRequest, session: Session, user: User, request: Request
    ) -> Optional[Lead]:

        logger.info("Extracting lead for user '%s'.", user.username)

        result = await extract_lead_chain.ainvoke({"text": message.text})
        accumulate_usage(request, result["raw"])

        response = result["parsed"]

        if not response:
            logger.warning("Lead extraction returned no result for user '%s'.", user.username)
            return None

        lead = Lead(user_id=user.user_id, **response.model_dump())

        saved = LeadRepo.add_response(session, lead)
        logger.info("Lead #%s saved for user '%s'.", saved.no, user.username)

        return saved
