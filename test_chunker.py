"""Focused tests for the reply-aware custom chunker."""

import unittest
from unittest.mock import patch

import config
from chunker import _chunk_document, _parse_thread, describe, split_documents
from ingest import Document, load_documents


class ChunkerTests(unittest.TestCase):
    def test_normal_thread_parsing(self):
        document = Document(
            "normal.txt",
            "THREAD: When should I apply?\n\n--- reply 1 (3 votes) ---\nApply early.",
        )
        parsed = _parse_thread(document)
        self.assertEqual(parsed.header, "THREAD: When should I apply?")
        self.assertEqual(parsed.replies, [("--- reply 1 (3 votes) ---", "Apply early.")])
        self.assertFalse(parsed.used_fallback)

    def test_whole_reply_moves_to_next_chunk(self):
        header = "THREAD: Is this a question?"
        first = "A" * 180
        second = "B" * 180
        document = Document(
            "move.txt",
            f"{header}\n\n--- reply 1 (1 votes) ---\n{first}\n\n"
            f"--- reply 2 (2 votes) ---\n{second}",
        )
        chunks = _chunk_document(document, 300, 0)
        self.assertEqual(len(chunks), 2)
        self.assertIn(first, chunks[0].text)
        self.assertNotIn(second, chunks[0].text)
        self.assertIn(second, chunks[1].text)

    def test_oversized_reply_splits_at_sentence_boundaries(self):
        header = "THREAD: Long reply?"
        body = " ".join(["This is a complete sentence."] * 35)
        document = Document("long.txt", f"{header}\n\n--- reply 1 (1 votes) ---\n{body}")
        chunks = _chunk_document(document, 220, 0)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk.text) <= 220 for chunk in chunks))
        self.assertTrue(all(chunk.text.rstrip().endswith(".") for chunk in chunks))

    def test_oversized_reply_without_punctuation_respects_limit(self):
        header = "THREAD: No punctuation?"
        body = "word " * 200
        document = Document("words.txt", f"{header}\n\n--- reply 1 (1 votes) ---\n{body}")
        chunks = _chunk_document(document, 180, 0)
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk.text) <= 180 for chunk in chunks))

    def test_non_thread_document_uses_visible_fallback(self):
        chunks = _chunk_document(Document("notes.txt", "Plain notes without a thread."), 500, 1)
        self.assertEqual(len(chunks), 1)
        self.assertTrue(chunks[0].text.startswith("SOURCE: notes.txt"))
        self.assertIn("--- content ---", chunks[0].text)
        self.assertTrue(chunks[0].parser_fallback)

    def test_describe_reports_fallback_documents(self):
        chunks = split_documents([Document("notes.txt", "Plain notes without a thread.")])
        self.assertIn("parser fallback for 1 document(s)", describe(chunks))

    def test_real_advice_threads_have_exact_headers_and_valid_sizes(self):
        documents = load_documents("advice_threads")
        headers = {document.source: document.text.splitlines()[0] for document in documents}
        for size, overlap, count in ((500, 1, 42), (900, 2, 23)):
            with self.subTest(size=size, overlap=overlap):
                with patch.object(config, "CHUNK_SIZE", size), patch.object(config, "SENTENCE_OVERLAP", overlap):
                    chunks = split_documents(documents)
                self.assertEqual(len(chunks), count)
                self.assertTrue(all(not chunk.parser_fallback for chunk in chunks))
                self.assertTrue(all(len(chunk.text) <= size for chunk in chunks))
                self.assertTrue(all(chunk.text.splitlines()[0] == headers[chunk.source] for chunk in chunks))
                for source in headers:
                    indices = [chunk.index for chunk in chunks if chunk.source == source]
                    self.assertEqual(indices, list(range(len(indices))))


if __name__ == "__main__":
    unittest.main()
