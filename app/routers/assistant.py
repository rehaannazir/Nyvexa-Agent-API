import asyncio
import json

from fastapi.routing import APIRouter
from fastapi import Depends, status
from app.auth.dependencies import get_user
from app.models.user import User
from app.schemas.assistant_schema import AssistantRequest
from app.core.agent import get_response
from sse_starlette import EventSourceResponse

from fastapi import Request
from app.core.limiter import limiter

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


@router.post("/", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def get_answer(
    request: Request,
    chat: AssistantRequest,
    user: User = Depends(get_user),
):
    async def event_generator():
        async for event in get_response(chat.message, user.username):
            await asyncio.sleep(0.02)
            yield {"data": json.dumps(event)}

    return EventSourceResponse(event_generator())
