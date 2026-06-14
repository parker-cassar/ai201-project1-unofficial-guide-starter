"""Build the ChromaDB vector store from document chunks."""

from __future__ import annotations

from vector_store import build_vector_store, load_chunks_from_json


def main() -> None:
    chunks = load_chunks_from_json()
    collection = build_vector_store(chunks=chunks, reset=True)
    print(f"Embedded {collection.count()} chunks into ChromaDB")


if __name__ == "__main__":
    main()
