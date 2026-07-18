/** Raw response shapes from the public Sleeper API (only the fields we consume). */

export interface SleeperLeague {
  league_id: string
  name: string
  /** Season year as a string, e.g. "2025". */
  season: string
  status: string
  avatar: string | null
  previous_league_id: string | null
  total_rosters: number
}

export interface SleeperRoster {
  roster_id: number
  /** Null when the owner left the league (orphan roster). */
  owner_id: string | null
  settings: {
    wins: number
    losses: number
    ties: number
    fpts: number
    fpts_decimal?: number
  }
}

export interface SleeperUser {
  user_id: string
  display_name: string
  /** Sleeper avatar id (not a URL), null if the user has none. */
  avatar: string | null
  metadata?: {
    team_name?: string | null
    /** Custom team avatar — a full URL when present. */
    avatar?: string | null
  } | null
}

export interface SleeperBracketMatchup {
  r: number
  m: number
  t1: number | null
  t2: number | null
  w: number | null
  l: number | null
  /** Placement game marker: winner finishes in place p, loser in place p+1. */
  p?: number
}
