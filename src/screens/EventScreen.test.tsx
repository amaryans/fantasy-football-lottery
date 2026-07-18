import { act, fireEvent, render, screen } from '@testing-library/react'
import EventScreen from './EventScreen.tsx'
import { useAppStore } from '../state/store.ts'
import type { League, Team } from '../data/types.ts'

vi.mock('canvas-confetti', () => ({ default: vi.fn() }))
import confetti from 'canvas-confetti'

function makeTeam(id: string, wins: number): Team {
  return {
    id,
    ownerName: `owner-${id}`,
    teamName: `team-${id}`,
    wins,
    losses: 14 - wins,
    ties: 0,
    pointsFor: 1000 + wins,
    avatarUrl: null,
    playoffFinish: null,
  }
}

function makeLeague(): League {
  return {
    source: 'manual',
    name: 'Event Test League',
    teams: [makeTeam('a', 2), makeTeam('b', 7), makeTeam('c', 12)],
  }
}

function setupLottery(slotMode: 'winnerChoosesSlot' | 'lotteryIsOrder') {
  useAppStore.getState().setLeague(makeLeague())
  useAppStore.getState().updateSettings({ slotMode })
  useAppStore.getState().startLottery()
}

beforeEach(() => {
  localStorage.clear()
  useAppStore.getState().startOver()
  vi.clearAllMocks()
  // Only fake the setTimeout family: framer-motion relies on real
  // requestAnimationFrame/performance to make progress in jsdom.
  vi.useFakeTimers({ toFake: ['setTimeout', 'clearTimeout', 'setInterval', 'clearInterval'] })
})

afterEach(() => {
  vi.useRealTimers()
})

/** Click "next" and run the drumroll out. */
async function revealOnePick() {
  fireEvent.click(screen.getByRole('button', { name: /reveal the first pick|next pick/i }))
  await act(async () => {
    await vi.advanceTimersByTimeAsync(5000)
  })
}

describe('EventScreen', () => {
  test('reveals picks from last to first with the drumroll', async () => {
    setupLottery('lotteryIsOrder')
    render(<EventScreen />)

    const lastPickId = useAppStore.getState().result?.pickOrder[2] as string

    fireEvent.click(screen.getByRole('button', { name: /reveal the first pick/i }))
    expect(screen.getByRole('button', { name: /drawing/i })).toBeDisabled()

    await act(async () => {
      await vi.advanceTimersByTimeAsync(5000)
    })

    expect(useAppStore.getState().revealCursor).toBe(1)
    // The card mounts after AnimatePresence finishes the drumroll exit animation,
    // which runs on requestAnimationFrame — needs real timers to elapse.
    vi.useRealTimers()
    expect(await screen.findByTestId('revealed-card')).toHaveTextContent(`team-${lastPickId}`)
  })

  test('fires confetti only on the #1 pick', async () => {
    setupLottery('lotteryIsOrder')
    render(<EventScreen />)

    await revealOnePick()
    expect(confetti).not.toHaveBeenCalled()
    await revealOnePick()
    expect(confetti).not.toHaveBeenCalled()
    await revealOnePick()
    expect(confetti).toHaveBeenCalledTimes(1)
  })

  test('winnerChoosesSlot mode requires a slot pick before advancing', async () => {
    setupLottery('winnerChoosesSlot')
    render(<EventScreen />)

    await revealOnePick()

    // The next-pick button is blocked until the winner picks a slot.
    expect(screen.getByRole('button', { name: /next pick/i })).toBeDisabled()

    fireEvent.click(screen.getByRole('button', { name: /draft slot 3/i }))

    expect(useAppStore.getState().slotAssignments).toHaveLength(1)
    expect(screen.getByRole('button', { name: /next pick/i })).toBeEnabled()
  })

  test('completing all picks offers the results button', async () => {
    setupLottery('lotteryIsOrder')
    render(<EventScreen />)

    await revealOnePick()
    await revealOnePick()
    await revealOnePick()

    fireEvent.click(screen.getByRole('button', { name: /see the final draft order/i }))
    expect(useAppStore.getState().phase).toBe('results')
  })

  test('undo steps back a reveal', async () => {
    setupLottery('lotteryIsOrder')
    render(<EventScreen />)

    await revealOnePick()
    expect(useAppStore.getState().revealCursor).toBe(1)

    fireEvent.click(screen.getByRole('button', { name: /^undo$/i }))
    expect(useAppStore.getState().revealCursor).toBe(0)
  })

  test('recovers gracefully with no lottery', () => {
    render(<EventScreen />)
    expect(screen.getByText(/no lottery in progress/i)).toBeInTheDocument()
  })
})
