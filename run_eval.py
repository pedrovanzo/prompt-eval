#!/usr/bin/env python3
"""
Prompt eval runner — uses the `claude` CLI instead of the Anthropic SDK.
Replace SDK calls like client.messages.create(...) with call_claude().
"""

import subprocess
import json
import csv
from pathlib import Path
from prompts import prompt_v1


def call_claude(prompt: str, system: str = "") -> str:
    """Drop-in replacement for client.messages.create()."""
    cmd = ["claude", "-p", prompt]
    if system:
        cmd += ["--system-prompt", system]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def load_dataset(path: str) -> list[dict]:
    """Load eval cases from a JSON or CSV file."""
    p = Path(path)
    if p.suffix == ".json":
        return json.loads(p.read_text())
    elif p.suffix == ".csv":
        with open(p) as f:
            return list(csv.DictReader(f))
    raise ValueError(f"Unsupported format: {p.suffix}")


def save_results(results: list[dict], path: str):
    Path(path).write_text(json.dumps(results, indent=2))
    print(f"Results saved to {path}")


# --- Fill these in as the module progresses ---

def run_eval(dataset_path: str, results_path: str):
    dataset = load_dataset(dataset_path)
    results = []

    for case in dataset:
        response = call_claude(prompt_v1(case["task"]))

        # TODO: replace with your grading logic (exact match, model-as-judge, etc.)
        passed = response.strip().lower() == case.get("expected", "").strip().lower()

        results.append({**case, "response": response, "passed": passed})
        print(f"[{'PASS' if passed else 'FAIL'}] {case.get('id', '?')}")

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n{passed}/{total} passed ({100*passed//total}%)")
    save_results(results, results_path)


if __name__ == "__main__":
    run_eval("data/dataset.json", "results/output.json")
