import ollama
from app.utils.config import OLLAMA_HOST

client = ollama.Client(host=OLLAMA_HOST)

def critic_agent(query, analyzed_papers):
    context = ""

    for p in analyzed_papers:
        context += f"\nTitle: {p['title']}\n"
        context += f"{p['analysis']}\n"

    prompt = f"""
    You are a critic reviewing a literature analysis system.

    Research Question:
    {query}

    Analyzed Papers:
    {context}

    Evaluate the following:

    1. Relevance of each paper to the query
    2. Quality of extracted analysis
    3. Any inconsistencies or hallucinations
    4. Missing important aspects
    5. Overall quality score (1-10)

    Provide structured feedback.
    """

    response = client.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']
