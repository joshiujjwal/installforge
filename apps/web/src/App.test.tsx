import { render, screen } from "@testing-library/react";
import { afterEach, expect, test, vi } from "vitest";
import { App } from "./App";

afterEach(() => {
  vi.restoreAllMocks();
});

test("renders the marketplace heading when the registry is empty", () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({ ok: true, json: async () => ({ recipes: [] }) }),
  );

  render(<App />);

  expect(screen.getByRole("heading", { name: /installforge/i })).toBeInTheDocument();
});
