from pathlib import Path
from langchain_community.chat_message_histories import SQLChatMessageHistory

store = {}
DB_PATH = Path(__file__).resolve().parent.parent / "memory" / "chat.db"


def get_session_history(session_id):

    if session_id not in store:
        store[session_id] = SQLChatMessageHistory(
            session_id=session_id,
            connection=f"sqlite+aiosqlite:///{DB_PATH}",
            async_mode=True,
        )

    return store[session_id]
