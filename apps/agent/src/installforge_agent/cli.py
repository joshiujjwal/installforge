"""`installforge` device-side CLI — run the skill agent against the local device."""
from __future__ import annotations

import json

import typer

from .device import probe_device

app = typer.Typer(
    help="InstallForge — install and verify any product on this device.",
    no_args_is_help=True,
)


@app.command()
def probe() -> None:
    """Print a DeviceConfig snapshot of this machine as JSON."""
    typer.echo(json.dumps(probe_device().model_dump(), indent=2))


@app.command()
def install(
    product: str = typer.Argument(..., help="Recipe id, e.g. 'flutter'."),
    registry: str = typer.Option("http://localhost:8000", help="Registry base URL."),
    execute: bool = typer.Option(
        False, "--execute", help="Actually run steps (default: plan only)."
    ),
) -> None:
    """Resolve a recipe and run the install loop on this device.

    TODO: fetch the recipe from the registry, then call
    installforge_agent.loop.install with a real CommandRunner.
    """
    mode = "execute" if execute else "dry-run"
    typer.echo(f"[installforge] resolving '{product}' from {registry} ({mode})")
    typer.echo("not yet implemented — see docs/spec.md and TODO.md Phase 1")
    raise typer.Exit(code=0)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
