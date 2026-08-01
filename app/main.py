from fastapi import FastAPI

from app.routers.auth import router as auth_router

app = FastAPI(
    title="Nyvexa Lead Agent",
    description="The agent helps in extracting the leads data, summarizing the meeting conversations and act as assistant to incoming leads and client having memory.",
    version="v1.0",
)

app.include_router(auth_router)


@app.get("/")
def health():

    return {"health": "The system is healthy and ready to execute."}
