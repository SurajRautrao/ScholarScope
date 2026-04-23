import math
from datetime import datetime

CURRENT_YEAR = datetime.now().year

def normalize(value, max_value):
    if max_value == 0:
        return 0
    return value / max_value

def compute_scores(results):
    # Extract max values for normalization
    max_citations = max([r["paper"].get("citations", 0) for r in results] or [1])

    ranked = []

    for r in results:
        paper = r["paper"]

        # 1. Relevance (lower distance = better)
        relevance_score = 1 / (1 + r["distance"])

        # 2. Citation score
        citations = paper.get("citations", 0)
        citation_score = normalize(math.log1p(citations), math.log1p(max_citations))

        # 3. Recency score
        year = paper.get("year")
        if year:
            recency_score = 1 / (1 + (CURRENT_YEAR - year))
        else:
            recency_score = 0

        final_score = (
            0.6 * relevance_score +
            0.3 * citation_score +
            0.1 * recency_score
        )

        ranked.append({
            "paper": paper,
            "score": final_score,
            "relevance": relevance_score,
            "citations": citations,
            "recency": recency_score
        })

    # Sort descending
    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked
