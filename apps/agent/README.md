# installforge-agent

The device-side skill agent. Resolves a recipe for a product + device, runs the
install steps, recovers from failures using curated known-issues (TSG) or an LLM
fallback, and runs `verify` checks as an evidence gate.

## Layout

| Path | Purpose |
|---|---|
| `src/installforge_agent/models.py` | Domain models (Recipe, DeviceConfig, RunReport). |
| `src/installforge_agent/device.py` | Probe the current device into a DeviceConfig. |
| `src/installforge_agent/loop.py` | The install + verify agent loop (skeleton). |
| `src/installforge_agent/cli.py` | `installforge` Typer CLI. |
| `tests/` | Pytest suite. |

## Develop

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest            # run tests (red/green TDD)
ruff check . && mypy .
installforge probe   # try the CLI
```
