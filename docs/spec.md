# InstallForge — Specification

> Status: Draft v0.1 · Owner: installforge-core · Updated: 2026-06-07

## 1. Overview

InstallForge is a **marketplace of curated install recipes** plus a **skill agent**
that actually installs and verifies a product on a target device. A user picks a
product (e.g. "Flutter", "GIMP", "Docker"), provides (or auto-detects) their device
config, and the agent runs the recipe end-to-end — recovering from common failures
using curated troubleshooting (TSG) knowledge — until installation is **verified**.

### Problem statement

Install instructions are scattered, version-specific, and riddled with platform
gotchas. Users burn hours stitching together docs, Stack Overflow, and GitHub issues.
InstallForge curates that knowledge into a runnable, self-verifying format and lets an
agent execute it on the actual device, closing the loop from "instructions" to
"it works on my machine."

### Goals

- Curate install knowledge as **structured, runnable recipes** with embedded TSG.
- An agent that installs + **verifies** on-device, adapting to failures.
- A marketplace to discover recipes and see real-world success rates per platform.

### Non-goals (v1)

- Configuration management / fleet orchestration (not Ansible/Puppet).
- Sandboxed remote execution as a service (agent runs on the user's own device).
- GUI-only installers with no scriptable path.

## 2. Requirements

### Functional

- [ ] FR1: Browse/search recipes by product, category, and platform.
- [ ] FR2: Fetch a single recipe with all platform `targets`.
- [ ] FR3: Detect the local device into a `DeviceConfig` (os, arch, package managers).
- [ ] FR4: Select the recipe `target` matching the device.
- [ ] FR5: Execute install `steps`, evaluating each against its `expect` check.
- [ ] FR6: On a step failure, match `known_issues` via `detect` and apply `fix` steps
      (bounded retries); otherwise fall back to LLM diagnosis from logs + recipe context.
- [ ] FR7: Run `verify` checks as an **evidence gate**; install is "successful" only
      if verification passes.
- [ ] FR8: Emit a `RunReport` (transcript, applied fixes, verify evidence, pass/fail).
- [ ] FR9: Submit anonymized run reports back to the registry to improve recipes.
- [ ] FR10: `--dry-run` (plan only) vs `--execute`; explicit confirmation for
      `elevated` (sudo) steps.

### Non-functional

- [ ] NFR1: Recipes validate against `packages/schemas/recipe.schema.json` in CI.
- [ ] NFR2: Agent execution is auditable — every command + output captured.
- [ ] NFR3: Safe by default — dry-run first; never run unreviewed destructive commands.
- [ ] NFR4: Cross-platform: macOS, Linux, Windows (agent host).
- [ ] NFR5: No secrets in recipes or run reports.

## 3. Data model

See `packages/schemas/` (JSON Schema) and `apps/agent/src/installforge_agent/models.py`
(Pydantic). Core entities:

- **Recipe** — `id`, `product`, `targets[]`, metadata.
- **Target** — `platform` (os/arch/version), `prerequisites[]`, `steps[]`, `verify[]`,
  `known_issues[]`.
- **Step** — `run` command, optional `expect` check, `elevated`, `idempotent`.
- **Check** — command + expectations (`expect_exit_code`, `expect_stdout_contains/regex`).
- **KnownIssue (TSG)** — `symptom`, `detect` (stdout/stderr regex, exit code), `cause`,
  `fix[]` steps, `source`, `confidence`.
- **DeviceConfig** — `os`, `arch`, `package_managers`, `installed`, `constraints`.
- **RunReport** — `recipe_id`, `device`, `steps[]` results, `verified`, `succeeded`.

## 4. Interfaces

### Registry API (`apps/registry`)

| Method | Path | Notes |
|---|---|---|
| GET | `/health` | Liveness. |
| GET | `/recipes` | Summaries; future: `?product=&platform=&category=`. |
| GET | `/recipes/{id}` | Full recipe. |
| POST | `/runs` | _Planned_: ingest run reports for success stats. |

### Agent CLI (`apps/agent`)

```
installforge probe                 # print DeviceConfig as JSON
installforge install <product>     # plan (dry-run) by default
installforge install <product> --execute
```

### Agent loop (FR4–FR8)

```
select_target → check prerequisites (recurse install_recipe)
  → for each step: run → evaluate(expect)
       fail → match known_issues(detect) → apply fix (≤ MAX_FIX_ATTEMPTS)
            → else LLM diagnose → retry
  → run verify[] (evidence gate) → RunReport
```

## 5. Test plan

- **Unit**: `evaluate(check, result)` truth table; `Recipe.target_for`; `detect`
  regex matching; device probe mapping.
- **Integration**: agent loop against a **fake `CommandRunner`** scripted to fail then
  succeed after a known fix (proves TSG recovery + evidence gate).
- **Schema**: every recipe validates against the models (`test_recipes_schema.py` ✅).
- **API**: registry endpoints (`test_health.py`, `test_recipes.py` ✅).
- **Edge cases**: no matching target; verify fails after steps "succeed"; elevated step
  without confirmation; offline/no-sudo constraints; infinite-fix-loop guard.

## 6. Open questions

- [ ] LLM provider abstraction — local vs hosted; how to keep runs reproducible?
- [ ] Recipe versioning & deprecation policy; pinning product versions.
- [ ] Trust/curation model — who approves recipes; signing run reports.
- [ ] Windows execution semantics (PowerShell vs cmd) for `shell`.
