from fastapi import FastAPI
from app.pipelines.pipeline import run_pipeline

app = FastAPI(
    title="Scientific Research Assistant API",
    description="Multi-agent research assistant using RAG",
    version="1.0"
)


@app.get("/")
def root():
    return {"message": "API is running 🚀"}


@app.get("/research")
def research(query: str):
    try:
        output = run_pipeline(query)

        return {
            "query": query,
            "result": output.get("result", ""),
            "sources": output.get("sources", []),
            "graph_path": output.get("graph_path", None)
        }

    except Exception as e:
        return {"error": str(e)}





