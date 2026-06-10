# ADR 0002: Monorepo layout, recipe format, and shared models

> Status: Accepted · Date: 2026-06-07

## Context

InstallForge spans three deployables (device-side agent, registry API, web
marketplace) across two languages (Python, TypeScript) that must agree on one domain:
the **recipe** and **device config**. We need a structure that keeps these in sync and
lets an agent pick up work across any part of the repo.

## Decision

1. **Monorepo** with `apps/*` (deployables) and `packages/*` (shared content/contracts).
   JS is wired via a pnpm workspace; each Python app has its own `pyproject.toml`.
2. **JSON Schema is the source of truth** for the domain (`packages/schemas/`). Python
   mirrors it as Pydantic models; TypeScript mirrors the UI-facing subset.
3. **Recipes are YAML** under `packages/recipes/<id>/recipe.yaml`, folder name == `id`,
   each with at least one `target` carrying both `steps` and `verify` (the evidence gate),
   plus curated `known_issues` (TSG).
4. **Verification is mandatory** — a recipe target without `verify` is invalid.

## Consequences

- Positive: one place for recipes; schema-validated in CI; agent can reason over the
  whole system from a single checkout.
- Negative: the registry currently reads recipes as raw dicts, duplicating light parsing
  instead of reusing the Pydantic models.
- Follow-up: promote the Pydantic models into a shared `packages/core` Python package
  consumed by both `apps/agent` and `apps/registry`; generate TS types from JSON Schema.

## Alternatives considered

- **Polyrepo** — rejected: recipe/schema drift and painful cross-cutting changes.
- **Recipes embedded per app** — rejected: duplication; the content library is the product.
- **Markdown-only recipes** — rejected: not machine-runnable or verifiable.
