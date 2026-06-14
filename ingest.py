"""Document loading and cleaning for the Berkeley study spots RAG pipeline."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

DOCUMENTS_DIR = Path(__file__).parent / "documents"

REDDIT_UI_LINES = {
    "upvote",
    "downvote",
    "reply",
    "share",
    "award",
    "go to comments",
    "join the conversation",
    "sort by:",
    "best",
    "comments section",
    "op",
    "[deleted]",
}

REDDIT_UI_PATTERN = re.compile(
    r"^(Upvote|Downvote|Reply|Share|Award|Go to comments|Join the conversation|"
    r"Sort by:|Best|Comments Section|\d+)$",
    re.IGNORECASE,
)
AVATAR_LINE = re.compile(r"^u/.+avatar$", re.IGNORECASE)
USERNAME_LINE = re.compile(r"^u/[A-Za-z0-9_]+$")
TIME_AGO_LINE = re.compile(r"^\d+[mhdwy]\s+ago$", re.IGNORECASE)
BULLET_ONLY = re.compile(r"^•$")
HTML_TAG = re.compile(r"<[^>]+>")
COLLAGE_LINE = re.compile(r"^A collage of", re.IGNORECASE)
DECORATIVE_IMAGE = re.compile(r"^decorative image$", re.IGNORECASE)
HEADER_LINE = re.compile(r"^(Source|Title):\s*.+", re.IGNORECASE)
PAGE_FOOTER = re.compile(
    r"^(Samantha Herrera|Reva Gokhale|Megan W\.|Meghaa R\.).*$", re.IGNORECASE
)
INSTAGRAM_BOILERPLATE = re.compile(
    r"^(Follow on Instagram|ucberkeleylife|\d+)$", re.IGNORECASE
)


@dataclass
class Document:
    filename: str
    source_url: str
    title: str
    raw_text: str
    cleaned_text: str


def load_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[Document]:
    """Load all .txt files from the documents directory."""
    documents: list[Document] = []
    for path in sorted(documents_dir.glob("*.txt")):
        raw_text = path.read_text(encoding="utf-8")
        source_url, title, body = _parse_header(raw_text)
        cleaned_text = clean_text(body, filename=path.name)
        documents.append(
            Document(
                filename=path.name,
                source_url=source_url,
                title=title,
                raw_text=raw_text,
                cleaned_text=cleaned_text,
            )
        )
    return documents


def _parse_header(text: str) -> tuple[str, str, str]:
    lines = text.splitlines()
    source_url = ""
    title = ""
    body_start = 0

    for i, line in enumerate(lines):
        if line.lower().startswith("source:"):
            source_url = line.split(":", 1)[1].strip()
            body_start = i + 1
        elif line.lower().startswith("title:"):
            title = line.split(":", 1)[1].strip()
            body_start = i + 1
        elif line.strip() == "":
            continue
        else:
            break

    while body_start < len(lines) and lines[body_start].strip() == "":
        body_start += 1

    body = "\n".join(lines[body_start:])
    return source_url, title, body


def clean_text(text: str, filename: str = "") -> str:
    """Remove boilerplate and normalize whitespace."""
    text = html.unescape(text)
    text = HTML_TAG.sub("", text)

    if filename == "01_reddit_study_spots.txt":
        return _clean_reddit_thread(text)

    lines = text.splitlines()
    cleaned_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue
        if HEADER_LINE.match(stripped):
            continue
        if COLLAGE_LINE.match(stripped) or DECORATIVE_IMAGE.match(stripped):
            continue
        if PAGE_FOOTER.match(stripped) or INSTAGRAM_BOILERPLATE.match(stripped):
            continue
        if stripped.lower().startswith("for more ideas, see our ig"):
            break
        cleaned_lines.append(stripped)

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _clean_reddit_thread(text: str) -> str:
    """Extract substantive post and replies from Reddit paste."""
    lines = text.splitlines()
    blocks: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if not current:
            return
        block = "\n".join(current).strip()
        if _is_substantive_reddit_block(block):
            blocks.append(block)
        current.clear()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        if (
            REDDIT_UI_PATTERN.match(line)
            or AVATAR_LINE.match(line)
            or USERNAME_LINE.match(line)
            or TIME_AGO_LINE.match(line)
            or BULLET_ONLY.match(line)
            or line.lower() in REDDIT_UI_LINES
        ):
            flush()
            i += 1
            continue

        if line.startswith("u/") and "avatar" not in line.lower():
            flush()
            i += 1
            continue

        current.append(line)
        i += 1

    flush()

    # Keep OP question as first block if present
    if not blocks:
        return text.strip()

    return "\n\n---REPLY---\n\n".join(blocks)


def _is_substantive_reddit_block(block: str) -> bool:
    if len(block) < 25:
        return False
    lower = block.lower()
    if lower.startswith("[paste"):
        return False
    if lower.startswith("op:") and "recommends" in lower and len(block) < 120:
        return False
    if lower in {"lol, thank you for clarifying and pointing that out!"}:
        return False
    noise_phrases = ("upvote", "downvote", "join the conversation")
    return not any(phrase in lower for phrase in noise_phrases)
