"""CLI helper: index every PDF/TXT file inside ./data into the vector store.

Usage:  python ingest.py
"""
import glob

from rag_pipeline import RAGPipeline

if __name__ == "__main__":
    pipe = RAGPipeline()
    files = glob.glob("data/*.pdf") + glob.glob("data/*.txt")
    if not files:
        print("No documents found in ./data — add a PDF or TXT file first.")
    for f in files:
        print(f"{f}: {pipe.ingest(f)} chunks indexed")
