import requests
import time
import arxiv
from app.utils.config import SEMANTIC_SCHOLAR_API_KEY

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


# API key allows 1 request/second, cumulative across all endpoints
MIN_INTERVAL = 1.1
_last_request = 0.0


def _headers(user_agent):
    headers = {"User-Agent": user_agent}
    if SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY
    return headers


def _get(url, params, headers, retries=4, timeout=10):
    """Rate-limited GET with backoff on 429. All Semantic Scholar calls go through here."""
    global _last_request

    response = None
    for attempt in range(retries):
        wait = _last_request + MIN_INTERVAL - time.monotonic()
        if wait > 0:
            time.sleep(wait)

        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        _last_request = time.monotonic()

        if response.status_code != 429:
            return response

        wait_time = 2 ** attempt
        print(f"Rate limited. Retrying in {wait_time}s...")
        time.sleep(wait_time)

    return response

def fetch_semantic_scholar_papers(query, limit=10, retries=3):
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,year,citationCount,authors,url"
    }

    headers = _headers("research-assistant/1.0")

    response = _get(BASE_URL, params, headers, retries=retries)

    if response.status_code == 200:
        data = response.json()

        papers = []
        for paper in data.get("data", []):
            papers.append({
                "title": paper.get("title"),
                "summary": paper.get("abstract"),
                "year": paper.get("year"),
                "citations": paper.get("citationCount", 0),
                "authors": [a["name"] for a in paper.get("authors", [])],
                "url": paper.get("url"),
                "source": "semantic_scholar",
            })

        return papers

    print(f"Error {response.status_code}: {response.text}")
    return []


def fetch_arxiv_references(title, max_results=5):
    try:
        search = arxiv.Search(
            query=title,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []

        for paper in search.results():
            results.append({
                "title": paper.title,
                "link": paper.entry_id
            })

        print(f"[ARXIV] Found {len(results)} papers for fallback")

        return results

    except Exception as e:
        print("[ARXIV ERROR]:", e)
        return []

import requests

RefBASE_URL = "https://api.semanticscholar.org/graph/v1"

def fetch_semantic_references(title):
    try:
        headers = _headers("Mozilla/5.0")

        # -------- STEP 1: SEARCH PAPER --------
        search_url = f"{RefBASE_URL}/paper/search"
        params = {
            "query": title,
            "limit": 1,
            "fields": "title,paperId"
        }

        res = _get(search_url, params, headers)

        if res.status_code != 200:
            print("[ERROR] Search API failed:", res.text)
            return []

        data = res.json()

        if not data.get("data"):
            print("[DEBUG] No paper found for:", title)
            return []

        paper = data["data"][0]
        paper_id = paper.get("paperId")

        print(f"[DEBUG] Found paper: {paper.get('title')}")

        # -------- STEP 2: FETCH REFERENCES --------
        ref_url = f"{RefBASE_URL}/paper/{paper_id}"
        params = {
            "fields": "references.title,references.url"
        }

        res = _get(ref_url, params, headers)

        if res.status_code != 200:
            print("[ERROR] Reference API failed:", res.text)
            return []

        data = res.json()
        references = data.get("references", [])

        print(f"[DEBUG] Got {len(references)} references")

        return [
            {
                "title": ref.get("title", "Unknown"),
                "link": ref.get("url", "")
            }
            for ref in references if ref.get("title")
        ]

    except Exception as e:
        print("[ERROR] Exception:", e)
        return []
    

def fetch_paper_references(title):
    # -------- 1. Try Semantic Scholar --------
    refs = fetch_semantic_references(title)

    if refs:
        print(f"[SEMANTIC] {len(refs)} references found")
        return refs[:5]

    # -------- 2. Fallback to arXiv --------
    print("[FALLBACK] Using arXiv...")

    refs = fetch_arxiv_references(title)

    if refs:
        return refs[:5]

    # -------- 3. Final fallback (never empty) --------
    print("[FALLBACK] Using dummy references")

    return [
        {"title": f"{title} - Related Work", "link": ""},
        {"title": f"{title} - Survey Paper", "link": ""}
    ]




