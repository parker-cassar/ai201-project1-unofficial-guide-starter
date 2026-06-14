"""Structure-aware chunking for the Berkeley study spots RAG pipeline."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ingest import Document

CHUNK_TARGET = 500
CHUNK_MAX = 700
CHUNK_MIN = 80
CHUNK_OVERLAP = 90

NUMBERED_SECTION = re.compile(r"^\d+\.\s+.+$", re.MULTILINE)
LAW_SEPARATOR = re.compile(r"\n---\n")
REDDIT_REPLY_SEPARATOR = re.compile(r"\n---REPLY---\n")
RANKED_LIBRARY = re.compile(r"^\d+\.\s+[A-Za-z].+$", re.MULTILINE)
APOSTROPHE = r"['\u2019]"
SPOT_HEADER = re.compile(
    rf"^(Ishi Court|Women{APOSTROPHE}s Faculty Club Garden|Courtyard of Latimer Hall|"
    rf"Haas Courtyard|Wurster Library|For Grad Students: Inclusive Excellence Hub)$",
    re.MULTILINE,
)
CAFE_HEADER = re.compile(
    r"^([A-Z][A-Za-z0-9 &'/-]+(?:Cafe|Coffee|Dining Commons)):",
    re.MULTILINE,
)
SIMONS_SECTION = re.compile(r"^(Cafés|Breakfast|Lunch|Dinner)\s*»?\s*$", re.MULTILINE)


@dataclass
class Chunk:
    text: str
    source: str
    chunk_index: int


def chunk_documents(documents: list[Document]) -> list[Chunk]:
    """Chunk all cleaned documents with source metadata."""
    all_chunks: list[Chunk] = []
    for doc in documents:
        sections = _split_into_sections(doc.cleaned_text, doc.filename)
        doc_chunks: list[str] = []
        for section in sections:
            doc_chunks.extend(_chunk_section(section))

        for index, text in enumerate(doc_chunks):
            all_chunks.append(
                Chunk(text=text, source=doc.filename, chunk_index=index)
            )
    return all_chunks


def _split_into_sections(text: str, filename: str) -> list[str]:
    if filename == "01_reddit_study_spots.txt":
        return [s.strip() for s in REDDIT_REPLY_SEPARATOR.split(text) if s.strip()]

    if filename == "14_law_mindfulness_guide.txt":
        sections = [s.strip() for s in LAW_SEPARATOR.split(text) if s.strip()]
        return [_strip_law_page_numbers(s) for s in sections if len(s.strip()) > 40]

    if filename in {"05_visit_underground_spots.txt", "02_life_top_5_libraries.txt"}:
        return _split_on_pattern(text, RANKED_LIBRARY)

    if filename == "06_life_hidden_spots.txt":
        return _split_on_pattern(text, SPOT_HEADER)

    if filename == "07_life_northside_cafes.txt":
        return _split_on_pattern(text, CAFE_HEADER)

    if filename == "15_simons_restaurants.txt":
        return _split_simons_list(text)

    if filename == "13_life_late_night.txt":
        return _split_late_night(text)

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return _merge_small_paragraphs(paragraphs, merge_limit=350)


def _split_on_pattern(text: str, pattern: re.Pattern[str]) -> list[str]:
    matches = list(pattern.finditer(text))
    if not matches:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        return _merge_small_paragraphs(paragraphs, merge_limit=350)

    sections: list[str] = []
    preamble = text[: matches[0].start()].strip()
    if preamble and len(preamble) > 60:
        sections.append(preamble)

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end].strip()
        if i + 1 < len(matches):
            next_header = matches[i + 1].group(0).strip()
            header_pos = section.rfind(next_header)
            if header_pos != -1 and header_pos >= len(section) - len(next_header) - 2:
                section = section[:header_pos].strip()
        if section:
            sections.append(section)

    return sections


def _split_simons_list(text: str) -> list[str]:
    sections = _split_on_pattern(text, SIMONS_SECTION)
    if len(sections) > 1:
        return sections
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    grouped: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.endswith("»") or line in {"Cafés", "Breakfast", "Lunch", "Dinner"}:
            if current:
                grouped.append("\n".join(current))
            current = [line]
        else:
            current.append(line)
    if current:
        grouped.append("\n".join(current))
    return grouped or [text]


def _split_late_night(text: str) -> list[str]:
    markers = [
        "Where to Study",
        "Where to Grab a Bite",
        "Evening Activities",
        "Services to Get Home Safely",
        "Enjoy Berkeley at Night!",
    ]
    sections: list[str] = []
    for i, marker in enumerate(markers):
        start = text.find(marker)
        if start == -1:
            continue
        end = text.find(markers[i + 1]) if i + 1 < len(markers) else len(text)
        section = text[start:end].strip()
        if section:
            sections.append(section)
    return sections or [text]


def _strip_law_page_numbers(section: str) -> str:
    lines = section.splitlines()
    cleaned = [
        line
        for line in lines
        if not re.fullmatch(r"\d+", line.strip())
        and line.strip() != "Mindfulness Initiative Guide to Peaceful Campus Spots"
    ]
    return "\n".join(cleaned).strip()


def _merge_small_paragraphs(paragraphs: list[str], merge_limit: int) -> list[str]:
    if not paragraphs:
        return []

    merged: list[str] = []
    current = paragraphs[0]
    for para in paragraphs[1:]:
        if len(current) < merge_limit and len(current) + len(para) + 2 <= CHUNK_MAX:
            current = f"{current}\n\n{para}"
        else:
            merged.append(current)
            current = para
    merged.append(current)
    return merged


def _chunk_section(section: str) -> list[str]:
    section = section.strip()
    if not section:
        return []

    if len(section) <= CHUNK_MAX:
        return [section] if len(section) >= CHUNK_MIN else []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", section) if p.strip()]
    raw_chunks: list[str] = []
    current = ""

    for para in paragraphs:
        candidate = f"{current}\n\n{para}".strip() if current else para
        if len(candidate) <= CHUNK_MAX:
            current = candidate
        else:
            if current:
                raw_chunks.append(current)
            if len(para) > CHUNK_MAX:
                raw_chunks.extend(_split_by_sentences(para))
                current = ""
            else:
                current = para

    if current:
        raw_chunks.append(current)

    return _apply_overlap(raw_chunks)


def _split_by_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        candidate = f"{current} {sentence}".strip() if current else sentence
        if len(candidate) <= CHUNK_MAX:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(sentence) > CHUNK_MAX:
                for i in range(0, len(sentence), CHUNK_TARGET):
                    piece = sentence[i : i + CHUNK_MAX]
                    if len(piece) >= CHUNK_MIN:
                        chunks.append(piece)
                current = ""
            else:
                current = sentence

    if current:
        chunks.append(current)
    return chunks


def _apply_overlap(chunks: list[str]) -> list[str]:
    if len(chunks) <= 1:
        return [c for c in chunks if len(c.strip()) >= CHUNK_MIN]

    overlapped: list[str] = [chunks[0]]
    for chunk in chunks[1:]:
        prev = overlapped[-1]
        paragraphs = [p.strip() for p in prev.split("\n\n") if p.strip()]
        if paragraphs:
            tail = paragraphs[-1]
            if (
                len(tail) <= CHUNK_OVERLAP
                and tail not in chunk
                and len(tail) + len(chunk) + 2 <= CHUNK_MAX
            ):
                overlapped.append(f"{tail}\n\n{chunk}")
                continue
        overlapped.append(chunk)

    return [c.strip() for c in overlapped if len(c.strip()) >= CHUNK_MIN]
