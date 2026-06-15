"""Run all 5 planning.md evaluation questions and print detailed results."""

from __future__ import annotations

import json

from query import ask
from vector_store import retrieve

EVAL_QUESTIONS = [
  "Which library is ranked #1 for study spots and why?",
  "Which libraries stay open until 2 a.m.?",
  "Where is Ishi Court and how do students recommend finding it?",
  "What do students say about Delah Coffee as a Northside study spot?",
  "What non-library spots do r/berkeley users recommend for studying?",
]


def main() -> None:
    results = []
    for i, question in enumerate(EVAL_QUESTIONS, start=1):
        chunks = retrieve(question, k=5)
        answer = ask(question)
        entry = {
            "id": i,
            "question": question,
            "answer": answer["answer"],
            "sources": answer["sources"],
            "retrieved": [
                {
                    "source": c.source,
                    "chunk_index": c.chunk_index,
                    "distance": c.distance,
                    "text_preview": c.text[:200],
                }
                for c in chunks
            ],
        }
        results.append(entry)
        print(json.dumps(entry, indent=2, ensure_ascii=False))
        print("\n" + "=" * 72 + "\n")

    with open("data/evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
