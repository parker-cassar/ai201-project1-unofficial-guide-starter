"""Grounded answer generation for the Berkeley study spots RAG pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from groq import Groq

from vector_store import DEFAULT_TOP_K, RetrievedChunk, retrieve

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"
REFUSAL_MESSAGE = "I don't have enough information on that."
MAX_CONTEXT_DISTANCE = 0.65

SYSTEM_PROMPT = """You are The Unofficial Guide, a Berkeley study spots assistant.

Rules:
1. Answer ONLY using the provided document excerpts. Do not use outside knowledge.
2. If the excerpts do not contain enough information to answer the question, respond with exactly: "I don't have enough information on that."
3. When you state a fact, mention which source file it came from (use the filename shown in brackets, e.g. 07_life_northside_cafes.txt).
4. Do not invent study spots, hours, or student opinions that are not supported by the excerpts.
5. Keep answers concise, practical, and grounded in the retrieved text."""


@dataclass
class AnswerResult:
    answer: str
    sources: list[str]
    chunks: list[RetrievedChunk]


def _get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your Groq API key."
        )
    return Groq(api_key=api_key)


def _format_context(chunks: list[RetrievedChunk]) -> str:
    parts: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        parts.append(
            f"[Source: {chunk.source} | chunk {chunk.chunk_index}]\n{chunk.text}"
        )
    return "\n\n---\n\n".join(parts)


def _should_refuse(chunks: list[RetrievedChunk]) -> bool:
    if not chunks:
        return True
    return chunks[0].distance > MAX_CONTEXT_DISTANCE


def ask(question: str, k: int = DEFAULT_TOP_K) -> dict:
    """Retrieve relevant chunks and generate a grounded answer."""
    question = question.strip()
    if not question:
        return {"answer": "Please enter a question.", "sources": []}

    chunks = retrieve(question, k=k)
    sources = sorted({chunk.source for chunk in chunks})

    if _should_refuse(chunks):
        return {
            "answer": REFUSAL_MESSAGE,
            "sources": sources,
        }

    context = _format_context(chunks)
    user_prompt = f"""Document excerpts:

{context}

Question: {question}

Answer using only the document excerpts above:"""

    client = _get_client()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )

    answer = response.choices[0].message.content or REFUSAL_MESSAGE
    if not any(source in answer for source in sources) and answer != REFUSAL_MESSAGE:
        cited = ", ".join(sources)
        answer = f"{answer}\n\nSources: {cited}"

    return {"answer": answer, "sources": sources}
