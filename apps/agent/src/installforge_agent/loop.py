"""The InstallForge skill-agent loop.

Given a Recipe and a DeviceConfig, run install steps, recover from failures using
curated known-issues (TSG) or an LLM fallback, then run verification as an evidence
gate. This module defines the loop's shape and seams; the executor, TSG matcher, and
LLM diagnosis are TODO (see docs/spec.md "Agent loop").
"""
from __future__ import annotations

from typing import Optional, Protocol

from .models import Check, DeviceConfig, Recipe, RunReport, StepResult, Target

MAX_FIX_ATTEMPTS = 3


class CommandRunner(Protocol):
    """Execution seam so the loop can be unit-tested with fakes/dry-runs."""

    def run(
        self,
        command: str,
        *,
        shell: Optional[str] = None,
        timeout: Optional[int] = None,
        elevated: bool = False,
    ) -> StepResult: ...


def select_target(recipe: Recipe, device: DeviceConfig) -> Optional[Target]:
    """Pick the recipe target matching the device's os/arch."""
    return recipe.target_for(device.os, device.arch)


def evaluate(check: Check, result: StepResult) -> bool:
    """Compare a StepResult against a Check's expectations.

    TODO: implement exit-code, stdout-contains, and stdout-regex matching, then
    cover it with red/green tests in tests/test_loop.py.
    """
    raise NotImplementedError


def install(recipe: Recipe, device: DeviceConfig, runner: CommandRunner) -> RunReport:
    """Run the full install + verify loop.

    Skeleton flow:
      1. select_target(recipe, device)
      2. satisfy prerequisites (recurse into install_recipe where needed)
      3. for each step: run -> evaluate(expect); on failure match known_issues via
         Detect and apply fix steps (bounded by MAX_FIX_ATTEMPTS), else LLM-diagnose
      4. run verify checks (evidence gate) -> set RunReport.verified
      5. return RunReport with the full transcript
    """
    raise NotImplementedError
