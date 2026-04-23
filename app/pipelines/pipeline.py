from app.graph.langgraph_pipeline import create_graph

graph = create_graph()

def run_pipeline(query):

    result = graph.invoke({
        "query": query
    })

    final_result = result.get("result")

    if isinstance(final_result, dict):
        final_result = final_result.get("text", "")

    # fallback (if result key itself missing)
    if not final_result:
        final_result = result.get("text", "")

    return {
        "query": query,
        "result": final_result,
        "sources": result.get("sources", []),
        "graph_path": result.get("graph_path", None)
    }


"""
from app.agents.planner import planner_agent
from app.agents.researcher import fetch_arxiv_papers
from app.agents.writer import writer_agent
from app.rag.retriever import retrieve_relevant_papers
from app.agents.analyst import analyze_paper
from app.agents.critic import critic_agent
from app.agents.semantic_scholar import fetch_semantic_scholar_papers
from app.utils.helpers import deduplicate_papers
import mlflow
from app.utils.mlflow_logger import init_mlflow
from app.graph.citation_graph import build_citation_graph, plot_graph
from app.agents.semantic_scholar import fetch_paper_references
import time

def run_pipeline(query):
    init_mlflow()

    with mlflow.start_run():

        mlflow.log_param("query", query)

        print("\n[1] Planning...")
        plan = planner_agent(query)

        search_queries = plan.get("search_queries", [query])
        keywords = plan.get("keywords", [])

        print("\n[2] Fetching papers...")

        all_papers = []
        for q in search_queries:
            arxiv_papers = fetch_arxiv_papers(q)
            ss_papers = fetch_semantic_scholar_papers(q, limit=3)
            if not ss_papers:
                print("Semantic Scholar unavailable, using arXiv only")
            
            all_papers.extend(arxiv_papers)
            all_papers.extend(ss_papers)

        papers = deduplicate_papers(all_papers)

        mlflow.log_metric("num_papers_fetched", len(papers))

        print("\n[3] Retrieving papers...")
        top_papers = retrieve_relevant_papers(query, papers, k=3)

        mlflow.log_metric("num_papers_selected", len(top_papers))

        print("\n[4] Building citation graph...")
        graph = build_citation_graph(
            top_papers,
            fetch_paper_references,
            max_refs=8
        )
        graph_path = plot_graph(graph)

        print("\n[5] Analyzing...")
        start_analysis = time.time()
        analyzed_papers = []
        for p in top_papers:
            analysis = analyze_paper(p)
            analyzed_papers.append({
                "title": p["title"],
                "analysis": analysis
            })

        analysis_time = time.time() - start_analysis
        mlflow.log_metric("time_analysis", analysis_time)
        print(f" Analysis Time: {analysis_time:.2f} sec")
        ""
        print("\n[6] Critic...")
        critique = critic_agent(query, analyzed_papers)

        mlflow.log_text(critique, "critic.txt")
        ""
        print("\n[7] Writing...")
        start_writer = time.time()
        writer_output = writer_agent(query, analyzed_papers)

        result = writer_output["text"]
        sources = writer_output["sources"]

        writer_time = time.time() - start_writer
        mlflow.log_metric("time_writer", writer_time)
        print(f" Writer Time: {writer_time:.2f} sec")

        mlflow.log_text(result, "output.txt")

        return {
        "result": result,
        "sources": sources,
        "graph_path": graph_path
        }
"""
