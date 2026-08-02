from sqlmodel import Session
from app.schemas.summary_schema import SummaryRequest
from app.models.summary import Summary
from app.models.user import User
from app.chains.summarize import chain_summary
from app.repositories.summary_repo import SummaryRepo


class SummaryService:

    @staticmethod
    async def fetch_summary(text: SummaryRequest, session: Session, user: User):

        response = await chain_summary.ainvoke({"text": text.text})

        if not response:
            return None

        summary = Summary(user_id=user.user_id, **response.model_dump())

        return SummaryRepo.add_summary(session, summary)
