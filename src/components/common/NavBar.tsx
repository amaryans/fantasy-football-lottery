import { useAppStore, type AppPhase } from '../../state/store.ts'

interface NavItem {
  label: string
  phase: AppPhase
  /** Phases that should highlight this item as active. */
  matches: AppPhase[]
  isEnabled: (hasLeague: boolean, hasResult: boolean) => boolean
}

const LOTTERY_ITEMS: NavItem[] = [
  {
    label: 'Settings',
    phase: 'config',
    matches: ['config'],
    isEnabled: (hasLeague) => hasLeague,
  },
  {
    label: 'Simulation Test',
    phase: 'simulation',
    matches: ['simulation'],
    isEnabled: (hasLeague) => hasLeague,
  },
  {
    label: 'Lottery Board',
    phase: 'event',
    matches: ['event', 'results'],
    isEnabled: (_hasLeague, hasResult) => hasResult,
  },
]

export default function NavBar() {
  const phase = useAppStore((state) => state.phase)
  const hasLeague = useAppStore((state) => state.league !== null)
  const hasResult = useAppStore((state) => state.result !== null)
  const goToPhase = useAppStore((state) => state.goToPhase)

  function linkClasses(isActive: boolean, isEnabled: boolean): string {
    if (!isEnabled) {
      return 'cursor-not-allowed text-white/25'
    }
    return isActive
      ? 'cursor-pointer rounded-md bg-white/15 text-white'
      : 'cursor-pointer rounded-md text-white/60 hover:bg-white/10 hover:text-white'
  }

  return (
    <nav
      aria-label="Main navigation"
      className="flex flex-wrap items-center gap-x-1 gap-y-1 border-b border-white/10 bg-navy-dark px-2 py-2 text-sm sm:px-4"
    >
      <button
        type="button"
        className={`px-3 py-1.5 font-semibold whitespace-nowrap ${linkClasses(phase === 'setup' || phase === 'review', true)}`}
        onClick={() => goToPhase('setup')}
      >
        🏈 Home
      </button>
      <span className="mx-1 font-semibold tracking-wider text-white/40 uppercase sm:mx-2 sm:ml-4">
        Lottery
      </span>
      {LOTTERY_ITEMS.map((item) => {
        const isEnabled = item.isEnabled(hasLeague, hasResult)
        return (
          <button
            key={item.phase}
            type="button"
            disabled={!isEnabled}
            title={isEnabled ? undefined : 'Load a league first'}
            className={`px-3 py-1.5 whitespace-nowrap ${linkClasses(item.matches.includes(phase), isEnabled)}`}
            onClick={() => goToPhase(item.phase)}
          >
            {item.label}
          </button>
        )
      })}
    </nav>
  )
}
