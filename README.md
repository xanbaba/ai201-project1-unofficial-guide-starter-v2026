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

These calls use the original targets in [criteria.md](criteria.md) and the
Milestone 1 baseline above. A target must hold in every run; averaging the
three runs would not rescue a miss. No criterion or target has been revised.

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | The top three results contained an answer-bearing chunk for 5/5 questions in each of the three runs, exceeding the original minimum of 4/5 every time; I checked the saved chunk text, not just the distance or source filename. |
| 2 | Every answer names a source | MET | All five generated answers in each run named at least one retrieved source document in their own answer text (15/15 total), meeting the requirement for every answer; I did not count the report's separate list of retrieved sources as a citation. |
| 3 | The relevance gate stops out-of-corpus questions | MET | The gate refused 5/5 unrelated questions, exceeding the original 4/5 target: all best distances (0.8097–0.9290) exceeded 0.60, and the failed-gate branch in `run_eval.py::run_once` returns `gate.py::REFUSAL`; the prescribed deterministic measurement is repeated as 5/5 in all three columns, not treated as 15 independent trials. |
| 4 | Every chunk retains its thread question | MET | Each of the three full-index audits found 42/42 chunks beginning with the exact `THREAD:` question line from its source document, including continuation chunks, so there were no exceptions to the original “every chunk” target. |
| 5 | The complete workflow is fast | MET | All five uncached questions finished within 10 seconds in each run (15/15 total); the slowest individual call took 1.921352 seconds, measured immediately before the original `run_eval.py::run_once` began until it returned, including the first query's initialization. |

### Challenging these calls

I considered the strongest argument for MISSED for each criterion before
keeping these verdicts:

- **1:** The deadline answers omit the expected `syllabus` phrase, and the
  relevant deadline and library chunks rank third rather than first. However,
  the original criterion asks whether the retrieved chunks contain the answer;
  the saved top-three text contains both the syllabus advice and the 2am
  library fact in every run. Neither first-place ranking nor generated-answer
  completeness is its target.
- **2:** Merely naming a filename does not prove an answer is accurate or fully
  supported. That is a limit of this criterion, but all 15 answers do name an
  actual retrieved document, satisfying its observable source-naming target.
- **3:** The out-of-scope report records gate decisions rather than returned
  refusal text, and it runs once. The assignment explicitly prescribes that
  deterministic measurement; inspecting the unchanged failed-gate branch
  confirms that it returns `I don't have enough information about that.`
  This is a gate measurement plus a code-path check, not a claim that the
  report captured five end-to-end refusal responses.
- **4:** Five sample chunks would not establish “every chunk,” and regenerated
  chunks would not necessarily establish what the system searches. These
  audits instead read all 42 chunks from the existing index and compare each
  heading with its source, so neither objection applies to the saved evidence.
- **5:** An average below 10 seconds could conceal a slow response, and cached
  answers could make the workflow look faster. Here every individual duration
  is below the limit, and the session recorded 15 real model calls with caching
  disabled. Future network or model delays remain untested by this baseline.

The speed result has the largest margin against its target: the original
10-second allowance accounts for ordinary model-response variation, but even
the slowest observed call was under two seconds. The individual timings and
model-call count support MET for this
baseline without establishing a guarantee for future runs. All five verdicts
remain MET against the filed targets; the answer-completeness limitation stays
visible without changing a criterion.

## Diagnoses

**No filed criterion was missed.** All five targets held in every measured
run, so there are no acceptance-criterion failures to assign to a pipeline
stage. The original verdicts and targets remain unchanged.

### Were the targets too safe?

Some were. Criterion 1 allows one retrieval miss among five familiar questions
and accepts an answer anywhere in the top three results. Criterion 3 tests
questions from clearly unrelated domains, with a large distance gap from the
cutoff; it does not challenge the gate with questions that sound like student
advice but ask for facts absent from the corpus. Criterion 5's 10-second limit
had substantial room above the slowest observed response of 1.921352 seconds.
Criteria 2 and 4 demand 100% compliance, but they check narrow properties:
naming a source and retaining a heading. Neither proves that an answer includes
the important advice or uses the source accurately. These passes establish a
working baseline, not an excellent system.

**The criterion I would tighten in a future evaluation is criterion 2:**
for all five questions in each of three uncached runs, every answer must name
a retrieved source **and include the expected fact already recorded in
`questions.py`, supported by that source**. I would judge the fact semantically,
so a paraphrase of getting department approval in writing would count. The
deadline answer would need to mention checking the syllabus or its
instructor-specific late-work policy. This is a proposed future standard,
not a revision to `criteria.md` or the current before/after scoring. Against
that additional completeness requirement, the saved baseline would be 4/5
in each run because all three deadline answers omit that detail.

### A limitation the passing criteria did not catch

**Question:** `What to do if I cannot finish my assignment by deadline?`

**Actual answer, run 3** — `generate.py::answer_from_chunks`, saved in
[the baseline report](results/run_2026-10-04_1527_before.md):

```text
You should ask for an extension before the deadline rather than after, as almost everyone will grant extra time if asked beforehand.

Source: `thread_late_work.txt`
```

**Retrieved evidence** — `thread_late_work.txt#0`, returned by
`store.py::search` in all three runs and saved in
[the supplementary evidence](results/milestone1_before_evidence.json):

```text
--- reply 1 (20 votes) ---
Entirely instructor-dependent and the syllabus is accurate. If it says 10% a day, it's 10% a day.
```

Working backwards gives three possible causes at different stages:

| Possible stage and mechanism | What the saved evidence shows |
|---|---|
| Loading: the syllabus advice was removed while reading or cleaning the document. | The exact advice survives in the indexed and retrieved text, so loading did not lose it. |
| Retrieval: the relevant chunk did not reach the model, leaving it only generic deadline advice. | The relevant chunk is third in all three results, and `generate.py::build_prompt` includes every retrieved chunk, so the model received it. |
| Generation: the model selected extension advice but omitted the accompanying instructor-specific policy. | The advice was available in the prompt, yet none of the three answers mentions the syllabus or the instructor-dependent policy. The omission occurs when producing the answer. |

**Stage: generation. Mechanism:** The model condenses the supplied replies into
an extension recommendation without carrying over the policy qualification.
`generate.py::GROUNDING_INSTRUCTION` asks for brevity (usually two or three
sentences), source naming, and grounding, but does not require coverage of
important qualifications. That prompt design is a plausible contributor to
the omission, not a proven causal explanation; changing it and measuring again
would test the hypothesis. Run 1 also uses space for group-project advice from
a different retrieved thread, even though the question does not specify a
group project.

The pattern is the same missing qualification in all three deadline answers,
not three unrelated errors. The other four questions' answers include their
expected facts in all three runs. This supports investigating generation's
selection of relevant details rather than rebuilding the corpus or chunker.
The deadline answer still gives supported advice, so this is a completeness
limitation relative to the recorded expectation, not a fabricated miss of the
original criteria. No system improvement has been made in Milestone 3.

## The Improvement

**What I changed:** I added one rule to
`generate.py::GROUNDING_INSTRUCTION`, used by
`generate.py::answer_from_chunks`:

```text
- When summarizing advice, preserve the relevant conditions, restrictions, and qualifications stated in the documents, including policy-dependent exceptions; do not present qualified advice as a universal rule.
```

**Why I picked it:** The Milestone 3 diagnosis found that generation omitted
the instructor-specific syllabus qualification even though retrieval supplied
it, so I asked the model to preserve relevant qualifications when summarizing.
The rule applies to advice generally and does not inject the test questions'
expected answers into the prompt.

Before evaluating, I considered why this might fail: the model still decides
which qualifications are relevant, and a general instruction may not make it
select the syllabus detail. The extra instruction could also produce longer
answers without improving coverage. I tested this single rule without changing
the model, corpus, index, chunking, top-k, relevance cutoff, test questions, or
acceptance criteria.

### Run Log — After

Measured on October 4, 2026 (America/New_York), using
`.venv\Scripts\python.exe tools/milestone1_eval.py --label after`.
The wrapper invokes `run_eval.py::main` with `--label after`, runs each of the
five questions three times with caching disabled, measures the same
`run_eval.py::run_once` boundary as before, and audits all 42 existing indexed
chunks three times. I added label selection to the measurement wrapper so it
saves separate after evidence and refuses to overwrite either result set;
this is measurement support, not another pipeline improvement.

Evidence: [full after answers and gate output](results/run_2026-10-04_1557_after.md)
and [after retrievals, timings, full chunk audits, and exact prompt](results/milestone4_after_evidence.json).
The session recorded 15 model calls, 7,802 tokens (7,188 input and 614 output),
and no cache hits. The original before files remain intact. All 15 retrieved
result sets and in-corpus gate decisions matched their corresponding baseline
trials exactly; the out-of-corpus distances and refusals also matched.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | At least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | At least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Every chunk retains its exact source thread question | All 42 chunks | 42/42 | 42/42 | 42/42 | MET |
| 5. The complete workflow is fast | Every question within 10 seconds | 5/5 | 5/5 | 4/5 | MISSED |

The retrieved chunks still contain the answer for every question, and all 15
generated answers name a retrieved document in their own text. The gate again
refused all five out-of-corpus questions in its prescribed deterministic pass;
that single measurement is repeated in all three columns. All 42 indexed
headings matched their source question in every audit. Criterion 5 is MISSED
because the deadline question's third call took 69.916947 seconds: two passing
runs do not compensate for one run below the required 5/5.

| Question topic | Run 1 (seconds) | Run 2 (seconds) | Run 3 (seconds) |
|---|---|---|---|
| Assignment deadline | 2.159770 | 0.702828 | 69.916947 |
| Study spot with coffee | 0.750037 | 0.659059 | 0.553682 |
| Verbal transfer-credit approval | 0.687840 | 0.493253 | 0.731736 |
| Meal-plan change | 0.628415 | 0.845569 | 0.645126 |
| Library closing time | 0.520271 | 0.640808 | 0.584204 |

Actual slow-call console output from the measurement wrapper:

```text
  elapsed: 69.916947 seconds
  run 3: —  (best distance 0.4775)
```

### Before and after side by side

The original Milestone 1 log above and the after log use the same five targets.
This comparison repeats both sets of counts to make the change visible:

| Criterion | Original target | Before R1 | Before R2 | Before R3 | After R1 | After R2 | After R3 | Verdict before → after |
|---|---|---|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | At least 4 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET → MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET → MET |
| 3. Gate stops out-of-corpus questions | At least 4 of 5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | MET → MET |
| 4. Every chunk retains its exact source thread question | All 42 chunks | 42/42 | 42/42 | 42/42 | 42/42 | 42/42 | 42/42 | MET → MET |
| 5. The complete workflow is fast | Every question within 10 seconds | 5/5 | 5/5 | 5/5 | 5/5 | 5/5 | 4/5 | MET → MISSED |

**Did it help?** It did not fix the diagnosed syllabus omission (0/3 answers
included it before and 0/3 after), and the after evaluation additionally missed
the original speed target because one response took 69.9 seconds.

There was one narrower positive observation: the café's “before 10am”
qualification appeared in 1/3 baseline café answers and 3/3 after answers.
That is an additional qualitative check of the intended prompt behavior,
not a new acceptance criterion or a reason to call the overall change a
success. The original source-naming criterion still scores 5/5 per run even
when important details are omitted.

Actual café answers, run 1, produced by `generate.py::answer_from_chunks`
and saved in the respective before and after reports:

**Before:**

```text
Ridgeway Café is mentioned as a study spot that has good coffee.

Source: thread_study_spots.txt
```

**After:**

```text
Based on the provided documents, Ridgeway Café is recommended as a study spot with good coffee, provided you go before 10am.

Source: `thread_study_spots.txt`
```

Actual deadline answer after the change, run 3:

```text
You should ask before the deadline rather than after, as almost everyone will give you two days if you ask beforehand, but almost nobody will on the following Monday (thread_late_work.txt). Additionally, if you need to adjust individual grades for a group project where someone disappears, you must raise the issue before the deadline rather than after (thread_group_project.txt).
```

The deadline answers still select extension advice and omit the
instructor-dependent policy; two after answers also include group-project
advice. This supports the diagnosis that the general prompt instruction did
not reliably control which qualifications generation selected.

The new speed miss is a long end-to-end call, but the captured timings do not
separate retrieval time from service time. Identical retrieval results and the
absence of a rate-limit warning do not prove why it took so long. I cannot
attribute the delay to the prompt rather than model-service or network
variation from one before/after evaluation. It remains a measured failure,
with the long trial preserved rather than discarded. I kept the tested prompt
change and made no second improvement or replacement evaluation in this
milestone.

### Additional measured improvement — hybrid search

Declared before implementation: I am adding BM25 keyword retrieval alongside
semantic retrieval and combining their rankings. The prompt-only experiment
above remains documented. This second experiment keeps that prompt fixed and
tests retrieval ranking: the answer-bearing late-work and library-hours chunks
were third in the semantic results. I will measure the same five original
criteria and separately compare answer-bearing chunk ranks. No criterion is
being changed.

**Implementation:** `store.py::search` now retrieves the semantic ranking of
all existing indexed chunks and scores their text with `rank_bm25.BM25Okapi`.
Both query and chunk text are tokenized into lowercase Unicode words and
numbers, with common grammatical words removed. Positive keyword matches are
ranked by BM25 score. Equal-weight reciprocal rank fusion combines the lists:
`1 / (60 + semantic_rank) + 1 / (60 + keyword_rank)`; a chunk with no positive
keyword score receives only its semantic contribution. Ties use semantic rank
and chunk ID, so ordering is deterministic. The final three results are sorted
by fusion score rather than distance.

The nearest semantic chunk is retained in the selected set, replacing the
last fused candidate if necessary. This keeps the gate's best cosine distance
comparable to the original calibration. `Result.distance` remains a real
cosine distance; BM25 and fusion scores are never compared with the 0.60
cutoff. `app.py retrieve` now prints fusion scores and both component ranks
alongside distances. With `top_k=1`, retaining the nearest semantic result
means keyword ranking cannot change the selected chunk. Ranking the whole
index is suitable for these small corpora; a larger deployment would need
bounded candidate retrieval.

The prior prompt improvement was retained unchanged, so the comparison with
the prompt-only after run isolates hybrid retrieval. No question-specific
prompt rule, query rewrite, or expected-answer keyword was added.

### Hybrid run log

Valid command: `.venv\Scripts\python.exe tools/milestone1_eval.py --label hybrid-retest`.
Evidence: [full answers and gate output](results/run_2026-10-04_1609_hybrid-retest.md),
[retrieved chunks, component ranks, timings, prompt, and full audits](results/milestone4_hybrid_retest_evidence.json),
and [answer-bearing chunk ranking comparison](results/hybrid_ranking_comparison.json).
There were 15 uncached model calls and 7,804 tokens (7,143 input, 661 output).
The same 42 advice-thread chunks, embedding model, generation model, cutoff,
top-k, questions, and original criteria were used.

| Criterion | Original target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunks contain the answer | At least 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | At least 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Every chunk retains its exact source thread question | All 42 chunks | 42/42 | 42/42 | 42/42 | MET |
| 5. The complete workflow is fast | Every question within 10 seconds | 5/5 | 5/5 | 5/5 | MET |

Criterion 1 only just meets its target: the library question has no
answer-bearing chunk in any of its three retrievals. The other four questions
still retrieve their expected facts. All 15 model responses name a retrieved
source, including the library refusals, so criterion 2 remains MET; that
source-naming result does not establish answer usefulness. The deterministic
out-of-corpus gate again refuses 5/5 questions, with the original distances.
Three full-index audits each verify all 42 exact source headings. All 15
responses finish within 10 seconds, including the three generated refusals.

| Question topic | Run 1 (seconds) | Run 2 (seconds) | Run 3 (seconds) |
|---|---|---|---|
| Assignment deadline | 2.595364 | 0.721352 | 0.882670 |
| Study spot with coffee | 0.958837 | 0.932506 | 0.665272 |
| Verbal transfer-credit approval | 0.727239 | 0.740011 | 0.766983 |
| Meal-plan change | 0.671936 | 0.809251 | 1.008581 |
| Library closing time | 0.718000 | 0.700021 | 0.723240 |

### Comparison with semantic retrieval

The baseline and prompt-only runs both used semantic retrieval and had the
same answer-bearing chunk ranks. The prompt-only after run is the direct
comparison because it uses the same grounding prompt as the hybrid run.

| Criterion | Semantic + original prompt R1/R2/R3 | Semantic + improved prompt R1/R2/R3 | Hybrid + improved prompt R1/R2/R3 |
|---|---|---|---|
| 1. Retrieved answer evidence | 5/5, 5/5, 5/5 — MET | 5/5, 5/5, 5/5 — MET | 4/5, 4/5, 4/5 — MET |
| 2. Source naming | 5/5, 5/5, 5/5 — MET | 5/5, 5/5, 5/5 — MET | 5/5, 5/5, 5/5 — MET |
| 3. Out-of-corpus gate | 5/5, 5/5, 5/5 — MET | 5/5, 5/5, 5/5 — MET | 5/5, 5/5, 5/5 — MET |
| 4. Exact thread headings | 42/42, 42/42, 42/42 — MET | 42/42, 42/42, 42/42 — MET | 42/42, 42/42, 42/42 — MET |
| 5. Within 10 seconds | 5/5, 5/5, 5/5 — MET | 5/5, 5/5, 4/5 — MISSED | 5/5, 5/5, 5/5 — MET |

| Answer-bearing chunk | Semantic rank | BM25 rank | Final hybrid position in top three |
|---|---|---|---|
| `thread_late_work.txt#0` | 3 | 2 | 3 |
| `thread_study_spots.txt#0` | 1 | 1 | 1 |
| `thread_transfer_credits.txt#0` | 1 | 1 | 1 |
| `thread_meal_plan_tier.txt#1` | 1 | 1 | 1 |
| `thread_sleep_schedule.txt#0` | 3 | 6 | Excluded (fused rank 5) |

**Did hybrid search help?** It did not improve the answer-bearing chunk ranks
in this test set, and it made retrieval coverage worse by excluding the only
chunk containing the library's 2am closing time. All original criteria still
pass because criterion 1 permits one miss; that does not erase the regression.

**Stage and mechanism of the library regression: retrieval.** BM25 ranks the
sleep-schedule chunk sixth for `When does library close`; fusion places it
fifth, outside `TOP_K = 3`. The selected internship thread contains “close”
in “close applications,” an exact word match about a different topic. The
nearest semantic library-study chunk keeps the gate open, but it contains no
closing time. Generation then appropriately declines to invent one.

Actual hybrid library answer, run 3, produced by
`generate.py::answer_from_chunks` and saved in the hybrid-retest report:

```text
I don't have enough information to answer when the library closes (thread_study_spots.txt and thread_internship_timing.txt).
```

The deadline chunk stays third because the first-year chunk ranks second
semantically and first lexically, while the group-project chunk ranks first
semantically and fourth lexically. Their combined scores still exceed the
late-work chunk's score. The syllabus qualification appears in 1/3 hybrid
deadline answers versus 0/3 in the prompt-only run, but this small improvement
in generated wording does not establish a reliable fix or a ranking gain.
All hybrid calls were under three seconds; the earlier 69.9-second call remains
in its original result set, and these timings do not prove hybrid search
caused faster service responses.

**Verification and invalid-run handling:** Five focused unit tests pass,
covering exact-term promotion, unmatched-keyword fallback, refusal preservation,
single-result gate preservation, and Unicode/numeric tokenization. The smoke
test passes across all four corpora. During the first hybrid evaluation, the
starter smoke test was mistakenly run against the working database and
overwrote real embeddings with its fake test embeddings. That evaluation is
explicitly marked invalid in `results/run_2026-10-04_1607_hybrid.md` and
`results/milestone4_hybrid_evidence.json` and is excluded from every comparison.
The smoke test now uses a temporary database. Real embeddings were restored
using the unchanged corpus and chunker, all five original best distances were
checked against the baseline after the isolated smoke test, and only then was
the valid hybrid-retest evaluation performed. Baseline and prompt-only result
files were not altered.

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
