# Recipes

The curated content library of InstallForge. Each subdirectory is one product and
contains a `recipe.yaml` (machine-runnable) plus optional `notes.md` (human context).

```
recipes/
├── flutter/
│   ├── recipe.yaml
│   └── notes.md
└── gimp/
    └── recipe.yaml
```

## Recipe format

A recipe is validated against [`../schemas/recipe.schema.json`](../schemas/recipe.schema.json).
Key parts of every `target`:

- **prerequisites** — commands that must already succeed, optionally pointing at
  another `install_recipe` the agent can run first.
- **steps** — ordered install commands, each with an optional `expect` check.
- **verify** — the **evidence gate**: commands that prove the install works on the device.
- **known_issues** — curated troubleshooting (TSG): `symptom → detect → cause → fix`.

## Adding a recipe

Use the agent skill at [`.github/skills/add-recipe`](../../.github/skills/add-recipe/SKILL.md),
or by hand:

1. Create `recipes/<id>/recipe.yaml` (folder name **must** equal the `id`).
2. Cover at least one `target` with `steps` **and** `verify`.
3. Add real `known_issues` with `source` links where possible.
4. Run `pytest` in `apps/agent` — `test_recipes_schema.py` validates your recipe.
