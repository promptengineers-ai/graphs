"""Common utilities for nodes."""
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    ToolMessage,
    AIMessage,
)

from src.config import OPENAI_API_KEY

# Helper function to create a node for a given agent
def agent_node(state, agent, name):
    result = agent.invoke(state)
    # We convert the agent output into a format that is suitable to append to the global state
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        "sender": name,
    }

llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)  # Fixed typo in model name from "gpt-4o" 