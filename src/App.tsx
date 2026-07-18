import { useAppStore } from './state/store.ts'
import ErrorBoundary from './components/common/ErrorBoundary.tsx'
import NavBar from './components/common/NavBar.tsx'
import SetupScreen from './screens/SetupScreen.tsx'
import LeagueReviewScreen from './screens/LeagueReviewScreen.tsx'
import ConfigScreen from './screens/ConfigScreen.tsx'
import SimulationScreen from './screens/SimulationScreen.tsx'
import EventScreen from './screens/EventScreen.tsx'
import ResultsScreen from './screens/ResultsScreen.tsx'

function CurrentScreen() {
  const phase = useAppStore((state) => state.phase)

  switch (phase) {
    case 'setup':
      return <SetupScreen />
    case 'review':
      return <LeagueReviewScreen />
    case 'config':
      return <ConfigScreen />
    case 'simulation':
      return <SimulationScreen />
    case 'event':
      return <EventScreen />
    case 'results':
      return <ResultsScreen />
  }
}

export default function App() {
  return (
    <ErrorBoundary>
      <div className="flex min-h-screen flex-col overflow-x-clip bg-navy">
        <NavBar />
        <div className="flex flex-1 flex-col">
          <CurrentScreen />
        </div>
      </div>
    </ErrorBoundary>
  )
}
