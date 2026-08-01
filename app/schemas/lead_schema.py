from pydantic import BaseModel
from app.models.lead import LeadBase


class LeadRequest(BaseModel):

    text: str


class LeadExtraction(LeadBase):
    pass
