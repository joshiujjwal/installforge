from fastapi.testclient import TestClient

from installforge_registry.main import app

client = TestClient(app)


def test_lists_curated_recipes() -> None:
    resp = client.get("/recipes")
    assert resp.status_code == 200
    ids = {r["id"] for r in resp.json()["recipes"]}
    assert {"flutter", "gimp"} <= ids


def test_get_known_recipe() -> None:
    resp = client.get("/recipes/flutter")
    assert resp.status_code == 200
    assert resp.json()["product"] == "Flutter SDK"


def test_unknown_recipe_returns_404() -> None:
    resp = client.get("/recipes/does-not-exist")
    assert resp.status_code == 404
