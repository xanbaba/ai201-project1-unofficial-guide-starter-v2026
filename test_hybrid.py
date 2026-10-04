"""Checks for hybrid ranking and preservation of the cosine gate contract."""

import unittest

import gate
from store import Result, _hybrid_rank, _tokens


def candidates():
    return [
        Result("A general discussion about equipment", "a.txt", "a.txt#0", 0.2, "test"),
        Result("ZX900 battery replacement procedure", "b.txt", "b.txt#0", 0.7, "test"),
        Result("Housing lottery dates", "c.txt", "c.txt#0", 0.8, "test"),
        Result("Library opening times", "d.txt", "d.txt#0", 0.9, "test"),
    ]


class HybridTests(unittest.TestCase):
    def test_exact_term_can_promote_a_semantically_lower_match(self):
        results = _hybrid_rank(candidates(), "ZX900", 2)
        self.assertEqual(results[0].source, "b.txt")
        self.assertEqual(results[0].keyword_rank, 1)
        self.assertEqual(results[0].semantic_rank, 2)
        self.assertEqual(results[0].distance, 0.7)
        self.assertTrue(gate.check(results, threshold=0.6).passed)

    def test_no_keyword_match_keeps_semantic_order(self):
        results = _hybrid_rank(candidates(), "unmatchedidentifier", 3)
        self.assertEqual([r.source for r in results], ["a.txt", "b.txt", "c.txt"])
        self.assertTrue(all(r.keyword_rank is None for r in results))

    def test_lexical_promotion_does_not_bypass_refusal(self):
        results = candidates()
        results[0].distance = 0.65
        ranked = _hybrid_rank(results, "ZX900", 2)
        self.assertFalse(gate.check(ranked, threshold=0.6).passed)
        self.assertEqual(min(r.distance for r in ranked), 0.65)

    def test_single_result_preserves_nearest_semantic_evidence(self):
        self.assertEqual(_hybrid_rank(candidates(), "ZX900", 1)[0].source, "a.txt")
        self.assertEqual(_hybrid_rank([], "ZX900", 3), [])

    def test_unicode_numbers_and_case_are_tokenized_consistently(self):
        self.assertEqual(_tokens("The CAFÉ ZX900 at 10am"), ["café", "zx900", "10am"])


if __name__ == "__main__":
    unittest.main()
