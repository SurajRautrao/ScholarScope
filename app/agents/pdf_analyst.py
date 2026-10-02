import ollama
from app.utils.config import OLLAMA_HOST

client = ollama.Client(host=OLLAMA_HOST)


def analyze_pdf(chunks):
    context = "\n\n[...]\n\n".join(chunks)

    prompt = f"""
    You are a research assistant.

    Explain the following research paper in a clear and structured way.

    The content is excerpts from the paper in document order, starting with
    the title and abstract; "[...]" marks skipped sections. Base your answer
    only on this content. If something (e.g. results) is not covered, say so
    instead of guessing.

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
        messages=[{"role": "user", "content": prompt}],
        # Ollama's default context is too small for ~2,500 words of excerpts
        # and silently truncates the prompt
        options={"num_ctx": 8192}
    )

    return response['message']['content']
