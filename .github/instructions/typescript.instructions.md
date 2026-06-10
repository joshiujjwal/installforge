---
applyTo: "apps/web/**/*.{ts,tsx}"
---

# TypeScript / React instructions

- TypeScript **strict** mode. Prefer `const`; never `var`. Use `async/await`.
- **Named exports** only (no default exports). Use early returns to reduce nesting.
- Keep domain types in `src/types.ts`, mirrored from `packages/schemas`.
- Network access goes through `src/api.ts`; handle non-OK responses by throwing `Error`.
- Components are function components; keep side effects in `useEffect`.
- Test with **Vitest** + Testing Library; query by role/text, not test ids.
- Red/green TDD: write the failing test first; never remove tests.
- Lint with ESLint (flat config), format with Prettier (`printWidth: 100`).
