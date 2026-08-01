import enum
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UrgencyLevel(str, enum.Enum):
    normal = "normal"
    urgent = "urgent"
    very_urgent = "very urgent"


class LeadBase(SQLModel):
    name: str = Field(description="Name of person who contacted you")
    company: str = Field(description="Company or organization name")
    email: Optional[EmailStr] = Field(
        default=None,
    )
    headcount: Optional[int] = Field(default=None, description="No of employees")
    intent: str = Field(description="Purpose of contact")
    follow_up: Optional[str] = Field(
        default="1 day", description="time to contact back"
    )
    urgency: UrgencyLevel = Field(description="Lead urgency")


class Lead(LeadBase, table=True):
    no: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.user_id")
