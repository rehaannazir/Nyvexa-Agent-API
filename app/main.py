from fastapi import FastAPI

app = FastAPI(
    title="Nyvexa Lead Agent",
    description="The agent helps in extracting the leads data, summarizing the meeting conversations and act as assistant to incoming leads and client having memory.",
    version="v1.0",
)


@app.get("/")
def health():

    return {"health": "The system is healthy and ready to execute."}
