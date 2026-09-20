# sorowatch-ai-agent

Standalone risk-scoring service for SoroWatch. Runs a real LangGraph
pipeline (gather_data -> score_risk -> decide_action) that pulls an
address's recent Stellar activity from Horizon and scores it with three
heuristics.

## Scoring heuristics (app/scoring.py)
- **Tx velocity** (0-40): many operations in a short time window scores
  higher than the same count spread over weeks.
- **Counterparty diversity** (0-30): activity concentrated with very few
  counterparties scores higher than diverse activity.
- **Volume anomaly** (0-30): a few outlier-large payments among mostly
  small ones scores higher than uniform amounts.

These are combined and capped at 100 in `compute_risk_score`.

## Run
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Test
```
python -m pytest
```
Tests cover the scoring heuristics directly (pure functions, no network)
and the full pipeline with mocked Horizon responses (via respx), including
a high-risk case, a no-history case, and threshold sensitivity.

## API
`POST /score` — body: `{"address": "G...", "threshold": 50}` — returns the
computed score, whether it crossed the threshold, and how many operations
were considered.
