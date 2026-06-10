"""Load curated recipe metadata from the packages/recipes directory.

For the scaffold this does light parsing only. TODO (ADR 0002): depend on the shared
recipe models for full validation instead of raw dict access.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

# .../apps/registry/src/installforge_registry/loader.py -> repo root is parents[4]
REPO_ROOT = Path(__file__).resolve().parents[4]
RECIPES_DIR = REPO_ROOT / "packages" / "recipes"


def load_recipes(recipes_dir: Path = RECIPES_DIR) -> Dict[str, Dict[str, Any]]:
    recipes: Dict[str, Dict[str, Any]] = {}
    for path in sorted(recipes_dir.glob("*/recipe.yaml")):
        data = yaml.safe_load(path.read_text())
        recipes[data["id"]] = data
    return recipes


def list_recipe_summaries(recipes_dir: Path = RECIPES_DIR) -> List[Dict[str, Any]]:
    summaries: List[Dict[str, Any]] = []
    for rid, data in load_recipes(recipes_dir).items():
        summaries.append(
            {
                "id": rid,
                "product": data.get("product"),
                "description": data.get("description"),
                "categories": data.get("categories", []),
                "platforms": [t["platform"]["os"] for t in data.get("targets", [])],
            }
        )
    return summaries
