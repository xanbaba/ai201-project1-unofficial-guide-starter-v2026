"""Capture evaluation evidence without changing the question-answering pipeline.

Run from the repository root: .venv\Scripts\python.exe tools/milestone1_eval.py
Pass --label after to measure an improvement separately from the baseline.
The standard run_eval report is also produced, with three uncached answers per
question. This companion records the full retrievals, exact run_once timings,
and three read-only audits of every chunk in the existing index.
"""

import argparse
import datetime as dt
import json
from pathlib import Path
import sys
import time
from dataclasses import asdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import config
import generate
import ingest
import run_eval
import store


def audit_chunks():
    """Compare all indexed chunk headings with their actual source documents."""
    headings = {
        doc.source: doc.text.splitlines()[0]
        for doc in ingest.load_documents(config.CORPUS)
    }
    collection = store._client().get_collection(config.collection_name())
    raw = collection.get(include=["documents", "metadatas"])
    chunks = []
    for label, text, meta in zip(raw["ids"], raw["documents"], raw["metadatas"]):
        expected = headings[meta["source"]]
        actual = text.splitlines()[0]
        chunks.append({
            "label": label, "text": text, "produced_by": meta["produced_by"],
            "expected_heading": expected, "actual_heading": actual,
            "passed": expected.startswith("THREAD:") and actual == expected,
        })
    chunks.sort(key=lambda chunk: chunk["label"])
    return {"passed": sum(chunk["passed"] for chunk in chunks),
            "total": len(chunks), "chunks": chunks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", choices=["before", "after"], default="before")
    args = parser.parse_args()
    filename = "milestone1_before_evidence.json" if args.label == "before" else "milestone4_after_evidence.json"
    path = config.RESULTS_DIR / filename
    if path.exists():
        raise FileExistsError(f"Preserve existing evaluation evidence: {path}")
    assert store.index_exists(), "Evaluation requires the existing index"
    evidence = {
        "started_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "corpus": config.CORPUS, "model": config.MODEL,
        "embedding_model": config.EMBEDDING_MODEL,
        "top_k": config.TOP_K, "threshold": config.THRESHOLD,
        "label": args.label, "grounding_instruction": generate.GROUNDING_INSTRUCTION,
        "cache": False, "trials": [], "chunk_audits": [],
    }

    def save():
        path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")

    original = run_eval.run_once

    def measured_run_once(question, top_k, threshold, corpus, variant):
        # Start immediately before the original function, including lazy imports,
        # first-query initialization, retrieval, rate limiting, and generation.
        started = time.perf_counter()
        answer, results, decision = original(question, top_k, threshold, corpus, variant)
        elapsed = time.perf_counter() - started
        run = 1 + sum(trial["question"] == question for trial in evidence["trials"])
        evidence["trials"].append({
            "question": question, "run": run, "elapsed_seconds": elapsed,
            "answer": answer, "results": [asdict(result) for result in results],
            "decision": asdict(decision),
        })
        save()
        print(f"  elapsed: {elapsed:.6f} seconds", flush=True)
        return answer, results, decision

    run_eval.run_once = measured_run_once
    sys.argv = ["run_eval.py", "--label", args.label]
    try:
        run_eval.main()
    finally:
        run_eval.run_once = original
        evidence["usage"] = generate.usage()
        save()
    for run in range(1, 4):
        audit = audit_chunks()
        audit["run"] = run
        evidence["chunk_audits"].append(audit)
        print(f"Chunk headings run {run}: {audit['passed']}/{audit['total']}")
    evidence["finished_at_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    save()
    print(f"Supplementary evidence: {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
