import json
from langchain_core.messages import ToolMessage
from app.tools.tools import TOOLS
from app.core.logging import logger

tool_use = {tool.name: tool for tool in TOOLS}


async def loop(agent_response, llm, history):
    """
    Runs tool calls requested by `agent_response`, then streams the
    model's follow-up response. Repeats until the model stops asking
    for tools.

    Yields:
        {"type": "tool_call", "tool": <tool name>} right before each
        tool runs, and {"type": "token", "content": <text>} for each
        piece of the model's streamed reply.
    """

    while agent_response.tool_calls:

        for call in agent_response.tool_calls:

            yield {"type": "tool_call", "tool": call["name"]}

            tool = tool_use[call["name"]]
            logger.info("Calling tool '%s' with args: %s", call["name"], call["args"])

            try:
                result = tool.invoke(call["args"])
            except Exception:
                logger.exception("Tool '%s' raised an error.", call["name"])
                raise

            await history.aadd_message(
                ToolMessage(
                    content=json.dumps(result, default=str), tool_call_id=call["id"]
                )
            )

        agent_response = None

        async for chunk in llm.astream(await history.aget_messages()):

            agent_response = chunk if agent_response is None else agent_response + chunk

            if chunk.content:
                yield {"type": "token", "content": chunk.content}

        await history.aadd_message(agent_response)
