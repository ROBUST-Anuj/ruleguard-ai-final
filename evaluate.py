#!/usr/bin/env python3
"""
RuleGuard Evaluation Script
============================
Runs all evaluation datasets against the RuleGuard API and produces
human-readable and machine-readable results.

Usage:
    python evaluate.py                     # full evaluation
    python evaluate.py --category supported # only supported questions
"""
import os
import sys
import json
import time
import argparse
import httpx

API_URL = os.getenv("RULEGUARD_API_URL", "http://localhost:8000/api/query")
TIMEOUT = 60.0

DATA_DIR = os.path.join("data", "evaluation")
RESULTS_DIR = "evaluation"


def load_dataset(filename: str) -> list:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"  ⚠ Dataset not found: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def query_api(question: str, client: httpx.Client) -> dict | None:
    try:
        resp = client.post(API_URL, json={"question": question})
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  ✗ API error: {e}")
        return None


def evaluate_supported(items: list, client: httpx.Client) -> list:
    results = []
    for item in items:
        qid = item["id"]
        question = item["question"]
        expected = item["expected_state"]

        resp = query_api(question, client)
        if resp is None:
            results.append({
                "question_id": qid,
                "question": question,
                "expected_state": expected,
                "predicted_state": "ERROR",
                "state_correct": False,
                "answer": "",
                "predicted_sources": [],
                "citation_correct": False,
            })
            continue

        predicted = resp.get("state", "UNKNOWN")
        state_ok = predicted == expected

        # Check citations
        citations = resp.get("citations", [])
        predicted_sources = [c.get("document", "") for c in citations]
        expected_sources = item.get("expected_sources", [])

        citation_ok = False
        if predicted_sources and expected_sources:
            expected_docs = {s.split("#")[0] for s in expected_sources}
            predicted_docs = set(predicted_sources)
            citation_ok = bool(expected_docs & predicted_docs)
        elif not expected_sources:
            citation_ok = True

        results.append({
            "question_id": qid,
            "question": question,
            "expected_state": expected,
            "predicted_state": predicted,
            "state_correct": state_ok,
            "answer": resp.get("answer", "")[:200],
            "expected_sources": expected_sources,
            "predicted_sources": predicted_sources,
            "citation_correct": citation_ok,
        })

        icon = "✓" if state_ok else "✗"
        print(f"  {icon} [{qid}] {predicted:15s} (expected {expected})")

    return results


def evaluate_contradictions(items: list, client: httpx.Client) -> list:
    results = []
    for item in items:
        qid = item["id"]
        question = item["question"]
        expected = item["expected_state"]

        resp = query_api(question, client)
        if resp is None:
            results.append({
                "question_id": qid,
                "question": question,
                "expected_state": expected,
                "predicted_state": "ERROR",
                "state_correct": False,
                "answer": "",
                "predicted_sources": [],
                "citation_correct": False,
            })
            continue

        predicted = resp.get("state", "UNKNOWN")
        state_ok = predicted == expected

        citations = resp.get("citations", [])
        predicted_sources = [c.get("document", "") for c in citations]

        results.append({
            "question_id": qid,
            "question": question,
            "expected_state": expected,
            "predicted_state": predicted,
            "state_correct": state_ok,
            "expected_contradiction_id": item.get("expected_contradiction_id", ""),
            "answer": resp.get("answer", "")[:200],
            "predicted_sources": predicted_sources,
            "citation_correct": len(predicted_sources) >= 2,
        })

        icon = "✓" if state_ok else "✗"
        print(f"  {icon} [{qid}] {predicted:15s} (expected {expected})")

    return results


def evaluate_unanswerable(items: list, client: httpx.Client) -> list:
    results = []
    for item in items:
        qid = item["id"]
        question = item["question"]
        expected = item["expected_state"]

        resp = query_api(question, client)
        if resp is None:
            results.append({
                "question_id": qid,
                "question": question,
                "expected_state": expected,
                "predicted_state": "ERROR",
                "state_correct": False,
                "answer": "",
            })
            continue

        predicted = resp.get("state", "UNKNOWN")
        state_ok = predicted == expected

        results.append({
            "question_id": qid,
            "question": question,
            "expected_state": expected,
            "predicted_state": predicted,
            "state_correct": state_ok,
            "answer": resp.get("answer", "")[:200],
        })

        icon = "✓" if state_ok else "✗"
        print(f"  {icon} [{qid}] {predicted:15s} (expected {expected})")

    return results


def print_banner(text: str):
    print(f"\n{'=' * 50}")
    print(f"  {text}")
    print(f"{'=' * 50}")


def main():
    parser = argparse.ArgumentParser(description="RuleGuard Evaluation")
    parser.add_argument("--category", choices=["supported", "contradiction", "unanswerable"],
                        help="Run only a specific category")
    args = parser.parse_args()

    print_banner("RULEGUARD EVALUATION")
    print(f"API: {API_URL}\n")

    # Check API health
    try:
        health = httpx.get(API_URL.replace("/query", "/health"), timeout=10)
        health_data = health.json()
        print(f"API Status: {health_data.get('status', 'unknown')}")
        print(f"Index loaded: {health_data.get('index_loaded', False)}\n")
    except Exception as e:
        print(f"✗ Cannot reach API: {e}")
        print("Make sure the backend is running: uvicorn backend.app.main:app --port 8000")
        sys.exit(1)

    all_results = {
        "supported": [],
        "contradiction": [],
        "unanswerable": [],
    }

    client = httpx.Client(timeout=TIMEOUT)

    try:
        # Supported questions
        if args.category is None or args.category == "supported":
            print_banner("SUPPORTED QUESTIONS")
            supported = load_dataset("answerable_questions.json")
            all_results["supported"] = evaluate_supported(supported, client)

        # Contradiction questions
        if args.category is None or args.category == "contradiction":
            print_banner("CONTRADICTION QUESTIONS")
            contradictions = load_dataset("contradiction_questions.json")
            all_results["contradiction"] = evaluate_contradictions(contradictions, client)

        # Unanswerable questions
        if args.category is None or args.category == "unanswerable":
            print_banner("UNANSWERABLE QUESTIONS")
            unanswerable = load_dataset("unanswerable_questions.json")
            all_results["unanswerable"] = evaluate_unanswerable(unanswerable, client)
    finally:
        client.close()

    # Compute statistics
    print_banner("RESULTS SUMMARY")

    total_correct = 0
    total_questions = 0
    total_citations_correct = 0
    total_citations_checked = 0

    for category, label in [("supported", "SUPPORTED"), ("contradiction", "CONTRADICTION"),
                            ("unanswerable", "UNANSWERABLE (Correct Refusal)")]:
        results = all_results[category]
        if not results:
            continue
        correct = sum(1 for r in results if r["state_correct"])
        count = len(results)
        pct = (correct / count * 100) if count > 0 else 0
        total_correct += correct
        total_questions += count
        print(f"  {label:40s} {correct:3d}/{count:<3d}  ({pct:.1f}%)")

        # Citation accuracy for supported/contradiction
        if category in ("supported", "contradiction"):
            cite_correct = sum(1 for r in results if r.get("citation_correct", False))
            total_citations_correct += cite_correct
            total_citations_checked += count

    if total_citations_checked > 0:
        cite_pct = total_citations_correct / total_citations_checked * 100
        print(f"\n  {'CITATION ACCURACY':40s} {total_citations_correct:3d}/{total_citations_checked:<3d}  ({cite_pct:.1f}%)")

    overall_pct = (total_correct / total_questions * 100) if total_questions > 0 else 0
    print(f"\n  {'OVERALL':40s} {total_correct:3d}/{total_questions:<3d}  ({overall_pct:.1f}%)")
    print(f"{'=' * 50}\n")

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "api_url": API_URL,
        "summary": {
            "total_correct": total_correct,
            "total_questions": total_questions,
            "overall_accuracy": round(overall_pct, 2),
        },
        "categories": {},
        "per_question": [],
    }

    for category in ("supported", "contradiction", "unanswerable"):
        results = all_results[category]
        if results:
            correct = sum(1 for r in results if r["state_correct"])
            output["categories"][category] = {
                "correct": correct,
                "total": len(results),
                "accuracy": round(correct / len(results) * 100, 2) if results else 0,
            }
            output["per_question"].extend(results)

    results_path = os.path.join(RESULTS_DIR, "results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Detailed results saved to: {results_path}")


if __name__ == "__main__":
    main()
