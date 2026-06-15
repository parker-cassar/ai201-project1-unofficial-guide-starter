"""Gradio web UI for The Unofficial Guide."""

from __future__ import annotations

import gradio as gr

from query import ask
from vector_store import build_vector_store, get_or_create_collection, load_chunks_from_json


def ensure_index() -> None:
    """Build the vector store if ChromaDB is empty."""
    try:
        collection = get_or_create_collection()
        if collection.count() == 0:
            chunks = load_chunks_from_json()
            build_vector_store(chunks=chunks, reset=True)
    except Exception:
        chunks = load_chunks_from_json()
        build_vector_store(chunks=chunks, reset=True)


def handle_query(question: str) -> tuple[str, str]:
    result = ask(question)
    sources = "\n".join(f"• {source}" for source in result["sources"])
    return result["answer"], sources


def main() -> None:
    ensure_index()

    with gr.Blocks(title="The Unofficial Guide — Berkeley Study Spots") as demo:
        gr.Markdown(
            "# The Unofficial Guide\n"
            "Ask about Berkeley study spots — libraries, cafés, hidden corners, and late-night options. "
            "Answers are grounded in student blogs, guides, and forum posts."
        )
        question = gr.Textbox(
            label="Your question",
            placeholder="Where can I study late on campus?",
            lines=2,
        )
        ask_button = gr.Button("Ask", variant="primary")
        answer = gr.Textbox(label="Answer", lines=10)
        sources = gr.Textbox(label="Retrieved from", lines=4)

        ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
        question.submit(handle_query, inputs=question, outputs=[answer, sources])

    demo.launch()


if __name__ == "__main__":
    main()
