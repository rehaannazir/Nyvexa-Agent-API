from fastapi.routing import APIRouter
from sqlmodel import Session
from fastapi import status, HTTPException, Depends
from app.models.summary import Summary
from app.schemas.summary_schema import SummaryRequest
from app.models.user import User
from app.auth.dependencies import get_user
from app.core.database import get_session
from app.services.summary_services import SummaryService

router = APIRouter(prefix="/summary", tags=["Summarizer"])


@router.post("/", response_model=Summary, status_code=status.HTTP_200_OK)
async def get_summary(
    text: SummaryRequest,
    session: Session = Depends(get_session),
    user: User = Depends(get_user),
):
    summary = await SummaryService.fetch_summary(text, session, user)

    if not summary:

        raise HTTPException(
            detail="ERROR! Model is not working well.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return summary
