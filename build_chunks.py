"""Build and inspect document chunks for the RAG pipeline."""

from __future__ import annotations

import json
import random
from pathlib import Path

from chunking import chunk_documents
from ingest import load_documents

CHUNKS_PATH = Path(__file__).parent / "data" / "chunks.json"


def save_chunks(chunks, output_path: Path = CHUNKS_PATH) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "text": chunk.text,
            "source": chunk.source,
            "chunk_index": chunk.chunk_index,
        }
        for chunk in chunks
    ]
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    documents = load_documents()
    print(f"Loaded {len(documents)} documents\n")

    sample_doc = next(d for d in documents if d.filename == "02_life_top_5_libraries.txt")
    print("=" * 72)
    print("CLEANED DOCUMENT SAMPLE: 02_life_top_5_libraries.txt")
    print("=" * 72)
    print(sample_doc.cleaned_text[:1200])
    if len(sample_doc.cleaned_text) > 1200:
        print("\n[... truncated ...]")
    print()

    chunks = chunk_documents(documents)
    save_chunks(chunks)

    print("=" * 72)
    print(f"TOTAL CHUNKS: {len(chunks)}")
    print(f"Saved to: {CHUNKS_PATH}")
    print("=" * 72)
    print()

    by_source: dict[str, int] = {}
    for chunk in chunks:
        by_source[chunk.source] = by_source.get(chunk.source, 0) + 1
    print("Chunks per document:")
    for source, count in sorted(by_source.items()):
        print(f"  {source}: {count}")
    print()

    print("=" * 72)
    print("5 SAMPLE CHUNKS")
    print("=" * 72)
    random.seed(42)
    sample_chunks = random.sample(chunks, min(5, len(chunks)))
    for i, chunk in enumerate(sample_chunks, start=1):
        print(f"\n--- Chunk {i} | source: {chunk.source} | index: {chunk.chunk_index} ---")
        print(chunk.text)
        print(f"({len(chunk.text)} characters)")

    ishi_chunks = [c for c in chunks if "ishi court" in c.text.lower()]
    print("\n" + "=" * 72)
    print(f"ISHI COURT CHUNKS: {len(ishi_chunks)} found")
    print("=" * 72)
    if ishi_chunks:
        print(ishi_chunks[0].text)
        print(f"\nSource: {ishi_chunks[0].source} ({len(ishi_chunks[0].text)} characters)")


if __name__ == "__main__":
    main()
