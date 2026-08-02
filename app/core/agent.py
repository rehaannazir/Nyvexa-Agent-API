from datetime import datetime

from langchain_core.runnables import RunnableWithMessageHistory

from app.chains.assistant import assistant_chain, llm
from app.utils.history import get_session_history
from app.utils.compact import compact_history
from app.utils.tool_loop import loop
from app.core.logging import logger

agent = RunnableWithMessageHistory(
    runnable=assistant_chain,
    get_session_history=get_session_history,
    history_messages_key="history",
    input_messages_key="text",
)


async def get_response(text: str, session_id: str):
    """
    Streams the assistant's reply for `text` as a series of small
    events, so the caller can forward them to the client as they
    happen instead of waiting for the whole answer.

    Yields:
        {"type": "token", "content": <text>} for each piece of the
        model's reply, and {"type": "tool_call", "tool": <name>}
        whenever a tool (calculator, CRM, calendar, ...) runs.
    """

    logger.info("Assistant request from session '%s'.", session_id)

    history = get_session_history(session_id)

    await compact_history(session_id)

    full_response = None

    async for chunk in agent.astream(
        {"text": text, "current_datetime": datetime.now().isoformat()},
        config={"configurable": {"session_id": session_id}},
    ):
        full_response = chunk if full_response is None else full_response + chunk

        if chunk.content:
            yield {"type": "token", "content": chunk.content}

    async for event in loop(full_response, llm, history):
        yield event

    logger.info("Assistant response ready for session '%s'.", session_id)
