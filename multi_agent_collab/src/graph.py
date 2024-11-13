from src.utils import router
from langgraph.graph import END, StateGraph, START
from src.utils.state import AgentState
from src.utils.nodes import supervisor_node, python_repl_node, tool_node, bash_node

def compile():
    workflow = StateGraph(AgentState)
    workflow.add_node("bash_chain", bash_node)
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("python_repl_chain", python_repl_node)
    workflow.add_node("call_tool", tool_node)

    workflow.add_edge(START, "Supervisor")

    workflow.add_conditional_edges(
        "Supervisor",
        router,
        {
            "bash": "bash_chain",
            "python": "python_repl_chain",
            "call_tool": "call_tool",
            END: END
        }
    )

    workflow.add_conditional_edges(
        "bash_chain",
        router,
        {
            "continue": "Supervisor",
            "call_tool": "call_tool",
            END: END
        }
    )

    workflow.add_conditional_edges(
        "python_repl_chain",
        router,
        {
            "continue": "Supervisor",
            "call_tool": "call_tool",
            END: END
        }
    )

    workflow.add_conditional_edges(
        "call_tool",
        lambda x: x["sender"],
        {
            "bash_chain": "bash_chain",
            "Supervisor": "Supervisor",
            "python_repl_chain": "python_repl_chain",
        },
    )

    graph = workflow.compile()
    return graph