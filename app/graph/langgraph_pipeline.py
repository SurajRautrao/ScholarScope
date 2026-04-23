from langgraph.graph import StateGraph, END
from app.graph.state import GraphState
from app.graph.nodes import (
    planner_node,
    fetch_node,
    retrieve_node,
    analyze_node,
    graph_node,
    writer_node
)


def create_graph():

    workflow = StateGraph(GraphState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("fetch", fetch_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("graph", graph_node)
    workflow.add_node("writer", writer_node)

    # Define flow
    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "fetch")
    workflow.add_edge("fetch", "retrieve")
    workflow.add_edge("retrieve", "analyze")
    workflow.add_edge("analyze", "graph")
    workflow.add_edge("graph", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()
