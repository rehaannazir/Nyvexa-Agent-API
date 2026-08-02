from app.models.summary import SummaryBase
from pydantic import BaseModel


class SummaryRequest(BaseModel):

    text: str


class SummaryExtraction(SummaryBase):

    pass
