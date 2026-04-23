import requests
import time
import arxiv

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def fetch_semantic_scholar_papers(query, limit=10, retries=3):
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,abstract,year,citationCount,authors,url"
    }

    headers = {
        "User-Agent": "research-assistant/1.0"
    }

    for attempt in range(retries):
        response = requests.get(BASE_URL, params=params, headers=headers)

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

        elif response.status_code == 429:
            wait_time = 2 ** attempt
            print(f"Rate limited. Retrying in {wait_time}s...")
            time.sleep(wait_time)

        else:
            print(f"Error {response.status_code}: {response.text}")
            return []

    print("Failed after retries.")
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
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        # -------- STEP 1: SEARCH PAPER --------
        search_url = f"{RefBASE_URL}/paper/search"
        params = {
            "query": title,
            "limit": 1,
            "fields": "title,paperId"
        }

        res = requests.get(search_url, params=params, headers=headers, timeout=10)

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

        res = requests.get(ref_url, params=params, headers=headers, timeout=10)

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




