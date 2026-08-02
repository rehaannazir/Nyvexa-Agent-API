import json
from langchain_core.messages import ToolMessage
from app.tools.tools import TOOLS

tool_use = {tool.name: tool for tool in TOOLS}


async def loop(agent_response, llm, history):

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
