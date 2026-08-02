from sqlmodel import Session
from app.schemas.summary_schema import SummaryRequest
from app.models.summary import Summary
from app.models.user import User
from app.chains.summarize import chain_summary
from app.repositories.summary_repo import SummaryRepo
from app.core.logging import logger


class SummaryService:

    @staticmethod
    async def fetch_summary(text: SummaryRequest, session: Session, user: User):

        logger.info("Generating summary for user '%s'.", user.username)

        response = await chain_summary.ainvoke({"text": text.text})

        if not response:
            logger.warning("Summary generation returned no result for user '%s'.", user.username)
            return None

        summary = Summary(user_id=user.user_id, **response.model_dump())

        saved = SummaryRepo.add_summary(session, summary)
        logger.info("Summary #%s saved for user '%s'.", saved.no, user.username)

        return saved
