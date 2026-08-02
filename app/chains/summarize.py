from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import get_setting
from app.schemas.summary_schema import SummaryExtraction

setting = get_setting()

SYSTEM_PROMPT = """
You are an expert summarization system.

Generate a concise, accurate, and factual summary of the provided text.

Rules:
- Preserve the original meaning.
- Do not invent information.
- Remove repetition and unnecessary details.
- Focus on the most important information.
- Return the response according to the provided output schema.
"""

USER_PROMPT = """
Summarize the following text.

Text:
{text}
"""

llm = (
    ChatGoogleGenerativeAI(model=setting.GEMINI_MODEL)
    .with_structured_output(SummaryExtraction)
    .with_retry(stop_after_attempt=3)
)

prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("human", USER_PROMPT)]
)

chain_summary = prompt | llm
