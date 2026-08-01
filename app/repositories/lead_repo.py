from sqlmodel import Session
from app.models.lead import Lead


class LeadRepo:

    @staticmethod
    def add_response(session: Session, lead: Lead):

        if not lead:
            return None

        session.add(lead)
        session.commit()
        session.refresh(lead)

        return lead
