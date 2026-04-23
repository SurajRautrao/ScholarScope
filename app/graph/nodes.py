from app.agents.planner import planner_agent
from app.agents.researcher import fetch_arxiv_papers
from app.agents.semantic_scholar import fetch_semantic_scholar_papers
from app.rag.retriever import retrieve_relevant_papers
from app.agents.analyst import analyze_paper
from app.agents.writer import writer_agent
from app.utils.helpers import deduplicate_papers
from app.graph.citation_graph import build_citation_graph, plot_graph
from app.agents.semantic_scholar import fetch_paper_references


# ---------------- PLANNER ----------------
def planner_node(state):
    plan = planner_agent(state["query"])
    return {
        "search_queries": plan.get("search_queries", [state["query"]])
    }


# ---------------- FETCH ----------------
def fetch_node(state):
    all_papers = []

    for q in state["search_queries"]:
        arxiv = fetch_arxiv_papers(q)
        ss = fetch_semantic_scholar_papers(q, limit=3)

        all_papers.extend(arxiv)
        all_papers.extend(ss)

    papers = deduplicate_papers(all_papers)

    return {"papers": papers}


# ---------------- RETRIEVE ----------------
def retrieve_node(state):
    top_papers = retrieve_relevant_papers(
        state["query"],
        state["papers"],
        k=3
    )
    return {"top_papers": top_papers}


# ---------------- ANALYZE ----------------
def analyze_node(state):
    analyzed = []

    for p in state["top_papers"]:
        analysis = analyze_paper(p)
        analyzed.append({
            "title": p["title"],
            "analysis": analysis
        })

    return {"analyzed_papers": analyzed}


# ---------------- GRAPH ----------------
def graph_node(state):
    papers = state.get("top_papers", [])
    print("GRAPH NODE PAPERS:", papers)

    if not papers:
        print("No papers → skipping graph")
        return {"graph_path": None}
    graph = build_citation_graph(
        papers,
        fetch_paper_references,
        max_refs=10
    )

    path = plot_graph(graph)
    print("TOP PAPERS:", state.get("top_papers"))
    return {"graph_path": path}


# ---------------- WRITE ----------------
def writer_node(state):
    raw_result = writer_agent(state["query"], state["analyzed_papers"])
    if isinstance(raw_result, dict):
        result = raw_result.get("text", "")
    else:
        result = raw_result

    # sources from top papers
    sources = [
        {"title": p["title"], "link": p.get("link", "")}
        for p in state["top_papers"]
    ]

    return {
        "result": result,
        "sources": sources
    }
