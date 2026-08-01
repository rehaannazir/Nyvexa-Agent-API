from langchain_core.prompts import ChatPromptTemplate
from app.core.llm import get_llm
from app.models.lead import Lead

SYSTEM_PROMPT = """You are a production-grade lead extraction engine.

Extract structured lead information from business communications.

Rules:
- Extract only supported schema fields.
- Never invent information.
- Preserve names, emails, phone numbers, and company names exactly as written.
- Normalize obvious formatting where appropriate (e.g., trim whitespace).
- If multiple values exist for a field, choose the one most relevant to the sender.
- Ignore greetings, signatures, disclaimers, quoted replies, and unrelated text.
- Return only the structured data defined by the output schema."""

USER_PROMPT = """Extract the lead information from the following text.
Text:
{query}"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT,
        ),
        (
            "human",
            USER_PROMPT,
        ),
    ]
)

llm = get_llm().with_structured_output(Lead).with_retry(stop_after_attempt=3)


extract_lead_chain = prompt | llm
