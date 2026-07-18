import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import NavBar from './NavBar.tsx'
import { useAppStore } from '../../state/store.ts'
import type { League, Team } from '../../data/types.ts'

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
    name: 'Nav Test League',
    teams: [makeTeam('a', 2), makeTeam('b', 7), makeTeam('c', 12)],
  }
}

beforeEach(() => {
  localStorage.clear()
  useAppStore.getState().startOver()
})

describe('NavBar', () => {
  test('lottery links are disabled until a league is loaded', () => {
    render(<NavBar />)
    expect(screen.getByRole('button', { name: /home/i })).toBeEnabled()
    expect(screen.getByRole('button', { name: /settings/i })).toBeDisabled()
    expect(screen.getByRole('button', { name: /simulation test/i })).toBeDisabled()
    expect(screen.getByRole('button', { name: /lottery board/i })).toBeDisabled()
  })

  test('settings and simulation unlock with a league; board needs a result', async () => {
    useAppStore.getState().setLeague(makeLeague())
    const user = userEvent.setup()
    render(<NavBar />)

    expect(screen.getByRole('button', { name: /lottery board/i })).toBeDisabled()

    await user.click(screen.getByRole('button', { name: /simulation test/i }))
    expect(useAppStore.getState().phase).toBe('simulation')

    await user.click(screen.getByRole('button', { name: /settings/i }))
    expect(useAppStore.getState().phase).toBe('config')

    act(() => useAppStore.getState().startLottery())
    expect(screen.getByRole('button', { name: /lottery board/i })).toBeEnabled()
  })

  test('home returns to the setup screen', async () => {
    useAppStore.getState().setLeague(makeLeague())
    const user = userEvent.setup()
    render(<NavBar />)
    await user.click(screen.getByRole('button', { name: /home/i }))
    expect(useAppStore.getState().phase).toBe('setup')
  })
})
