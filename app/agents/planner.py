import ollama
client = ollama.Client(host="http://host.docker.internal:11434")

def planner_agent(query):
    prompt = f"""
    Break the following research question into:

    - main topic
    - keywords (important terms)
    - subtopics (if any)
    - search queries (3 variations)

    Question:
    {query}

    Return in JSON format.
    """

    response = client.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['message']['content']

    #  simple fallback parsing (safe)
    try:
        import json
        plan = json.loads(content)
    except:
        plan = {
            "query": query,
            "keywords": query.split(),
            "subtopics": [],
            "search_queries": [query]
        }

    return plan
