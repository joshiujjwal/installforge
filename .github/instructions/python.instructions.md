---
applyTo: "apps/agent/**/*.py,apps/registry/**/*.py"
---

# Python instructions

- Target **Python ≥3.9**. Start modules with `from __future__ import annotations`.
- Use `typing.Optional`, `typing.List`, `typing.Dict` — **not** `X | None` / `list[str]`
  in runtime-evaluated positions (Pydantic resolves annotations on 3.9).
- Pydantic v2 models subclass a base with `model_config = ConfigDict(extra="forbid")`.
- Keep `installforge_agent/__init__.py` free of heavy imports (no typer/httpx at import).
- Lint/format with **ruff** (`E,F,I,B`), type-check with **mypy --strict**.
- Tests use **pytest** with `pythonpath = ["src"]`; name tests `test_<behavior>_when_<cond>`.
- Write the failing test first (red), then implement (green). Never delete tests.
- Resolve paths from the repo root via `Path(__file__).resolve().parents[N]`.
