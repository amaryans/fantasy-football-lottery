import { mulberry32 } from './rng.ts'
import type { LotteryConfig, LotteryResult } from './types.ts'

const BPS_TOTAL = 10000

/**
 * Run the draft lottery: successive weighted draws without replacement over
 * each team's odds. Mathematically equivalent to the NBA's physical 4-ball
 * combination process, but exact at any league size.
 *
 * Every pick 1..N is drawn by lottery. Deterministic for a given (config, seed):
 * replaying with the same inputs reproduces the identical pick order.
 */
export function runLottery(config: LotteryConfig, seed: number, timestamp: string): LotteryResult {
  validateConfig(config)
  const rng = mulberry32(seed)

  let remaining = config.teams.map((team, index) => ({
    id: team.id,
    weight: config.oddsBps[index] ?? 0,
  }))
  const pickOrder: string[] = []

  while (remaining.length > 0) {
    const totalWeight = remaining.reduce((sum, entry) => sum + entry.weight, 0)
    const roll = rng() * totalWeight

    let cumulative = 0
    let winnerIndex = remaining.length - 1 // guards against float edge where roll === totalWeight
    for (const [i, entry] of remaining.entries()) {
      cumulative += entry.weight
      if (roll < cumulative) {
        winnerIndex = i
        break
      }
    }

    const winner = remaining[winnerIndex]
    if (winner === undefined) {
      throw new Error('Lottery draw failed to select a winner') // unreachable
    }
    pickOrder.push(winner.id)
    remaining = remaining.filter((_, i) => i !== winnerIndex)
  }

  return { seedUsed: seed, pickOrder, timestamp }
}

/** Re-run a past lottery from its stored seed — lets anyone verify a result. */
export function replayLottery(config: LotteryConfig, result: LotteryResult): boolean {
  const replayed = runLottery(config, result.seedUsed, result.timestamp)
  return (
    replayed.pickOrder.length === result.pickOrder.length &&
    replayed.pickOrder.every((id, i) => id === result.pickOrder[i])
  )
}

function validateConfig(config: LotteryConfig): void {
  const { teams, oddsBps } = config
  if (teams.length === 0) {
    throw new Error('Lottery config must contain at least one team')
  }
  if (teams.length !== oddsBps.length) {
    throw new Error(`Team count (${teams.length}) must match odds count (${oddsBps.length})`)
  }
  if (oddsBps.some((bps) => !Number.isInteger(bps) || bps <= 0)) {
    throw new Error('All odds must be positive integers (basis points)')
  }
  const total = oddsBps.reduce((sum, bps) => sum + bps, 0)
  if (total !== BPS_TOTAL) {
    throw new Error(`Odds must sum to exactly ${BPS_TOTAL} bps, got ${total}`)
  }
  const ids = new Set(teams.map((team) => team.id))
  if (ids.size !== teams.length) {
    throw new Error('Team ids must be unique')
  }
}
