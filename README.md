
---

# ScholarScope

> AI-powered research assistant for literature review, citation analysis, and knowledge graph visualization.
> ScholarScope uses a multi-agent architecture built with LangGraph, where each node performs a specialized task in the research pipeline.

Problem Statement:

Researchers and students often spend hours manually searching, reading, and synthesizing academic papers from large databases. This process is slow, repetitive, and difficult to scale when dealing with large volumes of literature.

ScholarScope automates this workflow by using AI agents to retrieve, analyze, and summarize research papers, while also visualizing citation relationships to help users understand connections in the literature faster.

It transforms raw academic search into a structured, interactive research exploration experience.

---

## Overview

ScholarScope is an intelligent research assistant that helps users explore scientific literature efficiently.
It combines **Retrieval-Augmented Generation (RAG)**, **LangGraph orchestration**, and a **local LLM (Ollama)** to generate structured research summaries, extract key insights, and visualize citation relationships.

Unlike simple chatbot-based systems, ScholarScope uses a **multi-agent pipeline (LangGraph)** to break down complex research tasks into structured steps such as retrieval, analysis, synthesis, and visualization.

The system supports:

* Research queries (literature review)
* PDF-based analysis

---
## User Interface

**Main UI**
- Research Query
<img width="1910" height="862" alt="research query" src="https://github.com/user-attachments/assets/77cdcb18-1440-47c0-8711-4d41c1c2a3ce" />

- Pdf Upload
<img width="1917" height="875" alt="pdf upload" src="https://github.com/user-attachments/assets/add47358-ef25-4fcc-871a-e6d56d96726f" />

**Research Results:**
<img width="1918" height="867" alt="query result" src="https://github.com/user-attachments/assets/d104b9ef-37f3-43eb-ae98-d692537852f6" />

**References and Citation Graphs:**
<img width="1855" height="848" alt="citation graph" src="https://github.com/user-attachments/assets/81feaa8e-809e-4c86-8758-555dd71d2ce8" />

**Pdf Analysis Results:**
<img width="1918" height="872" alt="pdf results" src="https://github.com/user-attachments/assets/eaab8ca4-6715-4e44-8dde-6b85fa3eec75" />

## Agents Explained

### 1. Query Processing Agent

* Cleans and reformulates the user query using Mistral 7B LLM
* Prepares query for retrieval
* Improves semantic matching

### 2. Paper Retrieval Agent

* Fetches top research papers based on query
* Uses external APIs (e.g., arXiv, Semantic Scholar)
* Outputs structured paper metadata:
  * Title
  * Abstract
  * Citations
  * Links

### 3. Paper Analysis Agent

* Extracts key insights from each paper using Gemma3:4B
* Identifies:
  * Problem
  * Method
  * Results
  * Limitations

### 4. Synthesis Agent (LLM - Ollama)

* Combines insights from multiple papers using Gemma3:12B
* Generates:
  * Structured literature review
  * Comparisons
  * Trends
* Uses local LLM via Ollama

### 5. Citation Graph Agent

* Builds citation relationships between papers
* Uses NetworkX for graph structure
* Uses PyVis for interactive visualization
* Outputs HTML graph

---

## Features

* Research query processing using RAG (LangGraph pipeline)
* PDF analysis support
* AI-generated structured literature reviews
* Clickable research paper references
* Interactive citation graph visualization
* Chat history management (mode-based)

---

## Tech Stack

| Layer               | Technology         |
| ------------------- | ------------------ |
| Frontend            | Streamlit          |
| Backend             | FastAPI            |
| LLM                 | Ollama (Local LLM) |
| Orchestration       | LangGraph          |
| Graph Visualization | NetworkX + PyVis   |
| Containerization    | Docker             |

---

## Architecture

```text
User Query
    ↓
Streamlit UI
    ↓
FastAPI Backend
    ↓
LangGraph Pipeline
    ├── Retrieval (papers)
    ├── LLM reasoning (Ollama)
    ├── Citation Graph generation
    ↓
Response (Result + Sources + Graph)
```

---

## LangGraph Execution Flow

The pipeline is orchestrated using LangGraph:
* Each agent is represented as a node
* Data is passed via a shared state object

Execution:

```python
graph.invoke({"query": query})
```

---

## State Management

Each step updates a shared state object:

```python
state = {
    "query": str,
    "top_papers": list,
    "analysis": list,
    "result": str,
    "sources": list,
    "graph_path": str
}
```

---

## How Components Work Together

1. User enters a query in Streamlit
2. Request is sent to FastAPI
3. FastAPI triggers LangGraph pipeline
4. Each agent processes step-by-step
5. Final output includes:
   * Research summary
   * References
   * Citation graph

---

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/scholarscope.git
cd scholarscope
```

### 2. Start Using Docker

```bash
docker-compose up --build
```

### 3. Run Ollama (Required)

Make sure Ollama is running:

```bash
ollama serve
```

### 4. Access Application

* Frontend: [http://localhost:8501](http://localhost:8501)
* Backend: [http://localhost:8000](http://localhost:8000)

---

## Important Notes

* This project uses a local LLM (Ollama)
* Ensure required models are installed (e.g., mistral, llama3)

---

## Limitations

* Citation API rate limits (Semantic Scholar)
* Graph depth limited to avoid overload
* Requires local setup (no cloud deployment yet)

---

## Future Improvements

* Cloud deployment (GPU support)
* User authentication system
* Caching for research APIs
* Advanced graph analytics
* Improved ranking of research papers

---

## License

This project is licensed under the MIT License.

---

## Author

**Suraj Rautrao**
-  MSc Digital Engineering (Otto Von Guericke Universität Magdeburg, Germany)
