# Fantasy Football Draft Lottery 🏈

A zero-install web app that runs a suspenseful, NBA-style draft lottery for your fantasy football
league. Import your league from Sleeper (or enter it by hand), put it on the draft-night TV, and
reveal the picks one agonizing card flip at a time.

**Live app:** https://amaryans.github.io/fantasy-football-lottery/

## How it works

1. **Import your league** — paste a Sleeper league ID (or search by username), or enter owners and
   records manually. A bundled sample league lets you try everything instantly.
2. **Review and configure** — correct any team info, then choose how seeds are ordered (regular
   season standings or playoff results) and how draft slots are claimed (winners pick their slot,
   or lottery order = draft order).
3. **Run the event** — worst pick first, with a drumroll, card-flip reveals, an extended finale for
   the last three picks, and confetti for #1 overall. Keyboard-driven (Space = next, U = undo) so
   the commissioner isn't fumbling with a mouse on the projector.
4. **Share the results** — download or copy a results poster image for the league group chat.

## Fairness

- Odds follow the **NBA lottery table** (14%, 14%, 14%, 12.5%, …), adapted exactly to any league
  size from 2 to 16 teams. The worst team always gets the best odds.
- Every result records its random **seed**, shown on the results poster — anyone can replay the
  lottery with the same seed and get the identical order (`replayLottery` in
  [src/engine/lottery.ts](src/engine/lottery.ts)).
- The engine is validated by Monte Carlo tests (100k seeded trials per league size, 4σ bounds)
  plus an exact closed-form check — see [src/engine](src/engine).

Everything runs client-side: no accounts, no server, and your league data never leaves the
browser (state is kept in localStorage, so a mid-event page reload resumes exactly where you were).

## Development

```bash
npm install
npm run dev        # local dev server
npm test           # engine + UI test suite
npm run lint       # eslint
npm run typecheck  # tsc
npm run build      # production bundle in dist/
```

Stack: Vite, React 18 + TypeScript (strict), Tailwind CSS, Zustand, framer-motion, Vitest.

### Architecture

- `src/engine/` — pure, seedable lottery engine (no React, no network). NBA odds adaptation +
  weighted draws without replacement.
- `src/data/` — Sleeper API client, league mapping (records, avatars, playoff placements from the
  bracket), and seed-ordering logic. Fixture-tested against real API responses.
- `src/state/` — a single Zustand store: `setup → review → config → event → results` phase
  machine, persisted to localStorage.
- `src/screens/` + `src/components/` — one screen per phase; the event screen is the centerpiece.

### Deployment

CI ([.github/workflows/ci.yml](.github/workflows/ci.yml)) lints, typechecks, tests, and builds on
every PR; pushes to `main` deploy to GitHub Pages automatically. One-time repo setup: Settings →
Pages → Source: **GitHub Actions**.

## Legacy

The original PyQt5 desktop version of this app lives untouched in [legacy/](legacy/).
