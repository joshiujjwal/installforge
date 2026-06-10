import { useEffect, useState } from "react";
import { fetchRecipes } from "./api";
import type { RecipeSummary } from "./types";

export function App() {
  const [recipes, setRecipes] = useState<RecipeSummary[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchRecipes()
      .then(setRecipes)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : "failed to load"));
  }, []);

  return (
    <main>
      <h1>InstallForge</h1>
      <p>Install any product on any device — curated recipes, run by an agent.</p>
      {error !== null && <p role="alert">Could not reach registry: {error}</p>}
      <ul>
        {recipes.map((recipe) => (
          <li key={recipe.id}>
            <strong>{recipe.product}</strong> — {recipe.description}
          </li>
        ))}
      </ul>
    </main>
  );
}
