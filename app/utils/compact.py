from app.utils.history import get_session_history
from app.core.llm import get_llm
from langchain_core.messages import SystemMessage


async def compact_history(session_id: str):

    history = get_session_history(session_id)
    llm_instance = get_llm()

    messages = history.messages
    total_tokens = llm_instance.get_num_tokens_from_messages(messages)

    if total_tokens <= 1000:
        return

    recent_msgs = []
    recent_tokens = 0
    split = len(messages)

    for msg in reversed(messages):

        msg_tokens = llm_instance.get_num_tokens(msg.content)

        if recent_tokens + msg_tokens > 500:
            break

        recent_msgs.append(msg)
        recent_tokens += msg_tokens
        split -= 1

    summary_msgs = messages[:split]

    if not summary_msgs:
        return

    summary = await llm_instance.ainvoke(summary_msgs)

    history.clear()
    history.add_message(SystemMessage(content=summary.content))

    for msg in reversed(recent_msgs):
        history.add_message(msg)
