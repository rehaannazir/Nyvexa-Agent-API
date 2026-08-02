from sqlmodel import SQLModel, Field
from typing import List


class SummaryBase(SQLModel):

    title: str = Field(description="topic of text")
    summary: str = Field(description="summary of text one forth of it's actual size")
    keypoints: List[str] = Field(description="main ideas from text")


class Summary(SummaryBase, table=True):

    no: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.user_id")
