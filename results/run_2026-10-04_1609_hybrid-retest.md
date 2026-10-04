# Run log — hybrid-retest

- Produced by: `run_eval.py::main`
- Chunking: `chunker.py::split_documents` · 500-character maximum · 1-sentence overlap
- Corpus: `advice_threads` (index variant `default`)
- Indexed chunks: 42
- Retrieval: `store.py::search` · TOP_K = 3 · relevance cutoff = 0.60
- Embedding model: `all-MiniLM-L6-v2`
- Runs per question: 3, caching off
- When: 2026-10-04 16:09

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
| What is the capital of Mongolia? | 0.9290 | refused |
| How do I change the oil in a diesel engine? | 0.9121 | refused |
| Who won the 1994 World Cup? | 0.9165 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.8097 | refused |
| How do I write a for loop in Rust? | 0.8712 | refused |

---

## Real output

This is what the system actually produced. Paste the relevant parts
into your README underneath the table — the rubric asks for real
output as text, not a description of it.

### What to do if I cannot finish my assignment by deadline? — run 1

- Best distance: 0.4775 (passed the gate)
- Sources retrieved: thread_first_year_regret.txt, thread_group_project.txt, thread_late_work.txt

```
According to thread_late_work.txt, you should ask for an extension before the deadline rather than after. Almost everyone will grant a couple of days if you ask beforehand, but almost nobody will if you ask after the deadline has passed.
```

### What to do if I cannot finish my assignment by deadline? — run 2

- Best distance: 0.4775 (passed the gate)
- Sources retrieved: thread_first_year_regret.txt, thread_group_project.txt, thread_late_work.txt

```
You should ask for an extension before the deadline rather than after, as almost everyone will grant two days if you ask ahead of time, but almost nobody will on the following Monday (thread_late_work.txt).
```

### What to do if I cannot finish my assignment by deadline? — run 3

- Best distance: 0.4775 (passed the gate)
- Sources retrieved: thread_first_year_regret.txt, thread_group_project.txt, thread_late_work.txt

```
You should ask before the deadline rather than after, as almost everyone will grant an extension (such as two days if you ask in advance) while almost nobody will on the following Monday (thread_late_work.txt). Additionally, policies are entirely instructor-dependent, so you must check the syllabus since stated penalties, such as 10% a day, are accurate (thread_late_work.txt).
```

### What study spots do you know that have good coffee nearby? — run 1

- Best distance: 0.4259 (passed the gate)
- Sources retrieved: thread_first_gen.txt, thread_study_spots.txt

```
Ridgeway Café is recommended as a study spot that has good coffee, provided you go before 10am (*thread_study_spots.txt*).
```

### What study spots do you know that have good coffee nearby? — run 2

- Best distance: 0.4259 (passed the gate)
- Sources retrieved: thread_first_gen.txt, thread_study_spots.txt

```
Based on the provided documents, Ridgeway Café is suggested as a study spot that has good coffee (though it is recommended before 10am because it is empty, quiet, and they don't push you out). 

Source: `thread_study_spots.txt`
```

### What study spots do you know that have good coffee nearby? — run 3

- Best distance: 0.4259 (passed the gate)
- Sources retrieved: thread_first_gen.txt, thread_study_spots.txt

```
Ridgeway Café is recommended as a study spot that has good coffee, provided you go before 10am (*thread_study_spots.txt*).
```

### I want to transfer credits for my major. My department agreed verbally. — run 1

- Best distance: 0.2538 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_transfer_credits.txt

```
You should get that agreement in writing from the department before you rely on it, because a verbal yes might not survive a staff change (thread_transfer_credits.txt). Additionally, toward the major, transfer credits are decided on a case-by-case basis by the department rather than the registrar (thread_transfer_credits.txt).
```

### I want to transfer credits for my major. My department agreed verbally. — run 2

- Best distance: 0.2538 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_transfer_credits.txt

```
A verbal agreement is not reliable; you should get the approval in writing from the department before relying on it, as department decisions are made on a case-by-case basis (thread_transfer_credits.txt).
```

### I want to transfer credits for my major. My department agreed verbally. — run 3

- Best distance: 0.2538 (passed the gate)
- Sources retrieved: thread_changing_major.txt, thread_transfer_credits.txt

```
A verbal agreement is not sufficient; you should get it in writing from the department before relying on it, because a verbal yes might not survive a staff change (thread_transfer_credits.txt).
```

### Can I change my meal plan? — run 1

- Best distance: 0.4137 (passed the gate)
- Sources retrieved: thread_meal_plan_tier.txt, thread_transfer_credits.txt

```
Yes, you can change your meal plan, but you can only change it once and only in the first ten days of the semester (`thread_meal_plan_tier.txt`).
```

### Can I change my meal plan? — run 2

- Best distance: 0.4137 (passed the gate)
- Sources retrieved: thread_meal_plan_tier.txt, thread_transfer_credits.txt

```
Yes, you can change your meal plan, but you can only change it once and only in the first ten days of the semester (`thread_meal_plan_tier.txt`).
```

### Can I change my meal plan? — run 3

- Best distance: 0.4137 (passed the gate)
- Sources retrieved: thread_meal_plan_tier.txt, thread_transfer_credits.txt

```
Yes, you can change your meal plan, but you can only change it once and only in the first ten days (*thread_meal_plan_tier.txt*).
```

### When does library close — run 1

- Best distance: 0.5827 (passed the gate)
- Sources retrieved: thread_internship_timing.txt, thread_study_spots.txt

```
I do not have enough information to answer when the library closes. 

Source: thread_study_spots.txt and thread_internship_timing.txt
```

### When does library close — run 2

- Best distance: 0.5827 (passed the gate)
- Sources retrieved: thread_internship_timing.txt, thread_study_spots.txt

```
I do not have enough information to answer when the library closes. 

Source: thread_study_spots.txt and thread_internship_timing.txt
```

### When does library close — run 3

- Best distance: 0.5827 (passed the gate)
- Sources retrieved: thread_internship_timing.txt, thread_study_spots.txt

```
I don't have enough information to answer when the library closes (thread_study_spots.txt and thread_internship_timing.txt).
```
