from typing import Optional
from app.schemas.lead_schema import LeadRequest, LeadExtraction
from app.chains.extract_lead import extract_lead_chain


class LeadService:

    @staticmethod
    async def lead_extraction(message: LeadRequest) -> Optional[LeadExtraction]:

        response = await extract_lead_chain.ainvoke({"query": message.text})

        if not response:
            return None

        return response
