"""
server/app.py — Mistake Analyzer (Meta PyTorch Hackathon)
==========================================================
Authoritative entrypoint as declared in:
  - Dockerfile    : CMD ["uvicorn", "server.app:app", ...]
  - pyproject.toml: server = "server.app:main"

Load order (no NameError):
  1. imports
  2. grader functions   (defined first)
  3. tasks              (graders already exist — safe to reference)
  4. FastAPI app+routes (tasks already exist — safe to reference)
  5. main() / __main__ entrypoint
"""

import os
import sys
import re

from fastapi import FastAPI
import uvicorn


# ===========================================================================
# GRADER FUNCTIONS  — defined FIRST so tasks can safely reference them
# Each grader accepts (predicted, expected) and returns bool or float score.
# ===========================================================================

def grade_detection(predicted, expected) -> bool:
    """
    Grade the error-detection task.
    Returns True if predicted boolean/truthy value matches expected.
    """
    if isinstance(predicted, str):
        predicted = predicted.strip().lower() in ("true", "yes", "1", "error detected")
    return bool(predicted) == bool(expected)


def grade_correction(predicted, expected) -> float:
    """
    Grade the grammar-correction task.
    Returns a float score in [0.0, 1.0] based on token-level overlap.
    A perfect match scores 1.0; a completely wrong correction scores 0.0.
    """
    if not isinstance(predicted, str) or not isinstance(expected, str):
        return 0.0
    pred_tokens = set(re.sub(r"[^\w\s]", "", predicted.lower()).split())
    exp_tokens  = set(re.sub(r"[^\w\s]", "", expected.lower()).split())
    if not exp_tokens:
        return 1.0 if not pred_tokens else 0.0
    overlap = len(pred_tokens & exp_tokens)
    return round(overlap / len(exp_tokens), 4)


def grade_classification(predicted, expected) -> bool:
    """
    Grade the error-classification task.
    Returns True if the predicted error category matches the expected one
    (case-insensitive, whitespace-normalised).
    """
    if not isinstance(predicted, str) or not isinstance(expected, str):
        return False
    return predicted.strip().lower() == expected.strip().lower()


def grade_explanation(predicted, expected) -> float:
    """
    Grade the explanation task.
    Returns a float in [0.0, 1.0] measuring keyword coverage in the
    predicted explanation relative to expected keywords.
    """
    if not isinstance(predicted, str) or not isinstance(expected, str):
        return 0.0
    expected_keywords = set(re.sub(r"[^\w\s]", "", expected.lower()).split())
    predicted_words   = set(re.sub(r"[^\w\s]", "", predicted.lower()).split())
    if not expected_keywords:
        return 1.0
    matched = len(expected_keywords & predicted_words)
    return round(matched / len(expected_keywords), 4)


# ===========================================================================
# GLOBAL TASKS LIST  — defined AFTER graders so references are valid
# Must be at module level, NOT inside any function.
# ===========================================================================

tasks = [
    # ------------------------------------------------------------------
    # Task 1: Error Detection
    # Model must decide whether the input sentence contains a grammar error.
    # ------------------------------------------------------------------
    {
        "name": "error_detection",
        "input": "He go to school every day.",
        "expected_output": True,          # sentence HAS an error
        "grader": grade_detection,
    },

    # ------------------------------------------------------------------
    # Task 2: Grammar Correction
    # Model must return the corrected version of the sentence.
    # ------------------------------------------------------------------
    {
        "name": "grammar_correction",
        "input": "She don't like the homeworks.",
        "expected_output": "She doesn't like the homework.",
        "grader": grade_correction,
    },

    # ------------------------------------------------------------------
    # Task 3: Error Classification
    # Model must identify the grammatical category of the error.
    # ------------------------------------------------------------------
    {
        "name": "error_classification",
        "input": "They was playing in the park.",
        "expected_output": "subject-verb agreement",
        "grader": grade_classification,
    },

    # ------------------------------------------------------------------
    # Task 4 (bonus): Explanation
    # Model should explain why the sentence is wrong.
    # ------------------------------------------------------------------
    {
        "name": "error_explanation",
        "input": "I has been waiting for an hour.",
        "expected_output": "subject-verb agreement error: 'I' requires 'have', not 'has'",
        "grader": grade_explanation,
    },
]

# ---------------------------------------------------------------------------
# Debug / Validator confirmation — printed at import time
# ---------------------------------------------------------------------------
print("TASKS LOADED:", tasks, flush=True)
print(f"[INFO] Total tasks registered: {len(tasks)}", flush=True)
for _t in tasks:
    print(f"  - {_t['name']} | grader={_t['grader'].__name__}", flush=True)


# ===========================================================================
# FASTAPI APP + ROUTES — defined AFTER tasks (safe to reference tasks here)
# ===========================================================================

app = FastAPI(title="Mistake Analyzer", version="1.0.0")


@app.get("/")
def home():
    return {"message": "Mistake Analyzer is running", "tasks": len(tasks)}


@app.get("/tasks")
def get_tasks():
    """Return task metadata (grader is not JSON-serialisable, so excluded)."""
    return [
        {
            "name": t["name"],
            "input": t["input"],
            "expected_output": t["expected_output"],
        }
        for t in tasks
    ]


@app.post("/reset")
def reset():
    return {"status": "reset"}


@app.post("/step")
def step():
    return {"reward": 0.5}


@app.get("/state")
def state():
    return {"state": "ok"}


# ===========================================================================
# ENTRYPOINT
# ===========================================================================

def main():
    port = int(os.getenv("PORT", 7860))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    main()
