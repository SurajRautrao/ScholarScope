import json
import re

import ollama
from app.utils.config import OLLAMA_HOST

client = ollama.Client(host=OLLAMA_HOST)

def planner_agent(query):
    prompt = f"""
    Break the following research question into:

    - main topic
    - keywords (important terms)
    - subtopics (if any)
    - search queries (3 variations)

    Question:
    {query}

    Return only a JSON object with these keys:
    "main_topic" (string), "keywords" (list of strings),
    "subtopics" (list of strings), "search_queries" (list of 3 strings).
    """

    response = client.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}],
        format="json"
    )

    content = response['message']['content']

    plan = _parse_plan(content)

    queries = plan.get("search_queries") if plan else None
    if isinstance(queries, list):
        queries = [q.strip() for q in queries if isinstance(q, str) and q.strip()]

    if plan and queries:
        plan["search_queries"] = queries
    else:
        plan = {
            "query": query,
            "keywords": query.split(),
            "subtopics": [],
            "search_queries": [query]
        }

    return plan


def _parse_plan(content):
    # LLMs often wrap JSON in ```json fences or add prose around it
    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip())
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None
