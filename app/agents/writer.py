import ollama
from app.utils.config import OLLAMA_HOST

client = ollama.Client(host=OLLAMA_HOST)


def writer_agent(query, papers):
    context = ""

    for p in papers:
        context += f"\nTitle: {p['title']}\n"
        context += f"{p['analysis']}\n"

    prompt = f"""
    Write a structured review based on the following analyzed papers.

    Research Question: {query}

    Analyzed Papers:
    {context}

    Structure:
    - Introduction
    - Key Methods
    - Comparison of Approaches
    - Trends
    - Conclusion
    """

    response = client.chat(
        model="gemma3:12b",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "text": response['message']['content'],
        "sources": papers
    }

