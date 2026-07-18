import { useMemo } from 'react'
import { useAppStore } from '../state/store.ts'
import { computeLotterySeeds, hasPlayoffResults } from '../data/ordering.ts'
import { MAX_TEAMS, MIN_TEAMS, oddsForLeagueSize } from '../engine/odds.ts'
import type { OrderingSource, SlotMode } from '../data/types.ts'
import Button from '../components/common/Button.tsx'
import ErrorBanner from '../components/common/ErrorBanner.tsx'
import OddsTable from '../components/config/OddsTable.tsx'

const ORDERING_OPTIONS: { value: OrderingSource; label: string; description: string }[] = [
  {
    value: 'regularSeason',
    label: 'Regular season standings',
    description: 'Worst record gets the best odds.',
  },
  {
    value: 'playoffs',
    label: 'Playoff results',
    description: 'Final placements set the order — the champion always seeds last.',
  },
]

const SLOT_OPTIONS: { value: SlotMode; label: string; description: string }[] = [
  {
    value: 'winnerChoosesSlot',
    label: 'Winners pick their slot',
    description: 'Each revealed winner chooses any open draft position.',
  },
  {
    value: 'lotteryIsOrder',
    label: 'Lottery order is the draft order',
    description: 'The #1 lottery winner drafts first, and so on.',
  },
]

export default function ConfigScreen() {
  const league = useAppStore((state) => state.league)
  const settings = useAppStore((state) => state.settings)
  const updateSettings = useAppStore((state) => state.updateSettings)
  const goToPhase = useAppStore((state) => state.goToPhase)
  const startLottery = useAppStore((state) => state.startLottery)
  const startOver = useAppStore((state) => state.startOver)

  const teams = useMemo(() => league?.teams ?? [], [league])
  const playoffsAvailable = hasPlayoffResults(teams)
  const teamCount = teams.length
  const isSupportedSize = teamCount >= MIN_TEAMS && teamCount <= MAX_TEAMS

  const seededTeams = useMemo(() => {
    if (teams.length === 0 || !isSupportedSize) {
      return []
    }
    const source =
      settings.orderingSource === 'playoffs' && !playoffsAvailable
        ? 'regularSeason'
        : settings.orderingSource
    return computeLotterySeeds(teams, source)
  }, [teams, settings.orderingSource, playoffsAvailable, isSupportedSize])

  const oddsBps = useMemo(
    () => (isSupportedSize ? oddsForLeagueSize(teamCount) : []),
    [teamCount, isSupportedSize],
  )

  if (!league) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-navy text-white">
        <p>No league loaded yet.</p>
        <Button onClick={startOver}>Back to setup</Button>
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center gap-8 bg-navy px-4 py-10 text-white">
      <header className="w-full max-w-5xl">
        <h1 className="text-3xl font-bold">Lottery settings</h1>
        <p className="mt-1 text-white/60">{league.name}</p>
      </header>

      <div className="grid w-full max-w-5xl gap-6 lg:grid-cols-[minmax(280px,1fr)_2fr]">
        <div className="flex flex-col gap-6">
          <fieldset className="rounded-2xl border border-white/15 bg-white/5 p-5">
            <legend className="px-1 text-sm font-semibold text-white/80">Lottery order from</legend>
            <div className="flex flex-col gap-3">
              {ORDERING_OPTIONS.map((option) => {
                const isDisabled = option.value === 'playoffs' && !playoffsAvailable
                return (
                  <label
                    key={option.value}
                    className={`flex cursor-pointer items-start gap-3 rounded-lg p-2 hover:bg-white/5 ${isDisabled ? 'cursor-not-allowed opacity-40' : ''}`}
                  >
                    <input
                      type="radio"
                      name="orderingSource"
                      className="mt-1 accent-accent"
                      checked={settings.orderingSource === option.value}
                      disabled={isDisabled}
                      onChange={() => updateSettings({ orderingSource: option.value })}
                    />
                    <span>
                      <span className="font-medium">{option.label}</span>
                      <span className="block text-sm text-white/60">
                        {isDisabled
                          ? 'Unavailable — no playoff results found for this league.'
                          : option.description}
                      </span>
                    </span>
                  </label>
                )
              })}
            </div>
          </fieldset>

          <fieldset className="rounded-2xl border border-white/15 bg-white/5 p-5">
            <legend className="px-1 text-sm font-semibold text-white/80">Draft slots</legend>
            <div className="flex flex-col gap-3">
              {SLOT_OPTIONS.map((option) => (
                <label
                  key={option.value}
                  className="flex cursor-pointer items-start gap-3 rounded-lg p-2 hover:bg-white/5"
                >
                  <input
                    type="radio"
                    name="slotMode"
                    className="mt-1 accent-accent"
                    checked={settings.slotMode === option.value}
                    onChange={() => updateSettings({ slotMode: option.value })}
                  />
                  <span>
                    <span className="font-medium">{option.label}</span>
                    <span className="block text-sm text-white/60">{option.description}</span>
                  </span>
                </label>
              ))}
            </div>
          </fieldset>
        </div>

        <section className="rounded-2xl border border-white/15 bg-white/5 p-5">
          <h2 className="mb-3 text-lg font-semibold">Odds preview</h2>
          {isSupportedSize ? (
            <OddsTable seededTeams={seededTeams} oddsBps={oddsBps} />
          ) : (
            <ErrorBanner
              message={`Leagues of ${teamCount} teams aren't supported — the lottery works for ${MIN_TEAMS} to ${MAX_TEAMS} teams.`}
            />
          )}
        </section>
      </div>

      <footer className="flex w-full max-w-5xl items-center justify-between">
        <Button variant="ghost" onClick={() => goToPhase('review')}>
          ← Back to review
        </Button>
        <Button
          className="px-8 py-3 text-lg"
          disabled={!isSupportedSize}
          onClick={() => startLottery()}
        >
          Start the lottery 🏈
        </Button>
      </footer>
    </main>
  )
}
