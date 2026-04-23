from app.rag.embeddings import embed_texts
from app.rag.vector_store import VectorStore

def retrieve_relevant_chunks(query, chunks, k=5):
    embeddings = embed_texts(chunks)

    store = VectorStore(dim=len(embeddings[0]))
    store.add(embeddings, chunks)

    query_embedding = embed_texts([query])

    results = store.search(query_embedding, k)

    top_chunks = [r["paper"] for r in results]

    return top_chunks
