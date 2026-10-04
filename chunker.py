"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass
import re

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README
    parser_fallback: bool = False  # True when this document was not a thread

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


@dataclass(frozen=True)
class _ParsedThread:
    """The small, testable representation used while chunking one document."""

    header: str
    replies: list[tuple[str, str]]
    used_fallback: bool


def _sentences(text: str) -> list[str]:
    """Split prose into complete sentences, retaining punctuation."""
    return [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip())
        if sentence.strip()
    ]


def _split_long_sentence(sentence: str, limit: int) -> list[str]:
    """Use words, then a hard limit, if one sentence alone is oversized."""
    if len(sentence) <= limit:
        return [sentence]

    pieces: list[str] = []
    remaining = sentence
    while len(remaining) > limit:
        cut = remaining.rfind(" ", 0, limit + 1)
        if cut <= 0:
            cut = limit
        pieces.append(remaining[:cut].strip())
        remaining = remaining[cut:].strip()
    if remaining:
        pieces.append(remaining)
    return pieces


def _split_oversized_reply(
    label: str, body: str, header: str, chunk_size: int
) -> list[tuple[str, str]]:
    """Split only an oversized reply, preferring sentence boundaries."""
    # Leave room for a continuation label too; it is longer than the original
    # label and otherwise can push the later chunk over the configured limit.
    continuation_label = f"{label} (continued)"
    # The final layout also includes two newlines before the reply and one
    # newline between its label and body.
    room = chunk_size - len(header) - len(continuation_label) - 3
    if room <= 0:
        raise ValueError("CHUNK_SIZE is too small to hold a thread header and reply label")

    pieces: list[str] = []
    current: list[str] = []
    current_length = 0
    for sentence in _sentences(body) or [body.strip()]:
        for part in _split_long_sentence(sentence, room):
            added = len(part) + (1 if current else 0)
            if current and current_length + added > room:
                pieces.append(" ".join(current))
                current = []
                current_length = 0
            current.append(part)
            current_length += len(part) + (1 if current_length else 0)
    if current:
        pieces.append(" ".join(current))

    return [
        (label if number == 1 else f"{label} (continued)", piece)
        for number, piece in enumerate(pieces, 1)
    ]


def _parse_thread(document: Document) -> _ParsedThread:
    """Parse the expected thread format, making non-thread input visible."""
    match = re.match(r"^(THREAD:.*?)(?:\n\n|\n)(.*)$", document.text, flags=re.DOTALL)
    if not match:
        return _ParsedThread(
            header=f"SOURCE: {document.source}",
            replies=[("--- content ---", document.text.strip())],
            used_fallback=True,
        )

    header, remainder = match.groups()
    parts = re.split(r"(?m)^(--- reply \d+ \(\d+ votes\) ---)\n", remainder)
    replies = [
        (parts[position].strip(), parts[position + 1].strip())
        for position in range(1, len(parts) - 1, 2)
        if parts[position + 1].strip()
    ]
    if replies:
        return _ParsedThread(header.strip(), replies, used_fallback=False)

    return _ParsedThread(
        header=header.strip(),
        replies=[("--- content ---", remainder.strip())],
        used_fallback=True,
    )


def _make_chunk(header: str, overlap: list[str]) -> str:
    parts = [header]
    if overlap:
        parts.append("Previous context: " + " ".join(overlap))
    return "\n\n".join(parts)


def _append_part(chunk: str, part: str) -> str:
    return f"{chunk}\n\n{part}"


def _append_chunk(
    chunks: list[Chunk], document: Document, index: int, text: str, used_fallback: bool
) -> int:
    chunks.append(
        Chunk(
            text=text,
            source=document.source,
            index=index,
            produced_by="chunker.py::split_documents",
            parser_fallback=used_fallback,
        )
    )
    return index + 1


def _chunk_document(
    document: Document, chunk_size: int, sentence_overlap: int
) -> list[Chunk]:
    """Chunk one document without shared mutable state or nested functions."""
    parsed = _parse_thread(document)
    reply_queue: list[tuple[str, str]] = []
    for label, body in parsed.replies:
        whole_reply = f"{label}\n{body}"
        if len(_append_part(parsed.header, whole_reply)) > chunk_size:
            reply_queue.extend(
                _split_oversized_reply(label, body, parsed.header, chunk_size)
            )
        else:
            reply_queue.append((label, body))

    chunks: list[Chunk] = []
    current = _make_chunk(parsed.header, [])
    has_reply = False
    last_sentences: list[str] = []
    index = 0

    for label, body in reply_queue:
        reply = f"{label}\n{body}"
        if len(_append_part(current, reply)) > chunk_size and has_reply:
            index = _append_chunk(chunks, document, index, current, parsed.used_fallback)
            overlap = last_sentences[-sentence_overlap:] if sentence_overlap else []
            current = _make_chunk(parsed.header, overlap)
            has_reply = False

        # A complete reply can fit with its header but not after its overlap.
        # Keep the reply whole and omit overlap only when needed for the limit.
        if len(_append_part(current, reply)) > chunk_size and not has_reply:
            current = _make_chunk(parsed.header, [])

        if len(_append_part(current, reply)) > chunk_size:
            raise ValueError(
                f"Reply in {document.source} is still too large after sentence splitting"
            )

        current = _append_part(current, reply)
        has_reply = True
        last_sentences = _sentences(body) or [body]

    if has_reply:
        _append_chunk(chunks, document, index, current, parsed.used_fallback)
    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Coordinate reply-aware chunking for each input document."""
    chunk_size = config.CHUNK_SIZE
    sentence_overlap = config.SENTENCE_OVERLAP
    if chunk_size <= 0:
        raise ValueError("CHUNK_SIZE has to be positive")
    if sentence_overlap < 0:
        raise ValueError("SENTENCE_OVERLAP cannot be negative")

    chunks: list[Chunk] = []
    for document in documents:
        chunks.extend(_chunk_document(document, chunk_size, sentence_overlap))
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}, "
        f"parser fallback for {len({chunk.source for chunk in chunks if chunk.parser_fallback})} document(s)"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
