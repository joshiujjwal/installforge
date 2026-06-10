---
name: add-recipe
description: >-
  Author a new curated InstallForge recipe (packages/recipes/<id>/recipe.yaml) for a
  product on one or more platforms, including verification checks and curated
  troubleshooting (known issues / TSG). Use when asked to add or curate an installer.
---

# Skill: Add a Recipe

Goal: produce a schema-valid, **verifiable** recipe with real troubleshooting knowledge.

## Steps

1. **Identify** the product `id` (kebab-case) and the target platforms (os/arch).
2. **Research** the official install docs and the most common failure modes (issue
   trackers, forums). Capture `source` URLs.
3. **Scaffold** `packages/recipes/<id>/recipe.yaml`. Folder name must equal `id`.
4. For each `target` define:
   - `prerequisites` (with `install_recipe` refs where another recipe can satisfy them),
   - ordered `steps` (set `elevated: true` for sudo; prefer idempotent commands),
   - `verify` checks — the **evidence gate** that proves it works,
   - `known_issues`: `symptom → detect (stdout/stderr regex or exit_code) → cause → fix`.
5. **Validate**: run `pytest` in `apps/agent`; `test_recipes_schema.py` must pass.
6. Add a short `notes.md` with human context and a sources table (optional but encouraged).

## Definition of done

- [ ] Recipe validates against `packages/schemas/recipe.schema.json`.
- [ ] Every target has at least one `verify` check.
- [ ] At least one real, sourced `known_issue`.
- [ ] `apps/agent` tests pass.

## Reference

- Schema: `packages/schemas/recipe.schema.json`
- Examples: `packages/recipes/flutter/recipe.yaml`, `packages/recipes/gimp/recipe.yaml`
