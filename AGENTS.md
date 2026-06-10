# AGENTS.md

Operating guide for coding agents in the InstallForge monorepo. (See `CLAUDE.md` for a
deeper map; this file is the quick contract.)

## Setup

```bash
# Python apps (run inside each app dir)
cd apps/agent    && python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
cd apps/registry && python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"

# Web (pnpm workspace, from repo root)
pnpm install
```

## Code style

- **Python ≥3.9**: `from __future__ import annotations` in every module. Use
  `typing.Optional/List/Dict` (not `X | None`/`list[str]` at runtime — Pydantic 3.9).
  Pydantic v2 with `extra="forbid"`. Lint `ruff check .` (`E,F,I,B`), type `mypy --strict`.
- **TypeScript**: strict mode; `const` over `let`; **named exports**; `async/await`;
  early returns. UI types mirror `packages/schemas`. ESLint flat config + Prettier (100 cols).
- **Recipes (YAML)**: folder name == `id`; every `target` has `steps` + `verify`; encode
  real failures as `known_issues` with `source` + `confidence`.

## Testing (red/green TDD)

- Write the failing test first, confirm it fails, then implement until green.
- Python: `pytest` in each app (`pythonpath=["src"]`). Web: `pnpm --filter @installforge/web test`.
- Name tests `test_<behavior>_when_<condition>`. Cover error paths and edge cases.
- **Never remove existing tests.** A recipe change must keep `test_recipes_schema.py` green.

## PR instructions

- Title: `[<area>] <summary>` where area ∈ {agent, registry, web, recipes, docs}.
- Include **evidence**: test output and/or manual-run notes (e.g. `installforge probe`).
- Keep PRs small and single-purpose. Review AI-written code **and** the PR description
  yourself before submitting — they can be confidently wrong.
- CI (`.github/workflows/ci.yml`) must pass: ruff + pytest (Python), typecheck + lint +
  vitest (web).
