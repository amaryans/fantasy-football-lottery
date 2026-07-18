import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import confetti from 'canvas-confetti'
import { revealedTeamIds, useAppStore } from '../state/store.ts'
import type { Team } from '../data/types.ts'
import Button from '../components/common/Button.tsx'
import DraftBoard, { type BoardSlot } from '../components/event/DraftBoard.tsx'
import StandingsRail from '../components/event/StandingsRail.tsx'
import RevealCard, { type RevealStage } from '../components/event/RevealCard.tsx'
import SlotPicker from '../components/event/SlotPicker.tsx'

const DRUMROLL_MS = 2500
/** The last three picks get a longer, more agonizing drumroll. */
const FINALE_DRUMROLL_MS = 4200
const FINALE_PICKS = 3

export default function EventScreen() {
  const league = useAppStore((state) => state.league)
  const lotteryConfig = useAppStore((state) => state.lotteryConfig)
  const result = useAppStore((state) => state.result)
  const settings = useAppStore((state) => state.settings)
  const revealCursor = useAppStore((state) => state.revealCursor)
  const slotAssignments = useAppStore((state) => state.slotAssignments)
  const revealNext = useAppStore((state) => state.revealNext)
  const undoReveal = useAppStore((state) => state.undoReveal)
  const assignSlot = useAppStore((state) => state.assignSlot)
  const finishEvent = useAppStore((state) => state.finishEvent)
  const startOver = useAppStore((state) => state.startOver)

  const [stage, setStage] = useState<RevealStage>(revealCursor > 0 ? 'revealed' : 'idle')
  const drumrollTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  const teamsById = useMemo(
    () => new Map((league?.teams ?? []).map((team) => [team.id, team])),
    [league],
  )
  const seededTeams = useMemo(
    () =>
      (lotteryConfig?.teams ?? [])
        .map((entry) => teamsById.get(entry.id))
        .filter((team): team is Team => team !== undefined),
    [lotteryConfig, teamsById],
  )

  const totalPicks = result?.pickOrder.length ?? 0
  const revealedIds = useMemo(
    () => revealedTeamIds({ result, revealCursor }),
    [result, revealCursor],
  )
  const revealedIdSet = useMemo(() => new Set(revealedIds), [revealedIds])
  const lastRevealedTeam =
    revealedIds.length > 0
      ? (teamsById.get(revealedIds[revealedIds.length - 1] as string) ?? null)
      : null
  /** Pick number currently on the card (after reveal) or about to be drawn. */
  const currentPickNumber =
    stage === 'revealed' ? totalPicks - revealCursor + 1 : totalPicks - revealCursor
  const candidates = seededTeams.filter((team) => !revealedIdSet.has(team.id))

  const isChooseMode = settings.slotMode === 'winnerChoosesSlot'
  const takenSlots = useMemo(
    () => new Set(slotAssignments.map((assignment) => assignment.slot)),
    [slotAssignments],
  )
  const needsSlotChoice =
    isChooseMode &&
    stage === 'revealed' &&
    lastRevealedTeam !== null &&
    !slotAssignments.some((assignment) => assignment.teamId === lastRevealedTeam.id)

  const allRevealed = revealCursor === totalPicks && totalPicks > 0
  const isEventComplete = allRevealed && (!isChooseMode || slotAssignments.length === totalPicks)
  const canAdvance = stage !== 'drumroll' && !needsSlotChoice && !allRevealed

  const boardSlots: BoardSlot[] = useMemo(() => {
    return Array.from({ length: totalPicks }, (_, i) => {
      const slot = i + 1
      if (isChooseMode) {
        const assignment = slotAssignments.find((entry) => entry.slot === slot)
        return { slot, team: assignment ? (teamsById.get(assignment.teamId) ?? null) : null }
      }
      // Lottery order = draft order: pick k is revealed once revealCursor >= totalPicks - k + 1.
      const isRevealed = revealCursor >= totalPicks - slot + 1
      const teamId = result?.pickOrder[i]
      return { slot, team: isRevealed && teamId ? (teamsById.get(teamId) ?? null) : null }
    })
  }, [totalPicks, isChooseMode, slotAssignments, revealCursor, result, teamsById])

  const advance = useCallback(() => {
    if (!canAdvance) {
      return
    }
    const upcomingPickNumber = totalPicks - revealCursor
    setStage('drumroll')
    const duration = upcomingPickNumber <= FINALE_PICKS ? FINALE_DRUMROLL_MS : DRUMROLL_MS
    drumrollTimer.current = setTimeout(() => {
      revealNext()
      setStage('revealed')
      if (upcomingPickNumber === 1) {
        void confetti({ particleCount: 250, spread: 110, origin: { y: 0.6 } })
      }
    }, duration)
  }, [canAdvance, totalPicks, revealCursor, revealNext])

  const undo = useCallback(() => {
    if (stage === 'drumroll') {
      if (drumrollTimer.current) {
        clearTimeout(drumrollTimer.current)
      }
      setStage('idle')
      return
    }
    if (revealCursor > 0) {
      undoReveal()
      setStage('idle')
    }
  }, [stage, revealCursor, undoReveal])

  useEffect(
    () => () => {
      if (drumrollTimer.current) {
        clearTimeout(drumrollTimer.current)
      }
    },
    [],
  )

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (event.code === 'Space') {
        event.preventDefault()
        advance()
      } else if (event.key.toLowerCase() === 'u') {
        undo()
      }
    }
    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [advance, undo])

  if (!league || !result || !lotteryConfig) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center gap-4 bg-navy text-white">
        <p>No lottery in progress.</p>
        <Button onClick={startOver}>Back to setup</Button>
      </main>
    )
  }

  return (
    <main className="flex min-h-screen flex-col gap-4 bg-navy px-4 py-4 text-white lg:px-8">
      <header className="flex items-center justify-between gap-4">
        <h1 className="truncate text-xl font-bold text-white/80 sm:text-2xl">{league.name}</h1>
        <Button
          variant="ghost"
          onClick={() => void document.documentElement.requestFullscreen?.().catch(() => undefined)}
        >
          ⛶ Fullscreen
        </Button>
      </header>

      <DraftBoard slots={boardSlots} />

      <div className="grid flex-1 gap-6 lg:grid-cols-[280px_1fr_auto]">
        <aside className="hidden lg:block">
          <StandingsRail
            seededTeams={seededTeams}
            oddsBps={lotteryConfig.oddsBps}
            revealedIds={revealedIdSet}
          />
        </aside>

        <section className="flex flex-col items-center justify-center gap-6">
          <RevealCard
            stage={stage}
            candidates={candidates}
            revealedTeam={lastRevealedTeam}
            pickNumber={Math.max(currentPickNumber, 1)}
          />

          <div className="flex items-center gap-3">
            {isEventComplete ? (
              <Button className="px-8 py-3 text-lg" onClick={finishEvent}>
                See the final draft order →
              </Button>
            ) : (
              <>
                <Button className="px-8 py-3 text-lg" disabled={!canAdvance} onClick={advance}>
                  {stage === 'drumroll'
                    ? 'Drawing…'
                    : revealCursor === 0
                      ? 'Reveal the first pick'
                      : 'Next pick'}
                </Button>
                <Button
                  variant="ghost"
                  disabled={revealCursor === 0 && stage !== 'drumroll'}
                  onClick={undo}
                >
                  Undo
                </Button>
              </>
            )}
          </div>
          <p className="text-xs text-white/40">Space = next · U = undo</p>
        </section>

        <aside className="flex items-center justify-center lg:w-72">
          {needsSlotChoice && lastRevealedTeam && (
            <SlotPicker
              team={lastRevealedTeam}
              totalSlots={totalPicks}
              takenSlots={takenSlots}
              onPick={(slot) => assignSlot(lastRevealedTeam.id, slot)}
            />
          )}
        </aside>
      </div>
    </main>
  )
}
