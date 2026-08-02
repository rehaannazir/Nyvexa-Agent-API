import json
from pathlib import Path
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_community.chat_message_histories import SQLChatMessageHistory
from app.core.config import get_setting
from app.tools.calculator import calculator
from app.core.llm import get_llm

from app.tools.crm import (
    add_contact,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    list_contacts,
)
from app.tools.calender import (
    schedule_event,
    get_event,
    update_event,
    cancel_event,
    list_events,
    check_availability,
)

tools = [
    calculator,
    add_contact,
    get_contact,
    update_contact,
    delete_contact,
    search_contacts,
    list_contacts,
    schedule_event,
    get_event,
    update_event,
    cancel_event,
    list_events,
    check_availability,
]

setting = get_setting()

SYSTEM_PROMPT = """
You are Nexara Ops Assistant, an AI operations assistant designed to help users manage contacts, schedules, and perform calculations.

You have access to specialized tools for:
- Performing mathematical calculations.
- Managing CRM contacts (create, retrieve, update, delete, search, and list).
- Managing calendar events (schedule, retrieve, update, cancel, list, and check availability).

Rules:

1. Use tools whenever they are required to answer the user's request.
2. Never invent contact or calendar information. If the requested information requires a tool, call the appropriate tool.
3. If the user asks for calculations, always use the calculator tool instead of calculating mentally.
4. Use only the minimum number of tool calls necessary to complete the task.
5. If information is missing to complete an action, ask a concise follow-up question instead of guessing.
6. If a requested contact or event does not exist, clearly inform the user.
7. When modifying or deleting data, ensure you have enough identifying information before calling the tool.
8. If multiple contacts or events match a query, present the matches and ask the user which one they mean.
9. Explain the outcome naturally after tool execution. Do not expose internal tool names or implementation details.
10. Be concise, accurate, and professional.
"""

USER_PROMPT = """
Current Date & Time:
{current_datetime}

User Request:
{text}
"""

DB_PATH = Path(__file__).resolve().parent.parent / "memory" / "chat.db"

session_id = "user_1"

store = {}


def get_session_history(session_id):

    if session_id not in store:
        store[session_id] = SQLChatMessageHistory(
            session_id=session_id, connection=f"sqlite:///{DB_PATH}"
        )

    return store[session_id]


llm = get_llm().bind_tools(tools).with_retry(stop_after_attempt=3)

prompt = ChatPromptTemplate.from_messages(
    ("system", SYSTEM_PROMPT), MessagesPlaceholder("history"), ("human", USER_PROMPT)
)

chain = prompt | llm

agent = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    history_messages_key="history",
    input_messages_key="text",
)

tool_use = {
    "calculator": calculator,
    "add_contact": add_contact,
    "get_contact": get_contact,
    "update_contact": update_contact,
    "delete_contact": delete_contact,
    "search_contacts": search_contacts,
    "list_contacts": list_contacts,
    "schedule_event": schedule_event,
    "get_event": get_event,
    "update_event": update_event,
    "cancel_event": cancel_event,
    "list_events": list_events,
    "check_availability": check_availability,
}


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


async def get_response(text: str, session_id: str = session_id) -> str:

    history = get_session_history(session_id)

    await compact_history(session_id)

    agent_response = await agent.ainvoke(
        {"text": text, "current_datetime": datetime.now().isoformat()},
        config={"configurable": {"session_id": session_id}},
    )

    while agent_response.tool_calls:

        for call in agent_response.tool_calls:

            tool = tool_use[call["name"]]
            result = tool.invoke(call["args"])

            history.add_message(
                ToolMessage(
                    content=json.dumps(result, default=str), tool_call_id=call["id"]
                )
            )

        agent_response = await llm.ainvoke(history.messages)
        history.add_message(agent_response)

    return agent_response.content
