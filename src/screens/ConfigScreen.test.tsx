import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ConfigScreen from './ConfigScreen.tsx'
import { useAppStore } from '../state/store.ts'
import { oddsForLeagueSize } from '../engine/odds.ts'
import type { League, Team } from '../data/types.ts'

function makeTeam(id: string, wins: number, playoffFinish: number | null = null): Team {
  return {
    id,
    ownerName: `owner-${id}`,
    teamName: `team-${id}`,
    wins,
    losses: 14 - wins,
    ties: 0,
    pointsFor: 1000 + wins,
    avatarUrl: null,
    playoffFinish,
  }
}

function makeLeague(withPlayoffs: boolean): League {
  return {
    source: 'manual',
    name: 'Config Test League',
    teams: [
      makeTeam('worst', 2),
      makeTeam('mid', 7, withPlayoffs ? 2 : null),
      makeTeam('best', 12, withPlayoffs ? 1 : null),
    ],
  }
}

beforeEach(() => {
  localStorage.clear()
  useAppStore.getState().startOver()
})

describe('ConfigScreen', () => {
  test('displays odds that match oddsForLeagueSize exactly', () => {
    useAppStore.getState().setLeague(makeLeague(false))
    render(<ConfigScreen />)
    const expected = oddsForLeagueSize(3).map((bps) => `${(bps / 100).toFixed(1)}%`)
    for (const percentage of new Set(expected)) {
      const occurrences = expected.filter((p) => p === percentage).length
      expect(screen.getAllByText(percentage)).toHaveLength(occurrences)
    }
  })

  test('regular season ordering puts the worst team at seed 1', () => {
    useAppStore.getState().setLeague(makeLeague(false))
    render(<ConfigScreen />)
    const rows = screen.getAllByRole('row').slice(1) // skip header
    expect(rows[0]).toHaveTextContent('team-worst')
    expect(rows[2]).toHaveTextContent('team-best')
  })

  test('playoff option is disabled without playoff results', () => {
    useAppStore.getState().setLeague(makeLeague(false))
    render(<ConfigScreen />)
    expect(screen.getByRole('radio', { name: /playoff results/i })).toBeDisabled()
  })

  test('toggling to playoff ordering seeds the champion last', async () => {
    useAppStore.getState().setLeague(makeLeague(true))
    const user = userEvent.setup()
    render(<ConfigScreen />)

    await user.click(screen.getByRole('radio', { name: /playoff results/i }))

    const rows = screen.getAllByRole('row').slice(1)
    expect(rows[0]).toHaveTextContent('team-worst') // missed playoffs -> seed 1
    expect(rows[2]).toHaveTextContent('team-best') // champion -> last seed
    expect(useAppStore.getState().settings.orderingSource).toBe('playoffs')
  })

  test('start lottery runs the draw and enters the event phase', async () => {
    useAppStore.getState().setLeague(makeLeague(false))
    const user = userEvent.setup()
    render(<ConfigScreen />)

    await user.click(screen.getByRole('button', { name: /start the lottery/i }))

    const state = useAppStore.getState()
    expect(state.phase).toBe('event')
    expect(state.result?.pickOrder).toHaveLength(3)
  })
})
