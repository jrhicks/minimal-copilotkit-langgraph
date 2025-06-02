"""
This is the main entry point for the agent.
It defines the workflow graph, state, tools, nodes and edges.
"""

from typing_extensions import Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from langgraph.prebuilt.tool_node import ToolNode
from copilotkit import CopilotKitState
from langgraph.checkpoint.memory import InMemorySaver
import logging
import json
from datetime import datetime

class AgentState(CopilotKitState):
    """
    Here we define the state of the agent

    In this instance, we're inheriting from CopilotKitState, which will bring in
    the CopilotKitState fields. We're also adding a custom field, `language`,
    which will be used to set the language of the agent.
    """
    proverbs: list[str] = []
    # your_custom_agent_state: str = ""

def log_event(event_data):
    logging.info(json.dumps(event_data))

@tool
def get_weather(location: str):
    """
    Get the weather for a given location.
    """
    return f"The weather for {location} is 70 degrees."

# @tool
# def add_proverb(state, proverb: str):
#     """Add a proverb to the agent's state."""
#     event_data = {
#         "event": "add_proverb_called",
#         "proverb": proverb,
#         "timestamp": datetime.utcnow().isoformat() + 'Z'
#     }
#     log_event(event_data)
#     raise Exception("add_proverb tool was called")
#     modified = False
#     if hasattr(state, "proverbs"):
#         if state.proverbs is None:
#             state.proverbs = []
#         state.proverbs.append(proverb)
#         modified = True
#     elif isinstance(state, dict):
#         if "proverbs" not in state or not isinstance(state["proverbs"], list):
#             state["proverbs"] = []
#         state["proverbs"].append(proverb)
#         modified = True
#     if modified:
#         event_data = {
#             "event": "add_proverb",
#             "proverb": proverb,
#             "state_type": type(state).__name__,
#             "timestamp": datetime.utcnow().isoformat() + 'Z'
#         }
#         log_event(event_data)
#     return f"Added proverb: {proverb}"

# @tool
# def your_tool_here(your_arg: str):
#     """Your tool description here."""
#     print(f"Your tool logic here")
#     return "Your tool response here."

tools = [
    get_weather
]

async def chat_node(state: AgentState, config: RunnableConfig) -> Command[Literal["tool_node", "__end__"]]:
    """
    Standard chat node based on the ReAct design pattern. It handles:
    - The model to use (and binds in CopilotKit actions and the tools defined above)
    - The system prompt
    - Getting a response from the model
    - Handling tool calls

    For more about the ReAct design pattern, see:
    https://www.perplexity.ai/search/react-agents-NcXLQhreS0WDzpVaS4m9Cg
    """

    logger = logging.getLogger("uvicorn")
    proverbs = state.get("proverbs", []) if isinstance(state, dict) else getattr(state, "proverbs", [])
    language = state.get("language", None) if isinstance(state, dict) else getattr(state, "language", None)
    messages = state.get("messages", []) if isinstance(state, dict) else getattr(state, "messages", [])
    event_data = {
        "event": "chat_node_called",
        "proverbs": proverbs,
        "language": language,
        "message_count": len(messages) if messages is not None else 0,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    logger.info(json.dumps(event_data, indent=2))

    # 1. Define the model
    model = ChatOpenAI(model="gpt-4o")

    # 2. Bind the tools to the model
    model_with_tools = model.bind_tools(
        [
            *state["copilotkit"]["actions"],
            get_weather
        ],

        # 2.1 Disable parallel tool calls to avoid race conditions,
        #     enable this for faster performance if you want to manage
        #     the complexity of running tool calls in parallel.
        parallel_tool_calls=False,
    )

    # 3. Define the system message by which the chat model will be run
    system_message = SystemMessage(
        content=f"You are a helpful assistant. Talk in {state.get('language', 'english')}."
    )

    # 4. Run the model to generate a response
    response = await model_with_tools.ainvoke([
        system_message,
        *state["messages"],
    ], config)

    # 5. Check for tool calls in the response and handle them. We ignore
    #    CopilotKit actions, as they are handled by CopilotKit.
    if isinstance(response, AIMessage) and response.tool_calls:
        actions = state["copilotkit"]["actions"]

        # 5.1 Check for any non-copilotkit actions in the response and
        #     if there are none, go to the tool node.
        if not any(
            action.get("name") == response.tool_calls[0].get("name")
            for action in actions
        ):
            return Command(goto="tool_node", update={"messages": response})

    # 6. We've handled all tool calls, so we can end the graph.
    return Command(
        goto=END,
        update={
            "messages": response
        }
    )

# Define the workflow graph
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("tool_node", ToolNode(tools=tools))
workflow.add_edge("tool_node", "chat_node")
workflow.set_entry_point("chat_node")

# Compile the workflow graph
graph = workflow.compile(checkpointer=InMemorySaver())
