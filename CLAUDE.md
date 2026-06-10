# CLAUDE.md

Context for AI agents working in InstallForge. Read `TODO.md` and **run the tests first**.

## What this is

A monorepo: a marketplace of curated **install recipes** + a **skill agent** that installs
and **verifies** a product on a device, recovering from failures via curated `known_issues`.

## Commands

```bash
# Python agent
cd apps/agent && python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
pytest                  # run tests
ruff check . && mypy .  # lint + types
installforge probe      # CLI: print this device's DeviceConfig

# Python registry
cd apps/registry && python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
pytest
uvicorn installforge_registry.main:app --reload   # http://localhost:8000

# Web
pnpm install
pnpm --filter @installforge/web test       # vitest
pnpm --filter @installforge/web typecheck
pnpm --filter @installforge/web dev
```

## Directory map

| Path | Purpose |
|---|---|
| `apps/agent/src/installforge_agent/models.py` | Domain models (source of truth in code). |
| `apps/agent/src/installforge_agent/device.py` | Device probe → `DeviceConfig`. |
| `apps/agent/src/installforge_agent/loop.py` | Install + verify loop (skeleton; see spec). |
| `apps/agent/src/installforge_agent/cli.py` | `installforge` Typer CLI. |
| `apps/registry/src/installforge_registry/` | FastAPI app + recipe loader. |
| `apps/web/src/` | React marketplace (types, api client, App). |
| `packages/schemas/` | JSON Schemas — domain source of truth. |
| `packages/recipes/<id>/recipe.yaml` | Curated recipes (folder name == `id`). |
| `docs/spec.md`, `docs/adr/` | Spec and architecture decisions. |

## Conventions & gotchas

- **Python ≥3.9**: every module starts with `from __future__ import annotations`. Use
  `typing.Optional/List/Dict` — **not** `X | None` or `list[str]` in runtime positions;
  Pydantic resolves annotations at runtime on 3.9. Ruff is scoped to `E,F,I,B` for this.
- Pydantic models use `extra="forbid"` — unknown recipe keys fail validation (intentional).
- Keep `installforge_agent/__init__.py` import-light (no typer/httpx) so smoke tests stay cheap.
- The registry reads recipes as **raw dicts** today (decoupled from the agent package); see ADR 0002.
- Recipe rule: every `target` must have `steps` **and** `verify` (the evidence gate). The test
  `apps/agent/tests/test_recipes_schema.py` enforces this.
- Resolve repo paths via `Path(__file__).resolve().parents[N]` (agent tests use `[3]`,
  registry loader uses `[4]`).

## Workflow

1. Read `TODO.md`; pick the next unchecked task in the lowest open phase.
2. **Run the existing tests** to orient and confirm a green baseline.
3. Red/green TDD: write the failing test, confirm red, implement to green.
4. Review the diff; commit with a descriptive message + co-author trailer.
5. If you learned something reusable, update this file and `AGENTS.md` (compound loop) and
   add a note to `TODO.md` → Lessons Learned.

## Boundaries

- Don't refactor unrelated code; don't remove tests; keep PRs small with test evidence.
- Agent defaults to **dry-run**; `elevated` (sudo) steps require explicit intent.
- Never put secrets in recipes, run reports, or code.
