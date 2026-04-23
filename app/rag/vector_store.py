import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, vectors, texts):
        self.index.add(np.array(vectors))
        self.texts.extend(texts)

    def search(self, query_vector, k=5):
        distances, indices = self.index.search(query_vector, k)

        results = []
        for i, idx in enumerate(indices[0]):
            results.append({
                "paper": self.texts[idx],
                "distance": distances[0][i]
            })

        return results

