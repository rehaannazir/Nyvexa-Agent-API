from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import create_table
from app.core.logging import logger
from app.routers.auth import router as auth_router
from app.routers.extract_lead import router as lead_router
from app.routers.summarize import router as summary_router
from app.routers.assistant import router as assistant_router
from app.middleware.middleware import token_usage_middleware

from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.core.limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    logger.info("Nyvexa Ops API started.")
    yield
    logger.info("Nyvexa Ops API shutting down.")


app = FastAPI(
    title="Nyvexa Lead Agent",
    description="The agent helps in extracting the leads data, summarizing the meeting conversations and act as assistant to incoming leads and client having memory.",
    version="v1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(lead_router)
app.include_router(summary_router)
app.include_router(assistant_router)

app.middleware("http")(token_usage_middleware)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

app.add_middleware(SlowAPIMiddleware)


@app.get("/")
def health():

    return {"health": "The system is healthy and ready to execute."}
