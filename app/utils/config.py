import os
from dotenv import load_dotenv

load_dotenv()



ARXIV_API_URL = "http://export.arxiv.org/api/query"

# local Ollama by default; docker-compose overrides this with host.docker.internal
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")

SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

