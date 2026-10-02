from app.rag.embeddings import embed_texts
from app.rag.vector_store import VectorStore
from app.rag.ranker import compute_scores

def retrieve_relevant_papers(query, papers, k=5):
    # keep papers and texts aligned: only index papers that have an abstract
    papers = [p for p in papers if p.get("summary")]
    if not papers:
        return []

    texts = [f"{p['title']} {p['summary']}" for p in papers]

    paper_embeddings = embed_texts(texts)

    store = VectorStore(dim=len(paper_embeddings[0]))
    store.add(paper_embeddings, papers)

    query_embedding = embed_texts([query])

    results = store.search(query_embedding, k=10)  # get more candidates

    ranked = compute_scores(results)

    top_k = [r["paper"] for r in ranked[:k]]

    return top_k
