# GitHub Copilot — InstallForge

A monorepo: a **marketplace of curated install recipes** + a **skill agent** that
installs and verifies a product on a device.

## Stack

| Area | Tech |
|---|---|
| Agent (device-side) | Python ≥3.9, Pydantic v2, Typer, httpx |
| Registry API | Python, FastAPI, Uvicorn |
| Web marketplace | TypeScript, React 18, Vite, Vitest |
| Contracts | JSON Schema (`packages/schemas`) → Pydantic + TS types |
| Content | YAML recipes (`packages/recipes`) |

## Layout

- `apps/agent` — install + verify loop, device probe, CLI.
- `apps/registry` — serves recipes from `packages/recipes`.
- `apps/web` — marketplace UI.
- `packages/schemas` — source-of-truth JSON Schemas.
- `packages/recipes` — curated recipes (`<id>/recipe.yaml` + optional `notes.md`).

## Conventions

- **Python**: `from __future__ import annotations`; type everything; `typing.Optional/List`
  (not `X | None`) because we target 3.9. Pydantic models use `extra="forbid"`. Format/lint
  with ruff; type-check with mypy. Keep `installforge_agent/__init__.py` import-light.
- **TypeScript**: strict mode; `const` over `let`; named exports; `async/await`; early
  returns. Types mirror `packages/schemas`.
- **Recipes**: folder name must equal `id`; every `target` needs `steps` **and** `verify`;
  add real `known_issues` with `source` links.

## Testing (red/green TDD)

- Write a failing test first, confirm red, implement to green.
- Python: `pytest` in each app (`pythonpath=["src"]`). Web: `vitest`.
- A recipe is only "done" when it validates against the schema **and** its `verify`
  checks define a real evidence gate.

## Boundaries

- Don't refactor or "clean up" unrelated code unless asked.
- Never remove existing tests; add tests with every change.
- Never hardcode secrets; never put secrets in recipes or run reports.
- Agent must default to **dry-run**; `elevated` (sudo) steps require explicit intent.
- Keep changes small and focused; provide test evidence in PRs.
