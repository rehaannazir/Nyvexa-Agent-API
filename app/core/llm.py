from app.core.config import setting
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm(model: str = None, temperature: float = None):

    return ChatGoogleGenerativeAI(
        model=model or setting.GEMINI_MODEL,
        temperature=temperature if temperature is not None else setting.TEMPERATURE,
    )
