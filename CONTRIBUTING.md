# Contributing to sorowatch-ai-agent

## Setup
```
python -m venv .venv
.venv\Scripts\activate      # PowerShell
pip install -r requirements.txt
python -m pytest
uvicorn app.main:app --reload
```

## Before opening a PR
- Run python -m pytest and make sure it passes.
- New scoring heuristics belong in app/scoring.py as pure functions with
  their own tests in tests/test_scoring.py.
- Keep the PR scoped to one issue; reference it with `Closes #N`.

## Related repos
- sorowatch-contract — the Soroban contract this service ultimately flags on
- sorowatch-backend — coordinates calls to this service and the contract
- sorowatch-frontend — dashboard reading data derived from this pipeline
