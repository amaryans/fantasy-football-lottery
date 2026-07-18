import { useMemo, useRef, useState } from 'react'
import { finalDraftOrder, useAppStore } from '../state/store.ts'
import Button from '../components/common/Button.tsx'
import ResultsPoster, { type PosterEntry } from '../components/results/ResultsPoster.tsx'
import { copyPoster, downloadPoster, posterFilename } from '../utils/shareImage.ts'

export default function ResultsScreen() {
  const league = useAppStore((state) => state.league)
  const settings = useAppStore((state) => state.settings)
  const result = useAppStore((state) => state.result)
  const lotteryConfig = useAppStore((state) => state.lotteryConfig)
  const slotAssignments = useAppStore((state) => state.slotAssignments)
  const startLottery = useAppStore((state) => state.startLottery)
  const startOver = useAppStore((state) => state.startOver)

  const posterRef = useRef<HTMLDivElement>(null)
  const [shareStatus, setShareStatus] = useState<string | null>(null)

  const entries: PosterEntry[] = useMemo(() => {
    const order = finalDraftOrder({ result, slotAssignments, settings, league })
    if (!order || !lotteryConfig) {
      return []
    }
    const seedByTeamId = new Map(lotteryConfig.teams.map((entry) => [entry.id, entry.seed]))
    return order.map((team, index) => ({
      team,
      slot: index + 1,
      seed: seedByTeamId.get(team.id) ?? 0,
    }))
  }, [result, slotAssignments, settings, league, lotteryConfig])

  if (!league || !result || entries.length === 0) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-navy text-white">
        <p>No completed lottery to show.</p>
        <Button onClick={startOver}>Back to setup</Button>
      </main>
    )
  }

  async function handleDownload() {
    if (!posterRef.current || !league) {
      return
    }
    try {
      await downloadPoster(posterRef.current, posterFilename(league.name))
      setShareStatus('Image downloaded ✓')
    } catch {
      setShareStatus('Could not generate the image — try a screenshot instead')
    }
  }

  async function handleCopy() {
    if (!posterRef.current) {
      return
    }
    const didCopy = await copyPoster(posterRef.current)
    setShareStatus(didCopy ? 'Copied to clipboard ✓' : 'Copying not supported in this browser')
  }

  function handleRerun() {
    const shouldRerun = window.confirm(
      'Run the lottery again with a brand-new draw? The current result will be replaced.',
    )
    if (shouldRerun) {
      startLottery()
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center gap-8 bg-navy px-4 py-10 text-white">
      <h1 className="text-3xl font-bold">🏆 Final draft order</h1>

      <ResultsPoster
        ref={posterRef}
        leagueName={league.name}
        season={league.season}
        entries={entries}
        lotterySeed={result.seedUsed}
      />

      <div className="flex flex-wrap items-center justify-center gap-3">
        <Button onClick={() => void handleDownload()}>Download image</Button>
        <Button variant="secondary" onClick={() => void handleCopy()}>
          Copy image
        </Button>
        <Button variant="ghost" onClick={handleRerun}>
          Run again
        </Button>
        <Button variant="ghost" onClick={startOver}>
          Start over
        </Button>
      </div>
      {shareStatus && (
        <p role="status" className="text-sm text-white/60">
          {shareStatus}
        </p>
      )}
    </main>
  )
}
