from fastapi.routing import APIRouter
from app.models.lead import Lead, LeadRequest
from chains.extract_lead import extract_lead_chain

router = APIRouter(prefix="/leads", tags=["Lead Extraction"])


@router.post("/extract", response_model=Lead)
async def extract_lead(lead_message: LeadRequest):

    response = extract_lead_chain.ainvoke({"query": lead_message.text})

    return response
