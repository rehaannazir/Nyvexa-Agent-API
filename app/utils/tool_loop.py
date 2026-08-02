import json
from langchain_core.messages import ToolMessage
from app.tools.tools import TOOLS
from app.core.logging import logger

tool_use = {tool.name: tool for tool in TOOLS}


async def loop(agent_response, llm, history):

    while agent_response.tool_calls:

        for call in agent_response.tool_calls:

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

        agent_response = await llm.ainvoke(await history.aget_messages())
        await history.aadd_message(agent_response)

    return agent_response.content
