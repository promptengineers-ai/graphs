from langgraph.graph import END

def router(state):
    messages = state["messages"]
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "call_tool"
        
    if "FINAL ANSWER" in last_message.content:
        return END
        
    if state.get("sender") == "Supervisor":
        content = last_message.content
        if "execute bash" in content or "use bash" in content:
            return "bash"
        elif "execute python" in content or "use python" in content:
            return "python"
        
    if state.get("sender") == "bash_chain":
        return END
        
    return END