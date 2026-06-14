"""Test retrieval with evaluation questions from planning.md."""

from __future__ import annotations

from vector_store import build_vector_store, load_chunks_from_json, retrieve

EVAL_QUERIES = [
    {
        "id": 1,
        "question": "Which library is ranked #1 for study spots and why?",
        "expected_sources": ["02_life_top_5_libraries.txt"],
        "relevance": "Should mention Moffitt as #1 with reasons like long hours, variety of spaces, and outlets.",
    },
    {
        "id": 2,
        "question": "Which libraries stay open until 2 a.m.?",
        "expected_sources": ["13_life_late_night.txt"],
        "relevance": "Should mention Main Stacks open until 2 a.m. (and possibly Moffitt 24h with renovation note).",
    },
    {
        "id": 3,
        "question": "Where is Ishi Court and how do students recommend finding it?",
        "expected_sources": [
            "05_visit_underground_spots.txt",
            "06_life_hidden_spots.txt",
        ],
        "relevance": "Should describe Ishi Court inside Dwinelle and recommend the North entrance.",
    },
    {
        "id": 4,
        "question": "What do students say about Delah Coffee as a Northside study spot?",
        "expected_sources": [
            "07_life_northside_cafes.txt",
            "10_visit_cafe_ranking.txt",
        ],
        "relevance": "Should mention Delah on Euclid with outlets, quiet music, and studious vibe.",
    },
]


def print_results(query_info: dict) -> None:
    question = query_info["question"]
    print("=" * 72)
    print(f"Query {query_info['id']}: {question}")
    print(f"Expected relevance: {query_info['relevance']}")
    print("=" * 72)

    results = retrieve(question, k=5)
    for rank, result in enumerate(results, start=1):
        print(f"\n--- Rank {rank} | distance: {result.distance:.4f} ---")
        print(f"Source: {result.source} (chunk {result.chunk_index})")
        print(result.text[:500])
        if len(result.text) > 500:
            print("[... truncated ...]")

    top = results[0]
    source_match = top.source in query_info["expected_sources"]
    any_source_match = any(r.source in query_info["expected_sources"] for r in results)
    print(
        f"\nTop result source match: {'yes' if source_match else 'no'} "
        f"(got {top.source}, expected one of {query_info['expected_sources']})"
    )
    print(
        f"Any top-{len(results)} source match: "
        f"{'yes' if any_source_match else 'no'}"
    )
    print(f"Top distance: {top.distance:.4f} ({'good' if top.distance < 0.5 else 'weak'})")
    print()


def main() -> None:
    print("Building vector store from chunks...")
    chunks = load_chunks_from_json()
    build_vector_store(chunks=chunks, reset=True)
    print(f"Indexed {len(chunks)} chunks\n")

    for query_info in EVAL_QUERIES:
        print_results(query_info)


if __name__ == "__main__":
    main()
