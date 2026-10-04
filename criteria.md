# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
Retrieving the chunk that has the asnwer is the core purpose of this app; getting that chunk in at least 4 out of 5 times would prove that the system is reliable enough. It might get one wrong as there are questions that might imply one meaning and get mapped to some chunk, although it was supposed to mean something a bit different. It can be observed when the question is complex enough and the asnwer is in multiple chunks.
---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
This is a functionality that either works or not. So, it is important that all 5/5 answers cite a document where they got the info from. Otherwise, this could be halucinated info, and it is a bug in the system. It must written in code so that every answer gives out a document used.
---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

The final measurement in `results/run_2026-09-23_1955_unit1-final.md` had
in-corpus best distances from 0.2538 to 0.5827, while out-of-corpus questions
ranged from 0.8097 to 0.9290. The gap supported the 0.60 cutoff. I chose 4 of
5 rather than requiring every question to be refused because an unrelated
question can still share words or a broad topic with a student-advice thread
and produce one close semantic match.

---

## 4. Every chunk retains its thread question

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->
Every chunk begins with the `THREAD: question from its source document`

> **Clarification:** `THREAD:` means the exact thread-question line from the
> source document. This clarification does not change the original criterion.


**Why this target:**

Replies in this corpus often make sense only in relation to the original question. Repeating the short thread question gives each chunk its topic and context, so later replies can be retrieved and used without needing the preceding chunk.

---

## 5. The complete workflow is fast

For each of my five test questions, with the advice_threads index already built and caching disabled, the system returns either an answer or refusal within 10 seconds, measured from immediately before run_eval.py::run_once begins until it returns its result.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->



**Why this target:**

The custom chunker produces 42 indexed chunks, but loading, chunking, and
embedding are not repeated for each question. Retrieval searches only the top
3 chunks, so the main variable is one Gemini answer-generation call. Ten
seconds is short enough for an interactive question-answering tool while
allowing ordinary model-response variation.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
