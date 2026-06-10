"""InstallForge recipe registry API (FastAPI)."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import FastAPI, HTTPException

from .loader import list_recipe_summaries, load_recipes

app = FastAPI(title="InstallForge Registry", version="0.0.1")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/recipes")
def get_recipes() -> Dict[str, Any]:
    return {"recipes": list_recipe_summaries()}


@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: str) -> Dict[str, Any]:
    recipes = load_recipes()
    if recipe_id not in recipes:
        raise HTTPException(status_code=404, detail=f"recipe '{recipe_id}' not found")
    return recipes[recipe_id]
