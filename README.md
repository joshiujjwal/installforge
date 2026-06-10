# InstallForge

> 🚧 **Early Development** — A marketplace of curated install recipes + a skill agent
> that installs **and verifies** any product on any device.

Pick a product (Flutter, GIMP, Docker…), point it at your device, and an agent runs a
curated, self-verifying recipe — recovering from common failures using built-in
troubleshooting knowledge — until the install is **proven** to work.

```bash
installforge install flutter        # plan it (dry-run)
installforge install flutter --execute
```

## Why

Install docs are scattered, version-specific, and full of platform gotchas. InstallForge
curates that knowledge into a **runnable, schema-validated recipe** with embedded
troubleshooting (TSG), then has an agent execute and verify it on the real device.

## Tech stack

| Area | Tech |
|---|---|
| Agent (device-side) | Python ≥3.9 · Pydantic v2 · Typer · httpx |
| Registry API | Python · FastAPI · Uvicorn |
| Web marketplace | TypeScript · React 18 · Vite · Vitest |
| Contracts | JSON Schema → Pydantic + TS types |
| Content | YAML recipes with curated `known_issues` |

## Getting started

```bash
git clone <repo-url> installforge && cd installforge

# Agent (device-side CLI)
cd apps/agent && python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" && pytest && installforge probe

# Registry API (in another shell)
cd apps/registry && python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" && pytest
uvicorn installforge_registry.main:app --reload   # http://localhost:8000

# Web marketplace
pnpm install
pnpm --filter @installforge/web dev               # http://localhost:5173
```

## Project structure

```
installforge/
├── apps/
│   ├── agent/      # Python: install + verify skill-agent loop, device probe, CLI
│   ├── registry/   # Python: FastAPI API serving curated recipes
│   └── web/        # TypeScript: React marketplace UI
├── packages/
│   ├── recipes/    # Curated recipes (<id>/recipe.yaml + notes.md)
│   └── schemas/    # Source-of-truth JSON Schemas
├── docs/           # spec.md + ADRs
└── .github/        # Copilot instructions, skills, CI
```

## Contributing

- **Red/green TDD**: write a failing test first, confirm red, implement to green.
- **Evidence in PRs**: include test output / manual-run notes. Never ship unreviewed
  AI-generated code or PR descriptions.
- **Small, focused PRs**: one concern at a time. Never remove existing tests.
- **Recipes**: every target must have a `verify` evidence gate and real `known_issues`.

See [`docs/spec.md`](docs/spec.md), [`TODO.md`](TODO.md), and
[`AGENTS.md`](AGENTS.md) / [`CLAUDE.md`](CLAUDE.md).
