from app.utils.pdf_reader import extract_text_from_pdf
from app.rag.chunker import chunk_text
from app.rag.pdf_retriever import retrieve_relevant_chunks
from app.agents.pdf_analyst import analyze_pdf

def run_pdf_pipeline(file_path, query="Explain this paper"):
    print("\n[1] Extracting text from PDF...")
    text = extract_text_from_pdf(file_path)

    print("\n--- Sample Extracted Text ---")
    print(text[:500])
    
    print("\n[2] Chunking text...")
    chunks = chunk_text(text)

    print(f"Total chunks: {len(chunks)}")

    print("\n[3] Retrieving relevant chunks...")
    top_chunks = retrieve_relevant_chunks(query, chunks, k=5)

    print("\n[4] Analyzing paper...")
    result = analyze_pdf(top_chunks)

    return result
