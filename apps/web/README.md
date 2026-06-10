# @installforge/web

The marketplace UI. Browse curated recipes, see per-platform troubleshooting and
success rates, and copy the agent command to install on your device.

Stack: **Vite + React + TypeScript**, tested with **Vitest** + Testing Library.

## Develop

```bash
pnpm install          # from the repo root (pnpm workspace)
pnpm --filter @installforge/web dev        # http://localhost:5173
pnpm --filter @installforge/web test       # red/green TDD
pnpm --filter @installforge/web typecheck
pnpm --filter @installforge/web lint
```

Set `VITE_REGISTRY_URL` to point at the registry (default `http://localhost:8000`).

| Path | Purpose |
|---|---|
| `src/types.ts` | Types mirrored from `packages/schemas`. |
| `src/api.ts` | Typed registry client. |
| `src/App.tsx` | Marketplace listing. |
