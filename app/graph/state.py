from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict):
    query: str
    search_queries: List[str]
    papers: List[Dict]
    top_papers: List[Dict]
    analyzed_papers: List[Dict]
    result: str
    sources: List[Dict]
    graph_path: str
