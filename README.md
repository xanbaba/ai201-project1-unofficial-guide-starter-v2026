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

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:**
**Overlap:**

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

**Chunk 1** — source: `` — produced by: ``

```
```

**Chunk 2** — source: `` — produced by: ``

```
```

**Chunk 3** — source: `` — produced by: ``

```
```

**Chunk 4** — source: `` — produced by: ``

```
```

**Chunk 5** — source: `` — produced by: ``

```
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:**

**Answer:**

```
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
|  |  |  |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

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

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Every chunk retains its thread question | Every chunk begins with its source `THREAD:` question | 24 of 26 | 24 of 26 | 24 of 26 | MISSED |
| 5. The complete workflow is fast | All 5 questions return within 10 seconds | Not measured | Not measured | Not measured | NOT MEASURED |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### Evidence for criteria 1 and 2

Produced by: `results/run_2026-09-20_1840_before.md`, from
`run_eval.py::main`. Retrieval was performed by `store.py::search` using
chunks from `chunker.py::split_documents`.

**What to do if I cannot finish my assignment by deadline? — run 1**

- Sources retrieved: `thread_commuting.txt`, `thread_first_year_regret.txt`, `thread_group_project.txt`, `thread_late_work.txt`

```
If you cannot finish an assignment by the deadline, you should ask for an extension before the deadline arrives, as almost everyone will grant extra time if asked in advance rather than after the fact (*thread_late_work.txt*). Additionally, if you have a documented illness, that goes through the dean of students rather than the instructor (*thread_late_work.txt*).
```

**What study spots do you know that have good coffee nearby? — run 1**

- Sources retrieved: `thread_commuting.txt`, `thread_first_gen.txt`, `thread_internship_timing.txt`, `thread_laundry_timing.txt`, `thread_study_spots.txt`

```
Ridgeway Café is recommended as a study spot that has good coffee and stays empty and quiet before 10am (thread_study_spots.txt).
```

**I want to transfer credits for my major. My department agreed verbally. — run 1**

- Sources retrieved: `thread_changing_major.txt`, `thread_first_year_regret.txt`, `thread_office_hours_etiquette.txt`, `thread_pass_fail.txt`, `thread_transfer_credits.txt`

```
You should get the agreement in writing from the department before you rely on it, as a verbal yes may not survive a staff change.

Source: thread_transfer_credits.txt
```

**Can I change my meal plan? — run 1**

- Sources retrieved: `thread_changing_major.txt`, `thread_first_year_regret.txt`, `thread_meal_plan_tier.txt`, `thread_textbook_editions.txt`, `thread_transfer_credits.txt`

```
Yes, you can change your meal plan, but you can only change it once and only in the first ten days of the semester (thread_meal_plan_tier.txt).
```

**When does library close — run 1**

- Sources retrieved: `thread_group_project.txt`, `thread_internship_timing.txt`, `thread_laundry_timing.txt`, `thread_sleep_schedule.txt`, `thread_study_spots.txt`

```
The library is open until 2am, according to thread_sleep_schedule.txt.
```

### Evidence for criterion 4

Produced by: `app.py::cmd_chunks`, using chunks from
`chunker.py::fallback_split`. The baseline created 26 chunks. The 24 first
chunks from source documents began with `THREAD:`, but these two continuation
chunks did not:

```text
Chunk 2 | source: thread_bike_commute.txt#1
nd it's the only reason I got mine back after it was taken.

Chunk 2 | source: thread_first_year_regret.txt#1
) ---
That your adviser's job is partly to know the exceptions to rules. Ask before assuming a deadline is fixed.
```

### Evidence for criterion 3

Produced by: `results/run_2026-09-20_1840_before.md`, from
`run_eval.py::check_out_of_scope`. The relevance cutoff was `0.6`; the gate
refused 5 of 5 out-of-corpus questions.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.890 | refused |
| How do I change the oil in a diesel engine? | 0.930 | refused |
| Who won the 1994 World Cup? | 0.787 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.828 | refused |
| How do I write a for loop in Rust? | 0.871 | refused |

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | In each of the three runs, all five questions retrieved the source thread containing the expected answer, exceeding the target of 4 of 5. |
| 2 | Every answer names a source | MET | All five answers in each run named a source document, meeting the 5 of 5 target. |
| 3 | Gate stops out-of-corpus questions | MET | The deterministic gate check refused all 5 of 5 out-of-corpus questions at the 0.6 cutoff, exceeding the target of 4 of 5. |
| 4 | Every chunk retains its thread question | MISSED | The baseline fixed-window chunker produced 26 chunks, but 2 continuation chunks began in the middle of text rather than with their source `THREAD:` question. |
| 5 | The complete workflow is fast | NOT MEASURED | The baseline evaluation report records answers and distances but not elapsed time, so I cannot yet determine whether all five questions finished within 10 seconds. |

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
