# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fantasy Football Draft Lottery is a client-side React/TypeScript web app that runs an NBA-style
weighted draft lottery for fantasy football leagues. Leagues import from the public Sleeper API
(no key, CORS-enabled) or are entered manually; the lottery is revealed pick-by-pick with
animations on draft night; results export as a shareable PNG. Deployed to GitHub Pages — there is
no backend, and all state lives in localStorage.

The original PyQt5 desktop app is preserved in `legacy/` (reference only — do not modify).

## Commands

```bash
npm run dev        # Vite dev server (base path /fantasy-football-lottery/)
npm test           # Vitest run (engine Monte Carlo + RTL screen tests)
npm run lint       # ESLint flat config (includes purity boundary rules)
npm run typecheck  # tsc -b --noEmit (strict)
npm run build      # tsc + vite build -> dist/
npx prettier --write src   # format
```

## Architecture

**Phase flow:** `setup → review → config → event → results`, driven by the `phase` field in the
Zustand store (src/state/store.ts) — no router. `App.tsx` switches screens on it. The store
persists to localStorage key `ffl.v1` (crash recovery mid-event).

**Module boundaries (enforced by ESLint no-restricted-imports):**

- `src/engine/` — PURE: no React, no fetch, no `Math.random`/`Date.now`. Seedable mulberry32 RNG;
  `oddsForLeagueSize()` adapts the NBA odds table (basis points, largest-remainder rounding) to
  2–16 teams; `runLottery(config, seed, timestamp)` does weighted draws without replacement;
  `replayLottery` verifies stored results.
- `src/data/` — framework-free. `sleeper/client.ts` (typed fetch wrappers, `SleeperApiError`),
  `sleeper/mapping.ts` (rosters+users join, playoff placements from bracket `p` games),
  `ordering.ts` (`computeLotterySeeds`: regular-season or playoff ordering, worst first).
- `src/screens/` + `src/components/` — UI. The event screen owns the reveal state machine
  (idle → drumroll → revealed); reveals run worst pick → #1 pick.

**Key invariants:**

- Odds basis points always sum to exactly 10000; team count 2–16.
- The lottery result is computed up-front at "Start Lottery" (crypto-random seed); the event
  screen is pure theater over a fixed result.
- Store updates are immutable; the engine never mutates inputs.

## Testing

- Engine: determinism, validation, Monte Carlo (seeded trials, 4σ binomial bounds — deterministic,
  not flaky), exact 3-team closed-form distribution.
- Data: fixture tests using real captured Sleeper responses (`src/data/sleeper/__fixtures__/`).
- Screens: RTL with mocked Sleeper client / confetti / image export. EventScreen tests fake only
  the `setTimeout` family — framer-motion needs real rAF in jsdom.

## Deployment

`.github/workflows/ci.yml`: lint → format:check → typecheck → test → build on PRs; pushes to
`main` deploy `dist/` to GitHub Pages. `vite.config.ts` sets `base: '/fantasy-football-lottery/'`.
