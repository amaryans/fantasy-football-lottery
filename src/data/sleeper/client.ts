import type { SleeperBracketMatchup, SleeperLeague, SleeperRoster, SleeperUser } from './types.ts'

const API_BASE = 'https://api.sleeper.app/v1'
const CDN_AVATAR_BASE = 'https://sleepercdn.com/avatars/thumbs'

export type SleeperApiErrorKind = 'notFound' | 'network' | 'badResponse'

export class SleeperApiError extends Error {
  readonly kind: SleeperApiErrorKind

  constructor(kind: SleeperApiErrorKind, message: string) {
    super(message)
    this.name = 'SleeperApiError'
    this.kind = kind
  }
}

/** Everything needed to import a league, fetched together. */
export interface SleeperLeagueBundle {
  league: SleeperLeague
  rosters: SleeperRoster[]
  users: SleeperUser[]
  /** Null when the bracket fetch fails or playoffs haven't happened. */
  winnersBracket: SleeperBracketMatchup[] | null
}

async function fetchJson<T>(path: string, notFoundMessage: string): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${API_BASE}${path}`)
  } catch {
    throw new SleeperApiError('network', 'Could not reach Sleeper — check your internet connection')
  }
  if (response.status === 404) {
    throw new SleeperApiError('notFound', notFoundMessage)
  }
  if (!response.ok) {
    throw new SleeperApiError('badResponse', `Sleeper returned an error (HTTP ${response.status})`)
  }
  const body = (await response.json()) as T
  // Sleeper returns literal null with a 200 for some unknown resources.
  if (body === null) {
    throw new SleeperApiError('notFound', notFoundMessage)
  }
  return body
}

export function getLeague(leagueId: string): Promise<SleeperLeague> {
  validateLeagueId(leagueId)
  return fetchJson<SleeperLeague>(
    `/league/${leagueId.trim()}`,
    'League not found — double-check the league ID',
  )
}

/** Fetch league, rosters, and users together; the bracket is best-effort. */
export async function getLeagueBundle(leagueId: string): Promise<SleeperLeagueBundle> {
  validateLeagueId(leagueId)
  const id = leagueId.trim()
  const [league, rosters, users] = await Promise.all([
    getLeague(id),
    fetchJson<SleeperRoster[]>(`/league/${id}/rosters`, 'League rosters not found'),
    fetchJson<SleeperUser[]>(`/league/${id}/users`, 'League members not found'),
  ])
  const winnersBracket = await fetchJson<SleeperBracketMatchup[]>(
    `/league/${id}/winners_bracket`,
    'Bracket not found',
  ).catch(() => null)
  return { league, rosters, users, winnersBracket }
}

export function getUserByName(username: string): Promise<SleeperUser> {
  const trimmed = username.trim()
  if (trimmed.length === 0) {
    return Promise.reject(new SleeperApiError('notFound', 'Enter a Sleeper username'))
  }
  return fetchJson<SleeperUser>(
    `/user/${encodeURIComponent(trimmed)}`,
    `No Sleeper user named "${trimmed}"`,
  )
}

export function getUserLeagues(userId: string, season: string): Promise<SleeperLeague[]> {
  return fetchJson<SleeperLeague[]>(
    `/user/${encodeURIComponent(userId)}/leagues/nfl/${encodeURIComponent(season)}`,
    'No leagues found for that season',
  )
}

/** Build a CDN URL from a Sleeper avatar id. */
export function sleeperAvatarUrl(avatarId: string): string {
  return `${CDN_AVATAR_BASE}/${avatarId}`
}

function validateLeagueId(leagueId: string): void {
  if (!/^\d{5,}$/.test(leagueId.trim())) {
    throw new SleeperApiError(
      'notFound',
      'League IDs are long numbers — find yours in the Sleeper app under League > Settings',
    )
  }
}
