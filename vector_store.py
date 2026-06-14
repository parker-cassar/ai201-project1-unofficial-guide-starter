"""Embed chunks and retrieve from ChromaDB for the Berkeley study spots RAG pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import chromadb
from chromadb.errors import NotFoundError
from chromadb.utils import embedding_functions

from chunking import Chunk, chunk_documents
from ingest import load_documents

CHUNKS_PATH = Path(__file__).parent / "data" / "chunks.json"
CHROMA_PATH = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "berkeley_study_spots"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 5


def get_chroma_client(persist_path: Path = CHROMA_PATH) -> chromadb.PersistentClient:
    persist_path.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(persist_path))


@dataclass
class RetrievedChunk:
    text: str
    source: str
    chunk_index: int
    distance: float


def load_chunks_from_json(path: Path = CHUNKS_PATH) -> list[Chunk]:
    """Load pre-built chunks from JSON."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        Chunk(
            text=item["text"],
            source=item["source"],
            chunk_index=item["chunk_index"],
        )
        for item in payload
    ]


def get_embedding_function() -> embedding_functions.SentenceTransformerEmbeddingFunction:
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )


def get_or_create_collection(
    client: chromadb.PersistentClient | None = None,
) -> chromadb.Collection:
    client = client or get_chroma_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )


def _chunk_id(chunk: Chunk) -> str:
    return f"{chunk.source}::{chunk.chunk_index}"


def build_vector_store(
    chunks: list[Chunk] | None = None,
    reset: bool = True,
) -> chromadb.Collection:
    """Embed all chunks and persist them to ChromaDB."""
    if chunks is None:
        if CHUNKS_PATH.exists():
            chunks = load_chunks_from_json()
        else:
            chunks = chunk_documents(load_documents())

    client = get_chroma_client()
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except (ValueError, NotFoundError):
            pass

    collection = get_or_create_collection(client)
    collection.add(
        ids=[_chunk_id(chunk) for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        metadatas=[
            {"source": chunk.source, "chunk_index": chunk.chunk_index}
            for chunk in chunks
        ],
    )
    return collection


def retrieve(
    query: str,
    k: int = DEFAULT_TOP_K,
    collection: chromadb.Collection | None = None,
) -> list[RetrievedChunk]:
    """Return the top-k most relevant chunks for a query."""
    collection = collection or get_or_create_collection()
    results = collection.query(query_texts=[query], n_results=k)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved: list[RetrievedChunk] = []
    for text, metadata, distance in zip(documents, metadatas, distances):
        retrieved.append(
            RetrievedChunk(
                text=text,
                source=metadata["source"],
                chunk_index=metadata["chunk_index"],
                distance=distance,
            )
        )
    return retrieved
