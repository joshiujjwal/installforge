"""Validate every curated recipe against the domain models (Phase 0 evidence gate)."""
from __future__ import annotations

from pathlib import Path
from typing import List

import pytest
import yaml

from installforge_agent.models import Recipe

REPO_ROOT = Path(__file__).resolve().parents[3]
RECIPES_DIR = REPO_ROOT / "packages" / "recipes"


def _recipe_files() -> List[Path]:
    return sorted(RECIPES_DIR.glob("*/recipe.yaml"))


def test_recipes_exist() -> None:
    assert _recipe_files(), f"no recipes found under {RECIPES_DIR}"


@pytest.mark.parametrize("recipe_path", _recipe_files(), ids=lambda p: p.parent.name)
def test_recipe_matches_schema(recipe_path: Path) -> None:
    data = yaml.safe_load(recipe_path.read_text())
    recipe = Recipe.model_validate(data)

    assert recipe.id == recipe_path.parent.name, "folder name must equal recipe id"
    for target in recipe.targets:
        assert target.steps, f"{recipe.id}:{target.platform.os} has no steps"
        assert target.verify, f"{recipe.id}:{target.platform.os} has no verify (evidence gate)"


def test_flutter_macos_target_carries_tsg() -> None:
    data = yaml.safe_load((RECIPES_DIR / "flutter" / "recipe.yaml").read_text())
    recipe = Recipe.model_validate(data)

    target = recipe.target_for("macos", "arm64")
    assert target is not None
    assert any("cocoapods" in ki.id for ki in target.known_issues)
