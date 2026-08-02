from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.database import create_table
from app.routers.auth import router as auth_router
from app.routers.extract_lead import router as lead_router
from app.routers.summarize import router as summary_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield


app = FastAPI(
    title="Nyvexa Lead Agent",
    description="The agent helps in extracting the leads data, summarizing the meeting conversations and act as assistant to incoming leads and client having memory.",
    version="v1.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(lead_router)
app.include_router(summary_router)


@app.get("/")
def health():

    return {"health": "The system is healthy and ready to execute."}
