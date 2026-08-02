from sqlmodel import Session
from app.models.summary import Summary


class SummaryRepo:

    @staticmethod
    def add_summary(session: Session, summary: Summary):

        session.add(summary)
        session.commit()
        session.refresh(summary)

        return summary
