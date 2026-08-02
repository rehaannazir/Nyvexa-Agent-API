from fastapi.routing import APIRouter
from fastapi import Depends, status, HTTPException
from app.auth.dependencies import get_user
from app.models.user import User
from app.schemas.assistant_schema import AssistantRequest, AssistantResponse
from app.core.agent import get_response

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


@router.post("/", response_model=AssistantResponse, status_code=status.HTTP_200_OK)
async def get_answer(
    request: AssistantRequest,
    user: User = Depends(get_user),
):
    answer = await get_response(request.message, user.username)

    if not answer:

        raise HTTPException(
            detail="ERROR! Model is not working well.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return AssistantResponse(response=answer)
