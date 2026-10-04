# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project is an unofficial question-answering guide built from the
`advice_threads` corpus of student-advice discussions. It answers focused
questions about topics such as deadlines, study spaces, transfer credits, meal
plans, and library hours by retrieving relevant thread chunks first. The system
refuses unrelated questions when no retrieved chunk is close enough, rather
than asking the model to guess. When it does answer, it uses the retrieved
thread text and names the source document.

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** 500 characters maximum
**Overlap:** 1 complete sentence, plus the thread question in every chunk

The advice threads are made of short labelled replies. Across the corpus, a
reply averages about 122 characters, so 500 characters usually holds the
thread question and two or three complete replies without mixing too many
topics. The starter's 800-character windows made 26 chunks and left a
2-character fragment at the end of one document. My chunker moves a reply to
the next chunk when it does not fit, repeats the `THREAD:` question, and
repeats the previous chunk's final sentence as context. It only splits a reply
at sentence boundaries when that one reply is too large to fit by itself.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.
```

**Chunk 2** — source: `thread_first_gen.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Anything specific for first-generation students?

--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.

--- reply 2 (41 votes) ---
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.
```

**Chunk 3** — source: `thread_laptop_specs.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: How much laptop do I actually need for CS courses?

--- reply 1 (31 votes) ---
Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.

--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.
```

**Chunk 4** — source: `thread_office_hours_etiquette.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Is it weird to go to office hours with no specific question?

--- reply 1 (44 votes) ---
No, and this is the single most common thing first years get wrong. 'I'm following the lectures but I don't feel like I understand the shape of it' is a completely normal thing to say.

--- reply 2 (29 votes) ---
They're usually empty. You are doing the instructor a favour by turning up.
```

**Chunk 5** — source: `thread_roommate_conflict.txt#0` — produced by: `chunker.py::split_documents`

```
THREAD: Roommate situation isn't working. What now?

--- reply 1 (28 votes) ---
Talk to your RA early, and frame it as 'we need help sorting this out' rather than 'move me'. Room changes are possible but the process starts with mediation and skipping that step slows it down.

--- reply 2 (14 votes) ---
Room changes happen at the semester boundary almost always, and mid-semester only in fairly serious cases.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Can I change my meal plan?

**Answer:**

```
Yes, you can change your meal plan, but you can only change it once and only within the first ten days (from `thread_meal_plan_tier.txt`).

Sources retrieved: thread_commuting.txt, thread_meal_plan_tier.txt
```

**My relevance cutoff:** 0.60

The authoritative measurement is `results/run_2026-09-23_1955_unit1-final.md`.
It used the 42-chunk `advice_threads` index from
`chunker.py::split_documents` (500-character maximum, one-sentence overlap),
`TOP_K = 3`, and a 0.60 cutoff. My five in-corpus questions had best distances
from 0.2538 to 0.5827. The five out-of-corpus questions ranged from 0.8097 to
0.9290. There was a gap between 0.5827 and 0.8097, so 0.60 is above every
in-corpus result but below every unrelated result.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| What to do if I cannot finish my assignment by deadline? | Yes | 0.4775 |
| What study spots do you know that have good coffee nearby? | Yes | 0.4259 |
| I want to transfer credits for my major. My department agreed verbally. | Yes | 0.2538 |
| Can I change my meal plan? | Yes | 0.4137 |
| When does library close | Yes | 0.5827 |
| What is the capital of Mongolia? | No | 0.9290 |
| How do I change the oil in a diesel engine? | No | 0.9121 |
| Who won the 1994 World Cup? | No | 0.9165 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.8097 |
| How do I write a for loop in Rust? | No | 0.8712 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Codex whether the model receives one retrieved chunk or all
retrieved chunks, and how the relevance cutoff affects that decision. It
explained that retrieval returns the top-k chunks and the cutoff is a gate: if
the closest result passes, the model receives all retrieved chunks. I used that
explanation when testing retrieval and set `TOP_K = 3` so the model receives a
small, focused set of chunks.

**2.** I asked Codex how to adapt chunking to reply-based advice threads and
whether each later chunk should retain the original thread question. It
inspected several threads, found that replies average about 122 characters,
and showed that the starter's fixed windows produced a 2-character fragment.
I changed `split_documents` to keep whole replies together up to 500
characters, repeat the `THREAD:` question in every chunk, and retain one
sentence of prior context in continuation chunks.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

Measured on October 4, 2026 (America/New_York), against the unchanged targets
in [criteria.md](criteria.md). Preparation: `.venv\Scripts\python.exe test.py`
passed all 10 environment checks, and `app.py ask "Can I change my meal plan?"`
confirmed the existing index works. That preparation answer came from cache;
it is not counted in the evaluation.

Evaluation command: `.venv\Scripts\python.exe tools/milestone1_eval.py`.
This measurement wrapper calls `run_eval.py::main` with `--label before`,
times the original `run_eval.py::run_once` immediately before entry until its
return, and saves every retrieved chunk alongside every answer. It also reads
all existing indexed chunks three times to check their exact thread headings.
It changes no pipeline code, settings, corpus, model, or index. The baseline
uses 42 chunks, `TOP_K = 3`, and cutoff 0.60.

Evidence: [full answer and gate report](results/run_2026-10-04_1527_before.md),
[retrieved text, timings, and complete chunk audits](results/milestone1_before_evidence.json),
and [measurement wrapper](tools/milestone1_eval.py). No `scorer.py` exists, so
I judged retrieval and source naming by reading the captured text. The blank
question-level scores in the generated report are not failures.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | At least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | At least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Every chunk retains its exact source thread question | All 42 chunks | 42/42 | 42/42 | 42/42 | MET |
| 5. The complete workflow is fast | Every question within 10 seconds | 5/5 | 5/5 | 5/5 | MET |

Criterion 1 counts retrieved evidence, not whether the generated answer uses
every expected detail. In all three runs, the retrieved chunks contained the
syllabus and extension advice, Ridgeway Café, written department confirmation,
the first-ten-days meal-plan restriction, and the library's 2am closing time.
Criterion 2 checks the model's own answer text for a source filename; a separate
"Sources retrieved" line alone would not count. All 15 answers named a
retrieved source. Criterion 3 repeats the one deterministic gate measurement
in all three columns, as instructed. Criterion 4 checks every stored chunk,
including continuation chunks, against the first line of its source document.
Criterion 5 includes first-query initialization, retrieval, and generation;
the index was already built and there was no untimed warm-up inside the
evaluation process.

All criterion counts match across runs, but caching was disabled explicitly by
`run_eval.py::run_once` (`cache=False`). The session reported **15 model calls**
and no cache hits, and answer wording varied between trials. Retrieval and
chunk headings were deterministic.

### Criterion 1 — retrieved answer evidence

Actual run 1 retrieval for the deadline question, from
`store.py::search`; this chunk was originally produced by
`chunker.py::split_documents`. Saved in
`results/milestone1_before_evidence.json`, trial 1, `results`.
Source: `thread_late_work.txt#0`.

```text
THREAD: What actually happens if you hand something in late?

--- reply 1 (20 votes) ---
Entirely instructor-dependent and the syllabus is accurate. If it says 10% a day, it's 10% a day.

--- reply 2 (47 votes) ---
The universal rule: ask before the deadline, not after. Almost everyone will give you two days if you ask on Wednesday for a Friday deadline. Almost nobody will on the following Monday.
```

The following retrieved chunks contain the expected information in each run:

| Question topic | Chunk containing the answer |
|---|---|
| Assignment deadline | `thread_late_work.txt#0` |
| Study spot with coffee | `thread_study_spots.txt#0` |
| Verbal transfer-credit approval | `thread_transfer_credits.txt#0` |
| Meal-plan change | `thread_meal_plan_tier.txt#1` |
| Library closing time | `thread_sleep_schedule.txt#0` |

### Criterion 2 — answer names a source

Actual meal-plan answer, run 1. Produced by
`generate.py::answer_from_chunks`, called by `run_eval.py::run_once`, and saved
by `run_eval.py::write_report` in `results/run_2026-10-04_1527_before.md`.

```text
Yes, you can change your meal plan, but you can only change it once and only in the first ten days (thread_meal_plan_tier.txt).
```

### Criterion 3 — out-of-corpus gate output

Actual console output from `run_eval.py::check_out_of_scope`, which uses
`store.py::search` and `gate.py::check`. The same distances and decisions are
saved by `run_eval.py::write_report` in
`results/run_2026-10-04_1527_before.md`. These checks stop at the gate and do not
call the model.

```text
Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.9290)  What is the capital of Mongolia?
  refused  (best distance 0.9121)  How do I change the oil in a diesel engine?
  refused  (best distance 0.9165)  Who won the 1994 World Cup?
  refused  (best distance 0.8097)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.8712)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

`gate.py::REFUSAL` is `I don't have enough information about that.`;
`run_eval.py::run_once` returns that string on a failed gate. The assignment's
out-of-scope measurement uses `check_out_of_scope`, so its actual output above
records the refusal decision rather than printing the refusal string.

### Criterion 4 — exact thread headings

Actual console output from `tools/milestone1_eval.py::main`, using
`tools/milestone1_eval.py::audit_chunks`. Full expected and actual headings,
chunk text, and individual outcomes are saved in
`results/milestone1_before_evidence.json`, `chunk_audits`.

```text
Chunk headings run 1: 42/42
Chunk headings run 2: 42/42
Chunk headings run 3: 42/42
```

Actual indexed continuation chunk `thread_meal_plan_tier.txt#1`, originally
produced by `chunker.py::split_documents`, read from the existing Chroma
collection by `tools/milestone1_eval.py::audit_chunks`:

```text
THREAD: Which meal plan tier is right?

Previous context: The highest tier only makes sense if you eat three meals a day in the halls every single day, which basically nobody does past October.

--- reply 3 (11 votes) ---
Remember you can only change it once and only in the first ten days. I waited and got stuck on a plan I didn't use.

--- reply 4 (7 votes) ---
Declining balance rolls within the semester but not between them. Spend it in December or lose it.
```

### Criterion 5 — complete workflow timings

Measured by `tools/milestone1_eval.py::main`'s `measured_run_once` wrapper using
`time.perf_counter` around the original `run_eval.py::run_once`. Raw seconds
are saved in `results/milestone1_before_evidence.json`, `trials`;
the table displays them rounded to six decimal places.

| Question topic | Run 1 (seconds) | Run 2 (seconds) | Run 3 (seconds) |
|---|---|---|---|
| Assignment deadline | 1.921352 | 0.714774 | 0.686277 |
| Study spot with coffee | 0.605632 | 0.533877 | 0.510164 |
| Verbal transfer-credit approval | 0.511352 | 0.561281 | 0.598528 |
| Meal-plan change | 0.604303 | 0.588195 | 0.553622 |
| Library closing time | 0.586536 | 0.463852 | 0.598329 |

Actual first-trial console output from the timing wrapper:

```text
  elapsed: 1.921352 seconds
```

Actual evaluation session accounting from `generate.py::usage`, printed by
`run_eval.py::write_report` and saved in the supplementary JSON:

```text
15 model calls this session, 7220 tokens (6648 in, 572 out)
```

**Observation for later milestones:** The deadline chunk contains the expected
`syllabus` detail, but none of the three deadline answers mentions it. That
does not fail any of the five filed criteria: retrieval contains the answer,
source naming is present, and there is no separate answer-completeness target.
It does show a limitation that these passing counts do not measure. These
results describe this five-question baseline, not a guarantee for new questions
or future response times. No improvement has been made in Milestone 1.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
