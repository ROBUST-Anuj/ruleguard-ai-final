# RuleGuard Evaluation

## Overview

The evaluation suite tests RuleGuard's ability to correctly classify queries into three states:

1. **SUPPORTED** — The corpus contains sufficient evidence to answer (15 questions)
2. **CONTRADICTION** — Two or more corpus provisions conflict (10 questions)
3. **NOT_FOUND** — The corpus does not address the question (25 questions)

## Running the Evaluation

```bash
# Ensure the backend is running
uvicorn backend.app.main:app --port 8000

# Run full evaluation
python evaluate.py

# Run a specific category
python evaluate.py --category supported
python evaluate.py --category contradiction
python evaluate.py --category unanswerable
```

## Datasets

| File | Questions | Expected State |
|------|-----------|---------------|
| `data/evaluation/answerable_questions.json` | 15 | SUPPORTED |
| `data/evaluation/contradiction_questions.json` | 10 | CONTRADICTION |
| `data/evaluation/unanswerable_questions.json` | 25 | NOT_FOUND |

## Results

Results are saved to `evaluation/results.json` after each run.

The evaluation measures:
- **State classification accuracy** per category
- **Citation accuracy** for SUPPORTED and CONTRADICTION responses
- **Overall accuracy** across all 50 questions

## Note

Results depend on the LLM model used. Scores are not hardcoded — they reflect actual system performance.
