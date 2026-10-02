import ollama
from app.utils.config import OLLAMA_HOST

client = ollama.Client(host=OLLAMA_HOST)


def analyze_pdf(chunks):
    context = "\n\n".join(chunks[:3])  # only top 3 chunks

    prompt = f"""
    You are a research assistant.

    Explain the following research paper in a clear and structured way.

    Focus on:
    - What problem the paper solves
    - What method is used
    - Key results
    - Limitations
    - Simple explanation for beginners

    Content:
    {context}

    Provide a clear and detailed answer.
    """

    response = client.chat(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']
