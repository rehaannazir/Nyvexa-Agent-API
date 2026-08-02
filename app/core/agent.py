from datetime import datetime

from langchain_core.runnables import RunnableWithMessageHistory

from app.chains.assistant import assistant_chain, llm
from app.utils.history import get_session_history
from app.utils.compact import compact_history
from app.utils.tool_loop import loop

agent = RunnableWithMessageHistory(
    runnable=assistant_chain,
    get_session_history=get_session_history,
    history_messages_key="history",
    input_messages_key="text",
)


async def get_response(text: str, session_id: str) -> str:

    history = get_session_history(session_id)

    await compact_history(session_id)

    agent_response = await agent.ainvoke(
        {"text": text, "current_datetime": datetime.now().isoformat()},
        config={"configurable": {"session_id": session_id}},
    )

    return await loop(agent_response, llm, history)
