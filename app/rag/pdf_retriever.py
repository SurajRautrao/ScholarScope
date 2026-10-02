from app.rag.embeddings import embed_texts
from app.rag.vector_store import VectorStore

# with no specific question, cover the sections an explanation needs
SECTION_QUERIES = [
    "the proposed method and how it works",
    "experimental results and comparison with baselines",
]


def retrieve_relevant_chunks(query, chunks, k=5):
    """Always keep the first chunk (title, abstract, intro) and the last
    (conclusion), fill the rest from the middle by relevance, and return
    them in document order."""
    if len(chunks) <= k:
        return chunks

    middle = chunks[1:-1]
    queries = [query] if query else SECTION_QUERIES

    embeddings = embed_texts(middle)

    store = VectorStore(dim=len(embeddings[0]))
    store.add(embeddings, list(range(1, len(chunks) - 1)))

    # ranked chunk positions per query
    rankings = [
        [r["paper"] for r in store.search(embed_texts([q]), len(middle))]
        for q in queries
    ]

    # take the best unused chunk from each query in turn
    picked = []
    while len(picked) < k - 2:
        for ranking in rankings:
            best = next(i for i in ranking if i not in picked)
            picked.append(best)
            if len(picked) == k - 2:
                break

    positions = [0] + sorted(picked) + [len(chunks) - 1]

    return [chunks[i] for i in positions]
