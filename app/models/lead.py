from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal


class Lead(BaseModel):

    name: str = Field(description="Name of person who contact/message")
    company: str = Field(description="Company or organisation name whom he belongs")
    email: Optional[EmailStr] = Field(
        description="Email address of person", default=None
    )
    headcount: Optional[int] = Field(
        description="No of employees in company", default=None
    )
    intent: str = Field(
        description="Purpose of contact like one wants any service, support, demo or meeting"
    )
    follow_up: Optional[str] = Field(
        description="When we need to follow up him", default="1 day"
    )
    urgency: Literal["medium", "urgent", "very urgent"] = Field(
        description="From tone/emotion/words of message, urgency of lead"
    )


class LeadRequest(BaseModel):

    text: str
