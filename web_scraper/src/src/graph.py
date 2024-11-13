from langgraph.graph import StateGraph, END, START
from typing import Annotated, Sequence, TypedDict
import operator
from langchain_core.messages import BaseMessage, HumanMessage

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str
    url: str
    documents: list
    query: str
    results: list

def compile():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("scraper", scraper_node)
    workflow.add_node("indexer", indexer_node)
    workflow.add_node("searcher", searcher_node)
    workflow.add_node("supervisor", supervisor_node)

    # Add edges
    workflow.add_edge(START, "supervisor")

    # Add conditional edges from supervisor to other nodes
    workflow.add_conditional_edges(
        "supervisor",
        router,
        {
            "scrape": "scraper",
            "index": "indexer",
            "search": "searcher",
            END: END
        }
    )

    # Add edges back to supervisor
    workflow.add_edge("scraper", "supervisor")
    workflow.add_edge("indexer", "supervisor")
    workflow.add_edge("searcher", "supervisor")

    return workflow.compile() 