import { useAppStore } from '../state/store.ts'
import { makeSampleLeague } from '../data/sampleLeague.ts'
import SleeperImportForm from '../components/setup/SleeperImportForm.tsx'
import ManualLeagueForm from '../components/setup/ManualLeagueForm.tsx'
import Button from '../components/common/Button.tsx'

export default function SetupScreen() {
  const setLeague = useAppStore((state) => state.setLeague)
  const league = useAppStore((state) => state.league)
  const goToPhase = useAppStore((state) => state.goToPhase)

  return (
    <main className="flex min-h-screen flex-col items-center gap-10 bg-navy px-4 py-12 text-white">
      <header className="text-center">
        <h1 className="text-4xl font-bold sm:text-5xl">Fantasy Football Draft Lottery</h1>
        <p className="mt-3 max-w-xl text-lg text-white/70">
          Run a suspenseful NBA-style lottery for your league&apos;s draft order — right in the
          browser, nothing to install.
        </p>
      </header>

      {league && (
        <Button variant="secondary" onClick={() => goToPhase('review')}>
          Continue with {league.name} →
        </Button>
      )}

      <div className="grid w-full max-w-4xl gap-6 sm:grid-cols-2">
        <section className="flex flex-col gap-4 rounded-2xl border border-white/15 bg-white/5 p-6">
          <h2 className="text-2xl font-bold">Import from Sleeper</h2>
          <p className="text-sm text-white/60">
            Pull in your league&apos;s teams, records, and standings automatically.
          </p>
          <SleeperImportForm onImported={setLeague} />
        </section>

        <section className="flex flex-col gap-4 rounded-2xl border border-white/15 bg-white/5 p-6">
          <h2 className="text-2xl font-bold">Manual setup</h2>
          <p className="text-sm text-white/60">
            Not on Sleeper? Enter your owners and records by hand.
          </p>
          <ManualLeagueForm onCreated={setLeague} />
        </section>
      </div>

      <Button variant="ghost" onClick={() => setLeague(makeSampleLeague())}>
        Or try a sample league first →
      </Button>
    </main>
  )
}
