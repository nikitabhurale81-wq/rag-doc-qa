"""CLI: index every supported document inside ./data

Usage:  python -m scripts.ingest_data [folder]
"""
import glob
import sys

from app.services.ingest_service import IngestService

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "data"
    files = sorted(
        glob.glob(f"{folder}/*.pdf") + glob.glob(f"{folder}/*.txt") + glob.glob(f"{folder}/*.md")
    )
    if not files:
        print(f"No documents found in {folder}/")
        sys.exit(0)
    service = IngestService()
    for f in files:
        print(service.ingest_file(f))
