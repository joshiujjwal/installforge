# InstallForge — Task Breakdown

## How to use this file

Workflow per task (evidence-gated — do not skip the gate):

1. Write tests **first** (red phase) and confirm they fail.
2. Implement until tests pass (green phase).
3. Review the diff manually.
4. Commit with a descriptive message.
5. Update `CLAUDE.md` / `AGENTS.md` if you learned something new (compound loop).

A phase is "done" only when its tests pass **and** a human has reviewed the evidence.

---

## Phase 0: Foundation ✅ (scaffolded)
- [x] Monorepo layout (`apps/*`, `packages/*`)
- [x] Python apps with `pyproject.toml`, ruff, mypy config
- [x] Pytest + first smoke tests (agent 5 ✅, registry 4 ✅)
- [x] Recipe JSON Schema + Pydantic models + schema-validation test
- [x] Web app (Vite + React + Vitest) with first component test
- [x] CI workflow (GitHub Actions)
- [x] AI config: copilot-instructions, path instructions, add-recipe skill
- [ ] `pnpm install` and commit `pnpm-lock.yaml`
- [ ] Run `mypy` clean in both Python apps

## Phase 1: Recipe contract & registry ⬜
- [ ] Write `docs/spec.md` data-model section into tests (round-trip Recipe ⇄ YAML)
- [ ] Registry: `GET /recipes?product=&platform=&category=` filtering (red → green)
- [ ] Promote Pydantic models to shared `packages/core` (ADR 0002 follow-up)
- [ ] Registry validates recipes with the shared models (drop raw-dict parsing)
- [ ] Generate TS types from JSON Schema; replace hand-written `src/types.ts`

## Phase 2: Agent loop — install & verify ⬜
- [ ] `evaluate(check, result)`: failing tests for exit-code / stdout-contains / regex
- [ ] `CommandRunner` impl: real subprocess runner + a `FakeRunner` for tests
- [ ] Step execution with `expect` evaluation (red → green)
- [ ] `verify[]` evidence gate → set `RunReport.verified`
- [ ] Prerequisite resolution incl. recursive `install_recipe`
- [ ] Dry-run vs `--execute`; confirmation prompt for `elevated` steps

## Phase 3: Troubleshooting (TSG) recovery ⬜
- [ ] `detect` matching (stdout/stderr regex, exit_code) with tests
- [ ] Apply `known_issues.fix` steps, bounded by `MAX_FIX_ATTEMPTS`
- [ ] Integration test: scripted FakeRunner fails → fix applied → verify passes
- [ ] LLM fallback diagnosis from logs + recipe context (provider-abstracted)
- [ ] Guard against infinite fix loops

## Phase 4: Marketplace & feedback ⬜
- [ ] Web: recipe detail page (steps, TSG, sources)
- [ ] Web: search/filter by product/platform/category
- [ ] `POST /runs` ingest + per-platform success-rate stats
- [ ] "Install on my device" → copy CLI command with detected config

## Phase 5: Ship ⬜
- [ ] Package the agent CLI (pipx/uv tool) for macOS/Linux/Windows
- [ ] Security pass: no secrets, sandbox elevated steps, redact run reports
- [ ] Docs: authoring guide, quickstart, recorded demo
- [ ] Seed 10+ real recipes across platforms

## Parking Lot 🅿️
- Flutter tarball install target (no snap); Windows targets for both examples
- Recipe signing / trust model; version pinning & deprecation
- Offline / corporate-proxy / no-sudo constraint handling end-to-end

## Lessons Learned 📝
- Target Python 3.9 → keep `typing.Optional/List` (not `X | None`) so Pydantic resolves
  annotations at runtime; scoped ruff to `E,F,I,B` to avoid pyupgrade fighting that.
- Registry currently reads recipes as raw dicts to stay decoupled from the agent package;
  ADR 0002 tracks promoting models to `packages/core`.
