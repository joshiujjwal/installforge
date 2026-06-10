import type { RecipeSummary } from "./types";

const DEFAULT_BASE = import.meta.env.VITE_REGISTRY_URL ?? "http://localhost:8000";

export async function fetchRecipes(baseUrl: string = DEFAULT_BASE): Promise<RecipeSummary[]> {
  const res = await fetch(`${baseUrl}/recipes`);
  if (!res.ok) {
    throw new Error(`registry returned ${res.status}`);
  }
  const body = (await res.json()) as { recipes: RecipeSummary[] };
  return body.recipes;
}
