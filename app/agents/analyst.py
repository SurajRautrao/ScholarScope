import ollama
from app.utils.config import OLLAMA_HOST

client = ollama.Client(host=OLLAMA_HOST)

def analyze_paper(paper):
    prompt = f"""
    Extract structured information from the following research paper.

    Title: {paper.get("title", "")}
    Abstract: {paper.get("summary", "")}

    Provide output in this format:

    - Problem:
    - Method:
    - Key Results:
    - Limitations:
    """

    response = client.chat(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']
