# Run log — after-chunking

- Produced by: `run_eval.py::main`
- Chunking: `chunker.py::split_documents` · 900-character maximum · 2-sentence overlap
- Corpus: `advice_threads` (index variant `default`)
- Indexed chunks: 23
- Retrieval: `store.py::search` · TOP_K = 5 · relevance cutoff = 0.60
- Embedding model: `all-MiniLM-L6-v2`
- Runs per question: 3, caching off
- When: 2026-10-04 16:27

This table is one row per QUESTION. The run log your README asks for is
one row per CRITERION, so aggregate these into it — criterion 1 is how many
of your questions had the answer in the retrieved chunks, and so on.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| What to do if I cannot finish my assignment by deadline? |   |   |   |
| What study spots do you know that have good coffee nearby? |   |   |   |
| I want to transfer credits for my major. My department agreed verbally. |   |   |   |
| Can I change my meal plan? |   |   |   |
| When does library close |   |   |   |

> The Run columns are blank because `scorer.py` doesn't exist yet.
> Judge each question yourself by reading the output below, or build
> the scorer first and re-run.

---

## The relevance gate on out-of-corpus questions

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.60. Refused 5 of 5.

Retrieval is deterministic and the gate is a comparison against a
fixed number, so these do not vary between runs — one pass over the
list is the whole measurement.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.9479 | refused |
| How do I change the oil in a diesel engine? | 0.9299 | refused |
| Who won the 1994 World Cup? | 0.9517 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.8280 | refused |
| How do I write a for loop in Rust? | 0.8712 | refused |

---

## Real output

This is what the system actually produced. Paste the relevant parts
into your README underneath the table — the rubric asks for real
output as text, not a description of it.

### What to do if I cannot finish my assignment by deadline? — run 1

- Best distance: 0.4515 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_first_year_regret.txt, thread_group_project.txt, thread_late_work.txt, thread_sleep_schedule.txt

```
You should ask for an extension before the deadline rather than after. Almost everyone will grant a couple of days if you ask beforehand, but almost nobody will if you ask after the deadline has passed (thread_late_work.txt). Additionally, if your lateness is due to a documented illness, you should go through the dean of students rather than the instructor (thread_late_work.txt).
```

### What to do if I cannot finish my assignment by deadline? — run 2

- Best distance: 0.4515 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_first_year_regret.txt, thread_group_project.txt, thread_late_work.txt, thread_sleep_schedule.txt

```
According to `thread_late_work.txt`, you should ask for an extension before the deadline rather than after, as almost everyone will grant an extra two days if asked in advance. Additionally, if the late submission is due to an illness, documented illness goes through the dean of students rather than the instructor.
```

### What to do if I cannot finish my assignment by deadline? — run 3

- Best distance: 0.4515 (passed the gate)
- Sources retrieved: thread_commuting.txt, thread_first_year_regret.txt, thread_group_project.txt, thread_late_work.txt, thread_sleep_schedule.txt

```
You should ask for an extension before the deadline rather than after. Almost everyone will give you two days if you ask beforehand, but almost nobody will on the following Monday (thread_late_work.txt). Additionally, if your lateness is due to a documented illness, you should go through the dean of students rather than the instructor (thread_late_work.txt).
```

### What study spots do you know that have good coffee nearby? — run 1

- Best distance: 0.4202 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_commuting.txt, thread_first_gen.txt, thread_first_year_regret.txt, thread_study_spots.txt

```
Ridgeway Café is recommended as a study spot before 10am because it has good coffee, is empty and quiet, and the staff do not push you out (thread_study_spots.txt).
```

### What study spots do you know that have good coffee nearby? — run 2

- Best distance: 0.4202 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_commuting.txt, thread_first_gen.txt, thread_first_year_regret.txt, thread_study_spots.txt

```
Ridgeway Café is recommended as a study spot that has good coffee (thread_study_spots.txt).
```

### What study spots do you know that have good coffee nearby? — run 3

- Best distance: 0.4202 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_commuting.txt, thread_first_gen.txt, thread_first_year_regret.txt, thread_study_spots.txt

```
Ridgeway Café is noted as a good study spot that has good coffee, provided you go before 10am (thread_study_spots.txt).
```

### I want to transfer credits for my major. My department agreed verbally. — run 1

- Best distance: 0.3092 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_clubs.txt, thread_first_year_regret.txt, thread_pass_fail.txt, thread_transfer_credits.txt

```
You should get the agreement in writing from the department before relying on it, as a verbal yes may not survive a staff change (*thread_transfer_credits.txt*).
```

### I want to transfer credits for my major. My department agreed verbally. — run 2

- Best distance: 0.3092 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_clubs.txt, thread_first_year_regret.txt, thread_pass_fail.txt, thread_transfer_credits.txt

```
You should get the agreement in writing from the department before relying on it, because a verbal agreement may not survive a staff change (*thread_transfer_credits.txt*).
```

### I want to transfer credits for my major. My department agreed verbally. — run 3

- Best distance: 0.3092 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_clubs.txt, thread_first_year_regret.txt, thread_pass_fail.txt, thread_transfer_credits.txt

```
You should get the agreement in writing from the department before relying on it, because a verbal agreement may not survive a staff change (thread_transfer_credits.txt).
```

### Can I change my meal plan? — run 1

- Best distance: 0.4680 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_first_year_regret.txt, thread_meal_plan_tier.txt, thread_textbook_editions.txt, thread_transfer_credits.txt

```
Yes, you can change your meal plan, but you can only change it once and only within the first ten days (thread_meal_plan_tier.txt).
```

### Can I change my meal plan? — run 2

- Best distance: 0.4680 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_first_year_regret.txt, thread_meal_plan_tier.txt, thread_textbook_editions.txt, thread_transfer_credits.txt

```
Yes, you can change your meal plan, but you can only change it once and only within the first ten days (*thread_meal_plan_tier.txt*).
```

### Can I change my meal plan? — run 3

- Best distance: 0.4680 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_first_year_regret.txt, thread_meal_plan_tier.txt, thread_textbook_editions.txt, thread_transfer_credits.txt

```
Yes, you can change your meal plan, but you can only change it once and only within the first ten days (thread_meal_plan_tier.txt).
```

### When does library close — run 1

- Best distance: 0.5720 (passed the gate)
- Sources retrieved: thread_internship_timing.txt, thread_laundry_timing.txt, thread_sleep_schedule.txt, thread_study_spots.txt, thread_textbook_editions.txt

```
According to `thread_sleep_schedule.txt`, the library is open until 2am.
```

### When does library close — run 2

- Best distance: 0.5720 (passed the gate)
- Sources retrieved: thread_internship_timing.txt, thread_laundry_timing.txt, thread_sleep_schedule.txt, thread_study_spots.txt, thread_textbook_editions.txt

```
Based on the documents provided, the library is open until 2am (thread_sleep_schedule.txt).
```

### When does library close — run 3

- Best distance: 0.5720 (passed the gate)
- Sources retrieved: thread_internship_timing.txt, thread_laundry_timing.txt, thread_sleep_schedule.txt, thread_study_spots.txt, thread_textbook_editions.txt

```
According to thread_sleep_schedule.txt, the library is open until 2am.
```
