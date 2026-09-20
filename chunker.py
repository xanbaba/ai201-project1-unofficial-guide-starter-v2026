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


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks. ⚠️ REPLACE THE BODY OF THIS IN MILESTONE 3.

    Advice threads are split at reply boundaries. Every chunk repeats the
    original `THREAD:` question; continuation chunks also retain the previous
    chunk's last sentence as context. A reply moves to the next chunk when it
    would exceed the limit, and only an oversized reply is split by sentences.
    """
    chunk_size = config.CHUNK_SIZE
    sentence_overlap = config.SENTENCE_OVERLAP
    if chunk_size <= 0:
        raise ValueError("CHUNK_SIZE has to be positive")
    if sentence_overlap < 0:
        raise ValueError("SENTENCE_OVERLAP cannot be negative")

    def sentences(text: str) -> list[str]:
        """Split prose into complete sentences, retaining punctuation."""
        return [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", text.strip())
            if sentence.strip()
        ]

    def split_long_sentence(sentence: str, limit: int) -> list[str]:
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

    def split_oversized_reply(label: str, body: str, header: str) -> list[tuple[str, str]]:
        """Make sentence-sized pieces only when a reply cannot stand alone."""
        room = chunk_size - len(header) - len(label) - 2
        if room <= 0:
            raise ValueError("CHUNK_SIZE is too small to hold a thread header and reply label")

        pieces: list[str] = []
        current: list[str] = []
        current_length = 0
        for sentence in sentences(body) or [body.strip()]:
            for part in split_long_sentence(sentence, room):
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

    def parse_thread(text: str) -> tuple[str, list[tuple[str, str]]]:
        """Return a thread question and its labelled replies."""
        match = re.match(r"^(THREAD:.*?)(?:\n\n|\n)(.*)$", text, flags=re.DOTALL)
        if not match:
            return "THREAD: Context", [("--- content ---", text)]

        header, remainder = match.groups()
        parts = re.split(r"(?m)^(--- reply \d+ \(\d+ votes\) ---)\n", remainder)
        replies = [
            (parts[position].strip(), parts[position + 1].strip())
            for position in range(1, len(parts) - 1, 2)
            if parts[position + 1].strip()
        ]
        return header.strip(), replies or [("--- content ---", remainder.strip())]

    def make_chunk(header: str, overlap: list[str]) -> str:
        parts = [header]
        if overlap:
            parts.append("Previous context: " + " ".join(overlap))
        return "\n\n".join(parts)

    def append_part(chunk: str, part: str) -> str:
        return f"{chunk}\n\n{part}"

    chunks: list[Chunk] = []
    for doc in documents:
        header, replies = parse_thread(doc.text)
        reply_queue: list[tuple[str, str]] = []
        for label, body in replies:
            whole_reply = f"{label}\n{body}"
            if len(append_part(header, whole_reply)) > chunk_size:
                reply_queue.extend(split_oversized_reply(label, body, header))
            else:
                reply_queue.append((label, body))

        current = make_chunk(header, [])
        has_reply = False
        last_sentences: list[str] = []
        index = 0

        def finish_current() -> None:
            nonlocal current, has_reply, index
            if has_reply:
                chunks.append(
                    Chunk(
                        text=current,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1
            overlap = last_sentences[-sentence_overlap:] if sentence_overlap else []
            current = make_chunk(header, overlap)
            has_reply = False

        for label, body in reply_queue:
            reply = f"{label}\n{body}"
            if len(append_part(current, reply)) > chunk_size and has_reply:
                finish_current()

            # A large complete reply may fit with the header but not after its
            # overlap sentence. Keep the reply whole and omit that overlap only
            # when needed to honor the maximum size.
            if len(append_part(current, reply)) > chunk_size and not has_reply:
                current = make_chunk(header, [])

            if len(append_part(current, reply)) > chunk_size:
                raise ValueError(f"Reply in {doc.source} is still too large after sentence splitting")

            current = append_part(current, reply)
            has_reply = True
            last_sentences = sentences(body) or [body]

        finish_current()

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
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
