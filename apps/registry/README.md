# installforge-registry

FastAPI service that serves curated recipes from `packages/recipes` to the web
marketplace and the device-side agent.

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness probe. |
| `GET` | `/recipes` | List recipe summaries (id, product, platforms). |
| `GET` | `/recipes/{id}` | Full recipe document. |

## Develop

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn installforge_registry.main:app --reload   # http://localhost:8000
```

> Roadmap: search/filter params, run-report ingestion (`POST /runs`), success-rate
> stats per platform, and auth for recipe submission. See `../../TODO.md`.
