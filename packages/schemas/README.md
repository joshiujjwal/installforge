# Shared Schemas

Source-of-truth JSON Schemas (draft 2020-12) for the InstallForge domain. Both the
Python apps and the TypeScript web app derive their types from these.

| Schema | Describes |
|---|---|
| `recipe.schema.json` | A curated install recipe: per-platform `targets` with prerequisites, ordered `steps`, `verify` checks (the evidence gate), and `known_issues` (TSG). |
| `device-config.schema.json` | A snapshot of the target device used to select a target and plan execution. |

## Keeping types in sync

- **Python**: `apps/agent/src/installforge_agent/models.py` mirrors these schemas as
  Pydantic models. The test `apps/agent/tests/test_recipes_schema.py` validates every
  recipe against the models.
- **TypeScript**: `apps/web/src/types.ts` mirrors the parts the UI consumes.

> ADR 0002 tracks the plan to promote the models into a shared `packages/core`
> Python package and generate TS types from the JSON Schema, so this stays DRY.
