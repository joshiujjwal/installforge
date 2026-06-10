---
applyTo: "packages/recipes/**/*.yaml"
---

# Recipe authoring instructions

A recipe is curated, runnable install knowledge. It must validate against
`packages/schemas/recipe.schema.json`.

- The folder name **must equal** the recipe `id` (kebab-case).
- Provide at least one `target`; every target needs **`steps`** and **`verify`**.
- `verify` is the **evidence gate**: commands that prove the install works on-device
  (e.g. `flutter --version` with `expect_stdout_contains`). Never ship a target without it.
- Encode real-world failures as `known_issues` (TSG): `symptom → detect → cause → fix`,
  with a `source` URL and a `confidence` rating.
- Mark `elevated: true` on any step needing sudo/admin. Prefer `idempotent` commands.
- Keep commands portable for the declared `platform`; don't assume a package manager that
  isn't a `prerequisite`.
- After editing, run `pytest` in `apps/agent` — `test_recipes_schema.py` validates recipes.
